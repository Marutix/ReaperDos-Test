# ReaperDos

Welcome to ReaperDos! This is a precompiled Windows executable (`reaperdos.exe`) designed for various network and Discord-related operations. Follow the instructions below to set it up and run it on your Windows PC.

## Prerequisites

- **Operating System**: Windows 7, 8, 10, or 11.
- **Python Version**: The executable is bundled with Python 3.9 and all required dependencies, so no separate Python installation is needed.
- **Additional Software**: For packet analysis (option 16), Npcap or WinPcap may be required. Download from [Npcap](https://npcap.com/) if needed.

## Installation

### Step 1: Download the Executable Package
- Download the `ReaperDos-Test.zip` file from the official source (e.g., a trusted download link provided by the developer).

### Step 2: Extract and Prepare Files
- Extract the `ReaperDos-Test.zip` file to a directory of your choice.
- Ensure both `reaperdos.exe` and the included `GeoLite2-Country.mmdb` are in the same directory.
- **Free_Proxy_List.txt**: Create this file in the same directory as `reaperdos.exe` with a CSV format containing proxy data (e.g., `ip,port,protocols,latency,uptime` on each line, like `1.1.1.1,8080,http,100,99`). Use real, working proxies.

## Usage

1. **Run the Executable**:
   - Double-click `reaperdos.exe` to launch the program, or open Command Prompt, navigate to the directory containing `reaperdos.exe`, and run:
     ```bash
     reaperdos.exe
     ```

2. **Follow Prompts**:
   - Enter a valid license key in the format `xxxx-xxxx-xxxx-xxxx` when prompted. Obtain your key from the developer or the official source.
   - Use the menu to select options (1-17) and follow the on-screen instructions for targets, tokens, durations, etc.

## Features
- **DDoS Attacks**: Single, multi, and custom HTTP flood attacks.
- **Nuke Attacks**: Single, multi, and custom Discord server nukes.
- **Raider Attacks**: Single, multi, and custom Discord server raids.
- **Utilities**: IP lookup, port scanning, packet analysis, proxy speed test, geo-filtered attacks, and log viewing.

## Notes
- **Administrator Privileges**: Some features (e.g., packet analysis) may require running the executable as an administrator.
- **GeoLite2 Database**: The included `GeoLite2-Country.mmdb` is provided by MaxMind for geolocation features. It’s free for non-commercial use under MaxMind’s terms (see [MaxMind License](https://www.maxmind.com/en/geolite2/developers)). Update it manually from [MaxMind](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data) if needed.
- **Legal Disclaimer**: Use this tool responsibly and in compliance with all applicable laws and platform terms (e.g., Discord's Terms of Service).
- **Logs**: Check `logs/reaperdos.log` in the same directory for debugging information.
- **Support**: For issues or to obtain a license key, contact the developer through the official distribution channel.

---
*Last updated: September 14, 2025*

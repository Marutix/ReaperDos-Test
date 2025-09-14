# ReaperDos



Welcome to ReaperDos! This is a precompiled Windows executable (`reaperdos.exe`) designed for various network and Discord-related operations. Follow the instructions below to set it up and run it on your Windows PC.

## Prerequisites

- **Operating System**: Windows 7, 8, 10, or 11.
- **Python Version**: The executable is bundled with Python 3.9 and all required dependencies, so no separate Python installation is needed.

## Installation

### Step 1: Download the Executable
- Download the `reaperdos.exe` file from the official source (e.g., a trusted download link provided by the developer).

### Step 2: Prepare Required Files
- **GeoLite2-Country.mmdb**: Download the GeoIP2 database from [MaxMind](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data) and place it in the same directory as `reaperdos.exe`.
- **Free_Proxy_List.txt**: Create this file in the same directory as `reaperdos.exe` with a CSV format containing proxy data (e.g., `ip,port,protocols,latency,uptime` on each line, like `1.1.1.1,8080,http,100,99`). Use real, working proxies.

## Usage

1. **Run the Executable**:
   - Double-click `reaperdos.exe` to launch the program, or open Command Prompt, navigate to the directory containing `reaperdos.exe`, and run:
     ```bash
     reaperdos.exe
     ```

2. **Follow Prompts**:
   - Use the menu to select options (1-17) and follow the on-screen instructions for targets, tokens, durations, etc.

## Features
- **DDoS Attacks**: Single, multi, and custom HTTP flood attacks.
- **Nuke Attacks**: Single, multi, and custom Discord server nukes.
- **Raider Attacks**: Single, multi, and custom Discord server raids.
- **Utilities**: IP lookup, port scanning, packet analysis, proxy speed test, geo-filtered attacks, and log viewing.

## Notes
- **Administrator Privileges**: Some features (e.g., packet analysis) may require running the executable as an administrator.
- **Legal Disclaimer**: Use this tool responsibly and in compliance with all applicable laws and platform terms (e.g., Discord's Terms of Service).
- **Logs**: Check `logs/reaperdos.log` in the same directory for debugging information.
- **Support**: For issues, contact the developer through the official distribution channel.

---
*Last updated: September 14, 2025*

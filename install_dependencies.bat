@echo off
echo Installing ReaperDos dependencies...

:: Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed. Please install Python (https://www.python.org/downloads/) and ensure 'python' is in your PATH.
    pause
    exit /b 1
)

:: Install required Python packages
echo Installing Python packages...
python -m pip install --upgrade pip
python -m pip install requests aiohttp scapy colorama discord.py geoip2 aiohttp_socks

:: Create logs directory
if not exist "logs" mkdir logs
echo Logs directory created.

:: Download GeoIP2 database (replace with a valid URL or provide the file manually)
echo Downloading GeoIP2 database...
powershell -Command "Invoke-WebRequest -Uri 'https://example.com/GeoLite2-Country.mmdb' -OutFile 'GeoLite2-Country.mmdb'"
if %ERRORLEVEL% neq 0 (
    echo Warning: Failed to download GeoIP2 database. Please place 'GeoLite2-Country.mmdb' in the directory manually.
)

:: Copy reaperdos.py (assumes it's in the same folder)
copy reaperdos.py . >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to copy reaperdos.py. Ensure the file exists in the same directory.
    pause
    exit /b 1
)

echo Installation complete! Run reaperdos.py with 'python reaperdos.py'.
pause

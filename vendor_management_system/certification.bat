@echo off

REM Check if Chocolatey is installed
choco -v >nul 2>&1
if %errorlevel% neq 0 (
    echo Chocolatey is not installed. Installing Chocolatey...
    @powershell -NoProfile -ExecutionPolicy Bypass -Command ^
        "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    echo.
)

REM Install mkcert using Chocolatey
echo Installing mkcert...
choco install mkcert -y
echo.

REM Retrieve computer IP address
for /f "tokens=2 delims=:" %%f in ('ipconfig ^| findstr /c:"IPv4 Address"') do set COMPUTER_IP_ADDRESS=%%f

REM Create key.pem and cert.pem using mkcert
echo Creating key.pem and cert.pem...
mkcert -install
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1 %COMPUTER_IP_ADDRESS%
echo.

REM Trusting the generated certificate
echo Trusting the certificate...
mkcert -install
echo.

echo Setup completed successfully!
pause

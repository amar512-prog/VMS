@echo off

REM Get the computer's IP address
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4 Address"') do set IP_ADDRESS=%%i

REM Get the current folder absolute path
for %%I in ("%~dp0.") do set "current_folder=%%~fI"

REM Update the config.ini file
set "config_file=%current_folder%\config.ini"
set "new_base_path=%current_folder%"
set "new_web_gui_url=%ip_address%"

REM Create a temporary file to store the updated config.ini content
set "temp_file=%current_folder%\temp.ini"

REM Read the existing config.ini file and update the base_path value
(for /f "usebackq delims=" %%L in ("%config_file%") do (
  echo %%L | findstr /b /c:"base_path" >nul
  if not errorlevel 1 (
    echo base_path = %new_base_path%
  ) else (
    echo %%L | findstr /b /c:"web_gui_url" >nul
    if not errorlevel 1 (
        echo web_gui_url = %IP_ADDRESS%
    ) else (
        echo %%L | findstr /b /c:"[" >nul
        if not errorlevel 1 (
            echo.
        )
        echo %%L
    )
    
  )
  
)) >"%temp_file%"
REM Replace the original config.ini file with the updated content
move /y "%temp_file%" "%config_file%" >nul

echo Config.ini updated successfully!

:: Run.bat "manage.py runserver_plus"
:: Get port from config.ini
@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Initialize variables
set JSON=""
set CURRENT_SECTION=""
set PORT=

:: Read and process config.ini file
for /f "usebackq tokens=*" %%a in ("config.ini") do (
    set "line=%%a"
    :: Check if the line represents a section
    echo !line! | findstr /r /c:"^\[.*\]$" >nul
    if !ERRORLEVEL! EQU 0 (
        :: Extract section name
        set "section=!line:[=!"
        set "section=!section:]=!"
        set "section=!section: =!"
        set "section=!section: =_!"
        set "CURRENT_SECTION=!section!"
        set "JSON=!JSON!{ "!section!": {} }, "
    ) else (
        :: Check if the line represents a key-value pair
        echo !line! | findstr /r /c:"^[^=]*=.*$" >nul
        if !ERRORLEVEL! EQU 0 (
            :: Extract key and value
            for /f "tokens=1,2 delims==" %%b in ("!line!") do (
                set "key=%%b"
                set "value=%%c"
                :: Remove leading/trailing spaces from the key and value
                set "key=!key: =!"
                set "value=!value: =!"
                :: Append key-value pair to the JSON object
                set "JSON=!JSON!{ "!key!": "!value!" }, "
                
                :: Check if the key is 'port' and store its value in the PORT variable
                if /I "!key!"=="port" (
                    set "PORT=!value!"
                )
            )
        )
    )
)
echo [32m creating runpy.bat "manage.py runserver_plus %IP_ADDRESS%:%PORT% --cert-file cert.pem --key-file key.pem"... [0m
(echo python manage.py runserver_plus %IP_ADDRESS%:%PORT% --cert-file cert.pem --key-file key.pem) > runpy.bat
pause

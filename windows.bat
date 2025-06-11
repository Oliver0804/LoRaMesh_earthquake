@echo off
setlocal enabledelayedexpansion

set HOST=192.168.0.148
set PORT=5000
set API_URL=http://%HOST%:%PORT%/send
set CHANNEL=2
if "%~1"=="" (
    echo Error: Missing first argument.
    exit /b 1
)
if "%~2"=="" (
    echo Error: Missing second argument.
    exit /b 1
)

set ARG1=%~1
set ARG2=%~2
set MESSAGE=[LoRa Test]Earthquake Alert: Estimated Magnitude %ARG1%, ETA %ARG2% seconds
set LOGFILE=command_log.txt
set CURRENT_TIME=%date% %time%

echo Attempting to connect to %API_URL%... >> %LOGFILE%
echo [%CURRENT_TIME%] Sending API request with message: "%MESSAGE%" to channel %CHANNEL% >> %LOGFILE%

curl -s -X POST %API_URL% -H "Content-Type: application/json" -d "{\"message\": \"%MESSAGE%\", \"channel\": %CHANNEL%}"
if %ERRORLEVEL% neq 0 (
    echo API request failed >> %LOGFILE%
    exit /b %ERRORLEVEL%
)

echo API request sent successfully >> %LOGFILE%
echo. >> %LOGFILE%

@echo off
REM Start the server
start cmd /c "python manage.py runserver"

REM Wait for the server to start
:WAIT
timeout /t 1>nul
curl http://localhost:8000 >nul 2>&1
if errorlevel 1 goto WAIT

REM Open the browser
start "" http://localhost:8000
@echo off
title Aria - AI Travel Planner
color 0B
echo.
echo  =====================================================
echo    Aria - AI Travel Planner Agent  [IBM Granite]
echo  =====================================================
echo.

REM ── Kill any existing node process on port 3000 ──────────────────────────
echo  Checking for existing processes on port 3000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000 " ^| findstr "LISTENING"') do (
    echo  Found process %%a on port 3000. Stopping it...
    taskkill /PID %%a /F >nul 2>&1
)
timeout /t 1 /nobreak >nul

REM ── Check Node.js ─────────────────────────────────────────────────────────
where node >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Node.js not found!
    echo  Download from: https://nodejs.org
    pause
    exit /b 1
)
echo  Node.js found: OK

REM ── Install dependencies if missing ───────────────────────────────────────
if not exist "node_modules\express" (
    echo  Installing dependencies (first run only)...
    node "%ProgramFiles%\nodejs\node_modules\npm\bin\npm-cli.js" install
    if errorlevel 1 (
        echo  Install failed. Check your internet connection.
        pause
        exit /b 1
    )
)
echo  Dependencies: OK

REM ── Check .env ────────────────────────────────────────────────────────────
if not exist ".env" (
    echo.
    echo  WARNING: .env file not found!
    echo  Creating from .env.example...
    copy ".env.example" ".env" >nul
    echo  Please edit .env and add your real IBM credentials.
)
echo  Config: OK

REM ── Launch browser after 3 seconds ────────────────────────────────────────
echo.
echo  Starting server... Browser will open automatically.
echo  URL: http://localhost:3000
echo  Test: http://localhost:3000/api/test
echo  Press Ctrl+C to stop the server.
echo.
start "" /B cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:3000"

REM ── Start Node server ─────────────────────────────────────────────────────
node server.js

echo.
echo  Server stopped.
pause

@echo off
REM Video Splitter - Windows Installer and Runner
echo.
echo ================================================
echo          Video Splitter - Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Python... OK
echo.

REM Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg is not installed!
    echo.
    echo The app needs FFmpeg to work. Please install it:
    echo.
    echo Option 1: Download from https://ffmpeg.org/download.html
    echo Option 2: Use package manager like Chocolatey: choco install ffmpeg
    echo.
    echo After installing FFmpeg, run this script again.
    echo.
    pause
    exit /b 1
)

echo [2/3] Checking FFmpeg... OK
echo.

REM No packages needed for basic GUI
echo [3/3] Setup complete!
echo.
echo ================================================
echo          Starting Video Splitter...
echo ================================================
echo.

REM Run the application
python video_splitter_gui.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the application
    echo.
    pause
)

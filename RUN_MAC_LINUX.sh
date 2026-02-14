#!/bin/bash
# Video Splitter - macOS/Linux Installer and Runner

echo ""
echo "================================================"
echo "         Video Splitter - Setup"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed!"
    echo ""
    echo "Please install Python 3:"
    echo "  macOS: brew install python3"
    echo "  Ubuntu/Debian: sudo apt-get install python3"
    echo "  Fedora: sudo dnf install python3"
    echo ""
    exit 1
fi

echo "[1/3] Checking Python... OK"
echo ""

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "WARNING: FFmpeg is not installed!"
    echo ""
    echo "The app needs FFmpeg to work. Please install it:"
    echo ""
    echo "  macOS: brew install ffmpeg"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  Fedora: sudo dnf install ffmpeg"
    echo ""
    echo "After installing FFmpeg, run this script again."
    echo ""
    exit 1
fi

echo "[2/3] Checking FFmpeg... OK"
echo ""

# No packages needed for basic GUI
echo "[3/3] Setup complete!"
echo ""
echo "================================================"
echo "         Starting Video Splitter..."
echo "================================================"
echo ""

# Run the application
python3 video_splitter_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to start the application"
    echo ""
    read -p "Press Enter to continue..."
fi

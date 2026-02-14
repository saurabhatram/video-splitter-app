# 🎬 Video Splitter Desktop App

**A simple drag-and-drop desktop application to split videos into segments**

No command line needed! Just double-click and use.

![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)

---

## ✨ Features

- 🖱️ **Drag-and-drop interface** - No command line needed!
- ✂️ **Split videos into segments** - Customize duration (default: 30 minutes)
- 📁 **Batch processing** - Handle multiple videos at once
- 🏷️ **Smart naming** - Files named as `part1-video.mp4`, `part2-video.mp4`, etc.
- ⚡ **Ultra-fast** - Uses FFmpeg codec copy (no re-encoding)
- 🎯 **No quality loss** - Original quality preserved
- 💾 **All formats** - MP4, MOV, AVI, MKV, WebM, and more

---

## 📦 Installation

### Step 1: Install Requirements

#### Windows
1. **Install Python** (if not already installed)
   - Download from: https://www.python.org/downloads/
   - ⚠️ **Important:** Check "Add Python to PATH" during installation

2. **Install FFmpeg**
   - **Option A:** Download from https://ffmpeg.org/download.html
   - **Option B:** Use Chocolatey: `choco install ffmpeg`
   - Add FFmpeg to your system PATH

#### macOS
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and FFmpeg
brew install python3 ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3 ffmpeg
```

#### Linux (Fedora)
```bash
sudo dnf install python3 ffmpeg
```

### Step 2: Download the App

Download all files to a folder on your computer:
- `video_splitter_gui.py`
- `RUN_WINDOWS.bat` (Windows)
- `RUN_MAC_LINUX.sh` (macOS/Linux)

---

## 🚀 How to Use

### Windows
1. Double-click `RUN_WINDOWS.bat`
2. The app will check for requirements and open automatically

### macOS/Linux
1. Open Terminal in the folder
2. Run: `./RUN_MAC_LINUX.sh`
   - Or double-click `RUN_MAC_LINUX.sh` if your system allows it

### Alternative (All Platforms)
Just run the Python script directly:
```bash
python3 video_splitter_gui.py
```

---

## 📖 Using the App

1. **Launch the app** using one of the methods above

2. **Adjust settings** (optional)
   - Change segment duration (default: 30 minutes)
   - Choose output folder (default: `~/Videos/Split_Videos`)

3. **Add videos**
   - Click the blue area OR
   - Drag and drop video files into the app

4. **Click "Split Videos"**
   - The app will process all videos
   - Progress bar shows current status
   - Output folder opens automatically when complete

5. **Done!**
   - Your split videos are saved with names like:
     - `originalname-part1.mp4`
     - `originalname-part2.mp4`
     - `originalname-part3.mp4`

---

## 🎯 Example Use Cases

### Split a Long Recording
- **Input:** `meeting-2024.mp4` (2 hours)
- **Duration:** 30 minutes
- **Output:** 
  - `meeting-2024-part1.mp4`
  - `meeting-2024-part2.mp4`
  - `meeting-2024-part3.mp4`
  - `meeting-2024-part4.mp4`

### Split Multiple Lectures
- **Input:** 
  - `lecture1.mp4` (90 min)
  - `lecture2.mp4` (75 min)
  - `lecture3.mp4` (60 min)
- **Duration:** 15 minutes
- **Output:** Multiple parts for each lecture

---

## ⚙️ How It Works

The app uses **FFmpeg** to split videos at keyframes without re-encoding:

- ⚡ **Ultra-fast** - Splits in seconds, not minutes
- 🎯 **No quality loss** - Original quality preserved
- 📦 **No size overhead** - Output size ≈ input size

**Note:** Segments may be slightly longer/shorter than exact duration since splits occur at the nearest keyframe.

---

## ❓ Troubleshooting

### "Python is not installed"
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" (Windows)

### "FFmpeg is not installed"
- **Windows:** Download from https://ffmpeg.org/ or use `choco install ffmpeg`
- **macOS:** Run `brew install ffmpeg`
- **Linux:** Run `sudo apt-get install ffmpeg` (Ubuntu/Debian)

### "Error processing video"
- Make sure the video file is not corrupted
- Check that FFmpeg is properly installed
- Try with a different video format

### App window doesn't open
- Open Terminal/Command Prompt in the folder
- Run: `python3 video_splitter_gui.py` (or `python` on Windows)
- Check the error message

### "Permission denied" (macOS/Linux)
```bash
chmod +x RUN_MAC_LINUX.sh
./RUN_MAC_LINUX.sh
```

---

## 🎨 App Features

### Simple Interface
- Clean, modern design
- Easy-to-understand controls
- Real-time progress updates

### Smart Defaults
- 30-minute segments (adjustable)
- Saves to `~/Videos/Split_Videos`
- Supports all common video formats

### Batch Processing
- Process multiple videos at once
- Automatic file naming
- Opens output folder when done

---

## 💻 Technical Details

- **Language:** Python 3
- **GUI Framework:** Tkinter (built into Python)
- **Video Processing:** FFmpeg
- **Split Method:** Codec copy (no re-encoding)
- **Supported Formats:** All FFmpeg-supported formats

---

## 📝 System Requirements

- **Operating System:** Windows 10+, macOS 10.13+, or Linux
- **Python:** 3.6 or higher
- **FFmpeg:** Latest version
- **Disk Space:** Enough for output files (≈ same size as input)

---

## 🆘 Need Help?

If you encounter any issues:

1. Make sure Python and FFmpeg are properly installed
2. Check that you're running the latest version
3. Try with a simple MP4 video first
4. Check the Terminal/Command Prompt for error messages

---

## 📄 License

MIT License - Free to use and modify!

---

## 🌟 Tips

- **Best format:** MP4 files work best
- **Save space:** Total output size ≈ input size (no overhead)
- **Speed:** Process multiple videos for efficiency
- **Quality:** Original quality is always preserved

---

Made with ❤️ using Python and FFmpeg, Claude

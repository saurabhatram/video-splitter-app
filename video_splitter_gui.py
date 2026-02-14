#!/usr/bin/env python3
"""
Video Splitter - Desktop Application
A simple drag-and-drop desktop app to split videos into segments
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import json
import threading
from pathlib import Path
import os

class VideoSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Video Splitter")
        # Increase initial height so bottom controls remain visible when not maximized
        self.root.geometry("800x820")
        self.root.configure(bg='#f0f0f0')
        
        # Make window resizable but set a slightly larger minimum size
        self.root.minsize(780, 720)
        
        self.videos = []
        self.output_dir = str(Path.home() / "Videos" / "Split_Videos")
        self.is_processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🎬 Video Splitter",
            font=("Arial", 28, "bold"),
            bg='#f0f0f0',
            fg='#667eea'
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Split your videos into segments easily",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#666'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Settings Frame
        settings_frame = tk.LabelFrame(
            main_frame,
            text="Settings",
            font=("Arial", 11, "bold"),
            bg='white',
            fg='#333',
            padx=15,
            pady=15
        )
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Duration setting
        duration_frame = tk.Frame(settings_frame, bg='white')
        duration_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            duration_frame,
            text="Segment Duration (minutes):",
            font=("Arial", 10),
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.duration_var = tk.IntVar(value=30)
        duration_spinbox = tk.Spinbox(
            duration_frame,
            from_=1,
            to=120,
            textvariable=self.duration_var,
            width=10,
            font=("Arial", 10)
        )
        duration_spinbox.pack(side=tk.LEFT)
        
        # Output directory setting
        output_frame = tk.Frame(settings_frame, bg='white')
        output_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            output_frame,
            text="Output Folder:",
            font=("Arial", 10),
            bg='white'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.output_label = tk.Label(
            output_frame,
            text=self.output_dir,
            font=("Arial", 9),
            bg='white',
            fg='#667eea',
            cursor="hand2"
        )
        self.output_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        change_btn = tk.Button(
            output_frame,
            text="Change",
            command=self.change_output_dir,
            bg='#667eea',
            fg='white',
            font=("Arial", 9),
            padx=15,
            pady=3,
            relief=tk.FLAT,
            cursor="hand2"
        )
        change_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Drop zone
        self.drop_frame = tk.Frame(
            main_frame,
            bg='#e8eaff',
            relief=tk.SOLID,
            borderwidth=2,
            highlightbackground='#667eea',
            highlightthickness=2
        )
        # Use a fixed-ish height so the bottom controls remain visible
        self.drop_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 15))
        self.drop_frame.config(height=220)
        self.drop_frame.pack_propagate(False)
        
        # Drop zone content
        drop_content = tk.Frame(self.drop_frame, bg='#e8eaff')
        # Use pack with padding so inner content stays inside the outer container
        drop_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            drop_content,
            text="📹",
            font=("Arial", 48),
            bg='#e8eaff'
        ).pack()
        
        tk.Label(
            drop_content,
            text="Click to select videos or drag & drop here",
            font=("Arial", 12, "bold"),
            bg='#e8eaff',
            fg='#667eea',
            wraplength=600,
            justify=tk.CENTER
        ).pack(pady=(10, 5))
        
        tk.Label(
            drop_content,
            text="Supports all video formats",
            font=("Arial", 9),
            bg='#e8eaff',
            fg='#999'
        ).pack()
        
        # Make drop zone clickable
        self.drop_frame.bind("<Button-1>", lambda e: self.select_videos())
        for child in drop_content.winfo_children():
            child.bind("<Button-1>", lambda e: self.select_videos())
        
        # Video list frame
        list_frame = tk.LabelFrame(
            main_frame,
            text="Selected Videos",
            font=("Arial", 11, "bold"),
            bg='white',
            fg='#333',
            padx=10,
            pady=10
        )
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Scrollable list
        list_container = tk.Frame(list_frame, bg='white')
        list_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.video_listbox = tk.Listbox(
            list_container,
            font=("Arial", 10),
            bg='white',
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            height=6
        )
        self.video_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.video_listbox.yview)
        
        # List buttons
        list_btn_frame = tk.Frame(list_frame, bg='white')
        list_btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        remove_btn = tk.Button(
            list_btn_frame,
            text="Remove Selected",
            command=self.remove_selected,
            bg='#ff4757',
            fg='white',
            font=("Arial", 9),
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        remove_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = tk.Button(
            list_btn_frame,
            text="Clear All",
            command=self.clear_all,
            bg='#ff6b81',
            fg='white',
            font=("Arial", 9),
            padx=15,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_frame = tk.Frame(main_frame, bg='#f0f0f0')
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Arial", 9),
            bg='#f0f0f0',
            fg='#666'
        )
        self.progress_label.pack()
        
        self.progress_frame.pack_forget()  # Hide initially
        
        # Split button (styled)
        split_outer = tk.Frame(main_frame, bg='#f0f0f0')
        split_outer.pack(fill=tk.X)

        split_container = tk.Frame(split_outer, bg='#f0f0f0')
        split_container.pack(pady=(10, 0))

        self.split_btn = tk.Button(
            split_container,
            text="Split Videos",
            command=self.start_splitting,
            bg='#667eea',
            fg='white',
            font=("Arial", 14, "bold"),
            padx=28,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            bd=0,
            activebackground='#5563d6',
            disabledforeground='#dfe3ff'
        )
        # Center the button and give it a fixed max width look
        self.split_btn.pack()

        # Hover effects
        self.split_btn.bind('<Enter>', self._on_split_enter)
        self.split_btn.bind('<Leave>', self._on_split_leave)
        
    def select_videos(self):
        files = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm *.m4v"),
                ("All files", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.videos:
                self.videos.append(file)
                filename = Path(file).name
                size = Path(file).stat().st_size / (1024 * 1024)
                self.video_listbox.insert(tk.END, f"{filename} ({size:.1f} MB)")
        
        self.update_split_button()
    
    def remove_selected(self):
        selection = self.video_listbox.curselection()
        if selection:
            index = selection[0]
            self.videos.pop(index)
            self.video_listbox.delete(index)
            self.update_split_button()
    
    def clear_all(self):
        self.videos.clear()
        self.video_listbox.delete(0, tk.END)
        self.update_split_button()
    
    def change_output_dir(self):
        directory = filedialog.askdirectory(
            title="Select Output Folder",
            initialdir=self.output_dir
        )
        if directory:
            self.output_dir = directory
            self.output_label.config(text=directory)
    
    def update_split_button(self):
        if self.videos and not self.is_processing:
            self.split_btn.config(state=tk.NORMAL, bg='#667eea', fg='white')
        else:
            self.split_btn.config(state=tk.DISABLED, bg='#b7bbf7', fg='#ffffff')

    def _on_split_enter(self, event):
        try:
            if self.split_btn['state'] == tk.NORMAL:
                self.split_btn.config(bg='#5563d6')
        except tk.TclError:
            pass

    def _on_split_leave(self, event):
        try:
            if self.split_btn['state'] == tk.NORMAL:
                self.split_btn.config(bg='#667eea')
        except tk.TclError:
            pass
    
    def update_progress(self, percent, text):
        self.progress_var.set(percent)
        self.progress_label.config(text=text)
        self.root.update_idletasks()
    
    def get_video_duration(self, video_path):
        """Get video duration using ffprobe"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'json',
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            return float(data['format']['duration'])
        except:
            return 0
    
    def split_video(self, input_path, output_dir, segment_duration_minutes):
        """Split a single video"""
        input_path = Path(input_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        total_duration = self.get_video_duration(str(input_path))
        if total_duration == 0:
            return []
        
        segment_duration_seconds = segment_duration_minutes * 60
        num_segments = int(total_duration / segment_duration_seconds) + (
            1 if total_duration % segment_duration_seconds > 0 else 0
        )
        
        base_name = input_path.stem
        extension = input_path.suffix
        
        output_files = []
        
        for i in range(num_segments):
            start_time = i * segment_duration_seconds
            output_name = f"{base_name}--part{i + 1}{extension}"
            output_path = output_dir / output_name
            
            cmd = [
                'ffmpeg',
                '-i', str(input_path),
                '-ss', str(start_time),
                '-t', str(segment_duration_seconds),
                '-c', 'copy',
                '-avoid_negative_ts', 'make_zero',
                '-y',
                str(output_path)
            ]
            
            try:
                subprocess.run(cmd, capture_output=True, check=True)
                output_files.append(output_path)
            except subprocess.CalledProcessError as e:
                print(f"Error splitting segment {i+1}: {e}")
        
        return output_files
    
    def process_videos(self):
        """Process all videos in a separate thread"""
        self.is_processing = True
        self.split_btn.config(state=tk.DISABLED)
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        duration = self.duration_var.get()
        total_videos = len(self.videos)
        all_segments = []
        
        try:
            for idx, video in enumerate(self.videos):
                video_name = Path(video).name
                self.update_progress(
                    (idx / total_videos) * 100,
                    f"Processing {idx + 1}/{total_videos}: {video_name}"
                )
                
                segments = self.split_video(video, self.output_dir, duration)
                all_segments.extend(segments)
            
            self.update_progress(100, "Complete!")
            
            # Show success message
            self.root.after(100, lambda: messagebox.showinfo(
                "Success!",
                f"✅ Successfully created {len(all_segments)} video segments!\n\n"
                f"📁 Saved to:\n{self.output_dir}\n\n"
                f"Click OK to open the folder."
            ))
            
            # Open output folder
            if os.name == 'nt':  # Windows
                os.startfile(self.output_dir)
            elif os.name == 'posix':  # macOS and Linux
                subprocess.run(['xdg-open', self.output_dir])
            
        except Exception as e:
            self.root.after(100, lambda: messagebox.showerror(
                "Error",
                f"An error occurred:\n{str(e)}\n\n"
                f"Make sure FFmpeg is installed on your system."
            ))
        
        finally:
            self.is_processing = False
            self.progress_frame.pack_forget()
            self.update_split_button()
    
    def start_splitting(self):
        """Start the splitting process in a background thread"""
        if not self.videos:
            return
        
        # Check if FFmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showerror(
                "FFmpeg Not Found",
                "FFmpeg is not installed or not in your system PATH.\n\n"
                "Please install FFmpeg:\n"
                "• Windows: Download from ffmpeg.org\n"
                "• macOS: brew install ffmpeg\n"
                "• Linux: sudo apt-get install ffmpeg"
            )
            return
        
        # Start processing in background thread
        thread = threading.Thread(target=self.process_videos, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    app = VideoSplitterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

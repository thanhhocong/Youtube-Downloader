import yt_dlp
import json
import sys
import shutil

def check_dependencies():
    """Check if required dependencies are available"""
    ffmpeg_available = shutil.which('ffmpeg') is not None
    return ffmpeg_available

def download_full_hd(video_url, output_path='./video'):
    """
    Downloads a YouTube video in the best quality available (including full HD)
    using yt-dlp. Requires FFmpeg to be installed and in the system's PATH.
    """
    # Check if ffmpeg is available
    if not check_dependencies():
        print("ERROR: FFmpeg is not installed. Installing now...")
        return False
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'progress_hooks': [progress_hook],
        'quiet': False,
        'no_warnings': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"\nDownload complete: {video_url}")
        return True
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return False

def progress_hook(d):
    """
    Optional: A simple hook to print download progress.
    """
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"Downloading: {percent} at {speed} ETA: {eta}", end='\r')
    elif d['status'] == 'finished':
        print("\nFinished downloading, starting post-processing (merging)...")

if __name__ == "__main__":
    video_url = "https://youtube.com/EDIT_YOUR_LINK"
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs('./video', exist_ok=True)
    
    download_full_hd(video_url)
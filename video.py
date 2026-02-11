import yt_dlp
import os
import shutil
import sys

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
        print("ERROR: FFmpeg is not installed. Please install FFmpeg first.")
        print("Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("macOS: brew install ffmpeg")
        print("Windows: Download from https://ffmpeg.org/download.html")
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
            info = ydl.extract_info(video_url, download=True)
            video_title = info.get('title', 'Unknown')
            
        print(f"\n✓ Download complete!")
        print(f"✓ Video: {video_title}")
        return True
        
    except Exception as e:
        print(f"\n✗ Download failed: {e}")
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
        print("\n✓ Download finished, processing...")

def main():
    """Main function with input loop"""
    print("=" * 60)
    print("YouTube Video Downloader (Full HD)")
    print("=" * 60)
    
    # Create output directory if it doesn't exist
    os.makedirs('./video', exist_ok=True)
    
    while True:
        print("\n" + "-" * 60)
        video_url = input("Enter YouTube URL (or 'q' to quit): ").strip()
        
        # Check if user wants to quit
        if video_url.lower() in ['q', 'quit', 'exit']:
            print("\nGoodbye! 👋")
            break
        
        # Check if input is empty
        if not video_url:
            print("⚠️  Please enter a valid URL")
            continue
        
        # Check if URL looks like a YouTube URL
        if 'youtube.com' not in video_url and 'youtu.be' not in video_url:
            print("⚠️  This doesn't look like a YouTube URL")
            retry = input("Try anyway? (y/n): ").strip().lower()
            if retry != 'y':
                continue
        
        print(f"\n🎬 Processing: {video_url}")
        print("-" * 60)
        
        # Try to download
        success = download_full_hd(video_url)
        
        if success:
            print("\n✅ Success! Video saved to ./video/")
            
            # Ask if user wants to download another
            another = input("\nDownload another video? (y/n): ").strip().lower()
            if another != 'y':
                print("\nGoodbye! 👋")
                break
        else:
            print("\n❌ Failed to download video")
            print("This could be due to:")
            print("  - Invalid URL")
            print("  - Private/restricted video")
            print("  - Network issues")
            print("  - Video no longer available")
            
            # Ask if user wants to retry or enter new URL
            retry = input("\nTry another URL? (y/n): ").strip().lower()
            if retry != 'y':
                print("\nGoodbye! 👋")
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Goodbye! 👋")
        sys.exit(0)
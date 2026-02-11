import yt_dlp
import os
import shutil

def check_dependencies():
    """Check if required dependencies are available"""
    ffmpeg_available = shutil.which('ffmpeg') is not None
    return ffmpeg_available

def download_audio_wav(video_url, output_path='./audio'):
    """
    Downloads YouTube video audio and converts it to WAV format.
    Requires FFmpeg to be installed and in the system's PATH.
    
    Args:
        video_url: YouTube video URL
        output_path: Directory to save the audio file
    """
    # Check if ffmpeg is available
    if not check_dependencies():
        print("ERROR: FFmpeg is not installed. Please install FFmpeg first.")
        print("Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("macOS: brew install ffmpeg")
        print("Windows: Download from https://ffmpeg.org/download.html")
        return False
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',  # Download best quality audio
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Output template
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extract audio
            'preferredcodec': 'wav',  # Convert to WAV
            'preferredquality': '0',  # Best quality (0 = best for WAV)
        }],
        'noplaylist': True,  # Only download single video
        'progress_hooks': [progress_hook],  # Progress display
        'quiet': False,
        'no_warnings': False,
    }

    try:
        print(f"Downloading audio from: {video_url}")
        print(f"Output directory: {output_path}")
        print("-" * 50)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            # Replace extension with .wav
            wav_filename = os.path.splitext(filename)[0] + '.wav'
            
        print(f"\n✓ Download complete!")
        print(f"✓ Saved as: {wav_filename}")
        return True
        
    except Exception as e:
        print(f"\n✗ An error occurred: {e}")
        return False

def progress_hook(d):
    """
    Display download progress.
    """
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        print(f"Downloading: {percent} at {speed} ETA: {eta}", end='\r')
    elif d['status'] == 'finished':
        print("\n✓ Download finished, converting to WAV format...")

if __name__ == "__main__":
    # Example usage - replace with your YouTube URL
    video_url = "https://youtu.be/X7sSE3yCNLI?si=ERtFtWV-vTxqP3Xd"
    
    # Download audio as WAV
    download_audio_wav(video_url, output_path='./audio')
    
    # You can also download multiple videos:
    # urls = [
    #     "https://youtube.com/watch?v=VIDEO_ID_1",
    #     "https://youtube.com/watch?v=VIDEO_ID_2",
    # ]
    # for url in urls:
    #     download_audio_wav(url)
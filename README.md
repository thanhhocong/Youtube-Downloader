# YouTube Downloader - Complete Guide

Download YouTube videos and audio with yt-dlp and FFmpeg.

## 📦 What's Included

- `video.py` - Download videos in MP4 format (up to Full HD)
- `audio.py` - Download audio in WAV format (or other formats)

## 🚀 Quick Start

### Install Dependencies

**1. Install Python packages:**
```bash
pip install python
```
```bash
pip install yt-dlp
```

**2. Install FFmpeg (Required):**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
```bash
winget install "FFmpeg (Essentials Build)"
```
or run the FFMPEG.ps1 file that include in the repo

### Run the Scripts
**Customize the video URL and the destination folder (Initially the code will create folders inside the repo folder):**
```python
video_url = "YOUR_YOUTUBE_URL_HERE"
download_full_hd(video_url, output_path='YOUR_DESTINATION_FOLDER_HERE')
```
**Download Video:**
```bash
python video.py
```

**Download Audio:**
```bash
python audio.py
```

## 📹 Video Downloader (`ytbdl.py`)

Downloads YouTube videos in the best quality available (including Full HD).

### Features

✅ Best available video quality (up to 1080p+)  
✅ Automatically merges video and audio streams  
✅ MP4 format for universal compatibility  
✅ Progress display with speed and ETA  
✅ Dependency checking  

### Basic Usage

```python
from ytbdl import download_full_hd

video_url = "https://youtube.com/watch?v=VIDEO_ID"
download_full_hd(video_url)
```

### Custom Output Directory

```python
download_full_hd(video_url, output_path='./downloads')
```

### Video Format Options

The default format prioritizes quality:
```python
'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
```

**Specific resolution (1080p max):**
```python
'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best'
```

**Specific resolution (720p):**
```python
'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best'
```

**File size limit (under 500MB):**
```python
'bestvideo[filesize<500M][ext=mp4]+bestaudio[ext=m4a]/best'
```

**4K if available:**
```python
'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best'
```

## 🎵 Audio Downloader (`ytbdl_audio.py`)

Downloads YouTube audio and converts to WAV or other formats.

### Features

✅ Downloads best available audio quality  
✅ Automatically converts to WAV format  
✅ Progress display with ETA  
✅ Error handling and dependency checking  

### Basic Usage

```python
from ytbdl_audio import download_audio_wav

video_url = "https://youtube.com/watch?v=VIDEO_ID"
download_audio_wav(video_url)
```

### Custom Output Directory

```python
download_audio_wav(video_url, output_path='./my_music')
```

### Download Multiple Files

```python
urls = [
    "https://youtube.com/watch?v=VIDEO_ID_1",
    "https://youtube.com/watch?v=VIDEO_ID_2",
    "https://youtube.com/watch?v=VIDEO_ID_3",
]

for url in urls:
    download_audio_wav(url)
```

## 🎼 Audio Format Options

### WAV (Default - Lossless, Large)
```python
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'wav',
    'preferredquality': '0',
}],
```

### MP3 (Smaller file size)
```python
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '320',  # 320 kbps = highest MP3 quality
}],
```

### FLAC (Lossless compression)
```python
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'flac',
    'preferredquality': '0',
}],
```

### M4A/AAC (Good quality, smaller than WAV)
```python
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'm4a',
    'preferredquality': '256',
}],
```

### OGG Vorbis
```python
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'vorbis',
    'preferredquality': '9',  # 0-10, higher = better
}],
```

## 📊 Audio Format Comparison

| Format | Quality | File Size | Compatibility | Best For |
|--------|---------|-----------|---------------|----------|
| **WAV** | Lossless | Very Large (~50MB/5min) | Universal | Audio editing, professional work |
| **FLAC** | Lossless | Large (~25MB/5min) | Most players | Archiving, audiophile |
| **MP3 320** | Very High | Small (~12MB/5min) | Universal | General listening, portable devices |
| **M4A 256** | Very High | Small (~9MB/5min) | Most devices | Apple devices, streaming |
| **OGG** | High | Small (~8MB/5min) | Modern players | Web streaming, gaming |

## 🔧 Advanced Options

### Custom Audio Sample Rate

```python
'postprocessor_args': [
    '-ar', '48000',  # 48kHz sample rate
    '-ac', '2',      # Stereo (2 channels)
],
```

**Common sample rates:**
- `44100` - CD quality (standard)
- `48000` - Professional audio
- `96000` - High-resolution audio

### Download Playlist

```python
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
    'outtmpl': f'{output_path}/%(playlist_index)s - %(title)s.%(ext)s',
    'noplaylist': False,  # Enable playlist download
}
```

### Download Age-Restricted Videos

```python
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
    'age_limit': None,
    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
}
```

## 🐛 Troubleshooting

### FFmpeg Not Found
```
ERROR: FFmpeg is not installed
```
**Solution:** Install FFmpeg and ensure it's in your system PATH

### No Formats Found
```
ERROR: No formats found
```
**Solutions:**
- Video may be private or restricted
- Try adding: `'extractor_args': {'youtube': {'player_client': ['android']}}`
- Check if video is still available

### JavaScript Runtime Warning
```
WARNING: No supported JavaScript runtime could be found
```
**Solution (Optional):** Install Deno for better format support
```bash
# Linux/macOS
curl -fsSL https://deno.land/install.sh | sh

# Windows (PowerShell)
irm https://deno.land/install.ps1 | iex
```

### Merging Failed
```
ERROR: Requested merging of multiple formats but ffmpeg is not installed
```
**Solution:** Install FFmpeg (see installation section above)

### Postprocessing Failed
```
ERROR: Postprocessing failed
```
**Solutions:**
- Update FFmpeg to latest version
- Check available disk space
- Verify write permissions in output directory

### Slow Downloads
**Possible causes:**
- Network congestion
- YouTube throttling
- Peak usage hours

**Solutions:**
- Try during off-peak hours
- Check your internet connection
- Some throttling is normal

### Permission Errors
**Solution:** Ensure write permissions for output directory
```bash
chmod 755 ./video
chmod 755 ./audio
```

## 💡 Tips & Best Practices

### File Size Considerations

⚠️ **WAV files are very large!** A 10-minute video = ~100MB  
💡 For music listening, use MP3 320kbps or M4A 256kbps for great quality with smaller files  
🎵 Use WAV only for audio editing or when you need absolute source quality  

### Video Quality

- YouTube's max quality varies by video (480p, 720p, 1080p, 4K)
- The script automatically downloads the best available
- Premium videos may require authentication

### Audio Quality

- YouTube's max audio quality is typically ~160kbps (opus/aac)
- Converting to WAV won't improve quality beyond the source
- WAV just stores it without compression

### Batch Processing

For downloading multiple videos/audio files efficiently:

```python
import time

urls = ["url1", "url2", "url3"]

for i, url in enumerate(urls, 1):
    print(f"\n[{i}/{len(urls)}] Processing...")
    download_full_hd(url)  # or download_audio_wav(url)
    time.sleep(2)  # Be nice to YouTube servers
```

## 📝 Notes

- **Respect copyright**: Only download content you have permission to download
- **Rate limiting**: Don't download too many videos too quickly
- **Storage**: Monitor disk space, especially when downloading in WAV
- **Updates**: Keep yt-dlp updated: `pip install -U yt-dlp`

## 🔄 Keeping yt-dlp Updated

YouTube frequently changes their API. Keep yt-dlp updated to avoid issues:

```bash
pip install --upgrade yt-dlp
```

## 📄 License & Disclaimer

These scripts are for personal use. Respect copyright laws and YouTube's Terms of Service. The authors are not responsible for misuse of these tools.

## 🆘 Need Help?

If you encounter issues:
1. Check this troubleshooting section
2. Update yt-dlp: `pip install -U yt-dlp`
3. Verify FFmpeg is installed: `ffmpeg -version`
4. Check yt-dlp GitHub issues: https://github.com/yt-dlp/yt-dlp/issues

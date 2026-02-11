# YouTube Downloader - Complete Guide

<<<<<<< HEAD
Download YouTube videos and audio with interactive command-line interface.

## 📦 What's Included

- **`ytbdl.py`** - Download videos in MP4 format (up to Full HD)
- **`ytbdl_audio.py`** - Download audio in WAV format (or other formats)

## 🚀 Quick Start

### 1. Install Python Package

=======
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
>>>>>>> 4ab9807261b3525d0b2a96e4cd3c6acb80667529
```bash
pip install yt-dlp
```

<<<<<<< HEAD
### 2. Install FFmpeg (Required)
=======
**2. Install FFmpeg (Required):**
>>>>>>> 4ab9807261b3525d0b2a96e4cd3c6acb80667529

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
<<<<<<< HEAD

Or run the `FFMPEG.ps1` script included.

### 3. Run the Scripts

**Download Video:**
```bash
python ytbdl.py
```

**Download Audio (WAV):**
```bash
python ytbdl_audio.py
```

That's it! Just paste YouTube URLs when prompted.

## 🎯 How to Use

Both scripts are **fully interactive** - no need to edit code!

### Video Downloader Example

```
============================================================
YouTube Video Downloader (Full HD)
============================================================

------------------------------------------------------------
Enter YouTube URL (or 'q' to quit): https://youtube.com/watch?v=dQw4w9WgXcQ

🎬 Processing: https://youtube.com/watch?v=dQw4w9WgXcQ
------------------------------------------------------------
Downloading: 100% at 2.5MB/s ETA: 00:00
✓ Download finished, processing...

✓ Download complete!
✓ Video: Rick Astley - Never Gonna Give You Up

✅ Success! Video saved to ./video/

Download another video? (y/n): 
```

### Audio Downloader Example

```
============================================================
YouTube Audio Downloader (WAV Format)
============================================================
⚠️  Note: WAV files are large (~50MB per 5min)

------------------------------------------------------------
Enter YouTube URL (or 'q' to quit): https://youtube.com/watch?v=dQw4w9WgXcQ

🎵 Processing: https://youtube.com/watch?v=dQw4w9WgXcQ
------------------------------------------------------------
Downloading: 100% at 1.2MB/s ETA: 00:00
✓ Download finished, converting to WAV format...

✓ Download complete!
✓ Audio: Rick Astley - Never Gonna Give You Up
✓ Saved as: ./audio/Rick Astley - Never Gonna Give You Up.wav

✅ Success! Audio saved to ./audio/

Download another audio? (y/n):
```

## ✨ Features

### ✅ Interactive Input
- No need to edit code
- Just run and paste YouTube links
- Download multiple files in one session

### 🔁 Automatic Retry Loop
- If download fails, try another URL immediately
- No need to restart the program
- Clear error messages explain what went wrong

### 🛡️ URL Validation
- Checks if URL looks like a YouTube link
- Warns you if it doesn't match expected format
- Lets you try anyway if you want

### 🎯 Smart Error Handling
- Shows why download might have failed
- Asks if you want to try another URL
- Press Ctrl+C anytime to quit safely

### 📁 Auto-Created Directories
- `./video/` - For downloaded videos
- `./audio/` - For downloaded audio files
- Created automatically on first run

## 🎮 Commands

While running the scripts:
- **Enter URL** - Download that video/audio
- **q** (or 'quit', 'exit') - Exit the program
- **Ctrl+C** - Force quit anytime
- **y** - Yes (continue/retry)
- **n** - No (quit)

## 🔧 Advanced Configuration

### Video Format Options

To change video quality, modify the `format` option in `ytbdl.py`:

**Current default (best quality):**
```python
'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
```

**Specific resolution (1080p max):**
```python
'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best'
```

**Specific resolution (720p):**
```python
'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best'
```

**File size limit (under 500MB):**
```python
'format': 'bestvideo[filesize<500M][ext=mp4]+bestaudio[ext=m4a]/best'
```

**4K if available:**
```python
'format': 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best'
```

### Audio Format Options

To change audio format, modify the `postprocessors` section in `ytbdl_audio.py`:

**MP3 (smaller file size):**
```python
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '320',  # 320 kbps = highest MP3 quality
}],
```

**FLAC (lossless compression):**
```python
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'flac',
    'preferredquality': '0',
}],
```

**M4A/AAC (good quality, smaller than WAV):**
```python
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'm4a',
    'preferredquality': '256',
}],
```

### Audio Format Comparison

| Format | Quality | File Size (5min) | Compatibility | Best For |
|--------|---------|------------------|---------------|----------|
| **WAV** | Lossless | ~50MB | Universal | Audio editing, professional work |
| **FLAC** | Lossless | ~25MB | Most players | Archiving, audiophile |
| **MP3 320** | Very High | ~12MB | Universal | General listening, portable devices |
| **M4A 256** | Very High | ~9MB | Most devices | Apple devices, streaming |

### Custom Output Path

Both scripts support custom output directories:

**In code:**
```python
# For videos
download_full_hd(video_url, output_path='./my_videos')

# For audio
download_audio_wav(video_url, output_path='./my_music')
```

**Or modify the default in the script:**
```python
os.makedirs('./downloads', exist_ok=True)  # Change './video' to './downloads'
```

## 🐛 Troubleshooting

### "FFmpeg is not installed"
**Solution:** Install FFmpeg using the commands above, then ensure it's in your system PATH.

**Verify installation:**
```bash
ffmpeg -version
```

### "No formats found" / "Video unavailable"
**Possible causes:**
- Video is private or restricted
- Video has been removed
- Age-restricted content
- Geographic restrictions

**Solutions:**
- Verify the URL is correct and video is public
- Try adding this to `ydl_opts` in the script:
```python
'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
```

### JavaScript Runtime Warning
```
WARNING: No supported JavaScript runtime could be found
```

**This is optional** - most videos download fine without it.

**To fix (for better format support):**
=======
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
>>>>>>> 4ab9807261b3525d0b2a96e4cd3c6acb80667529

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

<<<<<<< HEAD
### "Requested format not available"
**Solution:** Video doesn't have MP4 format. Remove `[ext=mp4]` from the format string:
```python
'format': 'bestvideo+bestaudio/best'
```
=======
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
>>>>>>> 4ab9807261b3525d0b2a96e4cd3c6acb80667529

### Slow Downloads
**Possible causes:**
- Network congestion
- YouTube throttling
- Peak usage hours

**Solutions:**
<<<<<<< HEAD
- Check your internet connection
- Try during off-peak hours
- Some throttling is normal and expected

### Permission Errors
**Solution:** Ensure write permissions for output directory:
```bash
# Linux/macOS
chmod 755 ./video
chmod 755 ./audio

# Windows - Run as Administrator or check folder permissions
```

### "Please enter a valid URL"
**Cause:** You pressed Enter without typing anything.

**Solution:** Paste a YouTube URL and press Enter.

### "This doesn't look like a YouTube URL"
**Cause:** URL doesn't contain 'youtube.com' or 'youtu.be'

**Solution:** 
- Check you copied the correct URL
- Type 'y' to try anyway (for URL shorteners)
- Type 'n' to enter a different URL

### Download Keeps Failing on Same Video
**Try these steps:**
1. Verify the video plays in your browser
2. Check if video is age-restricted or region-locked
3. Update yt-dlp: `pip install -U yt-dlp`
4. Try a different video to test if issue is specific
5. Check internet connection stability

## 💡 Tips & Best Practices

### File Size Considerations
- **WAV files are very large!** (~10MB per minute)
- For music listening, use MP3 320kbps or M4A 256kbps
- Use WAV only for audio editing or when you need uncompressed quality
- A 5-minute video = ~50MB in WAV vs ~12MB in MP3

### Video Quality
- YouTube's max quality varies by video (720p, 1080p, 4K)
- Scripts automatically download the best available
- Premium videos may require authentication (not supported)

### Audio Quality
- YouTube's max audio quality is typically ~160kbps (opus/aac)
- Converting to WAV doesn't improve quality beyond source
- WAV just stores it without compression

### Batch Processing
For downloading multiple videos efficiently:

1. Run the script once
2. Paste first URL → Enter
3. When asked "Download another?", type **y**
4. Paste next URL → Enter
5. Repeat as needed
6. Type **n** or 'q' when done

### Storage Management
- Monitor disk space, especially when downloading in WAV
- Regularly clean up downloaded files you no longer need
- Consider using compressed formats (MP3, M4A) for music libraries
=======
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
>>>>>>> 4ab9807261b3525d0b2a96e4cd3c6acb80667529

## 🔄 Keeping yt-dlp Updated

YouTube frequently changes their API. Keep yt-dlp updated to avoid issues:

```bash
pip install --upgrade yt-dlp
```

<<<<<<< HEAD
Run this command monthly or if you encounter download errors.

## 📋 Quick Reference Card

| Action | Command |
|--------|---------|
| Install dependencies | `pip install yt-dlp` |
| Install FFmpeg | See installation section above |
| Run video downloader | `python ytbdl.py` |
| Run audio downloader | `python ytbdl_audio.py` |
| Quit program | Type `q` or press `Ctrl+C` |
| Download another | Type `y` when asked |
| Exit after download | Type `n` when asked |
| Find video downloads | Check `./video/` folder |
| Find audio downloads | Check `./audio/` folder |
| Update yt-dlp | `pip install -U yt-dlp` |
| Check FFmpeg | `ffmpeg -version` |

## ⚠️ Important Notes

- **Respect copyright**: Only download content you have permission to download
- **Terms of Service**: Respect YouTube's Terms of Service
- **Rate limiting**: Don't download too many videos too quickly
- **Legal use**: These tools are for personal, legal use only
- **No warranty**: Authors not responsible for misuse

## 🆘 Still Having Issues?

1. ✅ Check this troubleshooting section
2. ✅ Update yt-dlp: `pip install -U yt-dlp`
3. ✅ Verify FFmpeg is installed: `ffmpeg -version`
4. ✅ Try a different video to isolate the issue
5. ✅ Check yt-dlp GitHub issues: https://github.com/yt-dlp/yt-dlp/issues

## 📄 License & Disclaimer

These scripts are provided as-is for educational and personal use. Always respect copyright laws and YouTube's Terms of Service. The authors are not responsible for misuse of these tools.

---

**Happy downloading! 🎉**

*No code editing needed - just run and paste URLs!*
=======
## 📄 License & Disclaimer

These scripts are for personal use. Respect copyright laws and YouTube's Terms of Service. The authors are not responsible for misuse of these tools.

## 🆘 Need Help?

If you encounter issues:
1. Check this troubleshooting section
2. Update yt-dlp: `pip install -U yt-dlp`
3. Verify FFmpeg is installed: `ffmpeg -version`
4. Check yt-dlp GitHub issues: https://github.com/yt-dlp/yt-dlp/issues
>>>>>>> 4ab9807261b3525d0b2a96e4cd3c6acb80667529

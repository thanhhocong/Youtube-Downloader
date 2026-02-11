# YouTube Downloader Setup Guide
## Quick Setup

### 1. Install FFmpeg (Required)

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
or run the FFMPEG.ps1

### 2. Install JavaScript Runtime (Optional)

The JS runtime warning can be ignored for most videos, but for better format support:

**Install Deno:**
```bash
# Linux/macOS
curl -fsSL https://deno.land/install.sh | sh

# Windows (PowerShell)
irm https://deno.land/install.ps1 | iex
```

Then update your script to use it:
```python
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    'merge_output_format': 'mp4',
    'noplaylist': True,
    'progress_hooks': [progress_hook],
    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},  # Alternative approach
}
```

## Usage

```python
python ytbdl.py
```

Or customize the video URL:
```python
video_url = "YOUR_YOUTUBE_URL_HERE"
download_full_hd(video_url, output_path='./downloads')
```

## Improvements Made

✅ **Dependency checking** - Script now checks for FFmpeg before attempting download
✅ **Better error handling** - More informative error messages
✅ **Directory creation** - Automatically creates output directory
✅ **Safer progress hook** - Uses `.get()` to prevent KeyErrors

## Format Options

The current format string prioritizes quality:
```python
'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
```

Alternative options:

**Specific resolution:**
```python
'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best'
```

**File size limit:**
```python
'bestvideo[filesize<500M][ext=mp4]+bestaudio[ext=m4a]/best'
```

**Audio only:**
```python
'bestaudio[ext=m4a]/bestaudio'
```

## Troubleshooting

**"No formats found"**
- Video may be restricted or private
- Try adding `'extractor_args': {'youtube': {'player_client': ['android']}}`

**"Requested format not available"**
- Video doesn't have MP4 format
- Remove `[ext=mp4]` from format string

**Slow downloads**
- Network issue or YouTube throttling
- Try during off-peak hours

**Permission errors**
- Ensure write permissions for output directory
- Try different output path

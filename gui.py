import customtkinter as ctk
import yt_dlp
import os
import sys
import threading
import shutil
from tkinter import filedialog, messagebox
from io import BytesIO

try:
    from PIL import Image
    import requests
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ── Appearance ──────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Color palette ───────────────────────────────────────────
BG_DARK      = "#0f0f0f"
BG_CARD      = "#1a1a2e"
BG_ENTRY     = "#16213e"
ACCENT       = "#e94560"
ACCENT_HOVER = "#c81e45"
TEXT_PRIMARY  = "#ffffff"
TEXT_SECONDARY= "#a0a0b0"
SUCCESS      = "#00c853"
WARNING      = "#ffab00"
BORDER       = "#2a2a4a"


class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ── Window setup ────────────────────────────────────
        self.title("YouTube Downloader")
        self.geometry("900x720")
        self.minsize(800, 650)
        self.configure(fg_color=BG_DARK)

        # Center window on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 900) // 2
        y = (self.winfo_screenheight() - 720) // 2
        self.geometry(f"+{x}+{y}")

        # ── State ───────────────────────────────────────────
        self.video_info      = None
        self.video_formats   = []
        self.audio_formats   = []
        self.is_downloading  = False
        self.download_type   = ctk.StringVar(value="video")
        self.output_path     = ctk.StringVar(value=os.path.join(os.getcwd(), "downloads"))

        self._build_ui()

    # ════════════════════════════════════════════════════════
    #  BUILD UI
    # ════════════════════════════════════════════════════════
    def _build_ui(self):
        # Main scrollable container
        self.main_frame = ctk.CTkScrollableFrame(
            self, fg_color=BG_DARK, corner_radius=0,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=ACCENT,
        )
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        self.main_frame.columnconfigure(0, weight=1)

        row = 0

        # ── Header ──────────────────────────────────────────
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.grid(row=row, column=0, sticky="ew", pady=(18, 6), padx=24)
        header.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text="▶  YouTube Downloader",
            font=ctk.CTkFont(size=28, weight="bold"), text_color=ACCENT,
            anchor="w"
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header, text="Tải video & audio chất lượng cao từ YouTube",
            font=ctk.CTkFont(size=13), text_color=TEXT_SECONDARY, anchor="w"
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        row += 1

        # ── URL input card ──────────────────────────────────
        url_card = ctk.CTkFrame(self.main_frame, fg_color=BG_CARD, corner_radius=14, border_width=1, border_color=BORDER)
        url_card.grid(row=row, column=0, sticky="ew", padx=24, pady=(12, 6))
        url_card.columnconfigure(1, weight=1)

        ctk.CTkLabel(url_card, text="🔗  URL YouTube:", font=ctk.CTkFont(size=14, weight="bold"),
                      text_color=TEXT_PRIMARY).grid(row=0, column=0, columnspan=3, sticky="w", padx=16, pady=(14, 4))

        self.url_entry = ctk.CTkEntry(
            url_card, height=42, corner_radius=10,
            fg_color=BG_ENTRY, border_color=BORDER, text_color=TEXT_PRIMARY,
            placeholder_text="Dán link YouTube vào đây...",
            font=ctk.CTkFont(size=13)
        )
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(16, 8), pady=(0, 14))
        self.url_entry.bind("<Return>", lambda e: self._fetch_info())

        self.fetch_btn = ctk.CTkButton(
            url_card, text="Lấy thông tin", width=130, height=42,
            corner_radius=10, fg_color=ACCENT, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._fetch_info
        )
        self.fetch_btn.grid(row=1, column=2, sticky="e", padx=(0, 16), pady=(0, 14))

        row += 1

        # ── Video info card (hidden initially) ──────────────
        self.info_card = ctk.CTkFrame(self.main_frame, fg_color=BG_CARD, corner_radius=14, border_width=1, border_color=BORDER)
        self.info_card.columnconfigure(1, weight=1)
        # Will be shown after fetch

        # Thumbnail
        self.thumb_label = ctk.CTkLabel(self.info_card, text="", width=200, height=112, corner_radius=10)
        self.thumb_label.grid(row=0, column=0, rowspan=3, padx=16, pady=16)

        self.title_label = ctk.CTkLabel(self.info_card, text="", font=ctk.CTkFont(size=15, weight="bold"),
                                         text_color=TEXT_PRIMARY, anchor="w", wraplength=500)
        self.title_label.grid(row=0, column=1, sticky="w", padx=(0, 16), pady=(16, 2))

        self.uploader_label = ctk.CTkLabel(self.info_card, text="", font=ctk.CTkFont(size=12),
                                            text_color=TEXT_SECONDARY, anchor="w")
        self.uploader_label.grid(row=1, column=1, sticky="w", padx=(0, 16))

        self.duration_label = ctk.CTkLabel(self.info_card, text="", font=ctk.CTkFont(size=12),
                                            text_color=TEXT_SECONDARY, anchor="w")
        self.duration_label.grid(row=2, column=1, sticky="nw", padx=(0, 16), pady=(0, 16))

        self.info_row = row
        row += 1

        # ── Download type selection ─────────────────────────
        self.type_card = ctk.CTkFrame(self.main_frame, fg_color=BG_CARD, corner_radius=14, border_width=1, border_color=BORDER)
        self.type_card.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self.type_card, text="📂  Loại tải xuống:",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      text_color=TEXT_PRIMARY).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(14, 8))

        self.video_radio = ctk.CTkRadioButton(
            self.type_card, text="🎬  Video (có âm thanh)", variable=self.download_type,
            value="video", font=ctk.CTkFont(size=13), text_color=TEXT_PRIMARY,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, border_color=BORDER,
            command=self._on_type_change
        )
        self.video_radio.grid(row=1, column=0, sticky="w", padx=24, pady=(0, 14))

        self.audio_radio = ctk.CTkRadioButton(
            self.type_card, text="🎵  Chỉ âm thanh", variable=self.download_type,
            value="audio", font=ctk.CTkFont(size=13), text_color=TEXT_PRIMARY,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, border_color=BORDER,
            command=self._on_type_change
        )
        self.audio_radio.grid(row=1, column=1, sticky="w", padx=24, pady=(0, 14))

        self.type_row = row
        row += 1

        # ── Quality selection ───────────────────────────────
        self.quality_card = ctk.CTkFrame(self.main_frame, fg_color=BG_CARD, corner_radius=14, border_width=1, border_color=BORDER)
        self.quality_card.columnconfigure(0, weight=1)

        ctk.CTkLabel(self.quality_card, text="📊  Chất lượng:",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      text_color=TEXT_PRIMARY).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 8))

        self.quality_combo = ctk.CTkComboBox(
            self.quality_card, height=40, corner_radius=10,
            fg_color=BG_ENTRY, border_color=BORDER, text_color=TEXT_PRIMARY,
            button_color=ACCENT, button_hover_color=ACCENT_HOVER,
            dropdown_fg_color=BG_CARD, dropdown_text_color=TEXT_PRIMARY,
            dropdown_hover_color=ACCENT,
            font=ctk.CTkFont(size=13), state="readonly",
            values=["-- Lấy thông tin video trước --"]
        )
        self.quality_combo.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))
        self.quality_combo.set("-- Lấy thông tin video trước --")

        self.quality_row = row
        row += 1

        # ── Output path ────────────────────────────────────
        self.path_card = ctk.CTkFrame(self.main_frame, fg_color=BG_CARD, corner_radius=14, border_width=1, border_color=BORDER)
        self.path_card.columnconfigure(1, weight=1)

        ctk.CTkLabel(self.path_card, text="📁  Thư mục lưu:",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      text_color=TEXT_PRIMARY).grid(row=0, column=0, columnspan=3, sticky="w", padx=16, pady=(14, 4))

        self.path_entry = ctk.CTkEntry(
            self.path_card, height=40, corner_radius=10,
            fg_color=BG_ENTRY, border_color=BORDER, text_color=TEXT_PRIMARY,
            textvariable=self.output_path, font=ctk.CTkFont(size=12)
        )
        self.path_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(16, 8), pady=(0, 14))

        ctk.CTkButton(
            self.path_card, text="Chọn...", width=90, height=40,
            corner_radius=10, fg_color=BG_ENTRY, hover_color=BORDER,
            border_width=1, border_color=BORDER, text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(size=12), command=self._browse_folder
        ).grid(row=1, column=2, sticky="e", padx=(0, 16), pady=(0, 14))

        self.path_row = row
        row += 1

        # ── Download button ────────────────────────────────
        self.download_btn = ctk.CTkButton(
            self.main_frame, text="⬇  Tải xuống", height=50,
            corner_radius=12, fg_color=ACCENT, hover_color=ACCENT_HOVER,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._start_download, state="disabled"
        )
        self.download_row = row
        row += 1

        # ── Progress section ───────────────────────────────
        self.progress_card = ctk.CTkFrame(self.main_frame, fg_color=BG_CARD, corner_radius=14, border_width=1, border_color=BORDER)
        self.progress_card.columnconfigure(0, weight=1)

        self.progress_label = ctk.CTkLabel(
            self.progress_card, text="Sẵn sàng",
            font=ctk.CTkFont(size=13), text_color=TEXT_SECONDARY, anchor="w"
        )
        self.progress_label.grid(row=0, column=0, sticky="w", padx=16, pady=(14, 6))

        self.progress_bar = ctk.CTkProgressBar(
            self.progress_card, height=12, corner_radius=6,
            fg_color=BG_ENTRY, progress_color=ACCENT
        )
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 6))
        self.progress_bar.set(0)

        self.progress_detail = ctk.CTkLabel(
            self.progress_card, text="",
            font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY, anchor="w"
        )
        self.progress_detail.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 14))

        self.progress_row = row
        row += 1

        # ── Log area ───────────────────────────────────────
        self.log_card = ctk.CTkFrame(self.main_frame, fg_color=BG_CARD, corner_radius=14, border_width=1, border_color=BORDER)
        self.log_card.columnconfigure(0, weight=1)

        ctk.CTkLabel(self.log_card, text="📋  Nhật ký:",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      text_color=TEXT_PRIMARY).grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))

        self.log_text = ctk.CTkTextbox(
            self.log_card, height=120, corner_radius=10,
            fg_color=BG_ENTRY, text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(family="Consolas", size=11),
            border_width=1, border_color=BORDER,
            state="disabled"
        )
        self.log_text.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 14))

        self.log_row = row
        row += 1

        # ── Footer ─────────────────────────────────────────
        ctk.CTkLabel(
            self.main_frame, text="Made with ❤ — Powered by yt-dlp & FFmpeg",
            font=ctk.CTkFont(size=11), text_color="#505060"
        ).grid(row=row, column=0, pady=(4, 16))

        # Initially hide cards that need video info
        self._show_options(False)

    # ════════════════════════════════════════════════════════
    #  SHOW / HIDE OPTIONS
    # ════════════════════════════════════════════════════════
    def _show_options(self, show: bool):
        if show:
            self.info_card.grid(row=self.info_row, column=0, sticky="ew", padx=24, pady=6)
            self.type_card.grid(row=self.type_row, column=0, sticky="ew", padx=24, pady=6)
            self.quality_card.grid(row=self.quality_row, column=0, sticky="ew", padx=24, pady=6)
            self.path_card.grid(row=self.path_row, column=0, sticky="ew", padx=24, pady=6)
            self.download_btn.grid(row=self.download_row, column=0, sticky="ew", padx=24, pady=10)
            self.progress_card.grid(row=self.progress_row, column=0, sticky="ew", padx=24, pady=6)
            self.log_card.grid(row=self.log_row, column=0, sticky="ew", padx=24, pady=(6, 4))
            self.download_btn.configure(state="normal")
        else:
            self.info_card.grid_forget()
            self.type_card.grid_forget()
            self.quality_card.grid_forget()
            self.path_card.grid_forget()
            self.download_btn.grid_forget()
            self.progress_card.grid_forget()
            self.log_card.grid_forget()

    # ════════════════════════════════════════════════════════
    #  LOG
    # ════════════════════════════════════════════════════════
    def _log(self, msg: str):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    # ════════════════════════════════════════════════════════
    #  BROWSE FOLDER
    # ════════════════════════════════════════════════════════
    def _browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_path.get())
        if folder:
            self.output_path.set(folder)

    # ════════════════════════════════════════════════════════
    #  FETCH VIDEO INFO
    # ════════════════════════════════════════════════════════
    def _fetch_info(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Thiếu URL", "Vui lòng dán link YouTube vào ô URL!")
            return

        self.fetch_btn.configure(state="disabled", text="Đang lấy...")
        self._show_options(False)
        threading.Thread(target=self._fetch_thread, args=(url,), daemon=True).start()

    def _fetch_thread(self, url: str):
        try:
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            self.video_info = info
            formats = info.get('formats', [])
            self.video_formats = self._parse_video_formats(formats)
            self.audio_formats = self._parse_audio_formats(formats)

            # Update UI on main thread
            self.after(0, lambda: self._update_info_ui(info))
        except Exception as e:
            self.after(0, lambda: self._fetch_error(str(e)))

    def _fetch_error(self, err: str):
        self.fetch_btn.configure(state="normal", text="Lấy thông tin")
        messagebox.showerror("Lỗi", f"Không thể lấy thông tin video:\n{err}")

    def _update_info_ui(self, info):
        title    = info.get('title', 'Không rõ')
        uploader = info.get('uploader', 'Không rõ')
        duration = info.get('duration', 0)
        thumb_url = info.get('thumbnail', '')

        self.title_label.configure(text=f"🎬  {title}")
        self.uploader_label.configure(text=f"👤  {uploader}")
        dur_str = f"{duration // 60}:{duration % 60:02d}" if duration else "N/A"
        self.duration_label.configure(text=f"⏱  {dur_str}")

        # Load thumbnail
        if PIL_AVAILABLE and thumb_url:
            threading.Thread(target=self._load_thumbnail, args=(thumb_url,), daemon=True).start()
        else:
            self.thumb_label.configure(text="No\nThumbnail", fg_color=BG_ENTRY)

        self._on_type_change()
        self._show_options(True)
        self.fetch_btn.configure(state="normal", text="Lấy thông tin")
        self._log(f"✓ Đã lấy thông tin: {title}")

    def _load_thumbnail(self, url: str):
        try:
            resp = requests.get(url, timeout=10)
            img = Image.open(BytesIO(resp.content))
            img = img.resize((200, 112), Image.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 112))
            self.after(0, lambda: self.thumb_label.configure(image=ctk_img, text=""))
            self._thumb_ref = ctk_img  # prevent GC
        except Exception:
            pass

    # ════════════════════════════════════════════════════════
    #  FORMAT PARSING
    # ════════════════════════════════════════════════════════
    @staticmethod
    def _parse_video_formats(formats):
        video_fmts = []
        seen = set()
        for f in formats:
            # Include all formats that have video (both combined and video-only)
            if f.get('vcodec') == 'none':
                continue

            height = f.get('height', 0)
            if not height:
                continue

            quality    = f.get('format_note', 'unknown')
            resolution = f.get('resolution', f'{f.get("width", "?")}x{height}')
            ext        = f.get('ext', 'unknown')
            filesize   = f.get('filesize', 0) or f.get('filesize_approx', 0)
            has_audio  = f.get('acodec') != 'none'
            fps        = f.get('fps', 0)

            key = f"{height}_{fps}"
            if key not in seen:
                seen.add(key)
                video_fmts.append({
                    'format_id': f.get('format_id'),
                    'quality': quality,
                    'resolution': resolution,
                    'ext': ext,
                    'height': height,
                    'fps': fps,
                    'filesize': filesize or 0,
                    'has_audio': has_audio,
                })
        video_fmts.sort(
            key=lambda x: (x['height'], x.get('fps', 0)),
            reverse=True
        )
        return video_fmts

    @staticmethod
    def _parse_audio_formats(formats):
        # Find the best audio bitrate for display
        max_br = 0
        for f in formats:
            if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                abr = f.get('abr', 0)
                if abr:
                    max_br = max(max_br, abr)

        br_label = f"{max_br}kbps" if max_br else "Best"

        # Only offer WAV and MP3 (both converted from best audio)
        return [
            {
                'format_id': 'bestaudio',
                'bitrate': br_label,
                'ext': 'wav',
                'filesize': 0,
                'is_converted': True,
            },
            {
                'format_id': 'bestaudio',
                'bitrate': br_label,
                'ext': 'mp3',
                'filesize': 0,
                'is_converted': True,
            },
        ]

    # ════════════════════════════════════════════════════════
    #  TYPE CHANGE → POPULATE QUALITY COMBO
    # ════════════════════════════════════════════════════════
    def _on_type_change(self):
        if self.download_type.get() == "video":
            items = []
            for f in self.video_formats:
                sz = self._fmt_size(f['filesize'])
                fps_info = f"  {f['fps']}fps" if f.get('fps') else ""
                merge_tag = "  [merge]" if not f.get('has_audio') else ""
                items.append(f"{f['resolution']}{fps_info}  •  {f['quality']}  •  {f['ext']}  •  {sz}{merge_tag}")
            if not items:
                items = ["Không có định dạng video"]
            self.quality_combo.configure(values=items)
            self.quality_combo.set(items[0])
        else:
            items = []
            for f in self.audio_formats:
                sz = self._fmt_size(f['filesize'])
                tag = " (convert)" if f.get('is_converted') else ""
                items.append(f"{f['bitrate']}  •  {f['ext'].upper()}{tag}  •  {sz}")
            if not items:
                items = ["Không có định dạng audio"]
            self.quality_combo.configure(values=items)
            self.quality_combo.set(items[0])

    @staticmethod
    def _fmt_size(size):
        if not size:
            return "~"
        for u in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {u}"
            size /= 1024
        return f"{size:.1f} TB"

    # ════════════════════════════════════════════════════════
    #  DOWNLOAD
    # ════════════════════════════════════════════════════════
    def _start_download(self):
        if self.is_downloading:
            return
        self.is_downloading = True
        self.download_btn.configure(state="disabled", text="⏳  Đang tải...")
        self.progress_bar.set(0)
        self.progress_label.configure(text="Đang chuẩn bị...", text_color=WARNING)
        self.progress_detail.configure(text="")

        threading.Thread(target=self._download_thread, daemon=True).start()

    def _download_thread(self):
        try:
            url = self.url_entry.get().strip()
            out = self.output_path.get()
            os.makedirs(out, exist_ok=True)

            # Determine selected index
            selected = self.quality_combo.get()
            if self.download_type.get() == "video":
                idx = self._find_index(selected, self.video_formats, "video")
                fmt = self.video_formats[idx]
                self._download_video(url, fmt['format_id'], out, has_audio=fmt.get('has_audio', True))
            else:
                idx = self._find_index(selected, self.audio_formats, "audio")
                fmt = self.audio_formats[idx]
                if fmt['ext'].lower() == 'wav':
                    self._download_audio(url, out, 'wav', '0')
                else:
                    self._download_audio(url, out, 'mp3', '192')

            self.after(0, self._download_done)
        except Exception as e:
            self.after(0, lambda: self._download_error(str(e)))

    def _find_index(self, selected_text, fmt_list, kind):
        """Find the index of the selected format from combo text."""
        if kind == "video":
            for i, f in enumerate(fmt_list):
                if f['resolution'] in selected_text and f['quality'] in selected_text:
                    return i
        else:
            for i, f in enumerate(fmt_list):
                if f['bitrate'] in selected_text and f['ext'].upper() in selected_text:
                    return i
        return 0

    def _download_video(self, url, format_id, output_path, has_audio=True):
        if has_audio:
            dl_format = format_id
        else:
            dl_format = f"{format_id}+bestaudio"

        ydl_opts = {
            'format': dl_format,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'progress_hooks': [self._progress_hook],
        }
        
        # Always ensure MP4 container with AAC audio codec for maximum compatibility
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
        
        # Force audio codec to AAC for universal compatibility
        ydl_opts['postprocessor_args'] = [
            '-c:v', 'copy',  # Copy video without re-encoding
            '-c:a', 'aac',   # Convert audio to AAC
            '-b:a', '192k',  # Audio bitrate 192kbps
        ]
            
        if has_audio:
            self.after(0, lambda: self._log("⬇ Đang tải video (MP4/AAC)..."))
        else:
            self.after(0, lambda: self._log("⬇ Đang tải video + audio và merge (MP4/AAC)..."))
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def _download_audio(self, url, output_path, audio_format='mp3', quality='192'):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': quality,
            }],
            'progress_hooks': [self._progress_hook],
        }
        fmt_name = audio_format.upper()
        self.after(0, lambda: self._log(f"⬇ Đang tải và chuyển đổi sang {fmt_name}..."))
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            pct_str  = d.get('_percent_str', '0%').strip()
            speed    = d.get('_speed_str', 'N/A').strip()
            eta      = d.get('_eta_str', 'N/A').strip()

            # Parse percentage
            try:
                pct_val = float(pct_str.replace('%', '')) / 100.0
            except ValueError:
                pct_val = 0

            self.after(0, lambda p=pct_val, s=speed, e=eta, ps=pct_str: self._update_progress(p, ps, s, e))

        elif d['status'] == 'finished':
            self.after(0, lambda: self._update_progress(1.0, "100%", "", "Đang xử lý..."))
            self.after(0, lambda: self._log("✓ Tải xong, đang xử lý file..."))

    def _update_progress(self, value, pct, speed, eta):
        self.progress_bar.set(value)
        self.progress_label.configure(text=f"Đang tải: {pct}", text_color=WARNING)
        self.progress_detail.configure(text=f"Tốc độ: {speed}  |  ETA: {eta}")

    def _download_done(self):
        self.is_downloading = False
        self.download_btn.configure(state="normal", text="⬇  Tải xuống")
        self.progress_bar.set(1)
        self.progress_label.configure(text="✅  Hoàn tất!", text_color=SUCCESS)
        self.progress_detail.configure(text=f"File đã lưu tại: {self.output_path.get()}")
        self._log(f"✅ Tải xuống hoàn tất! Lưu tại: {self.output_path.get()}")

        # Open folder button
        open_btn = ctk.CTkButton(
            self.progress_card, text="📂 Mở thư mục", width=130, height=34,
            corner_radius=8, fg_color=SUCCESS, hover_color="#00a847",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: os.startfile(self.output_path.get()) if sys.platform == 'win32' else None
        )
        open_btn.grid(row=3, column=0, sticky="w", padx=16, pady=(0, 14))

    def _download_error(self, err):
        self.is_downloading = False
        self.download_btn.configure(state="normal", text="⬇  Tải xuống")
        self.progress_label.configure(text="❌  Lỗi tải xuống!", text_color=ACCENT)
        self.progress_detail.configure(text="")
        self._log(f"❌ Lỗi: {err}")
        messagebox.showerror("Lỗi tải xuống", f"Đã xảy ra lỗi:\n{err}")


# ════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()


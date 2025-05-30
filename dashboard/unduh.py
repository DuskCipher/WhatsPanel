# dashboard/unduh.py

import streamlit as st
import yt_dlp
import os

def show_unduh():
    st.title("📥 Multi Video & Audio Downloader")

    st.markdown("""
    Masukkan satu atau lebih URL dari <strong>YouTube, TikTok, Instagram</strong>, dll.  
    Pilih kualitas video atau MP3, lalu tekan <span style="color:#00cec9;"><strong>Download</strong></span> untuk memulai.
    """, unsafe_allow_html=True)

    urls_input = st.text_area("🔗 Masukkan URL (satu per baris):")
    download_type = st.radio("📦 Jenis download:", ["Video", "Audio (MP3)"])

    video_quality = None
    if download_type == "Video":
        video_quality = st.selectbox("📺 Resolusi Video:", ["360p", "720p", "1080p"])

    if st.button("🚀 Mulai Download"):
        if not urls_input.strip():
            st.warning("⚠️ Masukkan setidaknya satu URL terlebih dahulu.")
        else:
            urls = [url.strip() for url in urls_input.strip().splitlines() if url.strip()]
            st.success(f"🎯 Total: {len(urls)} URL akan diproses!")

            for i, url in enumerate(urls, start=1):
                st.markdown(f"---\n🔗 **[{i}] Sedang memproses:** `{url}`")
                progress_bar = st.progress(0)
                progress_text = st.empty()

                def my_hook(d):
                    if d['status'] == 'downloading':
                        downloaded_bytes = d.get("downloaded_bytes", 0)
                        total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate")
                        if total_bytes:
                            percent = downloaded_bytes / total_bytes
                            progress_bar.progress(min(int(percent * 100), 100))
                            progress_text.markdown(f"📥 Terunduh: **{downloaded_bytes / 1_048_576:.2f} MB** / **{total_bytes / 1_048_576:.2f} MB**")
                        else:
                            progress_text.markdown(f"📥 Terunduh: **{downloaded_bytes / 1_048_576:.2f} MB**")
                    elif d['status'] == 'finished':
                        progress_bar.progress(100)
                        progress_text.markdown("✅ Selesai mengunduh, sedang proses akhir...")

                try:
                    if download_type == "Audio (MP3)":
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': f'downloads/audio_%(title)s.%(ext)s',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'progress_hooks': [my_hook],
                            'quiet': True,
                        }
                    else:
                        resolution_map = {
                            "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
                            "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
                            "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
                        }
                        ydl_opts = {
                            'format': resolution_map[video_quality],
                            'outtmpl': f'downloads/video_%(title)s.%(ext)s',
                            'merge_output_format': 'mp4',
                            'progress_hooks': [my_hook],
                            'quiet': True,
                        }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        file_path = ydl.prepare_filename(info)
                        if download_type == "Audio (MP3)":
                            file_path = os.path.splitext(file_path)[0] + ".mp3"

                        file_name = os.path.basename(file_path)

                        with open(file_path, "rb") as f:
                            st.download_button(
                                label=f"⬇️ Download: {file_name}",
                                data=f,
                                file_name=file_name,
                                mime="audio/mpeg" if download_type == "Audio (MP3)" else "video/mp4"
                            )

                except Exception as e:
                    st.error(f"❌ Gagal download dari {url}: {e}")

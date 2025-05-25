import streamlit as st
import requests
from cryptography.fernet import Fernet
from streamlit_option_menu import option_menu
import time
import time
import pandas as pd
from PIL import Image
import os
from datetime import datetime
import base64
import sqlite3
import io
import subprocess
import platform
from pathlib import Path
import cloudinary
import cloudinary.uploader
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
from streamlit_option_menu import option_menu
from streamlit_ace import st_ace

st.set_page_config(
    page_title="WA Sender Blasting",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg",  # WhatsApp icon
    layout="wide"
)

import streamlit as st

# Inisialisasi session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Styling tambahan
custom_css = """
<style>
    #MainMenu, header, footer {visibility: hidden;}
    div.stButton > button {
        width: 100% !important;
        padding: 0.75rem;
        background-color: transparent;  /* ✅ diubah jadi transparan */
        border-radius: 8px;
        border: 2px solid #ffffff;  /* opsional: beri outline agar tetap terlihat */
        color: #ffffff;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: rgba(255, 75, 75, 0.1);  /* efek hover semi-transparan */
        transform: scale(1.01);
    }
    @media screen and (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
        .css-1v0mbdj, .stColumn {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    .login-box {
        background-color: #1e1e1e;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# Jika belum login, tampilkan form login
if not st.session_state.logged_in:
    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown("""
            <div style="position: relative;">
                <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgA2XeFUgIcaU0vFHJ7pE-PewzV1Nph_FJc4ETOpdF0mIENXNWe1OggrCmZtAN38y6M5URHJhwa9Et-DUkNwz_vU5Rn-HjzYnDBzYZmPOroWcuVbp4EkNTYvC8yd8VIzqEN6HeGwXPuiq9l6qvzO4j_gRYkyFH7kcUYLklR2F4NixHBKVExhMOXBYUN4xLb/s5760/Panel.png" style="width: 100%; border-radius: 10px;">
                <a href='https://beacons.ai/riz_project' target='_blank'>
                    <button style='
                        position: absolute;
                        bottom: 40px;
                        right: 40px;
                        background-color: #00c851;
                        color: white;
                        font-size: 1rem;
                        font-weight: bold;
                        padding: 0.75rem 2rem;
                        border-radius: 30px;
                        border: none;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                        transition: 0.3s ease;
                        cursor: pointer;
                    ' onmouseover="this.style.backgroundColor='#007E33'" onmouseout="this.style.backgroundColor='#00c851'">
                        🌐 Kunjungi Web saya
                    </button>
                </a>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 🔐 Login ke Dashboard")

        with st.form("login_form"):
            appkey_input = st.text_input("🕝 App Key", type="password", placeholder="Masukkan App Key")
            authkey_input = st.text_input("🔐 Auth Key", type="password", placeholder="Masukkan Auth Key")
            keep_login = st.checkbox("Tetap masuk")
            login_submit = st.form_submit_button("🚀 MASUK")

            if login_submit:
                if appkey_input and authkey_input:
                    progress_bar = st.empty()
                    for i in range(1, 101):
                        time.sleep(0.01)
                        progress_bar.progress(i, text=f"Login {i}%")
                    
                    st.session_state.appkey = appkey_input
                    st.session_state.authkey = authkey_input
                    st.session_state.logged_in = True
                    time.sleep(0.3)
                    st.rerun()
                else:
                    st.error("App Key atau Auth Key salah!")

        st.stop()

# --- Khusus Untuk Memangil file Tool ---
from tools.script_tool import show_script_tool
from dashboard.api_key_manager import show_api_key_manager
from dashboard.notepad import show_notepad
from dashboard.tool_oli import show_tool_oli
from dashboard.terminal import show_terminal
from dashboard.analisis_pengiriman import show_analisis_pengiriman

# Tambahkan copyright ke sidebar kiri bawah
if st.session_state.get("logged_in", False):
    st.sidebar.markdown("""
    <style>
    .sidebar-copyright {
        position: fixed;
        bottom: 10px;
        left: 0;
        width: 250px;
        text-align: center;
        font-size: 15px;
        color: #888;
        padding: 5px 10px;
        opacity: 0.7;
    }
    </style>
    <div class='sidebar-copyright'>
        © 2025 Bengkel Mobil Purwokerto<br>Bengkel Kaki Mobil Arumsari
    </div>
    """, unsafe_allow_html=True)

# --- Inisialisasi session_state jika belum ada ---
if "encryption_key" not in st.session_state:
    st.session_state.encryption_key = Fernet.generate_key()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "appkey" not in st.session_state:
    st.session_state.appkey = ""
if "authkey" not in st.session_state:
    st.session_state.authkey = ""
if "log_df" not in st.session_state:
    st.session_state.log_df = pd.DataFrame()
if "manual_data" not in st.session_state:
    st.session_state.manual_data = []
if "data_excel" not in st.session_state:
    st.session_state.data_excel = pd.DataFrame()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "encryption_key" not in st.session_state:
    st.session_state.encryption_key = Fernet.generate_key()

# --- Fungsi Kirim Pesan (didefinisikan di atas agar tidak error) ---
def send_text_message(number, message, appkey, authkey):
    url = "https://app.wapanels.com/api/create-message"
    payload = {'appkey': appkey, 'authkey': authkey, 'to': number, 'message': message}
    try:
        response = requests.post(url, data=payload)
        data = response.json()  # asumsi API mengembalikan JSON
        if response.status_code == 200 and data.get("status") == "success":
            return "✅ Berhasil", str(data)
        else:
            return "❌ Gagal", str(data)
    except Exception as e:
        return "❌ Error", str(e)

def send_image_message(number, caption, image_url, appkey, authkey):
    url = "https://app.wapanels.com/api/create-message"
    payload = {'appkey': appkey, 'authkey': authkey, 'to': number, 'message': caption, 'file': image_url}
    try:
        response = requests.post(url, data=payload)
        data = response.json()
        if response.status_code == 200 and data.get("status") == "success":
            return "✅ Berhasil", str(data)
        else:
            return "❌ Gagal", str(data)
    except Exception as e:
        return "❌ Error", str(e)

# Konfigurasi Cloudinary
cloudinary.config(
    cloud_name='ddkqrgb2v',
    api_key='956855212351643',
    api_secret='RbhZ9ct4I4dH_WX7_1Qb339acDw'
)

# --- Menu Bar Modern dengan Logout ---
with st.sidebar:
    menu = option_menu(
    "Dashboard Panel",
    [
        "Pengaturan & Input",
        "Kirim Pesan",
        "Analisis Pengiriman",
        "Terminal",
        "Tool Khusus Oli",
        "Script Tool",
        "NotePad",
        "Manajemen API",
        "Logout"
    ],
    icons=[
        "gear", "send", "bar-chart", "terminal", "send",
        "code-slash", "journal-text", "key", "box-arrow-right", "key"],
        menu_icon="chat-dots",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#1E1E1E"},
            "icon": {"color": "#FFA500", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#333333",
                "color": "#CCCCCC",
            },
            "nav-link-selected": {
                "background-color": "#FFA500",
                "color": "black",
                "font-weight": "bold"
            },
        }
    )

if menu == "Logout":
    for key in ["logged_in", "appkey", "authkey"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("✅ Logout berhasil! Sampai jumpa.")
    st.rerun()

# --- Konten Menu --
if menu == "Pengaturan & Input":
    st.title("📱 Dashboard Blasting Bengkel Version 0.2 Beta")
    st.markdown("Versi interaktif menggunakan API WA Panel dengan Excel, input manual, dan dukungan gambar.")

    st.subheader("📝 Pengaturan Pesan")
    st.session_state.message_template = st.text_area("✏️ Template Pesan (gunakan {nama})", "Halo {nama}, ini adalah pesan testing dari WA API via Python.")
    st.session_state.delay_input = st.number_input("⏱️ Jeda antar pesan (detik)", min_value=1, value=5)

    st.subheader("🖼️ Upload Gambar (Opsional)")
    st.session_state.image_file = st.file_uploader("Unggah Gambar", type=["jpg", "jpeg", "png"])
    st.session_state.caption = st.text_area("📎 Caption untuk Gambar (gunakan {nama})", "Hai {nama}, ini gambar untukmu.")

    st.subheader("📤 Upload File Excel")
    uploaded_file = st.file_uploader("Unggah file Excel (.xlsx) berisi kolom: Nama, Nomor", type=["xlsx"])
    if uploaded_file:
        st.session_state.data_excel = pd.read_excel(uploaded_file)

    st.subheader("📥 Tambah Nomor Manual")
    with st.form("manual_form"):
        nama_manual = st.text_input("Nama")
        nomor_manual = st.text_input("Nomor (format: 62xxx)")
        if st.form_submit_button("➕ Tambahkan") and nama_manual and nomor_manual:
            st.session_state.manual_data.append({"Nama": nama_manual, "Nomor": nomor_manual})
            st.success("✅ Ditambahkan")

    if st.session_state.manual_data:
        df_manual = pd.DataFrame(st.session_state.manual_data)
        st.dataframe(df_manual)
        csv_manual = df_manual.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Manual CSV", csv_manual, "data_manual.csv", "text/csv")

elif menu == "Kirim Pesan":
    st.title("📱 Dashboard Blasting Bengkel Version 0.2 Beta")
    st.markdown("Versi interaktif menggunakan API WA Panel dengan Excel, input manual, dan dukungan gambar.")

    data_excel = st.session_state.get("data_excel", pd.DataFrame())
    df_all = pd.concat([data_excel, pd.DataFrame(st.session_state.manual_data)], ignore_index=True)
    
    if not df_all.empty:
        st.warning("⚠️ Jangan berpindah tab selama proses pengiriman berlangsung. Tetap di halaman ini sampai semua pesan selesai dikirim!")
        st.subheader("🚀 Kirim Pesan Otomatis")
        if st.button("📨 Mulai Kirim Pesan"):
            with st.spinner("Mengirim pesan..."):
                log = []
                image_url = None
                image_file = st.session_state.get("image_file")

                if image_file:
                    upload_result = cloudinary.uploader.upload(image_file, folder="whatsapp_uploads")
                    image_url = upload_result.get("secure_url")

                progress_bar = st.progress(0, text="Memulai pengiriman...")
                total = len(df_all)

                for idx, row in df_all.iterrows():
                    nama, nomor = row["Nama"], row["Nomor"]
                    msg = st.session_state.message_template.replace("{nama}", nama)
                    cap = st.session_state.caption.replace("{nama}", nama)

                    if image_file and image_url:
                        status, _ = send_image_message(nomor, cap, image_url, st.session_state.appkey, st.session_state.authkey)
                        pesan = cap
                    else:
                        status, _ = send_text_message(nomor, msg, st.session_state.appkey, st.session_state.authkey)
                        pesan = msg

                    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Tampilkan status langsung dalam style warna
                    icon = "✅" if "✅" in status else "❌"
                    warna_status = "#22c55e" if "✅" in status else "#ef4444"
                    warna_waktu = "#9ca3af"

                    st.markdown(
                        f"""
                        <div style="
                            background: #262626;
                            border-left: 5px solid {warna_status};
                            padding: 10px 15px;
                            margin: 8px 0;
                            border-radius: 10px;
                            font-family: 'Segoe UI', sans-serif;
                            color: white;
                            box-shadow: 0 0 5px rgba(0,0,0,0.2);
                        ">
                            <div style="color: {warna_waktu}; font-size: 13px;">🕒 {waktu}</div>
                            <div style="margin-top: 5px;">
                                <span style="color: {warna_status}; font-weight: bold; font-size: 15px;">{icon} {status.split()[-1]}</span>
                                <span style="color: #e5e7eb; font-size: 15px;"> ke <strong>{nama}</strong> (<code>{nomor}</code>)</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    log.append({
                        "Waktu": waktu,
                        "Nama": nama,
                        "Nomor": nomor,
                        "Pesan": pesan,
                        "Status": "✅ Berhasil" if "✅" in status else "❌ Gagal"
                    })

                    progress_bar.progress((idx + 1) / total, text=f"{int((idx + 1) / total * 100)}% selesai")
                    time.sleep(st.session_state.delay_input)

                st.session_state.log_df = pd.DataFrame(log)
                st.success("✅ Semua pesan telah dikirim!")

                # Tampilkan log sebagai tabel
                st.subheader("📋 Log Pengiriman")
                styled_log = st.session_state.log_df.style.applymap(
                    lambda x: "color: green;" if x == "✅ Berhasil" else "color: red;", subset=["Status"]
                )
                st.dataframe(styled_log, use_container_width=True)

                # Tombol download
                csv_log = st.session_state.log_df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Download Log CSV", data=csv_log, file_name="log_pengiriman.csv", mime="text/csv")
    else:
        st.warning("⚠️ Data kosong. Silakan upload file Excel atau masukkan nomor manual terlebih dahulu.")

elif menu == "Analisis Pengiriman":
    show_analisis_pengiriman()

elif menu == "Terminal":
    show_terminal()

if menu == "Tool Khusus Oli":
    show_tool_oli()

if menu == "NotePad":
    show_notepad()
    
if menu == "Script Tool":
    show_script_tool()

if menu == "Manajemen API":
    show_api_key_manager()
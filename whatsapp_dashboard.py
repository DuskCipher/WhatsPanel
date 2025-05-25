# ===[ IMPORT MODULE ]===
import time
import pandas as pd
from cryptography.fernet import Fernet
import streamlit as st
from streamlit_option_menu import option_menu

# ===[ PAGE CONFIG & SESSION STATE ]===
st.set_page_config(
    page_title="WhatsPanel 2.1",
    page_icon="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg",
    layout="wide",
)

defaults = {
    "logged_in": False,
    "appkey": "",
    "authkey": "",
    "log_df": pd.DataFrame(),
    "manual_data": [],
    "data_excel": pd.DataFrame(),
    "encryption_key": Fernet.generate_key(),
}
for key, value in defaults.items():
    st.session_state.setdefault(key, value)

# ===[ LOGIN SECTION – DO NOT CHANGE ]===
if not st.session_state.logged_in:
    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.markdown(
            """
            <div style="position: relative;">
                <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgA2XeFUgIcaU0vFHJ7pE-PewzV1Nph_FJc4ETOpdF0mIENXNWe1OggrCmZtAN38y6M5URHJhwa9Et-DUkNwz_vU5Rn-HjzYnDBzYZmPOroWcuVbp4EkNTYvC8yd8VIzqEN6HeGwXPuiq9l6qvzO4j_gRYkyFH7kcUYLklR2F4NixHBKVExhMOXBYUN4xLb/s5760/Panel.png" style="width: 100%; border-radius: 10px;">
                <a href='https://beacons.ai/riz_project' target='_blank'>
                    <button style='position: absolute; bottom: 40px; right: 40px; background-color: #00c851; color: white; font-size: 1rem; font-weight: bold; padding: 0.75rem 2rem; border-radius: 30px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.2); transition: 0.3s ease; cursor: pointer;' onmouseover="this.style.backgroundColor='#007E33'" onmouseout="this.style.backgroundColor='#00c851'">
                        🌐 Kunjungi Web saya
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

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

# ===[ GLOBAL STYLE ]===
st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    div.stButton > button {
        width: 100% !important;
        padding: 0.75rem;
        background-color: transparent;
        border-radius: 8px;
        border: 2px solid #ffffff;
        color: #ffffff;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: rgba(255, 75, 75, 0.1);
        transform: scale(1.01);
    }
    @media screen and (max-width: 768px) {
        .block-container {padding: 1rem;}
        .css-1v0mbdj, .stColumn {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
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
    """,
    unsafe_allow_html=True,
)

# ===[ IMPORT FITUR DASHBOARD ]===
from tools.script_tool import show_script_tool
from dashboard.api_key_manager import show_api_key_manager
from dashboard.notepad import show_notepad
from dashboard.tool_oli import show_tool_oli
from dashboard.terminal import show_terminal
from dashboard.analisis_pengiriman import show_analisis_pengiriman
from dashboard.kirim_pesan import show_kirim_pesan
from dashboard.pengaturan_input import show_pengaturan_input

# ===[ SIDEBAR MENU ]===
with st.sidebar:
    menu = option_menu(
        "Dashboard Panel",
        [
            "Pengaturan & Input", "Kirim Pesan", "Analisis Pengiriman",
            "Terminal", "Tool Khusus Oli", "Script Tool",
            "NotePad", "Manajemen API", "Logout",
        ],
        icons=[
            "gear", "send", "bar-chart", "terminal", "droplet",
            "code-slash", "journal-text", "key", "box-arrow-right",
        ],
        menu_icon="chat-dots",
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#1E1E1E"},
            "icon": {"color": "#FFA500", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px", "text-align": "left", "margin": "0px",
                "--hover-color": "#333333", "color": "#CCCCCC",
            },
            "nav-link-selected": {
                "background-color": "#FFA500", "color": "black", "font-weight": "bold",
            },
        },
    )

# ===[ MENU ROUTING ]===
pages = {
    "Pengaturan & Input": show_pengaturan_input,
    "Kirim Pesan": show_kirim_pesan,
    "Analisis Pengiriman": show_analisis_pengiriman,
    "Terminal": show_terminal,
    "Tool Khusus Oli": show_tool_oli,
    "Script Tool": show_script_tool,
    "NotePad": show_notepad,
    "Manajemen API": show_api_key_manager,
}

if menu == "Logout":
    for key in ["logged_in", "appkey", "authkey"]:
        st.session_state.pop(key, None)
    st.success("✅ Logout berhasil! Sampai jumpa.")
    st.rerun()
else:
    pages.get(menu, lambda: st.warning("Halaman tidak ditemukan"))()

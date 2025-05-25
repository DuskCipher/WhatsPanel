# tools/api_key_manager.py

import streamlit as st

# Inisialisasi session state untuk appkey dan authkey
if "appkey" not in st.session_state:
    st.session_state["appkey"] = ""
if "authkey" not in st.session_state:
    st.session_state["authkey"] = ""

def show_api_key_manager():
    st.markdown("""
        <style>
        .api-title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: white;
            margin-bottom: 25px;
        }
        </style>
        <div class="api-title">🔐 MANAJEMEN API KEY / TOKEN</div>
    """, unsafe_allow_html=True)

    st.caption("Masukkan dan kelola `App Key` dan `Auth Key` kamu dengan aman.")

    def token_input(label, key_name):
        with st.expander(f"🔑 {label}", expanded=True):
            token_value = st.text_input(
                f"{label}",
                value=st.session_state[key_name],
                key=f"input_{key_name}",
                type="password" if key_name == "authkey" else "default"
            )

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"💾 Simpan", key=f"save_{key_name}"):
                    st.session_state[key_name] = token_value
                    st.success(f"{label} berhasil disimpan!")

            with col2:
                if st.button(f"📋 Salin", key=f"copy_{key_name}"):
                    st.code(st.session_state[key_name]) 
                    st.success(f"{label} disalin!")

            with col3:
                if st.button(f"❌ Hapus", key=f"delete_{key_name}"):
                    st.session_state[key_name] = ""
                    st.warning(f"{label} dihapus.")

    token_input("App Key", "appkey")
    token_input("Auth Key", "authkey")
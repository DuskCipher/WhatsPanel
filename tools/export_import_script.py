# tools/export_import_script.py

import streamlit as st
import os
from datetime import datetime
from pathlib import Path

SCRIPT_FOLDER = "scripts"
os.makedirs(SCRIPT_FOLDER, exist_ok=True)


def show_export_import_script():
    st.markdown("""
        <style>
        .export-title {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: #ffffff;
            text-transform: uppercase;
            margin-bottom: 25px;
        }
        </style>
        <div class='export-title'>📤📥 EXPORT / IMPORT SCRIPT</div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["⬆️ Export Script", "⬇️ Import Script"])

    with tab1:
        st.subheader("📤 Export Script dari Folder")
        file_list = [f for f in os.listdir(SCRIPT_FOLDER) if f.endswith(".py")]

        if not file_list:
            st.info("Tidak ada file .py di folder 'scripts'.")
        else:
            selected_file = st.selectbox("Pilih file untuk diunduh:", file_list)
            full_path = os.path.join(SCRIPT_FOLDER, selected_file)

            with open(full_path, "r", encoding="utf-8") as f:
                file_data = f.read()

            st.code(file_data, language="python")
            st.download_button("📥 Download Script", file_data, file_name=selected_file, mime="text/x-python")

    with tab2:
        st.subheader("📥 Import Script ke Folder")
        uploaded = st.file_uploader("Unggah file .py", type=["py"])
        if uploaded:
            save_path = Path(SCRIPT_FOLDER) / uploaded.name
            with open(save_path, "wb") as f:
                f.write(uploaded.read())
            st.success(f"✅ Berhasil diunggah: {uploaded.name}")

            if st.checkbox("📄 Lihat isi script"):
                content = open(save_path, "r", encoding="utf-8").read()
                st.code(content, language="python")

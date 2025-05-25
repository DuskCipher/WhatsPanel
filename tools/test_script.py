import streamlit as st
import contextlib
import io
import traceback
import time
from datetime import datetime
from pathlib import Path

def is_code_safe(code: str):
    """Cek apakah script aman (tidak mengandung perintah berbahaya)"""
    blacklist = ["import os", "subprocess", "eval", "exec(", "open(", "Path(", "shutil", "remove", "rmdir"]
    return [b for b in blacklist if b in code]

def show_test_script():
    st.markdown("""
        <style>
        .utility-title {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: #ffffff;
            text-transform: uppercase;
            margin-bottom: 25px;
        }
        </style>
        <div class='utility-title'>🧪 TEST SCRIPT LANGSUNG</div>
    """, unsafe_allow_html=True)

    option = st.radio("📂 Input dari:", ["Tulis Manual", "Upload File"], horizontal=True)

    if option == "Tulis Manual":
        code_input = st.text_area("📝 Script Python", height=300, placeholder="contoh: print('Hello World')")
    else:
        uploaded_file = st.file_uploader("📁 Upload file Python (.py)", type=["py"])
        code_input = ""
        if uploaded_file:
            code_input = uploaded_file.read().decode("utf-8")
            st.code(code_input, language="python")

    if st.button("🚀 Jalankan Script", use_container_width=True):
        if not code_input.strip():
            st.warning("⚠️ Script tidak boleh kosong.")
            return

        unsafe_found = is_code_safe(code_input)
        if unsafe_found:
            st.error("🚫 Script mengandung perintah yang tidak diperbolehkan:")
            st.code("\n".join(unsafe_found))
            return

        output_buffer = io.StringIO()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_time = time.time()

        try:
            with contextlib.redirect_stdout(output_buffer):
                exec(code_input, {})
            exec_time = time.time() - start_time
            result = output_buffer.getvalue()

            log_path = Path("logs")
            log_path.mkdir(exist_ok=True)
            log_file = log_path / f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            log_file.write_text(f"Time: {timestamp}\nExecution Time: {exec_time:.4f} seconds\n\nCode:\n{code_input}\n\nOutput:\n{result}")

            if result.strip():
                st.success(f"✅ Output Script ({timestamp})")
                st.code(result)
            else:
                st.info("ℹ️ Script dieksekusi tanpa output.")
            st.caption(f"⏱️ Waktu eksekusi: {exec_time:.4f} detik")
            st.caption(f"📤 Hasil log disimpan: `{log_file}`")

        except Exception:
            st.error(f"❌ Terjadi kesalahan saat menjalankan script ({timestamp}):")
            st.code(traceback.format_exc())
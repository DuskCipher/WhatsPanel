import streamlit as st
import subprocess
import platform
from io import StringIO


def show_terminal():
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
        <div class="api-title">🖥️ TERMINAL INTERAKTIF ALL OS</div>
    """, unsafe_allow_html=True)
    st.markdown("Masukkan perintah terminal untuk dieksekusi secara interaktif. Sistem akan mendeteksi OS secara otomatis.")

    current_os = platform.system()
    st.info(f"🧠 Sistem Operasi terdeteksi: **{current_os}**")

    # Inisialisasi session state
    if "terminal_history" not in st.session_state:
        st.session_state.terminal_history = []
    if "terminal_output" not in st.session_state:
        st.session_state.terminal_output = ""

    # Pilihan perintah dari histori
    if st.session_state.terminal_history:
        selected_history = st.selectbox("📜 Pilih dari histori perintah:", reversed(st.session_state.terminal_history))
        if st.button("🔁 Jalankan Ulang Perintah Histori"):
            st.session_state["current_input"] = selected_history
    else:
        st.session_state["current_input"] = ""

    # Input multi-line
    terminal_cmd = st.text_area("💬 Ketik perintah terminal:", value=st.session_state.get("current_input", ""), height=120)

    # Tombol eksekusi
    if st.button("▶️ Jalankan") and terminal_cmd:
        blocked = ["rm", "shutdown", "poweroff", "reboot", "curl", "wget", "pip uninstall"]
        if any(b in terminal_cmd for b in blocked):
            st.error("❌ Perintah berbahaya terdeteksi dan diblokir.")
            st.stop()

        try:
            if current_os == "Windows":
                result = subprocess.run(terminal_cmd, shell=True, capture_output=True, text=True, timeout=20)
            else:
                result = subprocess.run(["bash", "-c", terminal_cmd], capture_output=True, text=True, timeout=20)

            stdout = result.stdout or "(tidak ada output)"
            stderr = result.stderr

            st.session_state.terminal_history.append(terminal_cmd)
            st.session_state.terminal_output = stdout

            with st.expander("📤 Output" + (" (STDERR ada)" if stderr else ""), expanded=True):
                st.code(stdout, language="bash")
                if stderr:
                    st.error(stderr)

            # Unduh Output
            buffer = StringIO(stdout)
            st.download_button("⬇️ Unduh Output", buffer, file_name="terminal_output.txt", mime="text/plain")

        except subprocess.TimeoutExpired:
            st.error("⏱️ Timeout: Perintah terlalu lama dijalankan.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    # Bersihkan output
    if st.button("🧹 Bersihkan Output"):
        st.session_state.terminal_output = ""
        st.success("✅ Output dibersihkan.")

    # Tips umum
    st.markdown("""
    <hr>
    <small>💡 Contoh perintah bermanfaat:<br>
    - `ls -la` atau `dir`<br>
    - `whoami`<br>
    - `df -h`<br>
    - `ping google.com`</small>
    """, unsafe_allow_html=True)
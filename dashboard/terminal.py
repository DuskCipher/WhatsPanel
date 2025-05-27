import streamlit as st
import subprocess
import platform
import socket

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

    if "terminal_history" not in st.session_state:
        st.session_state.terminal_history = []
    if "terminal_output" not in st.session_state:
        st.session_state.terminal_output = ""

    if st.session_state.terminal_history:
        selected_history = st.selectbox("📜 Pilih dari histori perintah:", reversed(st.session_state.terminal_history))
        if st.button("🔁 Jalankan Ulang Perintah Histori"):
            st.session_state["current_input"] = selected_history
    else:
        st.session_state["current_input"] = ""

    terminal_cmd = st.text_area("💬 Ketik perintah terminal:", value=st.session_state.get("current_input", ""), height=120)

    if st.button("▶️ Jalankan") and terminal_cmd:
        try:
            if terminal_cmd.startswith("getip "):
                domain = terminal_cmd.split(" ", 1)[1]
                ip = socket.gethostbyname(domain)
                stdout = f"IP address dari {domain}: {ip}"
                stderr = ""
            else:
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

            # Perbaikan tombol download
            st.download_button("⬇️ Unduh Output", stdout.encode("utf-8"), file_name="terminal_output.txt", mime="text/plain")

        except socket.gaierror:
            st.error(f"❌ Domain tidak valid atau tidak bisa di-resolve: {terminal_cmd}")
        except subprocess.TimeoutExpired:
            st.error("⏱️ Timeout: Perintah terlalu lama dijalankan.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    if st.button("🧹 Bersihkan Output"):
        st.session_state.terminal_output = ""
        st.success("✅ Output dibersihkan.")

    st.markdown("""
    <hr>
    <small>💡 Contoh perintah:<br>
    - `ls -la` atau `dir`<br>
    - `getip google.com`<br>          
    - `whoami`<br>
    - `df -h`<br>
    - `getip google.com` (pengganti nslookup/ping)<br>
    - `uname -a`</small>
    """, unsafe_allow_html=True)

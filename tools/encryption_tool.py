import streamlit as st
from cryptography.fernet import Fernet

def show_encryption_tool():
    st.markdown("""
    <style>
    .encrypt-box {
        background-color: #1e1e2f;
        padding: 35px 40px;
        border-radius: 16px;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.35);
        color: white;
        margin-top: 20px;
    }
    .stTextInput input, .stTextArea textarea {
        background-color: #2b2f3f;
        color: white;
        border-radius: 8px;
        border: 1px solid #444;
        padding: 10px;
    }
    .stRadio > div {
        background-color: #2b2f3f;
        border-radius: 12px;
        padding: 12px;
        color: white;
    }
    .result-box {
        background-color: #0e1117;
        padding: 15px;
        border-radius: 10px;
        font-family: monospace;
        font-size: 0.85rem;
        color: #39ff14;
        overflow-x: auto;
        margin-top: 15px;
    }
    .copy-button {
        background-color: #00ffe0;
        border: none;
        color: #000;
        padding: 6px 12px;
        font-size: 0.8rem;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 8px;
    }
    .copy-button:hover {
        background-color: #00cfc0;
    }
    </style>
    <script>
    function copyToClipboard(text) {
        navigator.clipboard.writeText(text);
        alert("📋 Teks berhasil disalin ke clipboard!");
    }
    </script>
    """, unsafe_allow_html=True)

    st.subheader("🔐 AES-like Script Encryption / Decryption")

    if "encryption_key" not in st.session_state:
        st.session_state.encryption_key = Fernet.generate_key()

    key_display = st.session_state.encryption_key.decode()
    st.text_input("Kunci Enkripsi", value=key_display, type="password", key="visible_key")

    fernet = Fernet(st.session_state.encryption_key)

    st.subheader("⚙️ Sistem Operasi")
    operation = st.radio("Pilih Enkripsi", ["Encrypt", "Decrypt"], horizontal=True)

    st.markdown("### 📝 Masukkan Teks Anda")
    input_text = st.text_area("", height=160)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Jalankan", use_container_width=True):
            if not input_text.strip():
                st.warning("❗ Teks tidak boleh kosong.")
            else:
                try:
                    if operation == "Encrypt":
                        encrypted = fernet.encrypt(input_text.encode()).decode()
                        st.success("✅ Hasil Enkripsi")
                        st.markdown(f"""
                            <div class='result-box' id='output-text'>{encrypted}</div>
                            <button class='copy-button' onclick="copyToClipboard(`{encrypted}`)">📋 Salin</button>
                        """, unsafe_allow_html=True)
                    else:
                        decrypted = fernet.decrypt(input_text.encode()).decode()
                        st.success("✅ Hasil Dekripsi")
                        st.markdown(f"""
                            <div class='result-box' id='output-text'>{decrypted}</div>
                            <button class='copy-button' onclick="copyToClipboard(`{decrypted}`)">📋 Salin</button>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Gagal memproses teks: {e}")

    with col2:
        st.markdown("""
            <div style='background-color:#2c2f3f;padding:18px 20px;border-radius:10px;margin-top:5px;box-shadow:inset 0 0 5px #00000055'>
                <p style='color:#aaa;font-size:14px;margin-bottom:10px'>
                    <strong>ℹ️ Apa ini?</strong> <span style='color:#ccc'>Kunci ini digunakan untuk proses enkripsi dan dekripsi. Simpan dengan aman.</span>
                </p>
        """, unsafe_allow_html=True)

        if st.button("🔁 Generate Key Baru", use_container_width=True):
            st.session_state.encryption_key = Fernet.generate_key()
            st.rerun()

        st.markdown(f"""
            <div style='margin-top:18px'>
                <p style='color:#00ffe0;font-size:13px;margin-bottom:4px'>📄 Current Key:</p>
                <code id="keytext" style="word-wrap:break-word;color:#00ffe0">{key_display}</code><br><br>
                <button class="copy-button" onclick="copyToClipboard('{key_display}')">📋 Copy Key</button>
            </div>
            </div>
        """, unsafe_allow_html=True)
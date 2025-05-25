import streamlit as st
import os
import base64
from datetime import datetime

def show_notepad():
    st.markdown("""
        <style>
        .analyzer-title {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: #ffffff;
            text-transform: uppercase;
            margin-bottom: 25px;
        }
        </style>
        <div class='analyzer-title'>📝 NOTEPAD DUSKCIPHER 0.1</div>
    """, unsafe_allow_html=True)
    st.markdown("Gunakan notepad ini untuk mencatat ide, pesan, atau apapun yang dibutuhkan secara lokal.")

    # Folder penyimpanan catatan
    notes_folder = os.path.join(os.getcwd(), "catatan_streamlit")
    os.makedirs(notes_folder, exist_ok=True)

    # Dapatkan semua file catatan yang ada
    all_notes = [f for f in os.listdir(notes_folder) if f.endswith(".txt")]

    # Pilih catatan yang sudah ada atau buat baru
    selected_file = st.selectbox("📂 Pilih catatan", options=all_notes + ["📄 Buat catatan baru..."])

    if selected_file == "📄 Buat catatan baru...":
        new_filename = st.text_input("📝 Nama file baru (contoh: catatan_hari_ini.txt)")
        note_file = os.path.join(notes_folder, new_filename) if new_filename else None
    else:
        note_file = os.path.join(notes_folder, selected_file)

    # Checkbox Auto-Save
    auto_save = st.checkbox("💾 Aktifkan Auto-Save", value=False)

    # Load isi file jika sudah ada
    content = ""
    if note_file and os.path.exists(note_file):
        with open(note_file, "r", encoding="utf-8") as f:
            content = f.read()

    # Styling untuk textarea gelap
    st.markdown("""
        <style>
        textarea {
            background-color: #202020 !important;
            color: #FFFFFF !important;
            font-size: 16px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Textarea untuk mengedit catatan
    updated_content = st.text_area("✏️ Tulis catatan Anda di sini:", value=content, height=350)

    # Simpan manual
    if st.button("💾 Simpan Sekarang"):
        if note_file:
            with open(note_file, "w", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] Auto-generated\n")
                f.write(updated_content + "\n\n" + timestamp)
            st.success("✅ Catatan berhasil disimpan.")

    # Simpan otomatis jika auto-save aktif
    if auto_save and note_file:
        with open(note_file, "w", encoding="utf-8") as f:
            f.write(updated_content)

    # Hapus catatan
    if note_file and os.path.exists(note_file):
        if st.button("🗑 Hapus Catatan Ini"):
            os.remove(note_file)
            st.success("❌ Catatan dihapus.")
            st.experimental_rerun()

    # Unduh file catatan
    if note_file and os.path.exists(note_file):
        with open(note_file, "r", encoding="utf-8") as f:
            file_data = f.read()
            b64 = base64.b64encode(file_data.encode()).decode()
            file_name = os.path.basename(note_file)
            href = f'<a href="data:file/txt;base64,{b64}" download="{file_name}">⬇️ Unduh Catatan: {file_name}</a>'
            st.markdown(href, unsafe_allow_html=True)

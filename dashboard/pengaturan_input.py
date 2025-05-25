import streamlit as st
import pandas as pd
from dashboard.import_cloudinary import import_cloudinary
import cloudinary.uploader

def show_pengaturan_input():
    import_cloudinary() 

    st.title("📱 Dashboard WhatsPanel Blasting Version 2.1")
    st.markdown(
        "Versi interaktif menggunakan API WA Panel dengan Excel, input manual, dan dukungan gambar."
    )

    # Bagian Pengaturan Pesan
    st.subheader("📝 Pengaturan Pesan")
    st.session_state.message_template = st.text_area(
        "✏️ Template Pesan (gunakan {nama})",
        "Halo {nama}, ini adalah pesan testing dari WA API via Python.",
    )
    st.session_state.delay_input = st.number_input(
        "⏱️ Jeda antar pesan (detik)",
        min_value=1,
        value=5,
        step=1
    )

    # Upload Gambar Opsional
    with st.expander("🖼️ Upload Gambar (Opsional)", expanded=False):
        st.session_state.image_file = st.file_uploader(
            "Unggah Gambar", type=["jpg", "jpeg", "png"]
        )
        st.session_state.caption = st.text_area(
            "📎 Caption untuk Gambar (gunakan {nama})",
            "Hai {nama}, ini gambar untukmu."
        )

    # Upload Excel
    with st.expander("📤 Upload File Excel", expanded=False):
        uploaded_file = st.file_uploader(
            "Unggah file Excel (.xlsx) berisi kolom: Nama, Nomor",
            type=["xlsx"]
        )
        if uploaded_file:
            st.session_state.data_excel = pd.read_excel(uploaded_file)
            st.success("✅ Data berhasil diunggah!")

    # Tambah Manual
    with st.expander("📥 Tambah Nomor Manual", expanded=False):
        with st.form("manual_form"):
            nama_manual = st.text_input("Nama")
            nomor_manual = st.text_input("Nomor (format: 62xxx)")
            submit = st.form_submit_button("➕ Tambahkan")

            if submit:
                if nama_manual and nomor_manual:
                    st.session_state.manual_data.append({
                        "Nama": nama_manual,
                        "Nomor": nomor_manual
                    })
                    st.success("✅ Ditambahkan")
                else:
                    st.warning("⚠️ Nama dan Nomor wajib diisi.")

    # Tampilkan Data Manual (jika ada)
    if st.session_state.manual_data:
        df_manual = pd.DataFrame(st.session_state.manual_data)
        st.markdown("### 📄 Data Manual")
        st.dataframe(df_manual)

        csv_manual = df_manual.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Manual CSV",
            csv_manual,
            "data_manual.csv",
            "text/csv"
        )

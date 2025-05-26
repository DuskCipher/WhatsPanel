# tools/tool_oli.py

import streamlit as st
import pandas as pd
import requests
import time

# Simpan data manual di session_state
if "manual_data" not in st.session_state:
    st.session_state.manual_data = []

def show_tool_oli():
    # ====[ JUDUL ]====
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
        <div class="api-title">💬 Kirim Pesan WhatsApp Khusus Blasting Oli</div>
    """, unsafe_allow_html=True)

    # ====[ CEK KEY ]====
    if not st.session_state.appkey or not st.session_state.authkey:
        st.error("❌ App Key dan Auth Key tidak ditemukan. Silakan login ulang.")
        st.stop()

    # ====[ FUNGSI KIRIM PESAN ]====
    def kirim_pesan_oli(nomor, pesan):
        payload = {
            "appkey": st.session_state.appkey,
            "authkey": st.session_state.authkey,
            "to": nomor,
            "message": pesan
        }
        try:
            response = requests.post("https://app.wapanels.com/api/create-message", json=payload)
            if response.status_code == 200:
                return "✅ Sukses", response.text
            else:
                return f"❌ Gagal ({response.status_code})", response.text
        except Exception as e:
            return "❌ Error", str(e)

    # ====[ PETUNJUK TEMPLATE ]====
    st.markdown("""
    #### 🔁 Placeholder yang tersedia:
    - `{nama}`
    - `{jenis}`
    - `{mobil}`
    - `{tanggal_kunjungan}`
    - `{kilometer}`
    """)

    # ====[ TEMPLATE PESAN ]====
    template_text = st.text_area("📄 Template Pesan", height=400, value="""
🚗 Selamat pagi *{jenis} {nama}*,

Semoga sehat selalu dan mobil *{jenis} {nama}* dalam kondisi terbaik. Aamiin.

Kami mengingatkan bahwa servis terakhir dilakukan pada *{tanggal_kunjungan}* di km *{kilometer}* di Bengkel Arumsari Purwokerto.

Saatnya ganti oli agar mesin tetap awet dan performa optimal. Yuk booking servis online sesuai jadwal Anda!

📍 Arumsari – Jl. Sultan Agung, Purwokerto  
📞 0852-2148-6500  
📅 Booking: https://bengkelarumsari.com/booking-wa-as  
📖 Artikel: https://bengkelkakimobil.com/telat-ganti-oli-mobil-ini-resikonya/

Terima kasih atas kepercayaan *{jenis} {nama}* 💙
    """.strip())

    # ====[ INPUT JEDA KIRIM ]====
    jeda = st.number_input("⏳ Jeda antar pesan (detik)", min_value=0.0, value=1.0, step=0.5)

    st.divider()

    # ====[ INPUT MANUAL DATA ]====
    st.subheader("✍️ Input Data Manual")
    with st.form("manual_form", clear_on_submit=True):
        nama = st.text_input("Nama")
        jenis = st.text_input("Jenis Mobil")
        mobil = st.text_input("Tipe Mobil")
        tanggal_kunjungan = st.date_input("Tanggal Kunjungan")
        kilometer = st.number_input("Kilometer", step=100)
        nomor = st.text_input("Nomor WhatsApp (cth: 081234xxxx)")

        submitted = st.form_submit_button("➕ Tambah ke Daftar")
        if submitted:
            st.session_state.manual_data.append({
                "nama": nama,
                "jenis": jenis,
                "mobil": mobil,
                "tanggal_kunjungan": tanggal_kunjungan.strftime("%Y-%m-%d"),
                "kilometer": kilometer,
                "nomor": nomor
            })
            st.success("✅ Data berhasil ditambahkan.")

    # ====[ TABEL EDIT & HAPUS DATA MANUAL ]====
    if st.session_state.manual_data:
        df_manual = pd.DataFrame(st.session_state.manual_data)

        st.subheader("📋 Data Manual yang Telah Diinput")
        edited_df = st.data_editor(df_manual, num_rows="dynamic", use_container_width=True, key="editor")

        if st.button("🗑 Hapus Semua Data"):
            st.session_state.manual_data.clear()
            st.success("✅ Semua data manual dihapus.")
        else:
            st.session_state.manual_data = edited_df.to_dict("records")

    st.divider()

    # ====[ INPUT FILE EXCEL ]====
    st.subheader("📎 Upload File Excel")
    uploaded_file = st.file_uploader("Unggah file Excel (.xlsx)", type=["xlsx"])
    df_excel = None

    if uploaded_file:
        df_excel = pd.read_excel(uploaded_file)
        required_cols = {'nama', 'jenis', 'mobil', 'tanggal_kunjungan', 'kilometer', 'nomor'}
        if not required_cols.issubset(df_excel.columns):
            st.error("❌ File Excel tidak sesuai format.")
            df_excel = None
        else:
            st.success("✅ Data dari Excel berhasil dimuat.")
            st.dataframe(df_excel)

    # ====[ GABUNGKAN DATA MANUAL + EXCEL ]====
    total_data = []
    if st.session_state.manual_data:
        total_data.extend(st.session_state.manual_data)
    if df_excel is not None:
        total_data.extend(df_excel.to_dict("records"))

    # ====[ KIRIM SEMUA PESAN ]====
    if total_data:
        st.subheader("🚀 Kirim Pesan ke Semua Kontak")
        if st.button("📤 Kirim Sekarang"):
            log = []
            for row in total_data:
                try:
                    pesan = template_text.format(
                        nama=row["nama"],
                        jenis=row["jenis"],
                        mobil=row["mobil"],
                        tanggal_kunjungan=row["tanggal_kunjungan"],
                        kilometer=row["kilometer"]
                    ).strip()

                    nomor = str(row["nomor"])
                    if nomor.startswith("0"):
                        nomor = "62" + nomor[1:]

                    status, res = kirim_pesan_oli(nomor, pesan)
                except Exception as e:
                    status = "❌ Error"
                    res = str(e)
                    pesan = f"[Template Error] {e}"

                log.append({
                    "Nama": row.get("nama"),
                    "Nomor": nomor,
                    "Status": status,
                    "Respon": res,
                    "Pesan": pesan[:60] + "..." if len(pesan) > 60 else pesan
                })

                time.sleep(jeda)

            df_log = pd.DataFrame(log)
            st.success("✅ Pengiriman selesai!")
            st.dataframe(df_log)

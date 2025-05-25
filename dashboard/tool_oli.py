import streamlit as st
import pandas as pd
import requests

def show_tool_oli():
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
    st.markdown("Masukkan template pesan di bawah dan unggah file Excel untuk mengirim pesan WhatsApp otomatis.")

    if not st.session_state.appkey or not st.session_state.authkey:
        st.error("❌ App Key dan Auth Key tidak ditemukan. Silakan login ulang.")
        st.stop()

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

    st.markdown("""
    #### 🔁 Placeholder yang tersedia:
    - `{nama}`
    - `{jenis}`
    - `{mobil}`
    - `{tanggal_kunjungan}`
    - `{kilometer}`
    """)

    template_text = st.text_area(
        "📄 Template Pesan",
        height=500,
        value="""
🚗 Selamat pagi *{jenis} {nama}*,

Semoga sehat selalu dan mobil *{jenis} {nama}* dalam kondisi terbaik. Aamiin.

Kami mengingatkan bahwa servis terakhir dilakukan pada *{tanggal_kunjungan}* di km *{kilometer}* di Bengkel Arumsari Purwokerto.

Saatnya ganti oli agar mesin tetap awet dan performa optimal. Yuk booking servis online sesuai jadwal Anda!

🔧 Layanan:
• Service Berkala 
• Ganti Oli 
• AC 
• Rem & Suspensi 
• Spooring 
• Scanner 
• Nano Coating

📍 Arumsari – Jl. Sultan Agung, Purwokerto  
📞 0852-2148-6500  
📅 Booking: https://bengkelarumsari.com/booking-wa-as  
📖 Artikel: https://bengkelkakimobil.com/telat-ganti-oli-mobil-ini-resikonya/

Terima kasih atas kepercayaan *{jenis} {nama}* 💙
        """.strip()
    )

    uploaded_file = st.file_uploader("📎 Upload File Excel (.xlsx) berisi data pelanggan", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        required_columns = {'nama', 'jenis', 'tanggal_kunjungan', 'mobil', 'kilometer', 'nomor'}
        if not required_columns.issubset(df.columns):
            st.error("❌ File Excel harus memiliki kolom: 'nama', 'jenis', 'tanggal_kunjungan', 'mobil', 'kilometer', 'nomor'")
        else:
            st.success("✅ File berhasil dimuat.")
            st.dataframe(df)

            st.markdown("### 🚀 Klik tombol di bawah untuk mengirim pesan ke semua pelanggan:")
            if st.button("📤 Kirim Semua Pesan Sekarang"):
                status_log = []
                for _, row in df.iterrows():
                    try:
                        message = str(template_text.format(
                            nama=row['nama'],
                            jenis=row['jenis'],
                            tanggal_kunjungan=row['tanggal_kunjungan'],
                            mobil=row['mobil'],
                            kilometer=row['kilometer']
                        )).strip()

                        if not message or message.lower() == 'nan':
                            raise ValueError("Pesan kosong atau tidak valid.")

                        nomor = str(row['nomor'])
                        if nomor.startswith("0"):
                            nomor = "62" + nomor[1:]

                        status, response = kirim_pesan_oli(nomor, message)
                    except Exception as e:
                        message = f"[Template Error] {str(e)}"
                        status = '❌ Gagal'
                        response = str(e)

                    status_log.append({
                        'nama': row.get('nama', ''),
                        'nomor': nomor,
                        'pesan': message,
                        'status': status,
                        'response': response
                    })

                result_df = pd.DataFrame(status_log)
                st.write("### 🧾 Hasil Pengiriman:")
                st.dataframe(result_df)
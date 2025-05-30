import time
import pandas as pd
from datetime import datetime
import streamlit as st
import cloudinary.uploader
from dashboard.utils import send_text_message, send_image_message
from dashboard.import_cloudinary import import_cloudinary

def is_response_success(response_detail):
    return (
        response_detail.get("status") == "success"
        or response_detail.get("response", {}).get("data", {}).get("to")
    )

def show_kirim_pesan():
    import_cloudinary()

    st.title("📱Dashboard WhatsPanel Blasting Version 2.1")
    st.markdown("Versi interaktif menggunakan API WA Panel dengan Excel, input manual, dan dukungan gambar.")

    data_excel = st.session_state.get("data_excel", pd.DataFrame())
    df_all = pd.concat([
        data_excel, pd.DataFrame(st.session_state.manual_data)
    ], ignore_index=True)

    if not df_all.empty:
        st.warning("⚠️ Jangan berpindah tab selama proses pengiriman berlangsung.")
        st.subheader("🚀 Kirim Pesan Otomatis")

        if st.button("📨 Mulai Kirim Pesan"):
            with st.spinner("Mengirim pesan..."):
                log = []
                image_url = None
                image_file = st.session_state.get("image_file")

                if image_file:
                    upload_result = cloudinary.uploader.upload(
                        image_file, folder="whatsapp_uploads"
                    )
                    image_url = upload_result.get("secure_url")

                progress_bar = st.progress(0, text="Memulai pengiriman...")
                total = len(df_all)

                for idx, row in df_all.iterrows():
                    nama, nomor = row["Nama"], row["Nomor"]
                    msg = st.session_state.message_template.replace("{nama}", nama)
                    cap = st.session_state.caption.replace("{nama}", nama)

                    if image_file and image_url:
                        status_flag, response_detail = send_image_message(
                            nomor, cap, image_url,
                            st.session_state.appkey, st.session_state.authkey
                        )
                        pesan = cap
                    else:
                        status_flag, response_detail = send_text_message(
                            nomor, msg,
                            st.session_state.appkey, st.session_state.authkey
                        )
                        pesan = msg

                    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if status_flag or is_response_success(response_detail):
                        status = "Berhasil"
                        warna_status = "#22c55e"
                        icon = "✅"
                        error_detail = ""
                    else:
                        status = f"Gagal - {response_detail.get('error', 'Tidak diketahui')}"
                        warna_status = "#ef4444"
                        icon = "❌"
                        error_detail = str(response_detail)

                    st.markdown(f"""
                        <div style="
                            background: #262626;
                            border-left: 5px solid {warna_status};
                            padding: 10px 15px;
                            margin: 8px 0;
                            border-radius: 10px;
                            font-family: 'Segoe UI', sans-serif;
                            color: white;
                            box-shadow: 0 0 5px rgba(0,0,0,0.2);
                        ">
                            <div style="color: #9ca3af; font-size: 13px;">🕒 {waktu}</div>
                            <div style="margin-top: 5px;">
                                <span style="color: {warna_status}; font-weight: bold; font-size: 15px;">{icon} {status}</span>
                                <span style="color: #e5e7eb; font-size: 15px;"> ke <strong>{nama}</strong> (<code>{nomor}</code>)</span><br>
                                <span style="color: #f87171; font-size: 13px;">{error_detail}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    log.append({
                        "Waktu": waktu,
                        "Nama": nama,
                        "Nomor": nomor,
                        "Pesan": pesan,
                        "Status": status,
                    })

                    progress_bar.progress(
                        (idx + 1) / total,
                        text=f"{int((idx + 1) / total * 100)}% selesai"
                    )
                    time.sleep(st.session_state.delay_input)

                st.session_state.log_df = pd.DataFrame(log)

                if all(["✅ Berhasil" in l["Status"] for l in log]):
                    st.success("✅ Semua pesan telah dikirim!")
                else:
                    st.warning("⚠️ Beberapa pesan gagal dikirim. Silakan periksa log di bawah.")

                st.subheader("📋 Log Pengiriman")
                styled_log = st.session_state.log_df.style.applymap(
                    lambda x: "color: green;" if x == "✅ Berhasil" else "color: red;",
                    subset=["Status"]
                )
                st.dataframe(styled_log, use_container_width=True)

                csv_log = st.session_state.log_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download Log CSV",
                    data=csv_log,
                    file_name="log_pengiriman.csv",
                    mime="text/csv"
                )
    else:
        st.warning("⚠️ Data kosong. Silakan upload file Excel atau masukkan nomor manual terlebih dahulu.")

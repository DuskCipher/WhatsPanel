
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF

def show_analisis_pengiriman():
    # ====[ HEADER & STYLING ]====
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
        <div class="api-title">Analisis Pengiriman & Laporan</div>
    """, unsafe_allow_html=True)

    # ====[ CEK KETERSEDIAAN DATA ]====
    log_df = st.session_state.get("log_df", pd.DataFrame())
    if log_df.empty:
        st.warning("⚠️ Belum ada data pengiriman untuk dianalisis.")
        return

    # ====[ NORMALISASI STATUS DAN STATISTIK ]====
    st.subheader("📊 Ringkasan Statistik Pengiriman")
    log_df['Status_Normalized'] = log_df['Status'].str.lower().str.strip()

    berhasil = sum(log_df['Status_Normalized'].str.contains("✅|berhasil", na=False))
    gagal = sum(log_df['Status_Normalized'].str.contains("❌|gagal", na=False))
    total = len(log_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("📨 Total Pesan", total)
    col2.metric("✅ Berhasil", berhasil, delta_color="normal")
    col3.metric("❌ Gagal", gagal, delta_color="inverse")
    st.divider()

    # ====[ GRAFIK BAR BERHASIL VS GAGAL ]====
    st.subheader("📊 Grafik Bar: Jumlah Berhasil vs Gagal")
    fig_bar = go.Figure(data=[
        go.Bar(
            x=["Berhasil", "Gagal"],
            y=[berhasil, gagal],
            marker_color=["#22c55e", "#ef4444"],
            text=[berhasil, gagal],
            textposition="auto"
        )
    ])
    fig_bar.update_layout(
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        font_color="white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ====[ DIAGRAM PIE ]====
    st.subheader("🥧 Diagram Pie")
    pie_fig = px.pie(
        names=["Berhasil", "Gagal"],
        values=[berhasil, gagal],
        color_discrete_sequence=["#22c55e", "#ef4444"],
        hole=0.4
    )
    pie_fig.update_layout(paper_bgcolor="#111111", font_color="white")
    st.plotly_chart(pie_fig, use_container_width=True)

    # ====[ TIMELINE PENGIRIMAN ]====
    st.subheader("⏱️ Timeline Pengiriman")
    log_df['Waktu'] = pd.to_datetime(log_df['Waktu'], errors='coerce')
    fig_time = px.scatter(
        log_df,
        x="Waktu",
        y="Status",
        color="Status",
        hover_data=["Nama", "Nomor"],
        color_discrete_map={
            "✅ Berhasil": "#22c55e",
            "❌ Gagal": "#ef4444"
        }
    )
    fig_time.update_layout(paper_bgcolor="#111111", font_color="white")
    st.plotly_chart(fig_time, use_container_width=True)

    # ====[ FITUR EKSPOR: CSV & PDF ]====
    st.subheader("📁 Unduh Data Log")
    col_csv, col_pdf = st.columns(2)

    with col_csv:
        csv_data = log_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download CSV",
            data=csv_data,
            file_name="log_pengiriman.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col_pdf:
        if st.button("📄 Generate PDF Laporan", use_container_width=True):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Laporan Pengiriman WA", ln=True, align='C')
            pdf.ln(10)

            for _, row in log_df.iterrows():
                waktu = row.get('Waktu', '')
                status = row.get('Status', '')
                nama = row.get('Nama', '')
                nomor = row.get('Nomor', '')
                pdf.multi_cell(0, 10, txt=f"[{waktu}] {status} - {nama} ({nomor})", align='L')

            pdf_output = "/mnt/data/laporan_pengiriman.pdf"
            pdf.output(pdf_output)

            with open(pdf_output, "rb") as f:
                st.download_button(
                    "⬇️ Download PDF",
                    data=f.read(),
                    file_name="laporan_pengiriman.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

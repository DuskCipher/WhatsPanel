import streamlit as st

# ====[ INISIALISASI SESSION STATE ]====
# Pastikan session_state memiliki kunci "appkey" dan "authkey"
for key in ["appkey", "authkey"]:
    st.session_state.setdefault(key, "")

# ====[ FUNGSI UTAMA: MANAJEMEN API KEY ]====
def show_api_key_manager():
    # ====[ TAMPILKAN JUDUL HALAMAN DENGAN GAYA ]====
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
        <div class="api-title">🔐 MANAJEMEN API KEY / TOKEN</div>
    """, unsafe_allow_html=True)

    st.caption("Masukkan dan kelola `App Key` dan `Auth Key` kamu dengan aman.")

    # ====[ FUNGSI INPUT TOKEN & TOMBOL AKSI ]====
    def token_input(label, key_name):
        with st.expander(f"🔑 {label}", expanded=True):
            # ====[ INPUT TOKEN ]====
            token_value = st.text_input(
                label,
                value=st.session_state[key_name],
                key=f"input_{key_name}",
                type="password" if key_name == "authkey" else "default"
            )

            # ====[ TOMBOL AKSI: SIMPAN / SALIN / HAPUS ]====
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("💾 Simpan", key=f"save_{key_name}"):
                    st.session_state[key_name] = token_value
                    st.success(f"{label} berhasil disimpan!")

            with col2:
                if st.button("📋 Salin", key=f"copy_{key_name}"):
                    st.code(st.session_state[key_name])
                    st.success(f"{label} disalin!")

            with col3:
                if st.button("❌ Hapus", key=f"delete_{key_name}"):
                    st.session_state[key_name] = ""
                    st.warning(f"{label} dihapus.")

    # ====[ FORM UNTUK APP KEY & AUTH KEY ]====
    token_input("App Key", "appkey")
    token_input("Auth Key", "authkey")

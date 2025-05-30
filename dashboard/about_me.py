import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def show_about_me():
    st.title("🧠 Tentang Kami")
    st.markdown("Kolaborasi dua pengembang teknologi yang membangun sistem otomasi modern dan efisien.")

    col1, col2 = st.columns(2)

    with col1:
        st.header("👨‍💻 PMC Cyber")
        st.markdown("""
        **PMC-Cyber** adalah pengembang sistem automasi dan pengelolaan API yang aktif dalam membangun aplikasi berbasis Python dan integrasi WhatsApp API.

        - 🔧 Proyek utama: `PMC-Cyber`
        - 📂 Fitur: Automasi, Terminal Interaktif, WhatsApp Bot
        - 📌 Bahasa: Python, Shell Script

        🔗 [GitHub: PMC-Cyber](https://github.com/PMC-Cyber)
        """)

        try:
            pmc_img_url = "https://avatars.githubusercontent.com/u/104304973?v=4"
            pmc_img = Image.open(BytesIO(requests.get(pmc_img_url).content))
            st.image(pmc_img, caption="PMC Cyber", width=150)
        except:
            st.warning("Profil PMC Cyber gagal dimuat.")

    with col2:
        st.header("👨‍💻 DuskCipher")
        st.markdown("""
        **DuskCipher** adalah developer yang fokus pada analisis data, sistem AI, dan backend engineering, dengan beberapa proyek NLP dan data science.

        - 🧠 Fokus: Backend, Data Science, NLP
        - 📂 Tools: Python, FastAPI, Pandas, Streamlit
        - 🎯 Kontribusi: Otomasi & Integrasi AI

        🔗 [GitHub: DuskCipher](https://github.com/DuskCipher)
        """)

        try:
            dusk_img_url = "https://avatars.githubusercontent.com/u/65213343?v=4"
            dusk_img = Image.open(BytesIO(requests.get(dusk_img_url).content))
            st.image(dusk_img, caption="DuskCipher", width=150)
        except:
            st.warning("Profil DuskCipher gagal dimuat.")

    st.markdown("---")
    st.markdown("""
    🚀 **Proyek ini adalah hasil kolaborasi antara PMC-Cyber & DuskCipher**,  
    dua kreator yang berkomitmen untuk membangun aplikasi open-source yang bermanfaat dan scalable.

    Terima kasih telah berkunjung ke dashboard kami! ❤️
    """)

if __name__ == "__main__":
    show_about_me()
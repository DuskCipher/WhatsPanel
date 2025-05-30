import streamlit as st

def show_about_me():
    st.title("🧠 Tentang Kami")
    st.markdown("""
    Selamat datang! Kami adalah dua pengembang teknologi yang berkolaborasi  
    untuk membangun sistem **otomasi modern**, **berbasis AI**, dan **efisien**.  
    Kami percaya pada kekuatan *open source* dan inovasi berkelanjutan. ✨
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👨‍💻 PMC Cyber")
        st.markdown("""
        `PMC-Cyber` adalah seorang **pengembang sistem automasi dan integrasi API**,  
        dengan spesialisasi pada *command-line tools*, WhatsApp Bot, dan sistem backend.

        **🔧 Keahlian:**
        - Automasi sistem & API handler
        - Integrasi WhatsApp API
        - Terminal tools interaktif berbasis Python & Shell

        **🧰 Tools:** Python, Shell Script, Linux CLI  
        **🔗 GitHub:** [PMC-Cyber](https://github.com/PMC-Cyber)
        """)
        st.image(
            "https://avatars.githubusercontent.com/u/104304973?v=4",
            caption="PMC Cyber",
            width=150
        )

    with col2:
        st.subheader("👨‍💻 DuskCipher")
        st.markdown("""
        `DuskCipher` adalah developer yang fokus pada **analisis data**, **AI/NLP**, dan **pengembangan backend**,  
        dengan kontribusi nyata dalam sistem cerdas dan layanan data.

        **🧠 Keahlian:**
        - Natural Language Processing (NLP)
        - Otomasi berbasis AI
        - Backend & API Frameworks (FastAPI, Flask)

        **🧰 Tools:** Python, Pandas, Streamlit, FastAPI  
        **🔗 GitHub:** [DuskCipher](https://github.com/DuskCipher)
        """)
        st.image(
            "https://avatars.githubusercontent.com/u/65213343?v=4",
            caption="DuskCipher",
            width=150
        )

    st.markdown("---")
    st.markdown("""
    ### 🤝 Kolaborasi Kami
    Proyek ini merupakan hasil kerja sama antara **PMC-Cyber** dan **DuskCipher**  
    untuk membangun aplikasi **open-source** yang *bermanfaat, scalable*, dan siap dipakai secara profesional.

    > ❤️ Terima kasih telah mengunjungi dashboard kami.  
    > Jangan lupa untuk mengeksplorasi proyek-proyek keren lainnya!
    """)

if __name__ == "__main__":
    show_about_me()

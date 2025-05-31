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
            "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEga5eDYld5sbd55wLG6hivx55kTmK5K5KeSNcm6VCwdtwg_h3u5zrBJ_Fm3XsQa9O0mDOKkedMgCyppPbkM2JZaI7udXCnrB1iQg7Nu72BGCsPh0m9OoQggPntnsGuhCd52jdC_oTyrvsgsBC4kDfmIxEtvBKnz7HI3wbQOtpJEIbGdLMNiJNld8Yl9ZSo8/s316/139885500.jpeg",
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
            "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg1JONQ8j3atX4bveKY2AVQjDKuHr3ZDe23M1J1bBcAwqPU_MaGyhSir4A4bA-dsvscx8maiOldxRWtfWY4XQrQD3RprZVqe1UXjjuJGs5TmKKIpdlb6EWME2hrJE9EExUi4Fn7rrp78NDn7qm53-BEzV-vQUm8pQJyNCFJBZskOP1CTkd53eMukB7vEC9E/s460/208228760.png",
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

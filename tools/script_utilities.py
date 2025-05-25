# tools/script_utilities.py

import streamlit as st
import autopep8
import black
import python_minifier


def beautify_code(code):
    return autopep8.fix_code(code)


def format_with_black(code):
    try:
        mode = black.FileMode()
        formatted = black.format_str(code, mode=mode)
        return formatted
    except black.InvalidInput:
        return "❌ Format gagal: kode tidak valid"


def minify_code(code):
    try:
        return python_minifier.minify(code)
    except Exception as e:
        return f"❌ Gagal minify: {e}"


def show_script_utilities():
    st.markdown("""
        <style>
        .utility-title {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: #ffffff;
            text-transform: uppercase;
            margin-bottom: 25px;
        }
        </style>
        <div class='utility-title'>🧰 SCRIPT UTILITIES</div>
    """, unsafe_allow_html=True)

    st.info("Gunakan alat ini untuk memperindah (beautify), memformat, atau meminify kode Python Anda.")

    code_input = st.text_area("📄 Masukkan Script Python", height=300)
    action = st.radio("Pilih Aksi", ["Beautify (autopep8)", "Format (black)", "Minify"])

    if st.button("⚙️ Proses") and code_input.strip():
        if action == "Beautify (autopep8)":
            result = beautify_code(code_input)
        elif action == "Format (black)":
            result = format_with_black(code_input)
        elif action == "Minify":
            result = minify_code(code_input)
        else:
            result = "Tidak ada aksi yang dipilih."

        st.subheader("📋 Hasil")
        st.code(result, language="python")
        st.download_button(
            label="📥 Download Hasil",
            data=result,
            file_name="script_utility_output.py",
            mime="text/x-python",
            use_container_width=True
        )
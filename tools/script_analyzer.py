# tools/script_analyzer.py

import streamlit as st
import ast
import tokenize
import io
import pyflakes.api
import pyflakes.reporter
import traceback


def analyze_python(code):
    result = {}
    try:
        tree = ast.parse(code)
        result['status'] = '✅ Syntax valid'
        result['errors'] = []
        result['functions'] = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        result['classes'] = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        result['imports'] = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
        result['comments'] = sum(1 for t in tokenize.generate_tokens(io.StringIO(code).readline) if t.type == tokenize.COMMENT)
        result['lines'] = len(code.strip().splitlines())
    except SyntaxError as e:
        result['status'] = '❌ Syntax error'
        result['errors'] = [f"{e.msg} at line {e.lineno}"]
    return result


def analyze_with_pyflakes(code):
    buffer = io.StringIO()
    reporter = pyflakes.reporter.Reporter(buffer, buffer)
    pyflakes.api.check(code, filename="<input>", reporter=reporter)
    return buffer.getvalue()


def show_script_analyzer():
    st.markdown("""
        <style>
        .analyzer-title {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: #ffffff;
            text-transform: uppercase;
            margin-bottom: 25px;
        }
        </style>
        <div class='analyzer-title'>🔍 SCRIPT ANALYZER (PYTHON ONLY)</div>
    """, unsafe_allow_html=True)

    st.info("Masukkan kode Python untuk menganalisis syntax, fungsi, class, komentar, dan warning.")

    code_input = st.text_area("💻 Masukkan Script Python", height=300)
    if st.button("🔎 Analisa") and code_input.strip():
        with st.spinner("Menganalisa..."):
            result = analyze_python(code_input)
            flakes = analyze_with_pyflakes(code_input)

            st.subheader("📊 Hasil Analisa")
            st.markdown(f"**Status:** {result['status']}")

            if result['errors']:
                for err in result['errors']:
                    st.error(err)

            st.markdown(f"- 📄 Jumlah Baris: `{result['lines']}`")
            st.markdown(f"- 💬 Komentar: `{result['comments']}`")

            if result.get("functions"):
                st.markdown("**🔧 Fungsi Ditemukan:**")
                for f in result["functions"]:
                    st.code(f)

            if result.get("classes"):
                st.markdown("**🏛️ Class Ditemukan:**")
                for c in result["classes"]:
                    st.code(c)

            if result.get("imports"):
                st.markdown("**📦 Imports:**")
                for imp in result["imports"]:
                    st.code(imp)

            if flakes.strip():
                st.markdown("**⚠️ Pyflakes Warnings:**")
                st.code(flakes)

            st.download_button(
                label="📥 Download Script",
                data=code_input,
                file_name="script_analyzed.py",
                mime="text/x-python",
                use_container_width=True
            )
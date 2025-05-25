# tools/library_tools.py

import streamlit as st
import pkg_resources
import subprocess
import sys
import io
import contextlib
import traceback
import os


def show_library_tools():
    st.markdown("""
        <style>
        .library-title {
            text-align: center;
            font-size: 30px;
            font-weight: bold;
            color: #ffffff;
            text-transform: uppercase;
            margin-bottom: 25px;
        }
        </style>
        <div class='library-title'>📚 Library Tools</div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📦 Installed Libraries", "➕ Install", "📂 Install to Directory", "🧪 Try Import", "🛠️ Manage"
    ])

    with tab1:
        st.subheader("📦 Installed Libraries")
        packages = sorted([(d.project_name, d.version) for d in pkg_resources.working_set])
        for name, version in packages:
            st.code(f"{name}=={version}", language="bash")

    with tab2:
        st.subheader("➕ Install to Default Environment")
        pkg_name = st.text_input("Masukkan nama package", key="default_install")
        if st.button("🚀 Install Default") and pkg_name:
            with st.spinner("Menginstall..."):
                try:
                    result = subprocess.run([
                        sys.executable, "-m", "pip", "install", pkg_name
                    ], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.success(f"✅ Installed: {pkg_name}")
                        st.code(result.stdout)
                    else:
                        st.error(f"❌ Error installing: {pkg_name}")
                        st.code(result.stderr)
                except Exception as e:
                    st.error(f"❌ Exception: {e}")

    with tab3:
        st.subheader("📂 Install to Specific Directory")
        pkg_name2 = st.text_input("Nama package", key="target_install")
        target_dir = st.text_input("Target direktori (misal: ./libs)", value="./libs")
        if st.button("📦 Install ke Folder") and pkg_name2 and target_dir:
            os.makedirs(target_dir, exist_ok=True)
            with st.spinner("Menginstall ke direktori khusus..."):
                try:
                    result = subprocess.run([
                        sys.executable, "-m", "pip", "install", pkg_name2, "--target", target_dir
                    ], capture_output=True, text=True)
                    if result.returncode == 0:
                        st.success(f"✅ Berhasil diinstall ke: {target_dir}")
                        st.code(result.stdout)
                    else:
                        st.error("❌ Gagal install:")
                        st.code(result.stderr)
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with tab4:
        st.subheader("🧪 Coba Import Package")
        code = st.text_area("Masukkan kode import di bawah ini: contoh: import pandas as pd", height=120)
        if st.button("▶️ Jalankan Import") and code:
            try:
                output_buffer = io.StringIO()
                with contextlib.redirect_stdout(output_buffer):
                    exec(code, {})
                output = output_buffer.getvalue()
                st.success("✅ Import berhasil")
                if output.strip():
                    st.code(output)
            except Exception:
                st.error("❌ Terjadi error saat import:")
                st.code(traceback.format_exc())

    with tab5:
        st.subheader("🛠️ Manage Installed Package")
        manage_pkg = st.text_input("Nama package untuk dikelola")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬆️ Upgrade") and manage_pkg:
                with st.spinner("Meng-upgrade..."):
                    try:
                        result = subprocess.run([
                            sys.executable, "-m", "pip", "install", "--upgrade", manage_pkg
                        ], capture_output=True, text=True)
                        if result.returncode == 0:
                            st.success(f"✅ Berhasil upgrade: {manage_pkg}")
                            st.code(result.stdout)
                        else:
                            st.error(f"❌ Gagal upgrade: {manage_pkg}")
                            st.code(result.stderr)
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        with col2:
            if st.button("❌ Uninstall") and manage_pkg:
                with st.spinner("Menghapus package..."):
                    try:
                        result = subprocess.run([
                            sys.executable, "-m", "pip", "uninstall", "-y", manage_pkg
                        ], capture_output=True, text=True)
                        if result.returncode == 0:
                            st.success(f"✅ {manage_pkg} berhasil dihapus")
                            st.code(result.stdout)
                        else:
                            st.error(f"❌ Gagal uninstall: {manage_pkg}")
                            st.code(result.stderr)
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        with col3:
            st.markdown("""
                <div style='margin-top:30px'>
                <strong>📍 VENV Info:</strong><br>
                <code>{}</code>
                </div>
            """.format(sys.prefix), unsafe_allow_html=True)

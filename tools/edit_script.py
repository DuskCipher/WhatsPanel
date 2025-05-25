import streamlit as st
import os

def show_edit_script():
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
        <div class='analyzer-title'>✏️ EDIT SCRIPT PYTHON</div>
    """, unsafe_allow_html=True)

    script_folder = "scripts"
    os.makedirs(script_folder, exist_ok=True)

    file_list = [f for f in os.listdir(script_folder) if f.endswith(".py")]
    file_list.append("📄 Buat File Baru...")

    selected_file = st.selectbox("📂 Pilih File Script", file_list)

    if selected_file == "📄 Buat File Baru...":
        new_file_name = st.text_input("🆕 Nama File Baru", placeholder="contoh: my_script.py")
        full_path = os.path.join(script_folder, new_file_name) if new_file_name else None
    else:
        full_path = os.path.join(script_folder, selected_file)

    if full_path:
        content = ""
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

        edited_content = st.text_area("📝 Edit Script di sini:", value=content, height=400)

        if st.button("💾 Simpan Script"):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(edited_content)
            st.success(f"✅ Script disimpan ke: {full_path}")
            st.rerun()

        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                file_data = f.read()
            file_name = os.path.basename(full_path)
            st.download_button(
                label=f"⬇️ Unduh Script: {file_name}",
                data=file_data,
                file_name=file_name,
                mime="text/x-python",
                use_container_width=True
            )

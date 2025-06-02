import subprocess
import os
import sys

# Ambil path folder ini
base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(base_dir, "WhatsPanel-main")

# Jalankan streamlit app
script_path = os.path.join(project_dir, "dashboard", "kirim_pesan.py")

# Jalankan streamlit sebagai proses baru
subprocess.run(["streamlit", "run", script_path], shell=True)

import subprocess
import os

# Ambil path folder ini (PANEL/)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Path ke file utama yang ingin dijalankan
script_path = os.path.join(base_dir, "whatsapp_dashboard.py")

# Jalankan Streamlit app
subprocess.run(["streamlit", "run", script_path])

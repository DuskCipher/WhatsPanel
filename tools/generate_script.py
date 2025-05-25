import streamlit as st

def show_generate_script():
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
        <div class='analyzer-title'>🛠️ GENERATOR TEMPLATE SCRIPT OTOMATIS</div>
    """, unsafe_allow_html=True)
    task = st.selectbox("Pilih Jenis Script:", [
        "Kirim Request API",
        "Baca File CSV",
        "Enkripsi Teks",
        "Kirim Pesan WhatsApp"
    ])

    script = ""

    if task == "Kirim Request API":
        script = """import requests

url = "https://example.com/api"
payload = {"key": "value"}
headers = {"Authorization": "Bearer YOUR_TOKEN"}

response = requests.post(url, json=payload, headers=headers)
print("Status:", response.status_code)
print("Response:", response.text)
"""

    elif task == "Baca File CSV":
        script = """import pandas as pd

file_path = "data.csv"
df = pd.read_csv(file_path)

print("Data Loaded:")
print(df.head())
"""

    elif task == "Enkripsi Teks":
        script = """from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)

text = "data rahasia"
encrypted = fernet.encrypt(text.encode())
print("Encrypted:", encrypted)

decrypted = fernet.decrypt(encrypted).decode()
print("Decrypted:", decrypted)
"""

    elif task == "Kirim Pesan WhatsApp":
        script = """import requests

url = "https://app.wapanels.com/api/create-message"
payload = {
    "appkey": "YOUR_APP_KEY",
    "authkey": "YOUR_AUTH_KEY",
    "to": "6281234567890",
    "message": "Halo, ini pesan otomatis dari Python!"
}

response = requests.post(url, data=payload)
print(response.status_code)
print(response.text)
"""

    st.code(script, language="python")
    file_name = f"template_{task.replace(' ', '_').lower()}.py"
    st.download_button("⬇️ Download Script", data=script, file_name=file_name, mime="text/x-python")
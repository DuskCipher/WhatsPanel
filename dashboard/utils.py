# dashboard/utils.py
import requests
import json

def send_text_message(number, message, appkey, authkey):
    url = "https://app.wapanels.com/api/create-message"
    payload = {
        "appkey": appkey,
        "authkey": authkey,
        "to": number,
        "message": message,
    }
    try:
        response = requests.post(url, data=payload)
        response_data = response.json()
        status_flag = response.status_code == 200 and response_data.get("status") == "success"
        return status_flag, response_data
    except Exception as e:
        return False, str(e)

def send_image_message(number, caption, image_url, appkey, authkey):
    url = "https://app.wapanels.com/api/create-message"
    payload = {
        "appkey": appkey,
        "authkey": authkey,
        "to": number,
        "message": caption,
        "file": image_url,
    }
    try:
        response = requests.post(url, data=payload)
        response_data = response.json()
        status_flag = response.status_code == 200 and response_data.get("status") == "success"
        return status_flag, response_data
    except Exception as e:
        return False, str(e)

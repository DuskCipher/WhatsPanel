import requests

def is_valid_wa_number(number):
    """
    Validasi sederhana nomor WhatsApp.
    Harus berupa digit, mulai dengan '628', dan panjang minimal 10 digit.
    """
    number = str(number)  # konversi ke string agar .isdigit() tidak error
    return number.isdigit() and number.startswith("628") and len(number) >= 10


def send_text_message(number, message, appkey, authkey):
    if not is_valid_wa_number(number):
        return False, {"error": "Nomor tidak valid", "number": number}

    url = "https://app.wapanels.com/api/create-message"
    payload = {
        "appkey": appkey,
        "authkey": authkey,
        "to": number,
        "message": message,
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            try:
                res_json = response.json()
                if res_json.get("status", "").lower() == "success":
                    return True, res_json
                else:
                    return False, {
                        "error": "status != success",
                        "response": res_json
                    }
            except Exception as e:
                return False, {"error": "JSON Parsing Error", "exception": str(e)}
        else:
            return False, {"error": f"HTTP {response.status_code}", "text": response.text}
    except Exception as e:
        return False, {"error": "Exception", "exception": str(e)}


def send_image_message(number, caption, image_url, appkey, authkey):
    if not is_valid_wa_number(number):
        return False, {"error": "Nomor tidak valid", "number": number}

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
        if response.status_code == 200:
            try:
                res_json = response.json()
                if res_json.get("status", "").lower() == "success":
                    return True, res_json
                else:
                    return False, {
                        "error": "status != success",
                        "response": res_json
                    }
            except Exception as e:
                return False, {"error": "JSON Parsing Error", "exception": str(e)}
        else:
            return False, {"error": f"HTTP {response.status_code}", "text": response.text}
    except Exception as e:
        return False, {"error": "Exception", "exception": str(e)}

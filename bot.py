import requests
import time

TOKEN = "8796451286:AAEPhIX50hDWjsBkN4mu3xTPFWXfPLPf6wE"
CHAT_ID = "1010951175"
IDN_USERNAME = "jkt48_oniel"
CHECK_INTERVAL = 300  # 5 menit

def is_live():
    try:
        url = f"https://www.idn.app/{IDN_USERNAME}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        return "LIVE" in response.text
    except:
        return False

def send_notif():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": f"🔴 {IDN_USERNAME} sedang LIVE di IDN!\nhttps://www.idn.app/{IDN_USERNAME}"
    })

was_live = False
while True:
    live = is_live()
    if live and not was_live:
        send_notif()
    was_live = live
    time.sleep(CHECK_INTERVAL)

import requests
import time

import os
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
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
send_notif()
while True:
    live = is_live()
    if live and not was_live:
        send_notif()
    was_live = live
    time.sleep(CHECK_INTERVAL)

import requests
import time
import os
from datetime import datetime

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
IDN_USERNAME = "jkt48_oniel"
CHECK_INTERVAL = 300  # 5 menit

def get_thumbnail():
    try:
        url = f"https://www.idn.app/{IDN_USERNAME}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        text = response.text
        idx = text.find('og:image')
        if idx != -1:
            start = text.find('content="', idx) + 9
            end = text.find('"', start)
            return text[start:end]
    except:
        return None

def is_live():
    try:
        url = f"https://www.idn.app/{IDN_USERNAME}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        return "LIVE" in response.text
    except:
        return False

def send_notif_live(start_time):
    text = (
        f"🔴 *Oniel JKT48 sedang LIVE di IDN!*\n"
        f"🕐 Mulai: {start_time}\n"
        f"🔗 Web: https://www.idn.app/{IDN_USERNAME}\n"
        f"📱 App: https://www.idn.app/{IDN_USERNAME}"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    })
    print(response.json())
def send_notif_selesai(start_time, end_time):
    start = datetime.strptime(start_time, "%H:%M WIB")
    end = datetime.strptime(end_time, "%H:%M WIB")
    durasi = end - start
    total_menit = int(durasi.total_seconds() / 60)
    jam = total_menit // 60
    menit = total_menit % 60
    durasi_str = f"{jam} jam {menit} menit" if jam > 0 else f"{menit} menit"

    text = (
        f"⚫ <b>Oniel JKT48 sudah selesai LIVE</b>\n"
        f"🕐 Mulai: {start_time}\n"
        f"🕑 Selesai: {end_time}\n"
        f"⏱ Durasi: {durasi_str}"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    })
was_live = False
start_time = None

print("Bot started!")
send_notif_live("22:26 WIB")  # test
print("Notif sent!")

while True:
    live = is_live()
    now = datetime.now().strftime("%H:%M") + " WIB"

    if live and not was_live:
        start_time = now
        send_notif_live(start_time)

    if not live and was_live and start_time:
        send_notif_selesai(start_time, now)
        start_time = None

    was_live = live
    time.sleep(CHECK_INTERVAL)

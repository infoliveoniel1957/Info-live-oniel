import requests
import time
import os
from datetime import datetime

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
IDN_USERNAME = "jkt48_oniel"
IDN_USER_ID = "0078fe3c-8f4d-495b-bb7c-bdb2b98d0598"
CHECK_INTERVAL = 300  # 5 menit

def get_thumbnail():
    return "https://cdn.idn.media/idnaccount/avatar/500/b00afb482407c122800161b0bab0d04b.webp"

def get_live_title():
    try:
        url = f"https://api.idn.app/v1/live-stream/{IDN_USERNAME}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get("title", "")
    except:
        return ""

def is_live():
    try:
        url = f"https://www.idn.app/{IDN_USERNAME}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        return "LIVE" in response.text
    except:
        return False

def send_notif_live(start_time):
    thumbnail = get_thumbnail()
    title = get_live_title()
    text = (
        f"🔴 <b>Oniel JKT48 sedang LIVE di IDN!</b>\n"
        + (f"🎬 {title}\n" if title else "")
        + f"📅 Tanggal: {datetime.now().strftime('%d %B %Y')}\n"
        f"🕐 Mulai: {start_time}\n"
        f"🔗 <a href='https://www.idn.app/{IDN_USERNAME}'>Buka di Web</a>\n"
        f"📱 <a href='https://idn-app.idn.link/s/profile-5as6nw'>Buka di App IDN</a>"
    )
    if thumbnail:
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "photo": thumbnail,
            "caption": text,
            "parse_mode": "HTML"
        })
    else:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        })

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
        f"📅 Tanggal: {datetime.now().strftime('%d %B %Y')}\n"
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
send_notif_live("22:00 WIB")
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

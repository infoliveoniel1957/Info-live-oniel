import requests
import time
import os
from datetime import datetime

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# IDN Live
IDN_USERNAME = "jkt48_oniel"
IDN_USER_ID = "0078fe3c-8f4d-495b-bb7c-bdb2b98d0598"
IDN_THUMBNAIL = "https://cdn.idn.media/idnaccount/avatar/500/b00afb482407c122800161b0bab0d04b.webp"

# Showroom
SHOWROOM_ROOM_ID = "318218"
SHOWROOM_USERNAME = "JKT48_Oniel"
SHOWROOM_THUMBNAIL = "https://static.showroom-live.com/image/room/cover/6f5b72d14f8cf4d61ab8c16aa8b7a9c387c5f6de37f513a884b6fbadabb5784d_l.jpeg"

CHECK_INTERVAL = 60  # 1 menit

# ===================== IDN LIVE =====================

def is_live_idn():
    try:
        url = f"https://www.idn.app/{IDN_USERNAME}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        return "LIVE" in response.text
    except:
        return False

def get_live_title_idn():
    try:
        url = f"https://api.idn.app/v1/live-stream/{IDN_USERNAME}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get("title", "")
    except:
        return ""

def send_notif_live_idn(start_time):
    title = get_live_title_idn()
    text = (
        f"🔴 <b>Oniel JKT48 sedang LIVE di IDN!</b>\n"
        + (f"🎬 {title}\n" if title else "")
        + f"📅 Tanggal: {datetime.now().strftime('%d %B %Y')}\n"
        f"🕐 Mulai: {start_time}\n"
        f"🔗 <a href='https://www.idn.app/{IDN_USERNAME}'>Buka di Web</a>\n"
        f"📱 <a href='https://idn-app.idn.link/s/profile-5as6nw'>Buka di App IDN</a>"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": IDN_THUMBNAIL,
        "caption": text,
        "parse_mode": "HTML"
    })

def send_notif_selesai_idn(start_time, end_time):
    start = datetime.strptime(start_time, "%H:%M WIB")
    end = datetime.strptime(end_time, "%H:%M WIB")
    durasi = end - start
    total_menit = int(durasi.total_seconds() / 60)
    jam = total_menit // 60
    menit = total_menit % 60
    durasi_str = f"{jam} jam {menit} menit" if jam > 0 else f"{menit} menit"
    text = (
        f"⚫ <b>Oniel JKT48 selesai LIVE di IDN</b>\n"
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

# ===================== SHOWROOM =====================

def is_live_showroom():
    try:
        url = f"https://www.showroom-live.com/api/live/streaming_url?room_id={SHOWROOM_ROOM_ID}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        data = response.json()
        return len(data.get("streaming_url_list", [])) > 0
    except:
        return False

def send_notif_live_showroom(start_time):
    text = (
        f"🔴 <b>Oniel JKT48 sedang LIVE di Showroom!</b>\n"
        f"📅 Tanggal: {datetime.now().strftime('%d %B %Y')}\n"
        f"🕐 Mulai: {start_time}\n"
        f"🔗 <a href='https://www.showroom-live.com/r/{SHOWROOM_USERNAME}'>Buka Showroom</a>"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "photo": SHOWROOM_THUMBNAIL,
        "caption": text,
        "parse_mode": "HTML"
    })

def send_notif_selesai_showroom(start_time, end_time):
    start = datetime.strptime(start_time, "%H:%M WIB")
    end = datetime.strptime(end_time, "%H:%M WIB")
    durasi = end - start
    total_menit = int(durasi.total_seconds() / 60)
    jam = total_menit // 60
    menit = total_menit % 60
    durasi_str = f"{jam} jam {menit} menit" if jam > 0 else f"{menit} menit"
    text = (
        f"⚫ <b>Oniel JKT48 selesai LIVE di Showroom</b>\n"
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

# ===================== MAIN =====================

was_live_idn = False
was_live_showroom = False
start_time_idn = None
start_time_showroom = None
send_notif_selesai_showroom("22:00 WIB", "23:00 WIB")
while True:
    now = datetime.now().strftime("%H:%M") + " WIB"

    # Cek IDN Live
    live_idn = is_live_idn()
    if live_idn and not was_live_idn:
        start_time_idn = now
        send_notif_live_idn(start_time_idn)
    if not live_idn and was_live_idn and start_time_idn:
        send_notif_selesai_idn(start_time_idn, now)
        start_time_idn = None
    was_live_idn = live_idn

    # Cek Showroom
    live_showroom = is_live_showroom()
    if live_showroom and not was_live_showroom:
        start_time_showroom = now
        send_notif_live_showroom(start_time_showroom)
    if not live_showroom and was_live_showroom and start_time_showroom:
        send_notif_selesai_showroom(start_time_showroom, now)
        start_time_showroom = None
    was_live_showroom = live_showroom

    time.sleep(CHECK_INTERVAL)

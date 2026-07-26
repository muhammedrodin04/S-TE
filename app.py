import asyncio
import threading
import requests
import time
import re
import json
import os
import random
import hashlib
from datetime import datetime
from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
import phonenumbers
from phonenumbers import geocoder

app = Flask(__name__)
app.secret_key = "vexorp_web_secure_2026_key"

# ====================== AYARLAR ======================
ADMIN_PASSWORD = "VEXORP-SANAL-OTP"
KONTROL_ARALIGI_SN = 5
SON_KAYIT_SINIR = 7
USERS_FILE = "users.json"
STOK_FILE = "stok.json"
SEEN_CACHE_FILE = "seen_cache.json"

# Çoklu API listesi
API_LIST = [
    {"url": "http://147.135.212.197/crapi/st/viewstats", "token": "RFdUREJBUzR9T4dVc49ndmFra1NYV5CIhpGVcnaOYmqHhJZXfYGJSQ==", "type": "old"},
    {"url": "http://number-panel-production.up.railway.app/api/Junaidn?type=sms", "token": None, "type": "new"},
    {"url": "http://number-panel-production.up.railway.app/api/Junaid?type=sms", "token": None, "type": "new"},
    {"url": "http://number-panel-production.up.railway.app/api/psjunaid?type=sms", "token": None, "type": "new"},
    {"url": "https://mis-panel.onrender.com/api/fjunaid?type=sms", "token": None, "type": "new"},
    {"url": "https://mis-panel.onrender.com/api/junaid?type=sms", "token": None, "type": "new"},
    {"url": "http://mis-panel-production.up.railway.app/api/junaid?type=sms", "token": None, "type": "new"},
    {"url": "https://number-panel-production.up.railway.app/api/junaidn?type=sms", "token": None, "type": "new"},
    {"url": "https://number-panel-production.up.railway.app/api/junaid?type=sms", "token": None, "type": "new"},
    {"url": "http://mis-panel-production.up.railway.app/api/gijunaid?type=sms", "token": None, "type": "new"},
    {"url": "https://hadibhai-production-90b2.up.railway.app/api/psjunaid?type=sms", "token": None, "type": "new"},
]

# Ülke kodları (telegram botundaki aynı)
COUNTRY_CODES = {
    "1": "🇺🇸", "1242": "🇧🇸", "1246": "🇧🇧", "1264": "🇦🇮", "1268": "🇦🇬", "1284": "🇻🇬",
    "1340": "🇻🇮", "1345": "🇰🇾", "1441": "🇧🇲", "1473": "🇬🇩", "1649": "🇹🇨", "1664": "🇲🇸",
    "1671": "🇬🇺", "1684": "🇦🇸", "1758": "🇱🇨", "1767": "🇩🇲", "1784": "🇻🇨", "1787": "🇵🇷",
    "1809": "🇩🇴", "1829": "🇩🇴", "1849": "🇩🇴", "1868": "🇹🇹", "1869": "🇰🇳", "1876": "🇯🇲",
    "7": "🇷🇺", "20": "🇪🇬", "27": "🇿🇦", "30": "🇬🇷", "31": "🇳🇱", "32": "🇧🇪", "33": "🇫🇷",
    "34": "🇪🇸", "36": "🇭🇺", "39": "🇮🇹", "40": "🇷🇴", "41": "🇨🇭", "43": "🇦🇹", "44": "🇬🇧",
    "45": "🇩🇰", "46": "🇸🇪", "47": "🇳🇴", "48": "🇵🇱", "49": "🇩🇪", "51": "🇵🇪", "52": "🇲🇽",
    "53": "🇨🇺", "54": "🇦🇷", "55": "🇧🇷", "56": "🇨🇱", "57": "🇨🇴", "58": "🇻🇪", "60": "🇲🇾",
    "61": "🇦🇺", "62": "🇮🇩", "63": "🇵🇭", "64": "🇳🇿", "65": "🇸🇬", "66": "🇹🇭", "81": "🇯🇵",
    "82": "🇰🇷", "84": "🇻🇳", "86": "🇨🇳", "90": "🇹🇷", "91": "🇮🇳", "92": "🇵🇰", "93": "🇦🇫",
    "94": "🇱🇰", "95": "🇲🇲", "98": "🇮🇷", "211": "🇸🇸", "212": "🇲🇦", "213": "🇩🇿", "216": "🇹🇳",
    "218": "🇱🇾", "220": "🇬🇲", "221": "🇸🇳", "222": "🇲🇷", "223": "🇲🇱", "224": "🇬🇳", "225": "🇨🇮",
    "226": "🇧🇫", "227": "🇳🇪", "228": "🇹🇬", "229": "🇧🇯", "230": "🇲🇺", "231": "🇱🇷", "232": "🇸🇱",
    "233": "🇬🇭", "234": "🇳🇬", "235": "🇹🇩", "236": "🇨🇫", "237": "🇨🇲", "238": "🇨🇻", "239": "🇸🇹",
    "240": "🇬🇶", "241": "🇬🇦", "242": "🇨🇬", "243": "🇨🇩", "244": "🇦🇴", "245": "🇬🇼", "248": "🇸🇨",
    "249": "🇸🇩", "250": "🇷🇼", "251": "🇪🇹", "252": "🇸🇴", "253": "🇩🇯", "254": "🇰🇪", "255": "🇹🇿",
    "256": "🇺🇬", "257": "🇧🇮", "258": "🇲🇿", "260": "🇿🇲", "261": "🇲🇬", "262": "🇾🇹", "263": "🇿🇼",
    "264": "🇳🇦", "265": "🇲🇼", "266": "🇱🇸", "267": "🇧🇼", "268": "🇸🇿", "269": "🇰🇲", "290": "🇸🇭",
    "291": "🇪🇷", "297": "🇦🇼", "298": "🇫🇴", "299": "🇬🇱", "350": "🇬🇮", "351": "🇵🇹", "352": "🇱🇺",
    "353": "🇮🇪", "354": "🇮🇸", "355": "🇦🇱", "356": "🇲🇹", "357": "🇨🇾", "358": "🇫🇮", "359": "🇧🇬",
    "370": "🇱🇹", "371": "🇱🇻", "372": "🇪🇪", "373": "🇲🇩", "374": "🇦🇲", "375": "🇧🇾", "376": "🇦🇩",
    "377": "🇲🇨", "378": "🇸🇲", "380": "🇺🇦", "381": "🇷🇸", "382": "🇲🇪", "383": "🇽🇰", "385": "🇭🇷",
    "386": "🇸🇮", "387": "🇧🇦", "389": "🇲🇰", "420": "🇨🇿", "421": "🇸🇰", "423": "🇱🇮", "500": "🇫🇰",
    "501": "🇧🇿", "502": "🇬🇹", "503": "🇸🇻", "504": "🇭🇳", "505": "🇳🇮", "506": "🇨🇷", "507": "🇵🇦",
    "508": "🇵🇲", "509": "🇭🇹", "590": "🇬🇵", "591": "🇧🇴", "592": "🇬🇾", "593": "🇪🇨", "594": "🇬🇫",
    "595": "🇵🇾", "596": "🇲🇶", "597": "🇸🇷", "598": "🇺🇾", "599": "🇨🇼", "670": "🇹🇱", "672": "🇦🇶",
    "673": "🇧🇳", "674": "🇳🇷", "675": "🇵🇬", "676": "🇹🇴", "677": "🇸🇧", "678": "🇻🇺", "679": "🇫🇯",
    "680": "🇵🇼", "681": "🇼🇫", "682": "🇨🇰", "683": "🇳🇺", "685": "🇼🇸", "686": "🇰🇮", "687": "🇳🇨",
    "688": "🇹🇻", "689": "🇵🇫", "690": "🇹🇰", "691": "🇫🇲", "692": "🇲🇭", "850": "🇰🇵", "852": "🇭🇰",
    "853": "🇲🇴", "855": "🇰🇭", "856": "🇱🇦", "880": "🇧🇩", "886": "🇹🇼", "960": "🇲🇻", "961": "🇱🇧",
    "962": "🇯🇴", "963": "🇸🇾", "964": "🇮🇶", "965": "🇰🇼", "966": "🇸🇦", "967": "🇾🇪", "968": "🇴🇲",
    "970": "🇵🇸", "971": "🇦🇪", "972": "🇮🇱", "973": "🇧🇭", "974": "🇶🇦", "975": "🇧🇹", "976": "🇲🇳",
    "977": "🇳🇵", "992": "🇹🇯", "993": "🇹🇲", "994": "🇦🇿", "995": "🇬🇪", "996": "🇰🇬", "998": "🇺🇿"
}

# ====================== VERİ YÖNETİMİ ======================
def veri_yukle(dosya, varsayilan):
    if os.path.exists(dosya):
        try:
            with open(dosya, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return varsayilan
    return varsayilan

def veri_kaydet(dosya, veri):
    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

# Global veri yapıları
stok = veri_yukle(STOK_FILE, {})
seen_ids = set(veri_yukle(SEEN_CACHE_FILE, []))
user_numbers = {}   # session_id -> {"number": num, "country": country}
otp_logs = []       # tüm OTP'ler (liste)
MAX_LOG = 50000

# ====================== YARDIMCI FONKSİYONLAR ======================
def get_flag(phone: str) -> str:
    phone = re.sub(r'\D', '', phone)
    for length in [4, 3, 2, 1]:
        prefix = phone[:length]
        if prefix in COUNTRY_CODES:
            return COUNTRY_CODES[prefix]
    return "🏳️"

def mask_number(phone: str) -> str:
    phone = re.sub(r'\D', '', phone)
    if len(phone) <= 6:
        return f"+{phone}"
    visible_start = 3 if len(phone) > 8 else 2
    visible_end = 3
    masked = phone[:visible_start] + "*" * (len(phone) - visible_start - visible_end) + phone[-visible_end:]
    return f"+{masked}"

def extract_otp(full_msg: str) -> str:
    patterns = [
        r'(?:code|كود|رمز|كود التفعيل|رمز التحقق|código|код|验证码|code de vérification|codice|verification code|Your .* code|Your .* código|Your .* код|imo verification code|WhatsApp code|code is|is)[\s\W:-]*(\d{3,8})',
        r'\b(\d{3}-\d{3})\b',
        r'\b(\d{6})\b',
        r'\b(\d{5})\b',
        r'\b(\d{4})\b',
        r'OTP[:\s]*(\d+)',
        r'code[:\s]*(\d+)',
        r'kod[:\s]*(\d+)',
        r'رمز[:\s]*(\d+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, full_msg, re.IGNORECASE | re.UNICODE)
        if match:
            otp = re.sub(r'[- ]', '', match.group(1))
            return otp
    return "N/A"

def get_country_from_phonenumber(num: str):
    try:
        if not num.startswith('+'): 
            num = '+' + num
        parsed = phonenumbers.parse(num)
        region = phonenumbers.region_code_for_number(parsed)
        if region:
            base = 127462 - ord('A')
            flag = chr(base + ord(region[0])) + chr(base + ord(region[1]))
            country = geocoder.description_for_number(parsed, "en")
            return country or "Unknown", flag
    except:
        pass
    return "Unknown", get_flag(num)

def generate_unique_id(phone: str, message: str, time: str = "") -> str:
    unique_str = f"{phone}|{message[:100]}|{time}"
    return hashlib.md5(unique_str.encode()).hexdigest()

def is_new_record(phone: str, message: str, time: str = "") -> bool:
    global seen_ids
    uid = generate_unique_id(phone, message, time)
    if uid in seen_ids:
        return False
    seen_ids.add(uid)
    if len(seen_ids) > 10000:
        seen_ids = set(list(seen_ids)[-5000:])
    veri_kaydet(SEEN_CACHE_FILE, list(seen_ids))
    return True

def get_service_icon(service: str) -> str:
    svc = service.lower() if service else ""
    if "whatsapp" in svc:
        return "🟢"
    elif "telegram" in svc:
        return "🔵"
    elif "facebook" in svc or "fb" in svc:
        return "📘"
    elif "instagram" in svc or "ig" in svc:
        return "📷"
    elif "tiktok" in svc:
        return "🎵"
    else:
        return "📱"

# ====================== API VERİ ÇEKME ======================
def fetch_old_api(api_config):
    try:
        params = {"token": api_config["token"], "records": ""}
        r = requests.get(api_config["url"], params=params, timeout=15)
        return r.json()
    except Exception as e:
        print(f"Eski API Hatası ({api_config['url']}): {e}")
        return []

def fetch_new_api(api_config):
    try:
        r = requests.get(api_config["url"], timeout=10)
        data = r.json()
        return parse_new_api_response(data)
    except Exception as e:
        print(f"Yeni API Hatası ({api_config['url']}): {e}")
        return []

def parse_new_api_response(data):
    records = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                records.append({
                    "time": item.get("time") or item.get("created_at") or "",
                    "country": item.get("country") or item.get("country_name") or "",
                    "number": item.get("number") or item.get("phone") or item.get("mobile") or "",
                    "service": item.get("service") or item.get("source") or "",
                    "message": item.get("message") or item.get("msg") or item.get("text") or "",
                })
            elif isinstance(item, list) and len(item) >= 5:
                records.append({
                    "time": item[0],
                    "country": item[1],
                    "number": item[2],
                    "service": item[3],
                    "message": item[4],
                })
    elif isinstance(data, dict):
        for key in ["aaData", "data", "records", "result"]:
            if key in data and isinstance(data[key], list):
                for item in data[key]:
                    if isinstance(item, dict):
                        records.append({
                            "time": item.get("time") or item.get("created_at") or "",
                            "country": item.get("country") or "",
                            "number": item.get("number") or item.get("phone") or "",
                            "service": item.get("service") or "",
                            "message": item.get("message") or item.get("msg") or "",
                        })
                    elif isinstance(item, list) and len(item) >= 5:
                        records.append({
                            "time": item[0],
                            "country": item[1],
                            "number": item[2],
                            "service": item[3],
                            "message": item[4],
                        })
                break
    return records

# ====================== OTP İŞLEME (arka plan) ======================
def process_old_api_record(record):
    no = str(record[1]) if len(record) > 1 else ""
    full_msg = str(record[2]) if len(record) > 2 else ""
    if not no or not full_msg:
        return
    if not is_new_record(no, full_msg):
        return
    otp = extract_otp(full_msg)
    flag = get_flag(no)
    masked_no = mask_number(no)
    # Hangi kullanıcıya ait?
    user_id = None
    for sid, data in user_numbers.items():
        if data["number"] == no:
            user_id = sid
            break
    log_entry = {
        "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "numara": masked_no,
        "otp": otp,
        "mesaj": full_msg[:200],
        "ulke": flag,
        "user": user_id
    }
    otp_logs.insert(0, log_entry)
    if len(otp_logs) > MAX_LOG:
        otp_logs.pop()
    # Eğer kullanıcıya aitse, session'ına ekle (gerçek zamanlı göstermek için)
    if user_id:
        # Kullanıcının otp listesine ekleyebiliriz
        pass

def process_new_api_record(record):
    no = record.get("number", "")
    full_msg = record.get("message", "")
    service = record.get("service", "Unknown")
    time_str = record.get("time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    country = record.get("country", "")
    if not no or not full_msg:
        return
    if not is_new_record(no, full_msg, time_str):
        return
    otp = extract_otp(full_msg)
    if country:
        country_name = country
        flag = get_flag(no)
    else:
        country_name, flag = get_country_from_phonenumber(no)
    masked_no = mask_number(no)
    user_id = None
    for sid, data in user_numbers.items():
        if data["number"] == no:
            user_id = sid
            break
    log_entry = {
        "zaman": time_str,
        "numara": masked_no,
        "otp": otp,
        "mesaj": full_msg[:200],
        "ulke": f"{flag} {country_name}",
        "servis": service,
        "user": user_id
    }
    otp_logs.insert(0, log_entry)
    if len(otp_logs) > MAX_LOG:
        otp_logs.pop()

def api_izleme():
    """Arka plan thread'i"""
    print("🚀 OTP takibi başlatıldı (Web) - Çoklu API")
    while True:
        for api_config in API_LIST:
            try:
                if api_config["type"] == "old":
                    data = fetch_old_api(api_config)
                    if isinstance(data, list):
                        for row in reversed(data[-SON_KAYIT_SINIR:]):
                            process_old_api_record(row)
                else:
                    records = fetch_new_api(api_config)
                    for record in records:
                        process_new_api_record(record)
            except Exception as e:
                print(f"API Hatası ({api_config['url']}): {e}")
        time.sleep(KONTROL_ARALIGI_SN)

# ====================== FLASK ROUTES ======================

# Anasayfa
@app.route("/")
def index():
    user_id = session.get("user_id")
    if not user_id:
        session["user_id"] = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        user_id = session["user_id"]
    # Kullanıcının aktif numarası
    user_data = user_numbers.get(user_id, {})
    number = user_data.get("number")
    country = user_data.get("country", "")
    # Kullanıcıya özel OTP'leri filtrele
    user_logs = [log for log in otp_logs if log.get("user") == user_id]
    # Stoktaki ülke listesi
    countries = sorted(stok.keys())
    return render_template_string(HTML_TEMPLATE, 
                                   number=number,
                                   country=country,
                                   user_logs=user_logs,
                                   countries=countries,
                                   stok=stok)

# Numara alma
@app.route("/get_number", methods=["POST"])
def get_number():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("index"))
    country = request.form.get("country")
    if not country or country not in stok or not stok[country]:
        return "Stokta bu ülke için numara yok", 400
    num = stok[country].pop(random.randrange(len(stok[country])))
    veri_kaydet(STOK_FILE, stok)
    user_numbers[user_id] = {"number": num, "country": country}
    return redirect(url_for("index"))

# Admin giriş
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_panel"))
    return render_template_string('''
        <body style="background:#000;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;color:white;">
        <form method="post" style="background:#0f0f0f;padding:40px;border-radius:15px;border:2px solid #ff0000;">
            <h2 style="color:#ff0000">VEXORP ADMIN</h2>
            <input type="password" name="password" style="width:100%;padding:12px;margin:20px 0;background:#000;border:2px solid #333;color:white;border-radius:8px;">
            <button type="submit" style="width:100%;padding:12px;background:#ff0000;color:#000;border:none;border-radius:8px;font-weight:bold;cursor:pointer;">Giriş</button>
        </form>
        </body>
    ''')

@app.route("/admin/panel", methods=["GET", "POST"])
def admin_panel():
    if not session.get("admin"):
        return redirect(url_for("admin"))
    if request.method == "POST":
        action = request.form.get("action")
        if action == "upload":
            file = request.files.get("file")
            country = request.form.get("country")
            if file and country:
                lines = file.read().decode("utf-8").splitlines()
                stok.setdefault(country, []).extend([l.strip() for l in lines if l.strip()])
                veri_kaydet(STOK_FILE, stok)
                return "Stok eklendi! <a href='/admin/panel'>Geri</a>"
        elif action == "delete_all":
            stok.clear()
            veri_kaydet(STOK_FILE, stok)
            return "Tüm stok silindi! <a href='/admin/panel'>Geri</a>"
        elif action == "delete_country":
            country = request.form.get("country")
            if country in stok:
                del stok[country]
                veri_kaydet(STOK_FILE, stok)
                return f"{country} silindi! <a href='/admin/panel'>Geri</a>"
    return render_template_string('''
        <h2>VEXORP Admin</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="text" name="country" placeholder="Ülke adı (Turkey, USA...)" required>
            <button type="submit" name="action" value="upload">Yükle</button>
        </form>
        <form method="post">
            <button type="submit" name="action" value="delete_all">Tüm Stoku Sil</button>
        </form>
        <form method="post">
            <input type="text" name="country" placeholder="Ülke adı sil">
            <button type="submit" name="action" value="delete_country">Ülkeyi Sil</button>
        </form>
        <hr>
        <h3>Mevcut Stok</h3>
        <ul>
        {% for c, nums in stok.items() %}
            <li>{{ c }}: {{ nums|length }} adet</li>
        {% endfor %}
        </ul>
        <a href="/">Ana Sayfa</a>
    ''', stok=stok)

# ====================== HTML TEMPLATE (tek parça) ======================
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>
    <title>VEXORP OTP WEB</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background:#0a0a0a; color:#eee; font-family:'Segoe UI',Arial,sans-serif; padding:20px; }
        .container { max-width:1100px; margin:auto; background:#161616; border-radius:20px; padding:25px; box-shadow:0 0 40px rgba(255,0,0,0.2); border:1px solid #2a2a2a; }
        h1 { color:#ff1a1a; text-shadow:0 0 20px #ff1a1a; text-align:center; font-size:2.4em; margin-bottom:20px; }
        .row { display:flex; flex-wrap:wrap; gap:20px; margin:20px 0; }
        .col { flex:1; min-width:250px; background:#1f1f1f; padding:20px; border-radius:14px; border:1px solid #333; }
        .number-box { background:#000; padding:15px; border-radius:10px; border:2px solid #ff1a1a; font-size:1.5em; text-align:center; font-family:monospace; }
        .flag { font-size:1.8em; }
        .btn { background:#ff1a1a; color:#fff; border:none; padding:12px 24px; border-radius:30px; cursor:pointer; font-weight:bold; transition:0.3s; }
        .btn:hover { background:#cc0000; transform:scale(1.05); }
        select { padding:10px; background:#222; color:#fff; border:1px solid #555; border-radius:8px; width:100%; }
        table { width:100%; border-collapse:collapse; margin-top:15px; font-size:14px; }
        th { background:#2a2a2a; padding:10px; text-align:left; border-bottom:2px solid #ff1a1a; }
        td { padding:10px; border-bottom:1px solid #222; }
        .otp-badge { background:#ff1a1a; color:#fff; padding:4px 12px; border-radius:20px; font-weight:bold; font-family:monospace; }
        .admin-link { position:fixed; bottom:20px; right:20px; background:#333; padding:10px 15px; border-radius:30px; }
        .admin-link a { color:#ff1a1a; text-decoration:none; }
        @media (max-width:600px){ .col { flex:100%; } }
    </style>
</head>
<body>
<div class="container">
    <h1>📲 VEXORP · OTP PANEL</h1>
    <div class="row">
        <div class="col">
            <h3>📞 Aktif Numaran</h3>
            {% if number %}
                <div class="number-box">{{ get_flag(number) }} {{ number }}</div>
                <p style="margin-top:10px;">Ülke: {{ country }}</p>
            {% else %}
                <p>Henüz numara almadın.</p>
            {% endif %}
        </div>
        <div class="col">
            <h3>🌍 Yeni Numara Al</h3>
            <form method="post" action="/get_number">
                <select name="country" required>
                    <option value="">Seçiniz</option>
                    {% for c in countries %}
                        <option value="{{ c }}">{{ c }} ({{ stok[c]|length }})</option>
                    {% endfor %}
                </select>
                <button type="submit" class="btn" style="margin-top:12px;width:100%;">AL</button>
            </form>
            {% if not countries %}
                <p style="color:#888;">Stok boş, admin eklemeli.</p>
            {% endif %}
        </div>
    </div>

    <h2 style="margin-top:30px;">📨 OTP Geçmişi</h2>
    {% if user_logs %}
        <table>
            <tr><th>Zaman</th><th>Numara</th><th>OTP</th><th>Mesaj</th></tr>
            {% for log in user_logs %}
            <tr>
                <td>{{ log.zaman }}</td>
                <td>{{ log.ulke }} {{ log.numara }}</td>
                <td><span class="otp-badge">{{ log.otp }}</span></td>
                <td>{{ log.mesaj|truncate(60) }}</td>
            </tr>
            {% endfor %}
        </table>
    {% else %}
        <p>Henüz OTP gelmedi.</p>
    {% endif %}

    <div style="text-align:center;margin-top:30px;color:#555;font-size:13px;">
        ⚡ Çoklu API ile gerçek zamanlı OTP takibi
    </div>
</div>
<div class="admin-link"><a href="/admin">🔐 Admin</a></div>
<script>
    // Her 10 saniyede bir sayfa yenile (otomatik güncelleme)
    setTimeout(function(){ location.reload(); }, 10000);
</script>
</body>
</html>
"""

# ====================== APP ÇALIŞTIRMA ======================
if __name__ == "__main__":
    # Arka plan thread'ini başlat
    thread = threading.Thread(target=api_izleme, daemon=True)
    thread.start()
    # Flask uygulamasını çalıştır
    app.run(host="0.0.0.0", port=5000, debug=False)
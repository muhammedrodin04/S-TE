import os
import uuid
import json
from flask import Flask, request, render_template_string, redirect, url_for, session
import httpx
import random
import time
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# === ADMIN AYARLARI (Mutlaka değiştir!) ===
ADMIN_USERNAME = "vexorpvip"
ADMIN_PASSWORD = "12345"   # ← BURAYI GÜÇLÜ BİR ŞİFRE İLE DEĞİŞTİR

SITE_STATUS = {"open": True}
USERS = []

def check_reset(username):
    try:
        client = httpx.Client(http2=True, timeout=20.0)
        host = random.choice(["i.instagram.com", "b.i.instagram.com"])
        bloks_version = "81afa1a45e1df628a85f745314cd89f1bc4e518dd0a4bf62951250fce559ed05"

        headers = {
            'user-agent': 'Instagram 435.0.0.37.76 Android (28/9; 480dpi; 1080x1920; OnePlus; PJD110; marlin; qcom; en_US; 1001775661)',
            'x-ig-app-id': '567067343352427',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        payload = {
            "params": json.dumps({
                "client_input_params": {"search_query": username},
                "server_params": {
                    "event_request_id": str(uuid.uuid4()),
                    "is_from_logged_out": 1,
                }
            }),
            "bk_client_context": json.dumps({"bloks_version": bloks_version}),
            "bloks_versioning_id": bloks_version
        }

        r = client.post(f"https://{host}/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/", 
                       data=payload, headers=headers)
        
        if "We sent a code to" in r.text or "good" in r.text.lower():
            return "✅ GOOD"
        return "❌ BAD"
    except:
        return "❌ ERROR"
    finally:
        client.close()

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect('/adm-vex')
        return f(*args, **kwargs)
    return wrap

@app.route('/')
def home():
    if not SITE_STATUS["open"]:
        return "<h1>Site Kapalıdır.</h1>"
    return render_template_string('''
    <h1>VEXORPVIP RESET LİNK</h1>
    <form method="post" action="/check">
        <input type="text" name="username" placeholder="Instagram Username" required><br><br>
        <button type="submit">Check Reset</button>
    </form>
    <p><a href="/download">📁 Dosya İndir</a></p>
    <p>Telegram: <a href="https://t.me/Vexorpvip">@Vexorpvip</a></p>
    ''')

@app.route('/check', methods=['POST'])
def check():
    if not SITE_STATUS["open"]:
        return "Site kapalı"
    username = request.form.get('username')
    ip = request.remote_addr or request.headers.get('X-Forwarded-For', 'Unknown')
    result = check_reset(username)
    USERS.append({"ip": ip, "user": username, "result": result, "time": time.ctime()})
    return f"<h2>Sonuç: {result}</h2><p>IP: {ip}</p><a href='/'>Geri</a>"

@app.route('/download')
def download():
    return "<h2>📁 Dosya İndirme Bölümü</h2><p>Dosyalar buraya eklenecek.</p><a href='/'>Ana Sayfa</a>"

# ====================== ADMIN PANEL ======================
@app.route('/adm-vex', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('u') == ADMIN_USERNAME and request.form.get('p') == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect('/adm-vex/panel')
        return "Hatalı şifre!"
    return '''
    <h1>Admin Giriş - VEXORPVIP</h1>
    <form method="post">
        Kullanıcı: <input name="u"><br><br>
        Şifre: <input type="password" name="p"><br><br>
        <button>Giriş</button>
    </form>
    '''

@app.route('/adm-vex/panel')
@login_required
def admin_panel():
    return render_template_string('''
    <h1>Admin Panel</h1>
    <p>Durum: {{ "Açık ✅" if status else "Kapalı ❌" }}</p>
    <form action="/adm-vex/toggle" method="post"><button>Siteyi Aç/Kapat</button></form>
    <h2>Kayıtlar</h2>
    <pre>{{ logs }}</pre>
    <a href="/adm-vex/logout">Çıkış</a>
    ''', status=SITE_STATUS["open"], logs=json.dumps(USERS[-50:], indent=2, ensure_ascii=False))

@app.route('/adm-vex/toggle', methods=['POST'])
@login_required
def toggle():
    SITE_STATUS["open"] = not SITE_STATUS["open"]
    return redirect('/adm-vex/panel')

@app.route('/adm-vex/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/adm-vex')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

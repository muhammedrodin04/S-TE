# -*- coding: utf-8 -*-
from flask import Flask, request, render_template_string, session, redirect, url_for, jsonify, flash
import os
import random
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'VEXORPVIP_SUPER_SECRET_2026'

# ---------- VERİTABANI ----------
DB_FILE = '/tmp/data.db'  # Vercel'de /tmp yazılabilir

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            used INTEGER DEFAULT 0,
            ip TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS banned_ips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT UNIQUE,
            banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reason TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            phone TEXT,
            action TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------- ADMIN PANEL ŞİFRESİ ----------
ADMIN_PASSWORD = "vexor2026"

# ---------- YARDIMCI FONKSİYONLAR ----------
def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr
    return ip

def is_banned(ip):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT 1 FROM banned_ips WHERE ip = ?', (ip,))
    result = c.fetchone()
    conn.close()
    return result is not None

def log_action(ip, phone, action):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO logs (ip, phone, action) VALUES (?, ?, ?)', (ip, phone, action))
    conn.commit()
    conn.close()

def generate_codes(phone, count=50):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    codes = []
    for _ in range(count):
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        codes.append(code)
        c.execute('INSERT INTO codes (phone, code, ip) VALUES (?, ?, ?)', (phone, code, get_client_ip()))
    conn.commit()
    conn.close()
    log_action(get_client_ip(), phone, f'{count} kod oluşturuldu')
    return codes

def get_stats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM codes')
    total_codes = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM codes WHERE used = 1')
    used_codes = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM banned_ips')
    banned_count = c.fetchone()[0]
    conn.close()
    return total_codes, used_codes, banned_count

# ---------- HTML ŞABLONLARI ----------
MAIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>VEXORPVIP · CODE GENERATOR</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: #0a0a0f;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            color: #d0d8f0;
        }
        .container {
            max-width: 500px;
            width: 100%;
            background: #0d0d1a;
            border-radius: 30px;
            padding: 35px 30px;
            border: 1px solid #1e2d4a;
            box-shadow: 0 0 40px rgba(0,255,180,0.05);
        }
        .logo { text-align: center; margin-bottom: 30px; }
        .logo h1 { color: #00ffb3; font-size: 2rem; text-shadow: 0 0 20px rgba(0,255,180,0.2); }
        .logo span { color: #4a6a8a; font-size: 0.8rem; }
        .form-group { margin: 15px 0; }
        label { display: block; margin-bottom: 8px; color: #8cf0d0; font-weight: 600; }
        input[type="text"] {
            width: 100%;
            padding: 14px;
            background: #0b1222;
            border: 2px solid #2a3a5c;
            border-radius: 12px;
            color: #d0d8f0;
            font-size: 1rem;
        }
        input:focus { border-color: #00ffb3; outline: none; }
        .btn {
            width: 100%;
            padding: 14px;
            background: #00ffb3;
            color: #0a0a0f;
            border: none;
            border-radius: 30px;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            transition: 0.3s;
            margin-top: 5px;
        }
        .btn:hover { background: #00cc99; transform: scale(1.02); }
        .alert {
            background: #2a1a1a;
            border: 1px solid #ff6b6b;
            border-radius: 12px;
            padding: 15px;
            margin: 15px 0;
            color: #ff6b6b;
            text-align: center;
        }
        .alert-success {
            background: #1a2a1a;
            border-color: #00ffb3;
            color: #00ffb3;
        }
        .code-list {
            background: #0b1222;
            border-radius: 12px;
            padding: 15px;
            margin: 15px 0;
            max-height: 300px;
            overflow-y: auto;
        }
        .code-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 12px;
            border-bottom: 1px solid #1a2a4a;
            font-family: monospace;
        }
        .code-item .used { color: #ff6b6b; }
        .code-item .unused { color: #00ffb3; }
        .footer {
            margin-top: 25px;
            text-align: center;
            color: #4a6a8a;
            font-size: 0.75rem;
            border-top: 1px solid #0f1f33;
            padding-top: 15px;
        }
        .badge {
            display: inline-block;
            background: #132233;
            padding: 5px 15px;
            border-radius: 30px;
            border: 1px solid #2a6a8a;
            font-size: 0.7rem;
            color: #8cf0d0;
        }
        .admin-link {
            display: block;
            text-align: center;
            margin-top: 15px;
            color: #4a6a8a;
            font-size: 0.8rem;
        }
        .admin-link a { color: #00ffb3; text-decoration: none; }
        .admin-link a:hover { text-decoration: underline; }
    </style>
</head>
<body>
<div class="container">
    <div class="logo">
        <h1>🔐 VEXORPVIP</h1>
        <span>CODE GENERATOR · 2026</span>
    </div>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}
            <div class="alert {% if category == 'success' %}alert-success{% endif %}">
                {{ message }}
            </div>
        {% endfor %}
    {% endwith %}
    <form action="/generate" method="post">
        <div class="form-group">
            <label>📱 Telefon Numarası</label>
            <input type="text" name="phone" placeholder="Ör: 905551234567" required>
        </div>
        <button type="submit" class="btn">⚡ 50 Kod Oluştur</button>
    </form>
    {% if codes %}
    <div style="margin-top:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#8cf0d0;">📋 Oluşturulan Kodlar</span>
            <span class="badge">{{ codes|length }} adet</span>
        </div>
        <div class="code-list">
            {% for code, used, created in codes %}
            <div class="code-item">
                <span>{{ code }}</span>
                <span class="{% if used %}used{% else %}unused{% endif %}">
                    {% if used %}❌ Kullanıldı{% else %}✅ Aktif{% endif %}
                </span>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    <div class="admin-link">
        <a href="/vexorp-admin">🔑 Admin Paneli</a>
    </div>
    <div class="footer">
        <span style="color:#00ffb3;">❯</span> Bilgi paylaşıldıkça güçlenir.
    </div>
</div>
</body>
</html>
"""

ADMIN_PANEL = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>VEXORPVIP · Admin Panel</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background: #0a0a0f; font-family: 'Segoe UI', sans-serif; padding: 20px; color: #d0d8f0; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #1e2d4a;
            padding-bottom: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
            gap: 15px;
        }
        .header h1 { color: #00ffb3; }
        .header .logout { color: #ff6b6b; text-decoration: none; padding: 8px 20px; border: 1px solid #ff6b6b; border-radius: 30px; }
        .header .logout:hover { background: #ff6b6b; color: #0a0a0f; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #0d0d1a;
            border: 1px solid #1e2d4a;
            border-radius: 16px;
            padding: 20px;
            text-align: center;
        }
        .stat-card .number { font-size: 2rem; color: #00ffb3; font-weight: 700; }
        .stat-card .label { color: #4a6a8a; font-size: 0.8rem; margin-top: 5px; }
        .table-container {
            background: #0d0d1a;
            border-radius: 16px;
            border: 1px solid #1e2d4a;
            padding: 20px;
            overflow-x: auto;
            margin-bottom: 30px;
        }
        table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
        th { text-align: left; padding: 12px 10px; color: #8cf0d0; border-bottom: 2px solid #1e2d4a; }
        td { padding: 10px; border-bottom: 1px solid #0f1f33; }
        .ban-btn {
            background: #ff6b6b;
            color: #0a0a0f;
            border: none;
            padding: 5px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.75rem;
        }
        .ban-btn:hover { background: #cc5555; }
        .unban-btn {
            background: #00ffb3;
            color: #0a0a0f;
            border: none;
            padding: 5px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.75rem;
        }
        .unban-btn:hover { background: #00cc99; }
        .banned { color: #ff6b6b; font-weight: 700; }
        .active { color: #00ffb3; font-weight: 700; }
        .tab-bar {
            display: flex;
            gap: 5px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .tab-btn {
            padding: 10px 25px;
            background: #0b1222;
            border: 1px solid #2a3a5c;
            border-radius: 30px;
            color: #d0d8f0;
            cursor: pointer;
            font-weight: 600;
        }
        .tab-btn.active {
            background: #00ffb3;
            color: #0a0a0f;
            border-color: #00ffb3;
        }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .admin-login {
            max-width: 400px;
            margin: 50px auto;
            background: #0d0d1a;
            border-radius: 30px;
            padding: 35px;
            border: 1px solid #1e2d4a;
        }
        .admin-login input { width: 100%; padding: 14px; background: #0b1222; border: 2px solid #2a3a5c; border-radius: 12px; color: #d0d8f0; margin: 10px 0; }
        .admin-login .btn { width: 100%; padding: 14px; background: #00ffb3; color: #0a0a0f; border: none; border-radius: 30px; font-weight: 700; cursor: pointer; }
        @media (max-width: 600px) {
            .stats { grid-template-columns: 1fr 1fr; }
            .header { flex-direction: column; align-items: stretch; text-align: center; }
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🔐 VEXORPVIP Admin</h1>
        <div>
            <span style="margin-right:15px; color:#4a6a8a;">👤 Admin</span>
            <a href="/vexorp-admin?logout=1" class="logout">🚪 Çıkış</a>
        </div>
    </div>
    <div class="stats">
        <div class="stat-card">
            <div class="number">{{ stats.total_codes }}</div>
            <div class="label">📋 Toplam Kod</div>
        </div>
        <div class="stat-card">
            <div class="number">{{ stats.used_codes }}</div>
            <div class="label">✅ Kullanılan</div>
        </div>
        <div class="stat-card">
            <div class="number">{{ stats.banned_count }}</div>
            <div class="label">🚫 Banlı IP</div>
        </div>
        <div class="stat-card">
            <div class="number">{{ logs|length }}</div>
            <div class="label">📝 Log Kaydı</div>
        </div>
    </div>
    <div class="tab-bar">
        <button class="tab-btn active" onclick="showTab('logs')">📝 Loglar</button>
        <button class="tab-btn" onclick="showTab('codes')">📋 Kodlar</button>
        <button class="tab-btn" onclick="showTab('bans')">🚫 Ban Listesi</button>
    </div>
    <div id="tab-logs" class="tab-content active">
        <div class="table-container">
            <table>
                <thead><tr><th>ID</th><th>IP</th><th>Telefon</th><th>İşlem</th><th>Tarih</th></tr></thead>
                <tbody>
                    {% for log in logs %}
                    <tr><td>{{ log[0] }}</td><td>{{ log[1] }}</td><td>{{ log[2] }}</td><td>{{ log[3] }}</td><td>{{ log[4] }}</td></tr>
                    {% endfor %}
                    {% if not logs %}<tr><td colspan="5" style="text-align:center; color:#4a6a8a;">Henüz log kaydı yok</td></tr>{% endif %}
                </tbody>
            </table>
        </div>
    </div>
    <div id="tab-codes" class="tab-content">
        <div class="table-container">
            <table>
                <thead><tr><th>ID</th><th>Telefon</th><th>Kod</th><th>Durum</th><th>IP</th><th>Oluşturma</th></tr></thead>
                <tbody>
                    {% for code in all_codes %}
                    <tr><td>{{ code[0] }}</td><td>{{ code[1] }}</td><td>{{ code[2] }}</td><td>{% if code[4] %}❌ Kullanıldı{% else %}✅ Aktif{% endif %}</td><td>{{ code[5] }}</td><td>{{ code[3] }}</td></tr>
                    {% endfor %}
                    {% if not all_codes %}<tr><td colspan="6" style="text-align:center; color:#4a6a8a;">Henüz kod oluşturulmamış</td></tr>{% endif %}
                </tbody>
            </table>
        </div>
    </div>
    <div id="tab-bans" class="tab-content">
        <div class="table-container">
            <table>
                <thead><tr><th>ID</th><th>IP</th><th>Ban Tarihi</th><th>Sebep</th><th>İşlem</th></tr></thead>
                <tbody>
                    {% for ban in bans %}
                    <tr>
                        <td>{{ ban[0] }}</td>
                        <td class="banned">{{ ban[1] }}</td>
                        <td>{{ ban[2] }}</td>
                        <td>{{ ban[3] or 'Sistem tarafından' }}</td>
                        <td>
                            <form action="/admin/unban" method="post" style="display:inline;">
                                <input type="hidden" name="ip" value="{{ ban[1] }}">
                                <button type="submit" class="unban-btn">✅ Kaldır</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                    {% if not bans %}<tr><td colspan="5" style="text-align:center; color:#4a6a8a;">Banlanmış IP yok</td></tr>{% endif %}
                </tbody>
            </table>
        </div>
    </div>
</div>
<script>
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById('tab-' + tabName).classList.add('active');
    document.querySelector(`.tab-btn[onclick="showTab('${tabName}')"]`).classList.add('active');
}
</script>
</body>
</html>
"""

# ---------- ROTALAR ----------
@app.route('/')
def index():
    ip = get_client_ip()
    if is_banned(ip):
        return render_template_string("""
            <div style="text-align:center;padding:50px;background:#0a0a0f;color:#ff6b6b;min-height:100vh;display:flex;justify-content:center;align-items:center;flex-direction:column;">
                <h1 style="font-size:3rem;">🚫</h1>
                <h2>IP Adresiniz Banlandı</h2>
                <p style="color:#4a6a8a;">Bu siteden erişiminiz engellenmiştir.</p>
            </div>
        """), 403
    return render_template_string(MAIN_PAGE, codes=None)

@app.route('/generate', methods=['POST'])
def generate():
    ip = get_client_ip()
    if is_banned(ip):
        return "IP banlı", 403
    phone = request.form.get('phone', '').strip()
    if not phone or len(phone) < 10:
        flash('Geçerli bir telefon numarası girin')
        return redirect(url_for('index'))
    codes = generate_codes(phone, 50)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT code, used, created_at FROM codes WHERE phone = ? ORDER BY created_at DESC LIMIT 50', (phone,))
    result = c.fetchall()
    conn.close()
    flash(f'{len(codes)} kod başarıyla oluşturuldu!', 'success')
    return render_template_string(MAIN_PAGE, codes=result)

@app.route('/vexorp-admin', methods=['GET', 'POST'])
def admin_panel():
    ip = get_client_ip()
    if request.args.get('logout'):
        session.pop('admin_logged_in', None)
        return redirect(url_for('admin_panel'))
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Giriş başarılı!', 'success')
        else:
            flash('Şifre yanlış!', 'error')
        return redirect(url_for('admin_panel'))
    if not session.get('admin_logged_in'):
        return render_template_string("""
            <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Admin Girişi</title>
            <style>body{background:#0a0a0f;font-family:'Segoe UI',sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;color:#d0d8f0;}.login-box{max-width:400px;width:100%;background:#0d0d1a;border-radius:30px;padding:35px;border:1px solid #1e2d4a;}h1{color:#00ffb3;text-align:center;}input{width:100%;padding:14px;background:#0b1222;border:2px solid #2a3a5c;border-radius:12px;color:#d0d8f0;margin:10px 0;}.btn{width:100%;padding:14px;background:#00ffb3;color:#0a0a0f;border:none;border-radius:30px;font-weight:700;cursor:pointer;}.btn:hover{background:#00cc99;}.alert{background:#2a1a1a;border:1px solid #ff6b6b;border-radius:12px;padding:15px;margin:10px 0;color:#ff6b6b;text-align:center;}</style>
            </head><body><div class="login-box"><h1>🔐 Admin Girişi</h1>
            {% with messages = get_flashed_messages() %}{% for msg in messages %}<div class="alert">{{ msg }}</div>{% endfor %}{% endwith %}
            <form method="post"><input type="password" name="password" placeholder="Admin Şifresi" required><button type="submit" class="btn">Giriş Yap</button></form></div></body></html>
        """)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, ip, phone, action, timestamp FROM logs ORDER BY id DESC LIMIT 200')
    logs = c.fetchall()
    c.execute('SELECT id, phone, code, created_at, used, ip FROM codes ORDER BY id DESC LIMIT 200')
    all_codes = c.fetchall()
    c.execute('SELECT id, ip, banned_at, reason FROM banned_ips ORDER BY id DESC')
    bans = c.fetchall()
    conn.close()
    stats = get_stats()
    return render_template_string(
        ADMIN_PANEL,
        stats={'total_codes': stats[0], 'used_codes': stats[1], 'banned_count': stats[2]},
        logs=logs,
        all_codes=all_codes,
        bans=bans
    )

@app.route('/admin/unban', methods=['POST'])
def admin_unban():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_panel'))
    ip = request.form.get('ip', '')
    if ip:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('DELETE FROM banned_ips WHERE ip = ?', (ip,))
        conn.commit()
        conn.close()
        flash(f'IP {ip} banı kaldırıldı', 'success')
    return redirect(url_for('admin_panel'))

# Bu kısım Vercel için çok önemli!
app.debug = False

# Vercel için handler
def handler(request, *args, **kwargs):
    return app(request, *args, **kwargs)

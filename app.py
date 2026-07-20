import os
import uuid
import json
from flask import Flask, request, render_template_string, redirect, url_for, session, jsonify
import httpx
import random
import time
import secrets
from functools import wraps

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Change in production

# Admin credentials (change these!)
ADMIN_USERNAME = "vexorpvip"
ADMIN_PASSWORD = "your_secure_password_here"  # CHANGE THIS!

# Site status
SITE_STATUS = {"open": True}
USERS = []  # In-memory for demo; use DB in prod

# The provided checker function (cleaned/adapted)
def check_reset(username):
    client = httpx.Client(http2=True, timeout=30.0)
    host = random.choice(["i.instagram.com", "b.i.instagram.com"])
    bloks_version = "81afa1a45e1df628a85f745314cd89f1bc4e518dd0a4bf62951250fce559ed05"

    def _headers(friendly_name):
        return {
            'accept-language': 'en-US',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'ig-intended-user-id': '0',
            'priority': 'u=3',
            'x-bloks-is-layout-rtl': 'false',
            'x-bloks-prism-button-version': 'INDIGO_PRIMARY_BORDERED_SECONDARY',
            'x-bloks-prism-colors-enabled': 'true',
            'x-bloks-extended-palette-gray': 'true',
            'x-bloks-extended-palette-indigo': 'true',
            'x-bloks-prism-extended-palette-polish-enabled': 'false',
            'x-bloks-prism-extended-palette-red': 'true',
            'x-bloks-prism-extended-palette-rest-of-colors': 'true',
            'x-bloks-prism-font-enabled': 'true',
            'x-bloks-prism-indigo-link-version': '1',
            'x-bloks-version-id': bloks_version,
            'x-fb-client-ip': 'True',
            'x-fb-connection-type': 'WIFI',
            'x-fb-friendly-name': f'IgApi: {friendly_name}/',
            'x-fb-request-analytics-tags': '{"network_tags":{"product":"567067343352427","surface":"undefined","request_category":"api","purpose":"fetch","retry_attempt":"0"}}',
            'x-fb-server-cluster': 'True',
            'x-ig-android-id': f'android-{str(uuid.uuid4().hex)[:16]}',
            'x-ig-app-id': '567067343352427',
            'x-ig-app-locale': 'en_US',
            'x-ig-bandwidth-speed-kbps': '7060.000',
            'x-ig-bandwidth-totalbytes-b': '13597412',
            'x-ig-bandwidth-totaltime-ms': '1586',
            'x-ig-client-endpoint': 'IgCdsScreenNavigationLoggerModule:com.bloks.www.caa.ar.search',
            'x-ig-capabilities': '3brTv10=',
            'x-ig-connection-type': 'WIFI',
            'x-ig-device-id': f'{str(uuid.uuid4())}',
            'x-ig-device-locale': 'en_US',
            'x-ig-family-device-id': f'{str(uuid.uuid4())}',
            'x-ig-is-foldable': 'false',
            'x-ig-mapped-locale': 'en_US',
            'x-ig-timezone-offset': '19800',
            'x-ig-www-claim': '0',
            'x-pigeon-rawclienttime': f'{int(time.time())}.030',
            'x-pigeon-session-id': f'UFS-{str(uuid.uuid4())}-1',
            'x-tigon-is-retry': 'False',
            'user-agent': 'Instagram 435.0.0.37.76 Android (28/9; 480dpi; 1080x1920; OnePlus; PJD110; marlin; qcom; en_US; 1001775661)',
            'x-fb-conn-uuid-client': f'{str(uuid.uuid4())}',
            'x-fb-http-engine': 'Tigon/MNS/TCP',
        }

    try:
        # Simplified payload for demo - adapt as needed
        params = {
            "client_input_params": {
                "search_query": username,
            },
            "server_params": {
                "event_request_id": str(uuid.uuid4()),
                "is_from_logged_out": 1,
                "device_id": f"android-{str(uuid.uuid4().hex)[:16]}",
            }
        }

        payload = {
            'params': json.dumps(params, separators=(',', ':')),
            'bk_client_context': json.dumps({
                "bloks_version": bloks_version,
                "styles_id": "instagram",
            }, separators=(',', ':')),
            'bloks_versioning_id': bloks_version
        }

        response = client.post(
            f"https://{host}/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/",
            data=payload,
            headers=_headers('bloks/async_action/com.bloks.www.caa.ar.search.async')
        )

        clean_response = response.text.replace("/", "").replace("\\", "")
        if "We sent a code to" in clean_response or "good" in clean_response.lower():
            return "good"
        return "bad"
    except Exception as e:
        return f"error: {str(e)}"
    finally:
        client.close()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    if not SITE_STATUS["open"]:
        return "<h1>Site is currently closed.</h1>"
    return render_template_string('''
    <h1>VEXORPVIP RESET LINK</h1>
    <form action="/check" method="post">
        <input type="text" name="username" placeholder="Instagram Username" required>
        <button type="submit">Check Reset</button>
    </form>
    <p><a href="/download">Download Files</a></p>
    <p>Contact: <a href="https://t.me/Vexorpvip">@Vexorpvip</a></p>
    ''')

@app.route('/check', methods=['POST'])
def check():
    if not SITE_STATUS["open"]:
        return "Site closed"
    username = request.form.get('username')
    ip = request.remote_addr or request.headers.get('X-Forwarded-For')
    result = check_reset(username)
    
    # Log user
    USERS.append({"ip": ip, "username": username, "result": result, "time": time.ctime()})
    
    return f"<h2>Result for {username}: {result}</h2><p>IP logged: {ip}</p>"

@app.route('/download')
def download():
    return "<h2>Download Section</h2><p>Files will be here (add links to actual files).</p>"

# Admin Panel
@app.route('/adm-vex', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USERNAME and request.form.get('password') == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        return "Invalid credentials"
    return '''
    <h1>Admin Login - VEXORPVIP</h1>
    <form method="post">
        Username: <input name="username"><br>
        Password: <input type="password" name="password"><br>
        <button type="submit">Login</button>
    </form>
    '''

@app.route('/adm-vex/panel')
@login_required
def admin_panel():
    return render_template_string('''
    <h1>VEXORPVIP Admin Panel</h1>
    <p>Site Status: {{ "Open" if status else "Closed" }}</p>
    <form action="/adm-vex/toggle" method="post">
        <button type="submit">Toggle Site Open/Close</button>
    </form>
    <h2>Users / Logs</h2>
    <pre>{{ users }}</pre>
    <a href="/adm-vex/logout">Logout</a>
    ''', status=SITE_STATUS["open"], users=json.dumps(USERS, indent=2))

@app.route('/adm-vex/toggle', methods=['POST'])
@login_required
def toggle_site():
    SITE_STATUS["open"] = not SITE_STATUS["open"]
    return redirect(url_for('admin_panel'))

@app.route('/adm-vex/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, send_file
import httpx
import json
import uuid
import secrets
import random
import time
import os
from datetime import datetime
import threading

app = Flask(__name__)

# Admin paneli şifresi
ADMIN_PASSWORD = "vexorpvip2024"

# Site durumu
site_status = {"active": True}

# Ziyaretçi IP'leri ve logları
visitor_logs = []

# Dosya yükleme klasörü
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def check_reset(username):
    """Instagram reset kontrol fonksiyonu"""
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

    def _bk_context():
        return json.dumps({
            "bloks_version": bloks_version,
            "styles_id": "instagram",
            "theme_params": [{"value": ["three_neutral_gray"], "design_system_name": "XMDS"}]
        }, separators=(',', ':'))

    device_id = f"android-{str(uuid.uuid4().hex)[:16]}"
    family_device_id = str(uuid.uuid4())
    waterfall_id = str(uuid.uuid4())
    event_request_id = str(uuid.uuid4())
    aac_init_timestamp = int(time.time())
    aacjid = str(uuid.uuid4())
    aaccs = "AW" + secrets.token_urlsafe(32).replace('=', '').replace('+', '').replace('/', '')

    params = {
        "client_input_params": {
            "blocked_uids": [],
            "aac": json.dumps({
                "aac_init_timestamp": aac_init_timestamp,
                "aacjid": aacjid,
                "aaccs": aaccs
            }),
            "flash_call_permissions_status": {
                "READ_PHONE_STATE": "GRANTED",
                "READ_CALL_LOG": "DENIED",
                "ANSWER_PHONE_CALLS": "DENIED"
            },
            "was_headers_prefill_available": 0,
            "network_bssid": None,
            "sfdid": "",
            "fetched_email_token_list": {},
            "search_query": username,
            "auth_secure_device_id": "",
            "ig_oauth_token": [],
            "cloud_trust_token": None,
            "was_headers_prefill_used": 0,
            "sso_accounts_auth_data": [],
            "encrypted_msisdn": "",
            "device_network_info": {
                "default_subscription_info": {
                    "network_type": 13,
                    "is_data_roaming": 1,
                    "is_esim": 0,
                    "is_gsm_roaming": 0,
                    "is_sim_sms_capable": None,
                    "is_mobile_data_enabled": 1,
                    "sim_carrier_id": -1,
                    "sim_carrier_id_name": None,
                    "sim_state": 5,
                    "sim_operator": "310005",
                    "sim_operator_name": "Verizon Wireless",
                    "signal_strength": None,
                    "group_id_level_1": None,
                    "network_operator": "310005"
                },
                "sim_count": 1,
                "is_wifi": 1,
                "is_airplane_mode": 0,
                "is_active_network_cellular": 0,
                "is_device_sms_capable": 1,
                "active_subscriptions_info": [{
                    "network_type": 13,
                    "is_data_roaming": 1,
                    "is_esim": 0,
                    "is_gsm_roaming": 0,
                    "is_sim_sms_capable": None,
                    "is_mobile_data_enabled": 1,
                    "sim_carrier_id": -1,
                    "sim_carrier_id_name": None,
                    "sim_state": 5,
                    "sim_operator": "310005",
                    "sim_operator_name": "Verizon Wireless",
                    "signal_strength": None,
                    "group_id_level_1": None,
                    "network_operator": "310005"
                }]
            },
            "text_input_id": "4cbr8a:53",
            "zero_balance_state": None,
            "android_build_type": "release",
            "accounts_list": [],
            "is_oauth_without_permission": 0,
            "ig_android_qe_device_id": str(uuid.uuid4()),
            "gms_incoming_call_retriever_eligibility": "not_eligible",
            "search_screen_type": "email_or_username",
            "is_whatsapp_installed": 0,
            "lois_settings": {"lois_token": ""},
            "ig_vetted_device_nonce": None,
            "headers_infra_flow_id": "",
            "fetched_email_list": []
        },
        "server_params": {
            "event_request_id": event_request_id,
            "is_from_logged_out": 1,
            "layered_homepage_experiment_group": "Deploy: Not in Experiment",
            "device_id": device_id,
            "login_surface": "login_home",
            "waterfall_id": waterfall_id,
            "INTERNAL__latency_qpl_instance_id": 26256860200107,
            "is_platform_login": 0,
            "context_data": "",
            "login_entry_point": "logged_out",
            "INTERNAL__latency_qpl_marker_id": 36707139,
            "family_device_id": family_device_id,
            "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
            "access_flow_version": "pre_mt_behavior",
            "is_from_logged_in_switcher": 0,
            "qe_device_id": str(uuid.uuid4())
        }
    }

    payload = {
        'params': json.dumps(params, separators=(',', ':')),
        'bk_client_context': _bk_context(),
        'bloks_versioning_id': bloks_version
    }

    try:
        response = client.post(
            f"https://{host}/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/",
            data=payload,
            headers=_headers('bloks/async_action/com.bloks.www.caa.ar.search.async')
        )

        response_text = response.text
        clean_response = response_text.replace("/", "").replace("\\", "")

        if "We sent a code to" in clean_response:
            return "good"
        else:
            return "bad"

    except Exception as e:
        return f"error - {str(e)}"
    finally:
        client.close()

@app.route('/')
def index():
    """Ana sayfa"""
    if not site_status["active"]:
        return "Site şu anda bakımda.", 503
    
    # IP adresini logla
    user_ip = request.remote_addr
    visitor_logs.append({
        "ip": user_ip,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_agent": request.headers.get('User-Agent', 'Unknown')
    })
    
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    """Instagram reset kontrol endpoint'i"""
    if not site_status["active"]:
        return jsonify({"error": "Site şu anda bakımda."}), 503
    
    data = request.json
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({"error": "Kullanıcı adı gerekli."}), 400
    
    result = check_reset(username)
    
    return jsonify({
        "username": username,
        "result": result,
        "ip": request.remote_addr,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/admin-panel')
def admin_panel():
    """Admin paneli (VEXORPVIP)"""
    return render_template('admin.html')

@app.route('/admin-login', methods=['POST'])
def admin_login():
    """Admin giriş kontrolü"""
    data = request.json
    password = data.get('password', '')
    
    if password == ADMIN_PASSWORD:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Geçersiz şifre."}), 401

@app.route('/admin-data')
def admin_data():
    """Admin paneli verileri"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or auth_header != f"Bearer {ADMIN_PASSWORD}":
        return jsonify({"error": "Yetkisiz erişim."}), 401
    
    return jsonify({
        "logs": visitor_logs[-50:],  # Son 50 log
        "total_visitors": len(visitor_logs),
        "site_status": site_status["active"],
        "files": os.listdir(UPLOAD_FOLDER) if os.path.exists(UPLOAD_FOLDER) else []
    })

@app.route('/toggle-site', methods=['POST'])
def toggle_site():
    """Site aç/kapa"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or auth_header != f"Bearer {ADMIN_PASSWORD}":
        return jsonify({"error": "Yetkisiz erişim."}), 401
    
    site_status["active"] = not site_status["active"]
    return jsonify({"active": site_status["active"]})

@app.route('/upload-file', methods=['POST'])
def upload_file():
    """Dosya yükleme"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or auth_header != f"Bearer {ADMIN_PASSWORD}":
        return jsonify({"error": "Yetkisiz erişim."}), 401
    
    if 'file' not in request.files:
        return jsonify({"error": "Dosya bulunamadı."}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Dosya seçilmedi."}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    return jsonify({"success": True, "filename": file.filename})

@app.route('/download-file/<filename>')
def download_file(filename):
    """Dosya indirme"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or auth_header != f"Bearer {ADMIN_PASSWORD}":
        return jsonify({"error": "Yetkisiz erişim."}), 401
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "Dosya bulunamadı."}), 404
    
    return send_file(file_path, as_attachment=True)

@app.route('/delete-file/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Dosya silme"""
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or auth_header != f"Bearer {ADMIN_PASSWORD}":
        return jsonify({"error": "Yetkisiz erişim."}), 401
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "Dosya bulunamadı."}), 404
    
    os.remove(file_path)
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)

# -*- coding: utf-8 -*-
from flask import Flask, request, render_template_string, send_file, session, redirect, url_for, flash
import os
import zlib
import base64
import marshal
import uuid
import tempfile
import time

app = Flask(__name__)
app.secret_key = 'VEXORPVIP_SUPER_GIZLI_ANAHTAR_2026'
app.config['SESSION_TYPE'] = 'filesystem'

# ---------- ENCODE FONKSİYONLARI ----------
zlb = lambda in_: zlib.compress(in_)
b16 = lambda in_: base64.b16encode(in_)
b32 = lambda in_: base64.b32encode(in_)
b64 = lambda in_: base64.b64encode(in_)
mar = lambda in_: marshal.dumps(compile(in_, '<x>', 'exec'))
note = "# Güzeliğin kadar ömrüm olsa bir ömür yaşarım \n"

def encode_option(option, data):
    try:
        if option == 1:
            xx = "mar(data.encode('utf8'))[::-1]"
            heading = "_ = lambda __ : __import__('marshal').loads(__[::-1]);"
        elif option == 2:
            xx = "zlb(data.encode('utf8'))[::-1]"
            heading = "_ = lambda __ : __import__('zlib').decompress(__[::-1]);"
        elif option == 3:
            xx = "b16(data.encode('utf8'))[::-1]"
            heading = "_ = lambda __ : __import__('base64').b16decode(__[::-1]);"
        elif option == 4:
            xx = "b32(data.encode('utf8'))[::-1]"
            heading = "_ = lambda __ : __import__('base64').b32decode(__[::-1]);"
        elif option == 5:
            xx = "b64(data.encode('utf8'))[::-1]"
            heading = "_ = lambda __ : __import__('base64').b64decode(__[::-1]);"
        elif option == 6:
            xx = "b16(zlb(data.encode('utf8')))[::-1]"
            heading = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b16decode(__[::-1]));"
        elif option == 7:
            xx = "b32(zlb(data.encode('utf8')))[::-1]"
            heading = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));"
        elif option == 8:
            xx = "b64(zlb(data.encode('utf8')))[::-1]"
            heading = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));"
        elif option == 9:
            xx = "zlb(mar(data.encode('utf8')))[::-1]"
            heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__[::-1]));"
        elif option == 10:
            xx = "b16(mar(data.encode('utf8')))[::-1]"
            heading = "_ = lambda __ : __import__('marshal').loads(__import__('base64').b16decode(__[::-1]));"
        elif option == 11:
            xx = "b32(mar(data.encode('utf8')))[::-1]"
            heading = "_ = lambda __ : __import__('marshal').loads(__import__('base64').b32decode(__[::-1]));"
        elif option == 12:
            xx = "b64(mar(data.encode('utf8')))[::-1]"
            heading = "_ = lambda __ : __import__('marshal').loads(__import__('base64').b64decode(__[::-1]));"
        elif option == 13:
            xx = "b16(zlb(mar(data.encode('utf8'))))[::-1]"
            heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b16decode(__[::-1])));"
        elif option == 14:
            xx = "b32(zlb(mar(data.encode('utf8'))))[::-1]"
            heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b32decode(__[::-1])));"
        elif option == 15:
            xx = "b64(zlb(mar(data.encode('utf8'))))[::-1]"
            heading = "_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode(__[::-1])));"
        elif option == 16:
            for x in range(5):
                method = repr(b64(zlb(mar(data.encode('utf8'))))[::-1])
                data = "exec(__import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b64decode(%s[::-1]))))" % method
            z = []
            for i in data:
                z.append(ord(i))
            sata = "_ = %s\nexec(''.join(chr(__) for __ in _))" % z
            return note + sata
        else:
            return None
        
        for _ in range(1):
            data = "exec((_)(%s))" % repr(eval(xx))
        return note + heading + data
    except Exception as e:
        return None

# ---------- WEB ARAYÜZÜ ----------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>VEXORPVİP ENCODE</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            background: #0a0a0f; 
            color: #d0d8f0; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            padding: 20px; 
        }
        .container { 
            max-width: 750px; 
            width: 100%; 
            background: #0d0d1a; 
            border-radius: 30px; 
            padding: 35px 30px; 
            border: 1px solid #1e2d4a; 
            box-shadow: 0 0 40px rgba(0,255,180,0.05);
        }
        .logo { text-align: center; margin-bottom: 25px; }
        .logo h1 { 
            color: #00ffb3; 
            font-size: 2.2rem;
            text-shadow: 0 0 20px rgba(0,255,180,0.2);
            letter-spacing: 2px;
        }
        .logo span { color: #4a6a8a; font-size: 0.9rem; display: block; margin-top: 5px; }
        .form-group { margin: 20px 0; }
        label { 
            display: block; 
            margin-bottom: 8px; 
            color: #8cf0d0; 
            font-weight: 600;
            font-size: 0.95rem;
        }
        input[type="file"] { 
            width: 100%; 
            padding: 14px; 
            background: #0b1222; 
            border: 2px dashed #2a3a5c; 
            border-radius: 12px; 
            color: #d0d8f0;
            cursor: pointer;
        }
        input[type="file"]:hover { border-color: #00ffb3; }
        select { 
            width: 100%; 
            padding: 14px; 
            background: #0b1222; 
            border: 2px solid #2a3a5c; 
            border-radius: 12px; 
            color: #d0d8f0;
            font-size: 1rem;
            cursor: pointer;
        }
        select:hover { border-color: #00ffb3; }
        select option { background: #0d0d1a; }
        .btn { 
            background: #00ffb3; 
            color: #0a0a0f; 
            border: none; 
            padding: 14px 35px; 
            border-radius: 30px; 
            font-weight: 700; 
            font-size: 1rem;
            cursor: pointer; 
            transition: all 0.3s;
            width: 100%;
            margin-top: 5px;
        }
        .btn:hover { 
            background: #00cc99; 
            transform: scale(1.02);
            box-shadow: 0 0 30px rgba(0,255,180,0.2);
        }
        .btn-secondary {
            background: transparent;
            color: #ff6b6b;
            border: 2px solid #ff6b6b;
            margin-top: 10px;
            width: auto;
            padding: 10px 25px;
        }
        .btn-secondary:hover {
            background: #ff6b6b;
            color: #0a0a0f;
        }
        .footer { 
            margin-top: 30px; 
            text-align: center; 
            color: #4a6a8a; 
            font-size: 0.8rem; 
            border-top: 1px solid #0f1f33; 
            padding-top: 20px; 
        }
        .badge { 
            display: inline-block; 
            background: #132233; 
            padding: 5px 18px; 
            border-radius: 30px; 
            border: 1px solid #2a6a8a; 
            font-size: 0.75rem; 
            color: #8cf0d0;
            margin: 5px 0;
        }
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
        .file-info {
            background: #0b1222;
            border-radius: 12px;
            padding: 15px;
            margin: 15px 0;
            border: 1px solid #2a3a5c;
            color: #8cf0d0;
            text-align: center;
        }
        .file-info i { margin-right: 10px; }
        .flex-row { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
        @media (max-width: 500px) {
            .container { padding: 20px 15px; }
            .logo h1 { font-size: 1.5rem; }
            .flex-row { flex-direction: column; }
            .btn-secondary { width: 100%; }
        }
    </style>
</head>
<body>
<div class="container">
    <div class="logo">
        <h1>🔐 VEXORPVİP</h1>
        <span>Python Encoder · 2026</span>
        <div style="margin-top: 10px;">
            <span class="badge">⚡ ETHICAL HACKING</span>
            <span class="badge">🛡️ SECURE</span>
        </div>
    </div>

    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <div class="alert">
                {% for message in messages %}
                    {{ message }}
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    {% if not session.get('file_uploaded') %}
    <form action="/upload" method="post" enctype="multipart/form-data">
        <div class="form-group">
            <label>📂 Python Dosyası Seç (.py)</label>
            <input type="file" name="file" accept=".py" required>
        </div>
        <button type="submit" class="btn">Dosyayı Yükle</button>
    </form>
    {% else %}
    <div class="file-info">
        <i>📄</i> Dosya yüklendi: <strong>{{ session.get('filename', '') }}</strong>
    </div>
    <form action="/encode" method="post">
        <div class="form-group">
            <label>🔧 Encode Yöntemi Seç</label>
            <select name="option">
                <option value="1">Marshal</option>
                <option value="2">Zlib</option>
                <option value="3">Base16</option>
                <option value="4">Base32</option>
                <option value="5">Base64</option>
                <option value="6">Zlib + Base16</option>
                <option value="7">Zlib + Base32</option>
                <option value="8">Zlib + Base64</option>
                <option value="9">Marshal + Zlib</option>
                <option value="10">Marshal + Base16</option>
                <option value="11">Marshal + Base32</option>
                <option value="12">Marshal + Base64</option>
                <option value="13">Marshal + Zlib + Base16</option>
                <option value="14">Marshal + Zlib + Base32</option>
                <option value="15">Marshal + Zlib + Base64</option>
                <option value="16">Simple Encode (5 Katman)</option>
            </select>
        </div>
        <div class="flex-row">
            <button type="submit" class="btn" style="flex:1;">⚡ Encode Et ve İndir</button>
            <a href="/reset" class="btn btn-secondary">Yeni Dosya</a>
        </div>
    </form>
    {% endif %}

    <div class="footer">
        <span style="color:#00ffb3;">❯</span> Bilgi paylaşıldıkça güçlenir, güvenlik bilinçle sağlanır.
        <br><br>
        <span style="font-size:0.7rem; color:#2a4a6a;">VEXORPVIP · 2026</span>
    </div>
</div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            flash('Dosya bulunamadı')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('Dosya seçilmedi')
            return redirect(url_for('index'))
        
        if not file.filename.endswith('.py'):
            flash('Sadece .py dosyaları kabul edilir')
            return redirect(url_for('index'))

        # Geçici dosya oluştur
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.py')
        tmp_path = tmp.name
        tmp.close()
        file.save(tmp_path)
        
        session['file_uploaded'] = True
        session['file_path'] = tmp_path
        session['filename'] = file.filename
        
        flash(f'{file.filename} başarıyla yüklendi!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Hata: {str(e)}')
        return redirect(url_for('index'))

@app.route('/encode', methods=['POST'])
def encode():
    try:
        if not session.get('file_uploaded'):
            flash('Önce dosya yükleyin')
            return redirect(url_for('index'))
        
        file_path = session.get('file_path')
        if not file_path or not os.path.exists(file_path):
            flash('Dosya bulunamadı, tekrar yükleyin')
            session.clear()
            return redirect(url_for('index'))

        option = int(request.form.get('option', 1))
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        encoded = encode_option(option, code)
        if encoded is None:
            flash('Geçersiz encode seçeneği')
            return redirect(url_for('index'))

        # Çıktı dosyasını geçici oluştur
        out = tempfile.NamedTemporaryFile(delete=False, suffix='_ENC.py')
        out_path = out.name
        out.close()
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(encoded)

        # Dosyayı gönder
        return send_file(
            out_path,
            as_attachment=True,
            download_name=f'encoded_{session.get("filename", "file")}',
            mimetype='text/x-python'
        )
    except Exception as e:
        flash(f'Encode hatası: {str(e)}')
        return redirect(url_for('index'))

@app.route('/reset')
def reset():
    try:
        # Geçici dosyaları temizle
        if session.get('file_path'):
            try:
                os.unlink(session['file_path'])
            except:
                pass
    except:
        pass
    session.clear()
    flash('Yeni dosya yükleyebilirsiniz', 'success')
    return redirect(url_for('index'))

# Vercel için
app.debug = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

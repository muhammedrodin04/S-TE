# -*- coding: utf-8 -*-
from flask import Flask, request, render_template_string, send_file, session, redirect, url_for
import os
import zlib
import base64
import marshal
import uuid
import time

app = Flask(__name__)
app.secret_key = 'VEXORPVIP_GIZLI_ANAHTAR'  # Değiştirilebilir

# ---------- ENCODE FONKSİYONLARI (orijinal bot'tan alındı) ----------
zlb = lambda in_: zlib.compress(in_)
b16 = lambda in_: base64.b16encode(in_)
b32 = lambda in_: base64.b32encode(in_)
b64 = lambda in_: base64.b64encode(in_)
mar = lambda in_: marshal.dumps(compile(in_, '<x>', 'exec'))
note = "# Güzeliğin kadar ömrüm olsa bir ömür yaşarım \n"

def encode_option(option, data):
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

# ---------- WEB ARAYÜZÜ ----------
# Ana sayfa: dosya yükleme formu
HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>VEXORPVİP ENCODE</title>
    <style>
        body { background: #0a0a0f; color: #d0d8f0; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
        .container { max-width: 800px; width: 100%; background: #0d0d1a; border-radius: 30px; padding: 30px; border: 1px solid #1e2d4a; box-shadow: 0 0 30px rgba(0,255,180,0.05); }
        h1 { color: #00ffb3; text-align: center; border-bottom: 2px solid #1f2f4a; padding-bottom: 15px; }
        .form-group { margin: 20px 0; }
        label { display: block; margin-bottom: 8px; color: #8cf0d0; }
        input[type="file"], select { width: 100%; padding: 12px; background: #0b1222; border: 1px solid #2a3a5c; border-radius: 10px; color: #d0d8f0; }
        button { background: #00ffb3; color: #0a0a0f; border: none; padding: 12px 30px; border-radius: 30px; font-weight: bold; cursor: pointer; transition: 0.3s; margin-top: 10px; }
        button:hover { background: #00cc99; transform: scale(1.02); }
        .footer { margin-top: 30px; text-align: center; color: #4a6a8a; font-size: 0.8rem; border-top: 1px solid #0f1f33; padding-top: 15px; }
        .badge { display: inline-block; background: #132233; padding: 5px 15px; border-radius: 30px; border: 1px solid #2a6a8a; font-size: 0.8rem; color: #8cf0d0; }
        .download-btn { background: #2a6a8a; color: white; }
    </style>
</head>
<body>
<div class="container">
    <h1>🔐 VEXORPVİP ENCODE</h1>
    <p style="text-align:center; color:#7a9ab0;">Python dosyalarınızı şifreleyin / encode edin</p>

    {% if not session.get('filename') %}
    <form action="/upload" method="post" enctype="multipart/form-data">
        <div class="form-group">
            <label>📂 Python dosyası seç (.py)</label>
            <input type="file" name="file" accept=".py" required>
        </div>
        <button type="submit">Dosyayı Yükle</button>
    </form>
    {% else %}
    <form action="/encode" method="post">
        <div class="form-group">
            <label>🔧 Encode yöntemi seç</label>
            <select name="option" style="width:100%; padding:12px; background:#0b1222; border:1px solid #2a3a5c; border-radius:10px; color:#d0d8f0;">
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
                <option value="16">Simple Encode (5 katmanlı)</option>
            </select>
        </div>
        <button type="submit">Encode Et ve İndir</button>
        <a href="/reset" style="display:inline-block; margin-left:20px; color:#ff6b6b;">Yeni dosya seç</a>
    </form>
    {% endif %}

    <div class="footer">
        <span class="badge">⚡ VEXORPVİP · 2026</span>
        <br><br>
        <i class="fas fa-skull" style="color:#00ffb3;"></i> Bilgi paylaşıldıkça güçlenir.
    </div>
</div>
</body>
</html>
"""

@app.route('/')
def index():
    # session'daki dosya adını temizle (eğer varsa)
    if 'filename' in session:
        # dosya var mı kontrol et, yoksa temizle
        if not os.path.exists(session['filename']):
            session.pop('filename', None)
    return render_template_string(HTML)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "Dosya yok", 400
    file = request.files['file']
    if file.filename == '':
        return "Dosya seçilmedi", 400
    if not file.filename.endswith('.py'):
        return "Sadece .py dosyaları kabul edilir", 400

    # Geçici dosya adı oluştur
    tmp_name = f"upload_{uuid.uuid4().hex}_{file.filename}"
    file.save(tmp_name)
    session['filename'] = tmp_name
    return redirect(url_for('index'))

@app.route('/encode', methods=['POST'])
def encode():
    if 'filename' not in session:
        return "Dosya yok", 400
    infile = session['filename']
    if not os.path.exists(infile):
        session.pop('filename', None)
        return "Dosya kayboldu, tekrar yükleyin", 400

    option = int(request.form.get('option', 1))
    with open(infile, 'r', encoding='utf-8') as f:
        code = f.read()

    encoded = encode_option(option, code)
    if encoded is None:
        return "Geçersiz seçenek", 400

    outfile = infile.replace('.py', '_ENC.py') if '.py' in infile else infile + '_ENC.py'
    with open(outfile, 'w', encoding='utf-8') as f:
        f.write(encoded)

    # Dosyayı gönder ve geçici dosyaları sil
    return send_file(outfile, as_attachment=True, download_name='encoded.py')

@app.route('/reset')
def reset():
    # Geçici dosyayı sil
    if 'filename' in session:
        try:
            os.remove(session['filename'])
        except:
            pass
        session.pop('filename', None)
    return redirect(url_for('index'))

# Vercel için uyumluluk
app.debug = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

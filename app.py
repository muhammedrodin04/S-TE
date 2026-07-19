from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VEXORPVIP HACKER · Dijital Güvenlik</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #0a0a0f;
            font-family: 'Segoe UI', 'Roboto', system-ui, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1.5rem;
            margin: 0;
        }

        .hacker-card {
            max-width: 900px;
            width: 100%;
            background: #0d0d1a;
            background-image: radial-gradient(circle at 30% 20%, #1a1a2e 0%, #07070e 90%);
            border-radius: 2.5rem;
            padding: 2.8rem 2.5rem;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.9), 0 0 0 1px #2a3a5c inset, 0 0 20px rgba(0, 255, 200, 0.05);
            border: 1px solid #1e2d4a;
            color: #d0d8f0;
            transition: 0.3s;
        }

        .hacker-card:hover {
            box-shadow: 0 40px 80px rgba(0, 0, 0, 0.95), 0 0 0 2px #3a6a8f inset;
            transform: translateY(-3px);
        }

        /* Header */
        .hacker-header {
            display: flex;
            align-items: center;
            gap: 1.2rem;
            border-bottom: 2px solid #1f2f4a;
            padding-bottom: 1.4rem;
            margin-bottom: 2.2rem;
            flex-wrap: wrap;
        }

        .hacker-logo {
            background: #0f1a2b;
            padding: 0.6rem 1.2rem;
            border-radius: 40px;
            font-size: 2rem;
            color: #8cf0d0;
            box-shadow: 0 0 0 1px #2a5a7a;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .hacker-logo i {
            font-size: 2.4rem;
            color: #00ffb3;
            filter: drop-shadow(0 0 8px #00ffb3);
        }

        .hacker-logo span {
            font-weight: 700;
            font-size: 1.2rem;
            letter-spacing: 1.5px;
            color: #b0e0d0;
        }

        .hacker-title {
            font-size: 1.9rem;
            font-weight: 700;
            background: linear-gradient(135deg, #00ffb3, #00aaff);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            letter-spacing: -0.5px;
        }

        .hacker-badge {
            margin-left: auto;
            background: #132233;
            padding: 0.4rem 1.2rem;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 600;
            color: #8cf0d0;
            border: 1px solid #2a6a8a;
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 5px #00ffb3; }
            50% { box-shadow: 0 0 20px #00ffb3; }
            100% { box-shadow: 0 0 5px #00ffb3; }
        }

        .hacker-badge i {
            color: #ff4444;
        }

        /* Ana mesaj */
        .glitch-box {
            background: #0b1222;
            padding: 2rem 2.2rem;
            border-radius: 2rem;
            margin-bottom: 2.5rem;
            border-left: 6px solid #00ffb3;
            border-right: 1px solid #1a3a5a;
            box-shadow: inset 0 0 30px rgba(0, 255, 180, 0.05);
            position: relative;
        }

        .glitch-box::before {
            content: ">";
            font-size: 3rem;
            position: absolute;
            top: -5px;
            left: 15px;
            color: #00ffb3;
            opacity: 0.3;
            font-family: 'Courier New', monospace;
        }

        .glitch-text {
            font-size: 1.6rem;
            font-weight: 500;
            line-height: 1.5;
            color: #e0f0ff;
            text-shadow: 0 2px 10px rgba(0, 255, 200, 0.1);
            position: relative;
            z-index: 2;
            padding-left: 0.5rem;
        }

        .glitch-text i {
            color: #00ffb3;
            margin-right: 10px;
        }

        .glitch-text .highlight {
            color: #00ffb3;
            font-weight: 700;
            text-shadow: 0 0 15px #00ffb3;
        }

        .glitch-author {
            display: block;
            margin-top: 1.2rem;
            text-align: right;
            font-weight: 300;
            font-size: 1rem;
            color: #7a9ab0;
            border-top: 1px dashed #1a3a5a;
            padding-top: 1rem;
            letter-spacing: 1px;
        }

        .glitch-author i {
            color: #00ffb3;
            margin-right: 6px;
        }

        /* Grid - Hacker Bilgileri */
        .hacker-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 1.2rem;
            margin: 2rem 0 1.5rem;
        }

        .hacker-item {
            background: #0b1424;
            border-radius: 1.5rem;
            padding: 1.3rem 1rem;
            border: 1px solid #1a2a4a;
            transition: 0.2s;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }

        .hacker-item:hover {
            border-color: #00ffb3;
            background: #101a2e;
            transform: scale(1.02);
        }

        .hacker-item h3 {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.1rem;
            color: #b0d8f0;
            margin-bottom: 0.6rem;
            border-bottom: 1px solid #1a2a4a;
            padding-bottom: 0.4rem;
        }

        .hacker-item h3 i {
            color: #00ffb3;
            width: 1.6rem;
            font-size: 1.3rem;
        }

        .hacker-item p {
            color: #a0b8d0;
            line-height: 1.5;
            font-size: 0.9rem;
        }

        .hacker-item .tag {
            background: #0f1f33;
            display: inline-block;
            padding: 0.2rem 0.8rem;
            border-radius: 40px;
            font-size: 0.7rem;
            font-weight: 600;
            color: #8cf0d0;
            margin-top: 0.6rem;
            border: 1px solid #1a4a6a;
        }

        .tag i {
            margin-right: 4px;
            color: #ff6b6b;
        }

        /* Bilgi kutusu */
        .info-box {
            background: #0a1222;
            border-radius: 1.5rem;
            padding: 1.2rem 1.8rem;
            border: 1px solid #1a2a4a;
            margin: 0.2rem 0 0.8rem;
        }

        .info-box p {
            display: flex;
            align-items: center;
            gap: 12px;
            color: #b0c8e0;
            font-size: 0.95rem;
            flex-wrap: wrap;
        }

        .info-box i {
            color: #00ffb3;
            font-size: 1.4rem;
        }

        .info-box strong {
            color: #ff6b6b;
        }

        /* Footer */
        .hacker-footer {
            margin-top: 2.5rem;
            padding-top: 1.6rem;
            border-top: 2px solid #1a2a4a;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            align-items: center;
            gap: 1rem;
        }

        .hacker-cmd {
            background: #070e1a;
            padding: 0.7rem 1.5rem;
            border-radius: 50px;
            font-family: 'Fira Code', 'Courier New', monospace;
            font-size: 0.85rem;
            color: #8cb0d0;
            border: 1px solid #1a3a5a;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.6);
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        .hacker-cmd i {
            color: #00ffb3;
        }

        .hacker-cmd .cmd-text {
            color: #d0e8ff;
            background: #0f1a2a;
            padding: 0.1rem 0.8rem;
            border-radius: 24px;
            font-weight: 500;
        }

        .hacker-version {
            color: #6a8aaa;
            font-size: 0.85rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .hacker-version i {
            color: #00ffb3;
        }

        .footer-note {
            margin-top: 1.2rem;
            font-size: 0.7rem;
            color: #4a6a8a;
            text-align: center;
            border-top: 1px solid #0f1f33;
            padding-top: 1rem;
            letter-spacing: 0.3px;
        }

        @media (max-width: 750px) {
            .hacker-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

        @media (max-width: 550px) {
            .hacker-card {
                padding: 1.8rem 1.2rem;
            }
            .hacker-title {
                font-size: 1.3rem;
            }
            .glitch-text {
                font-size: 1.2rem;
            }
            .hacker-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            .hacker-badge {
                margin-left: 0;
                width: 100%;
                justify-content: center;
                white-space: normal;
            }
            .hacker-header {
                flex-direction: column;
                align-items: flex-start;
            }
            .hacker-footer {
                flex-direction: column;
                align-items: stretch;
            }
            .hacker-cmd {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="hacker-card">
        <!-- Header -->
        <div class="hacker-header">
            <div class="hacker-logo">
                <i class="fas fa-skull"></i>
                <span>VEXORPVIP</span>
            </div>
            <div class="hacker-title">#HACKER · 2026</div>
            <div class="hacker-badge">
                <i class="fas fa-circle" style="color: #00ffb3;"></i>
                <span>LIVE · OFFLINE</span>
            </div>
        </div>

        <!-- Ana mesaj -->
        <div class="glitch-box">
            <div class="glitch-text">
                <i class="fas fa-terminal"></i> 
                <span class="highlight">VEXORPVIP</span> HACKER · Dijital Güvenlik & Siber Operasyonlar
            </div>
            <div class="glitch-author">
                <i class="fas fa-shield-halved"></i> 0x7F · "Bilgi güçtür, güvenlik zorunluluktur."
            </div>
        </div>

        <!-- Hacker Bilgileri -->
        <div class="hacker-grid">
            <div class="hacker-item">
                <h3><i class="fas fa-user-astronaut"></i> Kimlik</h3>
                <p><strong style="color: #00ffb3;">VEXORPVIP</strong> — Siber güvenlik uzmanı, <br>etik hacker & pentester.</p>
                <div class="tag"><i class="fas fa-check-circle" style="color: #00ffb3;"></i> OSCP · CEH</div>
            </div>
            <div class="hacker-item">
                <h3><i class="fas fa-code"></i> Uzmanlık</h3>
                <p>Web güvenliği, zafiyet analizi, <br>sızma testleri ve tersine mühendislik.</p>
                <div class="tag"><i class="fas fa-bug"></i> CVE · Exploit</div>
            </div>
            <div class="hacker-item">
                <h3><i class="fas fa-eye"></i> Vizyon</h3>
                <p>Dijital dünyada <span style="color: #00ffb3;">güvenlik açıklarını</span> kapatmak ve farkındalık yaratmak.</p>
                <div class="tag"><i class="fas fa-shield-halved"></i> #RedTeam</div>
            </div>
        </div>

        <!-- Bilgi kutusu -->
        <div class="info-box">
            <p>
                <i class="fas fa-exclamation-triangle"></i>
                <span><strong>⚠️ ÖNEMLİ:</strong> VEXORPVIP, yalnızca <span style="color: #00ffb3;">etik hacking</span> ve <span style="color: #00ffb3;">siber güvenlik</span> eğitimleri için bilgi paylaşır. Tüm faaliyetler yasal çerçevede gerçekleşir.</span>
            </p>
        </div>

        <!-- Footer -->
        <div class="hacker-footer">
            <div class="hacker-cmd">
                <i class="fas fa-terminal"></i>
                <span>root@vexor:~$</span>
                <span class="cmd-text">./hack --ethical</span>
                <i class="fas fa-circle" style="color: #00ffb3; font-size: 0.5rem; margin-left: 6px;"></i>
            </div>
            <div class="hacker-version">
                <i class="fas fa-code-branch"></i> 
                <span>v·2.1.7 · "CyberShield"</span>
                <i class="fas fa-shield-halved" style="margin-left: 10px; color: #00ffb3;"></i>
            </div>
        </div>

        <div class="footer-note">
            <i class="fas fa-skull" style="margin-right: 5px; color: #00ffb3;"></i> 
            VEXORPVIP · HACKER · “Bilgi paylaşıldıkça güçlenir, güvenlik bilinçle sağlanır.”
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/hacker')
def hacker():
    return render_template_string(HTML_TEMPLATE)

@app.route('/vexor')
def vexor():
    return render_template_string(HTML_TEMPLATE)

# Vercel için
app.debug = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📌 Ortam Sanal, Suç Gerçek | Flask Sözü</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #1a1e2c;
            font-family: 'Segoe UI', 'Roboto', system-ui, sans-serif;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1.5rem;
            margin: 0;
        }

        .flask-card {
            max-width: 820px;
            width: 100%;
            background: #0b0d17;
            background-image: radial-gradient(circle at 10% 20%, #1f253b 0%, #0a0c14 90%);
            border-radius: 2.5rem;
            padding: 2.8rem 2.5rem;
            box-shadow: 0 30px 50px rgba(0, 0, 0, 0.8), 0 0 0 1px #3d445e inset, 0 0 0 2px #1f253b inset;
            transition: transform 0.2s ease, box-shadow 0.3s;
            color: #eceff4;
            border: 1px solid #2e354a;
        }

        .flask-card:hover {
            box-shadow: 0 40px 70px rgba(0, 0, 0, 0.9), 0 0 0 2px #5b6a8f inset;
            transform: translateY(-4px);
        }

        .flask-header {
            display: flex;
            align-items: center;
            gap: 0.9rem;
            border-bottom: 2px solid #3e4660;
            padding-bottom: 1.4rem;
            margin-bottom: 2.2rem;
            flex-wrap: wrap;
        }

        .flask-icon {
            background: #1f2937;
            padding: 0.6rem 1rem;
            border-radius: 40px;
            font-size: 2.1rem;
            color: #b7c7e8;
            box-shadow: 0 0 0 1px #4d5a7a;
            line-height: 1;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
        }

        .flask-icon i {
            font-size: 2.2rem;
            color: #d4e0ff;
            filter: drop-shadow(0 0 6px #6d8cd6);
        }

        .flask-icon span {
            font-weight: 600;
            font-size: 1.3rem;
            letter-spacing: 0.5px;
            color: #b7c7e8;
        }

        .flask-title {
            font-size: 2.1rem;
            font-weight: 700;
            background: linear-gradient(135deg, #d6e2ff, #9bb0e6);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            letter-spacing: -0.3px;
            word-break: break-word;
        }

        .flask-sub {
            margin-left: auto;
            background: #262e44;
            padding: 0.5rem 1.2rem;
            border-radius: 30px;
            font-size: 0.9rem;
            font-weight: 500;
            color: #b7c9f0;
            border: 1px solid #49547a;
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }

        .flask-sub i {
            color: #f1c40f;
        }

        .quote-box {
            background: #141a29;
            padding: 2rem 2.2rem;
            border-radius: 2rem;
            margin-bottom: 2.5rem;
            border-left: 6px solid #e67e22;
            border-right: 1px solid #2f3853;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
            position: relative;
        }

        .quote-box::before {
            content: "“";
            font-size: 4.5rem;
            position: absolute;
            top: -10px;
            left: 10px;
            color: #e67e22;
            opacity: 0.25;
            font-family: serif;
        }

        .quote-text {
            font-size: 1.7rem;
            font-weight: 500;
            line-height: 1.4;
            color: #f0f4ff;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
            position: relative;
            z-index: 2;
            padding-left: 0.5rem;
        }

        .quote-text i {
            color: #f1c40f;
            margin-right: 10px;
        }

        .quote-author {
            display: block;
            margin-top: 1.2rem;
            text-align: right;
            font-weight: 300;
            font-size: 1.1rem;
            color: #a3b5dd;
            border-top: 1px dashed #3d486a;
            padding-top: 1rem;
            letter-spacing: 1px;
        }

        .quote-author i {
            color: #e67e22;
            margin-right: 6px;
        }

        .grid-panel {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin: 2rem 0 1.5rem;
        }

        .feature-item {
            background: #121824;
            border-radius: 1.5rem;
            padding: 1.5rem 1.2rem;
            border: 1px solid #2e3852;
            transition: 0.2s;
            box-shadow: 0 5px 12px rgba(0, 0, 0, 0.3);
        }

        .feature-item:hover {
            border-color: #e67e22;
            background: #181f31;
            transform: scale(1.01);
        }

        .feature-item h3 {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.25rem;
            color: #d3defa;
            margin-bottom: 0.75rem;
            border-bottom: 1px solid #2f3b58;
            padding-bottom: 0.5rem;
        }

        .feature-item h3 i {
            color: #f39c12;
            width: 1.8rem;
            font-size: 1.5rem;
        }

        .feature-item p {
            color: #bcc9ed;
            line-height: 1.5;
            font-size: 0.98rem;
            margin-top: 0.3rem;
        }

        .feature-item .badge {
            background: #2a334e;
            display: inline-block;
            padding: 0.2rem 0.9rem;
            border-radius: 40px;
            font-size: 0.75rem;
            font-weight: 600;
            color: #e6edff;
            margin-top: 0.8rem;
            border: 1px solid #4b5a7e;
        }

        .badge i {
            margin-right: 4px;
            color: #f1c40f;
        }

        .flask-footer {
            margin-top: 2.5rem;
            padding-top: 1.6rem;
            border-top: 2px solid #2c344b;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            align-items: center;
            gap: 1rem;
        }

        .flask-cmd {
            background: #0c101c;
            padding: 0.75rem 1.5rem;
            border-radius: 50px;
            font-family: 'Fira Code', 'Courier New', monospace;
            font-size: 0.9rem;
            color: #a7bde0;
            border: 1px solid #39445f;
            box-shadow: inset 0 2px 6px rgba(0,0,0,0.6);
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        .flask-cmd i {
            color: #2ecc71;
        }

        .flask-cmd .cmd-text {
            color: #d8e2ff;
            background: #1f263b;
            padding: 0.1rem 0.8rem;
            border-radius: 24px;
            font-weight: 500;
        }

        .flask-version {
            color: #8892b0;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .flask-version i {
            color: #e67e22;
        }

        @media (max-width: 650px) {
            .flask-card {
                padding: 1.8rem 1.2rem;
            }
            .flask-title {
                font-size: 1.5rem;
            }
            .quote-text {
                font-size: 1.3rem;
            }
            .grid-panel {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            .flask-sub {
                margin-left: 0;
                width: 100%;
                justify-content: center;
                white-space: normal;
            }
            .flask-header {
                flex-direction: column;
                align-items: flex-start;
            }
            .flask-footer {
                flex-direction: column;
                align-items: stretch;
            }
            .flask-cmd {
                justify-content: center;
            }
        }

        @media (max-width: 420px) {
            .flask-icon {
                font-size: 1.5rem;
                padding: 0.3rem 0.7rem;
            }
            .quote-text {
                font-size: 1.1rem;
            }
        }
    </style>
</head>
<body>
    <div class="flask-card">
        <div class="flask-header">
            <div class="flask-icon">
                <i class="fas fa-flask"></i>
                <span>Flask</span>
            </div>
            <div class="flask-title">#SanalGerçeklik</div>
            <div class="flask-sub">
                <i class="fas fa-shield-alt"></i> 
                <span>cyber·law</span>
            </div>
        </div>

        <div class="quote-box">
            <div class="quote-text">
                <i class="fas fa-quote-left"></i> 
                Ortam sanal olsa da işlenen suçlar. <br><span style="font-weight:700; color:#f7d44a;">Her zaman gerçektir.</span>
            </div>
            <div class="quote-author">
                <i class="fas fa-gavel"></i> Flask·site · 2026
            </div>
        </div>

        <div class="grid-panel">
            <div class="feature-item">
                <h3><i class="fas fa-user-secret"></i> Dijital Suç</h3>
                <p>Siber zorbalık, dolandırıcılık, kimlik hırsızlığı, yasa dışı erişim… 
                <span style="color:#f1c40f;">Sanal</span> ortamda işlenen her eylem, 
                gerçek dünyada <strong>karşılığı olan</strong> bir suçtur.</p>
                <div class="badge"><i class="fas fa-exclamation-triangle"></i> TCK · 243-245</div>
            </div>
            <div class="feature-item">
                <h3><i class="fas fa-database"></i> Delil · İz</h3>
                <p>Her dijital ayak izi, her log kaydı, her mesaj <strong>gerçek delil</strong> olarak 
                kabul edilir. Flask ile oluşturulan bu sitede bile <i class="fas fa-fingerprint" style="color:#f39c12;"></i> 
                izler mevcuttur.</p>
                <div class="badge"><i class="fas fa-check-circle" style="color:#2ecc71;"></i> Adli bilişim</div>
            </div>
        </div>

        <div style="background: #0f1422; border-radius: 1.5rem; padding: 1.2rem 1.8rem; border: 1px solid #38415f; margin: 0.2rem 0 0.8rem;">
            <p style="display: flex; align-items: center; gap: 12px; color: #d0defa; font-size: 1rem; flex-wrap: wrap;">
                <i class="fas fa-balance-scale" style="color: #e67e22; font-size: 1.6rem;"></i>
                <span><strong>Hatırlatma:</strong> Sanal ortamda işlenen suçlar, mağduriyet, itibar kaybı, maddi zarar ve psikolojik etkiler doğurur. 
                <span style="color: #f7d44a;">Yargı kararları</span> dijital suçları aynen cezalandırır.</span>
            </p>
        </div>

        <div class="flask-footer">
            <div class="flask-cmd">
                <i class="fas fa-terminal"></i>
                <span>flask@site:~$</span>
                <span class="cmd-text">./suc-gercek --sanal</span>
                <i class="fas fa-circle" style="color: #2ecc71; font-size: 0.5rem; margin-left: 6px;"></i>
            </div>
            <div class="flask-version">
                <i class="fas fa-code-branch"></i> 
                <span>v·3.1.4 · "Adalet"</span>
                <i class="fas fa-shield-halved" style="margin-left: 10px; color: #f1c40f;"></i>
            </div>
        </div>

        <div style="margin-top: 1.2rem; font-size: 0.75rem; color: #5d6b8a; text-align: center; border-top: 1px solid #222b3f; padding-top: 1rem; letter-spacing: 0.3px;">
            <i class="fas fa-flask" style="margin-right: 5px;"></i> 
            Flask ile kurulmuştur · “Ortam sanal olsa da işlenen suçlar her zaman gerçektir.”
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/suc')
def suc():
    return render_template_string(HTML_TEMPLATE)

@app.route('/gercek')
def gercek():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

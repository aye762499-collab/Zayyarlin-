from flask import Flask, render_template_string, request, session, redirect, url_for
import os, requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'zayyarlin_tt_pro_v2')

# --- ဇေယျာလင်း အတွက် စိတ်ကြိုက်ပြင်ဆင်ရန် ---
MY_TIKTOK_URL = "https://www.tiktok.com/@zayyarlin" # မင်းရဲ့ Acc link ထည့်ပါ

# ဘာသာစကား ဒေတာများ
LANGUAGES = {
    'my': {'title': 'TikTok Downloader', 'placeholder': 'လင့်ခ်ကို ဤနေရာတွင် ထည့်ပါ', 'btn': 'ဗီဒီယိုရယူမည်', 'how': 'အသုံးပြုနည်း', 'safety': 'လုံခြုံမှုရှိပါသည်', 'about': 'Tool အကြောင်း'},
    'en': {'title': 'TikTok Downloader', 'placeholder': 'Insert link here', 'btn': 'Get Video', 'how': 'How to use', 'safety': 'Secure & Safe', 'about': 'About Tool'},
    'th': {'title': 'ดาวน์โหลด TikTok', 'placeholder': 'วางลิงก์ที่นี่', 'btn': 'รับวิดีโอ', 'how': 'วิธีใช้', 'safety': 'ปลอดภัย', 'about': 'เกี่ยวกับ'},
    'jp': {'title': 'TikTok 保存', 'placeholder': 'リンクを挿入', 'btn': '保存', 'how': '使い方', 'safety': '安全', 'about': 'について'},
    'cn': {'title': 'TikTok 下载器', 'placeholder': '在此处插入链接', 'btn': '下载', 'how': '如何使用', 'safety': '安全', 'about': '关于'}
}

STYLE = """
<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'>
<style>
    :root { --pink: #FF0050; --cyan: #00F2EA; }
    body.dark-mode { background: #010101; color: #fff; }
    body.light-mode { background: #f8f9fa; color: #333; }
    
    .glass-card { 
        background: rgba(255,255,255,0.05); backdrop-filter: blur(15px); 
        border: 1px solid rgba(255,255,255,0.1); border-radius: 25px; padding: 25px; 
    }
    .light-mode .glass-card { background: #fff; border: 1px solid #ddd; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }

    .nav-bottom { 
        position: fixed; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.9); 
        display: flex; justify-content: space-around; padding: 12px 0; border-top: 1px solid #333; 
    }
    .light-mode .nav-bottom { background: #fff; border-top: 1px solid #ddd; }
    .nav-btn { color: #888; text-decoration: none; text-align: center; font-size: 0.7rem; }
    .nav-btn.active { color: var(--cyan); }

    .btn-main { background: linear-gradient(45deg, var(--pink), var(--cyan)); color: #fff; border: none; border-radius: 50px; font-weight: bold; }
    .step-box { background: rgba(0,242,234,0.1); border-radius: 15px; padding: 15px; margin-bottom: 10px; border-left: 5px solid var(--cyan); }
</style>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    mode = session.get('mode', 'dark-mode')
    lang = session.get('lang', 'my')
    t = LANGUAGES[lang]
    video_url = None
    
    if request.method == "POST":
        tt_url = request.form.get("tiktok_url")
        if tt_url:
            api = f"https://api.tiklydown.eu.org/api/download?url={tt_url}"
            try:
                res = requests.get(api).json()
                video_url = res.get("video", {}).get("noWatermark")
            except: pass

    return render_template_string(f"""
    <html><head>{STYLE}</head><body class='{mode}'>
        <div class='container p-4 text-center'>
            <h2 class='fw-bold mb-4'><i class='fab fa-tiktok text-danger'></i> {t['title']}</h2>
            <div class='glass-card'>
                <form method='POST'>
                    <input type='text' name='tiktok_url' placeholder='{t['placeholder']}' class='form-control rounded-pill mb-3 py-3 border-0 bg-secondary bg-opacity-10 text-white'>
                    <button class='btn btn-main w-100 py-3'>{t['btn']}</button>
                </form>
                {% if video_url %}
                    <a href='{{{{video_url}}}}' target='_blank' class='btn btn-success rounded-pill mt-3 w-100'>Download Now</a>
                {% endif %}
            </div>
            
            <div class='mt-5 text-start'>
                <h5 class='fw-bold'><i class='fas fa-info-circle text-info'></i> {t['how']}</h5>
                <div class='step-box'>1. Open TikTok & Copy Video Link</div>
                <div class='step-box'>2. Paste link in the box above</div>
                <div class='step-box'>3. Click Download button</div>
            </div>
        </div>

        <div class='nav-bottom'>
            <a href='/' class='nav-btn active'><i class='fas fa-home d-block fa-lg'></i>Home</a>
            <a href='{MY_TIKTOK_URL}' class='nav-btn'><i class='fab fa-tiktok d-block fa-lg'></i>TikTok</a>
            <a href='/settings' class='nav-btn'><i class='fas fa-cog d-block fa-lg'></i>Settings</a>
        </div>
    </body></html>""", video_url=video_url)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        if 'lang' in request.form: session['lang'] = request.form.get('lang')
        if 'mode' in request.form: session['mode'] = request.form.get('mode')
        return redirect(url_for('settings'))
    
    mode = session.get('mode', 'dark-mode')
    return render_template_string(f"""
    <html><head>{STYLE}</head><body class='{mode}'>
        <div class='container p-4'>
            <h4 class='fw-bold mb-4'><i class='fas fa-cog'></i> Settings</h4>
            <div class='glass-card mb-4'>
                <h6>Language (ဘာသာစကား)</h6>
                <form method='POST' class='d-flex flex-wrap gap-2 mt-3'>
                    <button name='lang' value='my' class='btn btn-sm btn-outline-info'>Myanmar</button>
                    <button name='lang' value='en' class='btn btn-sm btn-outline-info'>English</button>
                    <button name='lang' value='th' class='btn btn-sm btn-outline-info'>Thai</button>
                    <button name='lang' value='jp' class='btn btn-sm btn-outline-info'>Japan</button>
                    <button name='lang' value='cn' class='btn btn-sm btn-outline-info'>China</button>
                </form>
            </div>
            <div class='glass-card mb-4'>
                <h6>Display Mode</h6>
                <form method='POST' class='mt-3'>
                    <button name='mode' value='light-mode' class='btn btn-light rounded-pill'>Light Mode</button>
                    <button name='mode' value='dark-mode' class='btn btn-dark rounded-pill border'>Dark Mode</button>
                </form>
            </div>
            <div class='text-center text-secondary small'>
                <p>Created by Zay Yar Lin</p>
                <i class='fas fa-shield-alt'></i> This tool is 100% safe and secure.
            </div>
        </div>
        <div class='nav-bottom'>
            <a href='/' class='nav-btn'><i class='fas fa-home d-block fa-lg'></i>Home</a>
            <a href='{MY_TIKTOK_URL}' class='nav-btn'><i class='fab fa-tiktok d-block fa-lg'></i>TikTok</a>
            <a href='/settings' class='nav-btn active'><i class='fas fa-cog d-block fa-lg'></i>Settings</a>
        </div>
    </body></html>""")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  

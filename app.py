import os
import telebot
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# إعدادات بوت تلغرام
TELEGRAM_API_TOKEN = '6822625757:AAFuBb7icwxuFpKjqFTWwlKb5poUSUfWTNo'
CHAT_ID = '5152526784'  # يمكنك الحصول عليه باستخدام بوت @userinfobot أو عبر API

# إنشاء كائن بوت باستخدام مكتبة telebot
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# تحديد المجلد لحفظ الملفات المرفوعة
UPLOAD_FOLDER = '/tmp/uploads'  # مجلد مؤقت على الخادم في Vercel
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# إعداد تطبيق Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def send_file_to_telegram(file_path):
    """دالة لإرسال الملف إلى بوت تلغرام باستخدام مكتبة telebot"""
    try:
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id=CHAT_ID, document=file)
            return f"تم إرسال الملف {file_path} إلى تلغرام."
    except Exception as e:
        return f"حدث خطأ أثناء إرسال الملف: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    """الصفحة الرئيسية لرفع الملفات وإرسالها إلى بوت تلغرام"""
    if request.method == 'POST':
        # الحصول على الملف المرفوع من النموذج
        file = request.files['file']
        if file:
            # تأكيد حفظ الملف في المجلد المؤقت
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # إرسال الملف إلى بوت تلغرام
            message = send_file_to_telegram(file_path)
            return render_template('index.html', message=message)

    return render_template('index.html', message=None)

if __name__ == '__main__':
    app.run(debug=True)

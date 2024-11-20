import os
import requests
from flask import Flask, render_template

# إعدادات بوت تلغرام
TELEGRAM_API_TOKEN = '6822625757:AAFuBb7icwxuFpKjqFTWwlKb5poUSUfWTNo'
CHAT_ID = '5152526784'  # يمكنك الحصول عليه باستخدام بوت @userinfobot أو عبر API

# المسار الذي يحتوي على الملفات
FILE_DIRECTORY = 'C:\\Users\\os\\Desktop\\SS'  # حدد المسار هنا

app = Flask(__name__)

def send_file_to_telegram(file_path):
    """دالة لإرسال الملف إلى بوت تلغرام باستخدام مكتبة requests"""
    try:
        # فتح الملف
        with open(file_path, 'rb') as file:
            # إعداد البيانات التي سيتم إرسالها عبر API
            url = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendDocument'
            files = {'document': file}
            data = {'chat_id': CHAT_ID}
            
            # إرسال الطلب إلى API
            response = requests.post(url, data=data, files=files)
            
            if response.status_code == 200:
                return f"تم إرسال الملف {file_path} إلى تلغرام."
            else:
                return f"حدث خطأ أثناء إرسال الملف: {response.text}"
    except Exception as e:
        return f"حدث خطأ أثناء فتح الملف: {e}"

@app.route('/', methods=['GET'])
def index():
    """الرابط الرئيسي للموقع الذي سيقوم بسحب الملفات وإرسالها للبوت"""
    try:
        # التأكد من وجود المسار والتحقق من الملفات فيه
        if os.path.exists(FILE_DIRECTORY) and os.path.isdir(FILE_DIRECTORY):
            files = os.listdir(FILE_DIRECTORY)
            if files:
                messages = []
                for file in files:
                    file_path = os.path.join(FILE_DIRECTORY, file)
                    
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

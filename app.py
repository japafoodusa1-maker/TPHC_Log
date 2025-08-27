from flask import Flask, render_template, request, redirect
from datetime import datetime
import pytz   # ← 追加

app = Flask(__name__)

# カリフォルニア（ロサンゼルス）のタイムゾーンを指定
tz = pytz.timezone('America/Los_Angeles')

logs = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        temperature = request.form['temperature']
        person = request.form['person']
        action = request.form['action']

        # カリフォルニア時間で現在時刻を取得
        now = datetime.now(tz)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        logs.append({
            'timestamp': timestamp,
            'temperature': temperature,
            'person': person,
            'action': action
        })
        return redirect('/')
    return render_template('index.html', logs=logs)

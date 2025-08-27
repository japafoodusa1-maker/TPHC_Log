from flask import Flask, render_template, request, redirect
from datetime import datetime
import pytz

app = Flask(__name__)

# カリフォルニア（ロサンゼルス）のタイムゾーン
tz = pytz.timezone('America/Los_Angeles')

# データ保存用（本来はDBを使うべきですが、ここでは簡易的にリスト）
logs = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        temperature = request.form['temperature']
        person = request.form['person']
        action = request.form['action']  # 受け取り or 出荷
        
        # カリフォルニア時間で記録
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

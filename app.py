from flask import Flask, render_template, request, redirect
from datetime import datetime
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

# カリフォルニア時間
tz = pytz.timezone('America/Los_Angeles')

# Google Sheets 接続
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Render環境変数からcredentialsを読み込む
credentials_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS")
credentials_dict = json.loads(credentials_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)

# シートを指定
SHEET_ID = os.environ.get("SHEET_ID")
sheet = client.open_by_key(SHEET_ID).sheet1

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        temperature = request.form['temperature']
        person = request.form['person']
        action = request.form['action']

        now = datetime.now(tz)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # Google Sheetsに追記
        sheet.append_row([timestamp, temperature, person, action])

        return redirect('/')
    return render_template('index.html')

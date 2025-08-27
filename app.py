from flask import Flask, render_template_string, request, redirect
import csv
from datetime import datetime

app = Flask(__name__)

FILENAME = "TPHC_log.csv"

# 初期化（ヘッダー付与）
def initialize_csv():
    try:
        with open(FILENAME, mode="x", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Timestamp", "Person", "Temperature (F)"])
    except FileExistsError:
        pass

initialize_csv()

# HTMLテンプレート
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>TPHC Logging</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; margin: 20px; }
        .container { max-width: 400px; margin: auto; }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input, select, button { width: 100%; padding: 10px; margin-top: 5px; }
        button { background: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background: #45a049; }
    </style>
</head>
<body>
    <div class="container">
        <h2>TPHC Temperature Control</h2>
        <form method="post">
            <label>記録タイプ</label>
            <select name="event_type" required>
                <option value="発送">発送</option>
                <option value="入荷">入荷</option>
            </select>
            
            <label>担当者名</label>
            <input type="text" name="person" required>
            
            <label>温度 (°F)</label>
            <input type="number" step="0.1" name="temperature" required>
            
            <button type="submit">記録</button>
        </form>
        <br>
        <a href="/logs">📑 記録を見る</a>
    </div>
</body>
</html>
"""

# ログページ
LOGS_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>TPHC Logs</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; margin: 20px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; }
        th { background: #f2f2f2; }
    </style>
</head>
<body>
    <h2>📑 TPHC Logs</h2>
    <table>
        <tr><th>Type</th><th>Timestamp</th><th>Person</th><th>Temp (°F)</th></tr>
        {% for row in logs %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] }}</td>
        </tr>
        {% endfor %}
    </table>
    <br>
    <a href="/">⬅️ 戻る</a>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        event_type = request.form["event_type"]
        person = request.form["person"]
        temperature = request.form["temperature"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(FILENAME, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([event_type, timestamp, person, temperature])
        
        return redirect("/logs")
    return render_template_string(HTML)

@app.route("/logs")
def logs():
    with open(FILENAME, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        logs = list(reader)
    return render_template_string(LOGS_HTML, logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

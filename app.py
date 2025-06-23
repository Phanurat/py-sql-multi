from flask import Flask, request, jsonify
import sqlite3
import os
import threading
from flask import send_from_directory

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_files = {}

# ✅ Load DBs จากหลายโฟลเดอร์
def scan_dbs():
    for folder in os.listdir(BASE_DIR):
        path = os.path.join(BASE_DIR, folder, "fb_comment_system.db")
        if os.path.isfile(path):
            db_files[folder] = path

@app.route('/')
def index():
    return send_from_directory('.','index.html')

@app.route('/api/projects')
def list_projects():
    return jsonify(list(db_files.keys()))

@app.route('/api/data/<project>')
def get_project_data(project):
    db_path = db_files.get(project)
    if not db_path: return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()

    result = {}
    for tname, in tables:
        try:
            cur.execute(f"SELECT * FROM {tname}")
            cols = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            result[tname] = {"columns": cols, "rows": rows}
        except: pass

    conn.close()
    return jsonify(result)

@app.route('/api/update/<project>/<table>', methods=['POST'])
def update_table(project, table):
    db_path = db_files.get(project)
    if not db_path: return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    data = request.json
    threading.Thread(target=save_data, args=(db_path, table, data)).start()
    return jsonify({"status": "updating in background"})

def save_data(db_path, table, data):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute(f"DELETE FROM {table}")
        cols = data["columns"]
        for row in data["rows"]:
            placeholders = ",".join(["?"] * len(cols))
            cur.execute(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders})", row)

        conn.commit()
        conn.close()
        print(f"[✓] อัปเดต {table} ใน {db_path}")
    except Exception as e:
        print(f"[X] Error:", e)

if __name__ == '__main__':
    scan_dbs()
    app.run(debug=True)

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

# Group ID table
@app.route('/group_id')
def group_id():
    return send_from_directory('.','group_id.html')
# Group ID API
@app.route('/like-and-comment')
def like_and_comment():
    return send_from_directory('.','like_and_comment.html')
#=================================
# like-comment-reply
@app.route('/like-comment-reply')
def like_comment_reply():
    return send_from_directory('.','like_comment_reply.html')
#=================================
# like-comment-only
@app.route('/like-comment-only')
def like_comment_reply_only():
    return send_from_directory('.','like_comment_only.html')
#=================================
# like-only
@app.route('/like-only')
def like_only():
    return send_from_directory('.','like_only.html')
#=================================
# like-reel-comment
@app.route('/like-reel-comment')
def like_reel_comment():
    return send_from_directory('.','like_reel_comment.html')
#=================================
# like-reel-only
@app.route('/like-reel-only')
def like_reel_only():
    return send_from_directory('.','like_reel_only.html')
#=================================

# pic-cation-text
@app.route('/pic-cation-text')
def pic_cation_text():
    return send_from_directory('.','pic_cation_text.html')
#=================================
# pic-status
@app.route('/pic-status')
def pic_status():
    return send_from_directory('.','pic_status.html')
#=================================
# set-status-text
@app.route('/set-status-text')
def set_status_text():
    return send_from_directory('.','set_status_text.html')
#=================================
# share-link
@app.route('/share-link')
def share_link():
    return send_from_directory('.','share_link.html')
#=================================
# share-link-text
@app.route('/share-link-text')
def share_link_text():
    return send_from_directory('.','share_link_text.html')
#=================================
#subscribe-id
@app.route('/subscribe-id')
def subscribe_id():
    return send_from_directory('.','subscribe_id.html')
#=================================
#unsubscribe-id
@app.route('/unsubscribe-id')
def unsubscribe_id():
    return send_from_directory('.','unsubscribe_id.html')
#=================================

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
    threading.Thread(target=save_data_app_profile, args=(db_path, table, data)).start()
    return jsonify({"status": "updating in background"})

#test for api
@app.route('/api/update/<project>/<table>?media_id=<meta_id>', methods=['POST'])
def update_api_media(project, table, meta_id):
    db_path = db_files.get(project)
    if not db_path: return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    data = request.json
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(f"DELETE FROM {table} WHERE media_id = ?", (meta_id,))
    cols = data["columns"]
    for row in data["rows"]:
        placeholders = ",".join(["?"] * len(cols))
        cur.execute(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders})", row)

    conn.commit()
    conn.close()
    return jsonify({"status": "updating in background"})

def save_data_app_profile(db_path, table, data):
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

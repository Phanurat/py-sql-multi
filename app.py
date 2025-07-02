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

@app.route('/bio-intro')
def bio_intro():
    return send_from_directory('.','bio_intro.html')

@app.route('/change-city')
def change_city():
    return send_from_directory('.','change_city.html')

@app.route('/change-name')
def change_name():
    return send_from_directory('.', 'change_name.html')

@app.route('/switch-bio')
def switch_bio():
    return send_from_directory('.', 'switch_bio.html')

@app.route('/switch-lock')
def switch_lock():
    return send_from_directory('.', 'switch_lock.html')

@app.route('/switch-unlock')
def switch_unlock():
    return send_from_directory('.', 'switch_unlock.html')


#=================================

@app.route('/api/data/<project>/<table>')
def get_table_data(project, table):
    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        cols = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        conn.close()
        return jsonify({"columns": cols, "rows": rows})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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

@app.route('/api/insert/<project>/change-bio', methods=['POST'])
def post_change_bio(project):
    db_path = db_files.get(project)
    bio_intro = request.args.get("bio_intro") or (request.json.get("bio_intro") if request.is_json else None)

    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404
    if not bio_intro:
        return jsonify({"error": "กรุณาระบุ bio_intro"}), 400

    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM change_bio_table")
            cur.execute("INSERT INTO change_bio_table (bio_intro) VALUES (?)", (bio_intro,))
            conn.commit()

        print(f"[✓] POST {project}: {bio_intro}")
        return jsonify({"status": "ok", "project": project, "bio_intro": bio_intro})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/get/<project>/change-bio', methods=['GET'])
def get_change_bio(project):
    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT bio_intro FROM change_bio_table LIMIT 1")
        row = cur.fetchone()
        conn.close()

        return jsonify({"bio_intro": row[0] if row else None})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/insert/<project>/change-city', methods=['POST'])
def post_change_city(project):
    db_path = db_files.get(project)
    city_id = request.args.get("city_id") or (request.json.get("city_id") if request.is_json else None)

    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404
    if not city_id:
        return jsonify({"error": "กรุณาระบุ city_id"}), 400

    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()

            # ✅ เช็กว่ามีตาราง change_city_table ก่อน
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='change_city_table'")
            exists = cur.fetchone()
            if not exists:
                print(f"[X] ข้าม {project} เพราะไม่มี change_city_table")
                return jsonify({"error": f"{project} ไม่มี change_city_table"}), 400

            cur.execute("DELETE FROM change_city_table")
            cur.execute("INSERT INTO change_city_table (city_id) VALUES (?)", (city_id,))
            conn.commit()

        print(f"[✓] POST {project}: {city_id}")
        return jsonify({"status": "ok", "project": project, "city_id": city_id})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/api/get/<project>/change-city', methods=['GET'])
def get_change_city(project):
    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # ✅ เช็กตารางก่อน SELECT
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='change_city_table'")
        exists = cur.fetchone()
        if not exists:
            return jsonify({"city_id": None})  # ไม่มีก็ส่ง null ไปเลย

        cur.execute("SELECT city_id FROM change_city_table LIMIT 1")
        row = cur.fetchone()
        conn.close()

        return jsonify({"city_id": row[0] if row else None})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

# ฟังก์ชันช่วย: อัปเดตค่าในตาราง switch ใดๆ
def update_switch_table(db_path, table_name, column_name, value):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table_name}")
        cur.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (?)", (value,))
        conn.commit()


# ✅ Update Switch
@app.route('/api/update/<project>/<switch_table>', methods=['POST'])
def update_switch(project, switch_table):
    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    value = request.args.get("value") or (request.json.get("value") if request.is_json else None)
    if not value:
        return jsonify({"error": "กรุณาระบุ value"}), 400

    try:
        # ตรวจสอบ column ที่ใช้
        column_map = {
            "switch_for_bio_profile_table": "status",
            "switch_for_lock_profile_table": "status_id",
            "switch_for_unlock_profile_table": "status_id"
        }

        if switch_table not in column_map:
            return jsonify({"error": "ตารางไม่รองรับ"}), 400

        column_name = column_map[switch_table]
        update_switch_table(db_path, switch_table, column_name, value)
        print(f"[✓] Updated {switch_table} in {project} → {column_name} = {value}")
        return jsonify({"status": "ok", "table": switch_table, "value": value})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500


# ✅ Get Switch Value
@app.route('/api/get/<project>/<switch_table>', methods=['GET'])
def get_switch(project, switch_table):
    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        column_map = {
            "switch_for_bio_profile_table": "status",
            "switch_for_lock_profile_table": "status_id",
            "switch_for_unlock_profile_table": "status_id"
        }

        if switch_table not in column_map:
            return jsonify({"error": "ตารางไม่รองรับ"}), 400

        column_name = column_map[switch_table]

        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT {column_name} FROM {switch_table} LIMIT 1")
            row = cur.fetchone()

        return jsonify({column_name: row[0] if row else None})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    scan_dbs()
    app.run(debug=True, port=5050)

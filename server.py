from flask import Flask, request, jsonify
import sqlite3
import os
import threading
from flask import send_from_directory

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_files = {}

def scan_dbs():
    for folder in os.listdir(BASE_DIR):
        path = os.path.join(BASE_DIR, folder, "fb_comment_system.db")
        if os.path.isfile(path):
            db_files[folder] = path

@app.route('/')
def index():
    return jsonify(list(db_files.keys()))

@app.route('/api/<project>')
def app_profiles(project):
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

    
#======= select table all data in project ==============

@app.route('/api/<project>/<table>')
def data_all_table(project, table):
    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # ตรวจสอบว่าตารางมีอยู่จริง
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
        if not cur.fetchone():
            return jsonify({"error": f"ไม่พบตาราง '{table}'"}), 404

        cur.execute(f"SELECT * FROM {table}")
        cols = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        conn.close()

        return jsonify({"columns": cols, "rows": rows}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# app_profiles
@app.route('/api/update/<project>/app_profiles/', methods=['POST'])
def update_app_profiles(project):
    # ดึงค่าจาก query string
    actor_id = request.args.get("actor_id")
    access_token = request.args.get("access_token")
    user_agent = request.args.get("user_agent")
    device_group = request.args.get("device_group")
    net_hni = request.args.get("net_hni")
    sim_hni = request.args.get("sim_hni")
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    school_name = request.args.get("school_name")
    bio_intro = request.args.get("bio_intro")
    city_id = request.args.get("city_id")

    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # ล้างข้อมูลเดิมก่อน
        cur.execute("DELETE FROM app_profiles")

        # เพิ่มข้อมูลใหม่ 1 แถว
        cur.execute("""
            INSERT INTO app_profiles (
                actor_id, access_token, user_agent, device_group,
                net_hni, sim_hni, first_name, last_name,
                school_name, bio_intro, city_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            actor_id, access_token, user_agent, device_group,
            net_hni, sim_hni, first_name, last_name,
            school_name, bio_intro, city_id
        ))

        conn.commit()
        conn.close()

        return jsonify({"status": "อัปเดตข้อมูล app_profiles สำเร็จ"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

#======================================================================================================
# update group id table 
@app.route('/api/update/<project>/group', methods=['POST'])
def update_group_id(project):
    group_id = request.args.get("group_id")
    if not group_id:
        return jsonify({"error": "ต้องระบุ group_id"}), 400

    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    conn = None
    try:
        conn = sqlite3.connect(db_path, timeout=5.0)  # เพิ่ม timeout ป้องกัน locked
        cur = conn.cursor()

        cur.execute("DELETE FROM group_id_table")
        cur.execute("INSERT INTO group_id_table (group_id) VALUES (?)", (group_id,))
        conn.commit()

        return jsonify({"status": "อัปเดต group_id สำเร็จ", "group_id": group_id}), 200

    except sqlite3.OperationalError as e:
        if "locked" in str(e).lower():
            return jsonify({"error": "ฐานข้อมูลถูกล็อก โปรดลองใหม่อีกครั้ง"}), 503
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()

# update pic status table > media id 
@app.route('/api/update/<project>/<table>', methods=['POST'])
def update_table(project, table):
    media_id = request.args.get("media_id")
    if not media_id:
        return jsonify({"error": "ต้องระบุ media_id ใน query string"}), 400

    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # ตรวจสอบว่ามี column media_id จริงหรือไม่
        cur.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cur.fetchall()]
        if "media_id" not in columns:
            return jsonify({"error": f"ตาราง '{table}' ไม่มีคอลัมน์ชื่อ media_id"}), 400

        # ลบข้อมูลเก่าแล้วใส่ใหม่
        cur.execute(f"DELETE FROM {table}")
        cur.execute(f"INSERT INTO {table} (media_id) VALUES (?)", (media_id,))
        conn.commit()
        conn.close()

        return jsonify({"status": f"อัปเดต {table} แล้ว", "media_id": media_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if conn:
            conn.close()

#=========================== clear All data when select projected
@app.route('/api/clear/<project>/<table>', methods=['POST'])
def clear_table(project, table):
    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # ตรวจสอบว่าตารางมีอยู่จริง
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
        if not cur.fetchone():
            return jsonify({"error": f"ไม่พบตาราง '{table}'"}), 404

        # ลบข้อมูลทั้งหมด
        cur.execute(f"DELETE FROM {table}")
        conn.commit()
        conn.close()

        return jsonify({"status": f"ล้างข้อมูลในตาราง '{table}' แล้ว"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if conn:
            conn.close()
#======================================================================================================

if __name__ == '__main__':
    scan_dbs()
    app.run(debug=True)
from flask import Flask, request, jsonify
import sqlite3
import os
import threading
from flask import send_from_directory

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_files = {}
DB_PATH = "news.db"
#=========================================================================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            link TEXT,
            reaction TEXT,
            like_value INTEGER,
            comment_value INTEGER,
            timestamp TEXT DEFAULT (datetime('now', 'localtime')),
            status TEXT,
            log TEXT,
            status_code TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/insert/news', methods=['POST'])
def insert_news():
    data = request.get_json()
    try:
        topic = data['topic']
        link = data['link']
        reaction = data['reaction']
        like_value = int(data['likeValue'])
        comment_value = int(data['commentValue'])
        timestamp = data.get('timestamp')  # ใช้ get ป้องกัน key error
        status = data['status']
        log = data['log']
        status_code = data['status_code']

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        if timestamp:
            cur.execute('''
                INSERT INTO news (topic, link, reaction, like_value, comment_value, timestamp, status, log, status_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (topic, link, reaction, like_value, comment_value, timestamp, status, log, status_code))
        else:
            cur.execute('''
                INSERT INTO news (topic, link, reaction, like_value, comment_value, status, log, status_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (topic, link, reaction, like_value, comment_value, status, log, status_code))

        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get/news', methods=['GET'])
def get_news():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM news ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()

        result = [dict(row) for row in rows]
        return jsonify(result)
    except Exception as e:
        print(f"❌ Error at /api/get/news: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/update/news', methods=['POST'])
def update_news():
    conn = None
    try:
        data = request.get_json()
        log_value = data['log']

        conn = sqlite3.connect(DB_PATH, timeout=5)  # ✅ ป้องกัน locked
        cur = conn.cursor()
        cur.execute('''
            UPDATE news SET status = 'used' WHERE log = ?
        ''', (log_value,))
        conn.commit()
        updated_rows = cur.rowcount

        return jsonify({'status': 'success', 'updated': updated_rows})
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()


#================================================================================================
def scan_dbs():
    for folder in os.listdir(BASE_DIR):
        path = os.path.join(BASE_DIR, folder, "fb_comment_system.db")
        if os.path.isfile(path):
            db_files[folder] = path

@app.route('/')
def index():
    return jsonify(list(db_files.keys()))

@app.route('/dashboard')
def dashboard():
    return send_from_directory('.','dashboard.html')

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
#======================================================================================================
# Update like and comment table
@app.route('/api/update/<project>/like-and-comment', methods=['POST'])
def update_like_and_comment(project):
    reaction_type = request.args.get("reaction_type")
    link = request.args.get("link")
    comment_text = request.args.get("comment_text")

    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # ลบข้อมูลเก่าแล้วใส่ใหม่
        cur.execute("DELETE FROM like_and_comment_table")
        cur.execute("""
            INSERT INTO like_and_comment_table (reaction_type, link, comment_text)
            VALUES (?, ?, ?)
        """, (reaction_type, link, comment_text))
        conn.commit()
        conn.close()

        return jsonify({"status": "อัปเดตข้อมูล like_and_comment สำเร็จ"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if conn:
            conn.close()
#======================================================================================================
@app.route('/api/update/<project>/like-comment-reply-comment', methods=['POST'])
def update_like_comment_reply_comment(project):
    reaction_type = request.args.get("reaction_type")
    link = request.args.get("link")
    comment_text = request.args.get("comment_text")

    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        # ลบข้อมูลเก่าแล้วใส่ใหม่
        cur.execute("DELETE FROM like_comment_and_reply_comment_table")
        cur.execute("""
            INSERT INTO like_comment_and_reply_comment_table (reaction_type, link, comment_text) 
            VALUES (?, ?, ?)
        """, (reaction_type, link, comment_text))
        conn.commit()
        conn.close()
        return jsonify({"status": "อัปเดตข้อมูล like_comment_and_reply_comment สำเร็จ"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()
#======================================================================================================
# update like comment only table
@app.route('/api/update/<project>/like-comment-only', methods=['POST'])
def update_like_comment_only(project):
    reaction_type = request.args.get("reaction_type")
    link = request.args.get("link")

    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # ลบข้อมูลเก่าแล้วใส่ใหม่
        cur.execute("DELETE FROM like_comment_only_table")
        cur.execute("""
            INSERT INTO like_comment_only_table (reaction_type, link)
            VALUES (?, ?)
        """, (reaction_type, link))
        conn.commit()
        conn.close()
        return jsonify({"status": "อัปเดตข้อมูล like_comment_only สำเร็จ"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()
#======================================================================================================
# like only table
@app.route('/api/update/<project>/like-only', methods=['POST'])
def update_like_only(project):
    reaction_type = request.args.get("reaction_type")
    link = request.args.get("link")

    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        # ลบข้อมูลเก่าแล้วใส่ใหม่
        cur.execute("DELETE FROM like_only_table")
        cur.execute("""
            INSERT INTO like_only_table (reaction_type, link)
            VALUES (?, ?)
        """, (reaction_type, link))
        conn.commit()
        conn.close()
        return jsonify({"status": "อัปเดตข้อมูล like_only สำเร็จ"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

#======================================================================================================
# like reel and comment table
@app.route('/api/update/<project>/like-reel-and-comment', methods=['POST'])
def update_like_reel_and_comment(project):
    reaction_type = request.args.get("reaction_type")
    link = request.args.get("link")
    comment_text = request.args.get("comment_text")

    db_path = db_files.get(project)

    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # ลบข้อมูลเก่าแล้วใส่ใหม่
        cur.execute("DELETE FROM like_reel_and_comment_reel_table")
        cur.execute("""
                    INSERT INTO like_reel_and_comment_reel_table (reaction_type, link, comment_text)
                    VALUES (?, ?, ?)
                """, (reaction_type, link, comment_text))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "อัปเดตข้อมูล like_reel_comment สำเร็จ"}), 200
    finally:
        if conn:
            conn.close()
#  =============================================================================
#  update like reel only table
@app.route('/api/update/<project>/like-reel-only', methods=['POST'])
def update_like_reel_only(project):
    reaction_type = request.args.get("reaction_type")
    link = request.args.get("link")

    db_path = db_files.get(project)

    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("DELETE FROM like_reel_only_table")
        cur.execute("""
            INSERT INTO like_reel_only_table (reaction_type, link)
            VALUES (?, ?)
        """, (reaction_type, link))
        conn.commit()
        conn.close()

        return jsonify({"status": "อัปเดตข้อมูล like_reel_only สำเร็จ"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()
#==========================================================================
# update pic caption text table
@app.route('/api/update/<project>/pic-caption-text', methods=['POST'])
def update_pic_caption_text(project):
    status_text = request.args.get("status_text")

    db_path = db_files.get(project)

    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("DELETE FROM pic_caption_text_table")
        cur.execute("""
            INSERT INTO pic_caption_text_table (status_text)
            VALUES (?)
        """, (status_text,))
        conn.commit()
        conn.close()
        return jsonify({"status": "อัปเดตข้อมูล pic_caption_text สำเร็จ"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()
#==================================================================================
# set status text table
@app.route('/api/update/<project>/set-status-text', methods=['POST'])
def update_set_status_text_table(project):
    status_text = request.args.get("status_text")  # หรือใช้ request.form.get(...) ถ้าส่งผ่าน form

    db_path = db_files.get(project)
    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404
    
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("DELETE FROM set_status_text_table")
        cur.execute("""
            INSERT INTO set_status_text_table (status_text, id)
            VALUES (?, ?)
        """, (status_text, 1))
        conn.commit()
        return jsonify({"status": "อัปเดตข้อมูล set_status_text สำเร็จ"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()
#=================================================================================================
# shared link table
@app.route('/api/update/<project>/share-link', methods=['POST'])
def update_share_link(project):
    link = request.args.get("link_link")
    db_path = db_files.get(project)

    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM shared_link_table")
        cur.execute("""
            INSERT INTO shared_link_table (link_link)
            VALUES (?)
        """, (link,))
        conn.commit()
        conn.close()
        return jsonify({"status": "อัปเดตข้อมูล shared_link สำเร็จ"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()
#=======================================================================
# shared link text table 
@app.route('/api/update/<project>/share-link-text', methods=['POST'])
def update_share_link_text(project):
    status_text = request.args.get("status_text")
    status_link = request.args.get("status_link")  # 👉 เปลี่ยนชื่อให้เป็น "status_link" จะสื่อความชัดกว่า
    db_path = db_files.get(project)

    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404
    # if not status_text or not status_link:
    #     return jsonify({"error": "ต้องระบุ status_text และ link_link"}), 400

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # ลบข้อมูลเก่า (ใช้แค่แถวเดียวในตาราง)
        cur.execute("DELETE FROM shared_link_text_table")

        # เพิ่มข้อมูลใหม่
        cur.execute("""
            INSERT INTO shared_link_text_table (status_text, status_link)
            VALUES (?, ?)
        """, (status_text, status_link))

        conn.commit()
        return jsonify({
            "status": "อัปเดตข้อมูล shared_link_text สำเร็จ",
            "status_text": status_text,
            "status_link": status_link
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # 👉 ส่งข้อความ error จริงจะช่วย debug ง่ายขึ้น

    finally:
        if conn:
            conn.close()
#====================================================================================
# subscribee id table
@app.route('/api/update/<project>/subscribe-id', methods=['POST'])
def update_subscribe_id(project):
    subscribe_id = request.args.get("subscribee_id")
    db_path = db_files.get(project)

    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("DELETE FROM subscribee_id_table")
        cur.execute("""
            INSERT INTO subscribee_id_table (subscribee_id)
            VALUES (?)
        """,(subscribe_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "อัปเดตข้อมูล subscribee_id สำเร็จ"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()
#=================================================================================
# unsubscribee id table
@app.route('/api/update/<project>/unsubscribe-id', methods=['POST'])
def update_unsubscribe_id(project):
    unsubscribe_id = request.args.get("unsubscribee_id")
    db_path = db_files.get(project)

    if not db_path:
        return jsonify({"error": "ไม่พบโปรเจกต์"}), 404
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("DELETE FROM unsubscribee_id_table")
        cur.execute("""
            INSERT INTO unsubscribee_id_table (unsubscribee_id)
            VALUES (?)
        """,(unsubscribe_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "อัปเดตข้อมูล unsubscribee_id สำเร็จ"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()
#==============================================================================

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
import os
import re
import requests
import json
import sqlite3
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import sys

# === STEP 0: ดึงข้อมูลจาก input DB ===

# 🧠 หา path โฟลเดอร์แม่จากที่ไฟล์ .py ตัวนี้อยู่
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
db_path = os.path.join(parent_dir, "link_news_reaction.db")

# ✅ เชื่อมต่อฐานข้อมูล
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ดึงข้อมูลแถวล่าสุด
cursor.execute("SELECT link, news_content, reaction FROM input ORDER BY id DESC LIMIT 1")
fb_url, news_text, reaction_type = cursor.fetchone()
conn.close()

print("✅ ดึงข้อมูลสำเร็จ:", fb_url, news_text, reaction_type)

# === STEP 1: ดึง owner_id / post_id จากลิงก์ ===

def get_fbid_from_username(username):
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10)"}
    url = f"https://mbasic.facebook.com/{username}"
    res = requests.get(url, headers=headers, allow_redirects=False)

    if "Location" in res.headers and res.headers["Location"].startswith("intent://profile/"):
        match = re.search(r'intent://profile/(\d+)', res.headers["Location"])
        if match:
            return match.group(1)

    res = requests.get(url, headers=headers)
    match = re.search(r'owner_id=(\d+)', res.text)
    if not match:
        match = re.search(r'profile\.php\?id=(\d+)', res.text)
    return match.group(1) if match else None

def extract_facebook_ids(url):
    story_fbid = re.search(r'story_fbid=(\d+)', url)
    id_qs = re.search(r'[?&]id=(\d+)', url)
    path_ids = re.search(r'facebook\.com/(\d+)/(?:videos|posts)/(\d+)', url)
    username_match = re.search(r'facebook\.com/([^/?&]+)', url)

    post_id = None
    owner_id = None

    if story_fbid:
        post_id = story_fbid.group(1)
    elif path_ids:
        owner_id, post_id = path_ids.groups()

    if not post_id:
        post_id_match = re.search(r'/posts/(\d+)|/videos/(\d+)', url)
        if post_id_match:
            post_id = post_id_match.group(1) or post_id_match.group(2)

    if id_qs:
        owner_id = id_qs.group(1)

    if not owner_id and username_match:
        username = username_match.group(1)
        if username.isdigit():
            owner_id = username
        else:
            owner_id = get_fbid_from_username(username)

    return {"owner_id": owner_id, "post_id": post_id}

ids = extract_facebook_ids(fb_url)
owner_id = ids["owner_id"]
post_id = ids["post_id"]
print("📌 owner_id:", owner_id)
print("📌 post_id :", post_id)

# === STEP 2: เตรียมฐานข้อมูลหลัก ===

db_path2 = os.path.join(os.path.dirname(__file__), "fb_comment_system.db")
conn = sqlite3.connect(db_path2)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        comment TEXT NOT NULL,
        reaction_type TEXT DEFAULT 'like',
        owner_id TEXT DEFAULT '00000000000000',
        post_id TEXT DEFAULT '00000000000000'
    )
''')
conn.commit()

# === STEP ที่คุณขอ: ดึง prompt จาก charactor.db ===

base_dir = os.path.dirname(os.path.abspath(__file__))  # โฟลเดอร์ที่ไฟล์นี้อยู่
char_db_path = os.path.join(base_dir, "promt.db")       # ไม่ต้องใช้ parent_dir แล้ว

conn_prompt = sqlite3.connect(char_db_path)
cursor_prompt = conn_prompt.cursor()
cursor_prompt.execute("SELECT * FROM charactor LIMIT 1")
row = cursor_prompt.fetchone()
prompt_text = row[1]  # คอลัมน์ที่ 2 (index 1)
conn_prompt.close()

# === STEP 3: ส่ง prompt ไปที่ Gemini ===

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:streamGenerateContent?alt=sse"
headers = {
    "Accept": "*/*",
    "Content-Type": "application/json",
    "x-goog-api-key": "AIzaSyCIvoMfv-v54yLrgXaWu52t-L7eymSXFnA"
}

body = {
    "contents": [
        {
            "parts": [
                {
                    "text": prompt_text
                },
                {
                    "text": f"""จากเนื้อหาข่าว: {news_text}  สร้างคอมเมนต์ 10 คอมเมนต์  Output Format: ให้ตอบเฉพาะ 10 คำตอบแยกบรรทัด ห้ามมีเลขลำดับ (1. 2. 3.) หรือคำว่า คอมเมนต์ / ข้อความ / ข้อใด ๆ ไม่ต้องเว้นบรรทัดระหว่างกัน ให้ตอบเป็นข้อความแต่ละบรรทัด 10 บรรทัด เท่านั้น """
                }
            ],
            "role": "user"
        }
    ],
    "generationConfig": {
        "temperature": 1,
        "topP": 1,
        "topK": 1500,
        "maxOutputTokens": 8192
    }
}

response = requests.post(url, headers=headers, data=json.dumps(body), stream=True)

# === STEP 4: รวมข้อความ, แยกบรรทัด, ลบของเก่า, บันทึกใหม่ ===

full_text = ""
for line in response.iter_lines():
    if line:
        decoded_line = line.decode('utf-8').strip()
        if decoded_line.startswith("data: "):
            try:
                data_json = json.loads(decoded_line[6:])
                parts = data_json.get("candidates", [])[0].get("content", {}).get("parts", [])
                for part in parts:
                    full_text += part.get("text", "")
            except Exception as e:
                print("❌ Error:", e)

# ลบของเก่าทั้งหมดก่อน
cursor.execute("DELETE FROM comments")
conn.commit()

# แยกเป็น 10 คำตอบ และบันทึกลง comments.db
for l in full_text.strip().split("\n"):
    clean = l.strip()
    if clean:
        cursor.execute(
            "INSERT INTO comments (comment, reaction_type, owner_id, post_id) VALUES (?, ?, ?, ?)",
            (clean, reaction_type, owner_id, post_id)
        )
        print("✅ saved:", clean)

conn.commit()
conn.close()

def run_main_go():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        main_go_path = os.path.join(current_dir, "main.go")

        if os.path.isfile(main_go_path):
            print(f"🚀 เปิด CMD ใหม่รัน main.go: {main_go_path}")
            subprocess.Popen(
                ["go", "run", "main.go"],
                cwd=current_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            print("❌ ไม่พบ main.go ในไดเรกทอรีเดียวกันกับ getlink.py")

    except Exception as e:
        print("❌ เกิดข้อผิดพลาด: ", e)


# ✅ เรียกใช้
if __name__ == "__main__":
    print("✅ __main__ ทำงานแล้ว")
    run_main_go()
    print("✅ getlink.py จบงานแล้ว ปิดตัวเอง")
    sys.exit(0)



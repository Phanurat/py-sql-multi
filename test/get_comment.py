import requests
import time 
import os
import sqlite3
from urllib.parse import quote_plus
import json
import random

url = "http://127.0.0.1:5000"

def generate_commnet(promt_text, topic_news):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:streamGenerateContent?alt=sse"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "x-goog-api-key": "AIzaSyCIvoMfv-v54yLrgXaWu52t-L7eymSXFnA"
    }
    prompt_text = promt_text
    news_text = topic_news
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
    try:
        response = requests.post(url, headers=headers, json=body, stream=True)
        print("📥 Gemini API Status:", response.status_code)

        if response.status_code != 200:
            print("❌ Gemini API response:", response.text)
            return []

        full_text = ""

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                if decoded_line.startswith("data: "):
                    json_data = decoded_line[6:]
                    try:
                        parsed = json.loads(json_data)
                        parts = parsed.get("candidates", [])[0].get("content", {}).get("parts", [])
                        for part in parts:
                            full_text += part.get("text", "")
                    except Exception as e:
                        continue  # ข้าม event ที่ไม่ใช่ JSON

        # แยกบรรทัด
        comment_lines = [line.strip() for line in full_text.split("\n") if line.strip()]
        return comment_lines[:10]

    except Exception as e:
        print("❌ ERROR calling Gemini API:", e)
        return []

def get_charactor():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    char_db_path = os.path.join(base_dir, "./promt.db")
    conn_prompt = sqlite3.connect(char_db_path)
    cursor_prompt = conn_prompt.cursor()
    cursor_prompt.execute("SELECT * FROM charactor LIMIT 1")
    row = cursor_prompt.fetchone()
    prompt_text = row[1]  # คอลัมน์ที่ 2 (index 1)
    conn_prompt.close()
    return prompt_text 

def get_project_folders():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # ⬅️ ย้ายออกจาก /test
    project_folders = []
    for name in os.listdir(base_dir):
        path = os.path.join(base_dir, name)
        if name.startswith("data") and os.path.isdir(path):
            project_folders.append(name)
    project_folders.sort()
    return project_folders

def main():
    project_list = get_project_folders()
    promt_text = get_charactor()
    topic_news = "แค่ลอง Test นะ"
    reaction = "like"
    link = "www.example.com"

    comments = generate_commnet(promt_text, topic_news)

    if not comments:
        print("❌ ไม่ได้คอมเมนต์จาก Gemini")
        return

    print("📋 คอมเมนต์ที่ได้:", comments)

    # 🔁 แจกเฉพาะ 1 คอมเมนต์ต่อ 1 โปรเจกต์ (ไม่วน)
    for project, comment in zip(project_list, comments):
        print(f"📝 [{project}] Comment =>", comment)

        insert_comment = f"{url}/api/update/{project}/like-and-comment?reaction_type={quote_plus(reaction)}&link={link}&comment_text={quote_plus(comment)}"

        try:
            response = requests.post(insert_comment)
            if response.status_code == 200:
                print(f"✅ บันทึกสำเร็จ [{project}]: {comment}")
            else:
                print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
        except Exception as e:
            print("❌ Error POST:", e)

        time.sleep(1)

if __name__ == "__main__":
    main()
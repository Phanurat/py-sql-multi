import requests
import json
import sqlite3
import os

def get_prompt_text():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    char_db_path = os.path.join(base_dir, "./promt.db")
    conn_prompt = sqlite3.connect(char_db_path)
    cursor_prompt = conn_prompt.cursor()
    cursor_prompt.execute("SELECT * FROM charactor LIMIT 1")
    row = cursor_prompt.fetchone()
    conn_prompt.close()
    return row[1] if row else ""

def check_topic():
    url = "http://127.0.0.1:5000/api/get/comments-get"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Error fetching comments:", response.status_code, response.text)
        return []

def gen_comment(prompt_text, news_text):
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
                    {"text": prompt_text},
                    {"text": f"""จากเนื้อหาข่าว: {news_text}
สร้างคอมเมนต์ 10 คอมเมนต์  
Output Format: ให้ตอบเฉพาะ 10 คำตอบแยกบรรทัด ห้ามมีเลขลำดับ (1. 2. 3.) หรือคำว่า คอมเมนต์ / ข้อความ 
ไม่ต้องเว้นบรรทัดระหว่างกัน ให้ตอบเป็นข้อความแต่ละบรรทัด 10 บรรทัด เท่านั้น"""}
                ],
                "role": "user"
            }
        ],
        "generationConfig": {
            "temperature": 1,
            "topP": 1,
            "topK": 1500,
            "maxOutputTokens": 2048
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(body), stream=True)
        response.raise_for_status()
    except Exception as e:
        print("❌ ERROR calling Gemini API:", e)
        return []

    full_text = ""
    try:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8').strip()
                if decoded_line.startswith("data: "):
                    data_json = json.loads(decoded_line[6:])
                    parts = data_json.get("candidates", [])[0].get("content", {}).get("parts", [])
                    for part in parts:
                        full_text += part.get("text", "")
                    break
    except Exception as e:
        print("❌ ERROR parsing response:", e)
        return []

    comment_lines = [line.strip() for line in full_text.strip().split("\n") if line.strip()]
    return comment_lines[:10]

def main():
    prompt_text = get_prompt_text()
    topic_data = check_topic()

    for item in topic_data:
        news_text = item['topic_content']
        print(f"📌 ข่าว: {news_text}")
        comments = gen_comment(prompt_text, news_text)

        if len(comments) < 10:
            print(f"⚠️ ได้แค่ {len(comments)} คอมเมนต์ → ข้าม")
            continue

        print("✅ คอมเมนต์ที่ได้:")
        for comment in comments:
            print(comment)
        print("-" * 40)

if __name__ == "__main__":
    main()

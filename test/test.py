import requests
import time 
import os
import sqlite3
from urllib.parse import quote_plus
import json
import random

url = "http://127.0.0.1:5000"

def check_dashboards():
    try:
        response = requests.get(f"{url}/api/get/news")
        if response.status_code == 200:
            return response.json()
        else:
            print("❌ Error fetching news:", response.status_code, response.text)
            return []
    except requests.exceptions.RequestException as e:
        print("❌ Error fetching news:", e)
        return []

def check_unused(rows_id):
    log_value="unused"
    payload = { "log": log_value, "id": rows_id }
    api = f"{url}/api/update/news"
    response = requests.post(api,json=payload)
    try: 
        if response.status_code == 200:
            print(f"Update Status สำเร็จ!")
        else:
            print(f"❌ บันทึกล้มเหลว:", response.status_code)
    except Exception as e:
        print("❌ Error POST:", e)
    
    time.sleep(1)

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
    

def generate_comment(promt_text, topic_news):
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

def get_project_folders():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_folders = []
    for name in os.listdir(base_dir):
        if name.startswith("data") and os.path.isdir(os.path.join(base_dir, name)):
            project_folders.append(name)
    project_folders.sort()  # เรียง data1, data2, ...
    return project_folders


def main():
    project_list = get_project_folders()
    news_data = check_dashboards()
    unused_rows = [row for row in news_data if row.get('log') == 'unused']

    if not unused_rows:
        print("✅ No unused rows found.")
        return

    print(f"📌 พบ {len(unused_rows)} รายการที่ log = 'unused'")
    
    for i, row in enumerate(unused_rows):
        project = project_list[i % len(project_list)]  # ใช้ folder ที่มีอยู่จริง
        status = row.get('status')
        rows_id = row.get('id')
        link = row.get("link", "")
        reaction = row.get("reaction", "")
        topic = row.get("topic", "")

        print(f"🔍 ตรวจ status: {status} | project: {project} | id: {rows_id}")
        
        if status == 'like_and_comment':
            pass
            print("like and comment")
            promt_text = get_charactor()
            topic_news = row.get("topic")

            print(promt_text)
            print(topic_news)

            comments = generate_comment(promt_text, topic_news)

            print(comments)

            for i in comments:
                print("Comment =>", i)

                insert_comment = f"{url}/api/insert/comment-dashboard?comment={quote_plus(i)}&log=unused&link={quote_plus(row.get('link'))}&topic={quote_plus(topic_news)}&reaction={quote_plus(row.get('reaction'))}"
                try:
                    response = requests.post(insert_comment)
                    if response.status_code == 200:
                        print(f"✅ INSERT สำเร็จ: {i}")
                    else:
                        print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
                
                except Exception as e:
                    print("❌ Error POST:", e)
                time.sleep(1)            

        elif status == 'like_and_reply_comment':
            pass
            print("like and reply comment")
            promt_text = get_charactor()
            topic_news = row.get("topic", "")
            print(promt_text)
            print(topic_news)

            comments = generate_comment(promt_text, topic_news)

            print(comments)

            for i in comments:
                print("Comment =>", i)

                insert_comment = f"{url}/api/insert/like-comment-reply-comment?comment={quote_plus(i)}&log=unused&link={quote_plus(row.get('link'))}&topic={quote_plus(topic_news)}&reaction={quote_plus(row.get('reaction'))}"
                try:
                    response = requests.post(insert_comment)
                    if response.status_code == 200:
                        print(f"✅ INSERT สำเร็จ: {i}")
                    else:
                        print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
                except Exception as e:
                    print("❌ Error POST:", e)
                time.sleep(1)
        
        elif status == 'like_reel_comment_reel':
            pass
            print("like reel comment reel")
            promt_text = get_charactor()
            topic_news = row.get("topic", "")
            print(promt_text)
            print(topic_news)

            comments = generate_comment(promt_text, topic_news)

            print(comments)

            for i in comments:
                print("Comment =>", i)

                insert_comment = f"{url}/api/insert/like-reel-comment-reel?comment={quote_plus(i)}&log=unused&link={quote_plus(row.get('link'))}&topic={quote_plus(topic_news)}&reaction={quote_plus(row.get('reaction'))}"
                try:
                    response = requests.post(insert_comment)
                    if response.status_code == 200:
                        print(f"✅ INSERT สำเร็จ: {i}")
                    else:
                        print("❌ บันทึกล้มเหลว: ", response.status_code, response.text)
                except Exception as e:
                    print("❌ Error POST:", e)
                time.sleep(1)
        
        elif status == 'like_reel_only':
            reaction = row.get("reaction", "")
            link = row.get("link", "")

            api_insert = f"{url}/api/update/{project}/like-reel-only?reaction_type={reaction}&link={link}"
            try:
                response = requests.post(api_insert)
                if response.status_code == 200:
                    check_unused(rows_id)
                    print(f"✅ บันทึก like_reel_only สำเร็จ: {reaction} | {link}")
                else:
                    print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
            except Exception as e:
                print("❌ Error POST:", e)

        elif status == 'like_comment_only':
            reaction = row.get("reaction", "")
            link = row.get("link", "")

            api_insert = f"{url}/api/update/{project}/like-comment-only?reaction_type={reaction}&link={link}"
            try:
                response = requests.post(api_insert)
                if response.status_code == 200:
                    check_unused(rows_id)
                    print(f"✅ บันทึก like_comment_only สำเร็จ: {reaction} | {link}")
                else:
                    print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
            except Exception as e:
                print("❌ Error POST:", e)

        elif status == 'like_only':
            reaction = row.get("reaction", "")
            link = row.get("link", "")

            api_insert = f"{url}/api/update/{project}/like-only?reaction_type={reaction}&link={link}"
            try:
                response = requests.post(api_insert)
                if response.status_code == 200:
                    check_unused(rows_id)
                    print(f"✅ บันทึก like_only สำเร็จ: {reaction} | {link}")
                else:
                    print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
            except Exception as e:
                print("❌ Error POST:", e)
            time.sleep(1)

        elif status == 'like_page':
            reaction = row.get("reaction", "")
            link = row.get("link", "")

            api_insert = f"{url}/api/update/{project}/like-page?reaction_type={reaction}&link={link}"
            try:
                response = requests.post(api_insert)
                if response.status_code == 200:
                    check_unused(rows_id)
                    print(f"✅ บันทึก like_page สำเร็จ: {reaction} | {link}")
                else:
                    print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
            except Exception as e:
                print("❌ Error POST:", e)

        elif status == 'subscribe_id':
            subscribee_id = row.get("link", "")

            api_insert = f"{url}/api/update/{project}/subscribee-id?subscribee_id={subscribee_id}"
            
            try:
                response = requests.post(api_insert)
                if response.status_code == 200:
                    check_unused(rows_id)
                    print(f"✅ บันทึก subscribee_id สำเร็จ: {subscribee_id}")
                else:
                    print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
            except Exception as e:
                print("❌ Error POST:", e)
            time.sleep(1)
            
        elif status == 'unsubscribe_id':
            unsubscribee_id = row.get("link", "")

            api_insert = f"{url}/api/update/{project}/unsubscribee-id?unsubscribee_id={unsubscribee_id}"

            try:
                response = requests.post(api_insert)
                if response.status_code == 200:
                    check_unused(rows_id)
                    print(f"✅ บันทึก unsubscribee_id สำเร็จ: {unsubscribee_id}")
                else:
                    print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
            except Exception as e:
                print("❌ Error POST:", e)
            time.sleep(1)

        elif status == 'share_link':
            link_link = requests.get("link", "")

            api_insert = f"{url}/api/update/{project}/share-link?link_link={link_link}"
            
            try:
                response = requests.post(api_insert)
                if response.status_code == 200:
                    check_unused(rows_id)
                    print(f"✅ บันทึก share_link สำเร็จ: {link_link}")
                else:
                    print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
            except Exception as e:
                print("❌ Error POST:", e)
            time.sleep(1)

        elif status == 'share_link_text':
            status_text = "ทดสอบข้อความ"
            status_link = requests.get("link", "")

            api_insert = f"{url}/api/update/{project}/share-link-text?status_text={status}&status_link={status_link}"
            
            try:
                response = requests.post(api_insert)
                if response.status_code == 200:
                    check_unused(rows_id)
                    print(f"✅ บันทึก share_link_text สำเร็จ: {status_text} | {status_link}")
                else:
                    print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
            except Exception as e:
                print("❌ Error POST:", e)
            time.sleep(1)

        elif status == 'join_group':
            group_id = row.get("link", "")

            api_insert = f"{url}/api/update/{project}/group-id?group_id={group_id}"
            
            try:
                response = requests.post(api_insert)
                if response.status_code == 200:
                    check_unused(rows_id)
                    print(f"✅ บันทึก group_id สำเร็จ: {group_id}")
                else:
                    print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
            except Exception as e:
                print("❌ Error POST:", e)
            time.sleep(1)

        elif status == 'leave_group':
            group_id = row.get("link", "")

            api_insert = f"{url}/api/update/{project}/group-id?group_id={group_id}"

            try:
                response = requests.post(api_insert)
                if response.status_code == 200:
                    check_unused(rows_id)
                    print(f"✅ บันทึก leave_group สำเร็จ: {group_id}")
                else:
                    print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
            except Exception as e:
                print("❌ Error POST:", e)
            time.sleep(1)

        else:
            print(f"⚠️ ยังไม่มี handler สำหรับ status: {status} | project: {project} | rows_id: {rows_id}")

if __name__ == "__main__":
    main()
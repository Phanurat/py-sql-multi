import requests
import time
import os
from urllib.parse import quote_plus
import sqlite3
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


def run_link_page_for_id_page(row, project, rows_id):
    page_id = row.get("page_id", "")

    api_url = f"{url}/api/update/{project}/link-page-for-id-page?page_id={page_id}"

    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก link_page_for_id_page สำเร็จ: {page_id}")
        else:
            print(f"❌ บันทึกล้มเหลว:", response.status_code)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_group_id(row, project, rows_id):
    group_id = row.get("group_id", "")

    api_url = f"{url}/api/update/{project}/group-id?group_id={group_id}"

    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก group_id สำเร็จ: {group_id}")
        else:
            print(f"❌ บันทึกล้มเหลว:", response.status_code)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_unsubscribee_id(row, project, rows_id):
    unsubscribee_id = row.get("unsubscribee_id", "")

    api_url = f"{url}/api/update/{project}/unsubscribee-id?unsubscribee_id={unsubscribee_id}"

    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก subscribee_id สำเร็จ: {unsubscribee_id}")
        else:
            print(f"❌ บันทึกล้มเหลว:", response.status_code)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_subscribee_id(row, project, rows_id):
    subscribee_id = row.get("subscribee_id", "")

    api_url = f"{url}/api/update/{project}/subscribee-id?subscribee_id={subscribee_id}"

    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก subscribee_id สำเร็จ: {subscribee_id}")
        else:
            print(f"❌ บันทึกล้มเหลว:", response.status_code)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_share_link_text(row, project, rows_id):
    status_text = row.get("status_text", "")
    status_link = row.get("status_link", "")

    api_url = f"{url}/api/update/{project}/share-link?status_text={status_text}&status_link={status_link}"
    
    try:
        response = requests.post(api_url)
        if response == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก share_link_text สำเร็จ: {status_text} | {status_link}")
        else:
            print(f"❌ บันทึกล้มเหลว:", response.status_code)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)


def run_share_link(row, project, rows_id):
    link_link = row.get("link_link", "")

    api_url = f"{url}/api/update/{project}/share-link?link_link={link_link}"
    try:
        response = requests.post(api_url)
        if response.status == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก share_link สำเร็จ: {link_link}")
        else:
            print(f"❌ บันทึกล้มเหลว:", response.status_code)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_set_status_text(row, project, rows_id):
    status_text = row.get("status_text", "")

    api_url = f"{url}/api/update/{project}/set-status-text?status_text={status_text}"
    try:
        response = requests.post(api_url)
        if response.status == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก set_status_text สำเร็จ: {status_text}")
        else:
            print(f"❌ บันทึกล้มเหลว:", response.status_code)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_pic_caption_text(row, project, rows_id):
    status_text = row.get("status_text", "")

    api_url = f"{url}/api/update/{project}/pic-caption-text?status_text={status_text}"
    try:
        response = requests.post(api_url)
        if response.status == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก pic_caption_text สำเร็จ: {status_text}")
        else:
            print(f"❌ บันทึกล้มเหลว:", response.status_code)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_like_reel_only(row, project, rows_id):
    reaction = row.get("reaction", "")
    link = row.get("link", "")

    api_url = f"{url}/api/update/{project}/like-reel-only?reaction_type={reaction}&link={link}"
    try:
        response = requests.post(api_url)
        if response.status == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก like_reel_only สำเร็จ: {reaction} | {link}")
        else:
            print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)
    
def run_like_reel_comment_reel(row, project, rows_id):
    reaction = row.get("reaction", "")
    link = row.get("link", "")
    comment_text = row.get("comment_text", "")

    api_url = f"{url}/api/update/{project}/like-reel-and-comment?reaction_type={reaction}&link={link}&comment_text={comment_text}"
    try:
        response = requests.post(api_url)
        if response.status == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก like_reel_comment_reel สำเร็จ: {reaction} | {link} | {comment_text}")
        else:
            print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_like_only(row, project, rows_id):
    reaction = row.get("reaction", "")
    link = row.get("link", "")

    api_url = f"{url}/api/update/{project}/like-only?reaction_type={reaction}&link={link}"
    
    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก like_only สำเร็จ: {reaction} | {link}")
        else:
            print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_like_comment_only(row, project, rows_id):
    reaction = row.get("reaction", "")
    link = row.get("link", "")

    api_url = f"{url}/api/update/{project}/like-comment-only?reaction_type={reaction}&link={link}"

    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก like_comment_only สำเร็จ: {reaction} | {link}")
        else:
            print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_like_and_reply_comment(row, project, rows_id):
    reaction = quote_plus(str(row.get("reaction", "")))
    link = quote_plus(str(row.get("link", "")))
    comment_text = quote_plus(str(row.get("comment_text", "")))

    api_url = f"{url}/api/update/{project}/like-comment-reply-comment?reaction_type={reaction}&link={link}&comment_text={comment_text}"
    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            check_unused(rows_id)
            print(f"✅ บันทึก Like and Reply Comment สำเร็จ: {reaction} | {link} | {comment_text}")
        else:
            print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
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

def random_comment():
    return [
        { "id": 1, "comment": "เห็นแล้วอึ้งเลยครับ ไม่คิดว่าจะเกิดขึ้นจริง" },
        { "id": 2, "comment": "เรื่องแบบนี้ต้องมีคนรับผิดชอบแล้วแหละ" },
        { "id": 3, "comment": "ทำไมมันถึงเงียบกันขนาดนี้?" },
        { "id": 4, "comment": "อยากให้สื่อช่วยขุดลึกกว่านี้อีก" },
        { "id": 5, "comment": "ใครคิดเหมือนเราบ้างว่าเรื่องมันแปลกๆ" },
        { "id": 6, "comment": "เอาใจช่วยทุกฝ่ายที่เกี่ยวข้องนะครับ" },
        { "id": 7, "comment": "สมัยนี้อะไรๆ ก็เกิดขึ้นได้หมดจริงๆ" },
        { "id": 8, "comment": "ถ้าไม่มีหลักฐานชัดเจนก็อย่าเพิ่งด่วนสรุปนะ" },
        { "id": 9, "comment": "น่าติดตามต่อว่าจะจบยังไง" },
        { "id": 10, "comment": "ไม่เชื่อว่าบังเอิญหรอก ต้องมีอะไรเบื้องหลัง" },
        { "id": 11, "comment": "อยากให้สังคมหันมาสนใจเรื่องพวกนี้มากกว่านี้" },
        { "id": 12, "comment": "ข่าวแบบนี้เห็นแล้วเครียดเลย" },
        { "id": 13, "comment": "รู้สึกหมดหวังกับระบบ" },
        { "id": 14, "comment": "อยากให้มีบทลงโทษที่จริงจังมากกว่านี้" },
        { "id": 15, "comment": "เป็นกำลังใจให้ผู้เสียหายครับ" },
        { "id": 16, "comment": "พวกเราต้องไม่ลืมเรื่องนี้เด็ดขาด" },
        { "id": 17, "comment": "ทำไมคนผิดยังลอยนวลอยู่ได้?" },
        { "id": 18, "comment": "ไม่ใช่ครั้งแรกที่เกิดเรื่องแบบนี้" },
        { "id": 19, "comment": "สื่อควรเสนอหลายๆ มุมให้รอบด้าน" },
        { "id": 20, "comment": "ถ้าไม่มีคนลุกขึ้นมาสู้ มันก็จะเป็นแบบนี้ไปเรื่อยๆ" }
    ]

def run_like_and_comment(row, project, rows_id):
    print(rows_id)
    check_list_data = check_like_and_comments()
    unused_rows = [row for row in check_list_data if row.get('log') == 'unused']

    prompt_text = get_charactor()
    news_text = "ทดสอบระบบ"
    comments = gen_comment(prompt_text, news_text)

    total_rows = len(unused_rows)
    if total_rows == 0:
        print("🚫 ไม่มี row ที่ยัง unused")
        return

    for i, comment in enumerate(comments):  # comments เป็น list[str]
        row = unused_rows[i % total_rows]
        project = f"data{(i % total_rows) + 1}"

        reaction = quote_plus(str(row.get("reaction", "")))
        link = quote_plus(str(row.get("link", "")))
        comment_text = quote_plus(comment)

        api_url = f"{url}/api/update/{project}/like-and-comment?reaction_type={reaction}&link={link}&comment_text={comment_text}"

        try:
            response = requests.post(api_url)
            if response.status_code == 200:
                print(f"✅ [{project}] → {comment}")
            else:
                print(f"❌ [{project}] → {response.status_code}: {response.text}")
        except Exception as e:
            print(f"❌ POST ERROR [{project}]:", e)

        time.sleep(1)

def check_like_and_comments():
    url_get = f"{url}/api/get/comments-get"
    response = requests.get(url_get)

    if response.status_code == 200:
        return response.json()
    else:
        print("❌ Error fetching comments:", response.status_code, response.text)
        return []
    
def main():
    news_data = check_dashboards()
    unused_rows = [row for row in news_data if row.get('log') == 'unused']

    if not unused_rows:
        print("✅ No unused rows found.")
        return

    print(f"📌 พบ {len(unused_rows)} รายการที่ log = 'unused'")
    
    for i, row in enumerate(unused_rows):
        project = f"data{i+1}"
        status = row.get('status')
        rows_id = row.get('id')
        
        print(f"🔍 ตรวจ status: {status} | project: {project}")
        
        if status == 'like_and_comment':
            run_like_and_comment(row, project, rows_id)

        elif status == 'like_comment_reply_comment':
            run_like_and_reply_comment(row, project, rows_id)

        elif status == 'like_comment_only':
            run_like_comment_only(row, project, rows_id)
        
        elif status == 'like_only':
            run_like_only(row, project, rows_id)

        elif status == 'like_reel_comment_reel':
            run_like_reel_comment_reel(row, project)
        
        elif status == 'like_reel_only':
            run_like_reel_only(row, project, rows_id)
        
        elif status == 'pic_caption_text':
            run_pic_caption_text(row, project, rows_id)
        
        elif status == "set_status_text":
            run_set_status_text(row, project, rows_id)
        
        elif status == "share-link":
            run_share_link(row, project, rows_id)
        
        elif status == "share-link-text":
            run_share_link_text(row, project, rows_id)
        
        elif status == "subscribee_id":
            run_subscribee_id(row, project, rows_id)
        
        elif status == "unsubscribee_id":
            run_unsubscribee_id(row, project, rows_id)
        
        elif status == "group_id":
            run_group_id(row, project, rows_id)
        
        elif status == "link-page-for-id-page":
            run_link_page_for_id_page(row, project, rows_id)

        else:
            print(f"⚠️ ยังไม่มี handler สำหรับ status: {status} | project: {project} | rows_id: {rows_id}")
  
if __name__ == "__main__":
    main()

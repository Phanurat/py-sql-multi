import requests
import time
from urllib.parse import quote_plus

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
    
def run_like_reel_comment_reel(row, project):
    reaction = row.get("reaction", "")
    link = row.get("link", "")
    comment_text = row.get("comment_text", "")

    api_url = f"{url}/api/update/{project}/like-reel-and-comment?reaction_type={reaction}&link={link}&comment_text={comment_text}"
    try:
        response = requests.post(api_url)
        if response.status == 200:
            print(f"✅ บันทึก like_reel_comment_reel สำเร็จ: {reaction} | {link} | {comment_text}")
        else:
            print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_like_only(row, project):
    reaction = row.get("reaction", "")
    link = row.get("link", "")

    api_url = f"{url}/api/update/{project}/like-only?reaction_type={reaction}&link={link}"
    
    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            print(f"✅ บันทึก like_only สำเร็จ: {reaction} | {link}")
        else:
            print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def  run_like_comment_only(row, project):
    reaction = row.get("reaction", "")
    link = row.get("link", "")

    api_url = f"{url}/api/update/{project}/like-comment-only?reaction_type={reaction}&link={link}"

    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            print(f"✅ บันทึก like_comment_only สำเร็จ: {reaction} | {link}")
        else:
            print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

def run_like_and_reply_comment(row, project):
    reaction = quote_plus(str(row.get("reaction", "")))
    link = quote_plus(str(row.get("link", "")))
    comment_text = quote_plus(str(row.get("comment_text", "")))

    api_url = f"{url}/api/update/{project}/like-comment-reply-comment?reaction_type={reaction}&link={link}&comment_text={comment_text}"
    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            print(f"✅ บันทึก Like and Reply Comment สำเร็จ: {reaction} | {link} | {comment_text}")
        else:
            print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)
    

def run_like_and_comment(row, project):
    reaction = quote_plus(str(row.get("reaction", "")))
    link = quote_plus(str(row.get("link", "")))

    api_url = f"{url}/api/update/{project}/like-and-comment?reaction_type={reaction}&link={link}"

    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            print(f"✅ บันทึก Like and Comment สำเร็จ: {reaction} | {link}")
        else:
            print(f"❌ บันทึกล้มเหลว: {response.status_code} →", response.text)
    except Exception as e:
        print("❌ Error POST:", e)

    time.sleep(1)

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
        
        print(f"🔍 ตรวจ status: {status} | project: {project}")
        
        if status == 'like_and_comment':
            run_like_and_comment(row, project)

        elif status == 'like_comment_reply_comment':
            run_like_and_reply_comment(row, project)

        elif status == 'like_comment_only':
            run_like_comment_only(row, project)
        
        elif status == 'like_only':
            run_like_only(row, project)

        elif status == 'like_reel_comment_reel':
            run_like_reel_comment_reel(row, project)

        else:
            print(f"⚠️ ยังไม่มี handler สำหรับ status: {status} | project: {project}")


if __name__ == "__main__":
    main()

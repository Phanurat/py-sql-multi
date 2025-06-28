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

def  run_like_comment_only(row, project, rows_id):
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
    

def run_like_and_comment(row, project, rows_id):
    reaction = quote_plus(str(row.get("reaction", "")))
    link = quote_plus(str(row.get("link", "")))

    api_url = f"{url}/api/update/{project}/like-and-comment?reaction_type={reaction}&link={link}"

    try:
        response = requests.post(api_url)
        if response.status_code == 200:
            check_unused(rows_id)
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

import requests
import time

url = "http://127.0.0.1:5000"

def check_data_news():
    try:
        reponse= requests.get(f"{url}/api/get/news")
        if reponse.status_code == 200:
            return reponse.json()
        else:
            print("❌ Error fetching news:", reponse.status_code, reponse.text)
            return []
    except Exception as e:
        print("❌ Exception fetching:", e)
        return []
    
def process_run_script():
    data = check_data_news()
    # Check Script
    unused_rows = [row for row in data if row.get('log') == 'unused']

    for row in unused_rows:
        status = row.get('status')
        if status == 'like_and_comment':
            print("Run Script Like and Comment")
            like_and_comment()
        elif status == 'like_comment_reply_comment':
            print("Run Script Like Comment Reply Comment")
        elif status == 'like_comment_only':
            print("Run Script Like Comment Only")
        elif status == 'like_only':
            print("Run Script Like Only")
        elif status == 'like_reel_comment_reel':
            print("Run Script Like Reel Comment Reel")
        elif status == 'like_reel_only':
            print("Run Script Like Reel Only")
        elif status == 'shared_link_text':
            print("Run Script Shared Link Text")
        elif status == 'shared_link':
            print("Run Script Shared Link")
        elif status == 'subscribee_id':
            print("Run Script Subscribee ID")
        elif status == 'unsubscribe_id':
            print("Run Script Unsubscribee ID")
        else:
            print("⚠️ ไม่พบ status ที่กำหนดไว้")
        time.sleep(2)

def update_log_to_used(log_value="unused", retries=3, delay=1):
    payload = { "log": log_value }
    data = check_data_news()

    for attempt in range(retries):
        try:
            res = requests.post(f"{url}/api/update/news", json=payload)
            res.raise_for_status()
            print("✅ Updated successfully:", res.json())
            return
        except Exception as e:
            print(f"⚠️ Retry {attempt + 1}/{retries} failed:", e)
            time.sleep(delay)

    print("❌ Failed to update after retries.")

def like_and_comment():
    data_check = check_data_news()
    unused_rows = [row for row in data_check if row.get('log') == 'unused']
    if not unused_rows:
        print("ℹ️ ไม่มีข่าวที่ log = 'unused'")
        return
    print(f"📌 พบ {len(unused_rows)} รายการที่ log = 'unused' → เริ่มอัปเดต...")
    # update_log_to_used("unused")

    response = requests.get(f"{url}/")
    data = response.json()
    print("Object Data =>", len(data))

    for object in data:
        print(object)

        response_get = requests.get(f"{url}/api/{object}/like_and_comment_table")
        data = response_get.json()

        columns = data['columns']
        rows = data['rows']

        if not rows:
            print("ไม่มีข้อมูลใน rows")
            continue

        # หาตำแหน่งของแต่ละ field
        reaction_index = columns.index("reaction_type")
        link_index = columns.index("link")

        for row in rows:
            print("Data =>", row[reaction_index])
            print("Data =>", row[link_index])
            
            response = requests.post(f"{url}/api/update/{object}/like-and-comment?reaction_type={row[reaction_index]}&link={row[link_index]}")
            if response.status_code == 200:
                print("✅ อัปเดตสำเร็จ")
            else:
                print("❌ อัปเดตไม่สำเร็จ")
            time.sleep(1)


def run(): 
    process_run_script()

    


run()

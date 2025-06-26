import requests
import time

url = "http://127.0.0.1:5000"

def check_data_news():
    try:
        response = requests.get(f"{url}/api/get/news")
        if response.status_code == 200:
            return response.json()
        else:
            print("❌ Error fetching news:", response.status_code, response.text)
            return []
    except Exception as e:
        print("❌ Exception fetching:", e)
        return []

def update_log_to_used(log_value="unused", retries=3, delay=1):
    payload = { "log": log_value }

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

def run():
    data = check_data_news()

    unused_rows = [row for row in data if row.get('log') == 'unused']
    if not unused_rows:
        print("ℹ️ ไม่มีข่าวที่ log = 'unused'")
        return

    print(f"📌 พบ {len(unused_rows)} รายการที่ log = 'unused' → เริ่มอัปเดต...")
    update_log_to_used("unused")

run()

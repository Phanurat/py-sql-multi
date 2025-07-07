import requests
import time
import os
import sqlite3
from urllib.parse import quote_plus
import json
import random
import json

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
    unused_rows = [row for row in news_data]

    if not unused_rows:
        print("✅ No unused rows found.")
        return
    
    numb = len(news_data)
    print(f"📌 พบ {numb} รายการ")

if __name__ == "__main__":
    main()
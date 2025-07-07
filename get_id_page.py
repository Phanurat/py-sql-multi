import re
import requests

def get_fbid_from_username(username):
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10)"}
    url = f"https://mbasic.facebook.com/{username}"
    res = requests.get(url, headers=headers, allow_redirects=False)

    # ตรวจจาก redirect
    if "Location" in res.headers and res.headers["Location"].startswith("intent://profile/"):
        match = re.search(r'intent://profile/(\d+)', res.headers["Location"])
        if match:
            return match.group(1)

    # ตรวจจากเนื้อ HTML
    res = requests.get(url, headers=headers)
    match = re.search(r'owner_id=(\d+)', res.text)
    if not match:
        match = re.search(r'profile\.php\?id=(\d+)', res.text)
    return match.group(1) if match else None


def extract_owner_id(url):
    match = re.search(r'[?&]id=(\d+)', url)
    if match:
        return match.group(1)

    match = re.search(r'facebook\.com/(\d+)/(?:videos|posts)/', url)
    if match:
        return match.group(1)

    match = re.search(r'facebook\.com/([^/?&]+)', url)
    if match:
        username = match.group(1)
        if username.isdigit():
            return username
        else:
            return get_fbid_from_username(username)

    return None


# === MAIN PROGRAM ===
if __name__ == "__main__":
    print("🔗 ใส่ลิงก์โพสต์ Facebook:")
    fb_url = input("👉 URL: ").strip()

    owner_id = extract_owner_id(fb_url)
    if owner_id:
        print("✅ owner_id:", owner_id)
    else:
        print("❌ ไม่สามารถดึง owner_id จากลิงก์นี้ได้")

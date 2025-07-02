import re
from urllib.parse import urlparse, parse_qs

def classify_facebook_link(url):
    # Normalize
    url = url.strip()

    # Parse domain
    parsed = urlparse(url)
    path = parsed.path
    query = parse_qs(parsed.query)

    # ตรวจสอบจากโครงสร้างลิงก์
    if 'comment_id' in query:
        return "comment"
    elif "photo.php" in path:
        return "photo"
    elif "reel" in path:
        return "reel"
    elif "groups/" in path:
        return "group"
    elif re.search(r"/videos/\d+", path):
        return "video"
    elif re.search(r"/watch/", path):
        return "watch"
    elif re.search(r"/posts/\d+", path):
        return "page_post"
    elif re.search(r"/permalink/\d+", path):
        return "group_post"
    elif re.search(r"/stories/\d+", path):
        return "story"
    elif re.match(r"^/profile\.php", path):
        return "user_profile"
    elif re.match(r"^/[\w\d\.]+/?$", path):
        return "username_profile"
    elif re.search(r"/photos/", path):
        return "photo_album"
    elif re.search(r"/marketplace/", path):
        return "marketplace"
    elif "events" in path:
        return "event"
    elif "live" in path:
        return "live_video"
    elif "/ads/" in path:
        return "ads"
    else:
        return "unknown"

# 🔍 ตัวอย่างการใช้งาน
examples = [
    "https://www.facebook.com/thairath/posts/1213590150807326",
    "https://www.facebook.com/thairath/videos/1933667300803481",
    "https://www.facebook.com/thairath/posts/1213577267475281",
    "https://www.facebook.com/thairath/videos/1074047681396252",
    "https://www.facebook.com/watch?v=3547403238818359",
    "https://www.facebook.com/reel/1412132203452629",
]

for url in examples:
    print(f"{url} → {classify_facebook_link(url)}")

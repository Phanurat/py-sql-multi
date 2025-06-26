# 📦 Facebook Comment System API

API นี้ใช้สำหรับจัดการและอัปเดตข้อมูลต่าง ๆ ในระบบจำลองจัดการคอมเมนต์ Facebook ผ่าน SQLite หลายโปรเจกต์ (ฐานข้อมูลละโฟลเดอร์)

## ✅ วิธีเริ่มต้น
```
python app.py
```

## 🔍 Index

| Method | Endpoint | คำอธิบาย |
|--------|----------|-----------|
| GET    | `/` | แสดงชื่อโปรเจกต์ทั้งหมด (folder name) ที่มี `fb_comment_system.db` |
| GET    | `/api/<project>` | ดึงข้อมูลทุกตารางในโปรเจกต์นั้น |
| GET    | `/api/<project>/<table>` | ดึงข้อมูลทั้งหมดจากตารางที่ระบุ |

---

## 📥 API สำหรับการอัปเดตข้อมูล

> หมายเหตุ: ข้อมูลส่งผ่าน `query string` เช่น `?status_text=xxx&link_link=yyy`

### 🔐 App Profiles
```
POST /api/update/<project>/app_profiles/
```
**Params**: `actor_id`, `access_token`, `user_agent`, `device_group`, `net_hni`, `sim_hni`, `first_name`, `last_name`, `school_name`, `bio_intro`, `city_id`

---

### 👥 Group ID
```
POST /api/update/<project>/group?group_id=xxx
```

---

### ❤️ Like & Comment
```
POST /api/update/<project>/like-and-comment
```
**Params**: `reaction_type`, `link`, `comment_text`

---

### ❤️💬 Like, Comment & Reply
```
POST /api/update/<project>/like-comment-reply-comment
```
**Params**: `reaction_type`, `link`, `comment_text`

---

### ❤️ Only Like Comment
```
POST /api/update/<project>/like-comment-only
```

---

### 👍 Like Only
```
POST /api/update/<project>/like-only
```

---

### 🎞️ Like Reel + Comment
```
POST /api/update/<project>/like-reel-and-comment
```

---

### 🎞️ Like Reel Only
```
POST /api/update/<project>/like-reel-only
```

---

### 🖼️ Pic Caption Text
```
POST /api/update/<project>/pic-caption-text?status_text=...
```

---

### 📝 Set Status Text
```
POST /api/update/<project>/set-status-text?status_text=...
```

---

### 🔗 Share Link
```
POST /api/update/<project>/share-link?link_link=...
```

---

### 📝🔗 Share Link + Status
```
POST /api/update/<project>/share-link-text?status_text=...&status_link=...
```

---

### ➕ Subscribe ID
```
POST /api/update/<project>/subscribe-id?subscribee_id=...
```

---

### ➖ Unsubscribe ID
```
POST /api/update/<project>/unsubscribe-id?unsubscribee_id=...
```

---

### 📷 อัปเดต media_id ลงตารางใด ๆ
```
POST /api/update/<project>/<table>?media_id=...
```

---

## ❌ ล้างข้อมูลตารางใด ๆ
```
POST /api/clear/<project>/<table>
```

---

## 🧠 เพิ่มเติม
- ระบบจะสแกนหาไฟล์ `fb_comment_system.db` ที่อยู่ในแต่ละโฟลเดอร์อัตโนมัติ
- ทุกคำสั่ง `POST` จะลบข้อมูลเดิมก่อนแล้วแทนที่ด้วยข้อมูลใหม่
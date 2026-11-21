# แก้ไข Deploy failed status 127 บน Render.com

## สาเหตุจากรูปที่ส่งมา:
```
Running 'wsgi:application'
bash: line 1: wsgi:application: command not found
Exited with status 127
```

**สาเหตุ:** ใส่ Start Command ผิด ใส่แค่ `wsgi:application` เฉยๆ
Render จะเอาไปรันเป็น shell command เลยหาไม่เจอ

**ต้องใส่:** `gunicorn wsgi:application`

---

## วิธีแก้บน Render Dashboard:

1. ไปที่ https://dashboard.render.com
2. เลือก Service ที่ Deploy failed
3. ไปที่ **Settings** > **Build & Deploy**
4. แก้ **Start Command** จาก:
   ```
   wsgi:application
   ```
   เป็น:
   ```
   gunicorn wsgi:application --bind 0.0.0.0:$PORT
   ```
   หรือแบบสั้น:
   ```
   gunicorn wsgi:app
   ```

5. กด **Save Changes** > **Manual Deploy** > **Deploy latest commit**

---

## ถ้าจะรัน Discord Bot + Web Realtime บน Render:

Discord bot ต้องรัน 24 ชม. ต้องใช้ Background Worker (ต้องใช้แผนเสียเงิน)

**ทางเลือกฟรี:**
- Web Dashboard รันบน Render (ใช้ wsgi.py)
- Discord Bot รันบน VPS / Railway / Replit / เครื่องตัวเองด้วย `python bot.py`

**ถ้ามี VPS:**
Start Command ใส่:
```
python bot.py
```
แล้วตั้ง ENV:
```
DISCORD_TOKEN=xxx
ALERT_CHANNEL_ID=xxx
PORT=10000
```

บอทจะเปิดเว็บเองที่ http://0.0.0.0:$PORT + WebSocket Realtime

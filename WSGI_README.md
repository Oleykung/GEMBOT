# วิธีใส่ค่า gunicorn your_application.wsgi

## ปัญหาที่เจอในรูป
ช่องที่ขึ้นว่า `gunicorn your_application.wsgi` + Required สีแดง
แปลว่าโฮสติ้งบังคับให้ใส่ชื่อไฟล์ WSGI

## ต้องใส่อะไร?

### แบบที่ 1: ใช้ไฟล์ wsgi.py ที่ให้ไป (แนะนำ)
ในโฟลเดอร์นี้มีไฟล์ `wsgi.py` แล้ว ให้ใส่ตามนี้:

```
wsgi
```
หรือ
```
wsgi:app
```
หรือถ้าโฮสให้ใส่เต็มๆ:
```
wsgi:application
```

### แบบที่ 2: ถ้าใช้ passenger_wsgi.py (cPanel)
```
passenger_wsgi
```

### แบบที่ 3: ถ้าใช้ asgi.py + uvicorn (Realtime WebSocket)
```
asgi:app
```
แล้วรันด้วย:
uvicorn asgi:app --host 0.0.0.0 --port 8000

### แบบที่ 4: รันบอท Discord + เว็บ Realtime บน VPS (แนะนำสุด)
บน VPS ไม่ต้องใช้ wsgi เลย รันแบบนี้:
```
python bot.py
```
มันจะเปิดทั้งบอท Discord และเว็บ http://localhost:8080 + WebSocket ws://localhost:8080/ws อัตโนมัติ

แล้วทำ Reverse Proxy จาก Nginx ไปพอร์ต 8080

---

## สรุป
- ช่อง `gunicorn your_application.wsgi` ให้ใส่ `wsgi` หรือ `wsgi:app`
- ถ้าไม่ได้ ให้ลอง `passenger_wsgi`
- บอท Discord ต้องรันแยกด้วย `python bot.py` ตลอด 24 ชม. ไม่ได้รันผ่าน gunicorn

"""
สำหรับโฮสติ้งที่ใช้ Passenger (cPanel, DirectAdmin บางเจ้า)
ไฟล์นี้ชื่อ passenger_wsgi.py

ช่อง WSGI ให้ใส่:
passenger_wsgi

หรือ

passenger_wsgi:application
"""
from wsgi import app as application

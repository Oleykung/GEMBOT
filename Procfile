# Procfile for Render / Heroku
# ใช้ gunicorn ไม่ใช่ wsgi:application เฉยๆ

web: gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 2

# ถ้าจะรันบอท Discord บน VPS
# bot: python bot.py

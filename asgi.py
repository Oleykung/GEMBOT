"""
ASGI for hosting with uvicorn - Realtime version (WebSocket support)
ใช้สำหรับโฮสที่รองรับ ASGI

รันด้วย:
uvicorn asgi:app --host 0.0.0.0 --port 8000

หรือ gunicorn:
gunicorn asgi:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
"""
from bot import create_web_app
import asyncio

# Create aiohttp app for ASGI
app = create_web_app()
# For uvicorn/gunicorn compatibility
application = app

#!/bin/bash
# Start script for Render.com - Fixed status 127

echo "🚀 Granado Espada M - Render Fixed Start"
echo "PORT: $PORT"

# ถ้ามี DISCORD_TOKEN ให้รันบอท + เว็บ Realtime
if [ ! -z "$DISCORD_TOKEN" ]; then
    echo "✅ DISCORD_TOKEN found - Running Discord bot + Web Realtime"
    python bot.py
else
    echo "⚠️ No DISCORD_TOKEN - Running Web Only (Flask WSGI)"
    echo "Start command: gunicorn wsgi:application --bind 0.0.0.0:$PORT"
    gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 2
fi

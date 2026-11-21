#!/bin/bash
echo "🚀 Granado Espada M - Render Fixed"
echo "PORT: $PORT"
echo "Checking requirements..."

if [ -f "requirements.txt" ]; then
  echo "requirements.txt found"
  cat requirements.txt
fi

# ถ้ามี TOKEN รันบอท + เว็บ
if [ ! -z "$DISCORD_TOKEN" ]; then
  echo "✅ DISCORD_TOKEN found - Running Discord bot + Web"
  python bot.py
else
  echo "⚠️ No DISCORD_TOKEN - Running Web Only"
  echo "Running: gunicorn wsgi:application --bind 0.0.0.0:$PORT"
  gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 2
fi

"""
WSGI for Render.com and other hosting
Fixed for Deploy failed status 127 error

Render Start Command ต้องใส่:
gunicorn wsgi:application --bind 0.0.0.0:$PORT

หรือ
gunicorn wsgi:app --bind 0.0.0.0:$PORT

ไม่ใช่ wsgi:application เฉยๆ (จะขึ้น command not found)

บอท Discord ต้องรันแยกบน VPS ด้วย python bot.py
ไฟล์นี้รันแค่หน้าเว็บ + API
"""
from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import json, datetime, os

BASE = Path(__file__).parent
BOSSES_FILE = BASE / "bosses.json"
TIMERS_FILE = BASE / "timers.json"

app = Flask(__name__)

def load_bosses():
    try:
        with open(BOSSES_FILE, encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def load_timers():
    try:
        with open(TIMERS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_timers(data):
    with open(TIMERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_bosses(bosses):
    with open(BOSSES_FILE, "w", encoding="utf-8") as f:
        json.dump(bosses, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    try:
        return send_from_directory(BASE, "index.html")
    except:
        return "<h1>Granado Espada M Boss Tracker - Render Fixed</h1><p>Deploy successful!</p>"

@app.route("/api/bosses")
def api_bosses():
    return jsonify(load_bosses())

@app.route("/api/timers")
def api_timers():
    return jsonify(load_timers())

@app.route("/api/status")
def api_status():
    return jsonify({
        "bosses": len(load_bosses()),
        "timers": len(load_timers()),
        "mode": "wsgi - Render fixed",
        "port": os.getenv("PORT", "8080"),
        "message": "Deploy fixed! Use gunicorn wsgi:application"
    })

@app.route("/api/bosses", methods=["POST"])
def api_add_boss():
    data = request.get_json()
    bosses = load_bosses()
    if any(b["id"] == data["id"] for b in bosses):
        return jsonify({"error": "id exists"}), 400
    bosses.append(data)
    save_bosses(bosses)
    return jsonify({"ok": True, "boss": data})

@app.route("/api/bosses/<bid>", methods=["PUT"])
def api_update_boss(bid):
    data = request.get_json()
    bosses = load_bosses()
    for i, b in enumerate(bosses):
        if b["id"] == bid:
            data["id"] = bid
            bosses[i] = data
            save_bosses(bosses)
            return jsonify({"ok": True, "boss": data})
    return jsonify({"error": "not found"}), 404

@app.route("/api/bosses/<bid>", methods=["DELETE"])
def api_delete_boss(bid):
    bosses = load_bosses()
    new_list = [b for b in bosses if b["id"] != bid]
    if len(new_list) == len(bosses):
        return jsonify({"error": "not found"}), 404
    save_bosses(new_list)
    timers = load_timers()
    timers.pop(bid, None)
    save_timers(timers)
    return jsonify({"ok": True})

@app.route("/api/kill", methods=["POST"])
def api_kill():
    data = request.get_json()
    bid = data.get("id")
    bosses = load_bosses()
    boss = next((b for b in bosses if b["id"] == bid), None)
    if not boss:
        return jsonify({"error": "boss not found"}), 404
    now = datetime.datetime.now()
    next_spawn = now + datetime.timedelta(minutes=boss["respawn_min"])
    timers = load_timers()
    timers[bid] = {"last_killed": now.isoformat(), "next_spawn": next_spawn.isoformat(), "killed_by": "web-render", "notified_10m": False, "notified_spawn": False}
    save_timers(timers)
    return jsonify({"ok": True, "next_spawn": next_spawn.isoformat()})

@app.route("/api/reset", methods=["POST"])
def api_reset():
    data = request.get_json()
    bid = data.get("id")
    timers = load_timers()
    if bid == "all":
        timers.clear()
    else:
        timers.pop(bid, None)
    save_timers(timers)
    return jsonify({"ok": True})

@app.route("/api/settime", methods=["POST"])
def api_settime():
    data = request.get_json()
    bid = data.get("id")
    next_spawn_str = data.get("next_spawn")
    try:
        ns = datetime.datetime.fromisoformat(next_spawn_str.replace("Z",""))
    except:
        return jsonify({"error": "invalid time"}), 400
    timers = load_timers()
    timers[bid] = {"last_killed": datetime.datetime.now().isoformat(), "next_spawn": ns.isoformat(), "killed_by": "web-render", "notified_10m": False, "notified_spawn": False}
    save_timers(timers)
    return jsonify({"ok": True})

@app.route("/api/timers", methods=["POST"])
def api_post_timers():
    data = request.get_json()
    save_timers(data)
    return jsonify({"ok": True})

# For gunicorn - both app and application work
app = app
application = app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)

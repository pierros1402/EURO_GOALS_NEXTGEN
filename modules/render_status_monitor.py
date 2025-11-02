# ===========================================================
# EURO_GOALS Render Status Monitor (Render-compatible version)
# ===========================================================

import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# -----------------------------------------------------------
# Load environment variables
# -----------------------------------------------------------
load_dotenv()

API_KEY = os.getenv("RENDER_API_KEY")
SERVICE_ID = os.getenv("RENDER_SERVICE_ID")
HEALTH_URL = os.getenv("RENDER_HEALTH_URL")

# -----------------------------------------------------------
# Logging
# -----------------------------------------------------------
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "render_monitor_log.txt")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def log_message(message: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

# -----------------------------------------------------------
# Health check
# -----------------------------------------------------------
def check_render_health():
    if not HEALTH_URL:
        log_message("❌ No HEALTH_URL defined in .env")
        return None, None
    try:
        res = requests.get(HEALTH_URL, timeout=10)
        return res.status_code, res.text.strip()
    except Exception as e:
        log_message(f"⚠️ Connection error: {e}")
        return None, None

# -----------------------------------------------------------
# Restart service
# -----------------------------------------------------------
def restart_render_service():
    try:
        url = f"https://api.render.com/v1/services/{SERVICE_ID}/deploys"
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {"clearCache": True}
        r = requests.post(url, headers=headers, json=data)

        if r.status_code in [200, 201]:
            log_message("🔄 Restart triggered successfully.")
        else:
            log_message(f"⚠️ Restart failed ({r.status_code}): {r.text}")
    except Exception as e:
        log_message(f"❌ Error triggering restart: {e}")

# -----------------------------------------------------------
# Helper for main app
# -----------------------------------------------------------
def get_render_status(url=None):
    """Επιστρέφει '🟢 Active' ή '🔴 Down' για το /system_summary"""
    test_url = url or HEALTH_URL
    if not test_url:
        return "⚪ Unknown"
    try:
        r = requests.get(test_url, timeout=5)
        return "🟢 Active" if r.status_code == 200 else f"🔴 {r.status_code}"
    except Exception:
        return "🔴 Down"

# -----------------------------------------------------------
if __name__ == "__main__":
    log_message("🟢 Render Status Monitor started")
    while True:
        status, content = check_render_health()
        if status == 200:
            log_message("✅ Service healthy")
        else:
            log_message(f"⚠️ Service status {status} - restarting")
            restart_render_service()
        time.sleep(900)

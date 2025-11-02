# ===========================================================
# EURO_GOALS Render Status Monitor (Cross-Platform Version)
# ===========================================================
# Ελέγχει την κατάσταση του Render service EURO_GOALS
# μέσω του Render API και της HEALTH URL.
# Καταγράφει αποτελέσματα σε logs/render_monitor_log.txt
# Χωρίς win10toast για πλήρη συμβατότητα Linux (Render)
# ===========================================================

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# -----------------------------------------------------------
# 1. Φόρτωση .env μεταβλητών
# -----------------------------------------------------------
load_dotenv()

API_KEY = os.getenv("RENDER_API_KEY")
SERVICE_ID = os.getenv("RENDER_SERVICE_ID")
HEALTH_URL = os.getenv("RENDER_HEALTH_URL")

# -----------------------------------------------------------
# 2. Ρυθμίσεις / Δομή φακέλων logs
# -----------------------------------------------------------
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "render_monitor_log.txt")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def log_message(message: str):
    """Αποθηκεύει μήνυμα με timestamp στο log αρχείο"""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

# -----------------------------------------------------------
# 3. Ενημέρωση κατάστασης Render Health
# -----------------------------------------------------------
def get_render_status(health_url=None):
    """Επιστρέφει σύντομη περιγραφή κατάστασης Render"""
    url = health_url or HEALTH_URL
    if not url:
        return "UNKNOWN"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return "🟢 Active"
        else:
            return f"🔴 Fail ({res.status_code})"
    except Exception as e:
        log_message(f"[Render Monitor] Error: {e}")
        return "⚫ Unavailable"

# -----------------------------------------------------------
# 4. Επανεκκίνηση υπηρεσίας (αν χρειάζεται)
# -----------------------------------------------------------
def restart_render_service():
    """Trigger νέου deploy μέσω Render API"""
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
        elif r.status_code == 401:
            log_message("⚠️ Restart failed: Unauthorized (401).")
        else:
            log_message(f"⚠️ Restart failed ({r.status_code}): {r.text}")
    except Exception as e:
        log_message(f"❌ Error triggering restart: {e}")

# -----------------------------------------------------------
# Τέλος
# -----------------------------------------------------------

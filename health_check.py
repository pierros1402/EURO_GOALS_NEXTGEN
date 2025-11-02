# ==============================================================
# EURO_GOALS v9.3 – Health Check Module (Final)
# ==============================================================
# Ελέγχει όλες τις βασικές υπηρεσίες της πλατφόρμας:
# - Render
# - Database
# - SmartMoney
# - Asianconnect
# - GoalMatrix
# - FootballData / SportMonks / BeSoccer
# και επιστρέφει unified JSON για το System Status Panel
# ==============================================================

import requests
import os
from datetime import datetime

# --------------------------------------------------------------
# 1️⃣  Render Health Check
# --------------------------------------------------------------
def check_render():
    url = os.getenv("RENDER_HEALTH_URL")
    if not url:
        return "PENDING"
    try:
        res = requests.get(url, timeout=5)
        return "OK" if res.status_code == 200 else f"FAIL ({res.status_code})"
    except Exception as e:
        print("[HEALTH] ⚠️ Render error:", e)
        return "FAIL"

# --------------------------------------------------------------
# 2️⃣  Database Check
# --------------------------------------------------------------
def check_database():
    db_path = "matches.db"
    try:
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            return "OK" if size > 1024 else "PENDING"
        else:
            return "FAIL (no DB)"
    except Exception as e:
        print("[HEALTH] ⚠️ Database error:", e)
        return "FAIL"

# --------------------------------------------------------------
# 3️⃣  SmartMoney Module Check
# --------------------------------------------------------------
def check_smartmoney():
    path = os.path.join("modules", "smartmoney_monitor.py")
    return "OK" if os.path.exists(path) else "FAIL"

# --------------------------------------------------------------
# 4️⃣  Asianconnect Check
# --------------------------------------------------------------
def check_asianconnect():
    url = "https://asianconnect88.com"
    try:
        res = requests.get(url, timeout=5)
        return "OK" if res.status_code == 200 else "FAIL"
    except:
        return "FAIL"

# --------------------------------------------------------------
# 5️⃣  GoalMatrix Engine Check
# --------------------------------------------------------------
def check_goalmatrix():
    url = "https://euro-goals-nextgen.onrender.com/goalmatrix_data"
    try:
        res = requests.get(url, timeout=5)
        return "OK" if res.status_code == 200 else "FAIL"
    except:
        return "FAIL"

# --------------------------------------------------------------
# 6️⃣  FootballData API
# --------------------------------------------------------------
def check_footballdata():
    key = os.getenv("FOOTBALLDATA_API_KEY")
    if not key:
        return "PENDING"
    try:
        url = "https://api.football-data.org/v4/competitions"
        headers = {"X-Auth-Token": key}
        res = requests.get(url, headers=headers, timeout=5)
        return "OK" if res.status_code == 200 else f"FAIL ({res.status_code})"
    except:
        return "FAIL"

# --------------------------------------------------------------
# 7️⃣  SportMonks API
# --------------------------------------------------------------
def check_sportmonks():
    key = os.getenv("SPORTMONKS_API_KEY")
    if not key:
        return "PENDING"
    try:
        url = f"https://api.sportmonks.com/v3/football/leagues?api_token={key}"
        res = requests.get(url, timeout=5)
        return "OK" if res.status_code == 200 else f"FAIL ({res.status_code})"
    except:
        return "FAIL"

# --------------------------------------------------------------
# 8️⃣  BeSoccer API
# --------------------------------------------------------------
def check_besoccer():
    key = os.getenv("BESOCCER_API_KEY")
    if not key:
        return "PENDING"
    try:
        url = f"https://apiclient.besoccerapps.com/scripts/api/api.php?key={key}&req=leagues"
        res = requests.get(url, timeout=5)
        return "OK" if res.status_code == 200 else f"FAIL ({res.status_code})"
    except:
        return "FAIL"

# --------------------------------------------------------------
# 9️⃣  Κεντρική Συνάρτηση
# --------------------------------------------------------------
def run_full_healthcheck():
    timestamp = datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")

    report = {
        "db": check_database(),
        "render": check_render(),
        "footballdata": check_footballdata(),
        "sportmonks": check_sportmonks(),
        "besoccer": check_besoccer(),
        "smartmoney": check_smartmoney(),
        "asianconnect": check_asianconnect(),
        "goalmatrix": check_goalmatrix(),
        "last_update": timestamp
    }

    return report

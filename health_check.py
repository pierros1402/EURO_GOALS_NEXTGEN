# ================================================================
# EURO_GOALS v9.3 – Health Check Module (Render Compatible)
# ================================================================
# Ελέγχει την κατάσταση βασικών υπηρεσιών (Render, DB, APIs)
# και επιστρέφει συνοπτικό JSON diagnostic report για Unified Monitor
# ================================================================

import requests
from datetime import datetime
import os

# ------------------------------------------------
# 1️⃣  ΕΛΕΓΧΟΣ ASIANCONNECT API
# ------------------------------------------------
def check_asianconnect():
    """Ελέγχει αν το Asianconnect API είναι διαθέσιμο."""
    url = "https://asianconnect88.com"
    try:
        res = requests.get(url, timeout=6)
        if res.status_code == 200:
            return "OK"
        else:
            return f"FAIL ({res.status_code})"
    except Exception:
        return "FAIL"

# ------------------------------------------------
# 2️⃣  ΕΛΕΓΧΟΣ RENDER SERVICE
# ------------------------------------------------
def check_render_health():
    """Ελέγχει το Render service URL από μεταβλητή περιβάλλοντος."""
    url = os.getenv("RENDER_HEALTH_URL")
    if not url:
        return "PENDING (no URL)"

    try:
        res = requests.get(url, timeout=6)
        if res.status_code == 200:
            return "OK"
        else:
            return f"FAIL ({res.status_code})"
    except Exception:
        return "FAIL"

# ------------------------------------------------
# 3️⃣  ΕΛΕΓΧΟΣ DATABASE (SQLite / PostgreSQL)
# ------------------------------------------------
def check_database():
    """Ελέγχει αν υπάρχει ενεργή σύνδεση DB (τοπικά ή σε Render)."""
    try:
        db_path = "matches.db"
        if os.path.exists(db_path):
            size = os.path.getsize(db_path)
            return "OK" if size > 1024 else "PENDING"
        else:
            return "FAIL (no DB)"
    except Exception:
        return "FAIL"

# ------------------------------------------------
# 4️⃣  ΕΛΕΓΧΟΣ SMART MONEY MODULE
# ------------------------------------------------
def check_smartmoney():
    """Ελέγχει αν το module SmartMoney είναι διαθέσιμο."""
    path = os.path.join("modules", "smartmoney_monitor.py")
    if os.path.exists(path):
        return "OK"
    else:
        return "FAIL"

# ------------------------------------------------
# 5️⃣  ΕΛΕΓΧΟΣ GOALMATRIX MODULE (αν υπάρχει)
# ------------------------------------------------
def check_goalmatrix():
    """Ελέγχει αν υπάρχει το module GoalMatrix."""
    path = os.path.join("modules", "goal_matrix.py")
    if os.path.exists(path):
        return "OK"
    else:
        return "PENDING"

# ------------------------------------------------
# 6️⃣  ΚΕΝΤΡΙΚΗ ΣΥΝΑΡΤΗΣΗ ΥΓΕΙΑΣ
# ------------------------------------------------
def run_full_healthcheck():
    """Τρέχει όλους τους ελέγχους και επιστρέφει συνολικό αποτέλεσμα."""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    components = {
        "Render Service": check_render_health(),
        "Database": check_database(),
        "SmartMoney": check_smartmoney(),
        "Asianconnect": check_asianconnect(),
        "GoalMatrix": check_goalmatrix(),
    }

    if any("FAIL" in v for v in components.values()):
        global_status = "FAIL"
        summary = "❌ Εντοπίστηκαν προβλήματα σε μία ή περισσότερες υπηρεσίες."
    elif any("PENDING" in v for v in components.values()):
        global_status = "PENDING"
        summary = "⏳ Μερικές υπηρεσίες εκκρεμούν για επιβεβαίωση."
    else:
        global_status = "OK"
        summary = "✅ Όλα λειτουργούν κανονικά."

    return {
        "status": global_status,
        "timestamp": timestamp,
        "components": components,
        "summary": summary,
        "service": "EURO_GOALS_NEXTGEN"
    }

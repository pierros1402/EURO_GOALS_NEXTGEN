# ============================================================
# EURO_GOALS v9.3.2 – Unified System Dashboard + Summary Bar
# ============================================================

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from datetime import datetime
import os

from dotenv import load_dotenv
from health_check import run_full_healthcheck
from render_status_monitor import get_render_status

# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------
load_dotenv()

APP_VERSION = "v9.3.2"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///matches.db")
AUTO_REFRESH = os.getenv("EURO_GOALS_REFRESH", "3600")
RENDER_HEALTH_URL = os.getenv("RENDER_HEALTH_URL", "")

# ------------------------------------------------------------
# FastAPI setup
# ------------------------------------------------------------
app = FastAPI(title="EURO_GOALS v9.3.2 – Unified System Dashboard")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ------------------------------------------------------------
# Database connection
# ------------------------------------------------------------
try:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
    )
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    DB_STATUS = f"Connected ({'SQLite' if 'sqlite' in DATABASE_URL else 'PostgreSQL'})"
except Exception as e:
    DB_STATUS = f"Disconnected ({str(e)})"

# ============================================================
# SYSTEM SUMMARY BAR ENDPOINT
# ============================================================
@app.get("/system_summary")
def system_summary():
    """Επιστρέφει περιληπτικά δεδομένα κατάστασης για το πάνω bar"""
    try:
        # Health
        health = run_full_healthcheck()
        render_state = get_render_status(RENDER_HEALTH_URL)

        summary = {
            "database": DB_STATUS,
            "health": f"OK (Last: {datetime.now().strftime('%H:%M')})",
            "auto_refresh": f"ON (Next in 00:{int(AUTO_REFRESH)//60:02d})",
            "smartmoney": "Monitor Active",
            "render_service": render_state,
            "version": APP_VERSION
        }
        return JSONResponse(content=summary)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ============================================================
# HEALTH ENDPOINTS (for Render / System Panels)
# ============================================================
@app.get("/health")
def health_status():
    """Επιστρέφει unified JSON με την κατάσταση όλων των modules"""
    try:
        report = run_full_healthcheck()
        return JSONResponse(content=report)
    except Exception as e:
        return JSONResponse(content={"status": "FAIL", "error": str(e)})

@app.get("/health_report", response_class=HTMLResponse)
def health_report_view(request: Request):
    """HTML πλήρης αναφορά για debugging"""
    return templates.TemplateResponse("health_report.html", {"request": request, "version": APP_VERSION})

# ============================================================
# MAIN ROUTES (UI Templates)
# ============================================================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "version": APP_VERSION})

@app.get("/system_status", response_class=HTMLResponse)
def system_status_view(request: Request):
    return templates.TemplateResponse("system_status.html", {"request": request, "version": APP_VERSION})

@app.get("/alert_history", response_class=HTMLResponse)
def alert_history_view(request: Request):
    return templates.TemplateResponse("alert_history.html", {"request": request, "version": APP_VERSION})

@app.get("/smartmoney", response_class=HTMLResponse)
def smartmoney_view(request: Request):
    return templates.TemplateResponse("smartmoney.html", {"request": request, "version": APP_VERSION})

# ============================================================
# STATIC FALLBACK (error pages)
# ============================================================
@app.exception_handler(404)
def not_found(request: Request, exc):
    return templates.TemplateResponse("index.html", {"request": request, "version": APP_VERSION})

# ============================================================
# END
# ============================================================

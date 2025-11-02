import requests
from datetime import datetime

BASE_URL = "https://eurogoals-nextgen.onrender.com"

ENDPOINTS = [
    "/health",
    "/system_status",
    "/health_report",
    "/smartmoney"
]

def test_endpoint(url):
    try:
        resp = requests.get(url, timeout=10)
        status = resp.status_code
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {url} → {status}")
        if status == 200:
            print(resp.text[:250] + "\n")
        else:
            print("⚠️ Non-200 response:", resp.text[:150], "\n")
    except Exception as e:
        print(f"❌ Error accessing {url}: {e}\n")

if __name__ == "__main__":
    print("====================================")
    print("EURO_GOALS – Endpoint Health Tester")
    print("====================================\n")

    for ep in ENDPOINTS:
        test_endpoint(BASE_URL + ep)

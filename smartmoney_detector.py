# ==============================================
# SMARTMONEY_DETECTOR MODULE – v9.3.2
# ==============================================
# Εικονική ανίχνευση "Smart Money" για σκοπούς demo.
# Επιστρέφει προσωρινά δεδομένα που χρησιμοποιούνται
# από το system_summary και το Smart Money Monitor.

from datetime import datetime
import random

def detect_smart_money():
    """
    Ανιχνεύει (προσομοιωμένα) μεταβολές αποδόσεων / όγκων
    σε ασιατικές αγορές ή μεγάλα πρωταθλήματα.
    Επιστρέφει λίστα με ύποπτα παιχνίδια.
    """
    print("[SMART MONEY] 🔍 Checking Asian market data...")

    # Τυχαία προσομοίωση αποτελεσμάτων
    sample_games = [
        {"league": "Premier League", "match": "Chelsea vs Arsenal", "movement": "1.92 → 1.78", "timestamp": datetime.now().strftime("%H:%M:%S")},
        {"league": "Bundesliga", "match": "Bayern vs Dortmund", "movement": "2.10 → 1.95", "timestamp": datetime.now().strftime("%H:%M:%S")},
        {"league": "Serie A", "match": "Napoli vs Inter", "movement": "2.25 → 2.05", "timestamp": datetime.now().strftime("%H:%M:%S")},
    ]

    # Προσομοίωση: 50% πιθανότητα να μην υπάρχουν νέα δεδομένα
    if random.choice([True, False]):
        print("[SMART MONEY] ✅ 3 matches flagged.")
        return sample_games
    else:
        print("[SMART MONEY] No movements detected.")
        return []

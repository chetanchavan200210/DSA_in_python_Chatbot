import json

from config import OUTPUT_DIR

# ----------------------------
# Tracker File
# ----------------------------
TRACKER_FILE = OUTPUT_DIR / "tracker.json"


# ----------------------------
# Load Tracker
# ----------------------------
def load_tracker():

    if TRACKER_FILE.exists():

        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return {}


# ----------------------------
# Save Tracker
# ----------------------------
def save_tracker(tracker):

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(
            tracker,
            f,
            indent=4,
            ensure_ascii=False,
        )
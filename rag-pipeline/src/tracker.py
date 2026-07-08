import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TRACKER_FILE = BASE_DIR / "outputs" / "tracker.json"


def load_tracker():
    if TRACKER_FILE.exists():
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_tracker(tracker):
    TRACKER_FILE.parent.mkdir(exist_ok=True)

    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(tracker, f, indent=4)
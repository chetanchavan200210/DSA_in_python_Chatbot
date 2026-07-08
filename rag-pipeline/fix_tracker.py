import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from tracker import load_tracker, save_tracker

tracker = load_tracker()
print("Current tracker:", tracker)

# Remove dental PDF from tracker to force re-ingestion
dental_pdf = "1_Color-Atlas-of-Dental-Medicine-Radiology (1).pdf"
if dental_pdf in tracker:
    del tracker[dental_pdf]
    print(f"Removed {dental_pdf} from tracker")
    save_tracker(tracker)
    print("Tracker updated")
else:
    print(f"{dental_pdf} not found in tracker")

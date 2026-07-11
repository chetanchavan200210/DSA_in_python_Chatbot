import json
from datetime import datetime
from pathlib import Path
import uuid


from config import OUTPUT_DIR



# --------------------------------------------------
# Tracker File
# --------------------------------------------------

TRACKER_FILE = OUTPUT_DIR / "tracker.json"



# --------------------------------------------------
# Load Tracker
# --------------------------------------------------

def load_tracker():

    if TRACKER_FILE.exists():

        with open(
            TRACKER_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    return {
        "queries": []
    }



# --------------------------------------------------
# Save Tracker
# --------------------------------------------------

def save_tracker(tracker):

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )


    with open(
        TRACKER_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            tracker,
            f,
            indent=4,
            ensure_ascii=False
        )



# --------------------------------------------------
# Add Query Log
# --------------------------------------------------

def add_query_log(
        question,
        answer,
        sources,
        retrieval_time=None,
        llm_time=None,
        status="success"
):


    tracker = load_tracker()


    log = {

        "id":
            str(uuid.uuid4()),


        "timestamp":
            datetime.now().isoformat(),


        "question":
            question,


        "answer":
            answer,


        "sources":
            sources,


        "performance":{

            "retrieval_time":
                retrieval_time,


            "llm_time":
                llm_time

        },


        "status":
            status

    }


    tracker["queries"].append(
        log
    )


    save_tracker(
        tracker
    )


    return log
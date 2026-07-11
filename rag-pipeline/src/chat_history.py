import json
from pathlib import Path
import uuid


# --------------------------------------------------
# History File
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

HISTORY_DIR = BASE_DIR / "output"

HISTORY_FILE = HISTORY_DIR / "chat_history.json"



# --------------------------------------------------
# Load All History
# --------------------------------------------------

def load_history():

    if HISTORY_FILE.exists():

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    return {}



# --------------------------------------------------
# Save All History
# --------------------------------------------------

def save_history(history):

    HISTORY_DIR.mkdir(
        exist_ok=True
    )


    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            indent=4,
            ensure_ascii=False
        )



# --------------------------------------------------
# Create Session
# --------------------------------------------------

def create_session():

    session_id = str(
        uuid.uuid4()
    )


    history = load_history()


    history[session_id] = []


    save_history(history)


    return session_id



# --------------------------------------------------
# Get Session History
# --------------------------------------------------

def get_history(session_id):

    history = load_history()


    return history.get(
        session_id,
        []
    )



# --------------------------------------------------
# Save Message
# --------------------------------------------------

def save_message(
        session_id,
        role,
        content
):

    history = load_history()


    # Automatically create session
    if session_id not in history:

        history[session_id] = []



    history[session_id].append(

        {
            "role": role,
            "content": content
        }

    )


    save_history(history)
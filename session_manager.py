import json
import os

SESSION_FILE = "sessions.json"

def save_session(host, user):
    sessions = load_sessions()
    sessions[host] = {"user": user}
    with open(SESSION_FILE, "w") as f:
        json.dump(sessions, f, indent=4)

def load_sessions():
    if not os.path.exists(SESSION_FILE):
        return {}
    with open(SESSION_FILE, "r") as f:
        return json.load(f)

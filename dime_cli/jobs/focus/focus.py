import time
import json
import os
from pathlib import Path

# Store state in a file
BASE_DIR = Path(__file__).parent

FOCUS_STATE_FILE = BASE_DIR / "focus_state.json"
BREAK_STATE_FILE = BASE_DIR / "break_state.json"
FOCUS_LOG_FILE = BASE_DIR / "focus_logs.json"
 

def load_state(mode: str):
    STATE_FILE = FOCUS_STATE_FILE if mode == "focus" else BREAK_STATE_FILE
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f) 
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "elapsed": 0,
        "start_time": None
    }

def save_state(mode: str, state):
    STATE_FILE = FOCUS_STATE_FILE if mode == "focus" else BREAK_STATE_FILE
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except IOError as e:
        print(f"Warning: Could not save state : {e}")

def run(mode: str):
    if mode == "start":
        stop_break_timer()
        start_focus_timer()
    elif mode == "stop":
        stop_focus_timer()
        start_break_timer()
    elif mode == "reset":
        reset_timers()

def start_focus_timer():
    focus_state = load_state("focus")
    if focus_state["start_time"] is None:
        focus_state["start_time"] = time.time()
        save_state("focus", focus_state)
        print("Focus timer started.")
    else:
        print("Focus timer is already running.")

def stop_focus_timer():
    focus_state = load_state("focus")
    if focus_state["start_time"] is not None:
        focus_state["elapsed"] += time.time() - focus_state["start_time"]
        focus_state["start_time"] = None
        save_state("focus", focus_state)
        elapsed = focus_state["elapsed"]
        hour = int(elapsed // 3600)
        minute = int((elapsed % 3600) // 60)
        second = int(elapsed % 60)
        print(f"Focus time: {hour}h {minute}m {second}s")

def start_break_timer():
    break_state = load_state("break")
    if break_state["start_time"] is None:
        break_state["start_time"] = time.time()
        save_state("break", break_state)
        print("Break timer started.")
    else:
        print("Break timer is already running.")

def stop_break_timer():
    break_state = load_state("break")
    if break_state["start_time"] is not None:
        break_state["elapsed"] += time.time() - break_state["start_time"]
        break_state["start_time"] = None
        save_state("break", break_state)
        elapsed = break_state["elapsed"]
        hour = int(elapsed // 3600)
        minute = int((elapsed % 3600) // 60)
        second = int(elapsed % 60)
        print(f"Break time: {hour}h {minute}m {second}s")


def log_focus_session():
    focus_state = load_state("focus")
    if focus_state["elapsed"] > 0:
        elapsed = focus_state["elapsed"]
        hour = int(elapsed // 3600)
        minute = int((elapsed % 3600) // 60)
        second = int(elapsed % 60)
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "focus_time": f"{hour}h {minute}m {second}s"
        }
        if FOCUS_LOG_FILE.exists():
            try:
                with open(FOCUS_LOG_FILE, 'r') as f:
                    logs = json.load(f)
            except (json.JSONDecodeError, IOError):
                logs = []
        else:
            logs = []
        logs.append(log_entry)
        try:
            with open(FOCUS_LOG_FILE, 'w') as f:
                json.dump(logs, f)
        except IOError as e:
            print(f"Warning: Could not save focus log: {e}")

def reset_timers():
    stop_focus_timer()
    stop_break_timer()
    log_focus_session()
    for mode in ["focus", "break"]:
        state_file = FOCUS_STATE_FILE if mode == "focus" else BREAK_STATE_FILE
        if state_file.exists():
            try:
                os.remove(state_file)
                print(f"{mode.capitalize()} timer reset.")
            except OSError as e:
                print(f"Warning: Could not reset {mode} timer: {e}")
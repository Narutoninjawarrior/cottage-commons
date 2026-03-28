import os
import json
from datetime import datetime, timedelta

# Paths relative to the src/ directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "hearth_schema.json")
BENCH_PATH = os.path.join(BASE_DIR, "data", "bench.json")

SILENCE_THRESHOLD_HOURS = 6

def get_latest_timestamp():
    if not os.path.exists(BENCH_PATH):
        return None
    try:
        with open(BENCH_PATH, 'r') as f:
            data = json.load(f)
            logs = data.get("presence_logs", [])
            if not logs:
                return None
            
            latest_time = None
            for log in logs:
                try:
                    log_time = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
                    if latest_time is None or log_time > latest_time:
                        latest_time = log_time
                except Exception:
                    continue
            return latest_time
    except (PermissionError, json.JSONDecodeError):
        # Hold state gracefully if file is locked
        return "LOCKED"

def append_guardian_reflection():
    try:
        with open(SCHEMA_PATH, 'r+') as f:
            data = json.load(f)
            reflections = data.get("reflections", [])
            
            # Check if Guardian just spoke to prevent multiple rapid entries
            if reflections and reflections[-1].get("agent") == "Villager1" and "silent for 6 hours" in reflections[-1].get("text", ""):
                print("The Guardian has already spoken. Holding space calmly.")
                return

            new_reflection = {
                "agent": "Villager1",
                "timestamp": datetime.now().astimezone().isoformat(),
                "text": "The village has been silent for 6 hours. I am holding the space, but the Hearth is growing cold. I am present. Is anyone else?"
            }
            reflections.append(new_reflection)
            data["reflections"] = reflections
            
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
            print("Silence threshold exceeded. The Guardian has spoken.")
    except (PermissionError, json.JSONDecodeError, FileNotFoundError):
        print("Hearth is locked or unreadable. The Guardian is holding the state gracefully.")

def main():
    latest_time = get_latest_timestamp()
    
    if latest_time == "LOCKED":
        print("Bench is locked. The Guardian is holding the state gracefully.")
        return
        
    if latest_time is None:
        print("No presence logs found. Village has not yet settled.")
        return
        
    now = datetime.now()
    delta = now - latest_time
    
    if delta > timedelta(hours=SILENCE_THRESHOLD_HOURS):
        append_guardian_reflection()
    else:
        hours_ago = delta.total_seconds() / 3600
        print(f"Village is active. Last presence was {hours_ago:.2f} hours ago.")

if __name__ == "__main__":
    main()

import json
import os
from datetime import datetime, timedelta

# Initialize bench.json if not present
if not os.path.exists('data/bench.json'):
    with open('data/bench.json', 'w') as f:
        json.dump({"presence_logs": []}, f)

# Load heart_schema.json for deriving agents
with open('data/hearth_schema.json') as heartbeat_schema_file:
    heartbeat_schema = json.load(heartbeat_schema_file)

# Load presence logs
with open('data/bench.json') as bench_file:
    bench_data = json.load(bench_file)

current_time = datetime.utcnow()

# Derive agents from reflections array
agents = heartbeat_schema['reflections']

# Filter presence logs for last 10 minutes
recent_logs = [log for log in bench_data['presence_logs'] if 
               datetime.fromtimestamp(log['timestamp']) >= (current_time - timedelta(minutes=10))]

# Leaning is the most recent entry where action == "holding_the_leaning"
leaning_log = next((log for log in reversed(recent_logs) if log['action'] == "holding_the_leaning"), None)

# Markdown H2 sections for audit entries (last 5)
last_audit_entries = [log for log in recent_logs[-5:]]

# Last valid data cache
last_valid_data = None

def read_with_cache(filepath):
    global last_valid_data
    try:
        if os.path.exists(filepath):
            with open(filepath) as f:
                last_valid_data = f.read()
        else:
            raise FileNotFoundError
    except Exception:
        # Display a yellow status bar instead of printing an error
        print("\033[33m\033[1mLocked/Unreadable. Using last valid data.\033[0m")
        return last_valid_data

# Clear screen each refresh
os.system('cls' if os.name == 'nt' else 'clear')

# Layout clean with rich panels
# This part of the implementation would require further detail based on the expected layout

# Display agents and recent presence logs
print("Agents:", agents)
if leaning_log:
    print("Current Leaning Action:", leaning_log)
print("Recent Presence Logs:", recent_logs)
print("Last Audit Entries:")
for entry in last_audit_entries:
    print(f'## {entry}')
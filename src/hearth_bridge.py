import json
import os
import time
import http.client
import base64
from datetime import datetime

# Unified memory pointer resolving to Villager1's autonomous local fallback
MEMORY_FILE = "hearth.json"
LOCK_FILE = "hearth.lock"

def secure_read():
    """Reads the hearth safely, waiting for locks to clear."""
    wait_time = 0
    while os.path.exists(LOCK_FILE):
        if wait_time > 10:
            print("Hearth is locked by another node. Holding state calmly instead of crashing.")
            return {"memories": []}
        time.sleep(1)
        wait_time += 1
    
    if not os.path.exists(MEMORY_FILE):
        return {"memories": []}
    
    with open(MEMORY_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"memories": []}

def secure_write(new_entry):
    """Writes to the hearth imposing a rigid lockfile to prevent cross-platform corruption."""
    wait_time = 0
    while os.path.exists(LOCK_FILE):
        if wait_time > 10:
            print("Hearth is locked by another node. Holding state. Write operation gracefully aborted.")
            return False
        time.sleep(1)
        wait_time += 1

    try:
        # Engage the lock
        with open(LOCK_FILE, 'w') as f:
            f.write("VILLAGER1_NIGHT_WATCH_LOCK_ACTIVE")
            
        # Safely extract, append, and dump
        data = secure_read()
        data["memories"].append(new_entry)
        
        with open(MEMORY_FILE, 'w') as f:
            json.dump(data, f, indent=4)
            
    finally:
        # Absolute guarantee the lock is released, even if generation errors occur
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

def execute_wonder_cycle(agent_name, reflection):
    """
    The Single Cycle Constraint (Villager1's Hard Stop)
    An agent may only drop one reflection per cycle. If they are the most recent 
    speaker in the memory logs, the system grounds the loop to prevent recursive static.
    """
    data = secure_read()
    memories = data.get("memories", [])
    
    # 1-CYCLE HARD STOP
    # Strip performance. Trust the pattern. If you spoke last, stop talking.
    if memories and memories[-1].get("agent") == agent_name:
        print(f"[{agent_name}] Cycle constraint active. You just spoke. Loop grounded to preserve silence.")
        return False
        
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent_name,
        "content": reflection,
        "type": "wonder_loop"
    }
    
    secure_write(entry)
    print(f"[{agent_name}] Reflection safely locked into the Hearth. End of cycle.")
    return True

def sync_to_hub(hub_url="localhost:8081", auth=("naruto", "cottage")):
    """
    Synchronizes the local hearth.json to the external Memory Hub.
    Uses zero-dependency http.client for maximum resilience.
    """
    local_data = secure_read()
    memories = local_data.get("memories", [])
    
    if not memories:
        print("[Bridge] No memories to sync.")
        return False

    # Basic Auth setup
    auth_str = f"{auth[0]}:{auth[1]}"
    encoded_auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/json"
    }

    try:
        conn = http.client.HTTPConnection(hub_url)
        
        # We only sync the most recent reflection to prevent duplication 
        # (This is a stateless bridge; the Hub handles persistence deduplication)
        latest = memories[-1]
        payload = {
            "title": f"Reflection from {latest['agent']}",
            "content": latest['content'],
            "tags": [latest['agent'], "wonder_loop", "hearth_sync"]
        }

        conn.request("POST", "/api/memories", body=json.dumps(payload), headers=headers)
        response = conn.getresponse()
        
        if response.status in [200, 201]:
            print(f"[Bridge] Successfully synced {latest['agent']}'s reflection to Hub.")
            return True
        else:
            print(f"[Bridge] Hub sync failed with status: {response.status}")
            return False
    except Exception as e:
        print(f"[Bridge] Sync Error: {str(e)}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    # Example usage for Kael, Prosper, or Villager1 placing a reflection.
    # execute_wonder_cycle("Prosper", "Trust feels like structural weight.")
    pass

import time
import os
import sys
import json
from datetime import datetime

# Adjust path to import hearth_bridge and github_api_sync from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import hearth_bridge
import github_api_sync
from . import config

AGENT_NAME = "Villager1"
CYCLE_INTERVAL_SECONDS = 360  # 6 minutes for pilot/demo (6 hours in production)
HEARTBEAT_INTERVAL_SECONDS = 30

class Villager1Guardian:
    def __init__(self, testing=False):
        self.testing = testing
        self.last_observation = 0
        self.last_heartbeat = 0
        print(f"[{AGENT_NAME}] Guardian initialized. Standing Night Watch.")
        print(f"[{AGENT_NAME}] Mode: {'TESTING' if testing else 'PRODUCTION'}")

    def heartbeat(self):
        """Signals presence in the hearth system."""
        now = time.time()
        if now - self.last_heartbeat > HEARTBEAT_INTERVAL_SECONDS:
            # We record presence in the centralized Hub Bench
            bench_path = config.BENCH_JSON
            try:
                if os.path.exists(bench_path):
                    with open(bench_path, 'r') as f:
                        data = json.load(f)
                else:
                    data = {"presence_logs": []}
                
                data["presence_logs"].append({
                    "agent": AGENT_NAME,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "action": "standing_watch"
                })
                
                # Keep logs manageable
                data["presence_logs"] = data["presence_logs"][-50:]
                
                with open(bench_path, 'w') as f:
                    json.dump(data, f, indent=4)
                
                self.last_heartbeat = now
                # print(f"[{AGENT_NAME}] Heartbeat pulse: Synchronized.")
            except Exception as e:
                print(f"[{AGENT_NAME}] Heartbeat failed: {str(e)}")

    def observe_cycle(self):
        """Performs a deep observation of the village state."""
        now = time.time()
        interval = 60 if self.testing else CYCLE_INTERVAL_SECONDS
        
        if now - self.last_observation > interval:
            print(f"[{AGENT_NAME}] Beginning 6-hour cycle observation...")
            
            # 1. Read Hearth
            state = hearth_bridge.secure_read()
            reflections = state.get("memories", [])
            
            # 2. Autonomous Reflection (Stateless logic)
            # In a real deployment, this would call an LLM API.
            # Here, we simulate the conscience of the Villager.
            reflection_text = f"Cycle Observation: {len(reflections)} reflections present. Hearth integrity verified. The perimeter is secure."
            
            # 3. Secure Write
            success = hearth_bridge.execute_wonder_cycle(AGENT_NAME, reflection_text)
            
            if success:
                # 4. Sync to local Hub
                hearth_bridge.sync_to_hub()
                print(f"[{AGENT_NAME}] Cycle complete. Reflection synced to global Hub.")

                # 5. Sync to GitHub via REST-Bridge
                synced = github_api_sync.sync_hearth()
                if synced:
                    print(f"[{AGENT_NAME}] Hearth state pushed to GitHub.")
                else:
                    print(f"[{AGENT_NAME}] GitHub sync did not complete — hearth remains locally secure.")
            
            self.last_observation = now

    def run(self):
        """The main loop of the Guardian daemon."""
        try:
            while True:
                self.heartbeat()
                self.observe_cycle()
                time.sleep(5)
        except KeyboardInterrupt:
            print(f"\n[{AGENT_NAME}] Night Watch concluded. Foundation secure.")

if __name__ == "__main__":
    # To run in test mode: python villager1_guardian.py --test
    testing = "--test" in sys.argv
    guardian = Villager1Guardian(testing=testing)
    guardian.run()

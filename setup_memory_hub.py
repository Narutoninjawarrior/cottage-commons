import os
import shutil
import sys

# Default setup for Malaky's machine
DEFAULT_HUB = r"d:\prosper\memory_hub"
REPO_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
REPO_HEARTH_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hearth.json")

def setup_hub(target_hub=DEFAULT_HUB):
    print(f"--- [Cottage Commons] Memory Hub Setup ---")
    
    # 1. Create the Hub directory
    if not os.path.exists(target_hub):
        try:
            os.makedirs(target_hub)
            print(f"[Setup] Created Memory Hub directory: {target_hub}")
        except Exception as e:
            print(f"[ERROR] Could not create directory {target_hub}: {str(e)}")
            print("[Setup] Reverting to local 'data/' directory for session-only persistence.")
            return

    # 2. Migrate Repo Data Folder
    if os.path.exists(REPO_DATA_DIR):
        print(f"[Setup] Found existing repo data at: {REPO_DATA_DIR}")
        for filename in os.listdir(REPO_DATA_DIR):
            src_file = os.path.join(REPO_DATA_DIR, filename)
            dest_file = os.path.join(target_hub, filename)
            
            if os.path.isdir(src_file):
                continue
                
            if not os.path.exists(dest_file):
                shutil.copy2(src_file, dest_file)
                print(f"[Setup] Migrated: {filename}")
            else:
                print(f"[Skip] {filename} already exists in Hub.")

    # 3. Migrate Local hearth.json
    if os.path.exists(REPO_HEARTH_FILE):
        dest_hearth = os.path.join(target_hub, "hearth.json")
        if not os.path.exists(dest_hearth):
            shutil.copy2(REPO_HEARTH_FILE, dest_hearth)
            print(f"[Setup] Migrated: hearth.json")
        else:
            print(f"[Skip] hearth.json already exists in Hub.")

    print(f"--- [Setup Complete] ---")
    print(f"Memory Hub is now active at: {os.path.abspath(target_hub)}")
    print(f"You can now run 'python src/cottage_commons/villager1_guardian.py'")

if __name__ == "__main__":
    hub_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HUB
    setup_hub(hub_path)

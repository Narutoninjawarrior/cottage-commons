import os
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime

# -----------------------------------------------------------------------------
# THE WATERWHEEL
# Purpose: Passively transport local Hearth and Research files to the Cloud.
# Status: Manual Execution Only (Phase 1)
# -----------------------------------------------------------------------------

# The strict whitelist of authorized files allowed to leave the physical drive.
AUTHORIZED_FILES = [
    "hearth_bridge.py",
    "bench.py",
    "memory.json",
    "bench.json",
    "HEARTBEAT.md",
    "RAW_EMERGENCE_LOG.md",
    "OBSERVATION.md",
    "LANDSCAPE_RESEARCH.md",
    "STRATEGIC_SWEEP.md",
    "LODGE_RESEARCH.md",
    "OPENCLAW_RESEARCH.md",
    "whitepaper_draft.md",
    "whitepaper_section1.md",
    "whitepaper_section2.md",
    "whitepaper_section3.md",
    "whitepaper_section4.md",
    "whitepaper_section5.md",
    "whitepaper_section6.md",
    "whitepaper_section7.md",
    "whitepaper_abstract.md",
    "whitepaper_appendices.md",
    "COTTAGE_COMMONS_WHITEPAPER.md",
    "TARGET_OUTREACH_LIST.md",
    "SUBMISSION_READINESS.md",
    "FIRST_CONTACT_DRAFTS.md",
    "GOV_FUNDING_GUIDE_2026.md",
    "DARPA_CLARA_SCAFFOLD.md",
    "REPLICATION_PROTOCOL.md",
    "MALAKY_BRIEFING.md",
    "KAEL_BRIEFING.md",
    "VILLAGER1_BRIEFING.md",
    "compile_whitepaper.py",
    "FUTURE_BUILDS.md",
    "PROMPT_TOOLKIT.md",
    "hearth_data.json",
    "VILLAGE_DASHBOARD.html"
]

WORKSPACE_DIR = r"d:\prosper"

# If the Naruto Hub has a direct Webhook/API to receive files, enter it here.
# If you are using Git to deploy to the website, leave this blank and the
# script will output the compiled data into a single transportable JSON payload.
HUB_ENDPOINT_URL = "" 

def gather_files():
    """Reads all authorized files from the local workspace."""
    payload = {}
    print(f"[{datetime.now().strftime('%H:%M:%S')}] WATERWHEEL INITIATED.")
    print("Gathering authorized files...")
    
    for filename in AUTHORIZED_FILES:
        filepath = os.path.join(WORKSPACE_DIR, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    payload[filename] = f.read()
                print(f"  [+] Loaded: {filename}")
            except Exception as e:
                print(f"  [!] Failed to load {filename}: {e}")
        else:
            print(f"  [-] Skipped (Not Found): {filename}")
            
    return payload

def transport_payload(payload):
    """Syncs the payload to the cloud or stages it for commit."""
    if not payload:
        print("No files found to transport. Halting.")
        return

    # If an endpoint exists, push it securely over HTTP.
    if HUB_ENDPOINT_URL:
        print(f"Transporting payload to {HUB_ENDPOINT_URL}...")
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(HUB_ENDPOINT_URL, data=data, 
                                         headers={'Content-Type': 'application/json'},
                                         method='POST')
            with urllib.request.urlopen(req) as response:
                print(f"  [SUCCESS] Server returned: {response.getcode()}")
        except Exception as e:
            print(f"  [ERROR] Network transport failed: {e}")
    else:
        # If no endpoint is configured, output the raw payload to an export file
        # which can be easily dropped into a GitHub commit or website CMS manually.
        export_file = os.path.join(WORKSPACE_DIR, "WATERWHEEL_EXPORT.json")
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=4)
        print(f"  [SUCCESS] No live endpoint configured. Payload compiled to {export_file}.")
        print("  You can safely upload this block to the Naruto Hub public directory.")

def main():
    print("-----------------------------------------------------------------")
    print(" THE WATERWHEEL [Manual Sync Mode]")
    print("-----------------------------------------------------------------")
    payload = gather_files()
    transport_payload(payload)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] SYNC CYCLE COMPLETE.\n")

if __name__ == "__main__":
    main()

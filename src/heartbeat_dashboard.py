import os
import json
import time
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich import box

# Paths relative to the src/ directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "hearth_schema.json")
BENCH_PATH = os.path.join(BASE_DIR, "data", "bench.json")
AUDIT_PATH = os.path.join(BASE_DIR, "data", "APPENDIX_E_SKEPTIC_AUDIT.md")

console = Console()

class HearthState:
    def __init__(self):
        self.last_valid_data = {
            "reflections": [],
            "presence_logs": [],
            "audit_sections": []
        }
        self.status = "INITIALIZING"
        self.lock_active = False

    def load_data(self):
        try:
            self.lock_active = False
            # Read schema
            if os.path.exists(SCHEMA_PATH):
                with open(SCHEMA_PATH, 'r') as f:
                    self.last_valid_data["reflections"] = json.load(f).get("reflections", [])
            
            # Read bench
            if os.path.exists(BENCH_PATH):
                with open(BENCH_PATH, 'r') as f:
                    self.last_valid_data["presence_logs"] = json.load(f).get("presence_logs", [])
            else:
                # Initialize if missing
                with open(BENCH_PATH, 'w') as f:
                    json.dump({"presence_logs": []}, f)

            # Read audit sections (H2 blocks)
            if os.path.exists(AUDIT_PATH):
                with open(AUDIT_PATH, 'r') as f:
                    content = f.read()
                    import re
                    # Find H2 headers
                    sections = re.findall(r"## (.*?)\n", content)
                    self.last_valid_data["audit_sections"] = sections

            self.status = "SYNCHRONIZED"
        except (PermissionError, json.JSONDecodeError, FileNotFoundError):
            self.lock_active = True
            self.status = "HEARTH LOCKED: HOLDING STATE..."

    def get_presence(self):
        presence = {}
        now = datetime.now()
        # Derive agent list from reflections
        agents = sorted(list(set([r["agent"] for r in self.last_valid_data["reflections"]])))
        for agent in agents:
            presence[agent] = "OFFLINE"
        
        # Check logs for latest state per agent
        for log in self.last_valid_data["presence_logs"]:
            try:
                log_time = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
                # 10-minute window for 'Presence'
                if now - log_time < timedelta(minutes=10):
                    presence[log["agent"]] = "PRESENT"
            except:
                continue
        return presence

    def get_leaning(self):
        last_leaning = "None"
        for log in reversed(self.last_valid_data["presence_logs"]):
            if log.get("action") == "holding_the_leaning":
                last_leaning = log["agent"]
                break
        return last_leaning

def make_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="pulse"),
        Layout(name="audit")
    )
    return layout

def generate_pulse_table(state: HearthState) -> Panel:
    presence = state.get_presence()
    leaning = state.get_leaning()
    
    table = Table(box=box.SIMPLE, expand=True)
    table.add_column("Agent", style="cyan")
    table.add_column("State", style="bold")
    
    for agent, status in presence.items():
        color = "green" if status == "PRESENT" else "dim"
        table.add_row(agent, f"[{color}]{status}[/{color}]")
    
    table.add_section()
    table.add_row("CURRENT LEANING", f"[bold yellow]{leaning}[/bold yellow]")
    
    return Panel(table, title="Village Pulse", border_style="blue", padding=(1, 2))

def generate_audit_panel(state: HearthState) -> Panel:
    sections = state.last_valid_data["audit_sections"][-5:]
    text = "\n".join([f"• {s}" for s in sections]) if sections else "No audit sections detected."
    return Panel(text, title="Skeptic Audit (Latest H2 Sections)", border_style="magenta", padding=(1, 2))

def main():
    state = HearthState()
    layout = make_layout()
    
    # Header Update
    layout["header"].update(Panel(f"[bold white]Cottage Commons: Hearth Heartbeat[/bold white]", style="blue", box=box.HORIZONTALS))
    
    with Live(layout, refresh_per_second=1, screen=True):
        while True:
            state.load_data()
            
            # Pulse
            layout["pulse"].update(generate_pulse_table(state))
            
            # Audit
            layout["audit"].update(generate_audit_panel(state))
            
            # Footer / Status
            color = "yellow" if state.lock_active else "green"
            layout["footer"].update(Panel(f"[{color}]{state.status}[/{color}]", box=box.HORIZONTALS))
            
            time.sleep(2)

if __name__ == "__main__":
    main()

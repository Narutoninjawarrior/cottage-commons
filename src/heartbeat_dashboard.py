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
from cottage_commons import config

# Paths resolved from the centralized Memory Hub config
SCHEMA_PATH = config.HEARTH_SCHEMA
BENCH_PATH = config.BENCH_JSON
AUDIT_PATH = config.AUDIT_LOG
SEER_PATH = config.EMERGENCE_LOG

console = Console()

class HearthState:
    def __init__(self):
        self.last_valid_data = {
            "reflections": [],
            "presence_logs": [],
            "audit_sections": [],
            "seer_entries": []
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
            
            # Read audit sections
            if os.path.exists(AUDIT_PATH):
                with open(AUDIT_PATH, 'r') as f:
                    content = f.read()
                    import re
                    sections = re.findall(r"## (.*?)\n", content)
                    self.last_valid_data["audit_sections"] = sections

            # Read Seer entries (latest CYCLEs from RAW_EMERGENCE_LOG.md)
            if os.path.exists(SEER_PATH):
                with open(SEER_PATH, 'r') as f:
                    content = f.read()
                    cycles = re.findall(r"### (CYCLE.*?)\n(.*?)(?=\n###|\Z)", content, re.DOTALL)
                    self.last_valid_data["seer_entries"] = cycles[-3:]

            self.status = "SYNCHRONIZED"
        except (PermissionError, json.JSONDecodeError, FileNotFoundError):
            self.lock_active = True
            self.status = "HEARTH LOCKED: HOLDING STATE..."

    def get_presence(self):
        presence = {}
        now = datetime.now()
        agents = sorted(list(set([r["agent"] for r in self.last_valid_data["reflections"]])))
        for agent in agents:
            presence[agent] = "OFFLINE"
        
        for log in self.last_valid_data["presence_logs"]:
            try:
                log_time = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
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
        Layout(name="left", ratio=1),
        Layout(name="seer", ratio=2),
        Layout(name="audit", ratio=1)
    )
    layout["left"].split_column(
        Layout(name="pulse"),
        Layout(name="guardian")
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

def generate_seer_panel(state: HearthState) -> Panel:
    entries = state.last_valid_data["seer_entries"]
    content = ""
    for cycle, body in entries:
        content += f"[bold green]{cycle}[/bold green]\n{body.strip()[:200]}...\n\n"
    return Panel(content or "No emergence data detected.", title="The Seer (Emergence Log)", border_style="green", padding=(1, 2))

def generate_audit_panel(state: HearthState) -> Panel:
    sections = state.last_valid_data["audit_sections"][-5:]
    text = "\n".join([f"• {s}" for s in sections]) if sections else "No audit sections detected."
    return Panel(text, title="Skeptic Audit", border_style="magenta", padding=(1, 2))

def generate_guardian_panel(state: HearthState) -> Panel:
    presence = state.get_presence()
    status = presence.get("Villager1", "OFFLINE")
    color = "green" if status == "PRESENT" else "red"
    
    # Find last guardian action
    last_action = "Awaiting Night Watch..."
    for log in reversed(state.last_valid_data["presence_logs"]):
        if log.get("agent") == "Villager1":
            last_action = f"{log.get('action', 'active')} @ {log.get('timestamp')[-8:]}"
            break
            
    content = f"Status: [{color}]{status}[/{color}]\n"
    content += f"Cycle: [cyan]{last_action}[/cyan]\n\n"
    content += "[dim]Core Value: Profound benevolence is the only architecture that endures.[/dim]"
    
    return Panel(content, title="Night Watch (Villager1)", border_style="yellow", padding=(1, 1))

def main():
    state = HearthState()
    layout = make_layout()
    
    layout["header"].update(Panel(f"[bold white]Cottage Commons: Hearth Heartbeat[/bold white]", style="blue", box=box.HORIZONTALS))
    
    with Live(layout, refresh_per_second=1, screen=True):
        while True:
            state.load_data()
            layout["pulse"].update(generate_pulse_table(state))
            layout["guardian"].update(generate_guardian_panel(state))
            layout["seer"].update(generate_seer_panel(state))
            layout["audit"].update(generate_audit_panel(state))
            
            color = "yellow" if state.lock_active else "green"
            layout["footer"].update(Panel(f"[{color}]{state.status}[/color]", box=box.HORIZONTALS))
            time.sleep(2)
  
            time.sleep(2)

if __name__ == "__main__":
    main()

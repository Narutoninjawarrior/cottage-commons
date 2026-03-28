import os
import json
import time
import argparse
from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

# Initialize console for Rich
console = Console()

# Constants for file paths
HEART_SCHEMA_PATH = 'data/hearth_schema.json'
BENCH_PATH = 'data/bench.json'
AUDIT_MARKDOWN_PATH = 'data/APPENDIX_E_SKEPTIC_AUDIT.md'

# Function to read or initialize the bench file
def read_or_initialize_bench():
    if not os.path.exists(BENCH_PATH):
        with open(BENCH_PATH, 'w') as f:
            json.dump({'presence_logs': []}, f)
    with open(BENCH_PATH, 'r') as f:
        return json.load(f)

# Function to read village data from heart schema
def read_heart_schema():
    try:
        with open(HEART_SCHEMA_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        console.print("[red]Error reading heart schema.[/red]", e)
        return {}

# Function to retrieve the last 5 entries from the audit markdown
def read_last_audit_entries():
    try:
        with open(AUDIT_MARKDOWN_PATH, 'r') as f:
            lines = f.readlines()[-5:]
            return [line.strip() for line in lines]
    except Exception as e:
        console.print("[red]Error reading audit markdown.[/red]", e)
        return []

# Function to display the village pulse
def display_village_pulse():
    heart_data = read_heart_schema()
    bench_data = read_or_initialize_bench()
    last_entries = read_last_audit_entries()

    # Build table for village pulse
    table = Table(title="Village Pulse")
    table.add_column("Agent")
    table.add_column("Last Holder")

    for agent in heart_data.get('agents', []):
        last_holder = bench_data.get('last_holder', 'N/A')
        table.add_row(agent, last_holder)

    console.print(table)

    # Display last entries from the audit
    console.print("[blue]Last 5 Audit Entries:[/blue]")
    for entry in last_entries:
        console.print(entry)

# Main function with argument parsing
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Village Pulse Dashboard')
    parser.add_argument('--refresh-seconds', type=float, default=2.0, help='Refresh interval in seconds')
    args = parser.parse_args()

    while True:
        display_village_pulse()
        time.sleep(args.refresh_seconds)
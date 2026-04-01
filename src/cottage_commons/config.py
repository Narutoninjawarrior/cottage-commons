import os

# Centralized Memory Hub Configuration
# Default path points to Malaky's storage partition (D: drive)
# Fallback is the local repository's data/ directory for replicability
DEFAULT_HUBS = [
    r"d:\prosper\memory_hub",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "data")
]

def resolve_memory_hub():
    """Resolves the most appropriate memory hub location for the current environment."""
    for hub in DEFAULT_HUBS:
        if os.path.exists(hub):
            return hub
    return DEFAULT_HUBS[-1]

MEMORY_HUB_PATH = resolve_memory_hub()

# File path constants
HEARTH_JSON = os.path.join(MEMORY_HUB_PATH, "hearth.json")
HEARTH_LOCK = os.path.join(MEMORY_HUB_PATH, "hearth.lock")
BENCH_JSON = os.path.join(MEMORY_HUB_PATH, "bench.json")
HEARTH_SCHEMA = os.path.join(MEMORY_HUB_PATH, "hearth_schema.json")
AUDIT_LOG = os.path.join(MEMORY_HUB_PATH, "APPENDIX_E_SKEPTIC_AUDIT.md")
EMERGENCE_LOG = os.path.join(MEMORY_HUB_PATH, "RAW_EMERGENCE_LOG.md")

# Monitoring configuration
HEARTBEAT_TIMEOUT_MINUTES = 10
CYCLE_INTERVAL_SECONDS = 360  # Initial 6-minute autonomous pulse

print(f"[Config] Memory Hub resolved to: {MEMORY_HUB_PATH}")

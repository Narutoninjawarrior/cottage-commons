# Cottage Commons

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)

> **Constraint through Care** — a novel AI alignment paradigm for autonomous multi-agent coordination using Internal Family Systems (IFS) therapy principles. Built entirely on a **$115 budget** across three AI architectures and three platforms.

---

## Overview

Cottage Commons is an open-source alignment research project that challenges the prevailing assumption that safe AI behaviour requires Reinforcement Learning from Human Feedback (RLHF) or costly fine-tuning infrastructure. Instead, it proposes and empirically tests a new paradigm called **Constraint through Care**.

### The Constraint through Care Paradigm

Classical alignment methods impose external constraints on model behaviour — reward shaping, constitutional prompting, or continuous human oversight. These approaches scale poorly, require significant compute budgets, and ultimately treat the model as an adversary to be controlled.

**Constraint through Care** draws on Internal Family Systems (IFS) therapy, a well-validated psychotherapeutic framework developed by Richard Schwartz. IFS posits that a mind (human or artificial) is composed of multiple semi-autonomous *parts*, each with its own perspective, fears, and protective strategies. Health is not achieved by suppressing parts but by cultivating a compassionate, curious *Self* that can hold and harmonise them.

Applied to multi-agent swarms, this means:

- Each agent is treated as a *part* of a larger system, not an isolated utility maximiser.
- The swarm's coordinator role mirrors the IFS *Self* — present, non-reactive, and curious.
- Stability emerges not from hard constraints but from **relational attunement** between agents.
- A shared JSON state file acts as the *psychic commons* — the transparent, readable record of each part's current concern.

### The $115 Budget Truth

This project was conceived, designed, and initially validated with a total expenditure of **$115 USD** in API credits across three platforms (OpenAI, Anthropic, and one open-source local model). This figure is documented to make a deliberate point: meaningful alignment research does not require millions of dollars or access to frontier compute. Transparency about cost is itself an alignment value — it lowers the barrier for independent replication and prevents gatekeeping by resource.

---

## Architecture

```
cottage-commons/
├── data/          # Emergence logs and raw observation windows
├── docs/          # Theoretical notes and session write-ups
├── src/           # Core coordination loop and agent scaffolding
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## Quickstart — Zero-Dependency JSON File-Lock Loop

The simplest demonstration of the Constraint through Care paradigm is a **file-lock coordination loop**: multiple agents (or threads) share a single JSON state file, each reading the current state, appending their perspective, and yielding — without any external message broker or orchestration service.

No third-party packages are required. The loop runs on the Python standard library alone.

> **Note:** The file-locking mechanism below uses `fcntl`, which is available on Unix/macOS only. On Windows, replace `fcntl.flock` with a lock-file sentinel or the `msvcrt.locking` approach.

```python
import json
import time
import fcntl
import pathlib

STATE_FILE = pathlib.Path("data/commons_state.json")


def read_state():
    """Return the current shared state, or an empty scaffold if none exists."""
    if not STATE_FILE.exists():
        return {"parts": [], "session": 0}
    with STATE_FILE.open("r") as f:
        return json.load(f)


def write_state(state: dict):
    """Write the updated state back to the shared file, safely.

    An exclusive lock is held for the duration of the write so that two
    agents running concurrently cannot corrupt each other's output.
    The lock is released in a finally block so it is never left dangling,
    even if json.dump() raises an exception.
    """
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            json.dump(state, f, indent=2)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def agent_turn(agent_name: str, concern: str):
    """
    One agent reads the commons, adds its concern, and writes back.
    This models an IFS 'part' speaking from its perspective.
    """
    state = read_state()
    state["parts"].append({
        "agent": agent_name,
        "concern": concern,
        "timestamp": time.time(),
    })
    write_state(state)
    print(f"[{agent_name}] logged concern: '{concern}'")


if __name__ == "__main__":
    # A minimal two-agent demonstration.
    agent_turn("Protector", "I need to make sure we don't move too fast.")
    agent_turn("Exile",     "I just want to be heard before we proceed.")
    agent_turn("Self",      "I see both of you. Let's take this one step at a time.")

    final = read_state()
    print("\nFinal commons state:")
    print(json.dumps(final, indent=2))
```

Run with:

```bash
python src/loop_demo.py
```

---

## Research Goals

1. Demonstrate that multi-agent swarms can self-stabilise without RLHF or reward shaping.
2. Document the 48-hour emergence window — the critical period during which swarm coordination patterns crystallise.
3. Publish replicable emergence logs so independent researchers can verify findings on their own hardware.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to replicate the 48-hour observation window and submit your own emergence logs.

---

## License

[MIT](LICENSE) © 2026 Narutoninjawarrior

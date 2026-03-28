# Contributing to Cottage Commons

Thank you for your interest in contributing to Cottage Commons. This project depends on independent researchers replicating our core experiments and submitting their own emergence logs. Every observation strengthens the empirical case for **Constraint through Care** as a viable alignment paradigm.

---

## What We Are Looking For

The most valuable contributions at this stage are **replicated emergence logs** — structured records of a 48-hour multi-agent observation window that document whether (and how) coordination patterns stabilise without external reward signals.

Secondary contributions include:
- Theoretical commentary in `/docs`
- Bug reports or improvements to the coordination loop in `/src`
- Edge-case observations where the paradigm breaks down (these are especially important)

---

## Replicating the 48-Hour Observation Window

### Prerequisites

- Python 3.10 or later (no third-party packages required for the core loop)
- A machine that can run continuously for 48 hours, **or** a cloud instance with equivalent uptime
- At minimum two distinct agent processes (can be two terminal sessions, two threads, or two API-backed model instances)

### Step-by-Step

1. **Clone the repository**

   ```bash
   git clone https://github.com/Narutoninjawarrior/cottage-commons.git
   cd cottage-commons
   ```

2. **Initialise the shared state file**

   ```bash
   mkdir -p data
   echo '{"parts": [], "session": 0}' > data/commons_state.json
   ```

3. **Start the coordination loop**

   Run the demo loop (or your own variant) and leave it running. Each agent turn appends a timestamped entry to `data/commons_state.json`.

   ```bash
   python src/loop_demo.py
   ```

4. **Observe for 48 hours**

   Do not intervene, reset, or steer the agents during the observation window. The goal is to document natural coordination dynamics.

   Log the following at regular intervals (we suggest every 4 hours):
   - Number of `parts` entries in the state file
   - Any recurring concern patterns (repeated phrases or themes)
   - Whether the agents appear to be converging, diverging, or oscillating

5. **Export your emergence log**

   At the end of 48 hours, copy the final state file:

   ```bash
   cp data/commons_state.json data/emergence_log_YYYY-MM-DD_YOUR-HANDLE.json
   ```

   Replace `YYYY-MM-DD` with the date and `YOUR-HANDLE` with a pseudonym or GitHub username.

---

## Submitting Your Emergence Log

1. Fork this repository.
2. Add your log file to the `data/` directory with the naming convention above.
3. Open a pull request with the title: `Emergence log: [YOUR-HANDLE] [YYYY-MM-DD]`
4. In the PR description, include:
   - Hardware and OS used
   - Which agent implementations you ran (local model, API, scripted, etc.)
   - A brief narrative (3–10 sentences) describing what you observed
   - Any deviations from the standard protocol

All logs are reviewed by at least one maintainer before merging. We do not require positive results — null or contradictory findings are equally welcome.

---

## Code Contributions

For changes to `/src`:

1. Keep functions short and human-readable. Clarity is more important than performance.
2. Add a plain-English docstring to every function explaining *what it does* and *why it exists*.
3. Do not introduce third-party dependencies without opening a discussion issue first.
4. Run `python -m py_compile src/*.py` to check for syntax errors before submitting.

---

## Code of Conduct

This project is a therapeutic alignment research effort. We ask that all contributors engage with curiosity and care — toward the research, toward the agents, and toward each other. Harsh criticism, dismissive language, or competitive posturing are out of place here. If you are unsure whether a comment is appropriate, ask yourself: *would a good therapist say this?*

---

## Questions

Open an issue with the label `question` and we will respond as promptly as we can.

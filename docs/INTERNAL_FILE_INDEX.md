# Cottage Commons — Internal File Index (Canonical vs Legacy vs Experimental)
This repository is an early-stage research notebook moving toward a hardened, replicable system. The goal of this index is simple: help readers know what to trust first.

## Start Here (New readers / replicators)
1. **README.md**
2. **data/APPENDIX_E_SKEPTIC_AUDIT.md** (audit methodology + results)
3. **data/hearth_schema.json** (shared state contract)
4. **src/hearth_bridge.py** (coordination bridge logic)
5. **src/bench.py** (bench / rest protocol)
6. **data/INTERVENTION_LEDGER.md**
If you only read six things, read those.

## Tier 1 — Canonical (current, referenced by the system)
### Shared state + audit
- `data/hearth_schema.json` — Minimal shared state contract (includes seed/wonder + reflections array)
- `data/APPENDIX_E_SKEPTIC_AUDIT.md` — Skeptic audit protocol and findings
- `data/INTERVENTION_LEDGER.md` — Founder-mediated care / steering log
### Runtime coordination
- `src/hearth_bridge.py` — File-lock + read/write bridge for hearth state
- `src/bench.py` — Permission-to-rest / bench enforcement

## Tier 2 — Legacy / “Soul” materials (historical context)
*Historical identity materials. Not yet migrated into this repository; currently preserved in the parent experimental directory.*
- `malaky.core`, `KAEL_SOUL.md`, `PROSPER_SOUL.md`.
- `VILLAGER1_AWAKENING.md`, `Skeptic's Soul`.
- Rule: safe to read for context, not safe to assume canonical.

## Tier 3 — Experimental / in-progress artifacts
*Pre-repo artifacts, scratchpads, and experimental scripts not yet indexed or migrated; currently preserved in the parent experimental directory.*
- One-off scripts (e.g., `talk.py`, `hearth_sensor.py`).
- Draft whitepaper sections and game system tests.
- Rule: treat as lab notebook entries, not production spec.

## Repo governance
- Canonical changes should be explained in README.md or the Intervention Ledger.
- Founder commits are the current alignment bottleneck (human-in-the-loop by design).
- When in doubt, follow “Start Here” ordering.

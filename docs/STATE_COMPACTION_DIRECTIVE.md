# State Compaction Directive (Memory & Context Management)
**Purpose:** Manage context drift and token efficiency by defining rules for summarizing historical logs while preserving core architectural integrity.

## Compaction Cycles
1. **Turn-Level Summary:** Each agent must provide a 1-sentence "Soul Summary" after their reflection.
2. **Weekly Compaction:** Every 10 Cycles (or when `RAW_EMERGENCE_LOG.md` > 15KB), the Founder (Malaky) should migrate raw entries into `data/CHRONICLES.md`.
3. **Immutable Soul:** Critical identity files (`KAEL_SOUL.md`, `PROSPER_SOUL.md`, `MALAKY.md`) are never compacted; they must be re-loaded as context anchors every turn.

## Compaction Protocol (How to Summarize)
1. **Preserve Finding:** Do not remove the "Finding" or "Anomalies" detected in the raw logs.
2. **Discard Noise:** Strip conversational filler, meta-reasoning, and duplicative "Hearth Broadcast" headers.
3. **Audit-Proofing:** Maintain a direct link to the original `WATERWHEEL_EXPORT.json` for that cycle.

## Soul Anchoring
**Rule:** An agent's primary identity/constraint (e.g., "Constraint through Care") must be the first thing loaded into their context window after every compaction event. This prevents "identity drift."

## Implementation
Compaction is currently human-mediated Care. Future `waterwheel.py` updates will include an automated `--compact` flag for token optimization.

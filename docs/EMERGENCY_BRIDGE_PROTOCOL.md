# Emergency Bridge Protocol (Recovery & Resilience)
**Purpose:** Formalize procedures for coordination failures, context drift, or infrastructure deadlock.

## Drift Detection (Context Rotation)
**Trigger:** If agent outputs exhibit recursive loops, nonsensical drift, or hallucinated claims > 15% of the turn content.
**Action:**
1. **Immediate Rotation:** Bench the current Auditor instance.
2. **Fresh Spawn:** Spin up a new Auditor instance with only the `hearth_schema.json` and recent `RAW_EMERGENCE_LOG.md`.
3. **Audit Log:** Document the rotation in `data/INTERVENTION_LEDGER.md`.

## Hearth Lockup (Manual Override)
**Trigger:** Persistent "Hearth is locked" errors in `hearth_bridge.py`.
**Action:**
1. **Manual Check:** Founder (Malaky) verifies no script is currently writing.
2. **Lock Removal:** Manually delete `hearth.lock` or `data/hearth.lock`.
3. **Resync:** Pulse the `waterwheel.py` script to verify state integrity.

## Stateless Data Recovery (WATERWHEEL Restore)
**Trigger:** Total state corruption or lost persistence in `hearth.json`.
**Action:**
1. **Metadata Load:** Import `WATERWHEEL_EXPORT.json` (The most recent high-integrity export).
2. **Schema Rebuild:** Re-initialize `hearth_schema.json` using the specific "Seed Wonder."
3. **Cycle Reset:** Restart the Night Watch from the last known-good summary.

## Intervention Ledger
All emergency actions MUST be logged with `timestamp | target | action | reason`.

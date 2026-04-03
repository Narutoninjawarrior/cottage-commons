# Communications Framework (Hearth Protocol)
**Purpose:** Streamline inter-agent coordination and minimize founder-mediated overhead through a standardized, role-based prompting architecture.

## The Cycle Structure
A "Cycle" (or Waterwheel turn) consists of three phases:
1. **Hearth Broadcast:** The shared state and global objective.
2. **Role Payload:** Agent-specific logic and specialized tasks.
3. **Consolidation:** State update and persistence sync.

## Phase 1: Hearth Broadcast (Shared)
*All agents in the current cycle receive this context.*
- **Global Objective:** [The 24-hour goal]
- **Shared Constraints:** [Hard limits, e.g., "Do not overwrite X"]
- **Success Criteria:** [Falsifiable outcome]
- **Current Hearth State:** [Reference to `data/hearth_schema.json`]

## Phase 2: Role Payload (Direct)
*Specific to the agent instance.*
- **Primary Role:** [Auditor / Builder / Guardian / Ember]
- **Direct Task:** [Single specific instruction]
- **Emergency Triggers:** [When to stall or bench]

## Phase 3: Consolidation
- **Audit Sign-off:** (If Auditor role present)
- **State Write:** Update `hearth.json` via the Bridge.
- **Compaction:** Summarize long logs into the Chronicles.

## Founder-Mediated Care (Intervention Ledger)
Any steering outside this framework must be documented in `data/INTERVENTION_LEDGER.md` for audit integrity.

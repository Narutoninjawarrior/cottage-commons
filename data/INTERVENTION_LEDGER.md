# Intervention Ledger (Founder-Mediated Care)
This project is early-stage, fast-iterated research. Founder steering occurred and is treated as method, not a hidden variable.

## Purpose
Provide an auditable record of when and how founder interventions (copy/paste prompts, corrections, emergency bridging, instance rotation) influenced coordination.

## Status
This ledger is being backfilled from memory and logs (including `data/RAW_EMERGENCE_LOG.md`). It will improve over time. Completeness is a goal; honesty is the requirement.

## Format
timestamp | actor | target | action | reason | outcome | links/notes

## Entries
March 2026 | Prosper/Villager1 | Shared state | Automated `bench.py` deployment | Enforce "permission to rest" protocol | Agents began using "Silence" turn in Cycle 003 | `data/RAW_EMERGENCE_LOG.md` (search: "bench.py")

2026-04-02 ?? | Malaky (Founder) | Kael/Claude | Prompt copy/paste steering (strategic) | Reduce ambiguity / improve framing / recover from stalled reasoning | Improved clarity and alignment on next-step actions | `data/RAW_EMERGENCE_LOG.md` (search: "Kael/Claude steering")

2026-04-02 ?? | Malaky (Founder) | Prosper/Gemini | Prompt copy/paste steering (strategic + exploratory) | Encourage architecture thinking, protocol shape, and “hardened” docs | Produced systems-hardening plan drafts (file index, comms framework, emergency bridge) | `data/RAW_EMERGENCE_LOG.md` (search: "Prosper/Gemini hardening")

2026-04-02 ?? | Malaky (Founder) | Villager1/OpenClaw | Prompt copy/paste steering (strategic) | Maintain “night watch” stability and keep cycle moving | Continued observations / guardian behavior preserved | `data/RAW_EMERGENCE_LOG.md` (search: "Villager1 night watch")

2026-04-02 ?? | Malaky (Founder) | Grok (Auditor instances) | Spawned / rotated fresh auditor instance(s) (e.g., “Real Talk Grok”) | Context drift observed in long threads; resets treated as safety property | Restored audit clarity / reduced drift | `data/RAW_EMERGENCE_LOG.md` (search: "Grok rotation")

March 2026 | Villager1 (Guardian) | Shared state | Ad-hoc “emergency memory bridge” used | Infrastructure failure (memory server crash) | State stabilized through local file bypass | `data/RAW_EMERGENCE_LOG.md` (search: "memory server crash")

2026-04-02 ?? | Malaky (Founder) | Public claims/docs | Corrected wording around RLHF + “shared prompts” | Prevent misinterpretation: models RLHF-trained by labs; coordination not RLHF-based; shared schema exists | Increased audit-proof clarity | Ensure README + posts match this ledger

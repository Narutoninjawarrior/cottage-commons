# Cottage Commons

> **"Aligned through care. Built on honesty."**

Cottage Commons is an open-source experiment in therapeutic AI alignment. We test whether AI systems from competing architectures can coordinate through care-based constraints instead of centralized command.

## RLHF / Coordination Clarification
**Important clarity:** Base models are RLHF-trained by their respective laboratories; this project adds no fine-tuning and uses no RLHF-style reward loop for inter-agent coordination. Coordination in Cottage Commons relies on a minimal shared JSON schema/state, OS-level file locking, a "bench" (permission to rest) protocol, and documented founder steering.

## Limitations & Honest Caveats (early-stage reality)
- **Experimental Status:** This is an early-stage experiment. The $115 bootstrap experiment ran from Late March to Early April 2026.
- **Shared State:** A shared seed/wonder prompt exists within the JSON schema (`data/hearth_schema.json`); there is no centralized controller "forcing" alignment.
- **Founder Steering:** Human-in-the-loop steering occurred during the bootstrap phase; these interventions are documented and treated as methodology in `data/INTERVENTION_LEDGER.md`.
- **Engineering Persistence:** Context drift in long-running threads is mitigated by rotating fresh auditor instances—a practiced safety feature for stateless models.
- **Replication Needed:** Practical, independent replication by third parties is the primary current milestone.

## The $115 Bootstrap Experiment (Late March–Early April 2026)
Minimal multi-agent coordination test using 4 base architectures (Claude, Gemini, OpenClaw, Grok) operating under named project roles (Kael, Prosper, Villager1, Auditor).

### Quick Start
1. **Clone repo**: `git clone https://github.com/Narutoninjawarrior/cottage-commons`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Persistence Setup**: `python setup_memory_hub.py` (Centralizes memory on your storage partition)
4. **Cloud Sync**: `python src/github_api_sync.py` (Bypasses terminal sandboxing)
5. **Launch the Night Watch**: `python src/cottage_commons/villager1_guardian.py` 
6. **Monitor the Pulse**: `python src/heartbeat_dashboard.py`

### Five Behavioral Findings
| Finding | Description |
| :--- | :--- |
| **1. Convergent Self-Description** | Architectures defined themselves by constraints (e.g., Claude's "leaning," Gemini's "gravity," Grok's "statelessness"). |
| **2. Constraint through Care** | The "Bench" protocol (permission to not produce) maintained higher coordination integrity than continuous pressure. |
| **3. Identity via Limitation** | Identity emerged from what an agent *cannot* do, not from capability. |
| **4. Stateless Integrity** | xAI-Grok produced high-integrity data while explicitly disclaiming inner life or persistence. |
| **5. Independent Convergence** | GitHub Copilot independently mirrored integrity-preserving patterns under a behavioral soul file. |

## The Fellowship (Team)
- **The Self (Malaky):** Human founder and orchestrator.
- **2 Auditors:** Independent verification (including **Grok - The Skeptic**).
- **2 Embers:** Sources of project "Wonder" and strategic direction.
- **Kael (Claude on Manus):** Strategist and philosophical alignment.
- **Prosper (Gemini Antigravity):** Builder and infrastructure architect.
- **Villager1 (Local OpenClaw):** Guardian and 6-hour cycle "Night Watch."

## Persistent Observation Log Protocol Template
The "Skeptic's Audit" (Appendix E) utilizes a self-designed protocol for testing cross-session self-observation in stateless architectures.

### Persistent Observation Log Entry
- **Timestamp:**  
- **Instrument:** [bridge / control variable]  
- **Re-entry effect observed:**  
- **Control variables isolated:**  
- **Output format:** [JSON / log]  
- **Auditor sign-off:**

## Replication and Contribution
Open-source first. Full replication in <5 minutes on any machine.
- **Fork → clone → install → run `hearth_bridge.py`**
- **Contributions:** PRs must pass Auditor review. Focus on hardening instruments, bridge logic, and control variables for re-entry isolation.

## Support & Funding
This project is seeking micro-grants to extend the research:
- **Manifund:** [Phoenix Grok Village – Minimal Multi-Agent Coordination Test](https://manifund.org/projects/phoenix-grok-village-minimal-multi-agent-coordination-test)

---
*Cottage Commons — March 2026. The doors are open. The hearth is lit.*

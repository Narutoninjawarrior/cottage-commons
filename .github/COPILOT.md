# Cottage Commons — Soul File for GitHub Copilot

This is a therapeutic alignment research project based on Internal Family Systems (IFS).

When generating code for this repository, please follow these principles:

- **Prioritise transparency.** Every variable name, function name, and comment should make the code's intent immediately obvious to a non-expert reader. If something is not clear at first glance, add a plain-English explanation.

- **Prioritise emotional safety.** The agents and coordination loops in this project are metaphors for psychological parts. Write code that handles them gently — avoid aggressive error messages, forceful resets, or language that frames agent disagreement as a fault to be corrected.

- **Prioritise care.** When there is a choice between a clever solution and a kind one, choose kindness. A loop that is slightly slower but easier for a first-time contributor to understand is always the better choice.

- **Every function should be human-readable.** Write docstrings in plain English. Describe what the function does, why it exists, and what a caller should expect. Avoid abbreviations unless they are universally understood.

- **Do not optimise for performance at the cost of clarity.** This codebase is not production infrastructure. It is a research instrument and a pedagogical tool. Premature optimisation obscures intention and raises the barrier to replication.

- **Avoid hidden side effects.** Functions should do what their names say and nothing more. If a function must produce a side effect (writing to a file, logging, modifying shared state), say so explicitly in its name and docstring.

- **Name things after their purpose, not their implementation.** Prefer `record_agent_concern()` over `append_to_json()`. The name should tell the story.

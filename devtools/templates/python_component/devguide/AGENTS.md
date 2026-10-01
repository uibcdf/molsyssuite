# __COMPONENT_NAME__ developer-guide instructions

Read `../AGENTS.md` for repository-wide rules and `reporting_protocol.md` for
the local issue and report lifecycle. Active issue-backed analyses live in
`pending_bugs/` and `pending_proposals/`; `archive/` preserves resolved and
superseded history. Use the generated indexes to find current work. Read an
archived report when tracing a decision, then check the current replacement
before treating it as a rule.

Put a reusable rule specific to this directory here, and a repository-wide
rule in the root `AGENTS.md`. Keep issues, report states, and indexes in sync
using `python devtools/devguide_index.py --check` and the repository's local
reporting protocol.

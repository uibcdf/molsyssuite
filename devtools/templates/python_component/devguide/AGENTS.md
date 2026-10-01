# __COMPONENT_NAME__ developer-guide instructions

Read `../AGENTS.md` for repository-wide rules and `reporting_protocol.md` for
the local issue and report lifecycle. Active issue-backed analyses live in
`pending_bugs/` and `pending_proposals/`; `archive/` preserves resolved and
superseded history. Use the generated indexes to find current work. Read an
archived report when tracing a decision, then check the current replacement
before treating it as a rule.

Keep technical facts and defect details in maintained documents, tests and
owning issues. Put only lasting working instructions specific to this
directory here, and repository-wide working instructions in the root
`AGENTS.md`. Follow the local reporting protocol to synchronize issues and
report states. After a report lifecycle change, run
`python devtools/devguide_index.py` to regenerate indexes, then run it with
`--check` to verify them.

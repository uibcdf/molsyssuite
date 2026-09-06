# MolSysSuite developer guide

This directory holds suite-wide decisions, coordination records, collective evidence and
long-lived technical guidance. Component-local implementation belongs in the relevant
member repository.

Before filing or closing work, read the normative
[`reporting_protocol.md`](reporting_protocol.md). The boundary between central and local
ownership is defined by [`repository_contract.md`](repository_contract.md), and the
machine-readable member registry is [`../suite.toml`](../suite.toml).

Current work is indexed in:

- [`pending_bugs/`](pending_bugs/README.md)
- [`pending_proposals/`](pending_proposals/README.md)

Closed records remain available under [`archive/`](archive/README.md). Plans, runbooks and
evidence artifacts are not queue entries unless they describe one independently closable
theme.

Coordinated adoption programs live under [`rollouts/`](rollouts/README.md); their central
issue carries public state while the rollout document carries the changing member matrix.

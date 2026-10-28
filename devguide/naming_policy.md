# MolI and Moli display names

Accepted for MolSysSuite and every registered member under
uibcdf/molsyssuite#121. This adopts the criterion accepted by Diego in
[MolI #73](https://github.com/uibcdf/moli/issues/73), including its
[published conceptual basis](https://github.com/uibcdf/moli/blob/e7a9f84ef685b9ecd11b753489ed9d702cc11924/devguide/policies/naming_policy.md).

## Meaning and applicability

| Name | Meaning |
| --- | --- |
| Molecular Intelligence | The complete scientific capability, combining scientific context, molecular modeling and scientific reasoning. |
| MolI | The platform supporting that capability; Mol from Molecular and I from Intelligence. |
| Moli | The proper name of MolI's optional scientific agent. It is distinct from MolSys-AI and its specialist agents. |

Use these names in new or substantively revised human-facing prose, in English
and Spanish: documentation, issues, discussions, reports and conversations.
When introducing both, make the distinction clear: **MolI is the Molecular
Intelligence platform. Moli is its scientific agent.** People and other systems
can use MolI directly; Molecular Intelligence does not require Moli or an LLM.
This editorial rule changes neither scientific authority nor component ownership.

## Technical identities and history

Keep repository/file/package/import/API/schema identifiers and URLs exact,
including `uibcdf/moli`, `uibcdf/moli-agent`, `moli.toml`, `MOLI_GUIDE.md` and
`architecture_1.0/MOLI_AGENT.md`. Do not apply a blanket replacement to source,
technical literals, immutable evidence, exact quotations or historical records.
Earlier MOLI / MOLI Agent identify the same platform / agent; explain that
mapping when necessary. Existing history needs no mass rewrite.

## Delivery and exceptions

The mandatory common guide carries this future-writing action; the official
starter inherits it. Distribution uses the registered synchronizer and records
source/adoption evidence independently of runtime or scientific qualification.
An immutable central source commit identifies the published editorial contract;
this adds no Python caller bump or automated prose-replacement gate.

A bounded deviation records the affected prose/scope, owning issue, reason,
responsible maintainer, interim wording, review/expiry and removal condition.
Technical identity preservation is normal applicability, not an exception.

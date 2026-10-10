---
summary: Define a reproducible molecular-tool discovery pilot and its ownership.
issue: uibcdf/molsyssuite#114
status: open
opened: 2026-10-10
closed:
verification: inspected
area: [governance, observability]
guard:
normative:
blocked_by: []
supersedes: []
---

# Molecular-tool discovery observatory

**Reported:** Incoming uibcdf/molsyssuite#114, 2026-10-10.
**Status:** Proposed measurement contract and initial query set; pilot scope,
provider, implementation ownership and publication remain undecided.

## What

Measure how users discover molecular tools and whether recommendations have
supporting evidence. Start with MolSysMT while keeping the measurement reusable
for other tools. The initial unit is one versioned query, one provider and one
acquired response, not an inferred population of users or independent agents.

The original qualitative exercise reported twenty generic English queries but
did not retain their exact texts, complete ranked responses or provider settings.
Those observations cannot be recovered from this issue as a quantitative baseline.
The candidate queries below are **new proposed queries**, not a reconstruction
of the original twenty and not measured results.

## How

### Recommended first stage

1. Review and version the methodology, twenty candidate generic queries, separate
   brand controls, target identities and role categories.
2. Select one permitted collection route, its provenance, result-depth guarantees,
   retention/publication terms and an explicit execution/cost limit.
3. Collect a manual pilot, preserve permissible evidence and reproduce its metrics
   offline from the same snapshot. An incomplete run remains visibly incomplete.
4. Review the pilot before selecting a public dashboard, monthly automation or
   an actual agent track. None is needed to begin the measurement contract.

This is an optional research pilot. It creates no member CI, admission, release,
visibility score or required documentation gate.

### Ownership and reusable operations

MolSysSuite #114 owns member discovery needs, relevant query families and member
adoption. A generic observatory intended as a MOLI service needs its own MOLI
coordination issue and an accepted implementation owner before repository creation.
`uibcdf/moli-visibility-observatory` is a proposed identity, not an admitted member
or an existing provider. Do not add it to `suite.toml` merely to host the pilot.

Read-only inspection of `uibcdf/moli-dev-observatory` at
`393150491bd5e5b3ef8d5d6536eb6933e8d3dc86` confirms its existing collector →
normalized JSON → metrics → static pages pattern. Its collector and metric
definitions are for GitHub issues; they do not collect search results or measure
discovery. Its public workflow excludes private/inaccessible repositories.
Keep those existing development metrics and their publication contract separate.

The eventual implementation owner should provide independently useful operations:
provider collection, snapshot validation, target attribution, offline scoring and
rendering/export. Consumers call those operations; provider adapters and generic
scoring do not belong in a MolSysMT documentation script. Review reusable support
already present in the chosen owner before implementation; avoid copying the
development observatory as an untracked starter template.

### Candidate query set for review

Proposed revision: `molecular-discovery-en-v1-draft`, twenty generic queries,
five per family, English. Exact text becomes fixed only after review. Each row
records its intended task; the query is not a claim that any named tool can do it.
No tool name is inserted into these generic queries.

| ID | Family | Exact proposed query |
| --- | --- | --- |
| D01 | General discovery | Python libraries for working with molecular structures and trajectories |
| D02 | General discovery | Python toolkit for inspecting and manipulating molecular systems |
| D03 | General discovery | Open source tools for biomolecular structure analysis in Python |
| D04 | General discovery | Python library for selecting atoms and residues in molecular structures |
| D05 | General discovery | Python tools for working with molecular topology and coordinates |
| I01 | Interoperability | Python tools to convert molecular structures between file formats |
| I02 | Interoperability | Python library for a common interface to molecular structures and trajectories |
| I03 | Interoperability | Python tools to preserve molecular topology when converting representations |
| I04 | Interoperability | Python library for handling molecular coordinates with physical units |
| I05 | Interoperability | Python tools to exchange molecular data between analysis and simulation libraries |
| S01 | Scientific tasks | Python tools for measuring distances and angles in molecular systems |
| S02 | Scientific tasks | Python library for aligning molecular structures and calculating RMSD |
| S03 | Scientific tasks | Python tools for analyzing molecular contacts across trajectories |
| S04 | Scientific tasks | Python tools for handling periodic boundary conditions in molecular trajectories |
| S05 | Scientific tasks | Python library for comparing multiple conformations of a protein |
| W01 | Unified workflows | Python workflow to load inspect select and export a molecular structure |
| W02 | Unified workflows | Python tools connecting molecular visualization with trajectory analysis |
| W03 | Unified workflows | Reproducible Python workflows for molecular structure analysis |
| W04 | Unified workflows | Python workflow to combine molecular analysis tools without losing units |
| W05 | Unified workflows | Python tools for interactive molecular system analysis in notebooks |

Separate proposed controls are `B01: MolSysMT documentation` and
`B02: MolSysMT molecular systems Python`. Report them only as brand/indexing
controls; never include them in the generic-discovery denominator.

Candidate reference identities from the incoming issue are MolSysMT, MDAnalysis,
MDTraj, Biotite, Sire, BioSimSpace, ParmEd and OpenMM. Before scoring, record
canonical domains, verified aliases, ambiguous names and task roles. This is a
comparison set, not a claim that these tools are equivalent or a ground-truth
list of all relevant tools. Keep other observed candidates visible.

### Proposed measurement contract

| Record | Minimum information |
| --- | --- |
| Benchmark | Revision/content digest, exact query IDs/text/families, controls, language, target attribution rules and metric revision |
| Run | Unique ID, UTC start/end, Mexico City display timezone, benchmark digest, provider/engine/model identity and version when exposed, locale/location, parameters, collector revision, execution route and declared limits |
| Response | Query ID, acquisition timestamp, success/error, track, requested depth, returned ordered depth, completeness/exhaustion evidence, permissible results or response/citations, retained-evidence digest and retention/publication disposition |
| Attribution | Target identity, result rank and matching evidence, canonical page / third-party mention / ambiguous, reviewer or deterministic rule revision; a mention is distinct from a recommendation |
| Assessment | Exact factual claim, supporting source and version/date, supported / contradicted / unknown outcome and reviewer; document access is separate from content correctness |
| Summary | Metric revision, eligible/query counts, exclusions and reasons, per-query values, family totals and raw-to-derived references |

Provider-hidden model versions remain `unknown`; a browser session, search API,
tool-returned selection and independent agent execution have different collection
routes. Acquisition errors, missing responses and unverifiable ranks do not become
negative observations. A selected search excerpt is not a complete top-ten list.

First-stage web results use proposed fixed `k = 10`. A response can enter a
negative presence/MRR denominator only if its ordered first ten eligible results
are verified, or the provider explicitly establishes an exhausted shorter list.
If completeness cannot be established, show observed matches separately and
exclude that query from comparative top-ten metrics. Preserve original ranks;
record treatment of advertisements, duplicates and non-organic blocks in the
provider adapter instead of silently reranking them.

- `presence@10(target, query)` is 1 when an eligible attributed result occurs,
  otherwise 0 for a complete eligible response. Publish canonical-page presence
  separately from third-party mentions.
- `coverage@10(target)` is positive eligible generic queries divided by all
  eligible generic queries; publish both counts and excluded query IDs. Report
  each family separately to avoid hiding different tasks in one aggregate.
- Reciprocal rank is `1 / first matching original rank`, or 0 for verified absence.
  MRR is its mean over eligible responses with the same attribution definition.
  Incomplete observed hits do not enter that comparative mean.
- Do not label query coverage as retrieval `recall@10`: a recall denominator
  needs a separately reviewed relevant-result ground truth, not this candidate set.

Web discovery, actual agent nomination/recommendation, factual correctness and
reference/documentation access are distinct tracks. A web search through an agent
interface remains a search observation. The agent track stays off until agents
are actually invoked with recorded configurations, responses and independence
limits; repeated identical queries do not establish independent-agent sampling.

Matched comparisons require the same benchmark, attribution/metric revisions,
provider settings and declared collection route. Record provider drift and content
changes. A before/after association does not establish that a documentation change
caused a rank change. Freeze methodology before evaluating such changes.

### Pilot evidence and future publication

Preserve the original permissible snapshot and its digest before deriving metrics.
Review one provider's actual terms and current API behavior before selecting it;
no API, paid service or automated scraper is selected by this proposal. If response
redistribution is restricted, retain permissible provenance/derived data with
explicit limits; do not call unavailable private/raw evidence publicly reproducible.

Use synthetic fixtures for later scoring guards: a known hit at rank 3, verified
absence, shorter exhausted results, incomplete results, provider errors, ambiguous
names, brand controls and changed benchmark revisions. These fixtures test scoring
semantics; they are not discovery observations. No new scientific test is needed.

Public data review occurs before a dashboard or dataset publication. Permit only
reviewed public queries and licensable evidence; keep credentials, private logs,
private repository data and unpublished scientific material out of artifacts.
JSON/CSV exports and drill-down should expose denominators and missing evidence.
Select an owner, budget and retention policy before monthly scheduling. DOI and
dataset licensing remain separate decisions after a usable dataset exists.

## Why

The suite needs evidence distinguishing poor indexing, absent discovery and
incorrect recommendations. A defined pilot can reveal which problem exists
before investing in infrastructure or changing documentation. Visibility is not
a measure of scientific correctness or a requirement to use a particular tool.

## What is measured and what is assumed

Measured discovery results: **none retained or produced by this work**.
The incoming issue's qualitative historical account remains attributed to its
author. Architecture/ownership statements above are source inspection on
2026-10-10, not an execution of the existing observatory or a search-provider audit.
The twenty queries, k, metrics and staging are proposals awaiting review.

## Alternatives and refuted paths

- Immediate repository/dashboard/monthly jobs: feasible as a later stage, but
  provider permissions, complete result acquisition, cost and ownership are open.
- Extend the existing development dashboard with discovery scores: would conflate
  distinct datasets and metric semantics; evaluate shared rendering support in
  the eventual owner instead.
- Reuse the original twenty-query result as 0/20: rejected because exact queries,
  ranked responses and provenance were not preserved.
- Build all tracks together: optional agent execution and factual assessment
  can follow the search pilot; neither is inferred from a search result list.

## Scope and exclusions

This issue coordinates an optional ecosystem measurement proposal. MolSysMT's
task tutorials, scientific paper and implementation remain owner work, to receive
a linked local issue once a concrete adoption need is accepted. No member policy,
guide, CI requirement, scientific code, provider pin or release route is changed.

## Acceptance criteria

The incoming issue's full acceptance remains: an executable reviewed methodology
and benchmark; permissible snapshots with provenance; separate search/agent
tracks; reviewed public reporting; demonstrated repeatability; and linked
MolSysMT follow-up. This document prepares a first stage and does not close #114.

The first decision is whether to proceed with **methodology plus one manual
provider pilot**, or defer the pilot and retain this discussion. Following that
decision, provider selection and its execution/cost/publication bounds still
require review. Repository ownership, automated cadence and agent execution
remain later decisions, not implicit authorization from accepting a draft.

## Local implementation issues

None opened yet. MOLI coordination and a MolSysMT local adoption issue are
proposed routes, not already delivered notices or assigned implementation.

## Dependencies and risks

Exact historical queries are unavailable in #114. Provider-specific completeness,
result terms, cost and version exposure are unqualified. Agent execution is
unqualified. These uncertainties must remain visible in any claimed baseline.

## Provenance

Incoming uibcdf/molsyssuite#114 and read-only source review of
`uibcdf/moli-dev-observatory` at the immutable revision above, 2026-10-10.
Cross-repository preflight fetched registered remotes and preserved dirty/active
clones. Local administrative verification uses `molsyssuite@uibcdf_3.14`,
Python 3.14.7; both receptors import from their participating editable clones.
The seven existing dependency-closure findings remain owned by #82 and do not
become a successful dependency-closure claim in this proposal.

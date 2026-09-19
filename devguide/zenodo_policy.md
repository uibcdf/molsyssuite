# Zenodo archival and DOI policy

This document is normative for the Zenodo archival lifecycle of repositories registered
in `suite.toml`. Accepted under `uibcdf/molsyssuite#24`.

## Scope and applicability

Wave-1 and infrastructure components use `zenodo-archival = "required"`. Before their
next public release after adopting this policy, they must validate repository metadata,
publish only after their local release gates pass, and independently verify the public
Zenodo record. Auxiliary and incubating components use `optional` until they enter
stabilization or prepare a public release. An exception names its repository, reason,
tracking issue, responsible role and expiration condition.

The mode is stable governance recorded in `suite.toml`. External observations live in
`devguide/rollouts/zenodo_inventory.toml`; account credentials and personal account data
never do.

## Evidence states

Use exactly these states:

- `unknown`: no policy-grade observation has been completed;
- `enabled_reported`: an authorized maintainer reports the repository toggle enabled;
- `webhook_observed`: a bounded query observed an active release delivery route;
- `release_published`: GitHub reports the release public;
- `ingestion_pending`: publication occurred and the bounded retry window remains open;
- `verified`: a public Zenodo record, DOI and exact file inventory were independently
  matched;
- `absent`: the bounded public query found no matching record after publication;
- `invalid`: a record exists but its identity, metadata or files contradict the expected
  release;
- `temporarily_unavailable`: Zenodo could not provide conclusive public evidence;
- `not_applicable`: an approved exception says archival does not apply.

The first five states are observations, not proof of archival. Only `verified` permits a
component or suite surface to claim successful Zenodo archival, and that claim must name
its coverage. A source snapshot does not imply that wheels, Conda packages, checksum
manifests or GitHub Release assets were archived.

## Ownership

- MolSysSuite governance defines applicability, evidence vocabulary, minimum metadata,
  audit rules and exceptions, and maintains the collective inventory.
- Authorized Zenodo maintainers connect or rotate the UIBCDF account integration and
  investigate account-side ingestion failures without disclosing configuration secrets.
- Component maintainers own release metadata, artifacts, workflows, component tests,
  publication decisions and exact-version evidence.
- Automation validates repository-contained or public facts. It never infers a toggle,
  webhook, DOI, deposit or archive from another green workflow.

No component publishes or repairs a sibling component's release.

## Metadata authority

`CITATION.cff` remains the GitHub-facing citation record. When `.zenodo.json` is also
present, Zenodo uses `.zenodo.json` and ignores `CITATION.cff` for GitHub release
archiving. Components retaining both files validate their shared title, creators, ORCIDs,
license and repository relation before publication. Zenodo-specific fields may live only
in `.zenodo.json`; silent disagreement is an error.

The authoritative upstream behavior is documented by Zenodo in
<https://help.zenodo.org/docs/github/describe-software/> and
<https://help.zenodo.org/docs/github/describe-software/zenodo-json/>.

## DOI rules

The concept DOI identifies the evolving project and is used in stable project badges,
README citation and general documentation. A version DOI identifies one immutable
release and is used for exact-version citation and reproducibility statements. Neither
DOI may be invented, copied from a sibling, or published before the public record proves
it. A version DOI must not replace the concept DOI in a permanent project badge.

## Release and verification procedure

1. Validate `CITATION.cff` and, when present, `.zenodo.json`; validate their shared
   fields and repository relation.
2. Run the component's complete release gates against the exact candidate commit.
3. Have an authorized maintainer confirm or repair the account connection using the
   least-disclosure procedure below.
4. Prefer draft-first GitHub publication when supported. Publication remains a deliberate
   maintainer action; this policy does not authorize it.
5. Record the exact public GitHub tag, release and asset inventory independently.
6. Wait a bounded interval for asynchronous Zenodo ingestion. Use `ingestion_pending`,
   then retry with a documented limit; never convert delay into success.
7. Query the anonymous public records API and verify repository identity, exact version,
   software type, open access, version DOI, concept DOI and every archived file's name,
   size and checksum. The Records API is documented at
   <https://developers.zenodo.org/#records>.
8. Record `verified`, `absent`, `invalid` or `temporarily_unavailable` with date and
   sanitized evidence. Publish DOI claims only for `verified` records.
9. Periodically re-audit registered verified evidence and remove or correct stale badges.

Zenodo documents that GitHub release processing can take time; a missing record during
the bounded retry window is `ingestion_pending`, not success or permanent absence:
<https://help.zenodo.org/docs/github/archive-software/github-upload/>.

## Least-disclosure account procedure

Account-side inspection is restricted to authorized maintainers. Routine checks project
only whether a release hook exists and is active, plus non-secret timestamps needed for
diagnosis. Never print or retain raw hook configuration, receiver URLs, query strings,
tokens, cookies, screenshots containing them or unfiltered API responses.

If a credential-bearing receiver URL is exposed, stop sharing the output, rotate the
connection by disabling and refreshing or synchronizing the repository integration, and
reenable it before the next release. A newly observed active hook is recovery evidence,
not proof that Zenodo ingested a release.

## Public audit and failures

`python devtools/scripts/audit_zenodo.py` validates the inventory offline. Add `--public`
to re-query only entries already registered as `verified`; it uses anonymous bounded
requests and no credential. Unknown rows remain visible rollout debt but do not become
false failures. A mismatch is `invalid` and fails the audit. Network or service failure
is `temporarily_unavailable` and must be reported separately from both success and
absence.

The audit inventory stores only durable public facts and expected file evidence. Mutable
account state stays out of Git. Raw public responses are not committed merely because
they are public; retain the bounded semantic result instead.

## Exceptions and historical releases

An exception records repository, reason, issue, responsible role and expiration
condition. `not_applicable` requires such an exception. Optional status is not a silent
exception: it expires when the component enters stabilization or prepares a public
release.

This policy governs releases after adoption. It does not claim that historical releases
were archived or require automatic backfill. Backfill is separately measured and decided
per component because enabling the integration is not assumed to archive older releases.

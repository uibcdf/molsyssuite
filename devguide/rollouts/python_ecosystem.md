# Python ecosystem policy rollout

**Owners:** `uibcdf/moli#6` for the platform rule;
`uibcdf/molsyssuite#6` for member adoption.

**Effective snapshot:** MOLI `6a91433bd38582980d0781474be6a80c58f48886` plus
MolSysSuite `policy-v1.4.11`.

MOLI published the support-library and developer-tool policies on 2026-09-23.
Publication changes the inherited baseline; it does not establish member adoption.
At the initial checkpoint, all 14 registered Python members had `pending` reviews for
both policies in `suite.toml`. Some members already use particular libraries or
receptors, but no complete applicability review has yet been accepted under this
snapshot. This conservative state prevents guide delivery or an older CI run from
being mistaken for proof of adoption.

The live declared inventory is:

```bash
python devtools/scripts/python_ecosystem_status.py
```

The validator checks record coverage and evidence requirements without requiring
all members to be adopted. `--require-adopted` is the rollout completion gate.
Each review advances only with a member issue and linked evidence describing
applicable boundaries, non-applicability, implementation and tests, and any bounded
exception. Existing member migration issues may carry the review when their scope
matches; the suite issue remains the coordination record.

The separate guide-copy and policy-caller inventory remains under
`uibcdf/molsyssuite#34`. A policy caller that is current or compatible with
`policy-v1.4.11` does not prove adoption of either newly inherited policy.

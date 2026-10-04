# Optional scientific attribution clients

Accepted under uibcdf/molsyssuite#68. This profile applies to new or changed
optional scientific method/result attribution boundaries in MolSysSuite members.
Utilities without such a boundary record non-applicability. Installing a package
does not itself earn scientific credit. Existing integrations are reviewed in
their member issues; distributing a guide does not establish runtime adoption.

## Client obligations

1. Keep offline bibliographic declarations in host-owned constants, verified
   against the original work. Defer Ackredit imports and provider registration
   until an attribution boundary is requested. Importing the host must not load
   Ackredit or enable network, filesystem or tracking side effects.
2. Credit the branch actually reached. Distinguish the scientific criterion,
   adapted reference implementation and executed software in the result context.
   Track once per calculation or meaningful child operation, not per pair, frame
   or occurrence. A reference implementation is not an executed dependency.
3. Completed evaluated-empty analyses retain their provenance. Failed operations
   cannot claim successful completion; independently completed children may
   retain their own credit. Scientific method definitions remain host-owned.
4. Applications own workflow sessions. Contribute to the current session rather
   than replacing it with an isolated component session. Do not infer individual
   result references by subtracting deduplicated before/after session IDs.
5. Results carry detached bibliography and original producer versions, including
   references reused across results. Saving, reading or forwarding those results
   preserves provenance without claiming a new scientific calculation.
6. Provider absence preserves scientific results and host-owned provenance.
   Provider failure emits a catalog diagnostic and preserves completed results
   without claiming successful tracking. Never swallow a scientific exception
   as a provider failure; isolate the provider boundary carefully.
7. Libraries must not automatically enable import hooks, auto tracking, DOI
   enrichment, journals or reminders. Applications may explicitly opt into
   documented provider features appropriate to their workflow.
8. Integration evidence uses a real provider and actual tracking observations.
   Cover two results reusing a reference, an enclosing workflow, evaluated-empty
   results, genuine absence, provider failure, detached ownership, fresh-process
   lazy import and a fresh reader preserving original versions without new
   credit. An installed flag or mocked success alone is insufficient.
9. Check provider floors and published dependency closure for every claimed
   client Python minor. Do not narrow MolSysMT/Viewer support to accommodate an
   optional provider. Editable pilot evidence does not authorize a public extra
   or published compatibility claim.

## Provider contract and adoption

Ackredit owns its public API and canonical
[integration guide](https://github.com/uibcdf/ackredit/blob/main/standards/ACKREDIT_GUIDE.md).
The portable contract requested in uibcdf/ackredit#75 is publicly delivered in
Ackredit 0.9.0: `ackredit.attribution@1`, `Attribution`, `capture` and
`get_attribution`. The released portable API floor is `ackredit>=0.9.0`;
this identifies provider capability, not a mandatory dependency for every member.
Exact public-file and installed qualification evidence is retained in the
[admission receipt](rollouts/ackredit_python314_admission_51.json).
Hosts use supported public operations and retain ownership of their scientific
result schemas and adoption checks. Do not read private provider registries,
duplicate renderers, treat journals containing IDs as portable bibliography,
or invent supported API names.

The inspected MolSysMT pilot at
`e21f03d9992b87af2cc9285211adee888462be41` supplies consumer evidence, not a shared
serialization schema or certification of a published Ackredit revision. Its
reported measurements and limitations are retained in the issue-backed review.
Scientific implementation and member runtime adoption stay with their owners.

## Exchange with component and project consumers

Accepted clarification under uibcdf/molsyssuite#76; applies when a member
exchanges detached attribution with another component or project. Keep the
original result/source identities, observed producer/software versions,
bibliography, contextual uses and explicit gaps or failures. A saved reader
preserves those original records without new acquisition, credit or silent
replacement by current metadata.

The host owns result/operation links and completeness outside the provider
payload. Source support, source-stated terms, permission decisions, execution
history and project Evidence retain their respective owners. A valid citation
record alone establishes none of those decisions. Required dependencies chosen
by external consumers do not change the suite's optional client profile.
This clarification establishes no universal wrapper, status enumeration or
new provider API. Hosts retain their documented exception route below.

The synthetic [two-result example](examples/ackredit_moli_boundary.py) and
[fresh saved reader](examples/ackredit_moli_saved_reader.py) demonstrate the
portable provider portion with installed Ackredit >=0.9.0. Run them outside
the source repositories, using absolute example paths:

```bash
python /path/to/molsyssuite/devguide/examples/ackredit_moli_boundary.py > saved-example.json
python -I /path/to/molsyssuite/devguide/examples/ackredit_moli_saved_reader.py saved-example.json
```

The outer records are example-local. They implement no project store, source
acquisition, authorization decision or scientific interpretation. The bounded
public-provider evidence is retained in the
[review receipt](rollouts/ackredit_moli_handoff_76_20261004.json).

Third-party hosts and deliberate eager/demo integrations may use the provider's
documented eager profile. A MolSysSuite integration needing different
initialization or session semantics records a reviewed member-owned exception:
affected rule, reason, owner and owning issue, interim controls, expiry and
removal condition. This follows the
[ecosystem exception mechanism](python_ecosystem_policy.md#member-review-and-evidence).

Synchronize canonical guidance through `sync_vendored_guides.py`, never by
editing consumer copies. Keep provider API implementation, public distribution,
guide delivery and actual member adoption as separate claims.

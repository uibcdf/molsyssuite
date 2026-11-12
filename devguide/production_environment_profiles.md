# Future production environment profiles

Design disposition under #175: MolSysSuite owns future
`molsyssuite@<python>` runtime profiles; MolI owns `moli@<python>`. Development
names are separately `molsyssuite_dev@<python>` and `moli_dev@<python>`.
The suffix always names the actual Python major.minor. No production environment
is created or qualified by this naming/design decision, and metapackage names
and release versions retain their independent meaning.

The first production profile must state its user/service purpose and selected
scientific capabilities before choosing packages. Use qualified installed
artifacts, not the mutable editable development cohort. Record exact package,
native engine, platform/minor and optional-feature closure; a source-only
component or unavailable public dependency remains an explicit blocker under
#45/#51. Optional engines are selected for an implemented purpose and keep their
owner's resource, scientific, licensing and availability contracts.

Qualification needs the actual clean solve/install, neutral-directory origins,
entry points/resources and representative capability tests of that profile.
Retain an exact package manifest/lock, immutable source/artifact digests, relevant
engine/build/tool versions and a tested recovery route. Environment recreation,
scientific reproducibility and public artifact compatibility are different claims.
Do not infer any of them from the development profile's name or import smoke.

Production recipe implementation and actual package/engine selection remain
unselected pending those owner capabilities and a concrete runtime use case.
MolSysSuite owns that future decision; MolI #94 owns the platform counterpart.
The existing `devtools/conda-envs/molsyssuite.yaml` remains its separately scoped
historical published-package recipe. #82's paused local workspace migration and
retained prefixes are preserved. No prefix rename, deletion, automatic upgrade,
package publication or service activation follows from this design.

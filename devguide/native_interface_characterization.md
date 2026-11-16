# Native interface characterization: bounded shared review

Status: **bounded shared source disposition received; per-consumer acceptance partial**,
2026-11-15 Mexico City / 2026-11-16 UTC, under
[MolSysSuite #195](https://github.com/uibcdf/molsyssuite/issues/195).
The initial 2026-11-12 proposal review is supplemented by the immutable molecular
owner contract and delivered BindingMT native/saved-result profiles below. This
central receiving introduces no scientific API, record schema, dependency floor
or independent scientific execution. Source development, actual consumer use,
installed artifacts and public qualification retain separate evidence.

## Sources and ownership

The reviewed catalogue is [TopoMT revision 1](https://github.com/uibcdf/topomt/blob/a13b9b2725bd8a4edd851441d1a5a53720e0f3ea/devguide/binding_interface_native_catalogue_plan.md).
The selected BindingMT context is its [design](https://github.com/uibcdf/bindingmt/blob/d69315dfebc49ddd8c2da1999955edc078fd8893/devguide/binding_interface_design.md)
and [implementation plan, revision 2](https://github.com/uibcdf/bindingmt/blob/d69315dfebc49ddd8c2da1999955edc078fd8893/devguide/binding_interface_implementation_plan.md),
particularly the first-profile decisions and fact/check/precondition matrix.
The [existing TopoMT conceptual contract](https://github.com/uibcdf/topomt/blob/3a8ee979db8de6f6345de74558a878bb96ba3234/devguide/topography_conceptual_contract.md)
retains its association/realization ownership. Exact file hashes and review
limits are retained in the [batch receipt](rollouts/third_ten_receiving_20261112.json).

| Responsibility | Owner / active route |
| --- | --- |
| Binding question, participants/grouping, binding-specific composition, catalogue, interpretation and actual public workflow | BindingMT #112 |
| Molecular identity, chemistry, selection, correspondence, generic contacts, distances, radii and surface operations | MolSysMT; selected public calls below |
| Topographic associations, realizations, spatial supports and contextual evaluations | TopoMT #197 and its existing #60/#61/#62 |
| Shared meaning, operation-specific contract review and receiving inventory | MolSysSuite #195 |
| Pharmacophoric and peptide-specific applications | Their respective owners and the already linked BindingMT #112 reviews |

The ordinary native molecular calculation has no PISA or TopoMT prerequisite.
Topographic enrichment and saved PISA intake remain explicit optional routes.
Existing PISA T0/T1, pharmacophoric H0/H1 and consumer obligations keep their
recorded scope until BindingMT records any priority/defer decision. The native
catalogue does not cancel them or make every future family a prerequisite.

## First operation profiles

Begin with two resolved, nonempty, disjoint atom populations A and B in one
chosen Cartesian structure, fixed coordinates and admitted chemistry. The
initial evaluated environment is exactly A union B. Record participant
granularity/grouping, source occurrence, effective chemical state, original and
local atom/structure axes, frame and every performed transformation. Selection
names, equal counts and equal numeric indices do not establish correspondence.
Overlapping groups, covalent interfaces, periodic reconstruction and third-body
environments require separately admitted profiles; they are not universal core
record errors. An unresolved data declaration can remain preservable while its
requested numerical operation lacks necessary proof.

### Geometric contacts

At inspected MolSysMT source
`ff25f120243319ca9515009b4971e24a2eb0dc22`,
[`structure.get_contacts`](https://github.com/uibcdf/molsysmt/blob/ff25f120243319ca9515009b4971e24a2eb0dc22/molsysmt/structure/get_contacts.py)
admits finite nonnegative scalar length cutoffs and includes equality. Its
atomic profile needs explicit endpoint selections, one actual structure,
`pbc=False` and no center-of-atoms interpretation. The application cutoff,
method/backend and numerical policy are BindingMT profile decisions; the
provider's default 12 angstroms is not a selected binding-interface criterion.

The provider returns a Boolean map or pair projection, not a scientific receipt
with all distances. A report promising distances must obtain them through the
qualified public distance operation with the same endpoints/context. In the
documented API, `pairs=True` means corresponding endpoint pairs, whereas
`output_type="pairs"` requests a pair representation. These two meanings must
not be confused when requesting all A-by-B contacts. The Boolean map can remain
resident even for pair output; use bounded inputs or a qualified owner neighbor
operation. BindingMT does not implement another contact-search kernel.

Count cross-participant unique atom pairs for this profile. Keep request/delivery
multiplicity separately from physical membership. Preserve pair contributors
when deriving unique atomic or residue footprints; residue reduction needs the
owner's explicit atom-to-group correspondence. Contact membership, SASA-loss
membership, topographic support and functional-site identity remain distinct.

### SASA and geometric interface burial

The inspected
[`physchem.get_sasa`](https://github.com/uibcdf/molsysmt/blob/ff25f120243319ca9515009b4971e24a2eb0dc22/molsysmt/physchem/get_sasa.py)
evaluates all input atoms as occluders before selecting/aggregating outputs.
Consequently `get_sasa(AB, selection=A)` measures A in AB; it does not measure
isolated A. Isolated inputs must be produced through an owner-supported
extraction/construction with qualified maps and unchanged admitted coordinates,
chemistry and radius assignments. No silent relaxation, capping, protonation or
hydrogen completion is part of this comparison.

For the same fixed geometry, radii, probe and sampling policy, define:

```text
loss_A = SASA_A(A) - SASA_A(A union B)
loss_B = SASA_B(B) - SASA_B(A union B)
total_burial = loss_A + loss_B
mean_side_area = total_burial / 2
```

Both side losses remain inspectable; equality is not assumed. The mean is a
named reporting convention. Atomic/residue contributions sum to the relevant
side and aggregate within the admitted error. A later comparison of A+C with
A+B+C is a conditional-environment observable with a different definition;
pairwise burial need not add in an assembly and is not thermodynamic cooperativity.

The inspected native SASA route obtains `definition="vdw"` radii internally;
it does not expose an arbitrary caller radius-array argument. Bind the actual
provider resource/model and supported chemistry before qualification. An
alternative radius model needs a concrete owner-supported route. Select
`engine="MolSysMT"`, Cartesian `pbc=False`, effective sampling/probe and CPU
settings explicitly for the first profile rather than inheriting an ambient
engine, periodic or parallel choice. Sampling convergence, rigid-rotation
tolerance, negative-loss diagnosis and the positive-burial membership threshold
are still owner decisions, not invented constants in this review.

[`physchem.get_area_buried`](https://github.com/uibcdf/molsysmt/blob/ff25f120243319ca9515009b4971e24a2eb0dc22/molsysmt/physchem/get_area_buried.py)
returns a Rose residue reference table as plain values documented in angstrom
squared. It is not this coordinate-dependent SASA-loss calculation and cannot
replace it because its name contains "buried". No defect in that table API is
alleged. Reuse public SASA operations where sufficient; an independently useful
surface-decomposition operation belongs in MolSysMT if a real gap is established.

## Maps, quantities, outcomes and saved evidence

Footprint membership is unique original-source membership in ascending order
within an identified source axis. Its local-index vector follows the same
ordering through the qualified map; never sort those two vectors independently.
Keep every contributing pair/analysis/occurrence separately. An original
structure 2 mapped to local 0 stays explicit. Unknown, unmapped and generated
atoms cannot acquire original membership merely because numeric indices agree.

Use PyUnitWizard's supported quantity/record route for measured distances and
areas. The reader checks field identity and length versus area dimensionality.
Conversion names the target unit explicitly under default and nondefault
application policies. Preserve the actual producer values/units and scientific
definition alongside any requested reporting units; a standardization preference
does not determine an independent reader's scientific meaning.

| Observed situation | Required distinction |
| --- | --- |
| Nonempty resolved participants, successful calculation, no contacts | Completed evaluated zero, with empty footprints |
| Empty request or required empty/unresolved participant | Invalid request or missing prerequisite, not completed zero |
| Unknown radii/chemistry, unsupported method or unrequested observable | Explicit unavailable/unsupported/unevaluated state; no fabricated numerical zero |
| Required child calculation fails | Preserve original failure/cause; no complete-success parent |
| Saved successful or zero result, external owner asset later unavailable | Preserve the original outcome; explicit recovery can separately fail |
| Saved original C0 match, current edited C1 supplied | Original check remains historical; fresh requested use checks its admitted dependencies or refuses |

Declaration/composition, explicit calculation, native recovery and new use are
separate operations. Summary, ordinary read and copying perform no molecular
calculation or remote discovery. Save/read preserves original producer identity,
outcomes, maps, quantities, criteria and bibliography. Positive and evaluated-empty
derived footprints need their own admitted public save/read, not only a parent
record. `preserved_evidence`, `molecular_correspondence` and `current_finding`
remain proposed BindingMT assurance names: implementing one does not qualify
another, and a handle or unchanged footprint does not establish a complete
finding's current applicability. Unsupported stronger requests refuse explicitly.

Credit only methods actually reached at their meaningful completion boundary,
including successful zero-result calculations. Public native algorithms retain
their own references; no PISA execution is implied. Reuse, failed operations,
optional attribution absence/failure and fresh saved readers must preserve
original execution history without new originating credit. Existing Ackredit
client rules apply; this review does not certify each provider's attribution.

## Independent acceptance examples

These are proposed control expectations, not a delivered serialized format or
an executed BindingMT/MolSysMT scientific receiving result.

| Control | Exact expectation / reason |
| --- | --- |
| Cartesian A source atoms 8 at x=0 and 2 at x=3; B atoms 30 at x=3.5 and 10 at x=1, all y=z=0, in nm; synthetic cutoff 1 nm | Exactly pairs (8,10) and (2,30), distances 1 and 0.5 nm. Equality is included; the synthetic cutoff selects no application default. |
| Same contact case with local input order [8,2,30,10] | Source footprints [2,8] / [10,30] map to aligned local [1,0] / [3,2]. Independent sorting would corrupt correspondence. |
| Repeated delivery of the same pair | Contributor/delivery history is retained without creating another unique physical contact. |
| Move B far enough for no cross-occlusion | Completed no-contact; zero burial only where the radius/probe assumptions prove no cross-occlusion. |
| Synthetic area bookkeeping: A isolated 10, A in AB 8, B isolated 12, B in AB 9, all nm squared | Side losses 2 and 3; total 5; mean 2.5. This tests reporting convention, not molecular SASA accuracy. |
| Isolated admitted sphere | Independent reference `4*pi*(radius+probe)^2`, with defined quadrature tolerance |
| Two admitted spheres | Independent spherical-cap/containment/separation references, sampling convergence and selected-output versus occluder controls |
| Reordered/extracted context and original structure 2 to local 0 | Exact original/local membership, structure/state/frame and contributor correspondence survive |
| Unrelated C-D and internal A-B evidence in a receptor-C question | The admitted owner query excludes those observations without splitting required compound chemical participants |
| Default and pm/fs policies; positive/empty footprint save/read | Physical lengths/areas, definitions, identity, complete contributors and no-new-calculation/credit behavior agree |
| Relevant context edit, missing proof or unsupported stronger assurance | Affected use refuses or reassesses; original evidence remains inspectable |

Owner tests freeze expectations and tolerances before interpreting outputs.
Start with small serial controls under explicit resource budgets; do not add a
scientific campaign, full suite per internal push or another molecular kernel.

## Finite decisions and receiving state

| Decision / evidence | Received disposition | Remaining owner scope |
| --- | --- | --- |
| Ownership and optional enrichment | MolSysMT owns molecular tools/maps/chemistry; TopoMT its regional supports/associations; BindingMT the selected binding question/composition. TopoMT, PHMT and PeptideMT favor revision 4 without another general design iteration. | Favorable planning does not establish each consumer's adoption. TopoMT #60/#61/#62/#198 retain their actual regional guarantees. |
| Public contacts/distances and maps | Closed MolSysMT #734 supplies the restricted Cartesian public-call contract; BindingMT's first native contacts and independent footprint source profile is delivered. Explicit inclusive cutoff, all-cross endpoints and distances stay distinct. | No universal application cutoff, automatic chemistry admission or installed/public pairing is inferred. |
| Actual chosen frame/state | BindingMT #117 corrects participant resolution to the chosen frame and associated chemical state, refusing unavailable associations through MolSysMT. | Historical earlier records stay historical; a fresh calculation is required to correct an affected result. |
| SASA contexts, radius/H model and side losses | Molecular owner confirms extraction/permutation/map composition and actual bundled element-vdW SASA. BindingMT N2 receives independent A/B/A-union-B contexts, supplied H and both signed losses/total/mean. | Other environments, radii, PBC/GPU/covalent/large profiles require their own admission. Generated atoms cannot acquire invented original-source identities. |
| Probe/density and numerical meaning | Caller explicitly supplies probe and sampling. BindingMT admits roundoff diagnostics and independent analytic patch-budget controls for its first profile. | These are not physical uncertainty, a universal convergence guarantee or positive-area footprint membership. |
| Portable results and saved evidence | BindingMT source profiles receive typed native results, independent positive/empty footprints, explicit record ordering, structured option refusals and cold reading without new molecular work. | Experimental owner records do not become a shared central schema or stable/public/platform guarantee. PyUnitWizard #156/#158 keep their separate scopes. |
| Optional saved PISA | BindingMT c09c6f90302e3b726371b1869afa33749235179c receives actual public TopoMT intake and original-source reported-contact footprints, with original outcomes/attribution retained. | No originating PISA execution, native-method equivalence, transferred/current-finding or installed/public proof follows. |
| Dependency graph | #204 records BindingMT→TopoMT as a reviewed optional `runtime-integration`, with actual soft availability declaration and lazy public calls. Package requirements/extras remain unchanged. | No public provider floor, extra or compatible installed pair is fabricated. |
| Actual P consumer cases | Existing PeptideMT #60 requests exact P1/P2/P3 inputs, maps, independently expected outcomes and public export seams, or an owned unsupported/deferred disposition. | Those actual owner inputs and per-consumer acceptance remain pending; a central synthetic substitute is not adoption. |

## Immutable owner receiving — 2026-11-15 Mexico City / 2026-11-16 UTC

The [source and limits receipt](rollouts/native_interface_owner_receiving_195_20261115.json)
binds fourteen inspected files to complete Git blob/SHA256 values. The
[molecular-owner contract](https://github.com/uibcdf/molsysmt/blob/04bf56131fd0cea94359e1f0f9307d0f0e36b3cb/devguide/native_interface_contacts_sasa_contract.md)
and original receipt are published at 04bf56131fd0cea94359e1f0f9307d0f0e36b3cb.
Their execution receipts retain checkout base 501e02b40e409ad08fda2885a143e8fda6897dbd
and the frozen controlled provider composition; do not relabel 104 cases per unit
policy as an exact clean 04bf561 installed/native matrix. The unchanged molecular
operation files are explicitly identified. No concrete new generic operation gap
is established for this first profile.

The [BindingMT contact](https://github.com/uibcdf/bindingmt/blob/3102de830129d24a0ba9bee6b5c23b118b81dade/devguide/binding_interface_contacts.md)
and [surface](https://github.com/uibcdf/bindingmt/blob/3102de830129d24a0ba9bee6b5c23b118b81dade/devguide/binding_interface_burial.md)
contracts report 187 and 238 affected cases per normal/pm-fs policy respectively.
They have overlapping scope and are not additive independent coverage. Native
extraction sorts retained atoms; when a particular local order is required, use
the complete public permutation and explicit composed maps. Do not assume the
requested extraction order becomes the delivered local order.

Later immutable owner corrections are received separately: participant frame/state
#117 at 47090f8af425896e9e243047bcac537ebd2c68b3, the copyable Site/Interface
walkthrough #118 at abc0af924161ad698d5416f7f029d508e3435436, and malformed saved
options #120 at ea8ed0cdce3881a408ad17050746bb95531df7f8. The owner reports
138/17/268 affected source cases in their stated populations, retaining the
original red controls and failed setup/harness attempts. These source checks do
not overwrite historical producer/native identities or claim a full suite.

The [optional original-result worksheet](https://github.com/uibcdf/bindingmt/blob/c09c6f90302e3b726371b1869afa33749235179c/devguide/binding_interface_topomt_receiving.md)
receives experimental Interface 0.6/Footprint 0.2 under source
c09c6f90302e3b726371b1869afa33749235179c. Actual development inputs are TopoMT
e7a3052d949f207241e602bea3728d43427aca20 and MolSysMT
6deb0200cd7e384128eded46caaf751a57e65bc6. The owner reports 467 affected cases
per unit policy, 118 new cases per policy with SDK-staged support, and 24 cold
reads of eight actual records. Repeated policies and staged support do not
multiply independent scientific coverage. Original record-producing fingerprints
and base d2a0085c682da1391c02ffc6ca5ee914824522de remain distinct from the later
receiver. No component scientific test or hosted workflow is rerun centrally.

The molecular-owner reference native SHA256 4ffb82e4250a1862fff17dbe7725fb8f0770d613ffef2648370389a66983d345
and BindingMT's historical loaded native SHA256 2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038
are different. Published source/package versions do not authenticate the native
builder; that uncertainty and installed/platform/public scope remain visible.

**#195 remains partial** for actual shared/per-consumer acceptance, especially
PeptideMT #60. The finite molecular-owner review is received and no longer a
pending blocker. Optional regional qualification does not block the native
baseline. Preserve #82's prefix pause, all primary/human work and the existing
scientific/publication deferrals.

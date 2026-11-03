# Python license metadata and compatible build tools

MolSysSuite #162 coordinates this packaging migration. This reference applies
when preparing or reviewing license metadata; it is not a new universal gate or
an instruction to republish existing files. Components retain their actual
licenses, notices, source/build profiles and owner-reviewed release timing.

## Metadata and backend compatibility

For a PEP 639 metadata migration, record the actual SPDX expression and explicit
license-file patterns, remove redundant deprecated license classifiers, and align
the build backend's declared capability with the fields being used. Preserve
third-party notices and any multiple-license expression; do not infer a license
from the repository name or mechanically replace every declaration with MIT.

For Setuptools, SPDX strings and `project.license-files` are supported from
77.0.0. The official [migration guide](https://setuptools.pypa.io/en/latest/userguide/license_migration.html)
requires a compatible build minimum; its
[77.0.3 history](https://setuptools.pypa.io/en/latest/history.html#v77-0-3)
records early license-handling corrections. The suite starter uses the locally
qualified **`setuptools>=77.0.3`** floor, without an upper bound or exact default
pin. Existing `>=77.0` declarations are not automatically noncompliant merely
because they differ from this starter patch choice. Other backends use their
own documented feature minimum and qualification.

Example for a project whose actual license is MIT and whose notice is `LICENSE`:

```toml
[build-system]
requires = ["setuptools>=77.0.3", "versioningit"]
build-backend = "setuptools.build_meta"

[project]
license = "MIT"
license-files = ["LICENSE"]
```

This changes build metadata, not `requires-python` or runtime provider floors.
Review explicit Conda build/host and development/test tools too: a route using
`--no-build-isolation` cannot rely on an unrelated newer backend supplied by a
different environment. Preserve scientific/native constraints and versioning
plugins; a minimum change does not qualify their complete tool matrix.

The [PyPA specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/#license-files)
defines the fields and matching/inclusion rules; [PEP 639](https://peps.python.org/pep-0639/)
does not choose a license for a project. A missing explicit `license-files`
declaration is not proof that an old archive omitted its license: backend
defaults and actual bytes must be inspected separately.

## Starter behavior and original notices

New generated Python repositories keep the seed's existing MIT choice, use the
SPDX fields and include the exact MolSysSuite seed `LICENSE` notice. Its copyright
is preserved. Owners review their actual project/author/third-party notices before
release; they do not replace an existing component's license with the seed notice.
The two generated Conda fixture profiles use the same backend floor.

The real distribution guard
`tests/test_starter_distribution.py::StarterDistributionTests::test_generated_sdist_and_rebuilt_wheel_include_declared_license`
builds a generated Git fixture, checks `License-Expression: MIT` and
`License-File: LICENSE`, compares actual sdist/wheel notice bytes with the seed,
and rebuilds a wheel from the sdist. It also rejects admitting a known
pre-feature Setuptools version. It failed before repair because the built wheel
had no SPDX expression. This is an administrative starter fixture, not a member
scientific build, actual release or public installation.

## Owner receiving and evidence

For an existing component, reuse its relevant open packaging issue or create a
focused owner review if none exists. Before edits, record the source, current
license choice, backend/versioning requirements, actual notice files and affected
build routes. An older-tool exception needs the owner, reason, retained metadata
route, review/removal condition and existing policy exception process; do not
silently claim unsupported fields work.

After a change, receive wheel and sdist metadata and actual license-file payloads,
including a wheel rebuilt from the sdist. Distinguish an observed build using a
new backend from a deliberately tested minimum. Keep exact backend/interpreter,
input and output identities and install/dependency limits. Real native builds,
installed/runtime/platform/scientific and public-file gates remain owner-local.
Do not rebuild, relabel or replace an already qualified/published file to update
its metadata; a future candidate follows the existing release route.

Current source inspection covers fifteen public Python members and a sanitized
private-owner route. Four already have modern compatible declarations, two have
modern fields with a pre-feature direct backend floor, and nine retain legacy
tables. These are declaration observations, not universal package defects or
instructions to release. MolSysMT #541, MolSysViewer #292 and DockingMT #47 are
existing concrete owner routes. Other component adoption remains coordinated in
#162; avoid duplicate issues and preserve early-development deferrals.

[Source inventory and starter qualification](rollouts/license_metadata_starter_162_20261103.json)
retain the before-fix regression, exact-minimum build and current-tool build scopes.

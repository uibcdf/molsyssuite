# Optional shared Conda environment tools

This additive SDK capability implements MolSysSuite #108. It is available to an
owner with a reviewed `molsyssuite.dependency-routes@3` inventory; it does not
mandate migration from qualified local tools or change CI/publication policy.
Owner tooling, selected outputs, native constraints and scientific decisions stay
in the component. Unsupported expressions or specialized document fields require
owner review or a qualified local exception, not a guessed successful conversion.

## Inputs and pure generation

`devtools/scripts/conda_environment_tools.py` exposes `environment_documents`,
`generate`, `selected_environment`, `observe_channels` and `apply_environment`. The first operation
returns validated YAML strings without writing or invoking a manager. `generate`
validates **every** selected output before writes; `check=True` fails on drift and
never writes. Existing environment files must be registered, directly present in
`devtools/conda-envs/` and not symlink aliases. Unselected files stay byte-identical.
Validation failure is non-mutating; ordinary I/O failure during a multi-file write
is not a transactional rollback, so review the diff before committing.

A local `devtools/environment_tools.toml` selects a tooling YAML and outputs:

```toml
schema = "molsyssuite.environment-tools@1"
tooling = "devtools/requirements.yaml"
inventory = "devtools/dependency_routes.toml" # default

[[environments]]
path = "devtools/conda-envs/production_env.yaml"
group = "production"
reason = "Reviewed public dependency declaration"

[[environments]]
path = "devtools/conda-envs/development_env.yaml"
group = "development"
python_minor = "3.14"
reason = "Routine development with owner tools"
```

Each tooling group contains `channels` and `dependencies` lists. Nested lists are
flattened without executing configuration. Runtime groups contain **tools only**:
metadata owns all runtime bounds and Python; reviewed source contexts own omitted
bootstrap requirements and overlays. Build-only groups may include libraries
needed as build tools, without asserting that they are package runtime. Channels
must equal the existing reviewed document. Runtime validation delegates to the
existing source/context proof, including source manifests and their hashes.

Generation preserves existing version/build restrictions for every dependency it
retains. An explicitly selected whole minor must fit both package metadata and
the existing Python selector; patch floors, incompatible build selectors or a
widened range fail. Routine development selects Python 3.14. With no minor given,
generation uses metadata's range; if that would widen an existing selector, supply
a reviewed minor or keep the specialized file outside generation. Different source
contexts requiring different bootstrap documents cannot share a generated output.

Only registered runtime/build-only documents are supported. Recipes (including
Jinja), release plans, Git manifests, resolved-package fixtures and unselected
scientific environments are not generation targets. A first owner adoption must
explicitly review its selection; the tool cannot infer which scientific inputs
are safe to rewrite. Changing an owner selector deliberately is separate work.

## Checked create/update

CLI examples use an immutable, qualified SDK checkout; owner wrappers may fix its
path and inject `--root` but must verify the SDK identity/import origin:

```bash
python SDK/devtools/scripts/conda_environment_tools.py --root COMPONENT generate --check
python SDK/devtools/scripts/conda_environment_tools.py --root COMPONENT create \
  devtools/conda-envs/production_env.yaml --python-minor 3.14 \
  --manager mamba --name component-dev-3.14
python SDK/devtools/scripts/conda_environment_tools.py --root COMPONENT update \
  devtools/conda-envs/development_env.yaml --python-minor 3.14 \
  --manager conda --prefix "$CONDA_PREFIX"
```

A manager command/path is explicit, resolved as an executable; there is no manager
selection at import time. Create checks the manager's environment inventory and
requires a new, unoccupied name (never `base`). Update requires the requested
prefix, `CONDA_PREFIX`, this interpreter's `sys.prefix` and a Conda metadata
directory to agree. It does not add `--prune`; unrelated active tools are not
implicitly removed. Both use argument vectors, checked return codes and strict
channel priority. A temporary YAML drops input name/prefix, remains outside the
owner tree and is cleaned on success and failure. Neither operation rewrites the
original file nor changes the process working directory.

The requested minor must fit the complete existing selector and metadata. Fixed
Git source contexts additionally require a matching reviewed minor. Source-free
selection can narrow a supported minor; this is a declaration selection proof,
not a new installed-context receipt. All declared runtime requirements, channels
and reviewed overlays are validated before manager invocation. Imports are inert.

## Channel receipts and optional restriction (#116)

`apply_environment(..., channel_policy="configured")` remains the default. It
preserves the existing owner document and manager inheritance, including an owner
`nodefaults` sentinel if already present. Strict priority orders eligible channels;
it does not itself remove inherited channels. Owners may retain specialized
declared channels and qualified local tools; this capability adds no common gate.

The additive `channel_evidence` result uses `molsyssuite.channel-evidence@1`:

| Field | Meaning |
| --- | --- |
| `declared` | Literal ordered owner YAML entries, including any existing sentinel |
| `policy`, `priority_requested` | Requested operation policy and strict priority |
| `adapter` | Qualified restriction adapter identity, or null for configured mode |
| `manager.family`, `manager.version` | Recognized public version response, or unknown/null |
| `manager.configuration` | Time-qualified pre-operation observation, or unknown with reason |
| `manager.effective` | Explicitly unknown: this operator does not inspect actual solver inputs |
| `invocation`, `manifest_sha256` | Executed argument vector and exact private manifest digest |

`observe_channels(executable, environment)` is independently usable and inert until
called. It queries the public version and only `channels` configuration for recognized
Conda/Mamba shapes. Each diagnostic query has a ten-second timeout. Locations are
represented by `<redacted-channel-location>`; raw responses, credentials, unrelated
configuration and diagnostic exception text are not returned. Configuration evidence
does not resolve aliases/multichannels or establish a target solver invocation. Failed,
malformed or unsupported observations return unknown and do not block configured
operations. Actual inventory/create/update failures continue to propagate.

Opt in through the keyword or matching `--channel-policy declared-only` CLI selector.
The qualified adapter adds `nodefaults` only to the private execution YAML, without
duplicating an owner sentinel or changing dependencies, pip sections or reviewed
sources. It restricts Conda solver channel inputs; it does not isolate other settings,
pip indexes, package caches or already installed packages, nor certify artifact origins.
Declared logical names may resolve through manager aliases; the receipt does not guess
their URLs. Consumers still need their existing installed/context checks.

Currently qualified: **Mamba 2.9.0, Linux x86_64, `create` only**, adapter
`mamba-2.9.0-linux-x86_64-create-nodefaults@1`. Unknown/other versions, Conda,
Micromamba, other architectures/platforms and every update refuse an exclusive
request before any inventory/create/update execution. Their configured route remains
available. Version/platform expansion requires native positive/negative and relevant
cache/operation controls; support for create does not qualify update. No global RC
editing, TLS disabling or silent fallback is allowed.

[Native qualification](rollouts/channel_policy_qualification_116_20261013.json)
executes the actual SDK and manager against private HTTP channels: inherited-only
archives install by default; exclusive cold/warm-cache controls reject them; identical
bytes install from a declared additional channel. Those are synthetic transaction
fixtures, including a synthetic Python record with **no Python executable**. They
prove the bounded channel route, not a real component environment or scientific Python.
Directories/server/cache are retired, and the manager inventory retires absent fixture
registrations. No caller environment or scientific suite is modified.

Run the native guard explicitly where the exact manager is available:

```bash
MOLSYSSUITE_MAMBA_116=/explicit/path/to/mamba python -m unittest \
  tests.test_conda_environment_native.NativeChannelPolicyTests -v
```

The ordinary offline guard covers receipt privacy/unknowns, compatibility, private
manifest preservation, source/pip inputs, unsupported refusal, failures and cleanup.
The native guard is skipped when not explicitly selected; that skip is not new manager
qualification. Adoption uses an immutable qualified provider revision, with local owner
notice and consumer validation separate from this shared capability.

## Evidence and adoption

`tests/test_conda_environment_tools.py` guards protected paths, selective outputs,
metadata propagation, drift/all-output validation, retained ranges, source drift,
manager failures/identity, strict priority, cleanup and inert imports. These tests
qualify administrative behavior; they neither solve a real environment nor run a
scientific suite. After an actual manager operation, run the existing installed
context preflight, `pip check`, import-origin checks and the owner's applicable
science/native checks. A successful manager exit alone is not that evidence.

Publish the shared commit with its executed qualification, give consumer notice
under the shared-provider rule and adopt only that immutable commit. Existing
publication callers may retain a separately qualified pin. Distinguish notice,
source adoption, actual environment checks, candidate/install gates and public
artifact evidence. Local qualified tools may remain in use; log unsupported needs
in their owning issue and cross-link the shared provider when reusable capability
is missing. Initial consumer: uibcdf/pharmacophoremt#10; potential reuse remains
uibcdf/elastnetmt#18, uibcdf/lindelint#13 and uibcdf/topomt#78.

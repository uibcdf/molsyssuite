# Shared development tools

Use existing supported operations before adding component-local copies, under
[the modular-tool policy](modular_reusable_tools.md). This catalogue makes
available tools discoverable; it does not require adopting every SDK, changing
qualified local implementations or installing unused runtime dependencies.

| Need | Existing owner tool and maintained contract |
| --- | --- |
| Inspect component clone state | `devtools/scripts/suite_status.py`; [cross-repository working state](../MOLSYSSUITE_GUIDE.md#cross-repository-working-state). |
| Find dependency impact and provider-first layers | `devtools/scripts/dependency_graph.py`; [typed graph contract](dependency_graph_policy.md). |
| Install/verify eligible shared-workspace editables or explicitly reinstall local sources | `devtools/scripts/development_environment.py`; [workspace contract](development_workspace.md). Profile eligibility and actual receiving remain separate. |
| Check metadata, environment, recipe or immutable source routes | Shared [dependency-route preflight](dependency_route_preflight.md), with reviewed owner inventory and explicit immutable SDK adoption. |
| Generate selected Conda environments or safely create/update them | [Optional environment-tools SDK](conda_environment_tools.md): owner-selected outputs, checked manager/target identity, truthful channel receipts and qualified optional restrictions. |
| Build, qualify and promote a noarch Python file | [Noarch workflow](noarch_conda_workflow.md), [release operator](noarch_release_operations.md) and [publication contract](conda_publication_policy.md). Installed helper support remains a declared, bounded route. |
| Review bundled ABI3 recipe declarations | [Native ABI3 tools](native_abi3_conda_workflow.md); native artifact/scientific qualification stays component-owned. |
| Receive command evidence from an existing public noarch file | [Public command receiver](public_noarch_commands.md); it does not replace full installed publication gates. |
| Synchronize/read adoption of canonical guides | `sync_vendored_guides.py` and `adoption_status.py`; [copy ownership](vendored_guides.md) and [adoption lifecycle](adoption_lifecycle.md). Run central tools from their owning clone. |
| Generate truthful README identity/coverage surfaces | `repository_badges.py` and the [badge/coverage policy](repository_badges.md); service evidence remains separate. |
| Inspect tests or Actions | Registered Pytest Receptor / GH Run Receptor guides; [applicable tooling](../MOLSYSSUITE_GUIDE.md#applicable-support-libraries-and-developer-tools). |

Follow each tool's actual inputs, platform/version/operation limits and qualified
source before calling it. Preserve the component's scientific environments,
native constraints and publication pins. Availability is not adoption; a source
or guide update does not qualify a new runtime/artifact or manager operation.

The environment-tools contract also owns the monitored Mamba compatibility range
and future-major release notice. Its optional channel restriction is qualified
only within that contract's declared boundary. Strict channel priority does not
by itself exclude inherited channels. Do not infer a suite-wide Mamba mandate,
an unrestricted update operation or new-major qualification from this catalogue.

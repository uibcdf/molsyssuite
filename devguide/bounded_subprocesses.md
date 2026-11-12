# Bounded local receiving subprocesses

Under #173, `devtools/scripts/bounded_subprocess.py` provides an optional,
stdlib-only Linux function. It is independently useful without the publication
SDK, a molecular import, a scheduler or a runtime dependency. Source inspection
of BindingMT's frozen interim guard motivated the shared controls; the original
producer and historical scientific results are not rewritten.

## Supported boundary

Use one single-threaded trusted supervisor and a caller-owned command, working
directory, environment and new attempt directory. Linux `/proc`, process groups
and `waitid(WNOWAIT)` are required; other platforms return a retained unsupported
preflight result. The unreaped session-leader PID reserves the group identity
until cleanup, including after leader exit. TERM is followed by KILL of surviving
owned members, never another process group. A failed/unknown cleanup cannot pass.

This is not a security sandbox. Commands escaping the owned session, external
reaping of its leader, supervisor SIGKILL/runner loss and hostile code are outside
the guarantee. Use an owner-qualified cgroup/container route where hard aggregate
containment or those lifecycle guarantees are needed. Caller thread/worker and
scientific allocation choices remain explicit; no whole-machine default exists.

`Limits` requires finite wall/CPU/address-space/RSS/reserve/log bounds and explicit
available CPUs. Affinity, non-increased priority and per-process CPU/address-space
rlimits are applied in the child. Group RSS, available memory, logs and aggregate
observed CPU are sampled, with possible overshoot and short-lived unobserved
members. RSS sums shared mappings; these observations are not PSS or peak/hard
cgroup accounting. Timer interruption is a supervisor observation, never inferred
from exit 124 or a GitHub cancellation. No retries, dependency changes, CI dispatch,
shared-cache deletion or automatic scientific acceptance occur.

## Calling the function

Pin a reviewed immutable SDK/helper source. Supply its independently retained
SHA-256 to `execute`; `source_digest()` checks the actual imported module file.
Declare the frozen `worker` and all relevant executable cells/input manifests as
`inputs={name: {'path': path, 'sha256': reviewed_digest}}`. The tool verifies these
before launch and after a completed command before semantic qualification. This
binds declared files, not an authenticated or complete dependency closure.

```python
receipt = execute(
    argv, cwd=working_directory, env=caller_environment,
    limits=reviewed_limits, attempt=new_owned_attempt,
    profile="normal", helper_sha256=reviewed_helper_digest,
    inputs=frozen_inputs, validate=component_final_receipt_validator,
)
```

The component's required validator reads its actual final receipts and checks the
complete expected selection, profile, identities and scientific acceptance. It
returns a JSON object with `state="passed"` only after those checks. No validator
or a zero process exit supplies a default PASS. The tool retains process status,
resource interruption, lifecycle cleanup and semantic result as separate fields.
Inspect the top-level `state`; only `qualified` accepts this bounded receiving.

For a dependent nondefault profile, add
`prerequisite={'path': normal_receipt, 'sha256': reviewed_receipt_digest,
'profile': 'normal'}`. It must be a completed `qualified` receipt bound to the
same helper and frozen worker/cells, with terminal cleanup. A random prior PASS
or a changed composition fails admission. The component still verifies actual
profile/selection semantics; the supervisor does not invent a scientific schema.

Every admitted new attempt retains `stdout.log`, `stderr.log`, `receipt.json`
and `error.log` on preflight/launch/validator failure. Existing directories are
refused, never overwritten. Raw records may contain caller paths/error text;
review/sanitize them before public reporting. Environment values are not dumped.
Keep needed evidence and use the normal owner-controlled temporary-resource
lifecycle after publication. Generic source/helper hashes are not authentication.

## Qualification and adoption

Real inert controls cover complete and missing semantic selection, raw exit 124,
low headroom, actual helper mismatch, launch failure, invalid finite limits,
matching/stale normal-profile composition, child OS limits and parent preservation,
an exceeded log bound after fast exit, wall interruption and leader-exit/stubborn-
child retirement with an unrelated sentinel. The frozen BindingMT validator can
be used as the caller callback without importing its molecular worker.

These are mechanism controls, not scientific reruns or new interpretation of old
results. BindingMT #80 owns future adoption in its receiving harness; existing
qualified owner launchers need no automatic replacement. SMonitor's optional
profiling remains a separate measurement capability. Global operation-timeout
instrumentation under #25 stays deferred.

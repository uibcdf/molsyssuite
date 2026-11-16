# Resource-aware contributor execution

Accepted for every member under uibcdf/molsyssuite#197. MolSysSuite owns this
member working rule and its receiving. It adopts the general MolI #96 action
reviewed at `dd4ac1301b092038934b594afbf7ec559ab20a1b`:
[platform rule](https://github.com/uibcdf/moli/blob/dd4ac1301b092038934b594afbf7ec559ab20a1b/devguide/policies/resource_aware_execution.md).
Infrastructure owners retain host configuration, scheduler/admission mechanisms,
numeric site limits, enforcement, deployment and operational recovery. This is
an instruction contract, not an implemented reservation service or runtime API.

## Before expensive work

Apply this rule to material test, build, benchmark, simulation, inference,
dependency-solver and data-preparation jobs. Ordinary reads and edits need no
reservation ceremony. Before an expensive job:

1. Identify the actual environment and the trusted operator/project route to its
   active execution policy. Read and apply the policy, recording its revision or
   digest and scope. A link alone is not policy loading. Unavailable required
   policy or conflicting constraints defers the affected expensive work until
   the owner resolves it; it does not block unrelated lightweight work.
2. Estimate the whole process family's RAM, CPU/process/thread fan-out,
   accelerator memory, scratch/I/O and duration where relevant. Include pytest
   workers, native BLAS/OpenMP, browsers, compiler/solver workers and child jobs.
   Distinguish measurements, estimates and unknowns; a launcher limit alone does
   not describe its children. Use the component's measured input/environment
   profiles where available; otherwise start with a small bounded probe or defer.
3. Inspect current authorized resource/pressure observations, running work and
   known reservations. Preserve the site's reserve for the OS, access/interactive
   sessions and other users. Available RAM or idle CPUs are observations, not
   reservations or protection against another agent starting work.
4. Use required scheduler/admission routes and their actual allocation. On a
   permitted direct route, select explicit bounded concurrency, budget, monitoring
   cadence and pressure/budget stop conditions under the active site policy.
   Unknown demand never justifies selecting every reported CPU. No suite-wide
   RAM fraction, worker count, host path or scheduler implementation is imposed.

## Execution, containment and recovery

Distinguish observed availability, cooperative reservations and enforceable
whole-family containment. Record which are actually provided. Do not bypass a
required scheduler because a machine appears idle or claim concurrent admission
from independent preflight observations. Required unavailable protections mean
reduced scope or deferral, with the missing capability and owner explicit.

Monitor pressure and the agreed budget. Bound admission waiting; on expiry return
a deferred outcome, reason, owner and retry trigger. Reduce supported work or
cancel only the owned workload through its approved route on a stop condition.
Prefer graceful interruption and retain useful permitted partial evidence.
Never terminate unrelated work, clear another task's scratch or reconfigure the
host to rescue a check. Escalation/orphans and uncertain termination go to the
infrastructure owner; do not release an owned reservation until termination is
confirmed, or record the cleanup uncertainty for the operator.

Keep completed, deferred, rejected, interrupted, cancelled and failed outcomes
distinct. OOM, incomplete artifacts and interrupted execution are not successful
tests or scientific results. Preserve original attempts and actual limits;
do not automatically retry into unchanged pressure. Follow the
[temporary-resource lifecycle](temporary_resources.md).

## Ownership, tools and receiving

The canonical guide's resource section is mandatory through existing root/nested
instruction precedence. Both existing components and official starters receive
that common route; a delivery or structural route check does not prove execution
protection or semantic adoption. Root instructions may add local workload and
command guidance. [Workload profiles](workload_profiles.md) distinguish measured
central examples from component-owned estimates and missing capabilities.

Published Pytest Receptor and GH Run Receptor retain their reporting roles;
their defaults do not override resource budgets or required evidence scope.
Infrastructure integration is optional for eligible local work when the site's
policy permits bounded direct execution. No UIBCDF-specific package becomes a
scientific runtime dependency. Policy loading authorizes no remote code execution,
credential access, provisioning or expansion of existing task authority.

MolI's [integration proposal](https://github.com/uibcdf/moli/blob/dd4ac1301b092038934b594afbf7ec559ab20a1b/devguide/pending_proposals/execution_infrastructure_contract.md)
is design review material. No serialized protocol, automatic policy discovery,
admission adapter or host-protection guarantee is implemented by this adoption.
UIBCDF infrastructure #1 owns the reference provider; communicate concrete suite
requirements there rather than implementing competing execution/scientific models.

An owner receiving record identifies policy/input revision, workload/estimate,
actual allocation/protection, outcome and cleanup/deferral. Keep outstanding member
reviews explicit in #197/#201. Historical runs and copied instructions do not
retroactively establish enforcement.

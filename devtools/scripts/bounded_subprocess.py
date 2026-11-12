"""Optional Linux subprocess receiving; component semantics remain caller-owned.

This is a single-threaded trusted-command supervisor, not a scheduler, security
sandbox or scientific validator. Its scope is the new session/process group.
Commands that escape that session are unsupported. RSS/headroom/log/aggregate
CPU limits are sampled observations; address-space and CPU rlimits are per process.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import signal
import subprocess
import sys
import threading
import time
import traceback
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    import resource
except ImportError:  # Import remains possible for a clear unsupported disposition.
    resource = None


@dataclass(frozen=True)
class Limits:
    cpus: tuple[int, ...]
    wall_seconds: float
    cpu_seconds: int
    address_space_bytes: int
    group_rss_bytes: int
    available_reserve_bytes: int
    max_log_bytes: int
    nice: int = 10
    sample_seconds: float = 0.05
    cleanup_seconds: float = 1.0

    def validate(self) -> None:
        if not self.cpus or any(type(c) is not int for c in self.cpus):
            raise ValueError("select explicit available CPU identities")
        if len(set(self.cpus)) != len(self.cpus) or not set(self.cpus).issubset(
            os.sched_getaffinity(0)
        ):
            raise ValueError("CPU selection is unavailable or duplicated")
        for value in (
            self.cpu_seconds,
            self.address_space_bytes,
            self.group_rss_bytes,
            self.available_reserve_bytes,
            self.max_log_bytes,
        ):
            if type(value) is not int or value <= 0:
                raise ValueError("finite positive integer resource limits are required")
        for value in (self.wall_seconds, self.sample_seconds, self.cleanup_seconds):
            if (
                type(value) not in (float, int)
                or not math.isfinite(value)
                or value <= 0
            ):
                raise ValueError("finite positive durations are required")
        if (
            self.sample_seconds > self.wall_seconds
            or type(self.nice) is not int
            or not 0 <= self.nice <= 19
        ):
            raise ValueError("invalid monitoring cadence or priority")


def source_digest() -> str:
    """Hash the actual imported helper, rather than a caller-supplied SDK path."""
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def available_memory() -> int:
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) * 1024
    raise ValueError("Linux available-memory observation is missing")


def group_members(group: int) -> list[dict]:
    """Observe only same-UID members of the new session and group, with start ticks."""
    found = []
    for path in Path("/proc").iterdir():
        if not path.name.isdigit():
            continue
        try:
            if path.stat().st_uid != os.getuid():
                continue
            stat = (path / "stat").read_text().rsplit(") ", 1)[1].split()
            if int(stat[2]) != group or int(stat[3]) != group or stat[0] == "Z":
                continue
            found.append(
                {
                    "pid": int(path.name),
                    "start_ticks": int(stat[19]),
                    "rss_bytes": int(stat[21]) * os.sysconf("SC_PAGE_SIZE"),
                    "cpu_seconds": (int(stat[11]) + int(stat[12]))
                    / os.sysconf("SC_CLK_TCK"),
                }
            )
        except (FileNotFoundError, ProcessLookupError):
            continue
    return found


def _exit_code(process: subprocess.Popen) -> int | None:
    """Observe without reaping: the reserved leader PID prevents group-ID reuse."""
    status = os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
    if status is None:
        return None
    return status.si_status if status.si_code == os.CLD_EXITED else -status.si_status


def stop_owned_group(process: subprocess.Popen, grace: float) -> bool:
    """Retire surviving members while retaining the unreaped leader's identity.

    Only this single-threaded supervisor owns/reaps this child. A zombie leader
    still reserves its PID, so the process-group ID cannot be reused by an
    unrelated process between observation and killpg. Reap only after cleanup.
    """
    for sig in (signal.SIGTERM, signal.SIGKILL):
        deadline = time.monotonic() + grace
        while True:
            _exit_code(process)
            members = group_members(process.pid)
            if not members:
                return True
            try:
                os.killpg(process.pid, sig)
            except ProcessLookupError:
                pass
            if time.monotonic() >= deadline:
                break
            time.sleep(0.01)
    _exit_code(process)
    return not group_members(process.pid)


def _input_binding(inputs: dict) -> dict:
    if not inputs or "worker" not in inputs:
        raise ValueError(
            "declare the frozen worker and relevant executable/input cells"
        )
    observed = {}
    for name, item in inputs.items():
        with Path(item["path"]).open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        if digest != item["sha256"]:
            raise ValueError(f"declared input digest changed: {name}")
        observed[name] = digest
    return observed


def require_previous(requirement: dict, binding: dict, helper: str) -> dict:
    """Bind a dependent profile to the same frozen worker/cells and actual helper."""
    with Path(requirement["path"]).open("rb") as stream:
        raw = stream.read(1024 * 1024 + 1)
    if (
        len(raw) > 1024 * 1024
        or hashlib.sha256(raw).hexdigest() != requirement["sha256"]
    ):
        raise ValueError("prerequisite receipt bytes differ")
    previous = json.loads(raw)
    if (
        previous.get("schema") != "molsyssuite.bounded-subprocess@1"
        or previous.get("state") != "qualified"
        or previous.get("profile") != requirement["profile"]
        or previous.get("binding") != binding
        or previous.get("helper_sha256") != helper
        or previous.get("process", {}).get("group_terminal") is not True
    ):
        raise ValueError(
            "prerequisite is not the completed matching composition/profile"
        )
    return {"sha256": requirement["sha256"], "profile": requirement["profile"]}


def execute(
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    limits: Limits,
    attempt: Path,
    profile: str,
    helper_sha256: str,
    inputs: dict,
    validate: Callable[[Path, dict], dict],
    prerequisite: dict | None = None,
) -> dict:
    """Run once; retain preflight/raw/resource/semantic results separately.

    validate is the component's required validator of final receipts, complete
    expected selection and profile. It returns a JSON object with state='passed'
    only after that check. A zero exit alone never invokes a default PASS.
    A caller selecting a dependent profile supplies its exact prerequisite.
    """
    attempt = Path(attempt)
    attempt.mkdir(exist_ok=False)
    (attempt / "stdout.log").touch()
    (attempt / "stderr.log").touch()
    receipt = {
        "schema": "molsyssuite.bounded-subprocess@1",
        "state": "preflight_failed",
        "profile": profile,
        "helper_sha256": source_digest(),
        "process": {"returncode": None, "group_terminal": None},
        "qualification": {"state": "not_run"},
        "resource_interruption": None,
        "limits": {
            k: list(v)
            if isinstance(v, tuple)
            else str(v)
            if isinstance(v, float) and not math.isfinite(v)
            else v
            for k, v in asdict(limits).items()
        },
    }
    process = None
    stage = "preflight"
    started = time.monotonic()
    try:
        if (
            sys.platform != "linux"
            or resource is None
            or not Path("/proc/self/stat").exists()
            or not hasattr(os, "waitid")
            or not hasattr(os, "WNOWAIT")
        ):
            raise ValueError(
                "unsupported platform; Linux /proc, waitid/WNOWAIT and process groups required"
            )
        if threading.active_count() != 1:
            raise ValueError("use a single-threaded supervisor process")
        limits.validate()
        if receipt["helper_sha256"] != helper_sha256:
            raise ValueError("actual imported helper differs from the frozen source")
        if (
            not isinstance(argv, list)
            or not argv
            or any(not isinstance(a, str) or "\0" in a for a in argv)
            or not Path(cwd).is_dir()
            or not isinstance(env, dict)
            or not callable(validate)
            or not isinstance(profile, str)
            or not profile
        ):
            raise ValueError("explicit argv/cwd/environment/profile/validator required")
        receipt["binding"] = _input_binding(inputs)
        if prerequisite is not None:
            receipt["prerequisite"] = require_previous(
                prerequisite, receipt["binding"], helper_sha256
            )
        if available_memory() < limits.available_reserve_bytes + limits.group_rss_bytes:
            raise ValueError(
                "insufficient available memory for reserve and bounded group"
            )

        def child_limits():
            os.sched_setaffinity(0, set(limits.cpus))
            os.setpriority(
                os.PRIO_PROCESS, 0, max(os.getpriority(os.PRIO_PROCESS, 0), limits.nice)
            )
            resource.setrlimit(resource.RLIMIT_AS, (limits.address_space_bytes,) * 2)
            resource.setrlimit(resource.RLIMIT_CPU, (limits.cpu_seconds,) * 2)

        stage = "launch"
        with (
            (attempt / "stdout.log").open("ab") as out,
            (attempt / "stderr.log").open("ab") as err,
        ):
            process = subprocess.Popen(
                argv,
                cwd=cwd,
                env=env,
                stdout=out,
                stderr=err,
                start_new_session=True,
                preexec_fn=child_limits,  # noqa: PLW1509 -- enforced single-threaded supervisor
            )
        receipt["process"]["pid"] = process.pid
        stage = "monitor"
        peak, cpu_samples = 0, {}
        reason = None
        while True:
            code = _exit_code(process)
            members = group_members(process.pid)
            rss = sum(m["rss_bytes"] for m in members)
            peak = max(peak, rss)
            for member in members:
                cpu_samples[(member["pid"], member["start_ticks"])] = member[
                    "cpu_seconds"
                ]
            checks = [
                (
                    code is None and time.monotonic() - started >= limits.wall_seconds,
                    "wall_deadline",
                ),
                (rss > limits.group_rss_bytes, "sampled_group_rss"),
                (sum(cpu_samples.values()) > limits.cpu_seconds, "sampled_group_cpu"),
                (
                    available_memory() < limits.available_reserve_bytes,
                    "available_memory_reserve",
                ),
                (
                    sum(
                        (attempt / name).stat().st_size
                        for name in ["stdout.log", "stderr.log"]
                    )
                    > limits.max_log_bytes,
                    "sampled_log_bytes",
                ),
            ]
            reason = next((name for refused, name in checks if refused), None)
            if reason:
                receipt["resource_interruption"] = reason
                break
            if code is not None:
                if members:
                    reason = "owned_descendants_after_leader_exit"
                break
            time.sleep(limits.sample_seconds)
        terminal = stop_owned_group(process, limits.cleanup_seconds)
        receipt["process"].update(
            returncode=_exit_code(process),
            group_terminal=terminal,
            termination_reason=reason,
        )
        receipt["resources"] = {
            "sampled_peak_group_rss_bytes": peak,
            "sampled_group_cpu_seconds": sum(cpu_samples.values()),
        }
        receipt["state"] = "interrupted" if reason or not terminal else "process_failed"
        if reason is None and terminal and receipt["process"]["returncode"] == 0:
            stage = "qualification"
            if (
                _input_binding(inputs) != receipt["binding"]
                or source_digest() != helper_sha256
            ):
                raise ValueError("frozen inputs/helper changed during execution")
            result = validate(attempt, receipt["binding"])
            if not isinstance(result, dict) or result.get("state") != "passed":
                receipt["qualification"] = {"state": "refused"}
                receipt["state"] = "semantic_refusal"
            else:
                json.dumps(result, allow_nan=False)
                receipt["qualification"] = result
                receipt["state"] = "qualified"
    except KeyboardInterrupt:
        receipt["state"] = "interrupted"
        receipt["error"] = {"stage": stage, "type": "KeyboardInterrupt"}
        (attempt / "error.log").write_text(traceback.format_exc())
        raise
    except Exception as error:  # noqa: BLE001 -- validator/launch failures must retain diagnostics and cannot qualify
        receipt["error"] = {
            "stage": stage,
            "type": type(error).__name__,
            "message": str(error),
        }
        receipt["state"] = "preflight_failed" if process is None else "receiving_failed"
        (attempt / "error.log").write_text(traceback.format_exc())
    finally:
        if process is not None:
            try:
                receipt["process"]["group_terminal"] = stop_owned_group(
                    process, limits.cleanup_seconds
                )
                if receipt["process"]["group_terminal"]:
                    receipt["process"]["returncode"] = process.wait(
                        timeout=limits.cleanup_seconds
                    )
            except Exception as error:  # noqa: BLE001 -- failed cleanup is explicitly unconfirmed, never success
                receipt["process"]["group_terminal"] = False
                receipt["cleanup_error"] = {
                    "type": type(error).__name__,
                    "message": str(error),
                }
            if not receipt["process"]["group_terminal"]:
                receipt["state"] = "cleanup_unconfirmed"
        receipt["elapsed_seconds"] = time.monotonic() - started
        (attempt / "receipt.json").write_text(
            json.dumps(receipt, indent=2, allow_nan=False) + "\n"
        )
    return receipt

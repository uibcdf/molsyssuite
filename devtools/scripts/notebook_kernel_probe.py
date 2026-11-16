"""Receive bounded real-kernel shell/comm interleaving, independently of viewers."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import queue
import sys
import tempfile
import time
from pathlib import Path


def probe(*, cycles: int = 30, deadline: float = 5.0) -> dict:
    """Require correlated replies during/after execution and retire the owned kernel."""
    from jupyter_client import KernelManager
    from packaging.version import Version

    if not 1 <= cycles <= 100 or not 0 < deadline <= 10:
        raise ValueError("probe needs 1..100 cycles and a deadline in (0, 10]")
    version = importlib.metadata.version("ipykernel")
    if Version(version) < Version("7.4.0"):
        raise ValueError("notebook baseline requires ipykernel >=7.4.0")
    prefix = Path(sys.prefix).resolve()
    for name in ("ipykernel", "jupyter_client", "zmq", "comm"):
        module = __import__(name)
        if not Path(module.__file__).resolve().is_relative_to(prefix):
            raise ValueError(f"notebook module is outside selected prefix: {name}")
    environment = dict(os.environ)
    environment.pop("PYTHONPATH", None)
    environment.pop("PYTHONHOME", None)
    environment["PYTHONNOUSERSITE"] = "1"
    environment.update(
        OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1"
    )
    latencies = []
    manager = KernelManager(kernel_name="python3")
    client = None
    with tempfile.TemporaryDirectory(prefix="suite-kernel-") as temporary:
        # Use this interpreter explicitly rather than any user kernelspec's Python.
        manager.kernel_spec.argv = [
            sys.executable,
            "-m",
            "ipykernel_launcher",
            "-f",
            "{connection_file}",
        ]
        try:
            manager.start_kernel(cwd=temporary, env=environment)
            client = manager.blocking_client()
            client.start_channels()
            client.wait_for_ready(timeout=30)

            def receive(channel, predicate):
                end = time.monotonic() + deadline
                while time.monotonic() < end:
                    try:
                        message = channel(timeout=max(0.01, end - time.monotonic()))
                    except queue.Empty:
                        continue
                    if predicate(message):
                        return message
                raise TimeoutError(
                    "correlated native kernel reply exceeded probe bound"
                )

            for cycle in range(cycles):
                request = client.execute(
                    "import time,sys\nfrom comm import create_comm\n"
                    f"cycle = {cycle}\n"
                    "c = create_comm(target_name='molsyssuite-probe', "
                    "data={'cycle':cycle,'python':sys.executable})\n"
                    "def receive(message, c=c, cycle=cycle):\n"
                    "    c.send({'cycle':cycle,'phase':message['content']['data']['phase']})\n"
                    "c.on_msg(receive)\ntime.sleep(0.03)\n",
                    stop_on_error=True,
                )
                opened = receive(
                    client.get_iopub_msg,
                    lambda m, request=request, cycle=cycle: (
                        m["msg_type"] == "comm_open"
                        and m["parent_header"].get("msg_id") == request
                        and m["content"]["data"].get("cycle") == cycle
                    ),
                )
                if (
                    Path(opened["content"]["data"]["python"]).resolve()
                    != Path(sys.executable).resolve()
                ):
                    raise ValueError(
                        "kernel interpreter differs from selected interpreter"
                    )
                comm_id = opened["content"]["comm_id"]
                for phase in ("during", "after"):
                    sent = time.monotonic()
                    client.shell_channel.send(
                        client.session.msg(
                            "comm_msg",
                            {"comm_id": comm_id, "data": {"phase": phase}},
                        )
                    )
                    if phase == "during":
                        reply = receive(
                            client.get_shell_msg,
                            lambda m, request=request: (
                                m["msg_type"] == "execute_reply"
                                and m["parent_header"].get("msg_id") == request
                            ),
                        )
                        if reply["content"].get("status") != "ok":
                            raise ValueError("native probe execution failed")
                    receive(
                        client.get_iopub_msg,
                        lambda m, comm_id=comm_id, cycle=cycle, phase=phase: (
                            m["msg_type"] == "comm_msg"
                            and m["content"]["comm_id"] == comm_id
                            and m["content"]["data"] == {"cycle": cycle, "phase": phase}
                        ),
                    )
                    latencies.append(time.monotonic() - sent)
                client.shell_channel.send(
                    client.session.msg("comm_close", {"comm_id": comm_id, "data": {}})
                )
        finally:
            try:
                if manager.has_kernel:
                    manager.shutdown_kernel(now=True)
            finally:
                if client is not None:
                    client.stop_channels()
                manager.cleanup_resources()
    return {
        "schema": "molsyssuite.notebook-kernel-probe@1",
        "state": "passed",
        "python": sys.version.split()[0],
        "ipykernel": version,
        "cycles": cycles,
        "correlated_replies": len(latencies),
        "deadline_seconds": deadline,
        "max_reply_seconds": max(latencies),
        "kernel_retired": True,
        "scope": "selected native kernel/comm closure only; no browser, viewer, science or whole-workspace qualification",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cycles", type=int, default=30)
    parser.add_argument("--deadline", type=float, default=5.0)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = probe(cycles=args.cycles, deadline=args.deadline)
        status = 0
    except (OSError, ValueError, RuntimeError, TimeoutError, ImportError) as error:
        result = {
            "schema": "molsyssuite.notebook-kernel-probe@1",
            "state": "failed",
            "failure_class": type(error).__name__,
            "scope": "incomplete probe is not qualification; owned cleanup attempted",
        }
        status = 1
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result))
    return status


if __name__ == "__main__":
    raise SystemExit(main())

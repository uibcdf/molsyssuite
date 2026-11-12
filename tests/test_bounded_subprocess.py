"""Real inert subprocesses exercise admission, semantic refusal and owned cleanup."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from devtools.scripts import bounded_subprocess as bounded


@unittest.skipUnless(
    sys.platform == "linux", "bounded receiver explicitly supports Linux"
)
class BoundedSubprocessTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="suite-bounded-control-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.worker = self.root / "worker.py"
        self.worker.write_text(
            "import json,os,pathlib\n"
            "pathlib.Path(os.environ['OUTPUT']).write_text(json.dumps("
            "{'complete':True,'selection':['a','b'],'profile':os.environ['PROFILE']}))\n"
        )
        self.limits = bounded.Limits(
            cpus=(min(os.sched_getaffinity(0)),),
            wall_seconds=2,
            cpu_seconds=2,
            address_space_bytes=256 * 1024**2,
            group_rss_bytes=64 * 1024**2,
            available_reserve_bytes=1024**2,
            max_log_bytes=65536,
            sample_seconds=0.01,
            cleanup_seconds=0.1,
        )

    def run_worker(self, name="attempt", profile="normal", **changes):
        attempt = self.root / name

        def validate(output, binding):
            path = output / "semantic.json"
            result = json.loads(path.read_text()) if path.exists() else {}
            return {
                "state": "passed"
                if result
                == {"complete": True, "selection": ["a", "b"], "profile": profile}
                else "refused",
                "selection": result.get("selection"),
            }

        options = {
            "cwd": self.root,
            "env": {
                **os.environ,
                "OUTPUT": str(attempt / "semantic.json"),
                "PROFILE": profile,
            },
            "limits": self.limits,
            "attempt": attempt,
            "profile": profile,
            "helper_sha256": bounded.source_digest(),
            "inputs": {
                "worker": {
                    "path": self.worker,
                    "sha256": hashlib.sha256(self.worker.read_bytes()).hexdigest(),
                }
            },
            "validate": validate,
        }
        options.update(changes)
        return bounded.execute(
            [sys.executable, "-I", "-S", str(self.worker)], **options
        )

    def test_actual_complete_selection_qualifies_and_logs_remain(self):
        result = self.run_worker()
        self.assertEqual(result["state"], "qualified")
        self.assertEqual(result["process"]["returncode"], 0)
        self.assertTrue(result["process"]["group_terminal"])
        self.assertEqual(result["qualification"]["selection"], ["a", "b"])
        self.assertEqual(
            json.loads((self.root / "attempt/receipt.json").read_text()), result
        )

    def test_zero_exit_with_incomplete_final_receipt_is_refused(self):
        self.worker.write_text("raise SystemExit(0)\n")
        result = self.run_worker()
        self.assertEqual(result["process"]["returncode"], 0)
        self.assertEqual(result["state"], "semantic_refusal")

    def test_exit_124_is_process_failure_without_inferred_timeout(self):
        self.worker.write_text("raise SystemExit(124)\n")
        result = self.run_worker()
        self.assertEqual(result["state"], "process_failed")
        self.assertEqual(result["process"]["returncode"], 124)
        self.assertIsNone(result["resource_interruption"])

    def test_child_observes_limits_without_changing_the_parent(self):
        parent_affinity = os.sched_getaffinity(0)
        parent_nice = os.getpriority(os.PRIO_PROCESS, 0)
        self.worker.write_text(
            "import os,resource,json,pathlib\n"
            "pathlib.Path('limits.json').write_text(json.dumps({'cpus': sorted(os.sched_getaffinity(0)), 'nice': os.getpriority(os.PRIO_PROCESS,0), 'as':resource.getrlimit(resource.RLIMIT_AS), 'cpu':resource.getrlimit(resource.RLIMIT_CPU)}))\n"
            + self.worker.read_text()
        )
        result = self.run_worker()
        self.assertEqual(result["state"], "qualified")
        observed = json.loads((self.root / "limits.json").read_text())
        self.assertEqual(observed["cpus"], list(self.limits.cpus))
        self.assertGreaterEqual(observed["nice"], self.limits.nice)
        self.assertEqual(observed["as"], [self.limits.address_space_bytes] * 2)
        self.assertEqual(observed["cpu"], [self.limits.cpu_seconds] * 2)
        self.assertEqual(os.sched_getaffinity(0), parent_affinity)
        self.assertEqual(os.getpriority(os.PRIO_PROCESS, 0), parent_nice)

    def test_rapid_success_cannot_hide_an_exceeded_log_bound(self):
        self.worker.write_text('print("x" * 100000)\n' + self.worker.read_text())
        result = self.run_worker(
            limits=dataclasses.replace(self.limits, sample_seconds=0.2)
        )
        self.assertEqual(result["state"], "interrupted")
        self.assertEqual(result["resource_interruption"], "sampled_log_bytes")

    def test_low_headroom_and_wrong_helper_retain_preflight_diagnostics(self):
        with patch.object(bounded, "available_memory", return_value=0):
            result = self.run_worker("low-memory")
        self.assertEqual(result["state"], "preflight_failed")
        self.assertIn("insufficient", result["error"]["message"])
        result = self.run_worker("wrong-helper", helper_sha256="0" * 64)
        self.assertEqual(result["state"], "preflight_failed")
        self.assertIsNone(result["process"]["returncode"])
        self.assertTrue((self.root / "wrong-helper/error.log").is_file())

    def test_launch_failure_and_nonfinite_limit_have_structured_receipts(self):
        with patch.object(
            bounded.subprocess,
            "Popen",
            side_effect=FileNotFoundError("missing executable"),
        ):
            result = self.run_worker("launch")
        self.assertEqual(result["error"]["stage"], "launch")
        result = self.run_worker(
            "nan", limits=dataclasses.replace(self.limits, wall_seconds=float("nan"))
        )
        self.assertEqual(result["state"], "preflight_failed")
        self.assertEqual(
            json.loads((self.root / "nan/receipt.json").read_text())["limits"][
                "wall_seconds"
            ],
            "nan",
        )

    def test_dependent_profile_requires_same_frozen_composition(self):
        normal = self.run_worker("normal")
        self.assertEqual(normal["state"], "qualified")
        path = self.root / "normal/receipt.json"
        prerequisite = {
            "path": path,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "profile": "normal",
        }
        result = self.run_worker(
            "nondefault", profile="pm_fs", prerequisite=prerequisite
        )
        self.assertEqual(result["state"], "qualified")
        self.worker.write_text(self.worker.read_text() + "# different frozen worker\n")
        result = self.run_worker("stale", profile="pm_fs", prerequisite=prerequisite)
        self.assertEqual(result["state"], "preflight_failed")
        self.assertIn("matching composition", result["error"]["message"])

    def test_wall_limit_retires_owned_group(self):
        self.worker.write_text(
            "import signal,time\nsignal.signal(signal.SIGTERM,signal.SIG_IGN)\ntime.sleep(20)\n"
        )
        result = self.run_worker(
            limits=dataclasses.replace(self.limits, wall_seconds=0.1)
        )
        self.assertEqual(result["resource_interruption"], "wall_deadline")
        self.assertEqual(result["state"], "interrupted")
        self.assertTrue(result["process"]["group_terminal"])

    def test_keyboard_interruption_is_retained_and_propagates_after_cleanup(self):
        def interrupted(output, binding):
            raise KeyboardInterrupt

        with self.assertRaises(KeyboardInterrupt):
            self.run_worker(validate=interrupted)
        receipt = json.loads((self.root / "attempt/receipt.json").read_text())
        self.assertEqual(receipt["state"], "interrupted")
        self.assertEqual(receipt["error"]["type"], "KeyboardInterrupt")
        self.assertTrue(receipt["process"]["group_terminal"])

    def test_leader_exit_and_stubborn_child_cleanup_preserve_unrelated_sentinel(self):
        self.worker.write_text(
            "import subprocess,sys,time\n"
            "subprocess.Popen([sys.executable,'-I','-S','-c','import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(20)'])\n"
            "time.sleep(0.15)\n"
        )
        sentinel = subprocess.Popen(
            [sys.executable, "-I", "-S", "-c", "import time;time.sleep(20)"],
            start_new_session=True,
        )
        try:
            result = self.run_worker()
            self.assertEqual(result["process"]["returncode"], 0)
            self.assertEqual(
                result["process"]["termination_reason"],
                "owned_descendants_after_leader_exit",
            )
            self.assertTrue(result["process"]["group_terminal"])
            self.assertEqual(result["state"], "interrupted")
            self.assertIsNone(sentinel.poll())
        finally:
            sentinel.terminate()
            sentinel.wait(timeout=3)

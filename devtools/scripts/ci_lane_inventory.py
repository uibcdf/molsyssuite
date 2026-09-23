"""Read-only observations of configured GitHub Actions Python test lanes.

This is an inventory, not a policy gate. It reports unresolved expressions and
conditional jobs instead of treating them as evidence of executed tests.
"""

from __future__ import annotations

import argparse
import ast
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any

import tomllib

try:
    import yaml
except ImportError:  # pragma: no cover - diagnosed by the CLI
    yaml = None


ROOT = Path(__file__).resolve().parents[2]
MATRIX_REFERENCE = re.compile(r"^\s*\${{\s*matrix\.([A-Za-z0-9_.-]+)\s*}}\s*$")
PYTEST_COMMAND = re.compile(
    r"^\s*(?:(?:python(?:\d+(?:\.\d+)?)?\s+-m\s+)?pytest|xvfb-run\s+.*?\bpytest)(?:\s|$)"
)
MICROMAMBA_PYTHON = re.compile(
    r"(?:^|\s)python\s*=\s*(\${{\s*matrix\.[A-Za-z0-9_.-]+\s*}}|\d+\.\d+)"
)


def _resolve(value: Any, combination: dict[str, Any]) -> str:
    if not isinstance(value, str):
        return "unknown"
    match = MATRIX_REFERENCE.fullmatch(value)
    if match is None:
        return "unknown" if "${{" in value else value.strip()
    current: Any = combination
    for part in match.group(1).split("."):
        if not isinstance(current, dict) or part not in current:
            return "unknown"
        current = current[part]
    return current.strip() if isinstance(current, str) else "unknown"


def _expand_matrix(matrix: Any) -> tuple[list[dict[str, Any]], str]:
    if matrix is None:
        return ([{}], "none")
    if not isinstance(matrix, dict):
        return ([{}], "unresolved")

    axes = {
        key: values
        for key, values in matrix.items()
        if key not in {"include", "exclude"}
    }
    if not all(isinstance(values, list) for values in axes.values()):
        return ([{}], "unresolved")
    includes = matrix.get("include", [])
    excludes = matrix.get("exclude", [])
    if not isinstance(includes, list) or not isinstance(excludes, list):
        return ([{}], "unresolved")
    if not all(isinstance(entry, dict) for entry in includes + excludes):
        return ([{}], "unresolved")

    if not axes and includes:
        return ([entry.copy() for entry in includes], "static")

    keys = list(axes)
    values = [axes[key] for key in keys]
    originals = [dict(zip(keys, selection)) for selection in itertools.product(*values)]
    records = [
        (original, original.copy())
        for original in originals
        if not any(
            all(original.get(key) == value for key, value in entry.items())
            for entry in excludes
        )
    ]
    extras: list[dict[str, Any]] = []
    for entry in includes:
        matched = False
        for original, combination in records:
            if all(
                original.get(key) == value
                for key, value in entry.items()
                if key in axes
            ):
                combination.update(entry)
                matched = True
        if not matched:
            extras.append(entry.copy())
    combinations = [combination for _, combination in records] + extras
    return (combinations, "static")


def _events(trigger: Any) -> list[tuple[str, bool, bool, bool]]:
    if isinstance(trigger, dict):
        return [
            (
                str(event),
                isinstance(config, dict)
                and ("paths" in config or "paths-ignore" in config),
                isinstance(config, dict)
                and any(
                    key in config
                    for key in ("branches", "branches-ignore", "tags", "tags-ignore")
                ),
                event == "push"
                and isinstance(config, dict)
                and "tags" in config
                and "branches" not in config
                and "branches-ignore" not in config,
            )
            for event, config in trigger.items()
        ]
    if isinstance(trigger, list):
        return [(str(event), False, False, False) for event in trigger]
    if isinstance(trigger, str):
        return [(trigger, False, False, False)]
    return [("unknown", False, False, False)]


def _python_from_steps(steps: Any, combination: dict[str, Any]) -> str:
    if not isinstance(steps, list):
        return "unknown"
    versions: set[str] = set()
    for step in steps:
        if not isinstance(step, dict):
            continue
        uses = step.get("uses", "")
        with_values = step.get("with", {})
        if not isinstance(with_values, dict):
            continue
        if isinstance(uses, str) and uses.startswith("actions/setup-python@"):
            versions.add(_resolve(with_values.get("python-version"), combination))
        if isinstance(uses, str) and uses.startswith("mamba-org/setup-micromamba@"):
            create_args = with_values.get("create-args", "")
            if isinstance(create_args, str):
                match = MICROMAMBA_PYTHON.search(create_args)
                if match is not None:
                    versions.add(_resolve(match.group(1), combination))
    return next(iter(versions)) if len(versions) == 1 else "unknown"


def _gating(value: Any, combination: dict[str, Any]) -> bool | None:
    if value is None:
        return True
    resolved = _resolve(value, combination)
    if resolved == "false":
        return True
    if resolved == "true":
        return False
    return None


def _event_condition(value: Any, event: str) -> bool | None:
    """Resolve only event-name logic; leave other Actions context unknown."""
    if value is None:
        return True
    if not isinstance(value, str):
        return None
    expression = value.strip()
    if expression.startswith("${{") and expression.endswith("}}"):
        expression = expression[3:-2].strip()
    if not expression:
        return True
    expression = re.sub(
        r"!(?!=)", " not ", expression.replace("&&", " and ").replace("||", " or ")
    ).strip()
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return None

    def evaluate(node: ast.AST) -> bool | str | None:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Name):
            if node.id in {"true", "True"}:
                return True
            if node.id in {"false", "False"}:
                return False
            return None
        if isinstance(node, ast.Constant) and isinstance(node.value, (str, bool)):
            return node.value
        if isinstance(node, ast.Compare) and len(node.ops) == 1:
            operands = (node.left, node.comparators[0])
            event_operand = next(
                (
                    operand
                    for operand in operands
                    if isinstance(operand, ast.Attribute)
                    and operand.attr == "event_name"
                    and isinstance(operand.value, ast.Name)
                    and operand.value.id == "github"
                ),
                None,
            )
            literal = next(
                (
                    operand.value
                    for operand in operands
                    if isinstance(operand, ast.Constant)
                    and isinstance(operand.value, str)
                ),
                None,
            )
            if event_operand is None or literal is None:
                return None
            equal = event.casefold() == literal.casefold()
            if isinstance(node.ops[0], ast.Eq):
                return equal
            if isinstance(node.ops[0], ast.NotEq):
                return not equal
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            operand = evaluate(node.operand)
            return not operand if isinstance(operand, bool) else None
        if isinstance(node, ast.BoolOp):
            values = [evaluate(part) for part in node.values]
            if isinstance(node.op, ast.And):
                if False in values:
                    return False
                return True if all(value is True for value in values) else None
            if isinstance(node.op, ast.Or):
                if True in values:
                    return True
                return False if all(value is False for value in values) else None
        return None

    result = evaluate(tree)
    return result if isinstance(result, bool) else None


def _test_step_evidence(
    steps: Any, combination: dict[str, Any], event: str
) -> tuple[bool, bool | None, bool | None]:
    if not isinstance(steps, list):
        return (False, True, False)
    test_steps = [
        step
        for step in steps
        if isinstance(step, dict)
        and isinstance(step.get("run"), str)
        and any(PYTEST_COMMAND.match(line) for line in step["run"].splitlines())
    ]
    if not test_steps:
        return (False, True, False)

    step_evidence = [
        (
            _event_condition(step.get("if"), event),
            _gating(step.get("continue-on-error"), combination),
        )
        for step in test_steps
    ]
    eligible = [gate for condition, gate in step_evidence if condition is True]
    possible = [gate for condition, gate in step_evidence if condition is None]
    event_eligible: bool | None
    if eligible:
        event_eligible = True
    elif possible:
        event_eligible = None
    else:
        event_eligible = False
    if True in eligible:
        gating = True
    elif None in eligible or any(gate is not False for gate in possible):
        gating = None
    else:
        gating = False
    return (True, gating, event_eligible)


def inventory_workflow(path: Path, repository: str) -> list[dict[str, Any]]:
    """Describe observable job cells without inferring that they ran or passed."""
    if yaml is None:
        raise RuntimeError(
            "PyYAML is required; use the MolSysSuite development environment"
        )
    try:
        document = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    except yaml.YAMLError as error:
        raise ValueError(f"{path}: invalid workflow YAML: {error}") from error
    if not isinstance(document, dict):
        raise TypeError(f"{path}: workflow root must be a mapping")
    jobs = document.get("jobs", {})
    if not isinstance(jobs, dict):
        raise TypeError(f"{path}: jobs must be a mapping")
    observations: list[dict[str, Any]] = []
    for job_name, job in jobs.items():
        if not isinstance(job, dict):
            continue
        strategy = job.get("strategy", {})
        matrix = strategy.get("matrix") if isinstance(strategy, dict) else None
        combinations, matrix_status = _expand_matrix(matrix)
        for event, path_filtered, ref_filtered, tag_only in _events(document.get("on")):
            for combination in combinations:
                has_test, test_gating, test_eligible = _test_step_evidence(
                    job.get("steps"), combination, event
                )
                job_eligible = _event_condition(job.get("if"), event)
                if False in (job_eligible, test_eligible):
                    event_eligible = False
                elif None in (job_eligible, test_eligible):
                    event_eligible = None
                else:
                    event_eligible = True
                job_gating = _gating(job.get("continue-on-error"), combination)
                if False in (job_gating, test_gating):
                    gating = False
                elif None in (job_gating, test_gating):
                    gating = None
                else:
                    gating = True
                observations.append(
                    {
                        "repository": repository,
                        "workflow": path.name,
                        "event": event,
                        "job": str(job_name),
                        "os": _resolve(job.get("runs-on"), combination),
                        "python": _python_from_steps(job.get("steps"), combination),
                        "test_command_observed": has_test,
                        "gating": gating,
                        "conditional": event_eligible is None,
                        "event_eligible": event_eligible,
                        "path_filtered": path_filtered,
                        "ref_filtered": ref_filtered,
                        "tag_only": tag_only,
                        "matrix_status": matrix_status,
                    }
                )
    return observations


def inventory_repository(root: Path, repository: str) -> list[dict[str, Any]]:
    workflows = root / ".github" / "workflows"
    if not workflows.is_dir():
        raise FileNotFoundError(
            f"{repository}: no .github/workflows directory at {root}"
        )
    paths = sorted(workflows.glob("*.yml")) + sorted(workflows.glob("*.yaml"))
    observations: list[dict[str, Any]] = []
    for path in paths:
        observations.extend(inventory_workflow(path, repository))
    return observations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workspace", type=Path, help="parent of the registered repositories"
    )
    parser.add_argument(
        "--repository", help="restrict to one uibcdf/<member> repository"
    )
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable observations"
    )
    args = parser.parse_args(argv)
    registry = tomllib.loads((ROOT / "suite.toml").read_text(encoding="utf-8"))
    members = [
        member
        for member in registry["members"]
        if "python-package" in member.get("capabilities", [])
        and (args.repository is None or member["repository"] == args.repository)
    ]
    if not members:
        parser.error("no registered Python member matches --repository")
    try:
        observations = [
            lane
            for member in members
            for lane in inventory_repository(
                args.workspace / member["name"], member["repository"]
            )
        ]
    except (FileNotFoundError, RuntimeError, TypeError, ValueError) as error:
        print(f"CI inventory unavailable: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(observations, indent=2, sort_keys=True))
    else:
        print("OBSERVATIONS ONLY: configured jobs are not proof of executed tests")
        for lane in observations:
            print(
                f"{lane['repository']} {lane['workflow']}:{lane['job']} "
                f"event={lane['event']} os={lane['os']} python={lane['python']} "
                f"test={lane['test_command_observed']} gating={lane['gating']} "
                f"eligible={lane['event_eligible']} conditional={lane['conditional']} "
                f"paths={lane['path_filtered']} "
                f"refs={lane['ref_filtered']} tag_only={lane['tag_only']} "
                f"matrix={lane['matrix_status']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

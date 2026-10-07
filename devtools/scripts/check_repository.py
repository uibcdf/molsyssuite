"""Read-only conformance audit for a registered MolSysSuite repository."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import tomllib

if __package__:
    from . import ci_lane_inventory, repository_badges, suite_policy
else:  # Direct scripts resolve siblings from their own script directory.
    import ci_lane_inventory
    import repository_badges
    import suite_policy

POLICY_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


def _load_policy() -> dict[str, object]:
    return suite_policy.load_effective_registry()


def _member(policy: dict[str, object], repository: str) -> dict[str, object] | None:
    wanted = repository.casefold()
    return next(
        (
            member
            for member in policy.get("members", [])
            if str(member.get("repository", "")).casefold() == wanted
        ),
        None,
    )


def _governance_pointer(root: Path) -> bool:
    candidates = (root / "AGENTS.md", root / "CONTRIBUTING.md")
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in candidates
        if path.is_file()
    ).casefold()
    return "uibcdf/molsyssuite" in text


def _agents_text(root: Path) -> str:
    path = root / "AGENTS.md"
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def _component_guide_findings(
    root: Path, policy: dict[str, object], *, check_content: bool = True
) -> list[Finding]:
    guide_policy = policy["policies"]["component-guide"]
    filename = str(guide_policy["filename"])
    canonical = POLICY_ROOT / filename
    local = root / filename
    findings: list[Finding] = []
    if not local.is_file():
        findings.append(Finding("GUIDE_MISSING", f"{filename} is missing"))
    elif check_content and local.read_bytes() != canonical.read_bytes():
        findings.append(
            Finding("GUIDE_DRIFT", f"{filename} differs from the canonical suite guide")
        )
    if filename not in _agents_text(root):
        findings.append(
            Finding("GUIDE_POINTER", f"AGENTS.md must require reading {filename}")
        )
    return findings


def _workflow_text(root: Path) -> str:
    directory = root / ".github" / "workflows"
    if not directory.is_dir():
        return ""
    return "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for suffix in ("*.yml", "*.yaml")
        for path in sorted(directory.glob(suffix))
    )


def _required_sibling_dependencies(
    pyproject: dict[str, object], policy: dict[str, object], repository: str
) -> list[str]:
    """Return registered distributions named by required project dependencies."""
    names = {
        re.sub(r"[-_.]+", "-", str(member["name"])).casefold()
        for member in policy["members"]
        if str(member["repository"]).casefold() != repository.casefold()
    }
    dependencies = pyproject.get("project", {}).get("dependencies", [])
    if not isinstance(dependencies, list):
        return []
    siblings: set[str] = set()
    for dependency in dependencies:
        if not isinstance(dependency, str):
            continue
        match = re.match(r"\s*([A-Za-z0-9][A-Za-z0-9._-]*)", dependency)
        if match is None:
            continue
        name = re.sub(r"[-_.]+", "-", match.group(1)).casefold()
        if name in names:
            siblings.add(name)
    return sorted(siblings)


def _noarch_entry_point_findings(
    root: Path, pyproject: dict[str, object]
) -> list[Finding]:
    """Compare noarch Conda launchers with the project's console scripts."""
    recipe = root / "devtools/conda-build/meta.yaml"
    if not recipe.is_file():
        return []

    lines = recipe.read_text(encoding="utf-8").splitlines()
    build_start = next(
        (
            index
            for index, line in enumerate(lines)
            if re.match(r"^build:\s*(?:#.*)?$", line)
        ),
        None,
    )
    if build_start is None:
        return []
    build_lines: list[str] = []
    for line in lines[build_start + 1 :]:
        if line.strip() and not line[0].isspace() and not line.lstrip().startswith("#"):
            break
        build_lines.append(line)

    noarch = next(
        (
            match
            for line in build_lines
            if (match := re.match(r"^(\s+)noarch:\s*([^#]*?)(?:\s+#.*)?$", line))
        ),
        None,
    )
    if noarch is None or noarch.group(2).strip().strip("\"'") != "python":
        return []
    field_indent = len(noarch.group(1))
    entry = next(
        (
            (index, match)
            for index, line in enumerate(build_lines)
            if (match := re.match(r"^(\s+)entry_points:\s*([^#]*?)(?:\s+#.*)?$", line))
            and len(match.group(1)) == field_indent
        ),
        None,
    )

    declared = pyproject.get("project", {}).get("scripts", {})
    expected = declared if isinstance(declared, dict) else {}
    observed: dict[str, str] = {}
    problems: list[str] = []
    if entry is not None:
        index, match = entry
        inline = match.group(2).strip()
        values: list[str] = []
        if inline.startswith("[") and inline.endswith("]"):
            values.extend(
                part.strip() for part in inline[1:-1].split(",") if part.strip()
            )
        elif inline:
            problems.append("entry_points must be a YAML list")
        else:
            entry_indent = len(match.group(1))
            for line in build_lines[index + 1 :]:
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                indent = len(line) - len(line.lstrip())
                if indent < entry_indent or (
                    indent == entry_indent and re.match(r"^\s+-\s+", line) is None
                ):
                    break
                item = re.match(r"^\s+-\s+(.+?)\s*(?:#.*)?$", line)
                if item is None:
                    problems.append(f"invalid entry_points item: {line.strip()}")
                    continue
                values.append(item.group(1))
        for raw in values:
            value = raw.strip().strip("\"'")
            if "=" not in value:
                problems.append(f"invalid entry_points item: {value}")
                continue
            name, target = (part.strip() for part in value.split("=", 1))
            if not name or not target or name in observed:
                problems.append(f"invalid or duplicate entry point: {name or value}")
            else:
                observed[name] = target

    missing = sorted(set(expected) - set(observed))
    extra = sorted(set(observed) - set(expected))
    changed = sorted(
        name
        for name in expected.keys() & observed.keys()
        if expected[name] != observed[name]
    )
    if missing:
        problems.append("missing: " + ", ".join(missing))
    if extra:
        problems.append("unexpected: " + ", ".join(extra))
    if changed:
        problems.append("target mismatch: " + ", ".join(changed))
    if not problems:
        return []
    return [
        Finding(
            "NOARCH_ENTRY_POINTS",
            "devtools/conda-build/meta.yaml build.entry_points differs from "
            "pyproject.toml [project.scripts]: " + "; ".join(problems),
        )
    ]


def _active_noarch_entry_point_exception(
    policy: dict[str, object], repository: str
) -> bool:
    """Honor only a complete, unexpired member distribution exception."""
    review = next(
        (
            entry
            for entry in policy.get("python-distribution-reviews", [])
            if entry.get("repository") == repository
        ),
        {},
    )
    if review.get("state") != "excepted" or not all(
        str(review.get(key, "")).strip()
        for key in ("reason", "owner", "removal-condition")
    ):
        return False
    if not str(review.get("review-issue", "")).startswith(f"{repository}#"):
        return False
    try:
        expires = date.fromisoformat(str(review.get("expires-on", "")))
    except ValueError:
        return False
    return expires >= datetime.now(tz=UTC).date()


def _sibling_ci_route_findings(
    root: Path,
    repository: str,
    pyproject: dict[str, object],
    policy: dict[str, object],
) -> list[Finding]:
    """Require each declared sibling through a committed CI acquisition route."""
    siblings = _required_sibling_dependencies(pyproject, policy, repository)
    if not siblings:
        return []

    covered: set[str] = set()
    directory = root / ".github" / "workflows"
    paths = sorted(directory.glob("*.yml")) + sorted(directory.glob("*.yaml"))
    pinned_source = re.compile(
        r"git\+https://github\.com/uibcdf/([A-Za-z0-9_.-]+)@"
        r"[0-9a-fA-F]{40}(?![0-9a-fA-F])",
        re.IGNORECASE,
    )
    for path in paths:
        workflow = path.read_text(encoding="utf-8", errors="replace")
        steps = re.split(r"(?m)^\s*-\s+(?=(?:name|uses):)", workflow)
        checkouts: dict[str, str] = {}
        install_steps: list[str] = []
        for step in steps:
            active = "\n".join(
                line for line in step.splitlines() if not line.lstrip().startswith("#")
            )
            if "mamba-org/setup-micromamba@" in active:
                for environment in re.findall(
                    r"(?m)^\s*environment-file:\s*['\"]?"
                    r"(devtools/conda-envs/[A-Za-z0-9_.-]+\.ya?ml)",
                    active,
                ):
                    environment_path = root / environment
                    if environment_path.is_file():
                        covered.update(
                            re.sub(r"[-_.]+", "-", match.group(1)).casefold()
                            for line in environment_path.read_text(
                                encoding="utf-8", errors="replace"
                            ).splitlines()
                            if (
                                match := re.match(
                                    r"\s*-\s*([A-Za-z0-9][A-Za-z0-9._-]*)", line
                                )
                            )
                        )
            if re.search(r"\buses:\s*actions/checkout@", active):
                fields = {
                    key: match.group(1)
                    for key in ("repository", "ref", "path")
                    if (
                        match := re.search(
                            rf"(?m)^\s*{key}:\s*['\"]?([^'\"\s#]+)", active
                        )
                    )
                }
                repository = fields.get("repository", "")
                source_path = fields.get("path", "")
                if (
                    repository.startswith("uibcdf/")
                    and re.fullmatch(r"[0-9a-fA-F]{40}", fields.get("ref", ""))
                    and re.fullmatch(r"\.[A-Za-z0-9_./-]+", source_path)
                    and ".." not in source_path
                ):
                    checkouts[source_path] = repository.removeprefix("uibcdf/")
            if "run:" in active and re.search(r"\bpip\s+install\b", active):
                install_steps.append(active)

        for step in install_steps:
            for line in step.replace("\\\n", " ").splitlines():
                if not re.search(r"\bpip\s+install\b", line):
                    continue
                covered.update(
                    match.group(1).casefold() for match in pinned_source.finditer(line)
                )
                for requirements in re.findall(
                    r"(?:^|\s)-r\s+(devtools/requirements/[A-Za-z0-9_.-]+\.txt)",
                    line,
                ):
                    requirements_path = root / requirements
                    if not requirements_path.is_file():
                        continue
                    for requirement in requirements_path.read_text(
                        encoding="utf-8", errors="replace"
                    ).splitlines():
                        if requirement.lstrip().startswith("#"):
                            continue
                        if match := pinned_source.fullmatch(requirement.strip()):
                            covered.add(match.group(1).casefold())
            for source_path, sibling in checkouts.items():
                if re.search(rf"(?<![\w/]){re.escape(source_path)}(?![\w/.-])", step):
                    covered.add(sibling.casefold())

    missing = [sibling for sibling in siblings if sibling not in covered]
    if not missing:
        return []
    return [
        Finding(
            "SIBLING_CI_ROUTE",
            "required MolSysSuite dependencies lack a CI acquisition route: "
            + ", ".join(missing)
            + "; use a referenced Conda environment, pinned VCS requirements, "
            "or a pinned source checkout that CI installs",
        )
    ]


def _workflow_fail_fast_findings(root: Path) -> list[Finding]:
    """Reject the measured import-smoke shape that hides a failed import.

    This deliberately does not claim to parse arbitrary shell. It recognizes the named
    shared step, a literal multi-line script, a Python command followed by another
    command, and the absence of the suite's explicit fail-fast preamble before Python.
    """
    directory = root / ".github" / "workflows"
    if not directory.is_dir():
        return []

    unsafe: list[str] = []
    paths = sorted(directory.glob("*.yml")) + sorted(directory.glob("*.yaml"))
    for path in paths:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for index, line in enumerate(lines):
            step = re.match(r"^(?P<indent>\s*)-\s+name:\s*(?P<name>.+?)\s*$", line)
            if step is None:
                continue
            name = step.group("name").strip("'\"")
            if re.search(r"\b(?:test\s+)?import module\b", name, re.IGNORECASE) is None:
                continue

            step_indent = len(step.group("indent"))
            end = len(lines)
            for following in range(index + 1, len(lines)):
                boundary = re.match(r"^(?P<indent>\s*)-\s+", lines[following])
                if (
                    boundary is not None
                    and len(boundary.group("indent")) == step_indent
                ):
                    end = following
                    break
            block = lines[index:end]

            run_index = next(
                (
                    offset
                    for offset, candidate in enumerate(block)
                    if re.match(r"^\s*run:\s*[|>]", candidate)
                ),
                None,
            )
            if run_index is None:
                continue
            commands = [
                candidate.strip()
                for candidate in block[run_index + 1 :]
                if candidate.strip() and not candidate.lstrip().startswith("#")
            ]
            python_indices = [
                offset
                for offset, command in enumerate(commands)
                if re.search(r"(?<![\w-])python(?:3)?(?![\w-])", command)
            ]
            if not python_indices or python_indices[-1] == len(commands) - 1:
                continue
            first_python = python_indices[0]
            fail_fast = any(
                re.fullmatch(
                    r"set\s+-[A-Za-z]*e[A-Za-z]*u[A-Za-z]*o\s+pipefail", command
                )
                for command in commands[:first_python]
            )
            if not fail_fast:
                relative = path.relative_to(root).as_posix()
                unsafe.append(f"{relative}:{index + 1} ({name})")

    if not unsafe:
        return []
    return [
        Finding(
            "WORKFLOW_FAIL_FAST",
            "import smoke steps can hide Python failure behind a later command: "
            + ", ".join(unsafe),
        )
    ]


def _version_is_present(text: str, version: str) -> bool:
    return re.search(rf"(?<![\d.]){re.escape(version)}(?![\d.])", text) is not None


def _canonical_specifiers(value: object) -> frozenset[str]:
    """Normalize the simple minor-version bounds used by the suite policy."""
    normalized: set[str] = set()
    for raw in str(value or "").split(","):
        match = re.fullmatch(r"\s*(<=|>=|==|!=|~=|<|>)\s*(\d+(?:\.\d+)*)\s*", raw)
        if match is None:
            return frozenset()
        operator, version = match.groups()
        parts = version.split(".")
        while len(parts) > 2 and parts[-1] == "0":
            parts.pop()
        normalized.add(operator + ".".join(parts))
    return frozenset(normalized)


def _rule_is_covered(rule: str, selected: list[str]) -> bool:
    return "ALL" in selected or any(rule.startswith(choice) for choice in selected)


def _ruff_conforms(pyproject: dict[str, object], required: list[str]) -> bool:
    ruff = pyproject.get("tool", {}).get("ruff", {})
    if ruff.get("target-version") != "py311":
        return False
    lint = ruff.get("lint", {})
    selected = list(lint.get("select", [])) + list(lint.get("extend-select", []))
    return all(_rule_is_covered(rule, selected) for rule in required)


def _vendored_guide_findings(
    root: Path,
    repository: str,
    pyproject: dict[str, object],
    policy: dict[str, object],
) -> list[Finding]:
    guide_policy = policy["policies"]["vendored-guides"]
    marker = str(guide_policy["marker"])
    excluded = {
        str(path).removeprefix("./")
        for path in pyproject.get("tool", {}).get("ruff", {}).get("extend-exclude", [])
    }
    findings: list[Finding] = []
    for guide in policy.get("guides", []):
        if repository not in guide["consumers"]:
            continue
        filename = str(guide["filename"])
        local = root / filename
        if not local.is_file():
            continue
        text = local.read_text(encoding="utf-8", errors="replace")
        if marker not in text:
            findings.append(
                Finding(
                    "VENDORED_GUIDE_MARKER",
                    f"{filename} lacks the synchronized read-only marker",
                )
            )
        if filename not in excluded:
            findings.append(
                Finding(
                    "VENDORED_GUIDE_RUFF",
                    f"tool.ruff.extend-exclude must contain {filename!r}",
                )
            )
    return findings


def missing_ruff_ci_commands(
    workflow_text: str, policy_releases: list[str]
) -> list[str]:
    shared_gates = [
        f"uibcdf/molsyssuite/.github/workflows/check-python-repository.yaml@{release}"
        for release in policy_releases
    ]
    if any(gate in workflow_text for gate in shared_gates):
        return []
    command = r"(?:python\s+-m\s+)?ruff"
    check_present = re.search(
        rf"(?m)^\s*(?:-?\s*run:\s*)?{command}\s+check(?:\s|$)", workflow_text
    )
    format_lines = [
        line
        for line in workflow_text.splitlines()
        if re.search(rf"^\s*(?:-?\s*run:\s*)?{command}\s+format(?:\s|$)", line)
    ]
    format_check_present = any("--check" in line for line in format_lines)
    missing = []
    if check_present is None:
        missing.append("ruff check")
    if not format_check_present:
        missing.append("ruff format --check")
    return missing


def _python_contract(
    policy: dict[str, object], member: dict[str, object]
) -> tuple[object, list[str], str | None]:
    """Return the range, CI versions, and transition state for one member."""
    python_policy = policy["policies"]["python"]
    transition = python_policy.get("transition", {})
    component = next(
        (
            entry
            for entry in transition.get("components", [])
            if entry.get("name") == member.get("name")
        ),
        None,
    )
    state = component.get("state") if component else None
    if state in {"authorized", "admitted"}:
        return (
            transition["target-requires-python"],
            list(transition["target-ci-versions"]),
            str(state),
        )
    return (
        python_policy["requires-python"],
        list(python_policy["ci-versions"]),
        None,
    )


def _toml_text_without_ruff(pyproject: dict[str, object]) -> str:
    """Return searchable active TOML text without Ruff's compatibility tables."""

    def strings(value: object) -> list[str]:
        if isinstance(value, dict):
            output: list[str] = []
            for key, nested in value.items():
                output.append(str(key))
                output.extend(strings(nested))
            return output
        if isinstance(value, list):
            return [text for nested in value for text in strings(nested)]
        return [str(value)]

    output: list[str] = []
    for key, value in pyproject.items():
        output.append(str(key))
        if key != "tool" or not isinstance(value, dict):
            output.extend(strings(value))
            continue
        for tool, settings in value.items():
            if tool == "ruff":
                continue
            output.append(str(tool))
            output.extend(strings(settings))
    return "\n".join(output)


def _legacy_tools(
    root: Path, workflow_text: str, pyproject: dict[str, object]
) -> list[str]:
    active_text = workflow_text + "\n" + _toml_text_without_ruff(pyproject)
    for name in ("setup.cfg", "tox.ini"):
        path = root / name
        if path.is_file():
            active_text += "\n" + path.read_text(encoding="utf-8", errors="replace")
    return [
        tool
        for tool in ("black", "isort", "flake8")
        if re.search(rf"(?<![\w-]){tool}(?![\w-])", active_text, re.IGNORECASE)
    ]


def _policy_release_tuple(value: str) -> tuple[int, int, int] | None:
    match = re.fullmatch(r"policy-v([0-9]+)\.([0-9]+)\.([0-9]+)", value)
    return tuple(map(int, match.groups())) if match else None


def accepted_release_gates(
    policy: dict[str, object], required: str | None = None
) -> set[str]:
    """Return registered caller pins satisfying the requested release capability."""
    if required is None:
        required = str(policy["policies"]["release-version"]["required-policy-release"])
    minimum = _policy_release_tuple(required)
    candidates = [
        str(policy["governance"]["policy-release"]),
        *map(str, policy["governance"].get("compatible-policy-releases", [])),
    ]
    accepted = {
        release
        for release in candidates
        if minimum is not None
        and (version := _policy_release_tuple(release)) is not None
        and version >= minimum
    }
    accepted.add(required)
    return accepted


def accepted_quality_callers(
    policy: dict[str, object], member: dict[str, object]
) -> list[str]:
    """Return caller pins that supply this member's required Ruff CI gate."""
    governance = policy["governance"]
    transition = policy["policies"]["python"].get("transition", {})
    component = next(
        (
            entry
            for entry in transition.get("components", [])
            if entry.get("name") == member.get("name")
            and entry.get("state") in {"authorized", "admitted"}
        ),
        None,
    )
    if component is not None:
        compatible = component.get(
            "compatible-policy-releases",
            governance.get("transition-compatible-policy-releases", []),
        )
    else:
        compatible = governance.get("compatible-policy-releases", [])
    return [str(governance["policy-release"]), *map(str, compatible)]


def _archive_gate_observes_tag_pushes(root: Path, gates: set[str]) -> bool:
    """Require an unconditional capable caller on all tags, including slashes."""
    prefix = "uibcdf/molsyssuite/.github/workflows/check-python-repository.yaml@"
    for path in sorted((root / ".github/workflows").glob("*")):
        if path.suffix not in {".yaml", ".yml"}:
            continue
        try:
            document = ci_lane_inventory.load_workflow(path)
        except (OSError, RuntimeError, ValueError, TypeError):
            continue
        events = document.get("on")
        if isinstance(events, str):
            all_tags = events == "push"
        elif isinstance(events, list):
            all_tags = "push" in events
        elif isinstance(events, dict) and "push" in events:
            push = events["push"]
            all_tags = push in (None, "") or (
                isinstance(push, dict)
                and "tags-ignore" not in push
                and (
                    push.get("tags") == ["**"]
                    or not any(
                        key in push for key in ("tags", "branches", "branches-ignore")
                    )
                )
            )
        else:
            all_tags = False
        jobs = document.get("jobs", {})
        if (
            all_tags
            and isinstance(jobs, dict)
            and any(
                isinstance(job, dict)
                and not job.get("if")
                and job.get("uses") in {prefix + gate for gate in gates}
                for job in jobs.values()
            )
        ):
            return True
    return False


def _release_version_findings(
    root: Path,
    repository: str,
    pyproject: dict[str, object],
    workflow_text: str,
    policy: dict[str, object],
) -> list[Finding]:
    release_policy = policy["policies"]["release-version"]
    pattern = str(release_policy["pattern"])
    project = pyproject.get("project", {})
    findings: list[Finding] = []

    version = project.get("version")
    dynamic = project.get("dynamic", [])
    if version is not None:
        if re.fullmatch(pattern, str(version)) is None:
            findings.append(
                Finding(
                    "RELEASE_VERSION",
                    f"project.version must match X.Y.Z exactly; found {version!r}",
                )
            )
    elif "version" in dynamic:
        tag2version = (
            pyproject.get("tool", {}).get("versioningit", {}).get("tag2version", {})
        )
        if (
            tag2version.get("regex") != release_policy["versioningit-pattern"]
            or tag2version.get("require-match") is not True
        ):
            findings.append(
                Finding(
                    "RELEASE_TAG_FILTER",
                    "dynamic versioning must enforce the exact MolSysSuite X.Y.Z tag parser",
                )
            )
    else:
        findings.append(
            Finding(
                "RELEASE_VERSION_SOURCE",
                "project metadata must declare a static version or dynamic version source",
            )
        )

    if not release_policy["public-prereleases"] and re.search(
        r"(?<![\w-])prereleased(?![\w-])", workflow_text
    ):
        findings.append(
            Finding(
                "PUBLIC_PRERELEASE",
                "release workflows must not subscribe to the prereleased event",
            )
        )

    if (root / ".git").exists():
        completed = subprocess.run(
            ["git", "tag", "--list"],
            cwd=root,
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )
        if completed.returncode == 0:
            tags = completed.stdout.splitlines()
            archive_prefix = release_policy.get("archive-tag-prefix")
            archives = {
                tag
                for tag in tags
                if archive_prefix
                and tag.startswith(archive_prefix)
                and len(tag) > len(archive_prefix)
            }
            legacy = next(
                (
                    set(entry["tags"])
                    for entry in release_policy.get("legacy-tags", [])
                    if entry["repository"].casefold() == repository.casefold()
                ),
                set(),
            )
            invalid = sorted(
                tag
                for tag in tags
                if re.fullmatch(pattern, tag) is None
                and tag not in legacy
                and tag not in archives
            )
            if invalid:
                findings.append(
                    Finding(
                        "RELEASE_TAG",
                        "noncanonical component release tags: " + ", ".join(invalid),
                    )
                )
            if archives:
                archive_release = str(release_policy["archive-required-policy-release"])
                archive_gates = accepted_release_gates(policy, archive_release)
                gate_prefix = (
                    "uibcdf/molsyssuite/.github/workflows/check-python-repository.yaml@"
                )
                if not any(
                    gate_prefix + release in workflow_text for release in archive_gates
                ):
                    findings.append(
                        Finding(
                            "ARCHIVE_POLICY_GATE",
                            "archive tags require the shared gate at "
                            + archive_release
                            + " or a compatible newer policy",
                        )
                    )
                elif not _archive_gate_observes_tag_pushes(root, archive_gates):
                    findings.append(
                        Finding(
                            "ARCHIVE_TAG_TRIGGER",
                            "the capable archive policy caller must run on all tag "
                            'pushes, including slashes (use tags: ["**"]), '
                            "without a conditional job",
                        )
                    )

    required_gate = str(release_policy["required-policy-release"])
    accepted_gates = accepted_release_gates(policy)
    gate_prefix = "uibcdf/molsyssuite/.github/workflows/check-python-repository.yaml@"
    if not any(gate_prefix + release in workflow_text for release in accepted_gates):
        findings.append(
            Finding(
                "RELEASE_POLICY_GATE",
                f"the release-version policy requires the shared gate at {required_gate}",
            )
        )
    return findings


def check(
    root: Path,
    repository: str,
    *,
    check_guide_content: bool = True,
    admission_root: Path | None = None,
    admission_sha: str | None = None,
) -> list[Finding]:
    """Return every independent policy finding without modifying *root*."""
    policy = _load_policy()
    if admission_root is not None or admission_sha is not None:
        try:
            if admission_root is None or admission_sha is None:
                raise ValueError(
                    "admission_root and admission_sha must be supplied together"
                )
            policy = suite_policy.apply_admission(
                policy,
                suite_policy.admission_at_commit(admission_root, admission_sha),
                repository,
            )
        except ValueError as error:
            return [Finding("ADMISSION", str(error))]
    member = _member(policy, repository)
    if member is None:
        return [
            Finding("UNREGISTERED", f"{repository} is not registered in suite.toml")
        ]

    findings: list[Finding] = []
    findings.extend(
        _component_guide_findings(root, policy, check_content=check_guide_content)
    )
    if not _governance_pointer(root):
        findings.append(
            Finding(
                "GOVERNANCE_POINTER",
                "AGENTS.md or CONTRIBUTING.md must route suite-wide work to uibcdf/molsyssuite",
            )
        )

    findings.extend(
        Finding(finding.code, finding.message)
        for finding in repository_badges.validate_readme(
            root,
            repository,
            policy,
        )
    )

    if "python-package" not in member.get("capabilities", []):
        return findings

    quality_policy = policy["policies"]["python-quality"]
    pyproject_path = root / "pyproject.toml"
    if not pyproject_path.is_file():
        findings.append(Finding("PYPROJECT", "a Python member requires pyproject.toml"))
        return findings
    try:
        pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        findings.append(Finding("PYPROJECT", f"pyproject.toml is invalid: {error}"))
        return findings

    if not _active_noarch_entry_point_exception(policy, repository):
        findings.extend(_noarch_entry_point_findings(root, pyproject))

    required_range, required_ci_versions, _ = _python_contract(policy, member)
    actual_range = pyproject.get("project", {}).get("requires-python")
    if _canonical_specifiers(actual_range) != _canonical_specifiers(required_range):
        findings.append(
            Finding(
                "PYTHON_RANGE",
                f"project.requires-python must be {required_range!r}; found {actual_range!r}",
            )
        )

    workflow_text = _workflow_text(root)
    findings.extend(_workflow_fail_fast_findings(root))
    findings.extend(_sibling_ci_route_findings(root, repository, pyproject, policy))
    findings.extend(
        _release_version_findings(
            root,
            repository,
            pyproject,
            workflow_text,
            policy,
        )
    )
    missing_versions = [
        version
        for version in required_ci_versions
        if not _version_is_present(workflow_text, version)
    ]
    if missing_versions:
        findings.append(
            Finding(
                "PYTHON_CI",
                f"workflow version literals missing: {', '.join(missing_versions)}",
            )
        )

    required_rules = quality_policy["required-lint-rules"]
    if not _ruff_conforms(pyproject, required_rules):
        findings.append(
            Finding(
                "RUFF_CONFIG",
                "Ruff must target py311 and select the common lint baseline",
            )
        )

    findings.extend(_vendored_guide_findings(root, repository, pyproject, policy))

    accepted_policy_releases = accepted_quality_callers(policy, member)
    missing_ruff_ci = missing_ruff_ci_commands(workflow_text, accepted_policy_releases)
    if missing_ruff_ci:
        findings.append(
            Finding(
                "RUFF_CI",
                "active workflow commands missing: " + ", ".join(missing_ruff_ci),
            )
        )

    legacy = _legacy_tools(root, workflow_text, pyproject)
    if legacy:
        findings.append(
            Finding(
                "LEGACY_TOOL", f"active replaced tooling remains: {', '.join(legacy)}"
            )
        )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--admission-root", type=Path)
    parser.add_argument("--admission-sha")
    parser.add_argument(
        "--skip-guide-content",
        action="store_true",
        help="delegate byte drift to the live cross-repository guide-sync guard",
    )
    arguments = parser.parse_args()

    findings = check(
        arguments.target.resolve(),
        arguments.repository,
        check_guide_content=not arguments.skip_guide_content,
        admission_root=arguments.admission_root,
        admission_sha=arguments.admission_sha,
    )
    if arguments.json:
        print(json.dumps([asdict(finding) for finding in findings], indent=2))
    elif findings:
        for finding in findings:
            print(f"[{finding.code}] {finding.message}")
    else:
        print(f"{arguments.repository} conforms to MolSysSuite policy 1.0.")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())

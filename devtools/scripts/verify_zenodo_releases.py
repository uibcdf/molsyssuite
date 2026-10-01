"""Probe public releases once; resume ingestion checks without resetting deadlines."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

try:
    from devtools.scripts.audit_zenodo import CHECKSUM_RE, DOI_RE, verify_record
except ImportError:
    from audit_zenodo import CHECKSUM_RE, DOI_RE, verify_record

OUTER_HOURS = 72
RESPONSE_BYTES = 4_000_000
REQUEST_SECONDS = 20


class EvidenceUnavailable(RuntimeError):
    """An incomplete query cannot establish archival or absence."""


def timestamp(value: str) -> datetime:
    if not isinstance(value, str):
        raise TypeError("publication/cutoff timestamp is missing")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("publication/cutoff timestamps must include a timezone")
    return result.astimezone(timezone.utc)


def fetch_json(url: str, *, github: bool = False):
    headers = {
        "Accept": "application/json",
        "User-Agent": "MolSysSuite-Zenodo-Recovery/1",
    }
    if github and os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    try:
        with urlopen(
            Request(url, headers=headers), timeout=REQUEST_SECONDS
        ) as response:
            body = response.read(RESPONSE_BYTES + 1)
        if len(body) > RESPONSE_BYTES:
            raise EvidenceUnavailable("public response exceeds the size bound")
        return json.loads(body)
    except (OSError, ValueError) as error:
        # Do not retain raw responses, request headers or account-side data.
        raise EvidenceUnavailable(
            f"public query failed ({type(error).__name__})"
        ) from error


def fetch_releases(repository: str, max_pages: int = 5) -> list[dict]:
    releases = []
    for page in range(1, max_pages + 1):
        payload = fetch_json(
            f"https://api.github.com/repos/{repository}/releases?per_page=100&page={page}",
            github=True,
        )
        if not isinstance(payload, list) or any(
            not isinstance(item, dict) for item in payload
        ):
            raise EvidenceUnavailable("GitHub release query has an unexpected shape")
        releases.extend(payload)
        if len(payload) < 100:
            return releases
    raise EvidenceUnavailable(
        "release discovery reached its page bound; no complete claim is possible"
    )


def fetch_records(concept_doi: str) -> list[dict]:
    records = []
    for page in range(1, 21):
        query = urlencode(
            {
                "q": f"conceptrecid:{concept_doi.rsplit('.', 1)[-1]}",
                "all_versions": "true",
                "size": 25,
                "page": page,
            }
        )
        payload = fetch_json(f"https://zenodo.org/api/records?{query}")
        try:
            hits = payload["hits"]["hits"]
            total = payload["hits"]["total"]
            if isinstance(total, dict):
                if total.get("relation", "eq") != "eq":
                    raise ValueError("inexact result total")
                total = total["value"]
            if not isinstance(hits, list) or any(
                not isinstance(item, dict) for item in hits
            ):
                raise ValueError("invalid result list")
            if type(total) is not int or total < 0:
                raise ValueError("invalid result total")
        except (KeyError, TypeError, ValueError) as error:
            raise EvidenceUnavailable(
                "Zenodo query has an unexpected or incomplete shape"
            ) from error
        records.extend(hits)
        if len(records) > total:
            raise EvidenceUnavailable(
                "Zenodo result count contradicts its reported total"
            )
        if len(records) >= total:
            return records
        if not hits:
            raise EvidenceUnavailable(
                "Zenodo pagination ended before its reported total"
            )
    raise EvidenceUnavailable(
        "Zenodo discovery reached its page bound; no complete claim is possible"
    )


def select_releases(releases: list[dict], since: datetime, now: datetime) -> list[dict]:
    covered = []
    tags = set()
    for release in releases:
        if release.get("draft"):
            continue
        published = timestamp(release["published_at"])
        if published > now:
            raise ValueError("release publication timestamp is in the future")
        tag = release["tag_name"]
        if not isinstance(tag, str) or not tag or tag in tags:
            raise ValueError("release identity is missing or duplicated")
        tags.add(tag)
        if published >= since:
            covered.append(release)
    return covered


def evaluate_release(
    release: dict,
    records: list[dict],
    repository: str,
    concept_doi: str,
    now: datetime,
    *,
    unavailable: bool = False,
) -> dict:
    """Classify one immutable publication, including late recovery and file facts."""
    published = timestamp(release["published_at"])
    age = (now - published).total_seconds() / 3600
    if age < 0:
        raise ValueError("release publication timestamp is in the future")
    tag = release["tag_name"]
    version = tag.removeprefix("v")
    result = {
        "repository": repository,
        "tag": tag,
        "version": version,
        "published_at": release["published_at"],
        "observed_at": now.isoformat(),
        "age_hours": round(age, 3),
        "archive_coverage": "source-snapshot",
        "escalation_required": age >= OUTER_HOURS,
    }
    if unavailable:
        return {**result, "state": "temporarily_unavailable"}
    matches = [
        item
        for item in records
        if isinstance(item.get("metadata"), dict)
        and item["metadata"].get("version") == version
    ]
    if not matches:
        if any(
            not isinstance(item.get("metadata"), dict)
            or not isinstance(item["metadata"].get("version"), str)
            or not item["metadata"]["version"].strip()
            for item in records
        ):
            return {
                **result,
                "state": "temporarily_unavailable",
                "errors": [
                    "concept records lack usable version identity; absence is inconclusive"
                ],
            }
        return {
            **result,
            "state": "absent" if age >= OUTER_HOURS else "ingestion_pending",
        }
    if len(matches) != 1:
        return {
            **result,
            "state": "invalid",
            "escalation_required": True,
            "errors": ["ambiguous exact-version records"],
        }
    record = matches[0]
    try:
        files = record["files"]
        if not isinstance(files, list) or not files:
            raise ValueError("record has no archived files")
        evidence = []
        for item in files:
            if not isinstance(item, dict) or not isinstance(item.get("key"), str):
                raise TypeError("invalid file name")
            if type(item.get("size")) is not int or item["size"] < 1:
                raise ValueError("invalid file size")
            if not CHECKSUM_RE.fullmatch(str(item.get("checksum", ""))):
                raise ValueError("invalid file checksum")
            evidence.append(
                {
                    "name": item["key"],
                    "size": item["size"],
                    "checksum": item["checksum"],
                }
            )
        names = [item["name"] for item in evidence]
        if len(names) != len(set(names)):
            raise ValueError("duplicate archived file names")
        if f"{repository}-{tag}.zip" not in names:
            raise ValueError("record lacks the exact repository/tag source archive")
        if type(record.get("id")) is not int or record["id"] < 1:
            raise ValueError("invalid public record ID")
        if (
            record.get("doi") != f"10.5281/zenodo.{record['id']}"
            or record["doi"] == concept_doi
        ):
            raise ValueError("record lacks a distinct valid version DOI")
        entry = {
            "repository": repository,
            "verified-version": version,
            "concept-doi": concept_doi,
            "version-doi": record["doi"],
            "record-id": record["id"],
            "files": evidence,
        }
        errors = verify_record(entry, record)
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        errors = [str(error)]
    if errors:
        return {
            **result,
            "state": "invalid",
            "escalation_required": True,
            "errors": errors,
        }
    return {
        **result,
        "state": "verified",
        "escalation_required": False,
        "record_id": record["id"],
        "concept_doi": concept_doi,
        "version_doi": record["doi"],
        "files": [
            {"key": item["name"], "size": item["size"], "checksum": item["checksum"]}
            for item in evidence
        ],
    }


def exit_status(results: list[dict]) -> int:
    if any(item["state"] == "temporarily_unavailable" for item in results):
        return 2
    return int(any(item["state"] in {"absent", "invalid"} for item in results))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--concept-doi", required=True)
    parser.add_argument(
        "--since", required=True, help="Fixed adoption cutoff, never a rolling lookback"
    )
    parser.add_argument(
        "--tag",
        default="",
        help="Probe this exact public tag, including older releases",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(
        r"uibcdf/[A-Za-z0-9_.-]+", args.repository
    ) or not DOI_RE.fullmatch(args.concept_doi):
        parser.error("a UIBCDF repository and a valid Zenodo concept DOI are required")
    results = []
    outcome = 2
    diagnostic = None
    now = datetime.now(timezone.utc)
    try:
        since = timestamp(args.since)
        if since > now:
            raise ValueError("adoption cutoff cannot be in the future")
        if args.tag:
            payload = fetch_json(
                f"https://api.github.com/repos/{args.repository}/releases/tags/{quote(args.tag, safe='')}",
                github=True,
            )
            if not isinstance(payload, dict) or payload.get("tag_name") != args.tag:
                raise EvidenceUnavailable(
                    "GitHub exact-tag response has a different identity"
                )
            releases = select_releases(
                [payload], datetime.min.replace(tzinfo=timezone.utc), now
            )
            if not releases:
                raise ValueError("requested tag is not a public release")
        else:
            releases = select_releases(fetch_releases(args.repository), since, now)
        unavailable = False
        records = []
        if releases:
            try:
                records = fetch_records(args.concept_doi)
            except EvidenceUnavailable as error:
                unavailable = True
                diagnostic = str(error)
        results = [
            evaluate_release(
                item,
                records,
                args.repository,
                args.concept_doi,
                now,
                unavailable=unavailable,
            )
            for item in releases
        ]
        outcome = exit_status(results)
    except (EvidenceUnavailable, ValueError, KeyError, TypeError) as error:
        diagnostic = str(error)
    report = {
        "repository": args.repository,
        "observed_at": now.isoformat(),
        "exit_status": outcome,
        "results": results,
    }
    if diagnostic:
        report["query_error"] = diagnostic
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for item in results:
        print(
            f"{item['state'].upper()} {args.repository} {item['tag']} age={item['age_hours']}h escalation={item['escalation_required']}"
        )
    if not results:
        print(
            "No covered public releases."
            if outcome == 0
            else "TEMPORARILY_UNAVAILABLE: release discovery incomplete."
        )
    if diagnostic:
        print(diagnostic, file=sys.stderr)
    return outcome


if __name__ == "__main__":
    sys.exit(main())

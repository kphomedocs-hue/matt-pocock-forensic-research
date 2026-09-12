#!/usr/bin/env python3
"""Classify every failed GitHub Actions run in the forensic research repo.

Produces a durable JSON ledger and Markdown summary. Unknowns remain explicit
and are treated as a failed closure condition by the workflow.
"""
from __future__ import annotations

import io
import json
import os
import pathlib
import subprocess
import urllib.request
import zipfile
from collections import Counter

REPO = "kphomedocs-hue/matt-pocock-forensic-research"
API = f"https://api.github.com/repos/{REPO}"
OUT_JSON = pathlib.Path("00_TOOLING_FAILURE_LEDGER.json")
OUT_MD = pathlib.Path("00_TOOLING_FAILURE_LEDGER.md")
CLASSIFICATION_VERSION = 2


def request(url: str, accept: str = "application/vnd.github+json") -> bytes:
    headers = {
        "Accept": accept,
        "User-Agent": "forensic-workflow-failure-classifier",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def get_json(url: str):
    return json.loads(request(url).decode("utf-8"))


def fetch_failed_runs() -> list[dict]:
    runs: list[dict] = []
    page = 1
    while True:
        data = get_json(f"{API}/actions/runs?status=failure&per_page=100&page={page}")
        chunk = data.get("workflow_runs", [])
        runs.extend(chunk)
        if len(chunk) < 100:
            break
        page += 1
    return runs


def fetch_job_log(job_id: int) -> str:
    """Use curl for GitHub's cross-host signed-log redirect."""
    try:
        token = os.environ.get("GITHUB_TOKEN", "")
        cmd = [
            "curl", "-L", "--fail", "--silent", "--show-error",
            "-H", "Accept: application/vnd.github+json",
            "-H", "X-GitHub-Api-Version: 2022-11-28",
            "-H", "User-Agent: forensic-workflow-failure-classifier",
        ]
        if token:
            cmd += ["-H", f"Authorization: Bearer {token}"]
        cmd += [f"{API}/actions/jobs/{job_id}/logs"]
        raw = subprocess.check_output(cmd, timeout=90)
        if raw[:2] == b"PK":
            with zipfile.ZipFile(io.BytesIO(raw)) as zf:
                return "\n".join(
                    zf.read(name).decode("utf-8", errors="replace")
                    for name in zf.namelist()
                )
        return raw.decode("utf-8", errors="replace")
    except Exception as exc:
        return f"<LOG_FETCH_ERROR {type(exc).__name__}: {exc}>"


def classify(failed_step: str, log: str) -> tuple[str, str, str]:
    s = failed_step.lower()
    l = log.lower()

    # Publication races can affect any generated-output workflow, not only the
    # original ledger and graph jobs.
    if "commit" in s and (
        "fetch first" in l
        or "non-fast-forward" in l
        or "failed to push some refs" in l
    ):
        return (
            "PUSH_RACE",
            "TEMPORARILY_STALE",
            "Generated output was valid locally but publication lost a race to main.",
        )

    if "rebuild frozen census and ledger" in s:
        parser_signatures = (
            "has no durable `status:` line",
            "has no `status: **...**` line",
            "has no `status:",
            "invalid durable status",
            "invalid durable",
        )
        if any(sig in l for sig in parser_signatures):
            return (
                "STATUS_PARSER",
                "DELAYED_PROMOTION",
                "Ledger failed closed on durable-note status parsing.",
            )
        return (
            "LEDGER_BUILD",
            "REQUIRES_REVIEW",
            "Ledger generation itself failed.",
        )

    if "validate physical denominator" in s:
        return (
            "DENOMINATOR_VALIDATION",
            "HIGH_RISK_REQUIRES_REVIEW",
            "Frozen-census invariant failed.",
        )

    if "build graph" in s:
        return (
            "GRAPH_BUILD",
            "REQUIRES_REVIEW",
            "Connection graph generation failed.",
        )

    if "validate generated outputs" in s:
        return (
            "OUTPUT_VALIDATION",
            "REQUIRES_REVIEW",
            "Expected generated graph output was missing or empty.",
        )

    # Foundation-validator failures are expected to fail closed while a
    # foundation inconsistency or validator defect is being repaired. Keep
    # them distinct from source-repository defects.
    if "validate foundation" in s or "enforce hard-integrity gate" in s:
        if "duplicate current contradiction ids" in l or "closure overlay id set" in l:
            return (
                "FOUNDATION_REGISTER_GATE",
                "DETECTED_AND_BLOCKED",
                "Foundation gate blocked on contradiction-register structural consistency.",
            )
        if "frozen commit missing/mismatch" in l or "blob sha missing/mismatch" in l:
            return (
                "FOUNDATION_PROVENANCE_GATE",
                "DETECTED_AND_BLOCKED",
                "Foundation gate blocked on durable-note provenance metadata.",
            )
        if "foundation integrity validation failed" in l or "hard integrity errors:" in l:
            return (
                "FOUNDATION_GATE",
                "DETECTED_AND_BLOCKED",
                "Foundation validator detected a hard inconsistency and blocked promotion.",
            )
        return (
            "FOUNDATION_GATE",
            "REQUIRES_REVIEW",
            "Foundation integrity gate failed without a more specific known signature.",
        )

    if "validate generated report files" in s:
        return (
            "FOUNDATION_REPORT_OUTPUT",
            "REQUIRES_REVIEW",
            "Foundation report output was missing or empty.",
        )

    if "normalize missing canonical metadata" in s:
        return (
            "NOTE_NORMALIZATION",
            "REQUIRES_REVIEW",
            "Canonical durable-note metadata normalization failed.",
        )

    if "classify failed runs" in s:
        return (
            "FAILURE_CLASSIFIER",
            "REQUIRES_REVIEW",
            "Historical failure classification itself failed.",
        )

    if "validate failure ledger outputs" in s:
        return (
            "FAILURE_LEDGER_VALIDATION",
            "REQUIRES_REVIEW",
            "Generated failure ledger failed its own closure checks.",
        )

    if "sync latest main" in s or "sync latest main before" in s:
        return (
            "GIT_SYNC",
            "TRANSIENT_OR_REQUIRES_REVIEW",
            "Workflow could not synchronize with the latest main before analysis.",
        )

    if "checkout" in s or "setup python" in s or "set up job" in s:
        return (
            "INFRA_SETUP",
            "TRANSIENT_OR_INFRA",
            "Runner/action setup failed before research logic.",
        )

    if "log_fetch_error" in l:
        return (
            "UNKNOWN_LOG_UNAVAILABLE",
            "UNKNOWN",
            "Failed step is known but its log could not be retrieved.",
        )

    return (
        "UNKNOWN",
        "UNKNOWN",
        "No known signature matched; manual inspection required.",
    )


def main() -> None:
    runs = fetch_failed_runs()
    entries: list[dict] = []
    for run in runs:
        jobs = get_json(f"{API}/actions/runs/{run['id']}/jobs?per_page=100").get("jobs", [])
        failed_jobs = [job for job in jobs if job.get("conclusion") == "failure"]
        if not failed_jobs:
            entries.append(
                {
                    "run_id": run["id"],
                    "run_number": run.get("run_number"),
                    "workflow": run.get("name"),
                    "created_at": run.get("created_at"),
                    "head_sha": run.get("head_sha"),
                    "title": run.get("display_title"),
                    "job_id": None,
                    "failed_step": None,
                    "classification": "UNKNOWN_NO_FAILED_JOB",
                    "impact": "UNKNOWN",
                    "reason": "Run failed but no failed job was returned.",
                }
            )
            continue

        for job in failed_jobs:
            failed_steps = [
                step
                for step in job.get("steps", [])
                if step.get("conclusion") == "failure"
            ]
            failed_step = (
                failed_steps[0]["name"]
                if failed_steps
                else "<unknown failed step>"
            )
            log = fetch_job_log(job["id"])
            cls, impact, reason = classify(failed_step, log)
            entries.append(
                {
                    "run_id": run["id"],
                    "run_number": run.get("run_number"),
                    "workflow": run.get("name"),
                    "created_at": run.get("created_at"),
                    "head_sha": run.get("head_sha"),
                    "title": run.get("display_title"),
                    "job_id": job["id"],
                    "failed_step": failed_step,
                    "classification": cls,
                    "impact": impact,
                    "reason": reason,
                }
            )

    entries.sort(key=lambda entry: (entry.get("created_at") or "", entry["run_id"]))
    counts = Counter(entry["classification"] for entry in entries)
    impacts = Counter(entry["impact"] for entry in entries)
    unknown = sum(
        1
        for entry in entries
        if entry["classification"].startswith("UNKNOWN")
        or entry["impact"] == "UNKNOWN"
    )

    payload = {
        "repository": REPO,
        "classification_version": CLASSIFICATION_VERSION,
        "failed_run_count": len(runs),
        "failed_job_entry_count": len(entries),
        "classification_counts": dict(sorted(counts.items())),
        "impact_counts": dict(sorted(impacts.items())),
        "unknown_entries": unknown,
        "entries": entries,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Tooling Failure Ledger",
        "",
        f"Repository: `{REPO}`",
        "",
        f"Classifier version: **{CLASSIFICATION_VERSION}**",
        "",
        f"Failed workflow runs enumerated: **{len(runs)}**",
        "",
        f"Failed job entries classified: **{len(entries)}**",
        "",
        f"Unknown/unclassified entries: **{unknown}**",
        "",
        "## Classification summary",
        "",
        "| Classification | Count |",
        "|---|---:|",
    ]
    md += [f"| {key} | {value} |" for key, value in sorted(counts.items())]
    md += [
        "",
        "## Impact summary",
        "",
        "| Impact | Count |",
        "|---|---:|",
    ]
    md += [f"| {key} | {value} |" for key, value in sorted(impacts.items())]
    md += [
        "",
        "## Run ledger",
        "",
        "| Run | Date | Workflow | Failed step | Classification | Impact |",
        "|---:|---|---|---|---|---|",
    ]
    for entry in entries:
        step = (entry.get("failed_step") or "").replace("|", "\\|")
        workflow = (entry.get("workflow") or "").replace("|", "\\|")
        md.append(
            f"| {entry['run_id']} | {entry.get('created_at','')} | {workflow} | "
            f"{step} | {entry['classification']} | {entry['impact']} |"
        )
    md += [
        "",
        "## Closure rule",
        "",
        "This ledger is closed only when `unknown_entries` is exactly zero. The CI workflow enforces this condition.",
        "",
    ]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print(
        f"Classified {len(entries)} failed job entries from {len(runs)} failed runs; "
        f"unknown={unknown}; counts={dict(counts)}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Classify every failed GitHub Actions run in the forensic research repo.

Produces a durable JSON ledger and Markdown summary. Unknowns remain explicit.
"""
from __future__ import annotations

import io
import json
import os
import pathlib
import re
import subprocess
import urllib.request
import zipfile
from collections import Counter

REPO = "kphomedocs-hue/matt-pocock-forensic-research"
API = f"https://api.github.com/repos/{REPO}"
OUT_JSON = pathlib.Path("00_TOOLING_FAILURE_LEDGER.json")
OUT_MD = pathlib.Path("00_TOOLING_FAILURE_LEDGER.md")


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
                return "\n".join(zf.read(n).decode("utf-8", errors="replace") for n in zf.namelist())
        return raw.decode("utf-8", errors="replace")
    except Exception as exc:
        return f"<LOG_FETCH_ERROR {type(exc).__name__}: {exc}>"


def classify(failed_step: str, log: str) -> tuple[str, str, str]:
    s = failed_step.lower()
    l = log.lower()
    if "commit regenerated ledger" in s or "commit generated graph" in s:
        if "fetch first" in l or "non-fast-forward" in l or "failed to push some refs" in l:
            return "PUSH_RACE", "TEMPORARILY_STALE", "Generated output was valid locally but publication lost a race to main."
        if "nothing to commit" in l:
            return "COMMIT_GATE", "NO_EVIDENCE_CORRUPTION", "Commit step found no staged change."
    if "rebuild frozen census and ledger" in s:
        parser_signatures = (
            "has no durable `status:` line",
            "has no `status: **...**` line",
            "has no `status:",
            "invalid durable status",
            "invalid durable",
        )
        if any(sig in l for sig in parser_signatures):
            return "STATUS_PARSER", "DELAYED_PROMOTION", "Ledger failed closed on durable-note status parsing."
        return "LEDGER_BUILD", "REQUIRES_REVIEW", "Ledger generation itself failed."
    if "validate physical denominator" in s:
        return "DENOMINATOR_VALIDATION", "HIGH_RISK_REQUIRES_REVIEW", "Frozen-census invariant failed."
    if "build graph" in s:
        return "GRAPH_BUILD", "REQUIRES_REVIEW", "Connection graph generation failed."
    if "validate generated outputs" in s:
        return "OUTPUT_VALIDATION", "REQUIRES_REVIEW", "Expected generated graph output missing/empty."
    if "checkout" in s or "setup python" in s or "set up job" in s:
        return "INFRA_SETUP", "TRANSIENT_OR_INFRA", "Runner/action setup failed before research logic."
    if "log_fetch_error" in l:
        return "UNKNOWN_LOG_UNAVAILABLE", "UNKNOWN", "Failed step known, log could not be retrieved."
    return "UNKNOWN", "UNKNOWN", "No known signature matched; manual inspection required."


def main() -> None:
    runs = fetch_failed_runs()
    entries: list[dict] = []
    for run in runs:
        jobs = get_json(f"{API}/actions/runs/{run['id']}/jobs?per_page=100").get("jobs", [])
        failed_jobs = [j for j in jobs if j.get("conclusion") == "failure"]
        if not failed_jobs:
            entries.append({
                "run_id": run["id"], "run_number": run.get("run_number"), "workflow": run.get("name"),
                "created_at": run.get("created_at"), "head_sha": run.get("head_sha"), "title": run.get("display_title"),
                "job_id": None, "failed_step": None, "classification": "UNKNOWN_NO_FAILED_JOB",
                "impact": "UNKNOWN", "reason": "Run failed but no failed job was returned.",
            })
            continue
        for job in failed_jobs:
            failed_steps = [s for s in job.get("steps", []) if s.get("conclusion") == "failure"]
            failed_step = failed_steps[0]["name"] if failed_steps else "<unknown failed step>"
            log = fetch_job_log(job["id"])
            cls, impact, reason = classify(failed_step, log)
            entries.append({
                "run_id": run["id"], "run_number": run.get("run_number"), "workflow": run.get("name"),
                "created_at": run.get("created_at"), "head_sha": run.get("head_sha"), "title": run.get("display_title"),
                "job_id": job["id"], "failed_step": failed_step, "classification": cls,
                "impact": impact, "reason": reason,
            })

    entries.sort(key=lambda e: (e.get("created_at") or "", e["run_id"]))
    counts = Counter(e["classification"] for e in entries)
    impacts = Counter(e["impact"] for e in entries)
    unknown = sum(1 for e in entries if e["classification"].startswith("UNKNOWN") or e["impact"] == "UNKNOWN")
    payload = {
        "repository": REPO,
        "failed_run_count": len(runs),
        "failed_job_entry_count": len(entries),
        "classification_counts": dict(sorted(counts.items())),
        "impact_counts": dict(sorted(impacts.items())),
        "unknown_entries": unknown,
        "entries": entries,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Tooling Failure Ledger", "",
        f"Repository: `{REPO}`", "",
        f"Failed workflow runs enumerated: **{len(runs)}**", "",
        f"Failed job entries classified: **{len(entries)}**", "",
        f"Unknown/unclassified entries: **{unknown}**", "",
        "## Classification summary", "",
        "| Classification | Count |", "|---|---:|",
    ]
    md += [f"| {k} | {v} |" for k, v in sorted(counts.items())]
    md += ["", "## Impact summary", "", "| Impact | Count |", "|---|---:|"]
    md += [f"| {k} | {v} |" for k, v in sorted(impacts.items())]
    md += ["", "## Run ledger", "", "| Run | Date | Workflow | Failed step | Classification | Impact |", "|---:|---|---|---|---|---|"]
    for e in entries:
        step = (e.get("failed_step") or "").replace("|", "\\|")
        title = (e.get("workflow") or "").replace("|", "\\|")
        md.append(f"| {e['run_id']} | {e.get('created_at','')} | {title} | {step} | {e['classification']} | {e['impact']} |")
    md += ["", "## Closure rule", "", "This ledger is complete only when `unknown_entries` is zero, or every remaining unknown has a separately documented reason and manual disposition.", ""]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"Classified {len(entries)} failed job entries from {len(runs)} failed runs; unknown={unknown}; counts={dict(counts)}")


if __name__ == "__main__":
    main()

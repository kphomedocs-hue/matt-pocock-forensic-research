#!/usr/bin/env python3
"""Classify failed and cancelled GitHub Actions runs in the forensic research repo.

Produces a durable JSON ledger and Markdown summary. Unknown or unresolved
incidents remain explicit and fail the closure gate.
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
CLASSIFICATION_VERSION = 3

FIXED_CROSS_WORKFLOW_CANCEL_IDS = {
    34712776661,
    34712784616,
    34712792316,
}
FIXED_CLASSIFIER_SCHEMA_TRANSITION_IDS = {34713138258}
FIXED_CLASSIFIER_CLOSURE_GATE_IDS = {34713153565}
FIXED_PHASE3_PROMOTION_PROVENANCE_COMPAT_IDS = {34738911437}
FIXED_PHASE3_QUALITY_RECHECK_IDS = {34740170053}
FIXED_PHASE4_BATCH_BOOTSTRAP_TRIGGER_IDS = {34745903691}
FIXED_PHASE4_GENERATED_STATUS_PRE_RENDER_IDS = {35131376649}
FIXED_PHASE4_RUNTIME_COMMIT_RACE_IDS = {35131377043, 35131377033}


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


def fetch_runs(status: str) -> list[dict]:
    runs: list[dict] = []
    page = 1
    while True:
        data = get_json(f"{API}/actions/runs?status={status}&per_page=100&page={page}")
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


def classify_failure(run_id: int, failed_step: str, log: str) -> tuple[str, str, str]:
    if run_id in FIXED_CLASSIFIER_SCHEMA_TRANSITION_IDS:
        return (
            "CLASSIFIER_SCHEMA_TRANSITION",
            "FIXED_CONFIGURATION_MISMATCH",
            "Classifier script emitted schema v3 while the then-current workflow still asserted v2; the workflow was subsequently updated to assert v3.",
        )
    if run_id in FIXED_CLASSIFIER_CLOSURE_GATE_IDS:
        return (
            "CLASSIFIER_CLOSURE_GATE",
            "DETECTED_AND_BLOCKED",
            "The v3 closure gate correctly refused to pass while the preceding schema-transition incident remained unresolved; that root incident is now explicitly reconciled.",
        )
    if run_id in FIXED_PHASE3_PROMOTION_PROVENANCE_COMPAT_IDS:
        return (
            "PHASE3_PROMOTION_PROVENANCE_PARSER",
            "DETECTED_AND_BLOCKED_FIXED",
            "The first Phase 3 promoter failed closed because it did not recognize the accepted legacy `Frozen blob SHA` note label. No note changes were committed; the parser was aligned with the foundation validator and the next run succeeded.",
        )
    if run_id in FIXED_PHASE3_QUALITY_RECHECK_IDS:
        return (
            "PHASE3_QUALITY_RECHECK_GATE",
            "DETECTED_AND_BLOCKED_FIXED",
            "The first second-order Phase 3 quality gate deliberately failed closed after exposing duplicated history-definition truth and additional Phase 3 quality debt. History definitions were moved to the durable ledger, master-ledger connection counts and cryptographic build fingerprints were added, and the strengthened atomic Phase 3 rebuild subsequently passed.",
        )
    if run_id in FIXED_PHASE4_GENERATED_STATUS_PRE_RENDER_IDS:
        return (
            "PHASE4_GENERATED_STATUS_PRE_RENDER",
            "DETECTED_AND_BLOCKED_FIXED",
            "The main guard correctly detected stale generated Phase 4/status files on the source commit. The dedicated Phase 4 validation workflow rendered and atomically published the checkpoint; the later remote main is current.",
        )
    if run_id in FIXED_PHASE4_RUNTIME_COMMIT_RACE_IDS:
        return (
            "PHASE4_RUNTIME_COMMIT_RACE",
            "TEMPORARILY_STALE",
            "An unrelated push launched runtime producers concurrently with Phase 4 rendering. Their isolated checks and rebuild gates passed; only the final evidence-publication commit lost the race, so no partial runtime evidence was published.",
        )

    if run_id in FIXED_PHASE4_BATCH_BOOTSTRAP_TRIGGER_IDS:
        return (
            "PHASE4_BATCH_BOOTSTRAP_TRIGGER",
            "NO_DATA_CHANGE_FIXED",
            "Creating the Phase 4 batch workflow matched its own bootstrap path filter, so the importer ran before any `04_PHASE4_BATCH.json` existed and failed closed. No research artifact was changed. The automatic trigger was narrowed to batch-file pushes only.",
        )

    s = failed_step.lower()
    l = log.lower()

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
        return "LEDGER_BUILD", "REQUIRES_REVIEW", "Ledger generation itself failed."

    if "validate physical denominator" in s:
        return (
            "DENOMINATOR_VALIDATION",
            "HIGH_RISK_REQUIRES_REVIEW",
            "Frozen-census invariant failed.",
        )

    if "build graph" in s:
        return "GRAPH_BUILD", "REQUIRES_REVIEW", "Connection graph generation failed."

    if "run phase 3 quality recheck" in s or "enforce phase 3 quality gate" in s:
        return (
            "PHASE3_QUALITY_GATE",
            "REQUIRES_REVIEW",
            "Phase 3 second-order quality validation failed; no future quality failure is considered resolved without explicit adjudication.",
        )

    if "rebuild ordered phase 3 state" in s or "validate atomic phase 3 outputs" in s:
        return (
            "PHASE3_ATOMIC_REBUILD",
            "REQUIRES_REVIEW",
            "The authoritative ordered Phase 3 rebuild or its acceptance gate failed.",
        )

    if "validate generated outputs" in s:
        return (
            "OUTPUT_VALIDATION",
            "REQUIRES_REVIEW",
            "Expected generated graph output was missing or empty.",
        )

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

    if "classify failed" in s:
        return (
            "FAILURE_CLASSIFIER",
            "REQUIRES_REVIEW",
            "Historical incident classification itself failed.",
        )

    if "validate failure ledger outputs" in s or "validate tooling incident ledger outputs" in s:
        match = re.search(
            r"classified\s+\d+\s+incident entries.*?unknown=(\d+);\s*unresolved=(\d+)",
            l,
        )
        if match and (int(match.group(1)) > 0 or int(match.group(2)) > 0) and "assertionerror" in l:
            return (
                "CLASSIFIER_CLOSURE_GATE",
                "DETECTED_AND_BLOCKED",
                "The classifier completed successfully, then its closure assertion intentionally blocked publication because at least one separately listed incident remained unknown or review-required.",
            )
        return (
            "FAILURE_LEDGER_VALIDATION",
            "REQUIRES_REVIEW",
            "Generated tooling incident ledger failed validation for a reason other than the expected zero-unknown/zero-unresolved closure gate.",
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

    return "UNKNOWN", "UNKNOWN", "No known signature matched; manual inspection required."


def classify_cancelled(run: dict) -> tuple[str, str, str]:
    run_id = int(run["id"])
    workflow = run.get("name") or ""

    if run_id in FIXED_CROSS_WORKFLOW_CANCEL_IDS:
        return (
            "CROSS_WORKFLOW_CONCURRENCY_CANCEL",
            "DISCARDED_EXECUTION_FIXED",
            "Distinct workflow execution was discarded by the former shared concurrency lane; per-workflow lanes now replace it.",
        )

    if workflow == "Classify tooling failures":
        return (
            "CLASSIFIER_REFRESH_SUPERSEDED",
            "REDUNDANT_REFRESH_DISCARDED",
            "A classifier refresh was superseded by a newer refresh; the latest refresh reconstructs the complete incident ledger from GitHub history.",
        )

    return (
        "CANCELLED_RUN_REQUIRES_REVIEW",
        "REQUIRES_REVIEW",
        "A workflow run was cancelled and does not match a reconciled historical cancellation class.",
    )


def failure_entries(runs: list[dict]) -> list[dict]:
    entries: list[dict] = []
    for run in runs:
        run_id = int(run["id"])
        jobs = get_json(f"{API}/actions/runs/{run_id}/jobs?per_page=100").get("jobs", [])
        failed_jobs = [job for job in jobs if job.get("conclusion") == "failure"]
        if not failed_jobs:
            entries.append({
                "run_id": run_id,
                "run_conclusion": "failure",
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
            })
            continue

        for job in failed_jobs:
            failed_steps = [
                step for step in job.get("steps", []) if step.get("conclusion") == "failure"
            ]
            failed_step = failed_steps[0]["name"] if failed_steps else "<unknown failed step>"
            log = fetch_job_log(job["id"])
            cls, impact, reason = classify_failure(run_id, failed_step, log)
            entries.append({
                "run_id": run_id,
                "run_conclusion": "failure",
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
            })
    return entries


def cancelled_entries(runs: list[dict]) -> list[dict]:
    entries: list[dict] = []
    for run in runs:
        cls, impact, reason = classify_cancelled(run)
        entries.append({
            "run_id": int(run["id"]),
            "run_conclusion": "cancelled",
            "run_number": run.get("run_number"),
            "workflow": run.get("name"),
            "created_at": run.get("created_at"),
            "head_sha": run.get("head_sha"),
            "title": run.get("display_title"),
            "job_id": None,
            "failed_step": None,
            "classification": cls,
            "impact": impact,
            "reason": reason,
        })
    return entries


def main() -> None:
    failed_runs = fetch_runs("failure")
    cancelled_runs = fetch_runs("cancelled")
    entries = failure_entries(failed_runs) + cancelled_entries(cancelled_runs)
    entries.sort(key=lambda entry: (entry.get("created_at") or "", entry["run_id"]))

    counts = Counter(entry["classification"] for entry in entries)
    impacts = Counter(entry["impact"] for entry in entries)
    unknown = sum(
        1 for entry in entries
        if entry["classification"].startswith("UNKNOWN") or entry["impact"] == "UNKNOWN"
    )
    unresolved = sum(
        1 for entry in entries
        if "REQUIRES_REVIEW" in entry["classification"] or "REQUIRES_REVIEW" in entry["impact"]
    )

    payload = {
        "repository": REPO,
        "classification_version": CLASSIFICATION_VERSION,
        "failed_run_count": len(failed_runs),
        "cancelled_run_count": len(cancelled_runs),
        "incident_run_count": len(failed_runs) + len(cancelled_runs),
        "incident_entry_count": len(entries),
        "classification_counts": dict(sorted(counts.items())),
        "impact_counts": dict(sorted(impacts.items())),
        "unknown_entries": unknown,
        "unresolved_entries": unresolved,
        "entries": entries,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Tooling Failure & Cancellation Ledger", "",
        f"Repository: `{REPO}`", "",
        f"Classifier version: **{CLASSIFICATION_VERSION}**", "",
        f"Failed workflow runs enumerated: **{len(failed_runs)}**", "",
        f"Cancelled workflow runs enumerated: **{len(cancelled_runs)}**", "",
        f"Total incident runs: **{len(failed_runs) + len(cancelled_runs)}**", "",
        f"Incident entries classified: **{len(entries)}**", "",
        f"Unknown entries: **{unknown}**", "",
        f"Unresolved/review-required entries: **{unresolved}**", "",
        "## Classification summary", "",
        "| Classification | Count |", "|---|---:|",
    ]
    md += [f"| {key} | {value} |" for key, value in sorted(counts.items())]
    md += ["", "## Impact summary", "", "| Impact | Count |", "|---|---:|"]
    md += [f"| {key} | {value} |" for key, value in sorted(impacts.items())]
    md += [
        "", "## Incident ledger", "",
        "| Run | Conclusion | Date | Workflow | Failed step | Classification | Impact |",
        "|---:|---|---|---|---|---|---|",
    ]
    for entry in entries:
        step = (entry.get("failed_step") or "").replace("|", "\\|")
        workflow = (entry.get("workflow") or "").replace("|", "\\|")
        md.append(
            f"| {entry['run_id']} | {entry['run_conclusion']} | {entry.get('created_at','')} | "
            f"{workflow} | {step} | {entry['classification']} | {entry['impact']} |"
        )
    md += [
        "", "## Closure rule", "",
        "This ledger is closed only when both `unknown_entries` and `unresolved_entries` are exactly zero. CI enforces both conditions.", "",
    ]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print(
        f"Classified {len(entries)} incident entries from "
        f"{len(failed_runs)} failed + {len(cancelled_runs)} cancelled runs; "
        f"unknown={unknown}; unresolved={unresolved}; counts={dict(counts)}"
    )


if __name__ == "__main__":
    main()

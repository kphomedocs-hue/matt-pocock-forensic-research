#!/usr/bin/env python3
"""Stable entrypoint for the historical tooling-incident classifier.

Keeps one-off, fully adjudicated run-ID reconciliations outside the large base
classifier so a narrow audit correction cannot accidentally rewrite historical
classification logic. Also prints only the rows that keep the closure gate
open, so a failed-closed run is directly diagnosable from its job log.
"""
from __future__ import annotations

import json

import classify_failed_workflows as base

PHASE4_RUNTIME_ACCEPTANCE_SCHEMA_TRANSITION_IDS = {34752972889}

_original_classify_failure = base.classify_failure


def classify_failure(run_id: int, failed_step: str, log: str):
    if run_id in PHASE4_RUNTIME_ACCEPTANCE_SCHEMA_TRANSITION_IDS:
        return (
            "PHASE4_RUNTIME_ACCEPTANCE_SCHEMA_TRANSITION",
            "NO_RESEARCH_DATA_CHANGE_FIXED",
            "The new B-004 local runtime check and every Phase 4 validator passed, but this older queued run retained the prior acceptance assertion expecting only B-015/B-018/B-056. The acceptance gate was updated to include B-004 and the immediately following run 34752990655 passed and published the same validated state.",
        )
    return _original_classify_failure(run_id, failed_step, log)


base.classify_failure = classify_failure


def print_open_rows() -> None:
    data = json.loads(base.OUT_JSON.read_text(encoding="utf-8"))
    open_rows = [
        row for row in data["entries"]
        if row["classification"].startswith("UNKNOWN")
        or row["impact"] == "UNKNOWN"
        or "REQUIRES_REVIEW" in row["classification"]
        or "REQUIRES_REVIEW" in row["impact"]
    ]
    if not open_rows:
        print("OPEN_TOOLING_ROWS: none")
        return
    print("OPEN_TOOLING_ROWS_BEGIN")
    for row in open_rows:
        print(json.dumps({
            "run_id": row["run_id"],
            "workflow": row.get("workflow"),
            "head_sha": row.get("head_sha"),
            "failed_step": row.get("failed_step"),
            "classification": row.get("classification"),
            "impact": row.get("impact"),
            "reason": row.get("reason"),
        }, sort_keys=True))
    print("OPEN_TOOLING_ROWS_END")


if __name__ == "__main__":
    base.main()
    print_open_rows()

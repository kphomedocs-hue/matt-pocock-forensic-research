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

# Exact historical Phase 3 runs that failed closed while the durable history
# ledger/bindings were being reconciled. Future Phase 3 failures still fall
# through to the base classifier and remain review-required.
PHASE3_HISTORY_EVENT_COUNT_TRANSITION_IDS = {
    34750032928,
    34753085943,
}
PHASE3_HISTORY_DEFINITION_RECONCILIATION_IDS = {
    34750032982,
    34753085869,
    34753173848,
    34753493374,
}
PHASE3_HISTORY_EXACT_EVIDENCE_GATE_IDS = {
    34753173840,
    34753493482,
}

# Exact Phase 4 repair/tooling transitions. These IDs are deliberately narrow:
# new failures in the same steps must still be inspected rather than inherited.
PHASE4_RUNTIME_PROVENANCE_ID_TYPE_TRANSITION_IDS = {34849974317}
PHASE4_RUNTIME_PROVENANCE_WIRING_TRANSITION_IDS = {34850175820}
PHASE4_CT019_ROW_ANCHOR_TRANSITION_IDS = {
    34850571686,
    34851582989,
}

_original_classify_failure = base.classify_failure


def classify_failure(run_id: int, failed_step: str, log: str):
    if run_id in PHASE4_RUNTIME_ACCEPTANCE_SCHEMA_TRANSITION_IDS:
        return (
            "PHASE4_RUNTIME_ACCEPTANCE_SCHEMA_TRANSITION",
            "NO_RESEARCH_DATA_CHANGE_FIXED",
            "The new B-004 local runtime check and every Phase 4 validator passed, but this older queued run retained the prior acceptance assertion expecting only B-015/B-018/B-056. The acceptance gate was updated to include B-004 and the immediately following run 34752990655 passed and published the same validated state.",
        )
    if run_id in PHASE3_HISTORY_EVENT_COUNT_TRANSITION_IDS:
        return (
            "PHASE3_HISTORY_EVENT_COUNT_TRANSITION",
            "DETECTED_AND_BLOCKED_FIXED",
            "The ordered Phase 3 rebuild failed closed after the durable history ledger had grown from nine to ten events while the generated-history path still expected nine. No promotion occurred from the inconsistent state; the H-001..H-010 durable/generated history set is now reconciled.",
        )
    if run_id in PHASE3_HISTORY_DEFINITION_RECONCILIATION_IDS:
        return (
            "PHASE3_HISTORY_DEFINITION_RECONCILIATION",
            "DETECTED_AND_BLOCKED_FIXED",
            "The Phase 3 quality gate detected drift between durable history definitions and generated bindings (including the H-010 denominator and H-003/H-004/H-009 definition state during reconciliation). The gate blocked the inconsistent snapshots; the current H-001..H-010 bindings are reconciled.",
        )
    if run_id in PHASE3_HISTORY_EXACT_EVIDENCE_GATE_IDS:
        return (
            "PHASE3_HISTORY_EXACT_EVIDENCE_GATE",
            "DETECTED_AND_BLOCKED_FIXED",
            "The ordered Phase 3 rebuild refused to publish while H-003 lacked exact PR or 40-character commit evidence. The missing history lineage was subsequently reconciled and the current H-001..H-010 history set passes the rebuilt gates.",
        )
    if run_id in PHASE4_RUNTIME_PROVENANCE_ID_TYPE_TRANSITION_IDS:
        return (
            "PHASE4_RUNTIME_PROVENANCE_ID_TYPE_TRANSITION",
            "FIXED_CONFIGURATION_MISMATCH",
            "The Phase 4 repair reached a green behavior matrix/coverage/queue, then the new runtime-provenance validator correctly rejected seven historical workflow_run_id values stored as digit strings rather than positive integers. The follow-up repair normalized those seven IDs and provenance validation passed.",
        )
    if run_id in PHASE4_RUNTIME_PROVENANCE_WIRING_TRANSITION_IDS:
        return (
            "PHASE4_RUNTIME_PROVENANCE_WIRING_TRANSITION",
            "FIXED_CONFIGURATION_MISMATCH",
            "Runtime provenance and foundation validation were green, but the repair invariant check detected that phase4-runtime-smoke.yml had not yet wired the new provenance-validation step. The workflow wiring was subsequently added and the main Phase 4 guard now validates runtime provenance successfully.",
        )
    if run_id in PHASE4_CT019_ROW_ANCHOR_TRANSITION_IDS:
        return (
            "PHASE4_CT019_ROW_ANCHOR_TRANSITION",
            "NO_RESEARCH_DATA_CHANGE_FIXED",
            "The six-test Phase 4 runtime smoke itself passed, then the CT-019 adjudication helper failed because it searched for obsolete full-row wording after CT-019 had already been rewritten as an audit correction. The helper now matches the stable CT-019 row IDs; run 34866017975 passed the full smoke/adjudication workflow with that idempotent repair.",
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

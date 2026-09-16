#!/usr/bin/env python3
"""Stable entrypoint for the historical tooling-incident classifier.

Keeps one-off, fully adjudicated run-ID reconciliations outside the large base
classifier so a narrow audit correction cannot accidentally rewrite historical
classification logic. Also preserves a previously closed historical
classification when GitHub temporarily cannot return that same run's job log.
New or previously open incidents still fail closed.
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

PHASE3_HISTORY_LEDGER_PARSER_SCOPE_IDS = {35127421564}
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
PHASE4_DEEP_MODULE_HARNESS_BOOTSTRAP_TRANSITION_IDS = {34867570179}
PHASE4_DEEP_MODULE_TYPESCRIPT_COMPATIBILITY_TRANSITION_IDS = {34867918904}
PHASE4_PRECOMMIT_EXECUTABLE_PREDICATE_DISCOVERY_IDS = {34868912572}
PHASE4_STATUS_CHECKPOINT_BOOTSTRAP_TRANSITION_IDS = {34925982246}
PHASE4_ARCHITECTURE_REPORT_BOOTSTRAP_MISSING_SCRIPT_IDS = {34928147482}
PHASE4_ARCHITECTURE_REPORT_CONNECTOR_ESCAPE_TRANSITION_IDS = {
    34928190384,
    34928232337,
    34928290191,
}
PHASE4_STATUS_STALE_GUARD_TRANSITION_IDS = {
    34926294022,
    34926308847,
    34926329873,
}
TOOLING_CLASSIFIER_BACKLOG_CLOSURE_IDS = {34928459181}
PHASE4_ARCHITECTURE_REPORT_PUBLISH_RACE_IDS = {34929956423}


def _is_closed(row: dict) -> bool:
    classification = str(row.get("classification") or "")
    impact = str(row.get("impact") or "")
    return (
        bool(classification)
        and not classification.startswith("UNKNOWN")
        and impact != "UNKNOWN"
        and "REQUIRES_REVIEW" not in classification
        and "REQUIRES_REVIEW" not in impact
    )


def _load_prior_closed() -> dict[tuple[int, str], tuple[str, str, str]]:
    """Load durable closed classifications before base.main overwrites the ledger.

    The failed-step name is part of the key so a later failure on the same run ID
    cannot accidentally inherit an unrelated adjudication.
    """
    if not base.OUT_JSON.exists():
        return {}
    try:
        data = json.loads(base.OUT_JSON.read_text(encoding="utf-8"))
    except Exception:
        return {}
    prior: dict[tuple[int, str], tuple[str, str, str]] = {}
    for row in data.get("entries", []):
        if not _is_closed(row):
            continue
        run_id = row.get("run_id")
        failed_step = row.get("failed_step")
        if isinstance(run_id, int) and isinstance(failed_step, str) and failed_step:
            prior[(run_id, failed_step)] = (
                str(row["classification"]),
                str(row["impact"]),
                "Preserved from the previously published closed tooling ledger because the current refresh could not retrieve this historical job log. Prior durable reason: "
                + str(row.get("reason") or "closed historical adjudication"),
            )
    return prior


PRIOR_CLOSED = _load_prior_closed()
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
    if run_id in PHASE3_HISTORY_LEDGER_PARSER_SCOPE_IDS:
        return (
            "PHASE3_HISTORY_LEDGER_PARSER_SCOPE",
            "DETECTED_AND_BLOCKED_FIXED",
            "The Phase 3 rebuild correctly refused to publish when the history parser scanned only the ledger Evidence column, even though H-003's exact PR/commit provenance is recorded in its durable Event column. The parser now reads the union of both ledger fields; no generated state was published by the failed run.",
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
    if run_id in PHASE4_DEEP_MODULE_HARNESS_BOOTSTRAP_TRANSITION_IDS:
        return (
            "PHASE4_DEEP_MODULE_HARNESS_BOOTSTRAP_TRANSITION",
            "NO_RESEARCH_DATA_CHANGE_FIXED",
            "The first isolated B-012/B-014 consumer harness failed closed before any runtime promotion while its synthetic TypeScript environment was still being made source-faithful. No behavior row was changed by the failed run. The harness was corrected and pinned to a dependency-cruiser-compatible TypeScript line; run 34868071587 then passed the exact frozen pass/fail/pass and fifth-rule observations and published the evidence.",
        )
    if run_id in PHASE4_DEEP_MODULE_TYPESCRIPT_COMPATIBILITY_TRANSITION_IDS:
        return (
            "PHASE4_DEEP_MODULE_TYPESCRIPT_COMPATIBILITY_TRANSITION",
            "NO_RESEARCH_DATA_CHANGE_FIXED",
            "The second isolated B-012/B-014 harness installed dependency-cruiser 18.3.0 alongside TypeScript 7. Dependency-cruiser explicitly reported support only for TypeScript <7 and therefore cruised 0 modules/0 dependencies, so the fail-closed run produced no valid behavior observation and no promotion. Pinning the synthetic fixture to TypeScript 6 fixed the environment; run 34868071587 passed and published the durable evidence.",
        )
    if run_id in PHASE4_PRECOMMIT_EXECUTABLE_PREDICATE_DISCOVERY_IDS:
        return (
            "PHASE4_PRECOMMIT_EXECUTABLE_PREDICATE_DISCOVERY",
            "DETECTED_AND_BLOCKED_FIXED",
            "The first isolated B-017 run failed closed before promotion because it enforced the frozen setup-pre-commit verification predicate that .husky/pre-commit itself must be executable. Direct runtime plus Husky 9.1.7 source inspection showed the generated user hook is non-executable while Git is wired to an executable .husky/_/pre-commit shim that invokes the user hook through sh -e. The finding was retained as frozen-contract/current-toolchain drift rather than hidden with chmod. Follow-up run 34869643879 completed the actual commit smoke, preserved the executable-bit mismatch in durable evidence, and promoted B-017. No invalid B-017 evidence was published from the failed run.",
        )
    if run_id in PHASE4_STATUS_STALE_GUARD_TRANSITION_IDS:
        return (
            "PHASE4_STATUS_STALE_GUARD_TRANSITION",
            "DETECTED_AND_BLOCKED_FIXED",
            "The main guard correctly detected a generated RESEARCH_STATUS.md stale after an earlier Phase 4 state transition. No invalid research state was accepted; the current generated checkpoint is synchronized and later main-guard runs pass.",
        )
    if run_id in PHASE4_ARCHITECTURE_REPORT_PUBLISH_RACE_IDS:
        return (
            "PUSH_RACE",
            "TEMPORARILY_STALE",
            "The B-008 architecture-report harness and every rebuild validator passed, but its generated-evidence commit lost a non-fast-forward race to concurrent main updates. No stale or invalid evidence was published from the rejected push; the later B-008 durable result remained green.",
        )
    if run_id in TOOLING_CLASSIFIER_BACKLOG_CLOSURE_IDS:
        return (
            "TOOLING_CLASSIFIER_BACKLOG_CLOSURE",
            "DETECTED_AND_BLOCKED_FIXED",
            "The tooling-ledger classifier correctly failed closed because three older stale-status main-guard runs had never been classified. Their exact logs were inspected and mappings were added before the next classifier run.",
        )
    if run_id in PHASE4_ARCHITECTURE_REPORT_BOOTSTRAP_MISSING_SCRIPT_IDS:
        return (
            "PHASE4_ARCHITECTURE_REPORT_BOOTSTRAP_MISSING_SCRIPT",
            "NO_RESEARCH_DATA_CHANGE_FIXED",
            "The newly added workflow ran on its own creation commit before the harness script existed in that commit. It failed closed before any evidence or matrix change. The harness was published in the next connector commit.",
        )
    if run_id in PHASE4_ARCHITECTURE_REPORT_CONNECTOR_ESCAPE_TRANSITION_IDS:
        return (
            "PHASE4_ARCHITECTURE_REPORT_CONNECTOR_ESCAPE_TRANSITION",
            "NO_RESEARCH_DATA_CHANGE_FIXED",
            "Connector publication converted two intended Python newline escapes into literal newlines inside string literals, causing three isolated B-008 harness runs to fail at Python parse time before execution or evidence promotion. The affected lines were corrected, and run 34928358966 passed the isolated test and published B-008 evidence.",
        )
    if run_id in PHASE4_STATUS_CHECKPOINT_BOOTSTRAP_TRANSITION_IDS:
        return (
            "PHASE4_STATUS_CHECKPOINT_BOOTSTRAP_TRANSITION",
            "NO_RESEARCH_DATA_CHANGE_FIXED",
            "All Phase 4 validators and runtime-provenance checks passed. The newly strengthened main guard then intentionally failed because RESEARCH_STATUS.md still contained the pre-generator checkpoint at that exact transition commit. The validation workflow generated and published the synchronized checkpoint immediately afterward as commit c198584d164e7f6ba6221df6eb36ee9f37205dfe; the failure exposed no research-data defect.",
        )

    # A transient GitHub log outage must not regress a previously adjudicated,
    # closed historical row back to UNKNOWN. Only the identical run + failed
    # step may inherit; genuinely new/open incidents continue to fail closed.
    if "<LOG_FETCH_ERROR" in log:
        prior = PRIOR_CLOSED.get((run_id, failed_step))
        if prior:
            return prior

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

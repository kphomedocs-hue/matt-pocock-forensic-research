"""Executable checks for the *synthetic trace* schema, not a human-work gate.

The frozen fixtures omit an owner field; their caller explicitly supplies Owner-A.
Evidence strings, identities and reasons are checked structurally, not authenticated.
See 17_PRE_TRIAL_SEMANTIC_RECHECK.md for the unimplemented evidence obligations.
"""
from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import re

MODEL = {
    "DEFINED": ["PROTOTYPING", "SPECIFIED", "CANCELLED"],
    "PROTOTYPING": ["SPECIFIED", "DEFINED", "BLOCKED", "CANCELLED"],
    "SPECIFIED": ["IN PROGRESS", "DEFINED", "BLOCKED", "CANCELLED"],
    "IN PROGRESS": ["REVIEW", "DEFINED", "BLOCKED", "CANCELLED"],
    "REVIEW": ["ACCEPTED", "REJECTED", "DEFINED", "BLOCKED", "CANCELLED"],
    "REJECTED": ["IN PROGRESS", "DEFINED", "CANCELLED"],
    "ACCEPTED": ["REOPENED"],
    "REOPENED": ["IN PROGRESS", "DEFINED", "CANCELLED"],
    "BLOCKED": ["PROTOTYPING", "SPECIFIED", "IN PROGRESS", "REVIEW", "CANCELLED"],
    "CANCELLED": [],
}
AXES = {"specification_fidelity", "quality_and_standards", "operational_readiness"}


def text(value):
    return isinstance(value, str) and bool(value.strip())


def validate_trace(case, *, owner):
    """Return stable error codes. This interface accepts synthetic fixtures only.

    A single case supplies immutable roles and work ID for the entire trace.
    Baseline changes are allowed only when approving a new SPECIFIED baseline;
    returning to DEFINED after approval requires a never-before-used version.
    """
    errors = []

    def need(ok, code, where="case"):
        if not ok:
            errors.append(f"{where}:{code}")

    if not isinstance(case, dict):
        return ["case:SCHEMA"]
    contributors = case.get("contributors")
    reviewer = case.get("reviewer")
    need(text(owner), "OWNER")
    need(text(case.get("id")), "WORK_ID")
    if not (isinstance(contributors, list) and contributors
            and all(text(p) for p in contributors)):
        return errors + ["case:CONTRIBUTORS"]
    need(len(contributors) == len(set(contributors)), "CONTRIBUTORS")
    need(text(reviewer), "REVIEWER")
    events = case.get("events")
    if not isinstance(events, list) or not events:
        return errors + ["case:EVENTS"]
    current = "DEFINED"
    baseline = "unassigned"
    used_baselines = set()
    blocked_from = None
    previous_time = None
    accepted = False
    for index, event in enumerate(events):
        where = f"event[{index}]"
        if not isinstance(event, dict):
            need(False, "EVENT_SCHEMA", where)
            continue
        source, target = event.get("from"), event.get("to")
        if not isinstance(source, str) or not isinstance(target, str):
            need(False, "STATE_SCHEMA", where)
            continue
        need(source == current, "ROUTE", where)
        need(target in MODEL.get(source, []), "EDGE", where)
        for field in ("actor", "timestamp_utc", "reason", "evidence", "baseline_version"):
            need(text(event.get(field)), f"REQUIRED_{field}", where)
        # Reject non-synthetic inputs: this is not an operational approval engine.
        for field in ("evidence", "unblock_evidence", "accepted_snapshot"):
            if field in event:
                value = event[field]
                need(isinstance(value, str) and value.startswith("synthetic://")
                     and bool(value[len("synthetic://"):].strip()), "SYNTHETIC_EVIDENCE", where)
        if "work_id" in event:
            need(event["work_id"] == case.get("id"), "WORK_ID", where)
        try:
            stamp = event.get("timestamp_utc")
            if not isinstance(stamp, str) or not re.fullmatch(
                    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", stamp):
                raise ValueError("UTC timestamp required")
            timestamp = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            need(timestamp.utcoffset() == timezone.utc.utcoffset(timestamp), "TIMESTAMP", where)
            need(previous_time is None or timestamp >= previous_time, "TIME_ORDER", where)
            previous_time = timestamp
        except (ValueError, TypeError):
            need(False, "TIMESTAMP", where)

        actor = event.get("actor")
        review_action = source == "REVIEW" and target in {"ACCEPTED", "REJECTED"}
        reopen = source == "ACCEPTED" and target == "REOPENED"
        if review_action or reopen:
            need(text(reviewer) and actor == reviewer, "REVIEW_AUTHORITY", where)
            need(reviewer not in contributors, "REVIEW_INDEPENDENCE", where)
        elif source == "IN PROGRESS" and target == "REVIEW":
            need(actor in contributors, "SUBMIT_AUTHORITY", where)
        else:
            need(actor == owner, "OWNER_AUTHORITY", where)
        if target == "REVIEW":
            need(text(reviewer) and reviewer not in contributors, "REVIEW_INDEPENDENCE", where)

        version = event.get("baseline_version")
        if target == "SPECIFIED" and source in {"DEFINED", "PROTOTYPING"}:
            valid_version = isinstance(version, str) and bool(re.fullmatch(r"v[1-9]\d*", version))
            need(valid_version, "BASELINE_VERSION", where)
            need(text(version) and version not in used_baselines, "BASELINE_REUSE", where)
            if valid_version:
                used_baselines.add(version)
                baseline = version
            if source == "DEFINED":
                need(text(event.get("prototype_skip_reason")), "PROTOTYPE_SKIP", where)
        else:
            need(version == baseline, "BASELINE_DRIFT", where)
        if source == "SPECIFIED" or target in {"IN PROGRESS", "REVIEW", "ACCEPTED", "REJECTED"}:
            need(baseline != "unassigned", "BASELINE_UNAPPROVED", where)

        if target == "BLOCKED":
            need(event.get("blocked_from") == source, "BLOCKED_ORIGIN", where)
            need(text(event.get("blocker_owner")), "BLOCKER_OWNER", where)
            need(text(event.get("next_unblock_action")), "UNBLOCK_ACTION", where)
            blocked_from = source
        elif source == "BLOCKED" and target != "CANCELLED":
            need(blocked_from is not None and target == blocked_from, "BLOCKED_RESUME", where)
            need(text(event.get("unblock_evidence")), "UNBLOCK_EVIDENCE", where)
            blocked_from = None

        if review_action:
            verdicts = event.get("review_verdicts")
            if not isinstance(verdicts, dict):
                need(False, "VERDICT_SCHEMA", where)
            else:
                need(set(verdicts) == AXES, "VERDICT_AXES", where)
                need(all(isinstance(v, str) and v in {"PASS", "FAIL"}
                         for v in verdicts.values()), "VERDICT_VALUE", where)
                if target == "ACCEPTED":
                    need(set(verdicts) == AXES and all(v == "PASS" for v in verdicts.values()),
                         "ACCEPT_REQUIRES_PASS", where)
                else:
                    # The historical schema models failure, not per-axis missing-evidence reasons.
                    need(any(v == "FAIL" for v in verdicts.values()), "REJECT_REQUIRES_FAIL", where)
            if target == "ACCEPTED":
                accepted = True
        if reopen:
            need(accepted, "REOPEN_WITHOUT_ACCEPTANCE", where)
            need(event.get("owner_request") == owner, "REOPEN_REQUEST", where)
            need(text(event.get("accepted_snapshot")), "REOPEN_SNAPSHOT", where)
        current = target
    need(current == case.get("expected") and current in MODEL, "TERMINAL")
    return errors


def execute_controls(red_team):
    """Replay four historical attempt payloads against copies of their valid traces.

    Never consult historical observed/result labels to determine actual rejection.
    Each control must fail for its intended semantic reason, not hash/route noise.
    """
    specs = {
        "NC-01": ("C-01", 3, "REVIEW_AUTHORITY"),
        "NC-02": ("C-01", 3, "VERDICT_AXES"),
        "NC-03": ("C-03", 3, "BLOCKED_RESUME"),
        "NC-04": ("C-01", 2, "BASELINE_DRIFT"),
    }
    controls = red_team.get("negative_controls")
    cases = red_team.get("synthetic_cases")
    if not isinstance(controls, list) or not isinstance(cases, list):
        return [], ["CONTROL_SCHEMA"]
    if any(not isinstance(c, dict) for c in controls + cases):
        return [], ["CONTROL_SCHEMA"]
    if len(controls) != 4 or any(not isinstance(c.get("id"), str) for c in controls):
        return [], ["CONTROL_IDS"]
    if sorted(c["id"] for c in controls) != sorted(specs):
        return [], ["CONTROL_IDS"]
    by_id = {c.get("id"): c for c in cases if isinstance(c.get("id"), str)}
    results, errors = [], []
    for control in controls:
        cid = control["id"]
        case_id, index, expected = specs[cid]
        trace = deepcopy(by_id.get(case_id))
        attempt = control.get("attempt")
        if not isinstance(attempt, dict) or trace is None or validate_trace(trace, owner="Owner-A"):
            errors.append(f"{cid}:CONTROL_INPUT")
            continue
        if len(trace["events"]) <= index:
            errors.append(f"{cid}:CONTROL_INPUT")
            continue
        event = trace["events"][index]
        if cid == "NC-03":
            if attempt.get("blocked_from") != trace["events"][index - 1].get("blocked_from"):
                errors.append(f"{cid}:CONTROL_INPUT")
                continue
            event["to"] = attempt.get("to")
        elif cid == "NC-04":
            if attempt.get("old") != event["baseline_version"] or attempt.get("route") != event["from"]:
                errors.append(f"{cid}:CONTROL_INPUT")
                continue
            event["baseline_version"] = attempt.get("now")
        else:
            event.update(attempt)
        # Check the attempted prefix only, avoiding unrelated downstream discontinuities.
        trace["events"] = trace["events"][:index + 1]
        trace["expected"] = event["to"]
        problems = validate_trace(trace, owner="Owner-A")
        rejected = any(p.endswith(":" + expected) for p in problems)
        results.append({"id": cid, "expected_error": expected, "rejected_as_expected": rejected,
                        "errors": problems})
        if not rejected:
            errors.append(f"{cid}:CONTROL_DID_NOT_REJECT_AS_EXPECTED")
    return results, errors

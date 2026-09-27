#!/usr/bin/env python3
"""Fail-closed validation for the neutral-method pre-trial package.

This validates static consistency only. It does not claim human use, agent-runtime
adherence, or promotion of any frozen-source file to VERIFIED.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys

METHOD = pathlib.Path("11_NEUTRAL_OPERATING_METHOD.md")
RED_TEAM = pathlib.Path("12_NEUTRAL_METHOD_RED_TEAM.json")
TRIAL = pathlib.Path("13_PRE_APPLICATION_TRIAL_AND_PILOT_GATE.md")
RECHECK = pathlib.Path("14_PRE_TRIAL_DESK_RECHECK.md")
KIT = pathlib.Path("16_HUMAN_TRIAL_KIT.md")
MANIFEST = pathlib.Path("15_PRE_TRIAL_PACKAGE_MANIFEST.json")
EXPECTED_METHOD_BLOB = "4f3dc9653e5a86456c079dc4a1faf5687aa41271"
FROZEN_SOURCE = "3cca18b368ae95cdbdebbff572ccafa662551015"

EXPECTED_MODEL = {
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


def read(path: pathlib.Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing required pre-trial package file: {path}")
    return path.read_text(encoding="utf-8")


def blob_sha(text: str) -> str:
    data = text.encode("utf-8")
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    method = read(METHOD)
    trial = read(TRIAL)
    recheck = read(RECHECK)
    kit = read(KIT)
    manifest_text = read(MANIFEST)

    try:
        red_team = json.loads(read(RED_TEAM))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Cannot parse {RED_TEAM}: {exc}") from exc
    try:
        manifest = json.loads(manifest_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Cannot parse {MANIFEST}: {exc}") from exc

    require(errors, blob_sha(method) == EXPECTED_METHOD_BLOB,
            "Neutral method blob differs from the frozen pre-trial baseline")
    require(errors, red_team.get("method_path") == str(METHOD),
            "Red-team record method_path mismatch")
    require(errors, red_team.get("method_version") == "v1.0-static-reviewed",
            "Red-team record method version mismatch")
    require(errors, red_team.get("frozen_source_commit") == FROZEN_SOURCE,
            "Red-team record frozen source mismatch")
    require(errors, red_team.get("transition_model") == EXPECTED_MODEL,
            "Red-team transition model differs from the method state model")
    for phrase in (
        "Each transition appends one entry with from, to, actor, timestamp, reason, evidence link, and baseline version.",
        "All three must PASS for acceptance.",
        "REOPENED cannot return directly to ACCEPTED.",
    ):
        require(errors, phrase in method, f"Method missing required control: {phrase}")

    cases = red_team.get("synthetic_cases")
    require(errors, isinstance(cases, list) and len(cases) == 3,
            "Red-team record must contain exactly three synthetic cases")
    for case in cases or []:
        case_id = case.get("id", "<missing>")
        current = "DEFINED"
        events = case.get("events", [])
        require(errors, bool(events), f"{case_id}: missing events")
        for index, event in enumerate(events):
            require(errors, event.get("from") == current,
                    f"{case_id} event {index}: route discontinuity")
            source = event.get("from")
            target = event.get("to")
            require(errors, target in EXPECTED_MODEL.get(source, []),
                    f"{case_id} event {index}: illegal transition {source!r} -> {target!r}")
            for field in ("actor", "timestamp_utc", "reason", "evidence", "baseline_version"):
                require(errors, bool(event.get(field)),
                        f"{case_id} event {index}: missing {field}")
            if source == "REVIEW" and target in {"ACCEPTED", "REJECTED"}:
                verdicts = event.get("review_verdicts", {})
                require(errors, set(verdicts) == {
                    "specification_fidelity", "quality_and_standards", "operational_readiness"
                }, f"{case_id} event {index}: review verdict axes incomplete")
            current = target
        require(errors, current == case.get("expected"),
                f"{case_id}: terminal state differs from expected")

    controls = red_team.get("negative_controls")
    require(errors, isinstance(controls, list) and len(controls) == 4,
            "Red-team record must contain exactly four negative controls")
    for control in controls or []:
        require(errors, control.get("observed") == "REJECT",
                f"{control.get('id', '<missing>')}: negative control did not reject")

    for phrase in (
        "Start every card at DEFINED.",
        "Keep the observer key hidden until all cards are finished.",
        "minimum retention",
        "A stopped trial, missing fixture, or refusal to retain minimum redacted evidence is INCONCLUSIVE.",
        "A reviewer distinct from every contributor must authorize reopening.",
        "REOPENED → DEFINED",
    ):
        require(errors, phrase in trial, f"Trial plan missing required control: {phrase}")
    require(errors, "P-07" in recheck, "Desk recheck does not record the complete-record correction")
    require(errors, "Participant Packet" in kit and "Observer Packet" in kit,
            "Trial kit must separate participant and observer materials")

    require(errors, manifest.get("artifact") == "PRE_TRIAL_PACKAGE_MANIFEST",
            "Pre-trial manifest artifact name mismatch")
    require(errors, manifest.get("frozen_source_commit") == FROZEN_SOURCE,
            "Pre-trial manifest frozen source mismatch")
    require(errors, manifest.get("method_blob") == EXPECTED_METHOD_BLOB,
            "Pre-trial manifest method blob mismatch")
    require(errors, manifest.get("human_trial_status") == "NOT_YET_RUN",
            "Pre-trial manifest must not claim a human trial")
    require(errors, manifest.get("live_project_changes") is False,
            "Pre-trial manifest must state that no live project changed")
    for path, expected in manifest.get("package_blobs", {}).items():
        actual_path = pathlib.Path(path)
        require(errors, actual_path.exists(), f"Manifest package file missing: {path}")
        if actual_path.exists():
            require(errors, blob_sha(read(actual_path)) == expected,
                    f"Manifest package blob mismatch: {path}")

    result = {
        "artifact": "PRE_TRIAL_PACKAGE_VALIDATION",
        "method_blob": blob_sha(method),
        "synthetic_case_count": len(cases or []),
        "synthetic_transition_count": sum(len(case.get("events", [])) for case in cases or []),
        "negative_control_count": len(controls or []),
        "hard_errors": errors,
        "human_trial_claimed": False,
        "live_project_changes": False,
    }
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

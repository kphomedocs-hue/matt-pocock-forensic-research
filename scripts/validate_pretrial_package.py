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

from pretrial_semantics import MODEL, execute_controls, validate_trace

METHOD = pathlib.Path("11_NEUTRAL_OPERATING_METHOD.md")
RED_TEAM = pathlib.Path("12_NEUTRAL_METHOD_RED_TEAM.json")
TRIAL = pathlib.Path("13_PRE_APPLICATION_TRIAL_AND_PILOT_GATE.md")
RECHECK = pathlib.Path("14_PRE_TRIAL_DESK_RECHECK.md")
KIT = pathlib.Path("16_HUMAN_TRIAL_KIT.md")
MANIFEST = pathlib.Path("15_PRE_TRIAL_PACKAGE_MANIFEST.json")
EXPECTED_METHOD_BLOB = "4f3dc9653e5a86456c079dc4a1faf5687aa41271"
FROZEN_SOURCE = "3cca18b368ae95cdbdebbff572ccafa662551015"

EXPECTED_MODEL = MODEL
REQUIRED_PACKAGE_FILES = {
    "10_RESEARCH_FINDINGS_ARCHITECTURE.md", str(METHOD), str(RED_TEAM),
    str(TRIAL), str(RECHECK), str(KIT), "scripts/validate_pretrial_package.py",
    "scripts/pretrial_semantics.py", "tests/test_pretrial_package.py",
}



def read(path: pathlib.Path) -> str:
    if not path.exists():
        raise SystemExit(f"Missing required pre-trial package file: {path}")
    return path.read_text(encoding="utf-8")


def blob_sha(content: str | bytes) -> str:
    data = content.encode("utf-8") if isinstance(content, str) else content
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def require(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate_manifest_files(manifest: dict, root: pathlib.Path) -> list[str]:
    if not isinstance(manifest, dict):
        return ["MANIFEST_SCHEMA"]
    errors = []
    require(errors, manifest.get("schema_version") == 2, "MANIFEST_SCHEMA")
    require(errors, manifest.get("method_version") == "v1.0-static-reviewed", "MANIFEST_METHOD_VERSION")
    entries = manifest.get("package_blobs")
    if not isinstance(entries, dict):
        return errors + ["MANIFEST_ENTRIES"]
    require(errors, set(entries) == REQUIRED_PACKAGE_FILES, "MANIFEST_REQUIRED_FILES")
    root = root.resolve()
    for path, expected in entries.items():
        # Exact allowlist prevents absolute paths, traversal, and unexpected input reads.
        if path not in REQUIRED_PACKAGE_FILES:
            errors.append(f"MANIFEST_PATH:{path}")
            continue
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{40}", expected):
            errors.append(f"MANIFEST_HASH:{path}")
            continue
        candidate = root / path
        if any(part.is_symlink() for part in (candidate, *candidate.parents)) or not candidate.resolve().is_relative_to(root):
            errors.append(f"MANIFEST_SYMLINK:{path}")
            continue
        try:
            actual = blob_sha(candidate.read_bytes())
        except OSError:
            errors.append(f"MANIFEST_MISSING:{path}")
            continue
        require(errors, actual == expected, f"MANIFEST_MISMATCH:{path}")
    return errors


def main() -> None:
    errors: list[str] = []
    if MANIFEST.is_symlink():
        raise SystemExit("Manifest must not be a symlink")
    try:
        manifest = json.loads(read(MANIFEST))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Cannot parse {MANIFEST}: {exc}") from exc
    errors.extend(validate_manifest_files(manifest, pathlib.Path.cwd()))
    if errors:
        print(json.dumps({"artifact": "PRE_TRIAL_PACKAGE_VALIDATION", "hard_errors": errors,
                          "evidence_class": "SYNTHETIC_TRACE_CHECK_ONLY",
                          "human_evidence_validated": False, "human_trial_claimed": False,
                          "live_project_changes": False}, indent=2))
        raise SystemExit(1)
    method = read(METHOD)
    trial = read(TRIAL)
    recheck = read(RECHECK)
    kit = read(KIT)

    try:
        red_team = json.loads(read(RED_TEAM))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Cannot parse {RED_TEAM}: {exc}") from exc
    if not isinstance(red_team, dict):
        raise SystemExit("Pre-trial JSON roots must be objects")

    require(errors, blob_sha(METHOD.read_bytes()) == EXPECTED_METHOD_BLOB,
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
    if not isinstance(cases, list):
        cases = []
    require(errors, all(isinstance(case, dict) for case in cases),
            "Synthetic cases must be objects")
    case_ids = [case.get("id") for case in cases if isinstance(case, dict)]
    require(errors, len(case_ids) == 3 and all(isinstance(cid, str) for cid in case_ids)
            and sorted(cid for cid in case_ids if isinstance(cid, str)) == ["C-01", "C-02", "C-03"],
            "Synthetic case IDs must be C-01, C-02 and C-03 without duplicates")
    for case in cases:
        errors.extend(validate_trace(case, owner="Owner-A"))
    executed_controls, control_errors = execute_controls(red_team)
    errors.extend(control_errors)

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

    result = {
        "artifact": "PRE_TRIAL_PACKAGE_VALIDATION",
        "method_blob": blob_sha(METHOD.read_bytes()),
        "synthetic_case_count": len(cases or []),
        "synthetic_transition_count": sum(len(case["events"]) for case in cases
                                          if isinstance(case, dict) and isinstance(case.get("events"), list)),
        "executed_negative_control_count": len(executed_controls),
        "executed_negative_controls": executed_controls,
        "evidence_class": "SYNTHETIC_TRACE_CHECK_ONLY",
        "human_evidence_validated": False,
        "hard_errors": errors,
        "human_trial_claimed": False,
        "live_project_changes": False,
    }
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

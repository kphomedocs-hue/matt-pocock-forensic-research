#!/usr/bin/env python3
"""Fail-closed checks for Phase 4 runtime provenance and contradiction status."""
from __future__ import annotations

import json
import pathlib
import re

FROZEN = "3cca18b368ae95cdbdebbff572ccafa662551015"
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
REGISTER = pathlib.Path("04_CONTRADICTION_REGISTER.md")


def load(path: pathlib.Path):
    if not path.exists():
        raise SystemExit(f"Missing required evidence file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_named_tests(bid: str, evidence: dict, data: dict, result_file: str, errors: list[str]) -> None:
    test_ids = set(evidence.get("test_ids", []))
    if not test_ids:
        errors.append(f"{bid}: {result_file} evidence missing test_ids")
        return
    tests = {t.get("test_id"): t for t in data.get("tests", [])}
    for test_id in sorted(test_ids):
        test = tests.get(test_id)
        if not test:
            errors.append(f"{bid}: test id {test_id} not found in {result_file}")
            continue
        if test.get("passed") is not True:
            errors.append(f"{bid}: test id {test_id} is not passing in {result_file}")
        behavior_ids = set(test.get("behavior_ids", []))
        if bid not in behavior_ids:
            errors.append(f"{bid}: test id {test_id} does not bind this behavior in {result_file}")


def validate_isolated_named_result(bid: str, evidence: dict, data: dict, result_file: str, errors: list[str]) -> None:
    if data.get("hard_errors") not in ([], None):
        errors.append(f"{bid}: {result_file} contains hard errors")
    if data.get("synthetic_inputs_only") is not True or data.get("user_or_live_repo_touched") is not False:
        errors.append(f"{bid}: {result_file} isolation flags are not safe")
    validate_named_tests(bid, evidence, data, result_file, errors)


def validate_result_file(bid: str, evidence: dict, errors: list[str]) -> None:
    result_file = evidence.get("result_file")
    if not result_file:
        errors.append(f"{bid}: runtime evidence missing result_file")
        return
    path = pathlib.Path(result_file)
    if not path.exists():
        errors.append(f"{bid}: runtime evidence result file does not exist: {result_file}")
        return
    try:
        data = load(path)
    except Exception as exc:
        errors.append(f"{bid}: cannot parse {result_file}: {exc}")
        return
    if data.get("frozen_commit") != FROZEN:
        errors.append(f"{bid}: {result_file} frozen_commit mismatch")
    if result_file == "04_RUNTIME_EXECUTION_EVIDENCE.json":
        matches = [t for t in data.get("tests", []) if t.get("behavior_id") == bid]
        if not matches or not all(t.get("passed") is True for t in matches):
            errors.append(f"{bid}: no passing deterministic local-runtime record in {result_file}")
    elif result_file == "04_CT019_REPRODUCTION.json":
        if data.get("behavior_id") != bid or data.get("hard_errors") not in ([], None):
            errors.append(f"{bid}: CT-019 reproduction record does not close cleanly")
    elif result_file == "04_RUNTIME_SMOKE_RESULTS.json":
        test_ids = set(evidence.get("test_ids", []))
        if not test_ids:
            errors.append(f"{bid}: smoke evidence missing test_ids")
        serialized = json.dumps(data, sort_keys=True)
        for test_id in test_ids:
            if test_id not in serialized:
                errors.append(f"{bid}: smoke test id {test_id} not found in {result_file}")
    elif result_file == "04_DEEP_MODULE_RUNTIME_RESULTS.json":
        validate_isolated_named_result(bid, evidence, data, result_file, errors)
    elif result_file == "04_PRECOMMIT_RUNTIME_RESULTS.json":
        validate_isolated_named_result(bid, evidence, data, result_file, errors)
        versions = data.get("package_versions", {})
        if set(versions) != {"husky", "lint-staged", "prettier"} or any(not versions.get(x) for x in versions):
            errors.append(f"{bid}: pre-commit evidence lacks resolved Husky/lint-staged/Prettier versions")
    elif result_file == "04_ARCHITECTURE_REPORT_RUNTIME_RESULTS.json":
        validate_isolated_named_result(bid, evidence, data, result_file, errors)
    elif result_file == "04_IMPLEMENT_REVIEW_VISIBILITY_RESULTS.json":
        validate_isolated_named_result(bid, evidence, data, result_file, errors)


def main() -> None:
    matrix = load(MATRIX)
    register_text = REGISTER.read_text(encoding="utf-8")
    errors: list[str] = []

    if matrix.get("frozen_commit") != FROZEN:
        errors.append("behavior matrix frozen_commit mismatch")

    status_header = re.search(r"Statuses: `([^`]+)`\.", register_text)
    if not status_header:
        errors.append("contradiction register status vocabulary header missing")
        allowed_statuses = set()
    else:
        allowed_statuses = {x.strip() for x in status_header.group(1).split("/")}

    for line in register_text.splitlines():
        if not re.match(r"^\| CT-\d{3} \|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            errors.append(f"Malformed contradiction row: {cells[0] if cells else '<unknown>'}")
            continue
        ct_id, status = cells[0], cells[5]
        if status not in allowed_statuses:
            errors.append(f"{ct_id}: status {status!r} outside declared vocabulary {sorted(allowed_statuses)}")

    observed = [r for r in matrix.get("rows", []) if r.get("runtime_observed") is True]
    for row in observed:
        bid = row.get("behavior_id", "<missing>")
        evidence_list = row.get("runtime_evidence")
        if not isinstance(evidence_list, list) or not evidence_list:
            errors.append(f"{bid}: runtime_observed=true without runtime_evidence")
            continue
        for ev in evidence_list:
            if ev.get("frozen_commit") != FROZEN:
                errors.append(f"{bid}: runtime evidence frozen_commit mismatch")
            if not isinstance(ev.get("workflow_run_id"), int) or ev.get("workflow_run_id") <= 0:
                errors.append(f"{bid}: runtime evidence requires positive integer workflow_run_id")
            validate_result_file(bid, ev, errors)

    integrity = load(pathlib.Path("04_BEHAVIOR_INTEGRITY.json"))
    queue = load(pathlib.Path("04_RUNTIME_OBSERVATION_QUEUE.json"))
    if integrity.get("runtime_observed_count") != len(observed):
        errors.append("behavior integrity runtime-observed count disagrees with matrix")
    if queue.get("runtime_observed") != len(observed):
        errors.append("runtime queue observed count disagrees with matrix")

    if errors:
        raise SystemExit("Phase 4 runtime provenance validation failed:\n- " + "\n- ".join(errors))
    print(f"Phase 4 runtime provenance GREEN: observed={len(observed)}, all observed rows have durable evidence")


if __name__ == "__main__":
    main()

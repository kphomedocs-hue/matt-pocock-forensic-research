#!/usr/bin/env python3
"""One-shot repair for Phase 4 issues found during the 2026-09 recheck.

Scope is deliberately narrow:
1. Normalize CT-004 status/wording without changing its substantive open scope.
2. Add durable runtime provenance to the four local-runtime observations.
3. Add a fail-closed runtime-provenance validator.
4. Wire provenance validation into all Phase 4 validation/runtime workflows.
5. Add a main-branch detection guard (CI guard; repository branch protection remains
   a GitHub repository setting outside this script).

The script is idempotent and exits non-zero if an expected anchor is missing.
"""
from __future__ import annotations

import json
from pathlib import Path

FROZEN = "3cca18b368ae95cdbdebbff572ccafa662551015"
LOCAL_RUN_ID = 34752990655


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count == 0:
        if new in text:
            return text
        raise SystemExit(f"Missing repair anchor for {label}")
    if count != 1:
        raise SystemExit(f"Expected one repair anchor for {label}, found {count}")
    return text.replace(old, new, 1)


def repair_contradictions() -> None:
    p = Path("04_CONTRADICTION_REGISTER.md")
    text = p.read_text(encoding="utf-8")
    old = (
        "| CT-004 | package lock version | Frozen package.json MP-0056 is version 1.2.3. | "
        "Frozen package-lock.json MP-0055 retains root version 0.0.0 in both top-level and root-package metadata. | "
        "METADATA DRIFT | PARTIALLY RESOLVED | History shows lockfile was never regenerated after bootstrap; runtime effect still UNKNOWN. Version sync MP-0059 does not touch package-lock. |"
    )
    new = (
        "| CT-004 | package lock version | Frozen package.json MP-0056 is version 1.2.3. | "
        "Frozen package-lock.json MP-0055 retains root version 0.0.0 in both top-level and root-package metadata. | "
        "METADATA DRIFT | OPEN | History shows lockfile was never regenerated after bootstrap. Direct local npm observation now shows npm pack uses package.json version 1.2.3 and package-lock-only normalization rewrites both root lock version fields to 1.2.3; live release/CI consumer behavior remains open under B-029. Version sync MP-0059 does not touch package-lock. |"
    )
    text = replace_once(text, old, new, "CT-004 row")
    p.write_text(text, encoding="utf-8")


def runtime_evidence(checks: list[str]) -> list[dict]:
    return [{
        "evidence_type": "DETERMINISTIC_LOCAL_RUNTIME",
        "test_ids": checks,
        "frozen_commit": FROZEN,
        "workflow_run_id": LOCAL_RUN_ID,
        "result_file": "04_RUNTIME_EXECUTION_EVIDENCE.json",
    }]


def repair_matrix() -> None:
    p = Path("04_BEHAVIOR_MATRIX.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    rows = {r["behavior_id"]: r for r in data["rows"]}
    expected = {
        "B-004": [
            "frozen_fixture_contains_expected_version_drift",
            "npm_pack_uses_package_json_version",
            "offline_lockfile_normalization_succeeds",
            "npm_normalizes_root_lock_versions_to_package_json",
        ],
        "B-015": [
            "bash_n",
            "first_run_writes_dummy_values_without_echoing_secret",
            "rerun_preserves_existing_values_idempotently",
        ],
        "B-018": [
            "in_sync_check_passes",
            "drift_check_fails",
            "repair_restores_package_version",
            "script_operates_without_package_lock_present",
        ],
        "B-056": [
            "bash_n",
            "benign_flow_completes",
            "captured_values_are_printed_for_agent",
        ],
    }
    for bid, checks in expected.items():
        row = rows.get(bid)
        if not row:
            raise SystemExit(f"Missing behavior row {bid}")
        if row.get("runtime_observed") is not True:
            raise SystemExit(f"Refusing provenance promotion: {bid} is not runtime_observed=true")
        existing = row.get("runtime_evidence", [])
        wanted = runtime_evidence(checks)[0]
        if not any(
            e.get("result_file") == wanted["result_file"]
            and e.get("workflow_run_id") == wanted["workflow_run_id"]
            for e in existing
        ):
            existing.append(wanted)
            row["runtime_evidence"] = existing
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def ensure_provenance_validator() -> None:
    p = Path("scripts/validate_phase4_runtime_provenance.py")
    content = r'''#!/usr/bin/env python3
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

    rows = re.findall(r"^\| (CT-\d{3}) \|.*?\| ([A-Z][A-Z ]*(?:DESIGN)?) \| ([A-Z][A-Z ]*(?:DESIGN)?) \|.*?\|$", register_text, re.MULTILINE)
    # Regex above is intentionally conservative; independently parse current CT table rows
    # so status checks do not silently disappear when classification wording contains punctuation.
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

    if len(observed) != 8:
        errors.append(f"expected current runtime-observed denominator 8, found {len(observed)}")

    if errors:
        raise SystemExit("Phase 4 runtime provenance validation failed:\n- " + "\n- ".join(errors))
    print(f"Phase 4 runtime provenance GREEN: observed={len(observed)}, all observed rows have durable evidence")


if __name__ == "__main__":
    main()
'''
    p.write_text(content, encoding="utf-8")


def patch_workflow(path: str, trigger_anchor: str | None = None) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if trigger_anchor and "scripts/validate_phase4_runtime_provenance.py" not in text:
        text = replace_once(
            text,
            trigger_anchor,
            trigger_anchor + "\n      - 'scripts/validate_phase4_runtime_provenance.py'\n      - '04_RUNTIME_EXECUTION_EVIDENCE.json'\n      - '04_RUNTIME_SMOKE_RESULTS.json'\n      - '04_CT019_REPRODUCTION.json'",
            f"{path} provenance triggers",
        )
    if "Validate Phase 4 runtime provenance" not in text:
        anchor = "      - name: Build Phase 4 behavior coverage\n        run: python scripts/build_phase4_coverage.py"
        if anchor in text:
            text = replace_once(
                text,
                anchor,
                "      - name: Validate Phase 4 runtime provenance\n        run: python scripts/validate_phase4_runtime_provenance.py\n" + anchor,
                f"{path} provenance step",
            )
        else:
            anchor = "      - name: Validate behavior matrix\n        run: python scripts/validate_behavior_matrix.py"
            if anchor in text:
                text = replace_once(
                    text,
                    anchor,
                    anchor + "\n      - name: Validate Phase 4 runtime provenance\n        run: python scripts/validate_phase4_runtime_provenance.py",
                    f"{path} provenance step",
                )
            else:
                anchor = "          python scripts/validate_behavior_matrix.py"
                text = replace_once(
                    text,
                    anchor,
                    anchor + "\n          python scripts/validate_phase4_runtime_provenance.py",
                    f"{path} provenance step",
                )
    p.write_text(text, encoding="utf-8")


def ensure_main_guard() -> None:
    p = Path(".github/workflows/phase4-main-guard.yml")
    p.write_text('''name: Phase 4 main guard\n\non:\n  push:\n    branches: [main]\n  workflow_dispatch:\n\npermissions:\n  contents: read\n\nconcurrency:\n  group: forensic-phase4-main-guard\n  cancel-in-progress: false\n\njobs:\n  validate:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v7.0.1\n        with:\n          fetch-depth: 0\n      - uses: actions/setup-python@v7.0.0\n        with:\n          python-version: '3.12'\n      - name: Validate Phase 4 matrix\n        run: python scripts/validate_behavior_matrix.py\n      - name: Validate Phase 4 breadth\n        run: python scripts/build_phase4_coverage.py\n      - name: Validate Phase 4 evidence queue\n        run: python scripts/build_phase4_runtime_queue.py\n      - name: Validate Phase 4 runtime provenance\n        run: python scripts/validate_phase4_runtime_provenance.py\n      - name: Ensure validators are non-mutating on committed main\n        run: |\n          if [[ -n "$(git status --porcelain -- 04_BEHAVIOR_MATRIX.md 04_BEHAVIOR_INTEGRITY.json 04_BEHAVIOR_COVERAGE.json 04_BEHAVIOR_COVERAGE.md 04_RUNTIME_OBSERVATION_QUEUE.json 04_RUNTIME_OBSERVATION_QUEUE.md)" ]]; then\n            echo "Committed Phase 4 generated state is stale" >&2\n            git status --short\n            exit 1\n          fi\n          echo "Phase 4 main guard GREEN"\n''', encoding="utf-8")


def main() -> None:
    repair_contradictions()
    repair_matrix()
    ensure_provenance_validator()
    patch_workflow(
        ".github/workflows/validate-phase4-behavior.yml",
        "      - 'scripts/build_phase4_runtime_queue.py'",
    )
    patch_workflow(".github/workflows/phase4-local-runtime-checks.yml")
    patch_workflow(".github/workflows/phase4-runtime-smoke.yml")
    ensure_main_guard()
    print("Phase 4 recheck repair applied")


if __name__ == "__main__":
    main()

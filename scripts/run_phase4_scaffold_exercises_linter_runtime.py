#!/usr/bin/env python3
"""Observe B-047 against the pinned external ai-hero-cli linter in disposable fixtures."""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import tempfile
from typing import Any

FROZEN = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXTERNAL_LINTER_COMMIT = "5071b7d2d0e0514e134dadd26d9bed23c7c54365"
EXTERNAL_LINTER_VERSION = "0.2.8"
COURSE_COMMIT = "73969f1a1ec65b390f0532bb8ae6c693376fca9e"
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
OUT_JSON = pathlib.Path("04_SCAFFOLD_EXERCISES_LINTER_RESULTS.json")
OUT_MD = pathlib.Path("04_SCAFFOLD_EXERCISES_LINTER_RESULTS.md")
SKILL_REL = pathlib.Path("skills/misc/scaffold-exercises/SKILL.md")


def run(cmd: list[str], cwd: pathlib.Path, timeout: int = 180) -> dict[str, Any]:
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    return {"command": cmd, "returncode": p.returncode, "stdout": p.stdout[-6000:], "stderr": p.stderr[-6000:]}


def concise(result: dict[str, Any]) -> dict[str, Any]:
    return {key: (result.get(key, "")[-3000:] if key in {"stdout", "stderr"} else result.get(key)) for key in ("command", "returncode", "stdout", "stderr")}


def output(result: dict[str, Any]) -> str:
    return result.get("stdout", "") + "\n" + result.get("stderr", "")


def record(test_id: str, title: str, assertions: list[str], evidence: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    return {"test_id": test_id, "behavior_ids": ["B-047"], "title": title, "assertions": assertions, "passed": not errors, "errors": errors, "evidence": evidence}


def write_fixture(root: pathlib.Path, primary: str) -> pathlib.Path:
    variant = root / "exercises" / "01-contracts" / f"01.01-{primary}-only" / primary
    variant.mkdir(parents=True)
    (variant / "readme.md").write_text(f"# {primary.title()} only fixture\n\nSynthetic runtime fixture.\n", encoding="utf-8")
    return root


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--linter-source", required=True)
    parser.add_argument("--course-source", required=True)
    args = parser.parse_args()
    source = pathlib.Path(args.source).resolve()
    linter_source = pathlib.Path(args.linter_source).resolve()
    course_source = pathlib.Path(args.course_source).resolve()
    try:
        run_id = int(os.environ.get("GITHUB_RUN_ID", "0"))
    except ValueError as exc:
        raise SystemExit("GITHUB_RUN_ID must be an integer") from exc
    if run_id <= 0:
        raise SystemExit("GITHUB_RUN_ID must be positive")

    source_head = run(["git", "rev-parse", "HEAD"], source)["stdout"].strip()
    linter_head = run(["git", "rev-parse", "HEAD"], linter_source)["stdout"].strip()
    course_head = run(["git", "rev-parse", "HEAD"], course_source)["stdout"].strip()
    if source_head != FROZEN:
        raise SystemExit(f"Frozen source checkout mismatch: {source_head!r}")
    if linter_head != EXTERNAL_LINTER_COMMIT:
        raise SystemExit(f"External linter checkout mismatch: {linter_head!r}")
    if course_head != COURSE_COMMIT:
        raise SystemExit(f"Course lockfile checkout mismatch: {course_head!r}")

    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows = {row["behavior_id"]: row for row in matrix.get("rows", [])}
    if matrix.get("frozen_commit") != FROZEN or "B-047" not in rows:
        raise SystemExit("Research matrix provenance mismatch")

    skill = (source / SKILL_REL).read_text(encoding="utf-8")
    lint_source = (linter_source / "src/internal/lint.ts").read_text(encoding="utf-8")
    dist_package = json.loads((linter_source / "dist/package.json").read_text(encoding="utf-8"))
    course_package = json.loads((course_source / "package.json").read_text(encoding="utf-8"))
    course_lock = (course_source / "pnpm-lock.yaml").read_text(encoding="utf-8")
    tick = chr(96)
    contract_errors: list[str] = []
    required_skill = [
        "Create exercise directory structures that pass " + tick + "pnpm ai-hero-cli internal lint" + tick,
        "- " + tick + "problem/" + tick + " - student workspace with TODOs",
        "- " + tick + "solution/" + tick + " - reference implementation",
        "- " + tick + "explainer/" + tick + " - conceptual material, no TODOs",
        "At least one of " + tick + "problem/" + tick + ", " + tick + "explainer/" + tick + ", or " + tick + "explainer.1/" + tick + " exists",
    ]
    for phrase in required_skill:
        if phrase not in skill:
            contract_errors.append(f"Frozen scaffold-exercises contract missing: {phrase!r}")
    for phrase in ('folder === "problem"', 'folder === "explainer"', 'folder === "explainer.1"', "No problem, explainer, or explainer.1 folder found in the exercise."):
        if phrase not in lint_source:
            contract_errors.append(f"External linter rule missing: {phrase!r}")
    if dist_package.get("version") != EXTERNAL_LINTER_VERSION:
        contract_errors.append(f"Built external linter package version {dist_package.get('version')!r} is not {EXTERNAL_LINTER_VERSION!r}")
    if dist_package.get("bin") != "bin.cjs":
        contract_errors.append("Built package no longer exposes the package-name bin entrypoint")
    if course_package.get("devDependencies", {}).get("ai-hero-cli") != "^0.2.8":
        contract_errors.append("Public course package no longer declares the observed ai-hero-cli range")
    if "ai-hero-cli@0.2.8:" not in course_lock:
        contract_errors.append("Public course lockfile does not resolve ai-hero-cli@0.2.8")
    contract = record(
        "SE-001",
        "frozen scaffold contract and pinned external linter provenance",
        [
            "frozen skill permits a solution-only exercise in its variant rule",
            "the same frozen skill mandates the ai-hero-cli linter and describes a primary set excluding solution",
            "the tagged external linter implements that primary-set rejection",
            "the public course lock resolves ai-hero-cli@0.2.8, and the built package reports that exact version",
        ],
        {
            "frozen_skill_blob": run(["git", "rev-parse", f"HEAD:{SKILL_REL.as_posix()}"], source)["stdout"].strip(),
            "external_linter_commit": linter_head,
            "external_linter_dist_package": {"version": dist_package.get("version"), "bin": dist_package.get("bin")},
            "public_course_lock": {
                "repo": "ai-hero-dev/cohort-002-skill-building",
                "commit": course_head,
                "declared_range": course_package.get("devDependencies", {}).get("ai-hero-cli"),
                "contains_exact_lock_entry": "ai-hero-cli@0.2.8:" in course_lock,
            },
        },
        contract_errors,
    )

    entrypoint = linter_source / "dist/bin.cjs"
    if not entrypoint.exists():
        raise SystemExit(f"Built linter entrypoint is missing: {entrypoint}")
    with tempfile.TemporaryDirectory(prefix="phase4-scaffold-exercises-") as td:
        root = pathlib.Path(td)
        solution_root = write_fixture(root / "solution-only", "solution")
        solution_run = run(["node", str(entrypoint), "internal", "lint", "--root", str(solution_root / "exercises"), "--cwd", str(solution_root)], root)
        solution_errors: list[str] = []
        if solution_run["returncode"] == 0:
            solution_errors.append("solution-only fixture unexpectedly passed the mandatory linter")
        if "No problem, explainer, or explainer.1 folder found in the exercise." not in output(solution_run):
            solution_errors.append("solution-only rejection did not name the primary-variant rule")
        solution = record(
            "SE-002",
            "solution-only scaffold is rejected by the actual external linter",
            [
                "fixture contains exactly one solution/readme.md variant with real content",
                "no problem, explainer, or explainer.1 directory exists",
                "the tagged external linter exits non-zero and names the missing primary-variant rule",
            ],
            {"fixture": "solution-only", "linter_run": concise(solution_run)},
            solution_errors,
        )

        control_root = write_fixture(root / "explainer-only", "explainer")
        control_run = run(["node", str(entrypoint), "internal", "lint", "--root", str(control_root / "exercises"), "--cwd", str(control_root)], root)
        control_errors: list[str] = []
        if control_run["returncode"] != 0:
            control_errors.append(f"explainer-only control did not pass the external linter (exit {control_run['returncode']})")
        control = record(
            "SE-003",
            "explainer-only control remains accepted",
            [
                "fixture contains exactly one explainer/readme.md variant with real content",
                "the same tagged external linter accepts that primary variant",
            ],
            {"fixture": "explainer-only", "linter_run": concise(control_run)},
            control_errors,
        )

    tests = [contract, solution, control]
    hard_errors = [f"{test['test_id']}: {error}" for test in tests for error in test["errors"]]
    result = {
        "schema_version": 1,
        "source_repo": "mattpocock/skills",
        "frozen_commit": FROZEN,
        "source_checkout_head": source_head,
        "workflow_run_id": run_id,
        "synthetic_inputs_only": True,
        "user_or_live_repo_touched": False,
        "external_linter": {"repo": "mattpocock/ai-hero-cli", "commit": linter_head, "tag": "v0.2.8", "package_version": dist_package.get("version"), "entrypoint": "dist/bin.cjs"},
        "external_course_lock": {"repo": "ai-hero-dev/cohort-002-skill-building", "commit": course_head, "declared_range": course_package.get("devDependencies", {}).get("ai-hero-cli"), "exact_lock_entry": "ai-hero-cli@0.2.8:"},
        "tool_versions": {
            "git": run(["git", "--version"], source)["stdout"].strip(),
            "python": run(["python", "--version"], source)["stdout"].strip(),
            "node": run(["node", "--version"], source)["stdout"].strip(),
            "npm": run(["npm", "--version"], source)["stdout"].strip(),
            "pnpm": run(["pnpm", "--version"], source)["stdout"].strip(),
        },
        "test_count": len(tests),
        "pass_count": sum(test["passed"] for test in tests),
        "fail_count": sum(not test["passed"] for test in tests),
        "tests": tests,
        "hard_errors": hard_errors,
        "runtime_closure_behavior_ids": ["B-047"] if not hard_errors else [],
    }
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Phase 4 Scaffold-Exercises Linter Runtime Evidence",
        "",
        "Frozen source: mattpocock/skills @ " + FROZEN + ".",
        "",
        "Workflow run: " + str(run_id) + ".",
        "",
        "External linter: mattpocock/ai-hero-cli @ " + linter_head + " (v0.2.8).",
        "",
        "All exercised inputs were synthetic disposable fixtures. The frozen source, public course lockfile checkout, and external linter checkout were read only.",
        "",
    ]
    for test in tests:
        lines.extend([f"## {test['test_id']} - {test['title']}", "", "Status: " + ("PASS" if test["passed"] else "FAIL") + ".", ""])
        lines.extend(f"- {assertion}" for assertion in test["assertions"])
        if test["errors"]:
            lines.extend(["", "Errors:"])
            lines.extend(f"- {error}" for error in test["errors"])
        lines.append("")
    lines.extend([
        "## Adjudication",
        "",
        "The frozen skill allows solution-only. The tagged linter selected by the public course lock rejects that same shape while accepting an explainer-only control. This confirms CT-020 operationally and does not promote any source file to VERIFIED.",
        "",
        "Hard errors: " + str(len(hard_errors)) + ".",
        "",
    ])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    if hard_errors:
        raise SystemExit("Scaffold-exercises linter runtime failed:\n- " + "\n- ".join(hard_errors))

    row = rows["B-047"]
    row["runtime_observed"] = True
    row["adjudication"] = (
        "Frozen scaffold-exercises permits a solution-only exercise, but isolated execution of the exact external ai-hero-cli v0.2.8 linter selected by the public course lock rejects a solution-only readme fixture with the stated missing-primary-variant error. An explainer-only control passes. The prompt/linter mismatch is operational; CT-020 remains open."
    )
    row["next_evidence"] = (
        "Frozen behavior is runtime-observed. Source-side correction must make the allowed-variant prose and mandatory linter acceptance set identical, then rerun solution-only and explainer-only fixtures."
    )
    runtime_evidence = {
        "evidence_type": "EXTERNAL_LINTER_SYNTHETIC_RUNTIME",
        "test_ids": ["SE-001", "SE-002", "SE-003"],
        "frozen_commit": FROZEN,
        "workflow_run_id": run_id,
        "result_file": str(OUT_JSON),
    }
    row["runtime_evidence"] = [evidence for evidence in row.get("runtime_evidence", []) if evidence.get("result_file") != str(OUT_JSON)] + [runtime_evidence]
    MATRIX.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    print("Scaffold-exercises linter runtime GREEN: B-047")


if __name__ == "__main__":
    main()

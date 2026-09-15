#!/usr/bin/env python3
"""Reproduce B-010's pre-commit code-review visibility boundary in a disposable git repo."""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import tempfile
from typing import Any

FROZEN = "3cca18b368ae95cdbdebbff572ccafa662551015"
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
OUT = pathlib.Path("04_IMPLEMENT_REVIEW_VISIBILITY_RESULTS.json")
IMPLEMENT = pathlib.Path("skills/engineering/implement/SKILL.md")
REVIEW = pathlib.Path("skills/engineering/code-review/SKILL.md")


def run(cmd: list[str], cwd: pathlib.Path) -> dict[str, Any]:
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    return {"command": cmd, "returncode": p.returncode, "stdout": p.stdout[-4000:], "stderr": p.stderr[-4000:]}


def record(test_id: str, title: str, assertions: list[str], evidence: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    return {"test_id": test_id, "behavior_ids": ["B-010"], "title": title, "assertions": assertions, "passed": not errors, "errors": errors, "evidence": evidence}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    args = parser.parse_args()
    source = pathlib.Path(args.source).resolve()
    try:
        run_id = int(os.environ.get("GITHUB_RUN_ID", "0"))
    except ValueError as exc:
        raise SystemExit("GITHUB_RUN_ID must be an integer") from exc
    if run_id <= 0:
        raise SystemExit("GITHUB_RUN_ID must be positive")
    source_head = run(["git", "rev-parse", "HEAD"], source)["stdout"].strip()
    if source_head != FROZEN:
        raise SystemExit(f"Frozen source checkout mismatch: {source_head!r}")
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows = {row["behavior_id"]: row for row in matrix["rows"]}
    if matrix.get("frozen_commit") != FROZEN or "B-010" not in rows:
        raise SystemExit("Research matrix provenance mismatch")

    implement = (source / IMPLEMENT).read_text(encoding="utf-8")
    review = (source / REVIEW).read_text(encoding="utf-8")
    errors: list[str] = []
    if implement.find("Once done, use /code-review") > implement.find("Commit your work"):
        errors.append("frozen implement ordering is not review-before-commit")
    if "git diff <fixed-point>...HEAD" not in review or "diff is non-empty" not in review:
        errors.append("frozen code-review precondition changed")
    contract = record(
        "IR-001", "frozen cross-skill ordering and diff precondition",
        ["implement requires code-review before commit", "code-review requires a non-empty fixed-point...HEAD diff before review"],
        {"implement_blob": run(["git", "rev-parse", f"HEAD:{IMPLEMENT.as_posix()}"], source)["stdout"].strip(), "review_blob": run(["git", "rev-parse", f"HEAD:{REVIEW.as_posix()}"], source)["stdout"].strip()},
        errors,
    )

    with tempfile.TemporaryDirectory(prefix="phase4-implement-review-") as td:
        root = pathlib.Path(td)
        for cmd in (["git", "init"], ["git", "config", "user.name", "phase4"], ["git", "config", "user.email", "phase4@example.invalid"]):
            result = run(list(cmd), root)
            if result["returncode"] != 0:
                raise SystemExit(f"fixture setup failed: {result}")
        (root / "feature.txt").write_text("base\n", encoding="utf-8")
        if run(["git", "add", "feature.txt"], root)["returncode"] != 0 or run(["git", "commit", "-m", "base"], root)["returncode"] != 0:
            raise SystemExit("fixture base commit failed")
        base = run(["git", "rev-parse", "HEAD"], root)["stdout"].strip()
        (root / "feature.txt").write_text("implemented but not committed\n", encoding="utf-8")
        required_diff = run(["git", "diff", f"{base}...HEAD"], root)
        worktree_diff = run(["git", "diff"], root)
        if run(["git", "add", "feature.txt"], root)["returncode"] != 0 or run(["git", "commit", "-m", "implementation"], root)["returncode"] != 0:
            raise SystemExit("fixture implementation commit failed")
        post_commit_diff = run(["git", "diff", f"{base}...HEAD"], root)

    runtime_errors: list[str] = []
    if required_diff["returncode"] != 0 or required_diff["stdout"] != "":
        runtime_errors.append("fixed-point...HEAD was not empty before implementation commit")
    if worktree_diff["returncode"] != 0 or "implemented but not committed" not in worktree_diff["stdout"]:
        runtime_errors.append("working-tree implementation change was not visible to ordinary git diff")
    if post_commit_diff["returncode"] != 0 or "implemented but not committed" not in post_commit_diff["stdout"]:
        runtime_errors.append("fixed-point...HEAD did not become visible after commit")
    reproduction = record(
        "IR-002", "pre-commit fixed-point review visibility",
        ["required code-review diff is empty before commit despite a real working-tree change", "the same change is visible through fixed-point...HEAD only after a commit"],
        {"base_commit": base, "before_commit_required_diff": required_diff, "before_commit_worktree_diff": worktree_diff, "after_commit_required_diff": post_commit_diff},
        runtime_errors,
    )
    tests = [contract, reproduction]
    hard = [f"{t['test_id']}: {t['errors']}" for t in tests if not t["passed"]]
    output = {
        "frozen_commit": FROZEN, "source_checkout_head": source_head, "workflow_run_id": run_id,
        "synthetic_inputs_only": True, "user_or_live_repo_touched": False,
        "test_count": len(tests), "pass_count": sum(t["passed"] for t in tests), "fail_count": sum(not t["passed"] for t in tests),
        "tests": tests, "hard_errors": hard, "runtime_closure_behavior_ids": ["B-010"] if not hard else [],
        "tool_versions": {"git": run(["git", "--version"], source)["stdout"].strip(), "python": run(["python", "--version"], source)["stdout"].strip()},
    }
    OUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    if hard:
        raise SystemExit("Implement-review visibility runtime failed: " + "; ".join(hard))
    row = rows["B-010"]
    row["runtime_observed"] = True
    row["adjudication"] = "Direct synthetic git-runtime observation confirms the pre-commit gap: Implement orders code-review before commit, while code-review's fixed-point...HEAD precondition is empty until the implementation is committed. The working-tree change exists but is outside the mandated review diff."
    row["next_evidence"] = "Frozen behavior is runtime-observed. A source correction would require committing before review or teaching code-review an explicit working-tree review mode."
    evidence = {"evidence_type": "ISOLATED_GIT_RUNTIME", "test_ids": ["IR-001", "IR-002"], "frozen_commit": FROZEN, "workflow_run_id": run_id, "result_file": str(OUT)}
    row["runtime_evidence"] = [e for e in row.get("runtime_evidence", []) if e.get("result_file") != str(OUT)] + [evidence]
    MATRIX.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    print("Implement-review visibility runtime GREEN: B-010")


if __name__ == "__main__":
    main()

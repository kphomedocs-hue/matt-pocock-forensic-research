#!/usr/bin/env python3
"""Reproduce and adjudicate CT-019 against the exact frozen grep command.

CT-019 originally claimed the documented grep misses `as unknown as Type`.
This script tests that hypothesis with a minimal fixture and updates the durable
Phase 4 records only if the exact command demonstrably returns both the simple
and double-assertion lines.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import tempfile

FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
REGISTER = pathlib.Path("04_CONTRADICTION_REGISTER.md")
OUT_JSON = pathlib.Path("04_CT019_REPRODUCTION.json")
OUT_MD = pathlib.Path("04_CT019_REPRODUCTION.md")

# Match the stable contradiction IDs rather than a mutable historical row title.
# This keeps reruns idempotent after CT-019 has already been adjudicated.
PRIMARY_OLD_PREFIX = "| CT-019 |"
OVERLAY_OLD_PREFIX = "| ↳ CT-019 |"


def run(cmd: list[str], *, cwd: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)


def replace_table_row(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError(f"Expected exactly one row beginning {prefix!r}, found {len(matches)}")
    lines[matches[0]] = replacement
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    args = ap.parse_args()
    source = pathlib.Path(args.source).resolve()

    head = run(["git", "rev-parse", "HEAD"], cwd=source)
    if head.returncode != 0 or head.stdout.strip() != FROZEN_COMMIT:
        raise SystemExit(f"Frozen source mismatch: {head.stdout.strip()!r}")

    skill = source / "skills/misc/migrate-to-shoehorn/SKILL.md"
    skill_text = skill.read_text(encoding="utf-8")
    documented = 'grep -r " as [A-Z]" --include="*.test.ts" --include="*.spec.ts"'
    if documented not in skill_text:
        raise SystemExit("Exact documented grep command not found in frozen skill source")

    fixture_text = (
        "// SIMPLE_ASSERTION\n"
        "const simple = {} as Request;\n"
        "// DOUBLE_ASSERTION\n"
        "const doubled = {} as unknown as Request;\n"
        "// LOWERCASE_TARGET_CONTROL\n"
        "const lower = {} as request;\n"
    )
    with tempfile.TemporaryDirectory(prefix="ct019-repro-") as td:
        root = pathlib.Path(td)
        (root / "fixture.test.ts").write_text(fixture_text, encoding="utf-8")
        proc = run(
            ["grep", "-r", " as [A-Z]", "--include=*.test.ts", "--include=*.spec.ts"],
            cwd=root,
        )

    out = proc.stdout
    simple_found = "const simple = {} as Request;" in out
    double_found = "const doubled = {} as unknown as Request;" in out
    lowercase_control_found = "const lower = {} as request;" in out
    hard_errors: list[str] = []
    if proc.returncode != 0:
        hard_errors.append(f"grep exited {proc.returncode}")
    if not simple_found:
        hard_errors.append("simple `as Request` fixture was not found")
    if not double_found:
        hard_errors.append("double `as unknown as Request` fixture was not found")
    if lowercase_control_found:
        hard_errors.append("lowercase target control unexpectedly matched")

    result = {
        "schema_version": 1,
        "source_repo": "mattpocock/skills",
        "frozen_commit": FROZEN_COMMIT,
        "source_checkout_head": head.stdout.strip(),
        "workflow_run_id": str(os.environ.get("GITHUB_RUN_ID", "local")),
        "ct_id": "CT-019",
        "behavior_id": "B-046",
        "documented_command": documented,
        "fixture": fixture_text,
        "returncode": proc.returncode,
        "stdout": out,
        "stderr": proc.stderr,
        "simple_assertion_found": simple_found,
        "double_assertion_found": double_found,
        "lowercase_target_control_found": lowercase_control_found,
        "conclusion": "CT-019 original discovery-gap hypothesis is false: grep scans the whole line, and the second `as Request` substring in `as unknown as Request` satisfies ` as [A-Z]`." if not hard_errors else "Reproduction did not support safe adjudication.",
        "hard_errors": hard_errors,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    OUT_MD.write_text(
        "# CT-019 Exact Reproduction\n\n"
        f"Frozen source: `mattpocock/skills` @ `{FROZEN_COMMIT}`.\n\n"
        f"Workflow run: `{result['workflow_run_id']}`.\n\n"
        "The frozen skill documents `grep -r \" as [A-Z]\" --include=\"*.test.ts\" --include=\"*.spec.ts\"`. "
        "A minimal fixture containing both `as Request` and `as unknown as Request` was searched with the same grep pattern.\n\n"
        f"- simple assertion found: **{simple_found}**\n"
        f"- double assertion found: **{double_found}**\n"
        f"- lowercase target control found: **{lowercase_control_found}**\n"
        f"- grep exit: **{proc.returncode}**\n\n"
        "## Adjudication\n\n"
        "The original CT-019 reasoning was incorrect. Regex matching is not anchored to the first `as` token. "
        "In `as unknown as Request`, the later substring ` as Request` matches ` as [A-Z]`, so the documented discovery command does find the advertised double-assertion line. "
        "CT-019 is retained as a resolved audit false positive so the correction remains visible. This reproduction does not prove the later migration edits are always correct; it closes only the discovery claim that CT-019 challenged.\n\n"
        f"Hard errors: **{len(hard_errors)}**.\n",
        encoding="utf-8",
    )

    if hard_errors:
        raise SystemExit("CT-019 reproduction failed:\n- " + "\n- ".join(hard_errors))

    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows = {row["behavior_id"]: row for row in matrix.get("rows", [])}
    row = rows.get("B-046")
    if not row:
        raise SystemExit("B-046 missing from behavior matrix")
    row["state"] = "CONFIRMED_MATCH"
    row["machine_enforced"] = "PARTIAL"
    row["runtime_observed"] = True
    row["adjudication"] = (
        "Exact frozen-command reproduction disproved the earlier discovery-gap hypothesis. The grep searches each whole line; "
        "a documented `as unknown as Request` fixture is returned because its second ` as Request` substring satisfies ` as [A-Z]`. "
        "A lowercase-target control (`as request`) did not match. The discovery command therefore covers both advertised assertion forms, "
        "although the subsequent migration edits remain prompt-driven rather than mechanically guaranteed."
    )
    row["next_evidence"] = "If deeper verification is needed, test the actual edit/import/type-check migration on representative single- and double-assertion files; discovery coverage itself is closed."
    evidence = {
        "evidence_type": "EXACT_COMMAND_REPRODUCTION",
        "test_id": "CT019-R1",
        "frozen_commit": FROZEN_COMMIT,
        "workflow_run_id": result["workflow_run_id"],
        "result_file": str(OUT_JSON),
    }
    existing = row.setdefault("runtime_evidence", [])
    if evidence not in existing:
        existing.append(evidence)
    MATRIX.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")

    register = REGISTER.read_text(encoding="utf-8")
    primary = (
        "| CT-019 | migrate-to-shoehorn assertion discovery — audit correction | Frozen operative MP-0139 promises both `as Type` and `as unknown as Type` and documents `grep -r \" as [A-Z]\" --include=\"*.test.ts\" --include=\"*.spec.ts\"` as its discovery step. | Exact frozen-command reproduction `CT019-R1` searched a fixture containing both forms. Grep returned the double assertion because `as unknown as Request` contains a later ` as Request` substring that matches the pattern; a lowercase-target control did not match. | AUDIT FALSE POSITIVE / NO SOURCE DISCOVERY GAP | RESOLVED | Earlier audit reasoning incorrectly treated the pattern as if it had to match the first `as` token. The source discovery command was not defective on the advertised double-assertion case. The correction is retained rather than deleting CT-019. |"
    )
    overlay = (
        "| ↳ CT-019 | AUDIT_TOOLING | FIXED | The audit temporarily overstated the source defect surface by registering a discovery gap that the exact command does not have. The frozen source itself was unchanged. | Reproduced exact documented grep against simple, double, and lowercase-control fixtures; both advertised forms are found and the negative control is not. Discovery hypothesis closed; migration-edit correctness remains a separate later test. |"
    )
    register = replace_table_row(register, PRIMARY_OLD_PREFIX, primary)
    register = replace_table_row(register, OVERLAY_OLD_PREFIX, overlay)
    REGISTER.write_text(register, encoding="utf-8")

    print("CT-019 corrected: exact grep finds both advertised assertion forms; B-046 runtime observed")


if __name__ == "__main__":
    main()

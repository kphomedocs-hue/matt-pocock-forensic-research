#!/usr/bin/env python3
"""Run the setup-ts-deep-modules contract in an isolated synthetic consumer repo.

The harness never edits the frozen source checkout. It copies the exact frozen
`dependency-cruiser.config.cjs` into a disposable TypeScript project, installs
the dependency named by the skill, and exercises the completion sequence the
skill itself requires. It also directly observes the shipped fifth rule that
contradicts the prose's unconditional intra-package-freedom claim.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
from typing import Any

FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
OUT_JSON = pathlib.Path("04_DEEP_MODULE_RUNTIME_RESULTS.json")
OUT_MD = pathlib.Path("04_DEEP_MODULE_RUNTIME_RESULTS.md")
CONFIG_REL = pathlib.Path("skills/in-progress/setup-ts-deep-modules/dependency-cruiser.config.cjs")
SKILL_REL = pathlib.Path("skills/in-progress/setup-ts-deep-modules/SKILL.md")


def run(cmd: list[str], *, cwd: pathlib.Path, timeout: int = 180) -> dict[str, Any]:
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def concise(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "command": result.get("command", []),
        "returncode": result.get("returncode"),
        "stdout": result.get("stdout", "")[-5000:],
        "stderr": result.get("stderr", "")[-5000:],
    }


def combined(result: dict[str, Any]) -> str:
    return f"{result.get('stdout', '')}\n{result.get('stderr', '')}"


def write_fixture(root: pathlib.Path) -> None:
    (root / "src/packages/example/lib").mkdir(parents=True, exist_ok=True)
    (root / "src/packages/example/tests").mkdir(parents=True, exist_ok=True)
    (root / "src/packages/example/index.ts").write_text(
        'import { internalThing } from "./lib/impl";\n\n'
        'export function publicThing(): string {\n'
        '  return internalThing();\n'
        '}\n',
        encoding="utf-8",
    )
    (root / "src/packages/example/lib/impl.ts").write_text(
        'export function internalThing(): string {\n'
        '  return "ok";\n'
        '}\n',
        encoding="utf-8",
    )
    (root / "src/packages/example/tests/fixture.ts").write_text(
        'export const fixture = "fixture";\n', encoding="utf-8"
    )
    (root / "src/packages/example/tests/example.test.ts").write_text(
        'import { publicThing } from "../index";\n\n'
        'export const observed = publicThing();\n',
        encoding="utf-8",
    )
    package = {
        "name": "phase4-deep-module-runtime-fixture",
        "private": True,
        "version": "0.0.0",
        "scripts": {"lint:boundaries": "depcruise src/packages"},
        "devDependencies": {},
    }
    (root / "package.json").write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
    tsconfig = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "NodeNext",
            "moduleResolution": "NodeNext",
            "strict": True,
            "skipLibCheck": True,
        },
        "include": ["src/**/*.ts"],
    }
    (root / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2) + "\n", encoding="utf-8")


def record_test(
    test_id: str,
    behavior_ids: list[str],
    title: str,
    assertions: list[str],
    evidence: dict[str, Any],
    errors: list[str],
) -> dict[str, Any]:
    return {
        "test_id": test_id,
        "behavior_ids": behavior_ids,
        "title": title,
        "assertions": assertions,
        "passed": not errors,
        "errors": errors,
        "evidence": evidence,
    }


def upsert_runtime_evidence(row: dict[str, Any], test_ids: list[str], run_id: int) -> None:
    evidence = {
        "evidence_type": "SYNTHETIC_CONSUMER_RUNTIME",
        "test_ids": test_ids,
        "frozen_commit": FROZEN_COMMIT,
        "workflow_run_id": run_id,
        "result_file": str(OUT_JSON),
    }
    existing = row.setdefault("runtime_evidence", [])
    existing = [e for e in existing if e.get("result_file") != str(OUT_JSON)]
    existing.append(evidence)
    row["runtime_evidence"] = existing
    row["runtime_observed"] = True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    args = ap.parse_args()
    source = pathlib.Path(args.source).resolve()

    run_id_raw = os.environ.get("GITHUB_RUN_ID", "0")
    try:
        workflow_run_id = int(run_id_raw)
    except ValueError as exc:
        raise SystemExit(f"GITHUB_RUN_ID must be an integer, got {run_id_raw!r}") from exc
    if workflow_run_id <= 0:
        raise SystemExit("GITHUB_RUN_ID must be a positive integer")

    head = run(["git", "rev-parse", "HEAD"], cwd=source)
    source_head = head["stdout"].strip() if head["returncode"] == 0 else ""
    if source_head != FROZEN_COMMIT:
        raise SystemExit(f"Frozen source checkout mismatch: {source_head!r}")

    skill_text = (source / SKILL_REL).read_text(encoding="utf-8")
    config_text = (source / CONFIG_REL).read_text(encoding="utf-8")
    required_skill_phrases = [
        "Four rules, all `error`",
        "a package's own files import each other freely",
        "pass, then a fail on the deep import, then a pass again",
        "tests-through-entrypoints",
    ]
    missing_phrases = [p for p in required_skill_phrases if p not in skill_text]
    if missing_phrases:
        raise SystemExit(f"Frozen skill contract changed unexpectedly: missing {missing_phrases}")

    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    if matrix.get("frozen_commit") != FROZEN_COMMIT:
        raise SystemExit("Behavior matrix frozen_commit mismatch")
    rows = {row["behavior_id"]: row for row in matrix.get("rows", [])}
    for bid in ("B-012", "B-014"):
        if bid not in rows:
            raise SystemExit(f"Behavior matrix missing {bid}")

    hard_errors: list[str] = []
    tests: list[dict[str, Any]] = []
    dep_version = "UNKNOWN"

    with tempfile.TemporaryDirectory(prefix="phase4-deep-module-") as td:
        fixture = pathlib.Path(td) / "consumer"
        fixture.mkdir(parents=True)
        write_fixture(fixture)
        (fixture / ".dependency-cruiser.cjs").write_text(config_text, encoding="utf-8")

        install = run(
            ["npm", "install", "--save-dev", "--no-audit", "--no-fund", "dependency-cruiser", "typescript"],
            cwd=fixture,
            timeout=240,
        )
        if install["returncode"] != 0:
            hard_errors.append(f"npm install failed with exit {install['returncode']}")
        else:
            versions = run(["npm", "list", "dependency-cruiser", "--json", "--depth=0"], cwd=fixture)
            if versions["returncode"] == 0:
                try:
                    vdata = json.loads(versions["stdout"])
                    dep_version = vdata.get("dependencies", {}).get("dependency-cruiser", {}).get("version", "UNKNOWN")
                except json.JSONDecodeError:
                    pass

        # DM-001 / B-014: exact completion semantics — pass, deliberate test deep import
        # fails with tests-through-entrypoints, revert, pass.
        dm001_errors: list[str] = []
        clean1: dict[str, Any] = {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        violated: dict[str, Any] = clean1
        clean2: dict[str, Any] = clean1
        test_file = fixture / "src/packages/example/tests/example.test.ts"
        original_test = test_file.read_text(encoding="utf-8")
        if not hard_errors:
            clean1 = run(["npm", "run", "lint:boundaries"], cwd=fixture)
            if clean1["returncode"] != 0:
                dm001_errors.append(f"initial clean boundary check exited {clean1['returncode']}")
            test_file.write_text(
                original_test
                + '\nimport { internalThing } from "../lib/impl";\n'
                + 'export const deepViolation = internalThing();\n',
                encoding="utf-8",
            )
            violated = run(["npm", "run", "lint:boundaries"], cwd=fixture)
            if violated["returncode"] == 0:
                dm001_errors.append("deliberate tests -> lib deep import unexpectedly passed")
            if "tests-through-entrypoints" not in combined(violated):
                dm001_errors.append("deep-import failure did not identify tests-through-entrypoints")
            test_file.write_text(original_test, encoding="utf-8")
            clean2 = run(["npm", "run", "lint:boundaries"], cwd=fixture)
            if clean2["returncode"] != 0:
                dm001_errors.append(f"reverted clean boundary check exited {clean2['returncode']}")
        else:
            dm001_errors.extend(hard_errors)
        tests.append(record_test(
            "DM-001",
            ["B-014"],
            "setup-ts-deep-modules required pass/fail/pass proof",
            [
                "clean synthetic example passes lint:boundaries",
                "temporary tests/example.test.ts deep import of ../lib/impl fails",
                "failure names tests-through-entrypoints",
                "reverting the deep import restores a passing boundary check",
            ],
            {
                "clean_before": concise(clean1),
                "deliberate_deep_import": concise(violated),
                "clean_after_revert": concise(clean2),
            },
            dm001_errors,
        ))

        # DM-002 / B-012: observe the shipped fifth rule and the concrete exception to
        # the prose's unconditional intra-package-freedom statement.
        dm002_errors: list[str] = []
        fifth_rule_run: dict[str, Any] = {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        final_clean: dict[str, Any] = fifth_rule_run
        bad_file = fixture / "src/packages/example/lib/import-test-fixture.ts"
        if not hard_errors and not dm001_errors:
            bad_file.write_text(
                'import { fixture } from "../tests/fixture";\n'
                'export const leakedFixture = fixture;\n',
                encoding="utf-8",
            )
            fifth_rule_run = run(["npm", "run", "lint:boundaries"], cwd=fixture)
            if fifth_rule_run["returncode"] == 0:
                dm002_errors.append("same-package non-test import of tests/ unexpectedly passed")
            if "tests-folder-is-private" not in combined(fifth_rule_run):
                dm002_errors.append("same-package tests/ import failure did not identify tests-folder-is-private")
            bad_file.unlink()
            final_clean = run(["npm", "run", "lint:boundaries"], cwd=fixture)
            if final_clean["returncode"] != 0:
                dm002_errors.append(f"clean fixture after fifth-rule test exited {final_clean['returncode']}")
        else:
            dm002_errors.extend(hard_errors or dm001_errors)

        # Directly inspect the exact copied frozen config as a cross-check that the
        # runtime event came from the five shipped error-level forbidden rules.
        config_probe = run(
            [
                "node",
                "-e",
                "const c=require('./.dependency-cruiser.cjs'); console.log(JSON.stringify(c.forbidden.map(r=>({name:r.name,severity:r.severity}))));",
            ],
            cwd=fixture,
        )
        config_rules: list[dict[str, str]] = []
        if config_probe["returncode"] != 0:
            dm002_errors.append("could not inspect copied frozen dependency-cruiser config")
        else:
            try:
                config_rules = json.loads(config_probe["stdout"].strip())
            except json.JSONDecodeError:
                dm002_errors.append("copied config rule probe returned invalid JSON")
        names = [r.get("name") for r in config_rules]
        if len(config_rules) != 5:
            dm002_errors.append(f"expected five shipped forbidden rules, observed {len(config_rules)}")
        if any(r.get("severity") != "error" for r in config_rules):
            dm002_errors.append("not all shipped forbidden rules have error severity")
        if "tests-folder-is-private" not in names:
            dm002_errors.append("shipped fifth tests-folder-is-private rule missing from runtime config probe")

        tests.append(record_test(
            "DM-002",
            ["B-012"],
            "shipped fifth rule constrains claimed intra-package freedom",
            [
                "exact copied frozen config exposes five forbidden rules, all severity=error",
                "tests-folder-is-private is present as a separately named fifth rule",
                "same-package non-test code importing its own tests/ fixture fails",
                "failure names tests-folder-is-private",
                "removing the violating file restores a passing boundary check",
            ],
            {
                "config_rules": config_rules,
                "fifth_rule_violation": concise(fifth_rule_run),
                "clean_after_revert": concise(final_clean),
                "config_probe": concise(config_probe),
            },
            dm002_errors,
        ))

    for test in tests:
        if not test["passed"]:
            hard_errors.append(f"{test['test_id']} failed: {test['errors']}")

    closure_ids = sorted(
        bid for test in tests if test["passed"] for bid in test["behavior_ids"]
    )
    expected_closures = ["B-012", "B-014"]
    if closure_ids != expected_closures:
        hard_errors.append(f"unexpected runtime closure set {closure_ids}; expected {expected_closures}")

    result = {
        "schema_version": 1,
        "source_repo": "mattpocock/skills",
        "frozen_commit": FROZEN_COMMIT,
        "source_checkout_head": source_head,
        "workflow_run_id": workflow_run_id,
        "synthetic_inputs_only": True,
        "user_or_live_repo_touched": False,
        "dependency_cruiser_version": dep_version,
        "runtime_closure_behavior_ids": closure_ids if not hard_errors else [],
        "tests": tests,
        "hard_errors": hard_errors,
    }
    OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Phase 4 Deep-Module Runtime Evidence",
        "",
        f"Frozen source: `mattpocock/skills` @ `{FROZEN_COMMIT}`.",
        "",
        f"Workflow run: `{workflow_run_id}`.",
        "",
        f"Installed dependency-cruiser version: `{dep_version}`.",
        "",
        "The test used only a disposable synthetic TypeScript consumer repo and copied the exact frozen deep-module config; no user or live repository was modified.",
        "",
    ]
    for test in tests:
        lines.extend([
            f"## {test['test_id']} — {test['title']}",
            "",
            f"Status: **{'PASS' if test['passed'] else 'FAIL'}**.",
            "",
        ])
        for assertion in test["assertions"]:
            lines.append(f"- {assertion}")
        if test["errors"]:
            lines.append("")
            lines.append("Errors:")
            for error in test["errors"]:
                lines.append(f"- {error}")
        lines.append("")
    lines.extend([
        "## Adjudication",
        "",
        "B-014 is runtime-observed only if the exact skill completion sequence succeeds: clean pass, deliberate test deep import fails specifically under `tests-through-entrypoints`, revert, clean pass.",
        "",
        "B-012 is runtime-observed only if the exact shipped config exposes five error-level forbidden rules and same-package non-test code is directly observed failing when it imports its own `tests/` fixture under `tests-folder-is-private`. This confirms the already-registered prose/config mismatch; it does not resolve CT-012.",
        "",
        f"Hard errors: **{len(hard_errors)}**.",
        "",
    ])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    if hard_errors:
        raise SystemExit("Deep-module runtime evidence failed:\n- " + "\n- ".join(hard_errors))

    upsert_runtime_evidence(rows["B-014"], ["DM-001"], workflow_run_id)
    rows["B-014"]["adjudication"] = (
        "The skill's proof-of-enforcement completion criterion is now directly runtime-observed in a disposable synthetic TypeScript consumer using the exact frozen config: the clean example passed, a temporary tests/example.test.ts -> ../lib/impl deep import failed specifically under tests-through-entrypoints, and reverting it restored a clean pass."
    )
    rows["B-014"]["next_evidence"] = (
        "Runtime completion semantics are closed for the representative synthetic consumer. Broader compatibility across package managers or unusual repository layouts is a separate generalization question, not required for this row's stated completion claim."
    )

    upsert_runtime_evidence(rows["B-012"], ["DM-002"], workflow_run_id)
    rows["B-012"]["adjudication"] = (
        "Static inspection already established that SKILL.md says four error rules and unconditional intra-package freedom while the shipped config contains five. Direct synthetic-consumer runtime now confirms the extra tests-folder-is-private rule bites: same-package non-test code importing its own tests/ fixture fails under that fifth rule. The prose/config contract mismatch is therefore both statically and operationally demonstrated; CT-012 remains open."
    )
    rows["B-012"]["next_evidence"] = (
        "Source-side correction remains: document five rules plus the tests/ exception, or change the config/prose so the four-rule model is exact. Runtime behavior of the frozen mismatch is now observed."
    )

    MATRIX.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    print(f"Deep-module runtime GREEN: closures={closure_ids}, dependency-cruiser={dep_version}")


if __name__ == "__main__":
    main()

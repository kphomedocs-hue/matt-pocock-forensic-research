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
    p = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return {"command": cmd, "returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


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
    # The frozen skill's own examples use extensionless TypeScript imports. A
    # bundler-style consumer is appropriate here because it resolves those
    # imports without inventing .js suffixes; NodeNext would make the fixture
    # itself unresolved before dependency-cruiser's path rules can be tested.
    tsconfig = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "ESNext",
            "moduleResolution": "Bundler",
            "strict": True,
            "skipLibCheck": True,
        },
        "include": ["src/**/*.ts"],
    }
    (root / "tsconfig.json").write_text(json.dumps(tsconfig, indent=2) + "\n", encoding="utf-8")


def test_record(
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
    ev = {
        "evidence_type": "SYNTHETIC_CONSUMER_RUNTIME",
        "test_ids": test_ids,
        "frozen_commit": FROZEN_COMMIT,
        "workflow_run_id": run_id,
        "result_file": str(OUT_JSON),
    }
    current = [x for x in row.setdefault("runtime_evidence", []) if x.get("result_file") != str(OUT_JSON)]
    current.append(ev)
    row["runtime_evidence"] = current
    row["runtime_observed"] = True


def explicit_check(root: pathlib.Path) -> dict[str, Any]:
    return run(
        [
            "npx",
            "--no-install",
            "depcruise",
            "--config",
            ".dependency-cruiser.cjs",
            "--output-type",
            "err-long",
            "src/packages",
        ],
        cwd=root,
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    args = ap.parse_args()
    source = pathlib.Path(args.source).resolve()

    try:
        workflow_run_id = int(os.environ.get("GITHUB_RUN_ID", "0"))
    except ValueError as exc:
        raise SystemExit("GITHUB_RUN_ID must be an integer") from exc
    if workflow_run_id <= 0:
        raise SystemExit("GITHUB_RUN_ID must be positive")

    head = run(["git", "rev-parse", "HEAD"], cwd=source)
    source_head = head["stdout"].strip() if head["returncode"] == 0 else ""
    if source_head != FROZEN_COMMIT:
        raise SystemExit(f"Frozen source checkout mismatch: {source_head!r}")

    skill_text = (source / SKILL_REL).read_text(encoding="utf-8")
    config_text = (source / CONFIG_REL).read_text(encoding="utf-8")
    required = [
        "Four rules, all `error`",
        "a package's own files import each other freely",
        "pass, then a fail on the deep import, then a pass again",
        "tests-through-entrypoints",
    ]
    missing = [x for x in required if x not in skill_text]
    if missing:
        raise SystemExit(f"Frozen skill contract changed unexpectedly: {missing}")

    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    if matrix.get("frozen_commit") != FROZEN_COMMIT:
        raise SystemExit("Behavior matrix frozen_commit mismatch")
    rows = {r["behavior_id"]: r for r in matrix.get("rows", [])}
    for bid in ("B-012", "B-014"):
        if bid not in rows:
            raise SystemExit(f"Behavior matrix missing {bid}")

    tests: list[dict[str, Any]] = []
    hard_errors: list[str] = []
    dep_version = "UNKNOWN"

    with tempfile.TemporaryDirectory(prefix="phase4-deep-module-") as td:
        root = pathlib.Path(td) / "consumer"
        root.mkdir(parents=True)
        write_fixture(root)
        (root / ".dependency-cruiser.cjs").write_text(config_text, encoding="utf-8")

        install = run(
            ["npm", "install", "--save-dev", "--no-audit", "--no-fund", "dependency-cruiser", "typescript"],
            cwd=root,
            timeout=240,
        )
        if install["returncode"] != 0:
            hard_errors.append(f"npm install failed with exit {install['returncode']}: {combined(install)[-2000:]}")
        else:
            version_run = run(["npm", "list", "dependency-cruiser", "--json", "--depth=0"], cwd=root)
            try:
                dep_version = json.loads(version_run["stdout"]).get("dependencies", {}).get("dependency-cruiser", {}).get("version", "UNKNOWN")
            except Exception:
                dep_version = "UNKNOWN"

        config_probe = run(
            [
                "node",
                "-e",
                "const c=require('./.dependency-cruiser.cjs'); console.log(JSON.stringify(c.forbidden.map(r=>({name:r.name,severity:r.severity}))));",
            ],
            cwd=root,
        )
        config_rules: list[dict[str, str]] = []
        if config_probe["returncode"] == 0:
            try:
                config_rules = json.loads(config_probe["stdout"].strip())
            except json.JSONDecodeError:
                pass

        # DM-001 / B-014: the exact completion proof required by the skill.
        dm1_errors: list[str] = []
        clean_before: dict[str, Any] = {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        exact_violation = clean_before
        explicit_violation = clean_before
        clean_after = clean_before
        test_file = root / "src/packages/example/tests/example.test.ts"
        original_test = test_file.read_text(encoding="utf-8")
        if hard_errors:
            dm1_errors.extend(hard_errors)
        else:
            clean_before = run(["npm", "run", "lint:boundaries"], cwd=root)
            if clean_before["returncode"] != 0:
                dm1_errors.append(f"clean boundary check exited {clean_before['returncode']}")

            test_file.write_text(
                original_test
                + '\nimport { internalThing } from "../lib/impl";\n'
                + 'export const deepViolation = internalThing();\n',
                encoding="utf-8",
            )
            exact_violation = run(["npm", "run", "lint:boundaries"], cwd=root)
            explicit_violation = explicit_check(root)
            if exact_violation["returncode"] == 0:
                dm1_errors.append("exact skill lint:boundaries command let tests -> lib deep import pass")
            if explicit_violation["returncode"] == 0:
                dm1_errors.append("explicit-config dependency-cruiser also let tests -> lib deep import pass")
            if "tests-through-entrypoints" not in combined(exact_violation):
                dm1_errors.append("exact skill command did not report tests-through-entrypoints")
            if "tests-through-entrypoints" not in combined(explicit_violation):
                dm1_errors.append("explicit-config command did not report tests-through-entrypoints")

            test_file.write_text(original_test, encoding="utf-8")
            clean_after = run(["npm", "run", "lint:boundaries"], cwd=root)
            if clean_after["returncode"] != 0:
                dm1_errors.append(f"reverted clean boundary check exited {clean_after['returncode']}")

        tests.append(test_record(
            "DM-001",
            ["B-014"],
            "required pass/fail/pass proof with the exact frozen config",
            [
                "clean example passes the skill's exact lint:boundaries command",
                "temporary tests/example.test.ts -> ../lib/impl deep import fails",
                "both auto-config and explicit-config runs name tests-through-entrypoints",
                "reverting the deep import restores a clean pass",
            ],
            {
                "clean_before": concise(clean_before),
                "exact_skill_violation": concise(exact_violation),
                "explicit_config_violation": concise(explicit_violation),
                "clean_after": concise(clean_after),
            },
            dm1_errors,
        ))

        # DM-002 / B-012: direct observation of the separately named fifth rule.
        dm2_errors: list[str] = []
        fifth_exact: dict[str, Any] = {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        fifth_explicit = fifth_exact
        fifth_clean = fifth_exact
        bad_file = root / "src/packages/example/lib/import-test-fixture.ts"
        if hard_errors:
            dm2_errors.extend(hard_errors)
        else:
            if len(config_rules) != 5:
                dm2_errors.append(f"expected five frozen forbidden rules, got {len(config_rules)}")
            if any(r.get("severity") != "error" for r in config_rules):
                dm2_errors.append("not all frozen forbidden rules have severity=error")
            if "tests-folder-is-private" not in [r.get("name") for r in config_rules]:
                dm2_errors.append("tests-folder-is-private is absent from copied frozen config")

            bad_file.write_text(
                'import { fixture } from "../tests/fixture";\n'
                'export const leakedFixture = fixture;\n',
                encoding="utf-8",
            )
            fifth_exact = run(["npm", "run", "lint:boundaries"], cwd=root)
            fifth_explicit = explicit_check(root)
            if fifth_exact["returncode"] == 0:
                dm2_errors.append("exact skill command let same-package non-test -> tests/ import pass")
            if fifth_explicit["returncode"] == 0:
                dm2_errors.append("explicit-config command let same-package non-test -> tests/ import pass")
            if "tests-folder-is-private" not in combined(fifth_exact):
                dm2_errors.append("exact skill command did not report tests-folder-is-private")
            if "tests-folder-is-private" not in combined(fifth_explicit):
                dm2_errors.append("explicit-config command did not report tests-folder-is-private")
            bad_file.unlink()
            fifth_clean = run(["npm", "run", "lint:boundaries"], cwd=root)
            if fifth_clean["returncode"] != 0:
                dm2_errors.append(f"clean fixture after fifth-rule test exited {fifth_clean['returncode']}")

        tests.append(test_record(
            "DM-002",
            ["B-012"],
            "fifth shipped rule constrains claimed intra-package freedom",
            [
                "exact frozen config exposes five forbidden rules, all severity=error",
                "tests-folder-is-private is the separately named fifth rule",
                "same-package non-test code importing its own tests/ fixture fails",
                "both auto-config and explicit-config runs name tests-folder-is-private",
                "removing the violating file restores a clean pass",
            ],
            {
                "config_rules": config_rules,
                "config_probe": concise(config_probe),
                "exact_skill_violation": concise(fifth_exact),
                "explicit_config_violation": concise(fifth_explicit),
                "clean_after": concise(fifth_clean),
            },
            dm2_errors,
        ))

    for test in tests:
        if not test["passed"]:
            hard_errors.append(f"{test['test_id']} failed: {test['errors']}")

    closure_ids = sorted({bid for test in tests if test["passed"] for bid in test["behavior_ids"]})
    if closure_ids != ["B-012", "B-014"]:
        hard_errors.append(f"unexpected runtime closure set {closure_ids}; expected ['B-012', 'B-014']")

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
        "Only a disposable synthetic TypeScript consumer was used; the frozen source and user/live repositories were not modified.",
        "",
    ]
    for test in tests:
        lines.extend([f"## {test['test_id']} — {test['title']}", "", f"Status: **{'PASS' if test['passed'] else 'FAIL'}**.", ""])
        lines.extend(f"- {a}" for a in test["assertions"])
        if test["errors"]:
            lines.extend(["", "Errors:"])
            lines.extend(f"- {e}" for e in test["errors"])
        lines.append("")
    lines.extend([
        "## Adjudication",
        "",
        "B-014 closes only if the exact frozen completion proof is observed: clean pass, deliberate test deep import fails specifically under `tests-through-entrypoints`, revert, clean pass.",
        "",
        "B-012 closes as runtime-observed only if the exact copied config exposes five error rules and the fifth `tests-folder-is-private` rule is observed rejecting same-package non-test access to `tests/`. CT-012 remains open because runtime evidence confirms the mismatch rather than repairing it.",
        "",
        f"Hard errors: **{len(hard_errors)}**.",
        "",
    ])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    if hard_errors:
        print(json.dumps(result, indent=2))
        raise SystemExit("Deep-module runtime evidence failed:\n- " + "\n- ".join(hard_errors))

    upsert_runtime_evidence(rows["B-014"], ["DM-001"], workflow_run_id)
    rows["B-014"]["adjudication"] = (
        "The skill's proof-of-enforcement completion criterion is directly runtime-observed in a disposable synthetic TypeScript consumer using the exact frozen config: clean pass, temporary tests/example.test.ts -> ../lib/impl failure specifically under tests-through-entrypoints, then clean pass after revert."
    )
    rows["B-014"]["next_evidence"] = (
        "Representative runtime completion semantics are closed. Broader compatibility across package managers and unusual repository layouts remains a separate generalization question."
    )

    upsert_runtime_evidence(rows["B-012"], ["DM-002"], workflow_run_id)
    rows["B-012"]["adjudication"] = (
        "Static inspection established that SKILL.md says four error rules and unconditional intra-package freedom while the shipped config contains five. Synthetic-consumer runtime now confirms the extra tests-folder-is-private rule bites: same-package non-test code importing its own tests/ fixture fails under that fifth rule. The prose/config mismatch is both static and operational; CT-012 remains open."
    )
    rows["B-012"]["next_evidence"] = (
        "Source-side correction remains: document five rules plus the tests/ exception, or change the config/prose so the four-rule model is exact. Frozen runtime behavior is now observed."
    )

    MATRIX.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    print(f"Deep-module runtime GREEN: closures={closure_ids}, dependency-cruiser={dep_version}")


if __name__ == "__main__":
    main()

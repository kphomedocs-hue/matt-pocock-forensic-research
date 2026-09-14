#!/usr/bin/env python3
"""Runtime-observe the frozen setup-pre-commit contract in a disposable npm repo."""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import stat
import subprocess
import tempfile
from typing import Any

FROZEN = "3cca18b368ae95cdbdebbff572ccafa662551015"
SKILL_REL = pathlib.Path("skills/misc/setup-pre-commit/SKILL.md")
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
OUT_JSON = pathlib.Path("04_PRECOMMIT_RUNTIME_RESULTS.json")
OUT_MD = pathlib.Path("04_PRECOMMIT_RUNTIME_RESULTS.md")


def run(cmd: list[str], cwd: pathlib.Path, timeout: int = 240) -> dict[str, Any]:
    p = subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return {
        "command": cmd,
        "returncode": p.returncode,
        "stdout": p.stdout,
        "stderr": p.stderr,
    }


def brief(r: dict[str, Any]) -> dict[str, Any]:
    return {
        "command": r.get("command", []),
        "returncode": r.get("returncode"),
        "stdout": r.get("stdout", "")[-5000:],
        "stderr": r.get("stderr", "")[-5000:],
    }


def text(r: dict[str, Any]) -> str:
    return f"{r.get('stdout', '')}\n{r.get('stderr', '')}"


def is_executable(path: pathlib.Path) -> bool:
    return path.exists() and bool(
        path.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    )


def package_versions(root: pathlib.Path) -> dict[str, str]:
    r = run(
        ["npm", "list", "husky", "lint-staged", "prettier", "--json", "--depth=0"],
        root,
    )
    if r["returncode"] != 0:
        return {}
    try:
        data = json.loads(r["stdout"])
    except json.JSONDecodeError:
        return {}
    return {
        name: info.get("version", "UNKNOWN")
        for name, info in data.get("dependencies", {}).items()
        if name in {"husky", "lint-staged", "prettier"}
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    args = ap.parse_args()
    source = pathlib.Path(args.source).resolve()

    try:
        run_id = int(os.environ.get("GITHUB_RUN_ID", "0"))
    except ValueError as exc:
        raise SystemExit("GITHUB_RUN_ID must be an integer") from exc
    if run_id <= 0:
        raise SystemExit("GITHUB_RUN_ID must be positive")

    head = run(["git", "rev-parse", "HEAD"], source)
    source_head = head["stdout"].strip() if head["returncode"] == 0 else ""
    if source_head != FROZEN:
        raise SystemExit(f"Frozen source checkout mismatch: {source_head!r}")

    skill = (source / SKILL_REL).read_text(encoding="utf-8")
    required = [
        "npx husky init",
        'prepare: "husky"',
        "npx lint-staged\nnpm run typecheck\nnpm run test",
        '"*": "prettier --ignore-unknown --write"',
        "Add pre-commit hooks (husky + lint-staged + prettier)",
        "a good smoke test that everything works",
        "exists and is executable",
    ]
    missing = [x for x in required if x not in skill]
    if missing:
        raise SystemExit(
            f"Frozen setup-pre-commit contract changed unexpectedly: {missing}"
        )

    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows = {r["behavior_id"]: r for r in matrix.get("rows", [])}
    row = rows.get("B-017")
    if row is None:
        raise SystemExit("B-017 missing from behavior matrix")
    if matrix.get("frozen_commit") != FROZEN:
        raise SystemExit("Behavior matrix frozen_commit mismatch")

    errors: list[str] = []
    evidence: dict[str, Any] = {}
    versions: dict[str, str] = {}
    contract_drift: dict[str, Any] = {}

    with tempfile.TemporaryDirectory(prefix="phase4-precommit-") as td:
        root = pathlib.Path(td) / "consumer"
        root.mkdir()

        init = run(["git", "init", "-b", "main"], root)
        if init["returncode"] != 0:
            errors.append("git init failed")
        run(["git", "config", "user.name", "phase4-precommit-runtime"], root)
        run(
            [
                "git",
                "config",
                "user.email",
                "phase4-precommit-runtime@example.invalid",
            ],
            root,
        )

        pkg = {
            "name": "phase4-precommit-runtime-fixture",
            "version": "0.0.0",
            "private": True,
            "scripts": {
                "typecheck": "node -e \"console.log('TYPECHECK_HOOK_OK')\"",
                "test": "node -e \"console.log('TEST_HOOK_OK')\"",
            },
        }
        (root / "package.json").write_text(
            json.dumps(pkg, indent=2) + "\n", encoding="utf-8"
        )
        (root / "package-lock.json").write_text(
            json.dumps(
                {
                    "name": pkg["name"],
                    "version": "0.0.0",
                    "lockfileVersion": 3,
                    "requires": True,
                    "packages": {
                        "": {"name": pkg["name"], "version": "0.0.0"}
                    },
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        # Keep installed dependencies out of the synthetic commit. The frozen
        # skill says to leave existing ignore rules untouched; this fixture
        # begins with the conventional npm ignore rule already present.
        (root / ".gitignore").write_text("node_modules/\n", encoding="utf-8")

        install = run(
            [
                "npm",
                "install",
                "--save-dev",
                "--no-audit",
                "--no-fund",
                "husky",
                "lint-staged",
                "prettier",
            ],
            root,
        )
        evidence["install"] = brief(install)
        if install["returncode"] != 0:
            errors.append(f"dependency install failed: {install['returncode']}")

        versions = package_versions(root) if install["returncode"] == 0 else {}
        if set(versions) != {"husky", "lint-staged", "prettier"}:
            errors.append(
                f"could not resolve all installed package versions: {versions}"
            )

        husky_init = (
            run(["npx", "--no-install", "husky", "init"], root)
            if not errors
            else {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        )
        evidence["husky_init"] = brief(husky_init)
        if not errors and husky_init["returncode"] != 0:
            errors.append(f"husky init failed: {husky_init['returncode']}")

        hook = root / ".husky/pre-commit"
        shim = root / ".husky/_/pre-commit"

        if not errors and not hook.exists():
            errors.append("npx husky init did not create .husky/pre-commit")

        if not errors:
            # Follow the frozen skill literally. Do not chmod the user hook:
            # Husky 9 writes this file non-executable and dispatches it through
            # its executable .husky/_ shim.
            hook.write_text(
                "npx lint-staged\nnpm run typecheck\nnpm run test\n",
                encoding="utf-8",
            )
            (root / ".lintstagedrc").write_text(
                json.dumps({"*": "prettier --ignore-unknown --write"}, indent=2)
                + "\n",
                encoding="utf-8",
            )
            (root / ".prettierrc").write_text(
                json.dumps(
                    {
                        "useTabs": False,
                        "tabWidth": 2,
                        "printWidth": 80,
                        "singleQuote": False,
                        "trailingComma": "es5",
                        "semi": True,
                        "arrowParens": "always",
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (root / "src").mkdir()
            (root / "src/manual-target.js").write_text(
                "const manual={alpha:1,beta:[1,2,3]}\n",
                encoding="utf-8",
            )

        pkg_after = (
            json.loads((root / "package.json").read_text(encoding="utf-8"))
            if (root / "package.json").exists()
            else {}
        )
        prepare_value = pkg_after.get("scripts", {}).get("prepare")
        user_hook_executable = is_executable(hook)
        shim_executable = is_executable(shim)
        hooks_path = run(["git", "config", "--get", "core.hooksPath"], root)
        hooks_path_value = hooks_path["stdout"].strip()
        evidence["core_hooks_path"] = brief(hooks_path)
        evidence["hook_modes"] = {
            "user_hook_exists": hook.exists(),
            "user_hook_executable": user_hook_executable,
            "shim_exists": shim.exists(),
            "shim_executable": shim_executable,
        }

        contract_drift = {
            "frozen_verification_predicate": (
                ".husky/pre-commit exists and is executable"
            ),
            "husky_version": versions.get("husky"),
            "observed_user_hook_exists": hook.exists(),
            "observed_user_hook_executable": user_hook_executable,
            "observed_shim_exists": shim.exists(),
            "observed_shim_executable": shim_executable,
            "core_hooks_path": hooks_path_value,
            "mechanism": (
                "Husky 9 wires Git to .husky/_; the executable pre-commit shim "
                "invokes the user .husky/pre-commit file through sh -e, so the "
                "user hook itself need not carry an executable bit."
            ),
            "frozen_predicate_matches_observation": bool(
                hook.exists() and user_hook_executable
            ),
        }

        if prepare_value != "husky":
            errors.append(
                f"prepare script is {prepare_value!r}, expected 'husky'"
            )
        if not hook.exists():
            errors.append(".husky/pre-commit missing after Husky initialization")
        if not shim.exists():
            errors.append(".husky/_/pre-commit shim missing after Husky initialization")
        if shim.exists() and not shim_executable:
            errors.append(".husky/_/pre-commit shim is not executable")
        if not (root / ".lintstagedrc").exists():
            errors.append(".lintstagedrc missing")
        if not (root / ".prettierrc").exists():
            errors.append(".prettierrc missing")
        if hooks_path["returncode"] != 0 or ".husky/_" not in hooks_path_value:
            errors.append(
                f"git core.hooksPath not wired to Husky: {hooks_path_value!r}"
            )

        stage_before_verify = (
            run(["git", "add", "."], root)
            if not errors
            else {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        )
        manual_lint = (
            run(["npx", "--no-install", "lint-staged"], root)
            if not errors
            else {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        )
        evidence["manual_lint_staged"] = brief(manual_lint)
        if not errors and stage_before_verify["returncode"] != 0:
            errors.append("git add before manual lint-staged failed")
        if not errors and manual_lint["returncode"] != 0:
            errors.append(
                f"manual npx lint-staged verification failed: "
                f"{manual_lint['returncode']}"
            )

        manual_text = (
            (root / "src/manual-target.js").read_text(encoding="utf-8")
            if (root / "src/manual-target.js").exists()
            else ""
        )
        if (
            not errors
            and "const manual = { alpha: 1, beta: [1, 2, 3] };" not in manual_text
        ):
            errors.append(
                "manual lint-staged did not apply Prettier to staged JavaScript"
            )

        # Add a fresh unformatted staged file *after* manual verification.
        # Its formatting in HEAD proves the actual Git pre-commit path ran
        # lint-staged, rather than reusing the manual verification result.
        hook_target = root / "src/hook-target.js"
        if not errors:
            hook_target.write_text(
                "const hook={works:true,list:[3,2,1]}\n",
                encoding="utf-8",
            )
            add_hook_target = run(["git", "add", "src/hook-target.js"], root)
            if add_hook_target["returncode"] != 0:
                errors.append("could not stage hook-only formatting target")

        commit = (
            run(
                [
                    "git",
                    "commit",
                    "-m",
                    "Add pre-commit hooks (husky + lint-staged + prettier)",
                ],
                root,
            )
            if not errors
            else {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        )
        evidence["commit_smoke"] = brief(commit)
        commit_log = text(commit)
        if not errors and commit["returncode"] != 0:
            errors.append(
                f"actual git commit smoke test failed: {commit['returncode']}"
            )
        if not errors and "TYPECHECK_HOOK_OK" not in commit_log:
            errors.append("commit hook output missing TYPECHECK_HOOK_OK")
        if not errors and "TEST_HOOK_OK" not in commit_log:
            errors.append("commit hook output missing TEST_HOOK_OK")

        log_subject = (
            run(["git", "log", "-1", "--pretty=%s"], root)
            if not errors
            else {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        )
        evidence["commit_subject"] = brief(log_subject)
        if (
            not errors
            and log_subject["stdout"].strip()
            != "Add pre-commit hooks (husky + lint-staged + prettier)"
        ):
            errors.append("expected smoke-test commit was not created")

        committed_hook_target = (
            run(["git", "show", "HEAD:src/hook-target.js"], root)
            if not errors
            else {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        )
        evidence["committed_hook_target"] = brief(committed_hook_target)
        if (
            not errors
            and "const hook = { works: true, list: [3, 2, 1] };"
            not in committed_hook_target["stdout"]
        ):
            errors.append(
                "actual pre-commit lint-staged hook did not format/re-stage "
                "hook-target.js"
            )

        status = (
            run(["git", "status", "--porcelain"], root)
            if not errors
            else {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        )
        evidence["final_status"] = brief(status)
        if not errors and status["stdout"].strip():
            errors.append(
                f"synthetic repo not clean after smoke commit: "
                f"{status['stdout']!r}"
            )

    passed = not errors
    result = {
        "schema_version": 2,
        "source_repo": "mattpocock/skills",
        "frozen_commit": FROZEN,
        "source_checkout_head": source_head,
        "workflow_run_id": run_id,
        "synthetic_inputs_only": True,
        "user_or_live_repo_touched": False,
        "package_versions": versions,
        "contract_drift": contract_drift,
        "tests": [
            {
                "test_id": "PC-001",
                "behavior_ids": ["B-017"],
                "title": "setup-pre-commit end-to-end Husky commit smoke",
                "passed": passed,
                "errors": errors,
                "evidence": evidence,
            }
        ],
        "runtime_closure_behavior_ids": ["B-017"] if passed else [],
        "hard_errors": errors,
    }
    OUT_JSON.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )

    drift_status = (
        "MISMATCH"
        if contract_drift
        and contract_drift.get("frozen_predicate_matches_observation") is False
        else "MATCH"
    )
    OUT_MD.write_text(
        "# Phase 4 Setup-Pre-Commit Runtime Evidence\n\n"
        f"Frozen source: `mattpocock/skills` @ `{FROZEN}`.\n\n"
        f"Workflow run: `{run_id}`.\n\n"
        f"Resolved packages: `{json.dumps(versions, sort_keys=True)}`.\n\n"
        "Only a disposable synthetic npm/git repository was used; no user or "
        "live repository was touched.\n\n"
        "## Frozen verification predicate vs current Husky\n\n"
        f"Executable-bit predicate: **{drift_status}**. "
        f"User hook executable: **{contract_drift.get('observed_user_hook_executable')}**; "
        f"Husky shim executable: **{contract_drift.get('observed_shim_executable')}**; "
        f"`core.hooksPath`: `{contract_drift.get('core_hooks_path')}`.\n\n"
        "The mismatch is preserved as evidence rather than repaired with "
        "`chmod`: current Husky dispatches through its executable `.husky/_` "
        "shim, which invokes the user hook with `sh -e`.\n\n"
        "## PC-001 — end-to-end hook smoke\n\n"
        f"Status: **{'PASS' if passed else 'FAIL'}**.\n\n"
        "The harness follows the frozen functional contract: unversioned "
        "Husky/lint-staged/Prettier installation, `husky init`, exact hook body, "
        "manual `lint-staged` verification, then an actual Git commit with the "
        "documented message. A second unformatted file is staged only after "
        "manual verification so its committed formatting proves the commit "
        "hook executed lint-staged; typecheck/test markers prove the later hook "
        "commands executed too.\n\n"
        f"Hard errors: **{len(errors)}**.\n",
        encoding="utf-8",
    )

    if errors:
        print(json.dumps(result, indent=2))
        raise SystemExit(
            "setup-pre-commit runtime failed:\n- " + "\n- ".join(errors)
        )

    row["runtime_observed"] = True
    row["adjudication"] = (
        "The frozen setup-pre-commit workflow is directly runtime-observed in "
        "a disposable npm/git repository. Husky initialization created "
        "prepare=husky and executable Git-hook shim plumbing; manual lint-staged "
        "formatted a staged file; then an actual commit using the documented "
        "message ran lint-staged, typecheck, and tests, formatted and re-staged "
        "a hook-only target, and completed cleanly. One frozen verification "
        "predicate is stale against the resolved Husky version: the generated "
        ".husky/pre-commit user file is not executable, while the executable "
        ".husky/_/pre-commit shim invokes it through sh -e. Functional hook "
        "execution still succeeds."
    )
    row["next_evidence"] = (
        "Representative npm end-to-end smoke is closed. Preserve the "
        "executable-bit predicate mismatch as toolchain drift; package-manager "
        "variants and future upstream Husky/lint-staged compatibility remain "
        "separate generalization/current-state questions."
    )
    ev = {
        "evidence_type": "SYNTHETIC_CONSUMER_RUNTIME",
        "test_ids": ["PC-001"],
        "frozen_commit": FROZEN,
        "workflow_run_id": run_id,
        "result_file": str(OUT_JSON),
    }
    existing = [
        x
        for x in row.setdefault("runtime_evidence", [])
        if x.get("result_file") != str(OUT_JSON)
    ]
    existing.append(ev)
    row["runtime_evidence"] = existing
    MATRIX.write_text(
        json.dumps(matrix, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "setup-pre-commit runtime GREEN: "
        f"B-017, packages={versions}, contract_drift={contract_drift}"
    )


if __name__ == "__main__":
    main()

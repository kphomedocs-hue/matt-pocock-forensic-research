#!/usr/bin/env python3
"""Run benign deterministic runtime checks against the exact frozen source tree.

This harness never uses real credentials or external accounts. It exercises only
local shell/Node/npm behavior with synthetic fixtures, writes durable evidence,
and optionally promotes named behavior rows to runtime_observed only when all
checks for that row pass.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone

FROZEN = "3cca18b368ae95cdbdebbff572ccafa662551015"
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
OUT_JSON = pathlib.Path("04_RUNTIME_EXECUTION_EVIDENCE.json")
OUT_MD = pathlib.Path("04_RUNTIME_EXECUTION_EVIDENCE.md")


def run(cmd, *, cwd=None, input_text=None, env=None):
    p = subprocess.run(
        cmd,
        cwd=cwd,
        input=input_text,
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    return {
        "cmd": cmd,
        "returncode": p.returncode,
        "stdout": p.stdout,
        "stderr": p.stderr,
    }


def check_source(source: pathlib.Path):
    r = run(["git", "rev-parse", "HEAD"], cwd=source)
    head = r["stdout"].strip()
    if r["returncode"] != 0 or head != FROZEN:
        raise SystemExit(f"Frozen source mismatch: expected {FROZEN}, got {head!r}")


def npm_env():
    env = os.environ.copy()
    env.update({
        "npm_config_audit": "false",
        "npm_config_fund": "false",
        "npm_config_update_notifier": "false",
    })
    return env


def test_b004(source: pathlib.Path):
    """Observe practical npm treatment of the frozen package/lock version drift."""
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        shutil.copy2(source / "package.json", root / "package.json")
        shutil.copy2(source / "package-lock.json", root / "package-lock.json")

        package = json.loads((root / "package.json").read_text(encoding="utf-8"))
        lock_before = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))
        package_version = package["version"]
        lock_top_before = lock_before["version"]
        lock_root_before = lock_before["packages"][""]["version"]

        pack = run(
            ["npm", "pack", "--dry-run", "--json", "--ignore-scripts"],
            cwd=root,
            env=npm_env(),
        )
        try:
            pack_json = json.loads(pack["stdout"])
            packed_version = pack_json[0]["version"]
            packed_filename = pack_json[0]["filename"]
        except Exception:
            packed_version = None
            packed_filename = None

        normalize = run(
            ["npm", "install", "--package-lock-only", "--ignore-scripts", "--offline"],
            cwd=root,
            env=npm_env(),
        )
        lock_after = json.loads((root / "package-lock.json").read_text(encoding="utf-8"))
        lock_top_after = lock_after["version"]
        lock_root_after = lock_after["packages"][""]["version"]

        checks = [
            {
                "name": "frozen_fixture_contains_expected_version_drift",
                "passed": package_version == "1.2.3" and lock_top_before == "0.0.0" and lock_root_before == "0.0.0",
                "returncode": 0,
            },
            {
                "name": "npm_pack_uses_package_json_version",
                "passed": pack["returncode"] == 0 and packed_version == package_version and package_version in (packed_filename or ""),
                "returncode": pack["returncode"],
            },
            {
                "name": "offline_lockfile_normalization_succeeds",
                "passed": normalize["returncode"] == 0,
                "returncode": normalize["returncode"],
            },
            {
                "name": "npm_normalizes_root_lock_versions_to_package_json",
                "passed": lock_top_after == package_version and lock_root_after == package_version,
                "returncode": normalize["returncode"],
            },
        ]
        passed = all(c["passed"] for c in checks)
        return {
            "behavior_id": "B-004",
            "passed": passed,
            "summary": "Frozen package/lock drift was reproduced; npm pack used package.json version 1.2.3, and offline package-lock-only normalization rewrote both root lockfile version fields to 1.2.3.",
            "checks": checks,
            "remaining_scope": "This establishes local npm practical behavior. It does not prove every CI/release consumer ignores the stale frozen lock metadata; release-path observation remains separate under B-029.",
        }


def test_b015(source: pathlib.Path):
    template = source / "skills/engineering/wizard/template.sh"
    checks = []
    syntax = run(["bash", "-n", str(template)])
    checks.append(("bash_n", syntax["returncode"] == 0, syntax))

    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        env_file = td / ".env.audit"
        dummy_pub = "pk_test_forensic_dummy"
        dummy_secret = "sk_test_forensic_dummy"
        first = run(
            ["bash", str(template)],
            cwd=td,
            input_text=f"\n{dummy_pub}\n{dummy_secret}\n",
            env={"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "ENV_FILE": str(env_file)},
        )
        env_text = env_file.read_text(encoding="utf-8") if env_file.exists() else ""
        first_ok = (
            first["returncode"] == 0
            and f"STRIPE_PUBLISHABLE_KEY={dummy_pub}" in env_text
            and f"STRIPE_SECRET_KEY={dummy_secret}" in env_text
            and dummy_secret not in first["stdout"]
            and dummy_secret not in first["stderr"]
        )
        checks.append(("first_run_writes_dummy_values_without_echoing_secret", first_ok, first))

        second = run(
            ["bash", str(template)],
            cwd=td,
            input_text="\n\n\n",
            env={"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "ENV_FILE": str(env_file)},
        )
        env_text2 = env_file.read_text(encoding="utf-8") if env_file.exists() else ""
        second_ok = (
            second["returncode"] == 0
            and env_text2.count("STRIPE_PUBLISHABLE_KEY=") == 1
            and env_text2.count("STRIPE_SECRET_KEY=") == 1
            and f"STRIPE_PUBLISHABLE_KEY={dummy_pub}" in env_text2
            and f"STRIPE_SECRET_KEY={dummy_secret}" in env_text2
        )
        checks.append(("rerun_preserves_existing_values_idempotently", second_ok, second))

    passed = all(ok for _, ok, _ in checks)
    return {
        "behavior_id": "B-015",
        "passed": passed,
        "summary": "Wizard template passed bash syntax plus benign end-to-end first-run and rerun/idempotence checks with synthetic values.",
        "checks": [{"name": n, "passed": ok, "returncode": d["returncode"]} for n, ok, d in checks],
        "remaining_scope": "This observes the shipped template library/example locally; it does not prove every future agent-generated wizard or browser instruction is correct.",
    }


def test_b018(source: pathlib.Path):
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "scripts").mkdir()
        (root / ".claude-plugin").mkdir()
        shutil.copy2(source / "package.json", root / "package.json")
        shutil.copy2(source / ".claude-plugin/plugin.json", root / ".claude-plugin/plugin.json")
        shutil.copy2(source / "scripts/sync-plugin-version.mjs", root / "scripts/sync-plugin-version.mjs")

        package_version = json.loads((root / "package.json").read_text(encoding="utf-8"))["version"]
        initial = run(["node", "scripts/sync-plugin-version.mjs", "--check"], cwd=root)

        plugin_path = root / ".claude-plugin/plugin.json"
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        plugin["version"] = "0.0.0-forensic-drift"
        plugin_path.write_text(json.dumps(plugin, indent=2) + "\n", encoding="utf-8")
        drift = run(["node", "scripts/sync-plugin-version.mjs", "--check"], cwd=root)
        repair = run(["node", "scripts/sync-plugin-version.mjs"], cwd=root)
        repaired_version = json.loads(plugin_path.read_text(encoding="utf-8"))["version"]

        checks = [
            {"name": "in_sync_check_passes", "passed": initial["returncode"] == 0, "returncode": initial["returncode"]},
            {"name": "drift_check_fails", "passed": drift["returncode"] == 1, "returncode": drift["returncode"]},
            {"name": "repair_restores_package_version", "passed": repair["returncode"] == 0 and repaired_version == package_version, "returncode": repair["returncode"]},
            {"name": "script_operates_without_package_lock_present", "passed": not (root / "package-lock.json").exists() and repair["returncode"] == 0, "returncode": repair["returncode"]},
        ]
        passed = all(c["passed"] for c in checks)
        return {
            "behavior_id": "B-018",
            "passed": passed,
            "summary": "Version sync executable detected synthetic plugin drift and repaired plugin.json to package.json without requiring package-lock.json.",
            "checks": checks,
            "remaining_scope": "This proves the local sync mechanism, not a live Changesets release run; package-lock remains outside the mechanism and is tracked separately by B-004/CT-004.",
        }


def test_b056(source: pathlib.Path):
    script = source / "skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh"
    syntax = run(["bash", "-n", str(script)])
    exec_result = run(
        ["bash", str(script)],
        input_text="\ny\nsynthetic-error-forensic\n",
        env={"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"},
    )
    combined = exec_result["stdout"] + exec_result["stderr"]
    checks = [
        {"name": "bash_n", "passed": syntax["returncode"] == 0, "returncode": syntax["returncode"]},
        {"name": "benign_flow_completes", "passed": exec_result["returncode"] == 0, "returncode": exec_result["returncode"]},
        {"name": "captured_values_are_printed_for_agent", "passed": "ERRORED=y" in combined and "ERROR_MSG=synthetic-error-forensic" in combined, "returncode": exec_result["returncode"]},
    ]
    passed = all(c["passed"] for c in checks)
    return {
        "behavior_id": "B-056",
        "passed": passed,
        "summary": "HITL template passed syntax and a benign synthetic interaction; captured values were emitted exactly as documented for agent parsing.",
        "checks": checks,
        "remaining_scope": "The observation confirms the helper contract and its disclosure surface; misuse resistance and secret/PII handling still require red-team testing.",
    }


def apply_results(results):
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    by_id = {r["behavior_id"]: r for r in matrix["rows"]}
    notes = {
        "B-004": "Direct frozen runtime observation: the stale 0.0.0 lock metadata was reproduced; npm pack selected package.json version 1.2.3, and an offline package-lock-only normalization rewrote both root lock version fields to 1.2.3.",
        "B-015": "Direct frozen runtime observation: bash syntax passed; the shipped example completed with synthetic values, wrote the expected env entries without echoing the dummy secret, and preserved existing values on rerun.",
        "B-018": "Direct frozen runtime observation: --check passed in sync, failed on synthetic drift, and the executable repaired plugin.json to package.json without package-lock.json present.",
        "B-056": "Direct frozen runtime observation: the HITL shell template passed syntax and completed a benign synthetic interaction, emitting captured values exactly as documented.",
    }
    nexts = {
        "B-004": "Release-path observation remains separate under B-029; local npm behavior shows the stale root lock version is normalized and does not control npm pack versioning.",
        "B-015": "Red-team generated wizard variants and browser-step accuracy later; this runtime observation covers the shipped template library/example only.",
        "B-018": "Observe a live Changesets release/version-PR path later; B-004 separately tracks package-lock version truth.",
        "B-056": "Red-team secret/PII misuse and shell-input edge cases later; do not use real credentials.",
    }
    for result in results:
        bid = result["behavior_id"]
        if not result["passed"]:
            continue
        row = by_id[bid]
        row["runtime_observed"] = True
        if notes[bid] not in row["adjudication"]:
            row["adjudication"] = row["adjudication"].rstrip() + " " + notes[bid]
        row["next_evidence"] = nexts[bid]
    MATRIX.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")


def render(results, source_head):
    report = {
        "schema_version": 1,
        "source_repo": "mattpocock/skills",
        "frozen_commit": FROZEN,
        "observed_source_head": source_head,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "tests": results,
        "all_passed": all(r["passed"] for r in results),
    }
    OUT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Phase 4 Local Runtime Execution Evidence",
        "",
        f"Frozen source: `mattpocock/skills` @ `{FROZEN}`.",
        "",
        "Scope: benign local execution only. No live credentials, external accounts, or destructive source mutations are used.",
        "",
        "| Behavior | Result | Observation | Remaining scope |",
        "|---|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {r['behavior_id']} | {'PASS' if r['passed'] else 'FAIL'} | {r['summary']} | {r['remaining_scope']} |")
    lines += ["", f"Overall: **{'PASS' if report['all_passed'] else 'FAIL'}**.", ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="source")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    source = pathlib.Path(args.source).resolve()
    check_source(source)
    source_head = run(["git", "rev-parse", "HEAD"], cwd=source)["stdout"].strip()

    results = [test_b004(source), test_b015(source), test_b018(source), test_b056(source)]
    report = render(results, source_head)
    if not report["all_passed"]:
        failed = [r["behavior_id"] for r in results if not r["passed"]]
        raise SystemExit(f"Runtime checks failed: {failed}")
    if args.apply:
        apply_results(results)
    print("Phase 4 local runtime checks PASS:", ", ".join(r["behavior_id"] for r in results))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Run isolated Phase 4 runtime smoke tests against the frozen source checkout.

The harness uses only synthetic inputs and disposable HOME/source copies. It
records supporting evidence separately from row-level runtime closure. Only a
behavior whose complete matrix claim is satisfied by the test may be promoted
from runtime_observed=false to true.
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
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
OUT_JSON = pathlib.Path("04_RUNTIME_SMOKE_RESULTS.json")
OUT_MD = pathlib.Path("04_RUNTIME_SMOKE_RESULTS.md")


def run(cmd: list[str], *, cwd: pathlib.Path, env: dict[str, str] | None = None, stdin: str | None = None) -> dict[str, Any]:
    p = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        input=stdin,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
    )
    return {"command": cmd, "returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def concise(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "command": result["command"],
        "returncode": result["returncode"],
        "stdout": result["stdout"][-4000:],
        "stderr": result["stderr"][-4000:],
    }


def result_row(test_id: str, behavior_ids: list[str], closure_ids: list[str], title: str, assertions: list[str], evidence: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    return {
        "test_id": test_id,
        "title": title,
        "behavior_ids": behavior_ids,
        "runtime_closure_behavior_ids": closure_ids if not errors else [],
        "status": "PASS" if not errors else "FAIL",
        "assertions": assertions,
        "errors": errors,
        "evidence": evidence,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    args = ap.parse_args()
    source = pathlib.Path(args.source).resolve()

    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    hard_errors: list[str] = []
    results: list[dict[str, Any]] = []

    if matrix.get("frozen_commit") != FROZEN_COMMIT or census.get("frozen_commit") != FROZEN_COMMIT:
        raise SystemExit("Research inputs do not match frozen commit")

    head = run(["git", "rev-parse", "HEAD"], cwd=source)
    source_head = head["stdout"].strip() if head["returncode"] == 0 else ""
    if source_head != FROZEN_COMMIT:
        raise SystemExit(f"Frozen source checkout mismatch: {source_head!r}")

    behavior_ids = {r["behavior_id"] for r in matrix.get("rows", [])}
    expected_skills = sorted(
        f["path"]
        for f in census.get("files", [])
        if f.get("category") == "skill" and f.get("path", "").endswith("/SKILL.md")
    )
    if len(expected_skills) != 37:
        raise SystemExit(f"Expected 37 current skills, found {len(expected_skills)}")

    # RT-001 — list-skills exact enumeration (B-020 row-level closure).
    errs: list[str] = []
    r = run(["bash", "scripts/list-skills.sh"], cwd=source)
    actual = [line for line in r["stdout"].splitlines() if line.strip()]
    if r["returncode"] != 0:
        errs.append(f"list-skills exited {r['returncode']}")
    if actual != expected_skills:
        errs.append("list-skills output does not exactly equal frozen 37-skill census")
    results.append(result_row(
        "RT-001", ["B-020"], ["B-020"], "list-skills exact frozen census enumeration",
        ["exit 0", "output exactly equals the 37 current SKILL.md census paths in sorted order"],
        {"observed_count": len(actual), "expected_count": len(expected_skills), "command": concise(r)}, errs,
    ))

    # RT-002 — link-skills exact set, targets, both destinations, idempotence (B-019 closure).
    errs = []
    expected_link_paths = [p for p in expected_skills if "/misc/" not in f"/{p}" and "/deprecated/" not in f"/{p}"]
    expected_names = sorted(pathlib.PurePosixPath(p).parent.name for p in expected_link_paths)
    if len(expected_link_paths) != 33 or len(set(expected_names)) != 33:
        errs.append(f"expected unique 33-skill link set, got paths={len(expected_link_paths)} names={len(set(expected_names))}")
    first: dict[str, Any] | None = None
    second: dict[str, Any] | None = None
    inspected: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="phase4-link-home-") as td:
        home = pathlib.Path(td)
        env = os.environ.copy(); env["HOME"] = str(home)
        first = run(["bash", "scripts/link-skills.sh"], cwd=source, env=env)
        second = run(["bash", "scripts/link-skills.sh"], cwd=source, env=env)
        if first["returncode"] != 0 or second["returncode"] != 0:
            errs.append(f"link-skills exit codes were {first['returncode']} then {second['returncode']}")
        source_targets = {pathlib.PurePosixPath(p).parent.name: (source / pathlib.PurePosixPath(p).parent).resolve() for p in expected_link_paths}
        for rel in [pathlib.Path(".claude/skills"), pathlib.Path(".agents/skills")]:
            dest = home / rel
            names = sorted(p.name for p in dest.iterdir()) if dest.is_dir() else []
            wrong_links: list[str] = []
            for name in names:
                p = dest / name
                if not p.is_symlink():
                    wrong_links.append(f"{name}:not-symlink")
                    continue
                resolved = p.resolve()
                if name not in source_targets or resolved != source_targets[name]:
                    wrong_links.append(f"{name}:{resolved}")
            inspected[str(rel)] = {"count": len(names), "names": names, "wrong_links": wrong_links}
            if names != expected_names:
                errs.append(f"{rel} does not contain exact expected 33 names")
            if wrong_links:
                errs.append(f"{rel} has wrong/non-symlink targets: {wrong_links}")
    results.append(result_row(
        "RT-002", ["B-019"], ["B-019"], "link-skills exact set, targets and idempotence",
        ["33 expected skills", "both harness destinations contain exact same symlink set", "all symlinks resolve into frozen checkout", "second run remains successful and exact"],
        {"expected_count": 33, "destinations": inspected, "first_run": concise(first or {}), "second_run": concise(second or {})}, errs,
    ))

    # RT-003 — link-skills refuses a destination symlink resolving into source repo (supporting B-019).
    errs = []
    with tempfile.TemporaryDirectory(prefix="phase4-link-guard-") as td:
        home = pathlib.Path(td)
        (home / ".claude").mkdir(parents=True)
        (home / ".claude" / "skills").symlink_to(source / "skills", target_is_directory=True)
        env = os.environ.copy(); env["HOME"] = str(home)
        guard = run(["bash", "scripts/link-skills.sh"], cwd=source, env=env)
        if guard["returncode"] != 1:
            errs.append(f"expected self-link guard exit 1, got {guard['returncode']}")
        if "symlink into this repo" not in guard["stderr"]:
            errs.append("self-link guard diagnostic missing")
    results.append(result_row(
        "RT-003", ["B-019"], [], "link-skills self-link pollution guard",
        ["destination symlink into frozen repo exits 1", "diagnostic identifies symlink-into-repo condition"],
        {"command": concise(guard)}, errs,
    ))

    # RT-004 — plugin sync executable mechanism. Supports B-018 but does not close its full release/CI claim.
    errs = []
    with tempfile.TemporaryDirectory(prefix="phase4-version-sync-") as td:
        copy = pathlib.Path(td) / "source"
        shutil.copytree(source, copy, symlinks=True, ignore=shutil.ignore_patterns(".git"))
        package = json.loads((copy / "package.json").read_text(encoding="utf-8"))
        plugin_path = copy / ".claude-plugin" / "plugin.json"
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        initial = run(["node", "scripts/sync-plugin-version.mjs", "--check"], cwd=copy)
        if initial["returncode"] != 0 or plugin.get("version") != package.get("version"):
            errs.append("frozen package/plugin versions are not initially check-clean")
        plugin["version"] = "0.0.0-runtime-smoke"
        plugin_path.write_text(json.dumps(plugin, indent=2) + "\n", encoding="utf-8")
        before_check = plugin_path.read_text(encoding="utf-8")
        mismatch = run(["node", "scripts/sync-plugin-version.mjs", "--check"], cwd=copy)
        after_check = plugin_path.read_text(encoding="utf-8")
        if mismatch["returncode"] != 1:
            errs.append(f"mismatch --check expected exit 1, got {mismatch['returncode']}")
        if after_check != before_check:
            errs.append("--check mutated plugin.json")
        fix = run(["node", "scripts/sync-plugin-version.mjs"], cwd=copy)
        fixed_plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        final_check = run(["node", "scripts/sync-plugin-version.mjs", "--check"], cwd=copy)
        if fix["returncode"] != 0 or fixed_plugin.get("version") != package.get("version") or final_check["returncode"] != 0:
            errs.append("normal sync did not restore package/plugin equality and final clean check")
    results.append(result_row(
        "RT-004", ["B-018"], [], "plugin-version executable sync/check mechanism",
        ["clean frozen pair passes --check", "synthetic mismatch fails --check without mutation", "normal sync repairs mismatch", "repaired pair passes --check"],
        {"package_version": package.get("version"), "initial": concise(initial), "mismatch": concise(mismatch), "fix": concise(fix), "final_check": concise(final_check), "row_closure_withheld_reason": "B-018 also claims release/CI path behavior; local script execution alone is supporting evidence, not full row closure."}, errs,
    ))

    # RT-005 — dangerous-command string matcher (B-016 row-level closure for the listed strings).
    errs = []
    guard_script = source / "skills/misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh"
    if shutil.which("jq") is None:
        errs.append("jq is unavailable on runner")
    dangerous_cases = [
        "git push origin main",
        "git reset --hard HEAD",
        "git clean -fd",
        "git clean -f",
        "git branch -D topic",
        "git checkout .",
        "git restore .",
        "echo push --force",
        "echo reset --hard",
    ]
    case_results: list[dict[str, Any]] = []
    if not errs:
        for command in dangerous_cases:
            payload = json.dumps({"tool_input": {"command": command}})
            rr = run(["bash", str(guard_script)], cwd=source, stdin=payload)
            case_results.append({"input_command": command, "returncode": rr["returncode"], "stderr": rr["stderr"][-1000:]})
            if rr["returncode"] != 2 or "BLOCKED:" not in rr["stderr"]:
                errs.append(f"listed dangerous string was not blocked: {command!r}")
        safe = run(["bash", str(guard_script)], cwd=source, stdin=json.dumps({"tool_input": {"command": "git status"}}))
        if safe["returncode"] != 0:
            errs.append("synthetic safe git status was not allowed")
        # Non-gating diagnostics make the heuristic boundary explicit without broadening B-016.
        false_positive = run(["bash", str(guard_script)], cwd=source, stdin=json.dumps({"tool_input": {"command": "printf 'git push'"}}))
        wrapped_equivalent = run(["bash", str(guard_script)], cwd=source, stdin=json.dumps({"tool_input": {"command": "git -C . push origin main"}}))
    else:
        safe = {"command": [], "returncode": None, "stdout": "", "stderr": ""}
        false_positive = safe
        wrapped_equivalent = safe
    results.append(result_row(
        "RT-005", ["B-016"], ["B-016"], "git guardrail listed-string blocking",
        ["all nine configured dangerous regex patterns are exercised with synthetic strings and exit 2", "git status exits 0"],
        {"cases": case_results, "safe": concise(safe), "non_gating_diagnostics": {"literal_in_non_git_context": concise(false_positive), "wrapped_git_equivalent": concise(wrapped_equivalent)}}, errs,
    ))

    # RT-006 — HITL helper mechanics with synthetic observations only. Supports B-056; no secret-safety closure claimed.
    errs = []
    hitl = source / "skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh"
    hitl_run = run(["bash", str(hitl)], cwd=source, stdin="\ny\nsynthetic error only\n")
    if hitl_run["returncode"] != 0:
        errs.append(f"HITL template exited {hitl_run['returncode']}")
    if "ERRORED=y" not in hitl_run["stdout"] or "ERROR_MSG=synthetic error only" not in hitl_run["stdout"]:
        errs.append("HITL template did not emit captured synthetic observations")
    results.append(result_row(
        "RT-006", ["B-056"], [], "diagnosing-bugs HITL pause/capture mechanics",
        ["synthetic Enter/y/error input completes", "captured observation values are printed in final KEY=VALUE block"],
        {"command": concise(hitl_run), "row_closure_withheld_reason": "This run proves pause/capture mechanics only. B-056 also records that secret-safety is advisory rather than technically enforced; no real or synthetic credential misuse is needed for this smoke pass."}, errs,
    ))

    # Validate test declarations and derive row-level runtime promotions.
    for item in results:
        unknown = sorted(set(item["behavior_ids"] + item["runtime_closure_behavior_ids"]) - behavior_ids)
        if unknown:
            hard_errors.append(f"{item['test_id']}: unknown behavior IDs {unknown}")
        if item["status"] != "PASS":
            hard_errors.append(f"{item['test_id']} failed: {item['errors']}")

    closure_ids = sorted({bid for item in results if item["status"] == "PASS" for bid in item["runtime_closure_behavior_ids"]})
    # This first smoke tranche must close exactly the contracts whose complete
    # matrix claims are directly exercised, and no broader release/harness claim.
    expected_closures = ["B-016", "B-019", "B-020"]
    if closure_ids != expected_closures:
        hard_errors.append(f"unexpected runtime closure set: {closure_ids}, expected {expected_closures}")

    if not hard_errors:
        by_id = {r["behavior_id"]: r for r in matrix["rows"]}
        run_id = os.environ.get("GITHUB_RUN_ID", "local")
        for bid in closure_ids:
            row = by_id[bid]
            row["runtime_observed"] = True
            existing = row.setdefault("runtime_evidence", [])
            test_ids = sorted(item["test_id"] for item in results if bid in item["runtime_closure_behavior_ids"] and item["status"] == "PASS")
            evidence = {
                "evidence_type": "ISOLATED_RUNTIME_SMOKE",
                "test_ids": test_ids,
                "frozen_commit": FROZEN_COMMIT,
                "workflow_run_id": str(run_id),
                "result_file": str(OUT_JSON),
            }
            if evidence not in existing:
                existing.append(evidence)
        MATRIX.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")

    data = {
        "schema_version": 1,
        "source_repo": "mattpocock/skills",
        "frozen_commit": FROZEN_COMMIT,
        "source_checkout_head": source_head,
        "workflow_run_id": str(os.environ.get("GITHUB_RUN_ID", "local")),
        "synthetic_inputs_only": True,
        "user_or_live_repo_touched": False,
        "test_count": len(results),
        "pass_count": sum(1 for r in results if r["status"] == "PASS"),
        "fail_count": sum(1 for r in results if r["status"] == "FAIL"),
        "runtime_closure_behavior_ids": closure_ids,
        "supporting_only_behavior_ids": sorted({bid for r in results for bid in r["behavior_ids"] if bid not in closure_ids}),
        "hard_errors": hard_errors,
        "tests": results,
    }
    OUT_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Phase 4 Runtime Smoke Results",
        "",
        f"Frozen source: `mattpocock/skills` @ `{FROZEN_COMMIT}`.",
        "",
        f"Workflow run: `{data['workflow_run_id']}`.",
        "Synthetic inputs only: **YES**. User/live repository touched: **NO**.",
        "",
        f"Tests: **{data['pass_count']}/{data['test_count']} PASS**; failures: **{data['fail_count']}**.",
        f"Row-level runtime closures: **{', '.join(closure_ids) if closure_ids else 'none'}**.",
        f"Supporting-only behavior evidence: **{', '.join(data['supporting_only_behavior_ids']) if data['supporting_only_behavior_ids'] else 'none'}**.",
        "",
        "| Test | Status | Behavior rows | Row closure | Purpose |",
        "|---|---|---|---|---|",
    ]
    for item in results:
        lines.append(
            f"| {item['test_id']} | {item['status']} | {', '.join(item['behavior_ids'])} | {', '.join(item['runtime_closure_behavior_ids']) or '—'} | {item['title']} |"
        )
    lines += [
        "",
        "## Closure rule",
        "",
        "A PASS may be supporting evidence without closing a behavior row. `runtime_observed=true` is written only for behavior IDs listed in `runtime_closure_behavior_ids`, and this first tranche hard-codes the accepted closure set to B-016/B-019/B-020. B-018 and B-056 remain unpromoted because these smoke tests do not satisfy their entire matrix claims.",
        "",
        f"Hard errors: **{len(hard_errors)}**.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if hard_errors:
        raise SystemExit("Phase 4 runtime smoke failed:\n- " + "\n- ".join(hard_errors))
    print(f"Phase 4 runtime smoke GREEN: {len(results)} tests, closures={closure_ids}")


if __name__ == "__main__":
    main()

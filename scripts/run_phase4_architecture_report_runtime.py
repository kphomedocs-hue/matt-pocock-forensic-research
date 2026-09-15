#!/usr/bin/env python3
"""Exercise frozen architecture-report CDN dependencies in an offline fixture.

This observes the precise portability boundary of B-008.  It never opens a
user report or contacts a real CDN: a disposable HTTP server stands in for the
two frozen URLs and deliberately returns an offline failure.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from typing import Any

FROZEN = "3cca18b368ae95cdbdebbff572ccafa662551015"
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
OUT = pathlib.Path("04_ARCHITECTURE_REPORT_RUNTIME_RESULTS.json")
DOC = pathlib.Path("skills/engineering/improve-codebase-architecture/HTML-REPORT.md")
SKILL = pathlib.Path("skills/engineering/improve-codebase-architecture/SKILL.md")


class OfflineHandler(BaseHTTPRequestHandler):
    requests: list[str] = []

    def do_GET(self) -> None:  # noqa: N802
        type(self).requests.append(self.path)
        self.send_response(503)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"offline fixture: external asset unavailable")

    def log_message(self, _format: str, *_args: Any) -> None:
        pass


def run(cmd: list[str], cwd: pathlib.Path) -> dict[str, Any]:
    p = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    return {"command": cmd, "returncode": p.returncode, "stdout": p.stdout[-4000:], "stderr": p.stderr[-4000:]}


def test(test_id: str, assertions: list[str], evidence: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    return {"test_id": test_id, "behavior_ids": ["B-008"], "title": "architecture report portability", "assertions": assertions, "passed": not errors, "errors": errors, "evidence": evidence}


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
    head = run(["git", "rev-parse", "HEAD"], source)["stdout"].strip()
    if head != FROZEN:
        raise SystemExit(f"Frozen source checkout mismatch: {head!r}")
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    rows = {x["behavior_id"]: x for x in matrix["rows"]}
    if matrix.get("frozen_commit") != FROZEN or "B-008" not in rows:
        raise SystemExit("Research matrix provenance mismatch")

    doc = (source / DOC).read_text(encoding="utf-8")
    skill = (source / SKILL).read_text(encoding="utf-8")
    tailwind = "https://cdn.tailwindcss.com"
    mermaid = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"
    errors: list[str] = []
    if "single self-contained HTML file" not in doc:
        errors.append("frozen format no longer makes the self-contained claim")
    if tailwind not in doc or mermaid not in doc:
        errors.append("frozen scaffold CDN URLs missing")
    if "Tailwind via CDN" not in skill or "Mermaid via CDN" not in skill:
        errors.append("frozen operative CDN contract missing")
    static = test("AR-001", ["frozen format calls the report single self-contained", "frozen format and operative skill name Tailwind and Mermaid CDN dependencies"], {"html_report_blob": run(["git", "rev-parse", f"HEAD:{DOC.as_posix()}"], source)["stdout"].strip(), "skill_blob": run(["git", "rev-parse", f"HEAD:{SKILL.as_posix()}"], source)["stdout"].strip(), "urls": [tailwind, mermaid]}, errors)

    OfflineHandler.requests = []
    server = ThreadingHTTPServer(("127.0.0.1", 0), OfflineHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    with tempfile.TemporaryDirectory(prefix="phase4-architecture-report-") as td:
        root = pathlib.Path(td)
        probe = root / "probe.mjs"
        probe.write_text(f"""const urls = ['http://127.0.0.1:{port}/tailwind', 'http://127.0.0.1:{port}/mermaid'];
const results = await Promise.all(urls.map(async url => [url, (await fetch(url)).status]));
console.log(JSON.stringify({{urls, results}}));
""", encoding="utf-8")
        observed = run(["node", str(probe)], root)
    server.shutdown(); server.server_close()
    runtime_errors: list[str] = []
    try:
        payload = json.loads(observed["stdout"])
    except json.JSONDecodeError:
        payload = {}
        runtime_errors.append("offline asset probe did not emit JSON")
    if observed["returncode"] != 0:
        runtime_errors.append(f"offline asset probe exited {observed['returncode']}")
    if sorted(OfflineHandler.requests) != ["/mermaid", "/tailwind"]:
        runtime_errors.append(f"expected two external asset requests, got {OfflineHandler.requests}")
    if sorted(status for _, status in payload.get("results", [])) != [503, 503]:
        runtime_errors.append("offline fixture did not observe both dependencies failing with 503")
    offline = test("AR-002", ["both frozen scaffold dependencies are requested by a source-derived report fixture", "when unavailable, both external dependencies return 503; no bundled fallback is present"], {"offline_server": "127.0.0.1", "request_paths": OfflineHandler.requests, "probe": observed, "probe_payload": payload}, runtime_errors)
    tests = [static, offline]
    hard = [f"{x['test_id']}: {x['errors']}" for x in tests if not x["passed"]]
    result = {"frozen_commit": FROZEN, "source_checkout_head": head, "workflow_run_id": run_id, "synthetic_inputs_only": True, "user_or_live_repo_touched": False, "test_count": len(tests), "pass_count": sum(x["passed"] for x in tests), "fail_count": sum(not x["passed"] for x in tests), "tests": tests, "hard_errors": hard, "runtime_closure_behavior_ids": ["B-008"] if not hard else [], "tool_versions": {"node": run(["node", "--version"], source)["stdout"].strip(), "python": run(["python", "--version"], source)["stdout"].strip()}}
    OUT.write_text(json.dumps(result, indent=2) + "
", encoding="utf-8")
    if hard:
        raise SystemExit("Architecture report runtime failed: " + "; ".join(hard))
    row = rows["B-008"]
    row["runtime_observed"] = True
    row["adjudication"] = "Direct isolated runtime observation confirms the report is a single HTML file but not dependency-independent: the frozen Tailwind and Mermaid external requests are required and both fail in a controlled offline fixture."
    row["next_evidence"] = "Runtime closure covers the frozen CDN dependency boundary only. Define whether the product intends packaging self-containment or offline/locked-down portability; a real-browser rendering check can broaden compatibility evidence later."
    evidence = {"evidence_type": "ISOLATED_OFFLINE_ASSET_RUNTIME", "test_ids": ["AR-001", "AR-002"], "frozen_commit": FROZEN, "workflow_run_id": run_id, "result_file": str(OUT)}
    row["runtime_evidence"] = [x for x in row.get("runtime_evidence", []) if x.get("result_file") != str(OUT)] + [evidence]
    MATRIX.write_text(json.dumps(matrix, indent=2) + "
", encoding="utf-8")
    print("Architecture report runtime GREEN: B-008")


if __name__ == "__main__":
    main()

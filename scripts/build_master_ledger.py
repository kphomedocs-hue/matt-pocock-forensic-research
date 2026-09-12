#!/usr/bin/env python3
"""Deterministically rebuild the forensic master file ledger from the frozen Git tree.

The frozen source is immutable for Project 01. This script is intentionally small,
standard-library only, and fails closed if the source tree is truncated or its blob
count differs from the manifest denominator.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import urllib.request

SOURCE_REPO = "mattpocock/skills"
FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
FROZEN_TREE = "6e84c093fda2026396cea9fad6a924a6da0e1452"
EXPECTED_BLOBS = 164
LEDGER = pathlib.Path("01_MASTER_FILE_LEDGER.md")
CENSUS_JSON = pathlib.Path("01_FILE_CENSUS.json")


def github_json(url: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "matt-pocock-forensic-research-ledger-builder",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def category(path: str) -> str:
    if path.startswith(".agents/"):
        return "governance"
    if path.startswith(".changeset/"):
        return "changeset"
    if path.startswith(".claude-plugin/"):
        return "distribution"
    if path.startswith(".github/"):
        return "ci-release"
    if path.startswith(".out-of-scope/"):
        return "negative-memory"
    if path.startswith("docs/"):
        return "human-docs"
    if path.startswith("scripts/"):
        return "repo-executable"
    if path.endswith("/agents/openai.yaml"):
        return "codex-metadata"
    if path.endswith("/SKILL.md"):
        return "skill"
    if path.startswith("skills/") and path.endswith("README.md"):
        return "bucket-docs"
    if path.startswith("skills/") and path.endswith((".sh", ".cjs", ".mjs")):
        return "skill-executable-config"
    if path.startswith("skills/"):
        return "skill-support"
    if path == "package-lock.json":
        return "dependency-lock"
    if path == "package.json":
        return "package-config"
    if path in {"README.md", "CLAUDE.md", "CONTEXT.md", "CHANGELOG.md", "LICENSE", "AGENTS.md", ".gitignore"}:
        return "root"
    return "other"


def runtime_risk(path: str, mode: str) -> str:
    if path.startswith(".github/workflows/") or path.startswith(".claude-plugin/"):
        return "HIGH"
    if path in {"package.json", "package-lock.json"} or path.startswith("scripts/"):
        return "HIGH"
    if mode == "100755" or path.endswith((".sh", ".cjs", ".mjs")):
        return "HIGH"
    if path.endswith("/agents/openai.yaml") or path.endswith("/SKILL.md") or path.startswith(".agents/"):
        return "MEDIUM"
    return "LOW"


def esc(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def load_existing_rows() -> dict[str, dict[str, str]]:
    """Preserve manually promoted status/evidence fields across regeneration."""
    if not LEDGER.exists():
        return {}
    rows: dict[str, dict[str, str]] = {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\| MP-\d{4} \|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 12:
            continue
        mp_id, path, mode_type, size, sha, cat, status, evidence, ref_out, ref_in, risk, notes = cells
        rows[path] = {
            "status": status,
            "evidence": evidence,
            "ref_out": ref_out,
            "ref_in": ref_in,
            "risk": risk,
            "notes": notes,
        }
    return rows


def main() -> None:
    url = f"https://api.github.com/repos/{SOURCE_REPO}/git/trees/{FROZEN_TREE}?recursive=1"
    tree = github_json(url)
    if tree.get("sha") != FROZEN_TREE:
        raise SystemExit(f"Wrong tree returned: {tree.get('sha')}")
    if tree.get("truncated"):
        raise SystemExit("GitHub returned a truncated recursive tree; refusing to build an incomplete ledger")

    blobs = sorted((item for item in tree["tree"] if item.get("type") == "blob"), key=lambda item: item["path"])
    if len(blobs) != EXPECTED_BLOBS:
        raise SystemExit(f"Expected {EXPECTED_BLOBS} blobs, got {len(blobs)}")

    previous = load_existing_rows()
    census = {
        "source_repo": SOURCE_REPO,
        "frozen_commit": FROZEN_COMMIT,
        "frozen_tree": FROZEN_TREE,
        "blob_count": len(blobs),
        "truncated": False,
        "files": [],
    }

    lines = [
        "# Master File Ledger",
        "",
        f"Source: frozen recursive tree of `{SOURCE_REPO}` at commit `{FROZEN_COMMIT}`, tree `{FROZEN_TREE}`.",
        "",
        f"Physical denominator: **{len(blobs)} blobs/files**.",
        "",
        "Generated deterministically by `scripts/build_master_ledger.py`. MP-IDs are assigned in lexicographic path order. Regeneration preserves manually recorded status/evidence fields by path.",
        "",
        "## Status rules",
        "",
        "`UNREAD → READ → CONNECTIONS TRACED → VERIFIED`",
        "",
        "A status transition requires durable evidence. A conversation summary is not evidence.",
        "",
        "## Ledger",
        "",
        "| MP-ID | Path | Mode/Type | Size | Blob SHA | Category | Status | Evidence | Ref-out | Ref-in | Runtime Risk | Notes |",
        "|---|---|---|---:|---|---|---|---|---|---|---|---|",
    ]

    for index, item in enumerate(blobs, start=1):
        path = item["path"]
        mp_id = f"MP-{index:04d}"
        prev = previous.get(path, {})
        status = prev.get("status", "UNREAD")
        evidence = prev.get("evidence", "")
        ref_out = prev.get("ref_out", "")
        ref_in = prev.get("ref_in", "")
        risk = prev.get("risk") or runtime_risk(path, item["mode"])
        notes = prev.get("notes", "")
        if item["mode"] == "120000" and not notes:
            notes = "Git symlink blob; logical target must be reconciled separately."
        cat = category(path)
        mode_type = f"{item['mode']}/blob"
        size = item.get("size", "")
        sha = item["sha"]
        values = [mp_id, path, mode_type, size, sha, cat, status, evidence, ref_out, ref_in, risk, notes]
        lines.append("| " + " | ".join(esc(v) for v in values) + " |")
        census["files"].append({
            "mp_id": mp_id,
            "path": path,
            "mode": item["mode"],
            "type": "blob",
            "size": size,
            "sha": sha,
            "category": cat,
            "runtime_risk": risk,
        })

    LEDGER.write_text("\n".join(lines) + "\n", encoding="utf-8")
    CENSUS_JSON.write_text(json.dumps(census, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(f"Wrote {LEDGER} and {CENSUS_JSON} with {len(blobs)} frozen blobs")


if __name__ == "__main__":
    main()

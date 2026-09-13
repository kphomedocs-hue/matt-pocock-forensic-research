#!/usr/bin/env python3
"""Bind durable history IDs to current frozen files by exact commit/PR changed paths.

This is a connection-mapping join, not a claim that every changed file's full
history is reconciled. Each binding inherits the durable H-entry lineage state.
"""
from __future__ import annotations

import json
import os
import pathlib
import urllib.request
from collections import defaultdict

SOURCE_REPO = "mattpocock/skills"
FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
OUT_JSON = pathlib.Path("03_HISTORY_BINDINGS.json")
OUT_MD = pathlib.Path("03_HISTORY_BINDINGS.md")

EVENTS = [
    {
        "id": "H-001",
        "state": "RECONCILED",
        "area": "Changesets / package metadata",
        "refs": [("commit", "a0324014864317489b5958bf632d7ec8dbccbdcd")],
    },
    {
        "id": "H-002",
        "state": "RECONCILED",
        "area": "TDD red-green lineage",
        "refs": [
            ("commit", "e81f97660af0bebfdbf2e23db6a71f7dfcb9a659"),
            ("commit", "80e9dcc6857f16cc08b8e5b190393ee7591517e0"),
        ],
    },
    {
        "id": "H-003",
        "state": "PARTIAL",
        "area": "Claude plugin creation",
        "refs": [("commit", "42a5b70fcacc7baff1977b13f3919fb2f63af14e")],
    },
    {
        "id": "H-004",
        "state": "PARTIAL",
        "area": "Codex metadata introduction",
        "refs": [("commit", "697d4ce9742da558fd1ba6697c8e9775e2e302dd")],
    },
    {
        "id": "H-005",
        "state": "RECONCILED",
        "area": "Router/docs coherence pass",
        "refs": [("commit", "8a475c438d90a2f1d7d3710c12658b60dc701a13")],
    },
    {
        "id": "H-006",
        "state": "RECONCILED",
        "area": "Release version synchronization",
        "refs": [("commit", "f3554acafee0f1549d3f8f7881eca0634fd446d0")],
    },
    {
        "id": "H-007",
        "state": "RECONCILED",
        "area": "Cross-skill invocation standardization",
        "refs": [("pr", "878")],
    },
    {
        "id": "H-008",
        "state": "RECONCILED",
        "area": "Cross-skill invocation regression fix",
        "refs": [("pr", "880")],
    },
    {
        "id": "H-009",
        "state": "PARTIAL",
        "area": "Local-link misc exclusion",
        "refs": [("pr", "1025")],
    },
]


def request_json(url: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "matt-pocock-forensic-history-bindings",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def commit_files(sha: str) -> list[str]:
    data = request_json(f"https://api.github.com/repos/{SOURCE_REPO}/commits/{sha}")
    return [item["filename"] for item in data.get("files", [])]


def pr_files(number: str) -> list[str]:
    paths: list[str] = []
    page = 1
    while True:
        data = request_json(
            f"https://api.github.com/repos/{SOURCE_REPO}/pulls/{number}/files?per_page=100&page={page}"
        )
        paths.extend(item["filename"] for item in data)
        if len(data) < 100:
            break
        page += 1
    return paths


def main() -> None:
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    if census.get("frozen_commit") != FROZEN_COMMIT or census.get("blob_count") != EXPECTED_FILES:
        raise SystemExit("Frozen census mismatch; refusing history binding build")

    current = {item["path"]: item for item in census["files"]}
    by_file: dict[str, list[dict]] = defaultdict(list)
    event_rows = []

    for event in EVENTS:
        changed: set[str] = set()
        refs = []
        for ref_type, ref in event["refs"]:
            paths = commit_files(ref) if ref_type == "commit" else pr_files(ref)
            changed.update(paths)
            refs.append({"type": ref_type, "ref": ref, "changed_file_count": len(paths)})

        current_paths = sorted(path for path in changed if path in current)
        historical_only = sorted(path for path in changed if path not in current)
        bindings = []
        for path in current_paths:
            binding = {
                "history_id": event["id"],
                "lineage_state": event["state"],
                "area": event["area"],
                "mp_id": current[path]["mp_id"],
                "path": path,
                "binding_basis": "CHANGED_IN_EXACT_EVENT_EVIDENCE",
            }
            bindings.append(binding)
            by_file[path].append(binding)

        event_rows.append({
            "history_id": event["id"],
            "lineage_state": event["state"],
            "area": event["area"],
            "refs": refs,
            "changed_paths_total": len(changed),
            "current_frozen_bindings": bindings,
            "historical_only_paths": historical_only,
        })

    file_rows = []
    for path, item in sorted(current.items(), key=lambda pair: pair[1]["mp_id"]):
        bindings = sorted(by_file.get(path, []), key=lambda b: b["history_id"])
        file_rows.append({
            "mp_id": item["mp_id"],
            "path": path,
            "history_bindings": bindings,
            "history_binding_count": len(bindings),
            "has_partial_history_binding": any(b["lineage_state"] == "PARTIAL" for b in bindings),
        })

    payload = {
        "source_repo": SOURCE_REPO,
        "frozen_commit": FROZEN_COMMIT,
        "file_count": len(current),
        "history_event_count": len(EVENTS),
        "events": event_rows,
        "files_with_history_bindings": sum(1 for row in file_rows if row["history_binding_count"]),
        "binding_count": sum(row["history_binding_count"] for row in file_rows),
        "file_rows": file_rows,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Phase 3 History Bindings",
        "",
        f"Frozen source: `{SOURCE_REPO}` @ `{FROZEN_COMMIT}`.",
        "",
        "Bindings are generated by intersecting the exact changed-file set of each durable H-entry's commit/PR evidence with the current 164-file frozen census.",
        "",
        "A binding means **this current file was changed by that historical event**. It does not upgrade a `PARTIAL` history entry to reconciled and does not by itself prove complete lineage for the file.",
        "",
        f"History entries bound: **{len(EVENTS)}**. Current files with one or more history bindings: **{payload['files_with_history_bindings']}**. Total current-file bindings: **{payload['binding_count']}**.",
        "",
        "## Event summary",
        "",
        "| History ID | State | Area | Changed paths | Current frozen bindings | Historical-only paths |",
        "|---|---|---|---:|---:|---:|",
    ]
    for event in event_rows:
        lines.append(
            f"| {event['history_id']} | {event['lineage_state']} | {event['area']} | "
            f"{event['changed_paths_total']} | {len(event['current_frozen_bindings'])} | {len(event['historical_only_paths'])} |"
        )

    lines += ["", "## Current-file bindings", "", "| MP-ID | Path | History bindings |", "|---|---|---|"]
    for row in file_rows:
        if not row["history_bindings"]:
            continue
        refs = ", ".join(
            f"{b['history_id']} ({b['lineage_state']})" for b in row["history_bindings"]
        )
        lines.append(f"| {row['mp_id']} | `{row['path']}` | {refs} |")

    lines += ["", "## Partial-lineage caution", ""]
    partial = [event for event in event_rows if event["lineage_state"] == "PARTIAL"]
    for event in partial:
        lines.append(
            f"- **{event['history_id']}** remains PARTIAL. Its exact event-to-file bindings are known, but later evolution/current lineage is not yet fully reconciled."
        )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"history events={len(EVENTS)} files_with_bindings={payload['files_with_history_bindings']} "
        f"bindings={payload['binding_count']}"
    )


if __name__ == "__main__":
    main()

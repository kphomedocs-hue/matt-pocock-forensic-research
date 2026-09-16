#!/usr/bin/env python3
"""Bind durable history-ledger events to current frozen files.

The Markdown history ledger is the human-authored source of truth for H-ID, area,
lineage state, and exact commit/PR evidence. This builder parses those fields rather
than duplicating them in Python, then intersects each exact event's changed-file set
with the current 164-file frozen census.

A binding means a current file was changed by that event. It does not upgrade a
PARTIAL lineage entry to RECONCILED and does not prove complete history for a file.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import urllib.request
from collections import defaultdict

SOURCE_REPO = "mattpocock/skills"
FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164
EXPECTED_HISTORY_EVENTS = 10
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
HISTORY_LEDGER = pathlib.Path("05_HISTORY_LEDGER.md")
OUT_JSON = pathlib.Path("03_HISTORY_BINDINGS.json")
OUT_MD = pathlib.Path("03_HISTORY_BINDINGS.md")


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


def parse_history_ledger() -> list[dict]:
    if not HISTORY_LEDGER.exists():
        raise SystemExit(f"Missing durable history ledger: {HISTORY_LEDGER}")

    events: list[dict] = []
    seen: set[str] = set()
    for line in HISTORY_LEDGER.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\| H-\d{3} \|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            raise SystemExit(f"Cannot parse history ledger row: {line}")
        history_id, date, area, event_text, evidence, significance, state = cells
        if history_id in seen:
            raise SystemExit(f"Duplicate history ID in ledger: {history_id}")
        seen.add(history_id)
        if state not in {"RECONCILED", "PARTIAL", "NOT MATERIAL"}:
            raise SystemExit(f"Invalid history lineage state for {history_id}: {state}")

        # Exact provenance may be stated in either the Event or Evidence
        # column. Both are durable ledger fields, so parse their union.
        exact_evidence = f"{event_text} {evidence}"
        prs = sorted(set(re.findall(r"PR\s+#(\d+)", exact_evidence, flags=re.IGNORECASE)))
        commits = sorted(set(re.findall(r"\b[0-9a-f]{40}\b", exact_evidence)))
        # Blob identifiers prove frozen-file identity but are not API commit
        # references. Keep them out of the event changed-file query.
        blob_shas = set(re.findall(r"\bblob SHA\s+\`?([0-9a-f]{40})", exact_evidence, flags=re.IGNORECASE))
        commits = [sha for sha in commits if sha not in blob_shas]

        # When a PR is named, use the PR changed-file set as the event boundary.
        # Merge/commit SHAs in the same evidence cell are supporting provenance,
        # not a second event whose changed paths should be unioned again.
        if prs:
            refs = [("pr", number) for number in prs]
        else:
            refs = [("commit", sha) for sha in commits]
        if not refs:
            raise SystemExit(f"History row {history_id} has no exact PR or 40-char commit evidence")

        events.append({
            "id": history_id,
            "date": date,
            "state": state,
            "area": area,
            "event": event_text,
            "significance": significance,
            "refs": refs,
        })

    if len(events) != EXPECTED_HISTORY_EVENTS:
        raise SystemExit(
            f"Expected {EXPECTED_HISTORY_EVENTS} durable history events, parsed {len(events)}"
        )
    expected_ids = {f"H-{i:03d}" for i in range(1, EXPECTED_HISTORY_EVENTS + 1)}
    if {event["id"] for event in events} != expected_ids:
        raise SystemExit("Durable history ID set is not the expected contiguous H-001..H-010 set")
    return events


def main() -> None:
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    if census.get("frozen_commit") != FROZEN_COMMIT or census.get("blob_count") != EXPECTED_FILES:
        raise SystemExit("Frozen census mismatch; refusing history binding build")

    events = parse_history_ledger()
    current = {item["path"]: item for item in census["files"]}
    by_file: dict[str, list[dict]] = defaultdict(list)
    event_rows = []

    for event in events:
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
            "date": event["date"],
            "lineage_state": event["state"],
            "area": event["area"],
            "event": event["event"],
            "current_significance": event["significance"],
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
        "history_definition_source": str(HISTORY_LEDGER),
        "file_count": len(current),
        "history_event_count": len(events),
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
        f"History definitions are parsed directly from `{HISTORY_LEDGER}`; H-ID, area, lineage state, and exact PR/commit evidence are not duplicated in this builder.",
        "",
        "Bindings are generated by intersecting the exact changed-file set of each durable H-entry's event evidence with the current 164-file frozen census.",
        "",
        "A binding means **this current file was changed by that historical event**. It does not upgrade a `PARTIAL` history entry to reconciled and does not by itself prove complete lineage for the file.",
        "",
        f"History entries bound: **{len(events)}**. Current files with one or more history bindings: **{payload['files_with_history_bindings']}**. Total current-file bindings: **{payload['binding_count']}**.",
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
        f"history events={len(events)} files_with_bindings={payload['files_with_history_bindings']} "
        f"bindings={payload['binding_count']} source={HISTORY_LEDGER}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Promote all frozen file notes from READ to CONNECTIONS TRACED, fail-closed.

Promotion is allowed only when the generated Phase 3 closure index has 164/164
READY_CANDIDATE and no blockers. Each note receives a durable per-file evidence
block derived from that closure row. This script never promotes to VERIFIED.
"""
from __future__ import annotations

import json
import pathlib
import re

FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164
EXPECTED_GRAPH_RULES_MIN = 4

CENSUS = pathlib.Path("01_FILE_CENSUS.json")
GRAPH = pathlib.Path("03_CONNECTION_EDGES.json")
CLOSURE = pathlib.Path("03_PHASE3_CLOSURE_INDEX.json")
NOTES_DIR = pathlib.Path("02_FILE_NOTES")

START = "<!-- PHASE3_CONNECTIONS_TRACED_START -->"
END = "<!-- PHASE3_CONNECTIONS_TRACED_END -->"

STATUS_RE = re.compile(
    r"^(?P<prefix>-\s*)?Status:\s*(?P<bold>\*\*)?(?P<status>READ|CONNECTIONS TRACED|VERIFIED)(?P=bold)?\s*$",
    re.MULTILINE,
)
COMMIT_RE = re.compile(r"^(?:-\s*)?Frozen commit:\s*`([0-9a-f]{40})`\s*$", re.MULTILINE)
BLOB_RE = re.compile(
    r"^(?:-\s*)?(?:Frozen\s+)?Blob SHA:\s*`?([0-9a-f]{40})`?\s*$",
    re.MULTILINE | re.IGNORECASE,
)


def load(path: pathlib.Path):
    if not path.exists():
        raise SystemExit(f"Required promotion input missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def strip_existing_block(text: str) -> str:
    if START not in text and END not in text:
        return text.rstrip()
    if text.count(START) != 1 or text.count(END) != 1:
        raise SystemExit("Malformed existing Phase 3 evidence marker block")
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    return (before.rstrip() + "\n" + after.lstrip()).rstrip()


def main() -> None:
    census = load(CENSUS)
    graph = load(GRAPH)
    closure = load(CLOSURE)

    for label, obj in [("census", census), ("graph", graph), ("closure", closure)]:
        if obj.get("frozen_commit") != FROZEN_COMMIT:
            raise SystemExit(f"{label} frozen commit mismatch")

    if census.get("blob_count") != EXPECTED_FILES:
        raise SystemExit("Census denominator mismatch")
    if graph.get("file_count") != EXPECTED_FILES:
        raise SystemExit("Graph denominator mismatch")
    if graph.get("extraction_rules_version", 0) < EXPECTED_GRAPH_RULES_MIN:
        raise SystemExit("Graph extraction rules are older than the Phase 3 promotion gate")
    if graph.get("invocation_policy_mismatch_count") != 0:
        raise SystemExit("Invocation policy mismatch blocks promotion")
    if graph.get("illegal_operative_call_count") != 0:
        raise SystemExit("Illegal operative call blocks promotion")
    if closure.get("file_count") != EXPECTED_FILES:
        raise SystemExit("Closure-index denominator mismatch")
    if closure.get("state_counts") != {"READY_CANDIDATE": EXPECTED_FILES}:
        raise SystemExit(f"Closure index is not 164/164 ready: {closure.get('state_counts')}")
    if closure.get("blocker_counts"):
        raise SystemExit(f"Closure blockers remain: {closure.get('blocker_counts')}")

    census_by_id = {row["mp_id"]: row for row in census["files"]}
    closure_by_id = {row["mp_id"]: row for row in closure["rows"]}
    if len(census_by_id) != EXPECTED_FILES or len(closure_by_id) != EXPECTED_FILES:
        raise SystemExit("Duplicate or missing MP-IDs in promotion inputs")
    if set(census_by_id) != set(closure_by_id):
        raise SystemExit("Census/closure MP-ID sets differ")

    changed = 0
    for mp_id in sorted(census_by_id):
        census_row = census_by_id[mp_id]
        closure_row = closure_by_id[mp_id]
        if closure_row.get("path") != census_row.get("path"):
            raise SystemExit(f"Path mismatch for {mp_id}")
        if closure_row.get("phase3_gate_state") != "READY_CANDIDATE" or closure_row.get("blockers"):
            raise SystemExit(f"Per-file closure not ready for {mp_id}")

        note_path = NOTES_DIR / f"{mp_id}.md"
        if not note_path.exists():
            raise SystemExit(f"Missing durable note: {note_path}")
        original = note_path.read_text(encoding="utf-8")

        commit_match = COMMIT_RE.search(original)
        blob_match = BLOB_RE.search(original)
        status_match = STATUS_RE.search(original)
        if not commit_match or commit_match.group(1) != FROZEN_COMMIT:
            raise SystemExit(f"Frozen commit provenance mismatch in {note_path}")
        if not blob_match or blob_match.group(1) != census_row.get("sha"):
            raise SystemExit(f"Blob SHA provenance mismatch in {note_path}")
        if not status_match:
            raise SystemExit(f"Missing/invalid durable Status line in {note_path}")
        old_status = status_match.group("status")
        if old_status == "VERIFIED":
            raise SystemExit(f"Refusing to overwrite later VERIFIED status in {note_path}")

        text = strip_existing_block(original)
        match = STATUS_RE.search(text)
        if not match:
            raise SystemExit(f"Status line disappeared while normalizing {note_path}")
        prefix = match.group("prefix") or ""
        replacement = f"{prefix}Status: **CONNECTIONS TRACED**"
        text = text[:match.start()] + replacement + text[match.end():]

        d = closure_row["dimensions"]
        evidence = [
            START,
            "## Phase 3 connection promotion evidence",
            "",
            "- Status promotion: `CONNECTIONS TRACED`.",
            f"- Frozen source: `{FROZEN_COMMIT}` / blob `{census_row['sha']}`.",
            f"- Phase 3 closure row: `{mp_id}` in `03_PHASE3_CLOSURE_INDEX.json`; gate state `READY_CANDIDATE` with zero blockers.",
            f"- Connection graph extraction rules version: `{graph['extraction_rules_version']}`.",
            f"- Incoming graph edges: **{d['incoming_edge_count']}**; outgoing graph edges: **{d['outgoing_edge_count']}**.",
            f"- Orphan evaluation: `{d['orphan_state']}`; closed: **{'YES' if d['orphan_closed'] else 'NO'}**.",
            f"- Raw unresolved references originating here: **{d['raw_unresolved_count']}**; all applicable raw references reconciled: **{'YES' if d['raw_unresolved_reconciled'] else 'NO'}**.",
            "- Applicable Phase 3 joins (config/distribution/router/invocation/symlink) are enforced by the generated closure index; history bindings are recorded separately and do not imply later-phase verification.",
            "- `CONNECTIONS TRACED` does **not** mean `VERIFIED`; behavior/enforcement, remaining history lineage, contradictions, runtime/distribution observation, second pass, and red-team verification remain later gates where applicable.",
            END,
        ]
        updated = text.rstrip() + "\n\n" + "\n".join(evidence) + "\n"
        if updated != original:
            note_path.write_text(updated, encoding="utf-8")
            changed += 1

    print(f"Phase 3 promotion evidence applied: {changed} note file(s) changed; denominator={EXPECTED_FILES}")


if __name__ == "__main__":
    main()

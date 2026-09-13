#!/usr/bin/env python3
"""Apply an ephemeral Phase 4 batch into the authoritative matrix/register.

The batch file is deleted after a successful merge, so durable truth remains in
04_BEHAVIOR_MATRIX.json and 04_CONTRADICTION_REGISTER.md only.
"""
from __future__ import annotations

import json
import pathlib
import re

BATCH = pathlib.Path("04_PHASE4_BATCH.json")
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
REGISTER = pathlib.Path("04_CONTRADICTION_REGISTER.md")
FROZEN = "3cca18b368ae95cdbdebbff572ccafa662551015"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main() -> None:
    if not BATCH.exists():
        raise SystemExit("Missing 04_PHASE4_BATCH.json")
    batch = load(BATCH)
    matrix = load(MATRIX)
    register = REGISTER.read_text(encoding="utf-8")

    if batch.get("frozen_commit") != FROZEN or matrix.get("frozen_commit") != FROZEN:
        raise SystemExit("Frozen commit mismatch")

    existing_cts = set(re.findall(r"^\| (CT-\d{3}) \|", register, re.MULTILINE))
    existing_overlay = set(re.findall(r"^\| ↳ (CT-\d{3}) \|", register, re.MULTILINE))
    new_cts = batch.get("contradictions", [])
    new_ct_ids = [c["id"] for c in new_cts]
    if len(new_ct_ids) != len(set(new_ct_ids)):
        raise SystemExit("Duplicate CT IDs in batch")
    if any(ct in existing_cts or ct in existing_overlay for ct in new_ct_ids):
        raise SystemExit("Batch CT already exists in register")

    # Require sequential CT numbering against current register.
    current_nums = sorted(int(ct.split("-")[1]) for ct in existing_cts)
    start = (current_nums[-1] + 1) if current_nums else 1
    expected_cts = [f"CT-{i:03d}" for i in range(start, start + len(new_ct_ids))]
    if new_ct_ids != expected_cts:
        raise SystemExit(f"Expected CT IDs {expected_cts}, got {new_ct_ids}")

    current_rows = []
    overlay_rows = []
    for c in new_cts:
        current_rows.append(
            f"| {c['id']} | {esc(c['area'])} | {esc(c['evidence_a'])} | {esc(c['evidence_b'])} | "
            f"{esc(c['classification'])} | {esc(c.get('status', 'OPEN'))} | {esc(c['notes'])} |"
        )
        overlay_rows.append(
            f"| ↳ {c['id']} | {esc(c.get('origin', 'SOURCE_REPO'))} | {esc(c['defect_state'])} | "
            f"{esc(c['impact'])} | {esc(c['resolution_test'])} |"
        )

    if current_rows:
        marker = "\n## Normalized closure overlay"
        if marker not in register:
            raise SystemExit("Contradiction register missing closure overlay marker")
        register = register.replace(marker, "\n" + "\n".join(current_rows) + "\n" + marker, 1)

        hist_marker = "\n## Resolved historical defects retained for pattern analysis"
        if hist_marker not in register:
            raise SystemExit("Contradiction register missing historical marker")
        register = register.replace(hist_marker, "\n" + "\n".join(overlay_rows) + "\n" + hist_marker, 1)

    rows = matrix.get("rows", [])
    existing_bids = [r["behavior_id"] for r in rows]
    additions = batch.get("behavior_rows", [])
    addition_ids = [r["behavior_id"] for r in additions]
    if len(addition_ids) != len(set(addition_ids)):
        raise SystemExit("Duplicate behavior IDs in batch")
    if any(bid in existing_bids for bid in addition_ids):
        raise SystemExit("Batch behavior ID already exists")

    next_num = len(rows) + 1
    expected_bids = [f"B-{i:03d}" for i in range(next_num, next_num + len(additions))]
    if addition_ids != expected_bids:
        raise SystemExit(f"Expected behavior IDs {expected_bids}, got {addition_ids}")

    all_cts_after = existing_cts | set(new_ct_ids)
    for row in additions:
        missing = sorted(set(row.get("contradiction_ids", [])) - all_cts_after)
        if missing:
            raise SystemExit(f"{row['behavior_id']} references missing CTs: {missing}")
        for key in ("area", "claim", "adjudication", "next_evidence"):
            if not row.get(key):
                raise SystemExit(f"{row['behavior_id']} missing {key}")

    matrix["rows"] = rows + additions
    MATRIX.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
    REGISTER.write_text(register, encoding="utf-8")
    BATCH.unlink()
    print(f"Applied Phase 4 batch: CTs={len(new_cts)}, behaviors={len(additions)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Populate master-ledger Ref-out / Ref-in columns from the current Phase 3 graph.

The Phase 1 ledger remains the physical inventory authority; this enrichment changes
only its two Phase 3 reference-count columns. It never changes MP-IDs, source paths,
blob provenance, category, status, evidence, runtime risk, or notes.
"""
from __future__ import annotations

import json
import pathlib
import re
from collections import Counter

FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164
LEDGER = pathlib.Path("01_MASTER_FILE_LEDGER.md")
GRAPH = pathlib.Path("03_CONNECTION_EDGES.json")


def main() -> None:
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    if graph.get("frozen_commit") != FROZEN_COMMIT or graph.get("file_count") != EXPECTED_FILES:
        raise SystemExit("Connection graph baseline mismatch; refusing ledger enrichment")

    outgoing = Counter(edge["from"] for edge in graph.get("edges", []))
    incoming = Counter(edge["to"] for edge in graph.get("edges", []))

    text = LEDGER.read_text(encoding="utf-8")
    lines = text.splitlines()
    changed_rows = 0
    seen_rows = 0
    out = []
    for line in lines:
        if not re.match(r"^\| MP-\d{4} \|", line):
            out.append(line)
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 12:
            raise SystemExit(f"Unexpected master-ledger row shape: {line}")
        seen_rows += 1
        path = cells[1]
        new_out = str(outgoing[path])
        new_in = str(incoming[path])
        if cells[8] != new_out or cells[9] != new_in:
            cells[8] = new_out
            cells[9] = new_in
            changed_rows += 1
        out.append("| " + " | ".join(cells) + " |")

    if seen_rows != EXPECTED_FILES:
        raise SystemExit(f"Expected {EXPECTED_FILES} ledger rows, found {seen_rows}")

    marker = "Generated deterministically by `scripts/build_master_ledger.py`. MP-IDs are assigned in lexicographic path order. Durable per-file notes under `02_FILE_NOTES/` are authoritative for READ-or-higher status."
    enriched = marker + " Ref-out / Ref-in are derived from the current `03_CONNECTION_EDGES.json` by `scripts/enrich_master_ledger_connections.py`."
    joined = "\n".join(out) + "\n"
    if marker in joined and enriched not in joined:
        joined = joined.replace(marker, enriched, 1)

    LEDGER.write_text(joined, encoding="utf-8")
    print(f"master ledger connection enrichment: rows={seen_rows} changed={changed_rows} graph_edges={graph.get('edge_count')}")


if __name__ == "__main__":
    main()

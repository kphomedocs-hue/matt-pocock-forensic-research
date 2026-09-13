#!/usr/bin/env python3
"""Create a deterministic SHA-256 manifest for authoritative Phase 3 state.

The manifest fingerprints all local inputs that define the Phase 3 generated-state
pipeline and acceptance gate, plus the resulting authoritative artifacts. It contains
no timestamp so an unchanged build is byte-for-byte reproducible.
"""
from __future__ import annotations

import hashlib
import json
import pathlib

FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
OUT_JSON = pathlib.Path("03_PHASE3_BUILD_MANIFEST.json")
OUT_MD = pathlib.Path("03_PHASE3_BUILD_MANIFEST.md")

INPUTS = [
    "01_FILE_CENSUS.json",
    "05_HISTORY_LEDGER.md",
    "03_REFERENCE_DISPOSITIONS.json",
    "03_ORPHAN_DISPOSITIONS.json",
    "scripts/build_connection_graph.py",
    "scripts/build_router_matrix.py",
    "scripts/build_distribution_matrix.py",
    "scripts/build_history_bindings.py",
    "scripts/build_phase3_closure_index.py",
    "scripts/enrich_master_ledger_connections.py",
    "scripts/build_phase3_manifest.py",
    "scripts/verify_phase3_manifest.py",
    "scripts/validate_phase3_quality.py",
    ".github/workflows/rebuild-phase3-state.yml",
]

OUTPUTS = [
    "01_MASTER_FILE_LEDGER.md",
    "03_CONNECTION_EDGES.json",
    "03_CONNECTION_INDEX.md",
    "03_ROUTER_MATRIX.json",
    "03_ROUTER_MATRIX.md",
    "03_DISTRIBUTION_MATRIX.json",
    "03_DISTRIBUTION_MATRIX.md",
    "03_HISTORY_BINDINGS.json",
    "03_HISTORY_BINDINGS.md",
    "03_PHASE3_CLOSURE_INDEX.json",
    "03_PHASE3_CLOSURE_INDEX.md",
]


def sha256(path: pathlib.Path) -> str:
    if not path.exists() or path.stat().st_size == 0:
        raise SystemExit(f"Manifest dependency missing/empty: {path}")
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fingerprint(paths: list[str]) -> dict[str, dict[str, object]]:
    result = {}
    for raw in paths:
        path = pathlib.Path(raw)
        result[raw] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    return result


def main() -> None:
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    if census.get("frozen_commit") != FROZEN_COMMIT or census.get("blob_count") != EXPECTED_FILES:
        raise SystemExit("Frozen census mismatch; refusing Phase 3 manifest build")

    payload = {
        "schema_version": 1,
        "source_repo": "mattpocock/skills",
        "frozen_commit": FROZEN_COMMIT,
        "frozen_tree": census.get("frozen_tree"),
        "physical_file_count": EXPECTED_FILES,
        "input_fingerprints": fingerprint(INPUTS),
        "output_fingerprints": fingerprint(OUTPUTS),
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Phase 3 Build Manifest",
        "",
        f"Frozen source: `mattpocock/skills` @ `{FROZEN_COMMIT}`.",
        "",
        "This manifest cryptographically binds the authoritative Phase 3 generator and acceptance-gate inputs to the generated outputs using SHA-256. It intentionally contains no timestamp so unchanged state is reproducible byte-for-byte.",
        "",
        f"Inputs fingerprinted: **{len(INPUTS)}**. Outputs fingerprinted: **{len(OUTPUTS)}**.",
        "",
        "## Inputs",
        "",
        "| Path | SHA-256 | Bytes |",
        "|---|---|---:|",
    ]
    for path, meta in payload["input_fingerprints"].items():
        lines.append(f"| `{path}` | `{meta['sha256']}` | {meta['bytes']} |")
    lines += ["", "## Outputs", "", "| Path | SHA-256 | Bytes |", "|---|---|---:|"]
    for path, meta in payload["output_fingerprints"].items():
        lines.append(f"| `{path}` | `{meta['sha256']}` | {meta['bytes']} |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"phase3 manifest: inputs={len(INPUTS)} outputs={len(OUTPUTS)}")


if __name__ == "__main__":
    main()

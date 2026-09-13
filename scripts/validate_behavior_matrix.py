#!/usr/bin/env python3
"""Validate and render the Phase 4 behavior/enforcement matrix.

The JSON matrix is the structured working source. This validator fails closed on
unknown MP/CT references, uncovered current CTs, duplicate IDs, invalid enforcement
labels, or frozen-source drift, then renders a deterministic Markdown view and
integrity report.
"""
from __future__ import annotations

import json
import pathlib
import re
from collections import Counter

FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
CONTRADICTIONS = pathlib.Path("04_CONTRADICTION_REGISTER.md")
OUT_MD = pathlib.Path("04_BEHAVIOR_MATRIX.md")
OUT_INTEGRITY = pathlib.Path("04_BEHAVIOR_INTEGRITY.json")


def load(path: pathlib.Path):
    if not path.exists():
        raise SystemExit(f"Missing required input: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def esc(text: object) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def main() -> None:
    matrix = load(MATRIX)
    census = load(CENSUS)
    ct_text = CONTRADICTIONS.read_text(encoding="utf-8")

    errors: list[str] = []
    if matrix.get("frozen_commit") != FROZEN_COMMIT:
        errors.append("Behavior matrix frozen commit mismatch")
    if census.get("frozen_commit") != FROZEN_COMMIT:
        errors.append("Census frozen commit mismatch")
    if census.get("blob_count") != EXPECTED_FILES or len(census.get("files", [])) != EXPECTED_FILES:
        errors.append("Census denominator is not 164")
    if matrix.get("phase") != 4:
        errors.append("Behavior matrix phase must be 4")

    allowed_layers = set(matrix.get("allowed_layers", []))
    allowed_states = set(matrix.get("allowed_states", []))
    if not allowed_layers or not allowed_states:
        errors.append("Allowed layer/state vocabularies must be non-empty")

    census_ids = {row["mp_id"] for row in census.get("files", [])}
    ct_ids = set(re.findall(r"^\| (CT-\d{3}) \|", ct_text, re.MULTILINE))
    rows = matrix.get("rows", [])
    ids = [row.get("behavior_id") for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate behavior IDs")
    expected_ids = [f"B-{i:03d}" for i in range(1, len(rows) + 1)]
    if ids != expected_ids:
        errors.append(f"Behavior IDs must be ordered/contiguous: expected {expected_ids}, got {ids}")

    layer_counts = Counter()
    state_counts = Counter()
    ct_refs = Counter()
    machine_counts = Counter()
    runtime_observed_count = 0

    for row in rows:
        bid = row.get("behavior_id", "<missing>")
        missing_mp = sorted(set(row.get("source_mp_ids", [])) - census_ids)
        if missing_mp:
            errors.append(f"{bid}: unknown MP IDs {missing_mp}")
        missing_ct = sorted(set(row.get("contradiction_ids", [])) - ct_ids)
        if missing_ct:
            errors.append(f"{bid}: unknown CT IDs {missing_ct}")
        layers = row.get("enforcement_layers", [])
        unknown_layers = sorted(set(layers) - allowed_layers)
        if unknown_layers:
            errors.append(f"{bid}: unknown enforcement layers {unknown_layers}")
        state = row.get("state")
        if state not in allowed_states:
            errors.append(f"{bid}: invalid state {state!r}")
        machine = row.get("machine_enforced")
        if machine not in (True, False, "PARTIAL"):
            errors.append(f"{bid}: machine_enforced must be true/false/PARTIAL")
        runtime = row.get("runtime_observed")
        if runtime not in (True, False):
            errors.append(f"{bid}: runtime_observed must be boolean")
        if not row.get("claim") or not row.get("adjudication") or not row.get("next_evidence"):
            errors.append(f"{bid}: claim/adjudication/next_evidence must be non-empty")

        layer_counts.update(layers)
        state_counts[state] += 1
        ct_refs.update(row.get("contradiction_ids", []))
        machine_counts[str(machine)] += 1
        runtime_observed_count += 1 if runtime is True else 0

    uncovered_ct_ids = sorted(ct_ids - set(ct_refs))
    if uncovered_ct_ids:
        errors.append(f"Current contradiction IDs missing behavior coverage: {uncovered_ct_ids}")

    integrity = {
        "frozen_commit": FROZEN_COMMIT,
        "row_count": len(rows),
        "hard_errors": errors,
        "state_counts": dict(sorted(state_counts.items())),
        "enforcement_layer_counts": dict(sorted(layer_counts.items())),
        "machine_enforced_counts": dict(sorted(machine_counts.items())),
        "runtime_observed_count": runtime_observed_count,
        "current_contradiction_ids": sorted(ct_ids),
        "contradiction_reference_counts": dict(sorted(ct_refs.items())),
        "uncovered_current_contradiction_ids": uncovered_ct_ids,
    }
    OUT_INTEGRITY.write_text(json.dumps(integrity, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Phase 4 Behavior & Enforcement Matrix",
        "",
        f"Frozen source: `mattpocock/skills` @ `{FROZEN_COMMIT}`.",
        "",
        f"Working rows: **{len(rows)}**. Matrix state: **{matrix.get('status', 'UNKNOWN')}**.",
        "",
        "This is a Phase 4 working artifact, not a VERIFIED-status ledger. It separates documented claims, prompt behavior, static/executable enforcement, runtime dependence, and contradiction state.",
        "",
        "## Enforcement vocabulary",
        "",
        "- `DOCUMENTATION` — secondary/human-facing description only.",
        "- `PROMPT` — operative agent instruction; adherence is not deterministic by itself.",
        "- `STATIC_CONFIG` — declarative machine-readable rule/configuration.",
        "- `EXECUTABLE_SCRIPT` — executable code/check/hook enforces or verifies behavior.",
        "- `CI` — enforcement is wired into an automated repository workflow.",
        "- `RUNTIME` — behavior depends on actual harness/consumer execution.",
        "- `EXTERNAL_DEPENDENCY` — behavior depends on an external service/network/tool.",
        "- `NONE` — claimed guard/behavior has no corresponding operative enforcement found.",
        "",
        "## Matrix",
        "",
        "| ID | Area | State | Layers | Machine enforced | Runtime observed | CT | Adjudication |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        layers = ", ".join(row["enforcement_layers"])
        cts = ", ".join(row["contradiction_ids"]) if row["contradiction_ids"] else "—"
        lines.append(
            f"| {row['behavior_id']} | {esc(row['area'])} | {row['state']} | {layers} | "
            f"{row['machine_enforced']} | {row['runtime_observed']} | {cts} | {esc(row['adjudication'])} |"
        )

    lines += [
        "",
        "## Current counts",
        "",
        f"- states: `{dict(sorted(state_counts.items()))}`",
        f"- enforcement layers: `{dict(sorted(layer_counts.items()))}`",
        f"- runtime observed rows: **{runtime_observed_count} / {len(rows)}**",
        f"- current CT coverage: **{len(ct_ids) - len(uncovered_ct_ids)} / {len(ct_ids)}**",
        f"- integrity hard errors: **{len(errors)}**",
        "",
        "## Phase 4 rule",
        "",
        "A row can be statically adjudicated without being runtime-observed. No file becomes `VERIFIED` from this matrix alone; later applicable history, contradictions, runtime/distribution, second-pass, and red-team gates still apply.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if errors:
        raise SystemExit("Behavior matrix integrity failed:\n- " + "\n- ".join(errors))
    print(
        f"Behavior matrix GREEN: rows={len(rows)}, states={dict(state_counts)}, "
        f"runtime_observed={runtime_observed_count}, ct_coverage={len(ct_ids)}/{len(ct_ids)}"
    )


if __name__ == "__main__":
    main()

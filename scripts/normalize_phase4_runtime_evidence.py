#!/usr/bin/env python3
"""Canonicalize Phase 4 runtime-evidence workflow run IDs.

GitHub exposes GITHUB_RUN_ID to shell/Python processes as text. Runtime smoke
producers therefore may write a decimal string into the behavior matrix. The
Phase 4 evidence schema uses positive integers for durable workflow_run_id
values. This narrow normalizer converts decimal strings to integers and fails
closed on any other non-null representation.
"""
from __future__ import annotations

import json
from pathlib import Path

MATRIX = Path("04_BEHAVIOR_MATRIX.json")


def main() -> None:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    changed = 0
    errors: list[str] = []

    for row in data.get("rows", []):
        bid = row.get("behavior_id", "<missing>")
        for evidence in row.get("runtime_evidence", []) or []:
            value = evidence.get("workflow_run_id")
            if isinstance(value, int) and value > 0:
                continue
            if isinstance(value, str) and value.isdigit() and int(value) > 0:
                evidence["workflow_run_id"] = int(value)
                changed += 1
                continue
            errors.append(f"{bid}: invalid workflow_run_id {value!r}")

    if errors:
        raise SystemExit("Runtime evidence normalization failed:\n- " + "\n- ".join(errors))

    MATRIX.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Phase 4 runtime evidence normalized: changed={changed}")


if __name__ == "__main__":
    main()

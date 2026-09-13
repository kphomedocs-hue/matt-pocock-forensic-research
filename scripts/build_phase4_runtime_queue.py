#!/usr/bin/env python3
"""Build the deterministic Phase 4 evidence-depth queue.

Breadth coverage answers whether a behavior-relevant surface is represented at
all. This queue answers what kind of stronger evidence each behavior contract
still needs. The classification is intentionally mechanical and mutually
exclusive so runtime work cannot be cherry-picked.
"""
from __future__ import annotations

import json
import pathlib
from collections import Counter

FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
OUT_JSON = pathlib.Path("04_RUNTIME_OBSERVATION_QUEUE.json")
OUT_MD = pathlib.Path("04_RUNTIME_OBSERVATION_QUEUE.md")

EXECUTION_LAYERS = {"EXECUTABLE_SCRIPT", "RUNTIME", "CI"}
CONSUMER_LAYERS = {"STATIC_CONFIG"}
EXTERNAL_LAYERS = {"EXTERNAL_DEPENDENCY"}
VALID_CLASSES = {
    "EXECUTION_OBSERVATION",
    "MACHINE_CONSUMER_VALIDATION",
    "EXTERNAL_DEPENDENCY_VALIDATION",
    "PROMPT_REDTEAM_LATER",
}


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def classify(row: dict) -> tuple[str, str]:
    layers = set(row.get("enforcement_layers", []))
    if layers & EXECUTION_LAYERS:
        return (
            "EXECUTION_OBSERVATION",
            "Contract names executable/runtime/CI behavior; direct isolated execution or equivalent runtime evidence is required before runtime closure.",
        )
    if layers & CONSUMER_LAYERS:
        return (
            "MACHINE_CONSUMER_VALIDATION",
            "Contract is machine-readable configuration without an executable/runtime layer in the row; validate that the intended consumer actually loads and obeys it.",
        )
    if layers & EXTERNAL_LAYERS:
        return (
            "EXTERNAL_DEPENDENCY_VALIDATION",
            "Contract depends on behavior outside the frozen repository; validate the dependency/portability assumption separately from source truth.",
        )
    return (
        "PROMPT_REDTEAM_LATER",
        "Contract is prompt/documentation-led at this stage; adversarial behavioral testing belongs in the red-team/second-pass evidence queue rather than executable runtime closure.",
    )


def main() -> None:
    census = load(CENSUS)
    matrix = load(MATRIX)
    errors: list[str] = []

    if census.get("frozen_commit") != FROZEN_COMMIT:
        errors.append("census frozen commit mismatch")
    if matrix.get("frozen_commit") != FROZEN_COMMIT:
        errors.append("behavior matrix frozen commit mismatch")

    files = census.get("files", [])
    by_mp = {f["mp_id"]: f for f in files}
    if len(by_mp) != 164:
        errors.append(f"expected 164 unique census MP IDs, found {len(by_mp)}")

    rows = matrix.get("rows", [])
    items: list[dict] = []
    seen_ids: set[str] = set()

    for row in rows:
        bid = row.get("behavior_id")
        if not bid or bid in seen_ids:
            errors.append(f"missing or duplicate behavior ID: {bid!r}")
            continue
        seen_ids.add(bid)

        evidence_class, rationale = classify(row)
        if evidence_class not in VALID_CLASSES:
            errors.append(f"{bid}: invalid evidence class {evidence_class}")

        mp_ids = row.get("source_mp_ids", [])
        missing_mp = sorted(mp for mp in mp_ids if mp not in by_mp)
        if missing_mp:
            errors.append(f"{bid}: missing census MP IDs {missing_mp}")

        source_paths = [by_mp[mp]["path"] for mp in mp_ids if mp in by_mp]
        observed = bool(row.get("runtime_observed", False))
        items.append(
            {
                "behavior_id": bid,
                "area": row.get("area"),
                "state": row.get("state"),
                "machine_enforced": row.get("machine_enforced"),
                "enforcement_layers": row.get("enforcement_layers", []),
                "evidence_class": evidence_class,
                "runtime_observed": observed,
                "pending": not observed,
                "source_mp_ids": mp_ids,
                "source_paths": source_paths,
                "contradiction_ids": row.get("contradiction_ids", []),
                "rationale": rationale,
                "next_evidence": row.get("next_evidence"),
            }
        )

    items.sort(key=lambda x: x["behavior_id"])
    if len(items) != len(rows):
        errors.append(f"classified {len(items)} rows but matrix has {len(rows)}")

    class_counts = Counter(i["evidence_class"] for i in items)
    observed_counts = Counter(i["evidence_class"] for i in items if i["runtime_observed"])
    pending_counts = Counter(i["evidence_class"] for i in items if i["pending"])

    # The four classes must form an exact partition of the behavior matrix.
    if sum(class_counts.values()) != len(rows):
        errors.append("evidence classes do not partition behavior rows")
    if set(class_counts) - VALID_CLASSES:
        errors.append(f"unexpected evidence classes: {sorted(set(class_counts) - VALID_CLASSES)}")

    data = {
        "schema_version": 1,
        "source_repo": "mattpocock/skills",
        "frozen_commit": FROZEN_COMMIT,
        "phase": 4,
        "behavior_denominator": len(rows),
        "classified_behaviors": len(items),
        "runtime_observed": sum(1 for i in items if i["runtime_observed"]),
        "pending_total": sum(1 for i in items if i["pending"]),
        "evidence_class_counts": dict(sorted(class_counts.items())),
        "observed_by_class": {k: observed_counts.get(k, 0) for k in sorted(VALID_CLASSES)},
        "pending_by_class": {k: pending_counts.get(k, 0) for k in sorted(VALID_CLASSES)},
        "hard_errors": errors,
        "items": items,
    }
    OUT_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Phase 4 Evidence-Depth Queue",
        "",
        f"Frozen source: `mattpocock/skills` @ `{FROZEN_COMMIT}`.",
        "",
        "This is an evidence-depth queue, not a breadth denominator. Every behavior row is assigned to exactly one evidence class. `runtime_observed: false` means the stronger evidence has not yet been recorded; it does not erase static findings already established in the behavior matrix.",
        "",
        f"Behavior denominator: **{len(rows)}**.",
        f"Classified: **{len(items)}/{len(rows)}**.",
        f"Runtime-observed rows: **{sum(1 for i in items if i['runtime_observed'])}/{len(rows)}**.",
        f"Pending stronger evidence: **{sum(1 for i in items if i['pending'])}**.",
        "",
        "## Evidence classes",
        "",
        "| Class | Total | Observed | Pending | Meaning |",
        "|---|---:|---:|---:|---|",
    ]
    meanings = {
        "EXECUTION_OBSERVATION": "Executable/runtime/CI contract; isolate and execute or obtain equivalent runtime evidence.",
        "MACHINE_CONSUMER_VALIDATION": "Static machine-readable config; prove the intended consumer loads/obeys it.",
        "EXTERNAL_DEPENDENCY_VALIDATION": "Behavior depends on an external service/tool/asset; validate the dependency assumption.",
        "PROMPT_REDTEAM_LATER": "Prompt/docs judgment contract; test adversarially in second-pass/red-team work.",
    }
    for cls in sorted(VALID_CLASSES):
        lines.append(
            f"| {cls} | {class_counts.get(cls, 0)} | {observed_counts.get(cls, 0)} | {pending_counts.get(cls, 0)} | {meanings[cls]} |"
        )

    lines += [
        "",
        "## Queue",
        "",
        "| Behavior | Evidence class | State | Observed | Source MPs | Area | Next evidence |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in items:
        mps = ", ".join(item["source_mp_ids"]) or "—"
        next_evidence = str(item.get("next_evidence") or "—").replace("|", "\\|").replace("\n", " ")
        area = str(item.get("area") or "—").replace("|", "\\|")
        lines.append(
            f"| {item['behavior_id']} | {item['evidence_class']} | {item['state']} | {'YES' if item['runtime_observed'] else 'NO'} | {mps} | {area} | {next_evidence} |"
        )

    lines += ["", f"Hard errors: **{len(errors)}**."]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if errors:
        raise SystemExit("Phase 4 runtime/evidence queue failed:\n- " + "\n- ".join(errors))
    print(
        f"Phase 4 evidence queue: classified={len(items)}/{len(rows)}, "
        f"observed={sum(1 for i in items if i['runtime_observed'])}, "
        f"pending={sum(1 for i in items if i['pending'])}, classes={dict(sorted(class_counts.items()))}"
    )


if __name__ == "__main__":
    main()

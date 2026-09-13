#!/usr/bin/env python3
"""Build deterministic Phase 4 coverage across every current SKILL.md.

This is a coverage index, not a verification gate. It makes untouched skills visible
while Phase 4 is in progress and can later become a zero-uncovered closure gate.
"""
from __future__ import annotations

import json
import pathlib
from collections import Counter, defaultdict

FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
MATRIX = pathlib.Path("04_BEHAVIOR_MATRIX.json")
OUT_JSON = pathlib.Path("04_BEHAVIOR_COVERAGE.json")
OUT_MD = pathlib.Path("04_BEHAVIOR_COVERAGE.md")


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    census = load(CENSUS)
    matrix = load(MATRIX)
    errors: list[str] = []

    if census.get("frozen_commit") != FROZEN_COMMIT:
        errors.append("census frozen commit mismatch")
    if matrix.get("frozen_commit") != FROZEN_COMMIT:
        errors.append("behavior matrix frozen commit mismatch")

    skills = [
        f for f in census.get("files", [])
        if f.get("category") == "skill" and f.get("path", "").endswith("/SKILL.md")
    ]
    skills.sort(key=lambda f: f["path"])
    if len(skills) != 37:
        errors.append(f"expected 37 current SKILL.md files, found {len(skills)}")

    by_mp: dict[str, list[dict]] = defaultdict(list)
    for row in matrix.get("rows", []):
        for mp in row.get("source_mp_ids", []):
            by_mp[mp].append(row)

    coverage = []
    state_counts = Counter()
    covered = 0
    for skill in skills:
        rows = sorted(by_mp.get(skill["mp_id"], []), key=lambda r: r["behavior_id"])
        row_ids = [r["behavior_id"] for r in rows]
        states = sorted({r["state"] for r in rows})
        cts = sorted({ct for r in rows for ct in r.get("contradiction_ids", [])})
        is_covered = bool(rows)
        if is_covered:
            covered += 1
            state_counts.update(r["state"] for r in rows)
        coverage.append({
            "mp_id": skill["mp_id"],
            "path": skill["path"],
            "covered": is_covered,
            "behavior_ids": row_ids,
            "states": states,
            "contradiction_ids": cts,
        })

    uncovered = [row for row in coverage if not row["covered"]]
    data = {
        "schema_version": 1,
        "source_repo": "mattpocock/skills",
        "frozen_commit": FROZEN_COMMIT,
        "phase": 4,
        "skill_denominator": len(skills),
        "covered_skills": covered,
        "uncovered_skills": len(uncovered),
        "uncovered_mp_ids": [r["mp_id"] for r in uncovered],
        "uncovered_paths": [r["path"] for r in uncovered],
        "behavior_row_count": len(matrix.get("rows", [])),
        "covered_state_occurrences": dict(sorted(state_counts.items())),
        "hard_errors": errors,
        "skills": coverage,
    }
    OUT_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Phase 4 Current-Skill Coverage",
        "",
        f"Frozen source: `mattpocock/skills` @ `{FROZEN_COMMIT}`.",
        "",
        f"Current `SKILL.md` denominator: **{len(skills)}**.",
        f"Skills with at least one Phase 4 behavior row: **{covered}/{len(skills)}**.",
        f"Uncovered current skills: **{len(uncovered)}**.",
        "",
        "Coverage means the skill participates in at least one explicit behavior contract. It does **not** mean the skill is VERIFIED or that all of its behaviors have been exhausted.",
        "",
        "| MP-ID | Skill | Covered | Behavior rows | States | CTs |",
        "|---|---|---|---|---|---|",
    ]
    for row in coverage:
        ids = ", ".join(row["behavior_ids"]) or "—"
        states = ", ".join(row["states"]) or "—"
        cts = ", ".join(row["contradiction_ids"]) or "—"
        lines.append(f"| {row['mp_id']} | `{row['path']}` | {'YES' if row['covered'] else 'NO'} | {ids} | {states} | {cts} |")

    lines += [
        "",
        "## Uncovered queue",
        "",
    ]
    if uncovered:
        lines.extend(f"- {r['mp_id']} — `{r['path']}`" for r in uncovered)
    else:
        lines.append("- None.")
    lines += ["", f"Hard errors: **{len(errors)}**."]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if errors:
        raise SystemExit("Phase 4 coverage failed:\n- " + "\n- ".join(errors))
    print(f"Phase 4 coverage: {covered}/{len(skills)} skills, uncovered={len(uncovered)}")


if __name__ == "__main__":
    main()

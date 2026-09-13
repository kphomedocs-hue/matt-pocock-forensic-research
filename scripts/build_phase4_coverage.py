#!/usr/bin/env python3
"""Build deterministic Phase 4 coverage across current skills and high-risk non-skill surfaces.

Coverage is a breadth index, not a verification gate. It makes untouched operative
skills and behavior-owning/configuring/enforcing/distributing files visible while
Phase 4 is in progress.
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

HIGH_RISK_SURFACE_CATEGORIES = {
    "skill-support",
    "skill-executable-config",
    "codex-metadata",
    "repo-executable",
    "package-config",
    "dependency-lock",
    "distribution",
    "ci-release",
}


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def coverage_row(item: dict, by_mp: dict[str, list[dict]]) -> dict:
    rows = sorted(by_mp.get(item["mp_id"], []), key=lambda r: r["behavior_id"])
    return {
        "mp_id": item["mp_id"],
        "path": item["path"],
        "category": item.get("category"),
        "covered": bool(rows),
        "behavior_ids": [r["behavior_id"] for r in rows],
        "states": sorted({r["state"] for r in rows}),
        "contradiction_ids": sorted({ct for r in rows for ct in r.get("contradiction_ids", [])}),
    }


def main() -> None:
    census = load(CENSUS)
    matrix = load(MATRIX)
    errors: list[str] = []

    if census.get("frozen_commit") != FROZEN_COMMIT:
        errors.append("census frozen commit mismatch")
    if matrix.get("frozen_commit") != FROZEN_COMMIT:
        errors.append("behavior matrix frozen commit mismatch")

    files = census.get("files", [])
    skills = [
        f for f in files
        if f.get("category") == "skill" and f.get("path", "").endswith("/SKILL.md")
    ]
    skills.sort(key=lambda f: f["path"])
    if len(skills) != 37:
        errors.append(f"expected 37 current SKILL.md files, found {len(skills)}")

    surfaces = [f for f in files if f.get("category") in HIGH_RISK_SURFACE_CATEGORIES]
    surfaces.sort(key=lambda f: f["path"])
    if not surfaces:
        errors.append("high-risk non-skill surface denominator is empty")
    if any(f.get("category") == "skill" for f in surfaces):
        errors.append("skill file leaked into non-skill surface denominator")

    by_mp: dict[str, list[dict]] = defaultdict(list)
    for row in matrix.get("rows", []):
        for mp in row.get("source_mp_ids", []):
            by_mp[mp].append(row)

    skill_coverage = [coverage_row(skill, by_mp) for skill in skills]
    surface_coverage = [coverage_row(surface, by_mp) for surface in surfaces]

    uncovered_skills = [row for row in skill_coverage if not row["covered"]]
    uncovered_surfaces = [row for row in surface_coverage if not row["covered"]]
    covered_skills = len(skill_coverage) - len(uncovered_skills)
    covered_surfaces = len(surface_coverage) - len(uncovered_surfaces)

    skill_state_counts = Counter(
        r["state"]
        for skill in skills
        for r in by_mp.get(skill["mp_id"], [])
    )
    surface_category_counts = Counter(row["category"] for row in surface_coverage)
    uncovered_surface_category_counts = Counter(row["category"] for row in uncovered_surfaces)

    data = {
        "schema_version": 2,
        "source_repo": "mattpocock/skills",
        "frozen_commit": FROZEN_COMMIT,
        "phase": 4,
        "skill_denominator": len(skills),
        "covered_skills": covered_skills,
        "uncovered_skills": len(uncovered_skills),
        "uncovered_mp_ids": [r["mp_id"] for r in uncovered_skills],
        "uncovered_paths": [r["path"] for r in uncovered_skills],
        "surface_categories": sorted(HIGH_RISK_SURFACE_CATEGORIES),
        "surface_denominator": len(surface_coverage),
        "covered_surfaces": covered_surfaces,
        "uncovered_surfaces": len(uncovered_surfaces),
        "uncovered_surface_mp_ids": [r["mp_id"] for r in uncovered_surfaces],
        "uncovered_surface_paths": [r["path"] for r in uncovered_surfaces],
        "surface_category_counts": dict(sorted(surface_category_counts.items())),
        "uncovered_surface_category_counts": dict(sorted(uncovered_surface_category_counts.items())),
        "behavior_row_count": len(matrix.get("rows", [])),
        "covered_state_occurrences": dict(sorted(skill_state_counts.items())),
        "hard_errors": errors,
        "skills": skill_coverage,
        "surfaces": surface_coverage,
    }
    OUT_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Phase 4 Behavior Coverage",
        "",
        f"Frozen source: `mattpocock/skills` @ `{FROZEN_COMMIT}`.",
        "",
        "Coverage means a file participates in at least one explicit Phase 4 behavior contract. It does **not** mean the file is VERIFIED or that every behavior has been exhausted.",
        "",
        "## Current skills",
        "",
        f"Current `SKILL.md` denominator: **{len(skills)}**.",
        f"Skills with at least one Phase 4 behavior row: **{covered_skills}/{len(skills)}**.",
        f"Uncovered current skills: **{len(uncovered_skills)}**.",
        "",
        "| MP-ID | Skill | Covered | Behavior rows | States | CTs |",
        "|---|---|---|---|---|---|",
    ]
    for row in skill_coverage:
        ids = ", ".join(row["behavior_ids"]) or "—"
        states = ", ".join(row["states"]) or "—"
        cts = ", ".join(row["contradiction_ids"]) or "—"
        lines.append(f"| {row['mp_id']} | `{row['path']}` | {'YES' if row['covered'] else 'NO'} | {ids} | {states} | {cts} |")

    lines += [
        "",
        "### Uncovered current-skill queue",
        "",
    ]
    if uncovered_skills:
        lines.extend(f"- {r['mp_id']} — `{r['path']}`" for r in uncovered_skills)
    else:
        lines.append("- None.")

    lines += [
        "",
        "## High-risk non-skill surfaces",
        "",
        "Included categories: `" + "`, `".join(sorted(HIGH_RISK_SURFACE_CATEGORIES)) + "`.",
        "",
        f"Surface denominator: **{len(surface_coverage)}**.",
        f"Surfaces with at least one Phase 4 behavior row: **{covered_surfaces}/{len(surface_coverage)}**.",
        f"Uncovered high-risk surfaces: **{len(uncovered_surfaces)}**.",
        "",
        "| MP-ID | Category | Surface | Covered | Behavior rows | CTs |",
        "|---|---|---|---|---|---|",
    ]
    for row in surface_coverage:
        ids = ", ".join(row["behavior_ids"]) or "—"
        cts = ", ".join(row["contradiction_ids"]) or "—"
        lines.append(f"| {row['mp_id']} | {row['category']} | `{row['path']}` | {'YES' if row['covered'] else 'NO'} | {ids} | {cts} |")

    lines += [
        "",
        "### Uncovered high-risk surface queue",
        "",
    ]
    if uncovered_surfaces:
        lines.extend(f"- {r['mp_id']} — `{r['path']}` ({r['category']})" for r in uncovered_surfaces)
    else:
        lines.append("- None.")
    lines += ["", f"Hard errors: **{len(errors)}**."]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if errors:
        raise SystemExit("Phase 4 coverage failed:\n- " + "\n- ".join(errors))
    print(
        f"Phase 4 coverage: skills={covered_skills}/{len(skills)}, "
        f"surfaces={covered_surfaces}/{len(surface_coverage)}, "
        f"uncovered_surfaces={len(uncovered_surfaces)}"
    )


if __name__ == "__main__":
    main()

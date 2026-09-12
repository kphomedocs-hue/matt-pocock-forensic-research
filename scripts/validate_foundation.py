#!/usr/bin/env python3
"""Validate the durable forensic foundation before Phase 3 status promotion.

This script is intentionally non-destructive. It validates provenance and cross-register
integrity, measures note-schema variation, derives distribution-set truth from the frozen
source, and emits a generated foundation report. It fails closed on hard integrity errors.
"""
from __future__ import annotations

import base64
import json
import os
import pathlib
import re
import urllib.request
from collections import Counter

SOURCE_REPO = "mattpocock/skills"
FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
NOTES = pathlib.Path("02_FILE_NOTES")
CONTRADICTIONS = pathlib.Path("04_CONTRADICTION_REGISTER.md")
HISTORY = pathlib.Path("05_HISTORY_LEDGER.md")
REPORT_JSON = pathlib.Path("00_FOUNDATION_INTEGRITY.json")
REPORT_MD = pathlib.Path("00_FOUNDATION_INTEGRITY.md")

STATUS_RE = re.compile(r"^(?:-\s*)?Status:\s*(?:\*\*)?(.+?)(?:\*\*)?\s*$", re.M)
COMMIT_RE = re.compile(r"^(?:-\s*)?Frozen commit:\s*`?([0-9a-f]{40})`?\s*$", re.M)
BLOB_RE = re.compile(r"^(?:-\s*)?Blob SHA:\s*`?([0-9a-f]{40})`?\s*$", re.M)
CATEGORY_RE = re.compile(r"^(?:-\s*)?Category:\s*(.+?)\s*$", re.M)
CT_REF_RE = re.compile(r"\bCT-(?:H)?\d{2,3}\b")
H_REF_RE = re.compile(r"\bH-\d{3}\b")

RECOMMENDED_NOTE_SECTIONS = {
    "read_evidence": ("## Read evidence", "## Full-read evidence"),
    "source_facts": ("## Source facts", "## Observations"),
    "connections": ("## References / connections to trace", "## Connections", "## Connection evidence"),
    "unresolved": ("## Unresolved / later-phase checks", "## Unresolved", "## Later-phase checks"),
}


def api_json(url: str) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "forensic-foundation-validator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def frozen_text(path: str) -> str:
    encoded = urllib.parse.quote(path, safe="/")
    data = api_json(f"https://api.github.com/repos/{SOURCE_REPO}/contents/{encoded}?ref={FROZEN_COMMIT}")
    if data.get("encoding") != "base64":
        raise SystemExit(f"Unexpected encoding for frozen source {path}")
    return base64.b64decode(data["content"]).decode("utf-8", errors="replace")


def parse_register_ids(text: str, prefix: str) -> set[str]:
    if prefix == "CT":
        return set(CT_REF_RE.findall(text))
    return set(H_REF_RE.findall(text))


def has_any(text: str, options: tuple[str, ...]) -> bool:
    return any(opt in text for opt in options)


def main() -> None:
    hard_errors: list[str] = []
    warnings: list[str] = []
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    files = census.get("files", [])
    if census.get("frozen_commit") != FROZEN_COMMIT:
        hard_errors.append("Census frozen commit does not match validator baseline")
    if census.get("blob_count") != EXPECTED_FILES or len(files) != EXPECTED_FILES:
        hard_errors.append(f"Expected {EXPECTED_FILES} census files, got blob_count={census.get('blob_count')} rows={len(files)}")

    by_id = {f["mp_id"]: f for f in files}
    if len(by_id) != EXPECTED_FILES:
        hard_errors.append("MP-ID uniqueness failure in census")

    note_rows = []
    note_ct_refs: set[str] = set()
    note_h_refs: set[str] = set()
    section_counts = Counter()
    status_counts = Counter()
    for mp_id, item in sorted(by_id.items()):
        path = NOTES / f"{mp_id}.md"
        if not path.exists():
            hard_errors.append(f"Missing durable note: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        sm = STATUS_RE.search(text)
        cm = COMMIT_RE.search(text)
        bm = BLOB_RE.search(text)
        catm = CATEGORY_RE.search(text)
        if not sm:
            hard_errors.append(f"{path}: missing Status")
            status = "MISSING"
        else:
            status = sm.group(1).strip()
            status_counts[status] += 1
        if not cm or cm.group(1) != FROZEN_COMMIT:
            hard_errors.append(f"{path}: frozen commit missing/mismatch")
        if not bm or bm.group(1) != item["sha"]:
            hard_errors.append(f"{path}: blob SHA missing/mismatch against census")
        if not catm:
            warnings.append(f"{path}: category line missing")
        elif catm.group(1).strip() != item["category"]:
            warnings.append(f"{path}: category differs from census ({catm.group(1).strip()} != {item['category']})")

        present = {}
        for key, options in RECOMMENDED_NOTE_SECTIONS.items():
            present[key] = has_any(text, options)
            if present[key]:
                section_counts[key] += 1
        note_ct_refs |= set(CT_REF_RE.findall(text))
        note_h_refs |= set(H_REF_RE.findall(text))
        note_rows.append({"mp_id": mp_id, "path": item["path"], "status": status, "sections": present})

    ct_text = CONTRADICTIONS.read_text(encoding="utf-8")
    hist_text = HISTORY.read_text(encoding="utf-8")
    ct_ids = parse_register_ids(ct_text, "CT")
    hist_ids = parse_register_ids(hist_text, "H")
    missing_ct = sorted(note_ct_refs - ct_ids)
    missing_hist = sorted(note_h_refs - hist_ids)
    if missing_ct:
        hard_errors.append(f"Note references missing from contradiction register: {missing_ct}")
    if missing_hist:
        hard_errors.append(f"Note references missing from history ledger: {missing_hist}")

    # Register structural checks.
    current_ct_rows = re.findall(r"^\| (CT-\d{3}) \|", ct_text, re.M)
    hist_ct_rows = re.findall(r"^\| (CT-H\d{2}) \|", ct_text, re.M)
    if len(set(current_ct_rows)) != len(current_ct_rows):
        hard_errors.append("Duplicate current contradiction IDs")
    if len(set(hist_ct_rows)) != len(hist_ct_rows):
        hard_errors.append("Duplicate historical contradiction IDs")
    history_rows = re.findall(r"^\| (H-\d{3}) \|", hist_text, re.M)
    if len(set(history_rows)) != len(history_rows):
        hard_errors.append("Duplicate history IDs")

    # Exact skill/distribution sets from frozen source.
    current_skills = sorted(f["path"][:-len("/SKILL.md")] for f in files if f["path"].startswith("skills/") and f["path"].endswith("/SKILL.md"))
    if len(current_skills) != 37:
        hard_errors.append(f"Expected 37 current skills, got {len(current_skills)}")

    plugin = json.loads(frozen_text(".claude-plugin/plugin.json"))
    plugin_entries = plugin.get("skills", [])
    promoted = sorted(x.rstrip("/") for x in plugin_entries)
    # plugin entries are relative paths beginning ./skills/... in this repo.
    promoted = sorted(x[2:] if x.startswith("./") else x for x in promoted)
    if len(promoted) != 25:
        hard_errors.append(f"Expected 25 plugin-promoted skills, got {len(promoted)}")
    missing_plugin_targets = sorted(set(promoted) - set(current_skills))
    if missing_plugin_targets:
        hard_errors.append(f"Plugin entries without current SKILL.md: {missing_plugin_targets}")

    link_script = frozen_text("scripts/link-skills.sh")
    # Current script explicitly traverses bucket directories. Capture quoted/unquoted bucket names conservatively.
    linked_buckets = []
    for bucket in ("engineering", "productivity", "in-progress", "misc", "deprecated"):
        if re.search(rf"skills/{re.escape(bucket)}|\b{re.escape(bucket)}\b", link_script):
            linked_buckets.append(bucket)
    # Semantic expected set at frozen commit, validated from Phase 2 source reading.
    expected_link_buckets = {"engineering", "productivity", "in-progress"}
    if not expected_link_buckets.issubset(set(linked_buckets)):
        warnings.append(f"Could not mechanically confirm all expected link buckets from script text; detected {linked_buckets}")
    linked_set = sorted(s for s in current_skills if s.split("/")[1] in expected_link_buckets)
    if len(linked_set) != 33:
        hard_errors.append(f"Expected 33 local-linked skills from bucket rule, got {len(linked_set)}")

    openai_metadata = sorted(f["path"] for f in files if f["path"].endswith("/agents/openai.yaml"))
    owner_paths = sorted(p[:-len("/agents/openai.yaml")] for p in openai_metadata)
    missing_openai = sorted(set(current_skills) - set(owner_paths))
    extra_openai = sorted(set(owner_paths) - set(current_skills))
    if missing_openai or extra_openai:
        hard_errors.append(f"Codex metadata ownership mismatch: missing={missing_openai}, extra={extra_openai}")

    distribution = []
    promoted_set = set(promoted)
    linked_set_s = set(linked_set)
    owner_set = set(owner_paths)
    for skill in current_skills:
        distribution.append({
            "skill": skill,
            "bucket": skill.split("/")[1],
            "plugin_promoted": skill in promoted_set,
            "local_linked": skill in linked_set_s,
            "codex_metadata": skill in owner_set,
        })

    report = {
        "baseline": {"source_repo": SOURCE_REPO, "frozen_commit": FROZEN_COMMIT, "physical_files": EXPECTED_FILES},
        "hard_errors": hard_errors,
        "warnings": warnings,
        "note_status_counts": dict(status_counts),
        "note_schema_coverage": {k: section_counts[k] for k in RECOMMENDED_NOTE_SECTIONS},
        "note_count": len(note_rows),
        "contradiction_ids_current": sorted(set(current_ct_rows)),
        "contradiction_ids_historical": sorted(set(hist_ct_rows)),
        "history_ids": sorted(set(history_rows)),
        "note_referenced_contradiction_ids": sorted(note_ct_refs),
        "note_referenced_history_ids": sorted(note_h_refs),
        "distribution_counts": {
            "current_skills": len(current_skills),
            "plugin_promoted": len(promoted),
            "local_linked": len(linked_set),
            "codex_metadata_owners": len(owner_paths),
        },
        "distribution": distribution,
        "notes": note_rows,
    }
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    md = [
        "# Foundation Integrity Report", "",
        f"Frozen source: `{SOURCE_REPO}` @ `{FROZEN_COMMIT}`", "",
        f"Hard integrity errors: **{len(hard_errors)}**", "",
        f"Warnings / normalization gaps: **{len(warnings)}**", "",
        "## Durable provenance", "",
        f"- Census rows: **{len(files)} / {EXPECTED_FILES}**",
        f"- Durable notes found: **{len(note_rows)} / {EXPECTED_FILES}**",
        f"- Status counts: `{dict(status_counts)}`", "",
        "## Note-schema coverage", "",
        "These are normalization measurements, not Phase 2 failures. Existing evidence is preserved.", "",
        "| Recommended field group | Notes containing it | Total |",
        "|---|---:|---:|",
    ]
    for k in RECOMMENDED_NOTE_SECTIONS:
        md.append(f"| {k} | {section_counts[k]} | {EXPECTED_FILES} |")
    md += ["", "## Register cross-checks", "",
           f"- Current contradiction IDs: **{len(set(current_ct_rows))}**",
           f"- Historical contradiction IDs: **{len(set(hist_ct_rows))}**",
           f"- History entries: **{len(set(history_rows))}**",
           f"- Note contradiction refs missing from register: **{len(missing_ct)}**",
           f"- Note history refs missing from ledger: **{len(missing_hist)}**", "",
           "## Generated distribution truth", "",
           f"- Current skills: **{len(current_skills)}**",
           f"- Claude plugin promoted: **{len(promoted)}**",
           f"- Maintainer local-linked: **{len(linked_set)}**",
           f"- Skills with Codex metadata owner: **{len(owner_paths)}**", "",
           "| Skill | Bucket | Plugin | Local link | Codex metadata |",
           "|---|---|---|---|---|"]
    for row in distribution:
        md.append(f"| `{row['skill']}` | {row['bucket']} | {'YES' if row['plugin_promoted'] else 'NO'} | {'YES' if row['local_linked'] else 'NO'} | {'YES' if row['codex_metadata'] else 'NO'} |")
    md += ["", "## Hard errors", ""]
    if hard_errors:
        md += [f"- {e}" for e in hard_errors]
    else:
        md.append("- None.")
    md += ["", "## Normalization warnings", ""]
    if warnings:
        md += [f"- {w}" for w in warnings]
    else:
        md.append("- None.")
    md += ["", "## Gate", "",
           "Phase 3 file promotion must not begin if this report has any hard integrity errors. Schema-coverage gaps are tracked for normalization but do not invalidate the completed physical read by themselves.", ""]
    REPORT_MD.write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({"hard_errors": len(hard_errors), "warnings": len(warnings), "status_counts": dict(status_counts), "schema": dict(section_counts), "distribution": report["distribution_counts"]}))
    if hard_errors:
        raise SystemExit("Foundation integrity validation failed; see 00_FOUNDATION_INTEGRITY.md")


if __name__ == "__main__":
    import urllib.parse
    main()

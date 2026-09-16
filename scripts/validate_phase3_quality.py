#!/usr/bin/env python3
"""Second-order quality checks for the completed Phase 3 connection state.

This validator does not replace the Phase 3 builders. It red-teams assumptions that
can make a mechanically green graph look more complete than it is:
- contextual backticked skill names must not be the sole proof of non-orphan status;
- Markdown reference definitions, autolinks and HTML href/src targets must not hide
  internal links from the main extractor;
- support files inside a skill directory should have an explicit relationship to
  their owning SKILL.md, or remain visible as an ownership gap;
- durable history ledger IDs/states/refs must agree with generated history bindings;
- the human master ledger should not present empty connection-count columns after
  Phase 3 is complete.

Outputs are diagnostic and fail closed only on evidence-integrity problems. Filing /
presentation debt is reported separately so it can be fixed without rewriting source
evidence.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import pathlib
import posixpath
import re
import urllib.request
from collections import Counter, defaultdict

SOURCE_REPO = "mattpocock/skills"
FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164

CENSUS = pathlib.Path("01_FILE_CENSUS.json")
GRAPH = pathlib.Path("03_CONNECTION_EDGES.json")
CLOSURE = pathlib.Path("03_PHASE3_CLOSURE_INDEX.json")
ORPHANS = pathlib.Path("03_ORPHAN_DISPOSITIONS.json")
HISTORY_BINDINGS = pathlib.Path("03_HISTORY_BINDINGS.json")
HISTORY_LEDGER = pathlib.Path("05_HISTORY_LEDGER.md")
MASTER_LEDGER = pathlib.Path("01_MASTER_FILE_LEDGER.md")
OUT_JSON = pathlib.Path("03_PHASE3_QUALITY.json")
OUT_MD = pathlib.Path("03_PHASE3_QUALITY.md")


def load(path: pathlib.Path):
    if not path.exists():
        raise SystemExit(f"Missing required Phase 3 artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def github_json(url: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "matt-pocock-forensic-phase3-quality",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def blob_text(sha: str) -> str:
    data = github_json(f"https://api.github.com/repos/{SOURCE_REPO}/git/blobs/{sha}")
    return base64.b64decode(data["content"]).decode("utf-8", errors="replace")


def normalize_link(source: str, raw: str) -> str | None:
    raw = raw.strip().strip('"\'')
    if raw.startswith("<") and raw.endswith(">"):
        raw = raw[1:-1].strip()
    if not raw or raw.startswith(("http://", "https://", "mailto:", "#", "data:")):
        return None
    raw = raw.split("#", 1)[0].split("?", 1)[0]
    if not raw:
        return None
    if raw.startswith("/"):
        return raw.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(source), raw)).removeprefix("./")


def structural_role(path: str) -> bool:
    if path.endswith("/agents/openai.yaml"):
        return True
    if path in {"README.md", ".gitignore", "package.json", "package-lock.json", ".changeset/config.json"}:
        return True
    if path.startswith("skills/") and path.endswith("/README.md"):
        return True
    if path.startswith("docs/") and path.endswith(".md"):
        return True
    if path.startswith(".changeset/") and path.endswith(".md"):
        return True
    if path.startswith(".github/workflows/") and path.endswith((".yml", ".yaml")):
        return True
    if path in {".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"}:
        return True
    return False


def history_ledger_rows(text: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line in text.splitlines():
        if not re.match(r"^\| H-\d{3} \|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            raise SystemExit(f"Cannot parse history ledger row: {line}")
        hid, date, area, event, evidence, significance, state = cells
        exact_evidence = f"{event} {evidence}"
        prs = sorted(set(re.findall(r"PR\s+#(\d+)", exact_evidence, re.I)))
        commits = sorted(set(re.findall(r"\b[0-9a-f]{40}\b", exact_evidence)))
        blob_shas = set(re.findall(r"\bblob SHA\s+\`?([0-9a-f]{40})", exact_evidence, re.I))
        commits = [sha for sha in commits if sha not in blob_shas]
        # A PR is the event boundary when explicitly present; merge/commit mentions
        # are supporting evidence and should not create a second binding event.
        refs = [("pr", p) for p in prs] if prs else [("commit", c) for c in commits]
        rows[hid] = {"state": state, "area": area, "refs": refs}
    return rows


def master_ledger_ref_debt(text: str) -> list[dict]:
    debt = []
    for line in text.splitlines():
        if not re.match(r"^\| MP-\d{4} \|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 12:
            continue
        mp_id, path, *_pre, ref_out, ref_in, _risk, _notes = cells
        if ref_out == "" or ref_in == "":
            debt.append({"mp_id": mp_id, "path": path, "ref_out": ref_out, "ref_in": ref_in})
    return debt


def main() -> None:
    census = load(CENSUS)
    graph = load(GRAPH)
    closure = load(CLOSURE)
    orphan_data = load(ORPHANS)
    history = load(HISTORY_BINDINGS)

    hard_errors: list[str] = []
    review_items: list[dict] = []
    improvements: list[dict] = []

    for label, obj in [("census", census), ("graph", graph), ("closure", closure), ("orphans", orphan_data), ("history", history)]:
        if obj.get("frozen_commit") != FROZEN_COMMIT:
            hard_errors.append(f"{label}: frozen commit mismatch")
    if census.get("blob_count") != EXPECTED_FILES or graph.get("file_count") != EXPECTED_FILES or closure.get("file_count") != EXPECTED_FILES:
        hard_errors.append("164-file denominator mismatch")

    files = census["files"]
    by_path = {row["path"]: row for row in files}
    texts = {row["path"]: blob_text(row["sha"]) for row in files}

    incoming: dict[str, list[dict]] = defaultdict(list)
    outgoing: dict[str, list[dict]] = defaultdict(list)
    pair_edges: set[tuple[str, str]] = set()
    for edge in graph.get("edges", []):
        incoming[edge["to"]].append(edge)
        outgoing[edge["from"]].append(edge)
        pair_edges.add((edge["from"], edge["to"]))

    # 1) Contextual backticks are weaker than explicit slash/$ skill labels.
    weak_backtick_edges = []
    for edge in graph.get("edges", []):
        if edge.get("type") != "SKILL_REFERENCE":
            continue
        evidence = edge.get("evidence", "")
        if re.search(r"exact skill label:\s*`[^`]+`", evidence):
            weak_backtick_edges.append(edge)

    weak_only_targets = []
    orphan_paths = {item["path"] for item in orphan_data.get("dispositions", [])}
    closure_by_path = {row["path"]: row for row in closure.get("rows", [])}
    for path in by_path:
        inc = incoming.get(path, [])
        if not inc:
            continue
        strong = [e for e in inc if e not in weak_backtick_edges]
        if strong:
            continue
        if structural_role(path) or path in orphan_paths:
            continue
        weak_only_targets.append({
            "path": path,
            "mp_id": by_path[path]["mp_id"],
            "weak_incoming": len(inc),
            "closure_orphan_state": closure_by_path.get(path, {}).get("dimensions", {}).get("orphan_state"),
        })
    if weak_only_targets:
        hard_errors.append(f"{len(weak_only_targets)} file(s) use contextual backtick skill mentions as sole non-orphan proof")
        review_items.extend({"kind": "WEAK_ONLY_ORPHAN_PROOF", **x} for x in weak_only_targets)

    # 2) Search link syntaxes not covered by the primary inline-link regex.
    refdef = re.compile(r"^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))", re.M)
    html = re.compile(r"\b(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.I)
    autolink = re.compile(r"<((?:\.\.?/|/)[^>\s]+)>")
    missing_link_edges = []
    for source, text in texts.items():
        raws = []
        raws.extend((a or b) for a, b in refdef.findall(text))
        raws.extend(html.findall(text))
        raws.extend(autolink.findall(text))
        for raw in raws:
            target = normalize_link(source, raw)
            if target and target in by_path and (source, target) not in pair_edges:
                missing_link_edges.append({"from": source, "to": target, "raw": raw})
    if missing_link_edges:
        hard_errors.append(f"{len(missing_link_edges)} internal reference-definition/HTML/autolink relationship(s) missing from graph")
        review_items.extend({"kind": "UNMAPPED_LINK_SYNTAX", **x} for x in missing_link_edges)

    # 3) Structural ownership: support artifacts inside a skill directory should
    # connect to the owner SKILL.md in at least one direction.
    support_owner_gaps = []
    skill_paths = {p for p in by_path if p.endswith("/SKILL.md")}
    for path, row in by_path.items():
        if not path.startswith("skills/") or path.endswith("/SKILL.md") or path.endswith("/agents/openai.yaml"):
            continue
        parts = path.split("/")
        if len(parts) < 4:
            continue
        owner = "/".join(parts[:3]) + "/SKILL.md"
        if owner not in skill_paths:
            continue
        if (path, owner) not in pair_edges and (owner, path) not in pair_edges:
            support_owner_gaps.append({"mp_id": row["mp_id"], "path": path, "owner": owner})
    if support_owner_gaps:
        improvements.append({
            "kind": "SUPPORT_OWNERSHIP_GAPS",
            "count": len(support_owner_gaps),
            "severity": "MEDIUM",
            "note": "Physical co-location proves ownership structurally but the graph does not encode it; add SUPPORT_BINDING edges or explicit dispositions.",
            "items": support_owner_gaps,
        })

    # 4) History bindings must match the durable history ledger, despite the
    # current builder having an internal event definition table.
    ledger_events = history_ledger_rows(HISTORY_LEDGER.read_text(encoding="utf-8"))
    generated_events = {event["history_id"]: event for event in history.get("events", [])}
    if set(ledger_events) != set(generated_events):
        hard_errors.append(f"History ID set drift: ledger={sorted(ledger_events)} generated={sorted(generated_events)}")
    history_parity = []
    for hid in sorted(set(ledger_events) & set(generated_events)):
        lrow = ledger_events[hid]
        grow = generated_events[hid]
        grefs = sorted((r["type"], str(r["ref"])) for r in grow.get("refs", []))
        state_ok = lrow["state"] == grow.get("lineage_state")
        refs_ok = sorted(lrow["refs"]) == grefs
        area_ok = lrow["area"] == grow.get("area")
        history_parity.append({"history_id": hid, "state_ok": state_ok, "refs_ok": refs_ok, "area_ok": area_ok})
        if not (state_ok and refs_ok and area_ok):
            hard_errors.append(f"History binding definition drift for {hid}: state_ok={state_ok} refs_ok={refs_ok} area_ok={area_ok}")

    # 5) Human-facing ledger Phase 3 columns should not remain blank after Phase 3.
    ledger_debt = master_ledger_ref_debt(MASTER_LEDGER.read_text(encoding="utf-8"))
    if ledger_debt:
        improvements.append({
            "kind": "MASTER_LEDGER_CONNECTION_COLUMNS_BLANK",
            "count": len(ledger_debt),
            "severity": "MEDIUM",
            "note": "Ref-in/Ref-out columns are preserved from old rows rather than derived from the current graph.",
        })

    # 6) Generated-state provenance currently lacks cryptographic input/output
    # fingerprints. Report as architecture debt until a build manifest exists.
    build_manifest = pathlib.Path("03_PHASE3_BUILD_MANIFEST.json")
    if not build_manifest.exists():
        improvements.append({
            "kind": "NO_PHASE3_BUILD_FINGERPRINT_MANIFEST",
            "count": 1,
            "severity": "HIGH",
            "note": "Atomic workflow reduces drift, but generated artifacts do not yet carry SHA-256 fingerprints of generator inputs and outputs.",
        })

    payload = {
        "source_repo": SOURCE_REPO,
        "frozen_commit": FROZEN_COMMIT,
        "file_count": len(files),
        "graph_edge_count": graph.get("edge_count"),
        "weak_backtick_skill_reference_count": len(weak_backtick_edges),
        "weak_only_orphan_proof_count": len(weak_only_targets),
        "unmapped_extra_link_syntax_count": len(missing_link_edges),
        "support_owner_gap_count": len(support_owner_gaps),
        "history_parity": history_parity,
        "master_ledger_blank_ref_row_count": len(ledger_debt),
        "hard_errors": hard_errors,
        "review_items": review_items,
        "improvements": improvements,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Phase 3 Quality Recheck",
        "",
        f"Frozen source: `{SOURCE_REPO}` @ `{FROZEN_COMMIT}`.",
        "",
        f"Files: **{len(files)}**. Graph edges: **{graph.get('edge_count')}**.",
        "",
        f"Hard quality errors: **{len(hard_errors)}**.",
        f"Contextual backtick skill-reference edges: **{len(weak_backtick_edges)}**.",
        f"Files relying only on contextual backticks for non-orphan proof: **{len(weak_only_targets)}**.",
        f"Internal reference-definition/HTML/autolink relationships missing from graph: **{len(missing_link_edges)}**.",
        f"Skill support ownership gaps: **{len(support_owner_gaps)}**.",
        f"Master-ledger rows with blank Ref-in or Ref-out: **{len(ledger_debt)}**.",
        "",
        "## Hard errors",
        "",
    ]
    lines += [f"- {e}" for e in hard_errors] or ["None."]
    lines += ["", "## Improvement backlog", ""]
    if improvements:
        for item in improvements:
            lines.append(f"- **{item['kind']}** — {item['severity']}; count={item['count']}. {item['note']}")
    else:
        lines.append("None from this validator.")
    lines += ["", "## Review items", ""]
    if review_items:
        for item in review_items:
            lines.append(f"- `{item['kind']}` — `{item.get('path') or item.get('from')}` {('→ `' + item['to'] + '`') if item.get('to') else ''}")
    else:
        lines.append("None.")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"phase3 quality: hard_errors={len(hard_errors)} weak_backticks={len(weak_backtick_edges)} "
        f"weak_only={len(weak_only_targets)} extra_links={len(missing_link_edges)} "
        f"support_gaps={len(support_owner_gaps)} ledger_ref_debt={len(ledger_debt)}"
    )

    if hard_errors:
        raise SystemExit("Phase 3 quality recheck found hard errors; see 03_PHASE3_QUALITY.md/json")


if __name__ == "__main__":
    main()

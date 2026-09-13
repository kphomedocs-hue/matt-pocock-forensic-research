#!/usr/bin/env python3
"""Build a conservative per-file Phase 3 CONNECTIONS TRACED readiness index.

This does not mutate file-note statuses. It identifies which files satisfy the
mechanical connection obligations and which still require explicit semantic/
orphan review before promotion.
"""
from __future__ import annotations

import json
import pathlib
from collections import Counter, defaultdict

FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164

CENSUS = pathlib.Path("01_FILE_CENSUS.json")
GRAPH = pathlib.Path("03_CONNECTION_EDGES.json")
DISTRIBUTION = pathlib.Path("03_DISTRIBUTION_MATRIX.json")
ROUTER = pathlib.Path("03_ROUTER_MATRIX.json")
HISTORY = pathlib.Path("03_HISTORY_BINDINGS.json")
DISPOSITIONS = pathlib.Path("03_REFERENCE_DISPOSITIONS.json")
OUT_JSON = pathlib.Path("03_PHASE3_CLOSURE_INDEX.json")
OUT_MD = pathlib.Path("03_PHASE3_CLOSURE_INDEX.md")


def load(path: pathlib.Path):
    if not path.exists():
        raise SystemExit(f"Required Phase 3 artifact missing: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def structural_orphan_role(path: str, dist_by_skill: dict[str, dict]) -> str | None:
    if path.endswith("/agents/openai.yaml"):
        return "CODEX_METADATA_CONVENTION"
    if path == "README.md":
        return "ROOT_SKILL_CATALOG"
    if path.startswith("skills/") and path.endswith("/README.md"):
        return "BUCKET_SKILL_CATALOG"
    if path.startswith("docs/") and path.endswith(".md"):
        parts = path.split("/")
        if len(parts) == 3:
            bucket, filename = parts[1], parts[2]
            name = filename.removesuffix(".md")
            skill_path = f"skills/{bucket}/{name}/SKILL.md"
            row = dist_by_skill.get(skill_path)
            if row and row.get("plugin_promoted") and row.get("docs_page_exists"):
                return "PROMOTED_HUMAN_DOC_PAGE"
    if path == ".changeset/config.json":
        return "CHANGESETS_CONFIG"
    if path.startswith(".changeset/") and path.endswith(".md"):
        return "CHANGESETS_INPUT_OR_GUIDE"
    if path.startswith(".github/workflows/") and path.endswith((".yml", ".yaml")):
        return "GITHUB_ACTIONS_ENTRYPOINT"
    if path == ".gitignore":
        return "GIT_CONFIGURATION"
    if path == "package.json":
        return "NPM_PACKAGE_MANIFEST"
    if path == "package-lock.json":
        return "NPM_LOCKFILE"
    if path in {".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"}:
        return "CLAUDE_PLUGIN_MANIFEST"
    return None


def main() -> None:
    census = load(CENSUS)
    graph = load(GRAPH)
    dist = load(DISTRIBUTION)
    router = load(ROUTER)
    history = load(HISTORY)
    dispositions = load(DISPOSITIONS)

    for label, obj in [
        ("census", census),
        ("graph", graph),
        ("distribution", dist),
        ("router", router),
        ("history", history),
        ("dispositions", dispositions),
    ]:
        if obj.get("frozen_commit") != FROZEN_COMMIT:
            raise SystemExit(f"{label} frozen commit mismatch")

    if census.get("blob_count") != EXPECTED_FILES or graph.get("file_count") != EXPECTED_FILES:
        raise SystemExit("164-file denominator mismatch")
    if graph.get("invocation_policy_mismatch_count") != 0:
        raise SystemExit("Invocation-policy mismatch blocks Phase 3 closure index")
    if graph.get("illegal_operative_call_count") != 0:
        raise SystemExit("Illegal operative call blocks Phase 3 closure index")
    if dist.get("anomaly_count") != 0:
        raise SystemExit("Distribution symmetry anomaly blocks Phase 3 closure index")
    if router.get("missing_promoted_targets") or router.get("extra_nonpromoted_targets"):
        raise SystemExit("Router symmetry anomaly blocks Phase 3 closure index")

    files = census["files"]
    by_path = {row["path"]: row for row in files}
    outgoing: dict[str, list[dict]] = defaultdict(list)
    incoming: dict[str, list[dict]] = defaultdict(list)
    for edge in graph["edges"]:
        outgoing[edge["from"]].append(edge)
        incoming[edge["to"]].append(edge)

    disp_keys = {
        (item["from"], item["raw"], item["kind"]): item
        for item in dispositions["dispositions"]
        if item.get("resolved") is True
    }
    unresolved_by_source: dict[str, list[dict]] = defaultdict(list)
    undisposed = []
    for item in graph["unresolved_internal"]:
        key = (item["from"], item["raw"], item["kind"])
        unresolved_by_source[item["from"]].append(item)
        if key not in disp_keys:
            undisposed.append(item)
    if undisposed:
        raise SystemExit(f"Raw unresolved references lack dispositions: {undisposed}")

    dist_by_skill = {row["path"]: row for row in dist["rows"]}
    router_by_skill = {row["path"]: row for row in router["rows"]}
    history_by_path = {row["path"]: row for row in history["file_rows"]}
    policy_by_skill = {row["skill_path"]: row for row in graph["invocation_policies"]}

    rows = []
    for file_row in files:
        path = file_row["path"]
        out_edges = outgoing.get(path, [])
        in_edges = incoming.get(path, [])
        blockers: list[str] = []
        dimensions: dict[str, object] = {}

        dimensions["graph_persisted"] = True
        dimensions["outgoing_edge_count"] = len(out_edges)
        dimensions["incoming_edge_count"] = len(in_edges)
        dimensions["raw_unresolved_count"] = len(unresolved_by_source.get(path, []))
        dimensions["raw_unresolved_reconciled"] = all(
            (item["from"], item["raw"], item["kind"]) in disp_keys
            for item in unresolved_by_source.get(path, [])
        )
        if not dimensions["raw_unresolved_reconciled"]:
            blockers.append("UNRESOLVED_REFERENCE_DISPOSITION")

        structural_role = structural_orphan_role(path, dist_by_skill)
        if in_edges:
            orphan_state = "NON_ORPHAN_BY_INCOMING_EDGE"
            orphan_closed = True
        elif structural_role:
            orphan_state = f"NON_ORPHAN_BY_STRUCTURAL_ROLE:{structural_role}"
            orphan_closed = True
        else:
            orphan_state = "ZERO_INCOMING_REQUIRES_SEMANTIC_ORPHAN_REVIEW"
            orphan_closed = False
            blockers.append("SEMANTIC_ORPHAN_REVIEW")
        dimensions["orphan_state"] = orphan_state
        dimensions["orphan_closed"] = orphan_closed

        if path.endswith("/SKILL.md"):
            drow = dist_by_skill.get(path)
            prow = policy_by_skill.get(path)
            rrow = router_by_skill.get(path)
            dimensions["skill_distribution_row"] = drow is not None
            dimensions["skill_invocation_policy_row"] = prow is not None
            if drow is None:
                blockers.append("MISSING_DISTRIBUTION_ROW")
            if prow is None:
                blockers.append("MISSING_INVOCATION_POLICY_ROW")
            elif not prow.get("consistent"):
                blockers.append("INVOCATION_POLICY_MISMATCH")

            operative = [e for e in out_edges if e["type"] == "OPERATIVE_CALL"]
            illegal = [e for e in operative if not e.get("invocation_legal", False)]
            dimensions["outgoing_operative_calls"] = len(operative)
            dimensions["illegal_outgoing_operative_calls"] = len(illegal)
            if illegal:
                blockers.append("ILLEGAL_OPERATIVE_CALL")

            if drow and drow.get("plugin_promoted") and path != "skills/engineering/ask-matt/SKILL.md":
                router_ok = bool(rrow and rrow.get("router_mentions"))
                dimensions["promoted_router_obligation_closed"] = router_ok
                if not router_ok:
                    blockers.append("PROMOTED_ROUTER_GAP")
            else:
                dimensions["promoted_router_obligation_closed"] = True

        if path.endswith("/agents/openai.yaml"):
            config_edges = [e for e in out_edges if e["type"] == "CONFIG_BINDING"]
            dimensions["config_binding_count"] = len(config_edges)
            if len(config_edges) != 1:
                blockers.append("CONFIG_BINDING_COUNT")

        if path == ".claude-plugin/plugin.json":
            dist_edges = [e for e in out_edges if e["type"] == "DISTRIBUTION_ENTRY"]
            dimensions["distribution_entry_count"] = len(dist_edges)
            if len(dist_edges) != 25:
                blockers.append("PLUGIN_DISTRIBUTION_COUNT")

        if file_row["mode"] == "120000":
            symlink_edges = [e for e in out_edges if e["type"] == "SYMLINK"]
            dimensions["symlink_target_count"] = len(symlink_edges)
            if len(symlink_edges) != 1:
                blockers.append("SYMLINK_TARGET_COUNT")

        hrow = history_by_path.get(path, {})
        bindings = hrow.get("history_bindings", [])
        dimensions["history_binding_count"] = len(bindings)
        dimensions["history_has_partial"] = any(
            b.get("lineage_state") == "PARTIAL" for b in bindings
        )

        ready = len(blockers) == 0
        rows.append({
            "mp_id": file_row["mp_id"],
            "path": path,
            "category": file_row["category"],
            "current_status": file_row.get("status", "READ"),
            "phase3_gate_state": "READY_CANDIDATE" if ready else "BLOCKED",
            "blockers": blockers,
            "dimensions": dimensions,
        })

    state_counts = Counter(row["phase3_gate_state"] for row in rows)
    blocker_counts = Counter(blocker for row in rows for blocker in row["blockers"])
    zero_incoming = [row for row in rows if row["dimensions"]["incoming_edge_count"] == 0]

    payload = {
        "frozen_commit": FROZEN_COMMIT,
        "file_count": len(rows),
        "gate_semantics": "READY_CANDIDATE is not automatic status promotion; per-file durable note promotion remains a separate write step.",
        "state_counts": dict(sorted(state_counts.items())),
        "blocker_counts": dict(sorted(blocker_counts.items())),
        "zero_incoming_count": len(zero_incoming),
        "rows": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Phase 3 Per-File Closure Index",
        "",
        f"Frozen source: `mattpocock/skills` @ `{FROZEN_COMMIT}`.",
        "",
        "This index applies the mechanical parts of the canonical `CONNECTIONS TRACED` gate. **READY_CANDIDATE is not a status promotion.** Notes remain READ until the candidate is explicitly promoted with durable evidence.",
        "",
        f"Files: **{len(rows)}**. READY_CANDIDATE: **{state_counts.get('READY_CANDIDATE', 0)}**. BLOCKED: **{state_counts.get('BLOCKED', 0)}**.",
        "",
        f"Files with zero incoming graph edges: **{len(zero_incoming)}**. Zero incoming is not treated as proof of orphan; conventional structural roles close some cases, and the rest require semantic orphan review.",
        "",
        "## Blocker summary",
        "",
        "| Blocker | Files |",
        "|---|---:|",
    ]
    if blocker_counts:
        for blocker, count in sorted(blocker_counts.items()):
            lines.append(f"| {blocker} | {count} |")
    else:
        lines.append("| None | 0 |")

    lines += [
        "",
        "## Per-file state",
        "",
        "| MP-ID | Path | Incoming | Outgoing | Orphan evaluation | Gate state | Blockers |",
        "|---|---|---:|---:|---|---|---|",
    ]
    for row in rows:
        d = row["dimensions"]
        blockers = ", ".join(row["blockers"]) if row["blockers"] else "—"
        lines.append(
            f"| {row['mp_id']} | `{row['path']}` | {d['incoming_edge_count']} | {d['outgoing_edge_count']} | "
            f"{d['orphan_state']} | {row['phase3_gate_state']} | {blockers} |"
        )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"phase3 closure: ready={state_counts.get('READY_CANDIDATE',0)} "
        f"blocked={state_counts.get('BLOCKED',0)} blockers={dict(blocker_counts)}"
    )


if __name__ == "__main__":
    main()

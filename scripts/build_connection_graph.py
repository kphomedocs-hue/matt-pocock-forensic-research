#!/usr/bin/env python3
"""Build a deterministic internal connection graph for the frozen mattpocock/skills tree.

This script uses the already-frozen 164-file census as the denominator, fetches each
blob by SHA, and derives only source-explicit or structurally deterministic edges.
It does not use ranked search to prove absence.
"""
from __future__ import annotations

import base64
import json
import os
import pathlib
import posixpath
import re
import urllib.request
from collections import defaultdict

SOURCE_REPO = "mattpocock/skills"
FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
EDGES_JSON = pathlib.Path("03_CONNECTION_EDGES.json")
INDEX_MD = pathlib.Path("03_CONNECTION_INDEX.md")


def github_json(url: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "matt-pocock-forensic-connection-builder",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def blob_text(sha: str) -> str:
    data = github_json(f"https://api.github.com/repos/{SOURCE_REPO}/git/blobs/{sha}")
    raw = base64.b64decode(data["content"])
    return raw.decode("utf-8", errors="replace")


def normalize_link(source_path: str, target: str) -> str | None:
    target = target.strip()
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    if target.startswith("/"):
        resolved = target.lstrip("/")
    else:
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source_path), target))
    return resolved.removeprefix("./")


def add_edge(edges, seen, source, edge_type, target, evidence, inferred=False):
    key = (source, edge_type, target, evidence, inferred)
    if key in seen:
        return
    seen.add(key)
    edges.append({
        "from": source,
        "type": edge_type,
        "to": target,
        "evidence": evidence,
        "inferred": inferred,
    })


def main() -> None:
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    if census.get("frozen_commit") != FROZEN_COMMIT or census.get("blob_count") != EXPECTED_FILES:
        raise SystemExit("Frozen census mismatch; refusing to build graph")

    files = census["files"]
    by_path = {f["path"]: f for f in files}
    skill_by_name = {}
    texts = {}

    for f in files:
        text = blob_text(f["sha"])
        texts[f["path"]] = text
        if f["path"].endswith("/SKILL.md"):
            m = re.search(r"^name:\s*[\"']?([^\"'\n]+)", text, re.MULTILINE)
            if m:
                skill_by_name[m.group(1).strip()] = f["path"]

    edges = []
    seen = set()
    unresolved_internal = []

    md_link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    skill_call_re = re.compile(r"(?:Call|call) the Skill tool(?: twice,)?(?: with)?[^\n]*?[\"'`](?:/)?([a-z0-9][a-z0-9-]+)[\"'`]", re.IGNORECASE)
    quoted_skill_re = re.compile(r"[\"'`]([a-z0-9][a-z0-9-]+)[\"'`]")

    for f in files:
        path = f["path"]
        text = texts[path]

        # Physical symlink target.
        if f["mode"] == "120000":
            target = normalize_link(path, text.strip())
            if target and target in by_path:
                add_edge(edges, seen, path, "SYMLINK", target, "git symlink blob target")
            else:
                unresolved_internal.append({"from": path, "raw": text.strip(), "kind": "symlink"})

        # Explicit Markdown links.
        if path.endswith((".md", ".MD")):
            for raw in md_link_re.findall(text):
                target = normalize_link(path, raw)
                if target is None:
                    continue
                if target in by_path:
                    add_edge(edges, seen, path, "DOC_LINK", target, f"markdown link: {raw}")
                else:
                    unresolved_internal.append({"from": path, "raw": raw, "resolved": target, "kind": "markdown-link"})

        # Explicit Skill-tool calls. Capture all quoted skill names on a line that says Skill tool.
        for line in text.splitlines():
            if "Skill tool" not in line:
                continue
            names = [n for n in quoted_skill_re.findall(line) if n in skill_by_name]
            for name in names:
                add_edge(edges, seen, path, "OPERATIVE_CALL", skill_by_name[name], f"Skill tool call: {name}")

        # Codex metadata structurally belongs to the sibling SKILL.md.
        if path.endswith("/agents/openai.yaml"):
            owner = path.removesuffix("/agents/openai.yaml") + "/SKILL.md"
            if owner in by_path:
                add_edge(edges, seen, path, "CONFIG_BINDING", owner, "agents/openai.yaml ownership")

    # Claude plugin distribution entries.
    plugin_path = ".claude-plugin/plugin.json"
    if plugin_path in texts:
        try:
            plugin = json.loads(texts[plugin_path])
            for raw in plugin.get("skills", []):
                target = raw.removeprefix("./").rstrip("/") + "/SKILL.md"
                if target in by_path:
                    add_edge(edges, seen, plugin_path, "DISTRIBUTION_ENTRY", target, f"plugin skills entry: {raw}")
                else:
                    unresolved_internal.append({"from": plugin_path, "raw": raw, "resolved": target, "kind": "plugin-entry"})
        except json.JSONDecodeError as e:
            raise SystemExit(f"Invalid frozen plugin.json: {e}")

    outgoing = defaultdict(list)
    incoming = defaultdict(list)
    for i, edge in enumerate(sorted(edges, key=lambda e: (e["from"], e["type"], e["to"], e["evidence"])), start=1):
        edge["edge_id"] = f"EG-A{i:04d}"
        outgoing[edge["from"]].append(edge)
        incoming[edge["to"]].append(edge)

    payload = {
        "source_repo": SOURCE_REPO,
        "frozen_commit": FROZEN_COMMIT,
        "file_count": len(files),
        "edge_count": len(edges),
        "unresolved_internal_count": len(unresolved_internal),
        "edges": sorted(edges, key=lambda e: e["edge_id"]),
        "unresolved_internal": unresolved_internal,
    }
    EDGES_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Connection Index",
        "",
        f"Frozen source: `{SOURCE_REPO}` @ `{FROZEN_COMMIT}`.",
        "",
        f"Files in denominator: **{len(files)}**. Extracted explicit/structural edges: **{len(edges)}**. Unresolved internal-looking references: **{len(unresolved_internal)}**.",
        "",
        "Generated by `scripts/build_connection_graph.py`. This is an extraction layer, not final semantic verification.",
        "",
        "| MP-ID | Path | Outgoing | Incoming | Extraction state |",
        "|---|---|---:|---:|---|",
    ]
    for f in files:
        path = f["path"]
        lines.append(f"| {f['mp_id']} | `{path}` | {len(outgoing[path])} | {len(incoming[path])} | EXTRACTED |")

    lines += ["", "## Unresolved internal-looking references", ""]
    if unresolved_internal:
        for item in unresolved_internal:
            lines.append(f"- `{item['from']}` → `{item.get('raw','')}` (resolved candidate `{item.get('resolved','')}`; {item['kind']})")
    else:
        lines.append("None from the extraction rules above.")

    INDEX_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {EDGES_JSON} and {INDEX_MD}: {len(edges)} edges, {len(unresolved_internal)} unresolved")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build a deterministic internal connection graph for the frozen mattpocock/skills tree.

This script uses the already-frozen 164-file census as the denominator, fetches each
blob by SHA, and derives source-explicit or structurally deterministic edges.
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
from collections import Counter, defaultdict

SOURCE_REPO = "mattpocock/skills"
FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164
EXPECTED_SKILLS = 37
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
EDGES_JSON = pathlib.Path("03_CONNECTION_EDGES.json")
INDEX_MD = pathlib.Path("03_CONNECTION_INDEX.md")
EXTRACTION_RULES_VERSION = 4


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


def has_source_target_edge(edges, source: str, target: str) -> bool:
    return any(edge["from"] == source and edge["to"] == target for edge in edges)


def unique_basename_regex(name: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z0-9_.-]){re.escape(name)}(?![A-Za-z0-9_.-])")


def skill_label_regex(name: str) -> re.Pattern[str]:
    escaped = re.escape(name)
    return re.compile(
        rf"(?<![A-Za-z0-9_-])(?:/{escaped}|\${escaped}|`{escaped}`)(?![A-Za-z0-9_-])"
    )


def text_without_urls(text: str) -> str:
    """Remove external URL bodies before /skill scanning to avoid path-segment false positives."""
    return re.sub(r"https?://[^\s)>\]\"']+", "", text)


def frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    if end == -1:
        return ""
    return text[4:end]


def invocation_class(skill_text: str, openai_text: str | None) -> dict:
    fm = frontmatter(skill_text)
    claude_user = bool(re.search(r"^disable-model-invocation:\s*true\s*$", fm, re.MULTILINE))
    claude_class = "USER_INVOKED" if claude_user else "MODEL_INVOKED"

    if openai_text is None:
        codex_class = "MISSING_METADATA"
    else:
        implicit_false = bool(
            re.search(r"^\s*allow_implicit_invocation:\s*false\s*$", openai_text, re.MULTILINE)
        )
        codex_class = "USER_INVOKED" if implicit_false else "MODEL_INVOKED"

    consistent = claude_class == codex_class
    effective = claude_class if consistent else "POLICY_MISMATCH"
    return {
        "claude_class": claude_class,
        "codex_class": codex_class,
        "consistent": consistent,
        "effective_class": effective,
    }


def main() -> None:
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    if census.get("frozen_commit") != FROZEN_COMMIT or census.get("blob_count") != EXPECTED_FILES:
        raise SystemExit("Frozen census mismatch; refusing to build graph")

    files = census["files"]
    by_path = {f["path"]: f for f in files}
    skill_by_name: dict[str, str] = {}
    skill_name_by_path: dict[str, str] = {}
    texts: dict[str, str] = {}

    for f in files:
        text = blob_text(f["sha"])
        texts[f["path"]] = text
        if f["path"].endswith("/SKILL.md"):
            m = re.search(r"^name:\s*[\"']?([^\"'\n]+)", text, re.MULTILINE)
            if m:
                name = m.group(1).strip()
                skill_by_name[name] = f["path"]
                skill_name_by_path[f["path"]] = name

    if len(skill_by_name) != EXPECTED_SKILLS:
        raise SystemExit(
            f"Expected {EXPECTED_SKILLS} named SKILL.md files, found {len(skill_by_name)}; refusing policy join"
        )

    invocation_policies = {}
    for name, skill_path in sorted(skill_by_name.items()):
        metadata_path = skill_path.removesuffix("/SKILL.md") + "/agents/openai.yaml"
        policy = invocation_class(texts[skill_path], texts.get(metadata_path))
        invocation_policies[skill_path] = {
            "name": name,
            "skill_path": skill_path,
            "openai_metadata_path": metadata_path if metadata_path in texts else None,
            **policy,
        }

    edges = []
    seen = set()
    unresolved_internal = []

    md_link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    quoted_skill_re = re.compile(r"[\"'`]([a-z0-9][a-z0-9-]+)[\"'`]")

    for f in files:
        path = f["path"]
        text = texts[path]

        if f["mode"] == "120000":
            target = normalize_link(path, text.strip())
            if target and target in by_path:
                add_edge(edges, seen, path, "SYMLINK", target, "git symlink blob target")
            else:
                unresolved_internal.append({"from": path, "raw": text.strip(), "kind": "symlink"})

        if path.endswith((".md", ".MD")):
            for raw in md_link_re.findall(text):
                target = normalize_link(path, raw)
                if target is None:
                    continue
                if target in by_path:
                    add_edge(edges, seen, path, "DOC_LINK", target, f"markdown link: {raw}")
                else:
                    unresolved_internal.append({"from": path, "raw": raw, "resolved": target, "kind": "markdown-link"})

        # Only current skill workflow sources can create operative dependencies.
        # Governance docs, changesets and human docs that mention the Skill tool are
        # evidence about invocation, not executable calls themselves.
        if path.endswith("/SKILL.md"):
            for line in text.splitlines():
                if "Skill tool" not in line:
                    continue
                names = [n for n in quoted_skill_re.findall(line) if n in skill_by_name]
                for name in names:
                    add_edge(edges, seen, path, "OPERATIVE_CALL", skill_by_name[name], f"Skill tool call: {name}")

        if path.endswith("/agents/openai.yaml"):
            owner = path.removesuffix("/agents/openai.yaml") + "/SKILL.md"
            if owner in by_path:
                add_edge(edges, seen, path, "CONFIG_BINDING", owner, "agents/openai.yaml ownership")

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

    basename_to_paths = defaultdict(list)
    for path in by_path:
        basename_to_paths[posixpath.basename(path)].append(path)
    unique_basenames = {
        name: paths[0]
        for name, paths in basename_to_paths.items()
        if len(paths) == 1 and name
    }
    basename_patterns = {name: unique_basename_regex(name) for name in unique_basenames}
    skill_label_patterns = {name: skill_label_regex(name) for name in skill_by_name}

    passive_path_mentions = 0
    passive_basename_mentions = 0
    passive_skill_label_mentions = 0
    for source_path, text in texts.items():
        for target_path in by_path:
            if target_path == source_path or has_source_target_edge(edges, source_path, target_path):
                continue
            if target_path in text:
                add_edge(
                    edges,
                    seen,
                    source_path,
                    "PASSIVE_REFERENCE",
                    target_path,
                    f"exact repository path mention: {target_path}",
                )
                passive_path_mentions += 1

        for basename, target_path in unique_basenames.items():
            if target_path == source_path or has_source_target_edge(edges, source_path, target_path):
                continue
            if basename_patterns[basename].search(text):
                add_edge(
                    edges,
                    seen,
                    source_path,
                    "PASSIVE_REFERENCE",
                    target_path,
                    f"unique filename mention: {basename}",
                )
                passive_basename_mentions += 1

        # Exact skill labels are passive relationships, not operative calls.
        # Supported forms are /name (Claude-style), $name (Codex-style), and
        # an exact backticked skill name. External URL bodies are removed first
        # so path segments such as https://.../research do not become skill edges.
        label_text = text_without_urls(text)
        for name, target_path in skill_by_name.items():
            if target_path == source_path or has_source_target_edge(edges, source_path, target_path):
                continue
            match = skill_label_patterns[name].search(label_text)
            if match:
                add_edge(
                    edges,
                    seen,
                    source_path,
                    "SKILL_REFERENCE",
                    target_path,
                    f"exact skill label: {match.group(0)}",
                )
                passive_skill_label_mentions += 1

    # Join current operative calls against both harness invocation policies.
    illegal_operative_calls = []
    for edge in edges:
        if edge["type"] != "OPERATIVE_CALL":
            continue
        target_policy = invocation_policies.get(edge["to"])
        if target_policy is None:
            edge["target_invocation"] = "UNKNOWN"
            edge["invocation_legal"] = False
            illegal_operative_calls.append({**edge, "reason": "target policy missing"})
            continue
        edge["target_invocation"] = target_policy["effective_class"]
        edge["invocation_legal"] = target_policy["effective_class"] == "MODEL_INVOKED"
        if not edge["invocation_legal"]:
            illegal_operative_calls.append(
                {
                    **edge,
                    "reason": (
                        "operative Skill-tool calls may target only model-invoked skills; "
                        f"target is {target_policy['effective_class']}"
                    ),
                }
            )

    sorted_edges = sorted(edges, key=lambda e: (e["from"], e["type"], e["to"], e["evidence"]))
    outgoing = defaultdict(list)
    incoming = defaultdict(list)
    operative_incoming = defaultdict(list)
    for i, edge in enumerate(sorted_edges, start=1):
        edge["edge_id"] = f"EG-A{i:04d}"
        outgoing[edge["from"]].append(edge)
        incoming[edge["to"]].append(edge)
        if edge["type"] == "OPERATIVE_CALL":
            operative_incoming[edge["to"]].append(edge)

    edge_type_counts = Counter(edge["type"] for edge in sorted_edges)
    effective_policy_counts = Counter(
        policy["effective_class"] for policy in invocation_policies.values()
    )
    policy_mismatches = [
        policy for policy in invocation_policies.values() if not policy["consistent"]
    ]

    payload = {
        "source_repo": SOURCE_REPO,
        "frozen_commit": FROZEN_COMMIT,
        "file_count": len(files),
        "skill_count": len(invocation_policies),
        "extraction_rules_version": EXTRACTION_RULES_VERSION,
        "edge_count": len(sorted_edges),
        "edge_type_counts": dict(sorted(edge_type_counts.items())),
        "passive_path_mention_count": passive_path_mentions,
        "passive_unique_basename_mention_count": passive_basename_mentions,
        "passive_skill_label_mention_count": passive_skill_label_mentions,
        "unique_basename_count": len(unique_basenames),
        "invocation_policy_counts": dict(sorted(effective_policy_counts.items())),
        "invocation_policy_mismatch_count": len(policy_mismatches),
        "illegal_operative_call_count": len(illegal_operative_calls),
        "invocation_policies": sorted(invocation_policies.values(), key=lambda p: p["skill_path"]),
        "illegal_operative_calls": illegal_operative_calls,
        "unresolved_internal_count": len(unresolved_internal),
        "edges": sorted_edges,
        "unresolved_internal": unresolved_internal,
    }
    EDGES_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    type_summary = ", ".join(f"{name}={count}" for name, count in sorted(edge_type_counts.items()))
    policy_summary = ", ".join(
        f"{name}={count}" for name, count in sorted(effective_policy_counts.items())
    )
    lines = [
        "# Connection Index",
        "",
        f"Frozen source: `{SOURCE_REPO}` @ `{FROZEN_COMMIT}`.",
        "",
        f"Extraction rules version: **{EXTRACTION_RULES_VERSION}**.",
        "",
        f"Files in denominator: **{len(files)}**. Extracted explicit/structural/passive edges: **{len(sorted_edges)}**. Unresolved internal-looking references: **{len(unresolved_internal)}**.",
        "",
        f"Edge types: {type_summary}.",
        "",
        f"Passive-reference scan: **{passive_path_mentions}** exact-path mentions + **{passive_basename_mentions}** unique-filename mentions + **{passive_skill_label_mentions}** exact skill-label mentions; **{len(unique_basenames)}** globally unique basenames were eligible.",
        "",
        f"Invocation-policy join: **{len(invocation_policies)}** skills; {policy_summary}; policy mismatches **{len(policy_mismatches)}**; illegal current operative calls **{len(illegal_operative_calls)}**.",
        "",
        "Generated by `scripts/build_connection_graph.py`. This is an extraction layer, not final semantic verification.",
        "",
        "| MP-ID | Path | Outgoing | Incoming | Extraction state |",
        "|---|---|---:|---:|---|",
    ]
    for f in files:
        path = f["path"]
        lines.append(f"| {f['mp_id']} | `{path}` | {len(outgoing[path])} | {len(incoming[path])} | EXTRACTED |")

    lines += ["", "## Invocation policy join", ""]
    lines += [
        "| Skill | Claude | Codex | Consistent | Incoming operative calls |",
        "|---|---|---|---|---:|",
    ]
    for policy in sorted(invocation_policies.values(), key=lambda p: p["skill_path"]):
        lines.append(
            f"| `{policy['skill_path']}` | {policy['claude_class']} | {policy['codex_class']} | "
            f"{'YES' if policy['consistent'] else 'NO'} | {len(operative_incoming[policy['skill_path']])} |"
        )

    lines += ["", "### Illegal current operative calls", ""]
    if illegal_operative_calls:
        for item in illegal_operative_calls:
            lines.append(
                f"- `{item['from']}` → `{item['to']}` — {item['reason']} ({item['evidence']})"
            )
    else:
        lines.append("None detected among current `SKILL.md` Skill-tool calls.")

    lines += ["", "## Unresolved internal-looking references", ""]
    if unresolved_internal:
        for item in unresolved_internal:
            lines.append(f"- `{item['from']}` → `{item.get('raw','')}` (resolved candidate `{item.get('resolved','')}`; {item['kind']})")
    else:
        lines.append("None from the extraction rules above.")

    INDEX_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"Wrote {EDGES_JSON} and {INDEX_MD}: {len(sorted_edges)} edges, "
        f"{len(unresolved_internal)} unresolved, "
        f"passive={passive_path_mentions + passive_basename_mentions + passive_skill_label_mentions}, "
        f"policy_mismatches={len(policy_mismatches)}, illegal_calls={len(illegal_operative_calls)}"
    )


if __name__ == "__main__":
    main()

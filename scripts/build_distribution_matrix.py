#!/usr/bin/env python3
"""Build per-skill distribution/visibility symmetry for the frozen skills tree."""
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
EXPECTED_SKILLS = 37
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
OUT_JSON = pathlib.Path("03_DISTRIBUTION_MATRIX.json")
OUT_MD = pathlib.Path("03_DISTRIBUTION_MATRIX.md")


def github_json(url: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "matt-pocock-forensic-distribution-builder",
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
    return base64.b64decode(data["content"]).decode("utf-8", errors="replace")


def skill_name(text: str) -> str | None:
    m = re.search(r"^name:\s*[\"']?([^\"'\n]+)", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def invocation_class(text: str) -> str:
    return "USER_INVOKED" if re.search(
        r"^disable-model-invocation:\s*true\s*$", text, re.MULTILINE
    ) else "MODEL_INVOKED"


def token_pattern(name: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(name)}(?![A-Za-z0-9_-])")


def slash_pattern(name: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z0-9_-])/{re.escape(name)}(?![A-Za-z0-9_-])")


def bucket_for(path: str) -> str:
    parts = path.split("/")
    if len(parts) < 4 or parts[0] != "skills":
        raise ValueError(path)
    return parts[1]


def main() -> None:
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    if census.get("frozen_commit") != FROZEN_COMMIT or census.get("blob_count") != EXPECTED_FILES:
        raise SystemExit("Frozen census mismatch; refusing distribution build")

    files = census["files"]
    by_path = {f["path"]: f for f in files}
    required = [
        ".claude-plugin/plugin.json",
        "README.md",
        "scripts/link-skills.sh",
        "scripts/list-skills.sh",
        "skills/engineering/README.md",
        "skills/productivity/README.md",
        "skills/in-progress/README.md",
        "skills/misc/README.md",
        "skills/engineering/ask-matt/SKILL.md",
    ]
    missing_required = [p for p in required if p not in by_path]
    if missing_required:
        raise SystemExit(f"Required frozen files missing: {missing_required}")

    cache: dict[str, str] = {}
    def text(path: str) -> str:
        if path not in cache:
            cache[path] = blob_text(by_path[path]["sha"])
        return cache[path]

    skills = []
    for f in files:
        path = f["path"]
        if not path.endswith("/SKILL.md"):
            continue
        st = text(path)
        name = skill_name(st)
        if not name:
            raise SystemExit(f"Missing skill name: {path}")
        skills.append({
            "name": name,
            "path": path,
            "mp_id": f["mp_id"],
            "bucket": bucket_for(path),
            "invocation": invocation_class(st),
        })
    if len(skills) != EXPECTED_SKILLS:
        raise SystemExit(f"Expected {EXPECTED_SKILLS} skills, found {len(skills)}")

    plugin = json.loads(text(".claude-plugin/plugin.json"))
    plugin_set = {
        raw.removeprefix("./").rstrip("/") + "/SKILL.md"
        for raw in plugin.get("skills", [])
    }

    link_script = text("scripts/link-skills.sh")
    if "-not -path '*/deprecated/*'" not in link_script or "-not -path '*/misc/*'" not in link_script:
        raise SystemExit("link-skills exclusion semantics changed; review parser")
    local_link_set = {
        row["path"] for row in skills if row["bucket"] not in {"deprecated", "misc"}
    }

    list_script = text("scripts/list-skills.sh")
    if "find . -name SKILL.md" not in list_script or "deprecated" in list_script or "misc" in list_script:
        raise SystemExit("list-skills semantics changed; review parser")
    list_visible_set = {row["path"] for row in skills}

    root_readme = text("README.md")
    bucket_readmes = {
        bucket: text(f"skills/{bucket}/README.md")
        for bucket in {row["bucket"] for row in skills}
    }
    ask_text = text("skills/engineering/ask-matt/SKILL.md")

    rows = []
    for row in sorted(skills, key=lambda r: r["path"]):
        name = row["name"]
        path = row["path"]
        bucket = row["bucket"]
        metadata_path = path.removesuffix("/SKILL.md") + "/agents/openai.yaml"
        docs_path = f"docs/{bucket}/{name}.md"
        rows.append({
            **row,
            "plugin_promoted": path in plugin_set,
            "local_linked": path in local_link_set,
            "list_skills_visible": path in list_visible_set,
            "root_readme_visible": bool(token_pattern(name).search(root_readme)),
            "bucket_readme_visible": bool(token_pattern(name).search(bucket_readmes[bucket])),
            "docs_page_exists": docs_path in by_path,
            "ask_matt_router_visible": bool(slash_pattern(name).search(ask_text)),
            "codex_metadata_exists": metadata_path in by_path,
        })

    promoted = [r for r in rows if r["plugin_promoted"]]
    expected_router = [r for r in promoted if r["name"] != "ask-matt"]
    checks = {
        "promoted_missing_local_link": [r["path"] for r in promoted if not r["local_linked"]],
        "promoted_missing_list_visibility": [r["path"] for r in promoted if not r["list_skills_visible"]],
        "promoted_missing_root_readme": [r["path"] for r in promoted if not r["root_readme_visible"]],
        "promoted_missing_bucket_readme": [r["path"] for r in promoted if not r["bucket_readme_visible"]],
        "promoted_missing_docs_page": [r["path"] for r in promoted if not r["docs_page_exists"]],
        "promoted_missing_codex_metadata": [r["path"] for r in promoted if not r["codex_metadata_exists"]],
        "promoted_missing_router": [r["path"] for r in expected_router if not r["ask_matt_router_visible"]],
        "nonpromoted_unexpected_plugin": [r["path"] for r in rows if r["bucket"] in {"in-progress", "misc"} and r["plugin_promoted"]],
        "misc_unexpected_local_link": [r["path"] for r in rows if r["bucket"] == "misc" and r["local_linked"]],
        "nonpromoted_unexpected_router": [r["path"] for r in rows if not r["plugin_promoted"] and r["ask_matt_router_visible"]],
    }
    anomaly_count = sum(len(v) for v in checks.values())

    counts = {
        key: sum(1 for row in rows if row[key])
        for key in [
            "plugin_promoted",
            "local_linked",
            "list_skills_visible",
            "root_readme_visible",
            "bucket_readme_visible",
            "docs_page_exists",
            "ask_matt_router_visible",
            "codex_metadata_exists",
        ]
    }
    bucket_counts = Counter(r["bucket"] for r in rows)

    payload = {
        "source_repo": SOURCE_REPO,
        "frozen_commit": FROZEN_COMMIT,
        "skill_count": len(rows),
        "bucket_counts": dict(sorted(bucket_counts.items())),
        "dimension_counts": counts,
        "anomaly_count": anomaly_count,
        "checks": checks,
        "rows": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Distribution Symmetry Matrix",
        "",
        f"Frozen source: `{SOURCE_REPO}` @ `{FROZEN_COMMIT}`.",
        "",
        f"Current skills: **{len(rows)}**. Automated symmetry anomalies: **{anomaly_count}**.",
        "",
        "Dimension counts:",
        "",
    ]
    for key, value in counts.items():
        lines.append(f"- `{key}`: **{value}**")
    lines += [
        "",
        "| Skill | Bucket | Plugin | Local link | List | Root README | Bucket README | Docs | Ask-matt | Codex metadata |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        yn = lambda key: "YES" if r[key] else "NO"
        lines.append(
            f"| `{r['name']}` | {r['bucket']} | {yn('plugin_promoted')} | {yn('local_linked')} | "
            f"{yn('list_skills_visible')} | {yn('root_readme_visible')} | {yn('bucket_readme_visible')} | "
            f"{yn('docs_page_exists')} | {yn('ask_matt_router_visible')} | {yn('codex_metadata_exists')} |"
        )

    lines += ["", "## Symmetry checks", ""]
    for key, paths in checks.items():
        lines.append(f"### {key}")
        if paths:
            lines.extend(f"- `{p}`" for p in paths)
        else:
            lines.append("None.")
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"distribution counts={counts}; anomalies={anomaly_count}")


if __name__ == "__main__":
    main()

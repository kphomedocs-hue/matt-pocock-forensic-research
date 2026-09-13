#!/usr/bin/env python3
"""Build exact ask-matt router coverage against the frozen promoted skill set."""
from __future__ import annotations

import base64
import json
import os
import pathlib
import re
import urllib.request

SOURCE_REPO = "mattpocock/skills"
FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
EXPECTED_FILES = 164
EXPECTED_SKILLS = 37
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
OUT_JSON = pathlib.Path("03_ROUTER_MATRIX.json")
OUT_MD = pathlib.Path("03_ROUTER_MATRIX.md")
ASK_MATT = "skills/engineering/ask-matt/SKILL.md"
PLUGIN = ".claude-plugin/plugin.json"


def github_json(url: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "matt-pocock-forensic-router-builder",
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
    if re.search(r"^disable-model-invocation:\s*true\s*$", text, re.MULTILINE):
        return "USER_INVOKED"
    return "MODEL_INVOKED"


def slash_label_pattern(name: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z0-9_-])/{re.escape(name)}(?![A-Za-z0-9_-])")


def main() -> None:
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    if census.get("frozen_commit") != FROZEN_COMMIT or census.get("blob_count") != EXPECTED_FILES:
        raise SystemExit("Frozen census mismatch; refusing router build")

    files = census["files"]
    by_path = {f["path"]: f for f in files}
    if ASK_MATT not in by_path or PLUGIN not in by_path:
        raise SystemExit("Required ask-matt/plugin paths missing from frozen census")

    skill_rows = []
    by_name = {}
    by_skill_path = {}
    for f in files:
        path = f["path"]
        if not path.endswith("/SKILL.md"):
            continue
        text = blob_text(f["sha"])
        name = skill_name(text)
        if not name:
            raise SystemExit(f"Missing skill name in {path}")
        row = {
            "name": name,
            "path": path,
            "mp_id": f["mp_id"],
            "invocation": invocation_class(text),
        }
        skill_rows.append(row)
        by_name[name] = row
        by_skill_path[path] = row

    if len(skill_rows) != EXPECTED_SKILLS:
        raise SystemExit(f"Expected {EXPECTED_SKILLS} skills, found {len(skill_rows)}")

    ask_text = blob_text(by_path[ASK_MATT]["sha"])
    plugin = json.loads(blob_text(by_path[PLUGIN]["sha"]))
    promoted_paths = {
        raw.removeprefix("./").rstrip("/") + "/SKILL.md"
        for raw in plugin.get("skills", [])
    }
    if len(promoted_paths) != 25:
        raise SystemExit(f"Expected 25 promoted plugin skills, found {len(promoted_paths)}")
    if not promoted_paths.issubset(by_skill_path):
        raise SystemExit("Plugin contains a target that is not a current SKILL.md")

    router_names = {
        name
        for name in by_name
        if slash_label_pattern(name).search(ask_text)
    }
    router_paths = {by_name[name]["path"] for name in router_names}

    expected_targets = promoted_paths - {ASK_MATT}
    routed_promoted = router_paths & expected_targets
    missing_promoted = expected_targets - router_paths
    extra_nonpromoted = router_paths - promoted_paths

    rows = []
    for row in sorted(skill_rows, key=lambda r: r["path"]):
        path = row["path"]
        rows.append({
            **row,
            "promoted": path in promoted_paths,
            "expected_router_target": path in expected_targets,
            "router_mentions": path in router_paths,
        })

    payload = {
        "source_repo": SOURCE_REPO,
        "frozen_commit": FROZEN_COMMIT,
        "current_skill_count": len(skill_rows),
        "promoted_skill_count": len(promoted_paths),
        "expected_promoted_router_targets": len(expected_targets),
        "router_skill_mentions": len(router_paths),
        "promoted_targets_routed": len(routed_promoted),
        "missing_promoted_targets": sorted(missing_promoted),
        "extra_nonpromoted_targets": sorted(extra_nonpromoted),
        "rows": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Ask-Matt Router Matrix",
        "",
        f"Frozen source: `{SOURCE_REPO}` @ `{FROZEN_COMMIT}`.",
        "",
        f"Current skills: **{len(skill_rows)}**. Promoted plugin skills: **{len(promoted_paths)}**.",
        "",
        f"Expected promoted targets other than ask-matt itself: **{len(expected_targets)}**.",
        "",
        f"Exact `/skill-name` targets mentioned by ask-matt: **{len(router_paths)}**.",
        "",
        f"Promoted targets covered: **{len(routed_promoted)}/{len(expected_targets)}**.",
        "",
        f"Missing promoted targets: **{len(missing_promoted)}**. Extra non-promoted targets: **{len(extra_nonpromoted)}**.",
        "",
        "This matrix treats slash-labelled skill names as router references, not operative Skill-tool calls.",
        "",
        "| Skill | MP-ID | Invocation | Promoted | Expected router target | Mentioned by ask-matt |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['name']}` | {row['mp_id']} | {row['invocation']} | "
            f"{'YES' if row['promoted'] else 'NO'} | "
            f"{'YES' if row['expected_router_target'] else 'NO'} | "
            f"{'YES' if row['router_mentions'] else 'NO'} |"
        )

    lines += ["", "## Missing promoted router targets", ""]
    if missing_promoted:
        lines.extend(f"- `{path}`" for path in sorted(missing_promoted))
    else:
        lines.append("None.")

    lines += ["", "## Extra non-promoted router targets", ""]
    if extra_nonpromoted:
        lines.extend(f"- `{path}`" for path in sorted(extra_nonpromoted))
    else:
        lines.append("None.")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"router: promoted={len(promoted_paths)} expected={len(expected_targets)} "
        f"covered={len(routed_promoted)} missing={len(missing_promoted)} extras={len(extra_nonpromoted)}"
    )


if __name__ == "__main__":
    main()

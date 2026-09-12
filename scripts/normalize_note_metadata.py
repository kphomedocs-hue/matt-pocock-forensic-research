#!/usr/bin/env python3
"""Insert missing canonical provenance metadata into durable file notes.

The script is deliberately narrow: it never changes Status, evidence prose, observations,
connections, or conclusions. It only inserts exact Frozen commit and Category fields from
the authoritative census when those canonical lines are absent.
"""
from __future__ import annotations

import json
import pathlib
import re

FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"
CENSUS = pathlib.Path("01_FILE_CENSUS.json")
NOTES = pathlib.Path("02_FILE_NOTES")

STATUS_LINE = re.compile(r"^(?:-\s*)?Status:.*$", re.M)
DIRECT_COMMIT = re.compile(r"^(?:-\s*)?Frozen commit:\s*`?[0-9a-f]{40}`?\s*$", re.M)
CATEGORY = re.compile(r"^(?:-\s*)?Category:\s*.+$", re.M)


def insert_after_status(text: str, lines: list[str]) -> str:
    m = STATUS_LINE.search(text)
    if not m:
        raise SystemExit("Cannot normalize note without Status line")
    insert_at = m.end()
    return text[:insert_at] + "\n" + "\n".join(lines) + text[insert_at:]


def main() -> None:
    census = json.loads(CENSUS.read_text(encoding="utf-8"))
    changed = []
    for item in census["files"]:
        note = NOTES / f"{item['mp_id']}.md"
        text = note.read_text(encoding="utf-8")
        additions = []
        if not DIRECT_COMMIT.search(text):
            additions.append(f"- Frozen commit: `{FROZEN_COMMIT}`")
        if not CATEGORY.search(text):
            additions.append(f"- Category: {item['category']}")
        if additions:
            new_text = insert_after_status(text, additions)
            note.write_text(new_text, encoding="utf-8")
            changed.append(str(note))
    print(f"Normalized {len(changed)} notes")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()

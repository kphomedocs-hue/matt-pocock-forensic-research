#!/usr/bin/env python3
"""Verify every SHA-256 fingerprint recorded in the Phase 3 build manifest."""
from __future__ import annotations

import hashlib
import json
import pathlib

MANIFEST = pathlib.Path("03_PHASE3_BUILD_MANIFEST.json")
FROZEN_COMMIT = "3cca18b368ae95cdbdebbff572ccafa662551015"


def digest(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("frozen_commit") != FROZEN_COMMIT:
        raise SystemExit("Phase 3 manifest schema/baseline mismatch")
    checked = 0
    for section in ("input_fingerprints", "output_fingerprints"):
        mapping = data.get(section)
        if not isinstance(mapping, dict) or not mapping:
            raise SystemExit(f"Manifest section missing/empty: {section}")
        for raw, meta in mapping.items():
            path = pathlib.Path(raw)
            if not path.exists():
                raise SystemExit(f"Manifest path missing: {path}")
            actual = digest(path)
            if actual != meta.get("sha256"):
                raise SystemExit(f"Manifest SHA-256 mismatch: {path}")
            if path.stat().st_size != meta.get("bytes"):
                raise SystemExit(f"Manifest byte-size mismatch: {path}")
            checked += 1
    print(f"phase3 manifest verified: fingerprints={checked}")


if __name__ == "__main__":
    main()

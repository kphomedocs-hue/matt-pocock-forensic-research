#!/usr/bin/env python3
"""Validate draft documentary mappings, NOT truth, approvals or work readiness.

Standard-library checker for the local contract in 19_MINIMUM_EVIDENCE_SCHEMA.md.
This is not a JSON Schema implementation and performs no remote operations.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import re
import subprocess

SNAPSHOT = {
    "repository": "kphomedocs-hue/matt-pocock-forensic-research",
    "commit": "48dcfb47a8153e69316d9f6d47bee02b8b44ae8e",
}
PINS = {
    "labels": {"path": "04_B024_GITHUB_LABEL_RUNTIME_RESULTS.json",
               "blob_sha": "ce8106b6f5746a856e01ac4f24dd31806d337ab7"},
    "linter": {"path": "04_SCAFFOLD_EXERCISES_LINTER_RESULTS.json",
               "blob_sha": "5b0c7d0a6ca8f33c8af30e514b900fa896bd9596"},
    "grep": {"path": "04_CT019_REPRODUCTION.json",
             "blob_sha": "96f4e798dd8a6a778eca8f8ce0e865367bb5a329"},
    "matrix": {"path": "04_BEHAVIOR_MATRIX.json",
               "blob_sha": "255ba6e696169caa241f1f03108af8e4000cc20b"},
}
METHOD_FIELDS = {
    "owner", "contributors", "reviewer", "specification_approval",
    "criteria_preapproval", "event_times", "transition_history",
    "specification_fidelity_review", "quality_and_standards_review",
    "operational_readiness_review",
}
RECORD_FIELDS = {
    "record_id", "subject_id", "mode", "question", "inputs", "checks",
    "conclusion", "limits", "next_action", "method_evidence", "adoption_status",
}


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def git_blob(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def parse_json(text):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    def reject_constant(value):
        raise ValueError("Non-JSON constant: " + value)
    return json.loads(text, object_pairs_hook=unique, parse_constant=reject_constant)


def resolve(document, pointer):
    if not isinstance(pointer, str) or (pointer and not pointer.startswith("/")):
        raise ValueError("Invalid pointer")
    if not pointer:
        return document
    for token in pointer[1:].split("/"):
        if re.search(r"~(?![01])", token):
            raise ValueError("Invalid pointer escape")
        key = token.replace("~1", "/").replace("~0", "~")
        if isinstance(document, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", key):
                raise ValueError("Invalid array index")
            document = document[int(key)]
        elif isinstance(document, dict):
            document = document[key]
        else:
            raise ValueError("Pointer traverses a scalar")
    return document


def check_statement(value, sources):
    if not isinstance(value, dict) or set(value) != {"basis", "value", "evidence", "reason"}:
        return ["STATEMENT_SHAPE"]
    errors = []
    basis, evidence = value["basis"], value["evidence"]
    if not nonblank(value["reason"]):
        errors.append("REASON_REQUIRED")
    if not isinstance(evidence, list):
        return errors + ["EVIDENCE_SHAPE"]
    resolved = []
    for ref in evidence:
        try:
            if not isinstance(ref, dict) or set(ref) != {"source", "pointer"}:
                raise ValueError("Reference shape")
            if not isinstance(ref["source"], str):
                raise ValueError("Reference source")
            resolved.append(resolve(sources[ref["source"]], ref["pointer"]))
        except (KeyError, IndexError, TypeError, ValueError):
            errors.append("EVIDENCE_REFERENCE")
    if basis == "UNKNOWN":
        if value["value"] is not None or evidence:
            errors.append("UNKNOWN_HAS_CLAIM")
    elif basis == "RECORDED":
        if len(evidence) != 1 or len(resolved) != 1:
            errors.append("RECORDED_REFERENCE")
        elif json.dumps(value["value"], sort_keys=True) != json.dumps(resolved[0], sort_keys=True):
            errors.append("RECORDED_VALUE_MISMATCH")
    elif basis == "INFERRED":
        if not nonblank(value["value"]) or not evidence:
            errors.append("INFERENCE_BASIS")
    else:
        errors.append("BASIS")
    return errors


def validate(bundle, sources):
    """Validate structure and source-value equality, never judge evidence truth."""
    if not isinstance(bundle, dict) or set(bundle) != {
            "artifact", "version", "status", "snapshot", "source_catalog", "records"}:
        return ["BUNDLE_SHAPE"]
    errors = []
    for key, expected in (("artifact", "MINIMUM_EVIDENCE_DRAFT_EXAMPLES"),
                          ("version", "0.1-draft"), ("status", "DRAFT_NOT_ADOPTED"),
                          ("snapshot", SNAPSHOT), ("source_catalog", PINS)):
        if bundle.get(key) != expected:
            errors.append("BUNDLE_" + key.upper())
    records = bundle["records"]
    if not isinstance(records, list) or not records:
        return errors + ["RECORDS"]
    record_ids = set()
    for index, record in enumerate(records):
        prefix = f"record[{index}]:"
        if not isinstance(record, dict) or set(record) != RECORD_FIELDS:
            errors.append(prefix + "RECORD_SHAPE")
            continue
        for key in ("record_id", "subject_id"):
            if not nonblank(record[key]):
                errors.append(prefix + "ID")
        rid = record["record_id"]
        if isinstance(rid, str):
            if rid in record_ids:
                errors.append(prefix + "DUPLICATE_RECORD")
            record_ids.add(rid)
        if record["mode"] != "RETROSPECTIVE" or record["adoption_status"] != "NOT_ESTABLISHED":
            errors.append(prefix + "SCOPE_ESCALATION")
        for key in ("question", "conclusion", "next_action"):
            errors.extend(prefix + key + ":" + e for e in check_statement(record[key], sources))
        inputs = record["inputs"]
        if not isinstance(inputs, list) or not inputs:
            errors.append(prefix + "INPUTS")
        else:
            for item in inputs:
                errors.extend(prefix + "input:" + e for e in check_statement(item, sources))
        limits = record["limits"]
        if not isinstance(limits, list) or not limits or not all(nonblank(x) for x in limits):
            errors.append(prefix + "LIMITS")
        checks = record["checks"]
        if not isinstance(checks, list) or not checks:
            errors.append(prefix + "CHECKS")
        else:
            seen = set()
            for check in checks:
                if not isinstance(check, dict) or set(check) != {
                        "check_id", "criterion", "observation", "reported_outcome"}:
                    errors.append(prefix + "CHECK_SHAPE")
                    continue
                cid = check["check_id"]
                if not nonblank(cid):
                    errors.append(prefix + "CHECK_ID")
                elif cid in seen:
                    errors.append(prefix + "DUPLICATE_CHECK")
                else:
                    seen.add(cid)
                for key in ("criterion", "observation", "reported_outcome"):
                    errors.extend(prefix + key + ":" + e for e in check_statement(check[key], sources))
        method = record["method_evidence"]
        if not isinstance(method, dict) or set(method) != METHOD_FIELDS:
            errors.append(prefix + "METHOD_FIELDS")
        else:
            for key, value in method.items():
                errors.extend(prefix + key + ":" + e for e in check_statement(value, sources))
                if isinstance(value, dict) and value.get("basis") == "INFERRED":
                    errors.append(prefix + key + ":METHOD_INFERENCE_FORBIDDEN")
    return errors


def snapshot_bytes(root, pin):
    # Full checkouts read the frozen commit, not today's potentially changed files.
    # Outside Git, a fetched snapshot directory is accepted only if its hashes match.
    if (root / ".git").exists():
        result = subprocess.run(
            ["git", "-C", str(root), "show", SNAPSHOT["commit"] + ":" + pin["path"]],
            capture_output=True, check=True)
        return result.stdout
    path = root / pin["path"]
    if path.is_symlink() or not path.is_file():
        raise ValueError("Missing snapshot file or symlink")
    return path.read_bytes()


def load_sources(root):
    sources, errors = {}, []
    root = root.resolve()
    for source, pin in PINS.items():
        try:
            data = snapshot_bytes(root, pin)
            if git_blob(data) != pin["blob_sha"]:
                raise ValueError("Changed snapshot bytes")
            sources[source] = parse_json(data.decode("utf-8"))
        except (OSError, ValueError, UnicodeError, subprocess.CalledProcessError) as exc:
            errors.append(f"SOURCE:{source}:{exc}")
    return sources, errors


def main():
    root = pathlib.Path(__file__).resolve().parents[1]
    sources, errors = load_sources(root)
    bundle = None
    try:
        path = root / "19_EVIDENCE_RECORD_EXAMPLES.json"
        if path.is_symlink():
            raise ValueError("Example file must not be a symlink")
        bundle = parse_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        errors.append("EXAMPLES:" + str(exc))
    if not errors:
        errors.extend(validate(bundle, sources))
    valid = not errors
    unknowns = (sum(v["basis"] == "UNKNOWN" for r in bundle["records"]
                    for v in r["method_evidence"].values()) if valid else None)
    print(json.dumps({
        "artifact": "EVIDENCE_DRAFT_MAPPING_VALIDATION",
        "snapshot": SNAPSHOT, "hard_errors": errors,
        "records_checked": len(bundle["records"]) if valid else None,
        "unknown_method_fields": unknowns,
        "claim": "Documentary shape and value mappings only",
        "method_adoption": "NOT_ESTABLISHED",
        "human_trial_claimed": False,
    }, indent=2))
    raise SystemExit(0 if valid else 1)


if __name__ == "__main__":
    main()

"""Regression tests for the draft contract; no historical experiments are rerun."""
from copy import deepcopy
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_evidence_draft import (
    PINS, SNAPSHOT, load_sources, parse_json, resolve, snapshot_bytes, validate,
)

SOURCES, SOURCE_ERRORS = load_sources(ROOT)
BUNDLE = parse_json((ROOT / "19_EVIDENCE_RECORD_EXAMPLES.json").read_text())


class EvidenceDraftTests(unittest.TestCase):
    def reject(self, data, code):
        errors = validate(data, SOURCES)
        self.assertTrue(any(e.endswith(code) for e in errors), (code, errors))

    def test_positive_bundle_and_source_pins(self):
        self.assertEqual(SOURCE_ERRORS, [])
        self.assertEqual(validate(BUNDLE, SOURCES), [])
        self.assertEqual(len(BUNDLE["records"]), 3)

    def test_cli_keeps_thirty_unknowns_and_no_adoption(self):
        result = subprocess.run([sys.executable, "scripts/validate_evidence_draft.py"],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = parse_json(result.stdout)
        self.assertEqual(output["unknown_method_fields"], 30)
        self.assertEqual(output["method_adoption"], "NOT_ESTABLISHED")
        self.assertFalse(output["human_trial_claimed"])

    def test_unknown_cannot_hide_claim_or_evidence(self):
        for key, value in (("value", "Approved"), ("evidence", [{"source": "grep", "pointer": "/conclusion"}])):
            data = deepcopy(BUNDLE)
            data["records"][0]["method_evidence"]["owner"][key] = value
            self.reject(data, "UNKNOWN_HAS_CLAIM")

    def test_unknown_reason_required(self):
        data = deepcopy(BUNDLE)
        data["records"][0]["method_evidence"]["owner"]["reason"] = " "
        self.reject(data, "REASON_REQUIRED")

    def test_changed_recorded_outcome_rejected_for_each_check(self):
        for i, record in enumerate(BUNDLE["records"]):
            for j in range(len(record["checks"])):
                with self.subTest(record=i, check=j):
                    data = deepcopy(BUNDLE)
                    data["records"][i]["checks"][j]["reported_outcome"]["value"] = "Invented"
                    self.reject(data, "RECORDED_VALUE_MISMATCH")

    def test_boolean_is_not_integer_evidence(self):
        data = deepcopy(BUNDLE)
        data["records"][0]["checks"][0]["reported_outcome"]["value"] = 1
        self.reject(data, "RECORDED_VALUE_MISMATCH")

    def test_missing_or_broken_reference(self):
        for refs, code in (([], "RECORDED_REFERENCE"),
                           ([{"source": "missing", "pointer": ""}], "EVIDENCE_REFERENCE"),
                           ([{"source": "grep", "pointer": "/does-not-exist"}], "EVIDENCE_REFERENCE")):
            data = deepcopy(BUNDLE)
            data["records"][0]["question"]["evidence"] = refs
            self.reject(data, code)

    def test_inference_requires_sources_and_reason(self):
        data = deepcopy(BUNDLE)
        stmt = data["records"][2]["checks"][0]["criterion"]
        stmt["evidence"] = []
        self.reject(data, "INFERENCE_BASIS")
        stmt["reason"] = ""
        self.reject(data, "REASON_REQUIRED")

    def test_inference_cannot_supply_method_authorization(self):
        data = deepcopy(BUNDLE)
        data["records"][0]["method_evidence"]["owner"] = deepcopy(
            data["records"][2]["checks"][0]["criterion"])
        self.reject(data, "METHOD_INFERENCE_FORBIDDEN")

    def test_missing_method_field_rejected(self):
        data = deepcopy(BUNDLE)
        del data["records"][0]["method_evidence"]["reviewer"]
        self.reject(data, "METHOD_FIELDS")

    def test_scope_escalation_rejected(self):
        for key, value in (("adoption_status", "ACCEPTED"), ("mode", "HUMAN_TRIAL")):
            data = deepcopy(BUNDLE)
            data["records"][0][key] = value
            self.reject(data, "SCOPE_ESCALATION")
        data = deepcopy(BUNDLE)
        data["status"] = "ADOPTED"
        self.reject(data, "BUNDLE_STATUS")

    def test_duplicate_record_and_check_ids_rejected(self):
        data = deepcopy(BUNDLE)
        data["records"].append(deepcopy(data["records"][0]))
        self.reject(data, "DUPLICATE_RECORD")
        data = deepcopy(BUNDLE)
        data["records"][0]["checks"].append(deepcopy(data["records"][0]["checks"][0]))
        self.reject(data, "DUPLICATE_CHECK")

    def test_snapshot_and_source_catalog_cannot_silently_drift(self):
        data = deepcopy(BUNDLE)
        data["snapshot"]["commit"] = "0" * 40
        self.reject(data, "BUNDLE_SNAPSHOT")
        data = deepcopy(BUNDLE)
        data["source_catalog"]["grep"]["path"] = "../outside.json"
        self.reject(data, "BUNDLE_SOURCE_CATALOG")

    def test_missing_limits_rejected(self):
        data = deepcopy(BUNDLE)
        data["records"][0]["limits"] = []
        self.reject(data, "LIMITS")

    def test_bad_shapes_do_not_crash(self):
        for value in (None, [], 3, "text"):
            self.reject(value, "BUNDLE_SHAPE")
        data = deepcopy(BUNDLE)
        data["records"][0]["question"] = None
        self.reject(data, "STATEMENT_SHAPE")
        data["records"][0]["checks"] = [None]
        self.reject(data, "CHECK_SHAPE")

    def test_strict_json_and_pointer_handling(self):
        for text in ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}'):
            with self.assertRaises(ValueError):
                parse_json(text)
        self.assertEqual(resolve({"a/b": {"~x": [False]}}, "/a~1b/~0x/0"), False)
        for pointer in ("/a/01", "/a/-1", "/a/-", "/a/4", "/a~2", None):
            with self.assertRaises((ValueError, IndexError, KeyError)):
                resolve({"a": [1]}, pointer)

    def test_changed_source_bytes_rejected(self):
        with patch("validate_evidence_draft.snapshot_bytes", return_value=b"{}"):
            sources, errors = load_sources(ROOT)
            self.assertEqual(sources, {})
            self.assertEqual(len(errors), 4)

    def test_symlink_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(pathlib.Path, "is_symlink", return_value=True):
                sources, errors = load_sources(pathlib.Path(tmp))
                self.assertEqual(sources, {})
                self.assertEqual(len(errors), 4)

    def test_missing_git_snapshot_does_not_fallback_to_working_tree(self):
        with patch.object(pathlib.Path, "exists", return_value=True):
            with patch("validate_evidence_draft.subprocess.run",
                       side_effect=subprocess.CalledProcessError(128, ["git"])):
                with patch.object(pathlib.Path, "read_bytes",
                                  side_effect=AssertionError("No fallback allowed")):
                    sources, errors = load_sources(ROOT)
                    self.assertEqual(sources, {})
                    self.assertEqual(len(errors), 4)

    def test_git_reader_targets_snapshot_not_current_branch(self):
        with patch.object(pathlib.Path, "exists", return_value=True):
            with patch("validate_evidence_draft.subprocess.run") as run:
                run.return_value.stdout = b"snapshot bytes"
                self.assertEqual(snapshot_bytes(ROOT, PINS["grep"]), b"snapshot bytes")
                run.assert_called_once_with(
                    ["git", "-C", str(ROOT), "show",
                     SNAPSHOT["commit"] + ":" + PINS["grep"]["path"]],
                    capture_output=True, check=True)


if __name__ == "__main__":
    unittest.main()

"""No network, credentials, live projects or human evidence used by these tests."""
from copy import deepcopy
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pretrial_semantics import AXES, MODEL, execute_controls, validate_trace
from validate_pretrial_package import REQUIRED_PACKAGE_FILES, blob_sha, validate_manifest_files

RECORD = json.loads((ROOT / "12_NEUTRAL_METHOD_RED_TEAM.json").read_text())


class TraceTests(unittest.TestCase):
    def case(self, number=0):
        return deepcopy(RECORD["synthetic_cases"][number])

    def rejected(self, case, code):
        errors = validate_trace(case, owner="Owner-A")
        self.assertTrue(any(e.endswith(":" + code) for e in errors), (code, errors))

    def test_historical_positive_traces(self):
        for case in RECORD["synthetic_cases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(validate_trace(case, owner="Owner-A"), [])

    def test_every_transition_rejects_unknown_actor(self):
        for case in RECORD["synthetic_cases"]:
            for index in range(len(case["events"])):
                with self.subTest(case=case["id"], event=index):
                    changed = deepcopy(case)
                    changed["events"][index]["actor"] = "Unassigned-Person"
                    self.assertTrue(any("AUTHORITY" in e for e in validate_trace(changed, owner="Owner-A")))

    def test_every_transition_requires_metadata(self):
        for case in RECORD["synthetic_cases"]:
            for index in range(len(case["events"])):
                for field in ("actor", "reason", "evidence", "timestamp_utc", "baseline_version"):
                    with self.subTest(case=case["id"], event=index, field=field):
                        changed = deepcopy(case)
                        del changed["events"][index][field]
                        self.rejected(changed, "REQUIRED_" + field)

    def test_accept_rejects_each_failed_axis(self):
        for axis in AXES:
            with self.subTest(axis=axis):
                case = self.case()
                case["events"][-1]["review_verdicts"][axis] = "FAIL"
                self.rejected(case, "ACCEPT_REQUIRES_PASS")

    def test_accept_rejects_missing_axis(self):
        case = self.case()
        del case["events"][-1]["review_verdicts"]["operational_readiness"]
        self.rejected(case, "VERDICT_AXES")

    def test_verdict_values_and_shape_fail_closed(self):
        for value in (None, True, [], {}, "pass", "UNKNOWN"):
            with self.subTest(value=value):
                case = self.case()
                case["events"][-1]["review_verdicts"]["operational_readiness"] = value
                self.rejected(case, "VERDICT_VALUE")
        case["events"][-1]["review_verdicts"] = []
        self.rejected(case, "VERDICT_SCHEMA")

    def test_reject_requires_failure(self):
        case = self.case(1)
        case["events"][6]["review_verdicts"] = {axis: "PASS" for axis in AXES}
        self.rejected(case, "REJECT_REQUIRES_FAIL")

    def test_reviewer_cannot_be_any_contributor(self):
        case = self.case()
        case["contributors"].append("Reviewer-B")
        self.rejected(case, "REVIEW_INDEPENDENCE")

    def test_noncontributing_owner_can_review(self):
        case = self.case()
        case["reviewer"] = "Owner-A"
        case["events"][-1]["actor"] = "Owner-A"
        self.assertEqual(validate_trace(case, owner="Owner-A"), [])

    def test_no_prototype_requires_reason(self):
        case = self.case()
        del case["events"][0]["prototype_skip_reason"]
        self.rejected(case, "PROTOTYPE_SKIP")

    def test_silent_baseline_change_at_every_postapproval_event(self):
        for index in range(1, 4):
            case = self.case()
            case["events"][index]["baseline_version"] = "v2"
            self.rejected(case, "BASELINE_DRIFT")

    def test_numbered_baseline_required(self):
        for value in ("unassigned", "v0", "latest", {}, None):
            case = self.case()
            case["events"][0]["baseline_version"] = value
            self.rejected(case, "BASELINE_VERSION")

    def respecified(self, version):
        case = self.case()
        case["events"] = case["events"][:2]
        for source, target, stamp, baseline in (
                ("IN PROGRESS", "DEFINED", "2026-09-27T18:02:00Z", "v1"),
                ("DEFINED", "SPECIFIED", "2026-09-27T18:03:00Z", version)):
            event = deepcopy(case["events"][0])
            event.update({"from": source, "to": target, "timestamp_utc": stamp,
                          "baseline_version": baseline})
            case["events"].append(event)
        case["expected"] = "SPECIFIED"
        return case

    def test_material_change_requires_new_baseline(self):
        self.rejected(self.respecified("v1"), "BASELINE_REUSE")
        self.assertEqual(validate_trace(self.respecified("v2"), owner="Owner-A"), [])

    def test_blocked_resume_cannot_skip(self):
        case = self.case(2)
        case["events"][3]["to"] = "REVIEW"
        self.rejected(case, "BLOCKED_RESUME")

    def test_blocked_metadata_and_resolution(self):
        for index, field, code in ((2, "blocked_from", "BLOCKED_ORIGIN"),
                                   (2, "blocker_owner", "BLOCKER_OWNER"),
                                   (2, "next_unblock_action", "UNBLOCK_ACTION"),
                                   (3, "unblock_evidence", "UNBLOCK_EVIDENCE")):
            case = self.case(2)
            del case["events"][index][field]
            self.rejected(case, code)

    def test_reopen_requires_request_snapshot_and_reviewer(self):
        for field, value, code in (("owner_request", "Other", "REOPEN_REQUEST"),
                                   ("accepted_snapshot", "", "REOPEN_SNAPSHOT"),
                                   ("actor", "Owner-A", "REVIEW_AUTHORITY")):
            case = self.case(2)
            case["events"][6][field] = value
            self.rejected(case, code)

    def test_reopen_cannot_directly_accept(self):
        case = self.case(2)
        case["events"][7]["to"] = "ACCEPTED"
        self.rejected(case, "EDGE")

    def test_cancel_is_terminal(self):
        case = self.case()
        case["events"][0]["to"] = "CANCELLED"
        case["events"][0]["baseline_version"] = "unassigned"
        case["events"] = case["events"][:1]
        case["expected"] = "CANCELLED"
        self.assertEqual(validate_trace(case, owner="Owner-A"), [])
        later = deepcopy(case["events"][0])
        later.update({"from": "CANCELLED", "to": "DEFINED"})
        case["events"].append(later)
        case["expected"] = "DEFINED"
        self.rejected(case, "EDGE")

    def test_all_forbidden_edges_from_reachable_prefixes(self):
        prefixes = {"DEFINED": []}
        for case in RECORD["synthetic_cases"]:
            for index, event in enumerate(case["events"]):
                prefixes.setdefault(event["to"], deepcopy(case["events"][:index + 1]))
        cancelled = deepcopy(self.case()["events"][0])
        cancelled.update({"to": "CANCELLED", "baseline_version": "unassigned"})
        prefixes["CANCELLED"] = [cancelled]
        self.assertEqual(set(prefixes), set(MODEL))
        for source, prefix in prefixes.items():
            for target in MODEL:
                if target in MODEL[source]:
                    continue
                with self.subTest(source=source, target=target):
                    case = self.case()
                    event = deepcopy(case["events"][0])
                    event.update({"from": source, "to": target, "timestamp_utc": "2026-09-28T00:00:00Z"})
                    case.update({"events": prefix + [event], "expected": target})
                    self.rejected(case, "EDGE")

    def test_timestamp_format_and_order(self):
        for value in ("yesterday", "2026-02-30T00:00:00Z", "2026-09-27T18:02:00", True):
            case = self.case()
            case["events"][2]["timestamp_utc"] = value
            self.rejected(case, "TIMESTAMP")
        case["events"][2]["timestamp_utc"] = "2026-09-26T00:00:00Z"
        self.rejected(case, "TIME_ORDER")

    def test_no_silent_work_id_change(self):
        case = self.case()
        case["events"][2]["work_id"] = "Different-ID"
        self.rejected(case, "WORK_ID")

    def test_real_evidence_not_accepted_as_synthetic(self):
        case = self.case()
        case["events"][3]["evidence"] = "https://example.org/real-output"
        self.rejected(case, "SYNTHETIC_EVIDENCE")

    def test_malformed_shapes_fail_closed(self):
        for value in (None, [], "case", 1):
            self.rejected(value, "SCHEMA")
        for field, value, code in (("events", {}, "EVENTS"), ("contributors", [], "CONTRIBUTORS"),
                                   ("reviewer", None, "REVIEWER"), ("id", " ", "WORK_ID")):
            case = self.case()
            case[field] = value
            self.rejected(case, code)
        case = self.case()
        case["events"][0] = None
        self.rejected(case, "EVENT_SCHEMA")
        case = self.case()
        case["events"][0]["from"] = []
        self.rejected(case, "STATE_SCHEMA")

    def test_route_and_terminal(self):
        case = self.case()
        case["events"][1]["from"] = "REJECTED"
        self.rejected(case, "ROUTE")
        case = self.case()
        case["expected"] = "CANCELLED"
        self.rejected(case, "TERMINAL")

    def test_all_event_fields_reject_wrong_types_and_empty_values(self):
        # Arbitrary nonempty prose is not included: its truth needs evidence review.
        for original in RECORD["synthetic_cases"]:
            for index, event in enumerate(original["events"]):
                for field in event:
                    for value in (None, True, False, 0, [], {}, "", " "):
                        with self.subTest(case=original["id"], event=index, field=field, value=value):
                            changed = deepcopy(original)
                            changed["events"][index][field] = value
                            self.assertTrue(validate_trace(changed, owner="Owner-A"))


class ControlTests(unittest.TestCase):
    def test_four_controls_execute(self):
        results, errors = execute_controls(RECORD)
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 4)
        self.assertTrue(all(r["rejected_as_expected"] for r in results))

    def test_historical_labels_do_not_determine_results(self):
        record = deepcopy(RECORD)
        for control in record["negative_controls"]:
            control.update({"observed": "ACCEPT", "result": "FAIL"})
        self.assertEqual(execute_controls(record), execute_controls(RECORD))

    def test_benign_attempt_is_not_reported_as_rejected(self):
        record = deepcopy(RECORD)
        record["negative_controls"][0]["attempt"]["actor"] = "Reviewer-B"
        results, errors = execute_controls(record)
        self.assertFalse(results[0]["rejected_as_expected"])
        self.assertIn("NC-01:CONTROL_DID_NOT_REJECT_AS_EXPECTED", errors)

    def test_control_ids_and_schema(self):
        for value in (None, [], [None], RECORD["negative_controls"] * 2):
            record = deepcopy(RECORD)
            record["negative_controls"] = value
            self.assertTrue(execute_controls(record)[1])


class ManifestTests(unittest.TestCase):
    def manifest(self):
        return {"schema_version": 2, "method_version": "v1.0-static-reviewed",
                "package_blobs": {p: blob_sha((ROOT / p).read_bytes()) for p in REQUIRED_PACKAGE_FILES}}

    def test_complete_manifest(self):
        self.assertEqual(validate_manifest_files(self.manifest(), ROOT), [])

    def test_omitted_or_empty_manifest_rejected(self):
        for value in (None, {}, []):
            manifest = self.manifest()
            manifest["package_blobs"] = value
            self.assertTrue(validate_manifest_files(manifest, ROOT))
        manifest = self.manifest()
        del manifest["package_blobs"]["scripts/pretrial_semantics.py"]
        self.assertIn("MANIFEST_REQUIRED_FILES", validate_manifest_files(manifest, ROOT))

    def test_traversal_and_absolute_path_rejected_before_read(self):
        for path in ("../outside", "/etc/passwd"):
            manifest = self.manifest()
            manifest["package_blobs"][path] = "0" * 40
            self.assertIn("MANIFEST_PATH:" + path, validate_manifest_files(manifest, ROOT))

    def test_missing_files_bad_hash_and_drift(self):
        manifest = self.manifest()
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(any(e.startswith("MANIFEST_MISSING:")
                                for e in validate_manifest_files(manifest, pathlib.Path(directory))))
        for value, code in (([], "MANIFEST_HASH:"), ("0" * 40, "MANIFEST_MISMATCH:")):
            manifest["package_blobs"]["scripts/pretrial_semantics.py"] = value
            self.assertIn(code + "scripts/pretrial_semantics.py", validate_manifest_files(manifest, ROOT))

    def test_symlinks_rejected(self):
        with patch.object(pathlib.Path, "is_symlink", return_value=True):
            self.assertTrue(any(e.startswith("MANIFEST_SYMLINK:")
                                for e in validate_manifest_files(self.manifest(), ROOT)))

    def test_raw_bytes_hash_not_newline_normalized(self):
        self.assertNotEqual(blob_sha(b"a\r\n"), blob_sha(b"a\n"))

    def test_cli_package_and_executed_results(self):
        result = subprocess.run([sys.executable, "scripts/validate_pretrial_package.py"],
                                cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["hard_errors"], [])
        self.assertEqual(output["executed_negative_control_count"], 4)
        self.assertFalse(output["human_evidence_validated"])


if __name__ == "__main__":
    unittest.main()

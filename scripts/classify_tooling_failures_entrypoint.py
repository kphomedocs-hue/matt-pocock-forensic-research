#!/usr/bin/env python3
"""Stable entrypoint for the historical tooling-incident classifier.

Keeps one-off, fully adjudicated run-ID reconciliations outside the large base
classifier so a narrow audit correction cannot accidentally rewrite historical
classification logic.
"""
from __future__ import annotations

import classify_failed_workflows as base

PHASE4_RUNTIME_ACCEPTANCE_SCHEMA_TRANSITION_IDS = {34752972889}

_original_classify_failure = base.classify_failure


def classify_failure(run_id: int, failed_step: str, log: str):
    if run_id in PHASE4_RUNTIME_ACCEPTANCE_SCHEMA_TRANSITION_IDS:
        return (
            "PHASE4_RUNTIME_ACCEPTANCE_SCHEMA_TRANSITION",
            "NO_RESEARCH_DATA_CHANGE_FIXED",
            "The new B-004 local runtime check and every Phase 4 validator passed, but this older queued run retained the prior acceptance assertion expecting only B-015/B-018/B-056. The acceptance gate was updated to include B-004 and the immediately following run 34752990655 passed and published the same validated state.",
        )
    return _original_classify_failure(run_id, failed_step, log)


base.classify_failure = classify_failure

if __name__ == "__main__":
    base.main()

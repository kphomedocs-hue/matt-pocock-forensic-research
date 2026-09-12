# Tooling Integrity Audit

Audit date: 2026-09-12

Scope: the forensic research repository itself (`kphomedocs-hue/matt-pocock-forensic-research`), not `mattpocock/skills`.

## Purpose

This audit checks whether our own automation could silently lose, stale, cancel, or misclassify durable forensic state. It began after the Phase 3 graph workflow generated files successfully but failed to persist them, and it was extended until failed and cancelled workflow history had an explicit durable disposition.

## Current closure state

The durable incident ledger (`00_TOOLING_FAILURE_LEDGER.md` / `.json`, classifier version 3) now covers both failed and cancelled Actions runs.

- Failed runs enumerated: **78**
- Cancelled runs enumerated: **7**
- Total incident runs: **85**
- Incident entries classified: **85**
- Unknown entries: **0**
- Unresolved / review-required entries: **0**
- Evidence-corruption failures found: **0**

Classification totals:

| Classification | Count |
|---|---:|
| `PUSH_RACE` | 61 |
| `STATUS_PARSER` | 10 |
| `FOUNDATION_GATE` | 1 |
| `FOUNDATION_PROVENANCE_GATE` | 1 |
| `FOUNDATION_REGISTER_GATE` | 3 |
| `CROSS_WORKFLOW_CONCURRENCY_CANCEL` | 3 |
| `CLASSIFIER_REFRESH_SUPERSEDED` | 4 |
| `CLASSIFIER_SCHEMA_TRANSITION` | 1 |
| `CLASSIFIER_CLOSURE_GATE` | 1 |

## Confirmed tooling defects and fixes

### TI-001 — Untracked generated files ignored by `git diff --quiet`

**State:** FIXED

The first Phase 3 graph workflow generated `03_CONNECTION_EDGES.json` and `03_CONNECTION_INDEX.md` successfully (`204 edges`, `5 unresolved`) but used `git diff --quiet` to decide whether to commit. New untracked files are invisible to that check, so the workflow incorrectly reported no graph changes.

**Impact:** generated Phase 3 outputs were temporarily absent. Frozen-source evidence and Phase 2 notes were not corrupted.

**Fix:** generated-file workflows use `git status --porcelain` and explicit output existence/non-empty checks.

### TI-002 — Non-fast-forward publication races

**State:** FIXED / MONITORED

The incident ledger classifies **61** historical runs as `PUSH_RACE`. Their logs show generation completing locally and publication losing a race to another write on `main`.

**Impact:** a generated ledger/report could be temporarily stale relative to already-committed durable notes. The durable notes themselves remained committed.

**Fix:** generated workflows synchronize from `main` before generation and retry push after fetch/rebase up to five times. This remains the cross-workflow write-conflict defense.

### TI-003 — Durable-note status parser mismatch

**State:** FIXED

The incident ledger classifies **10** historical runs as `STATUS_PARSER`. The old ledger parser required the older bold syntax while newer notes used `- Status: READ`.

**Impact:** READ promotion was delayed. The workflow failed closed; it did not fabricate a READ state.

**Fix:** the current parser accepts both durable status syntaxes and still fails closed on malformed/invalid status.

### TI-004 — Historical failure ledger could become stale

**State:** FIXED

The first historical ledger closed at 71 failed runs, but later foundation-hardening work created additional fail-closed runs. The durable ledger therefore stopped matching GitHub history.

**Fix:** the classifier now refreshes from GitHub run history and is triggered by non-success completion of the upstream research workflows as well as explicit classifier changes/manual execution. The ledger is regenerated from history rather than incrementally patched.

### TI-005 — Classifier closure rule was descriptive but not enforced

**State:** FIXED

Earlier classifier CI generated `unknown_entries` but did not require the count to be zero.

**Fix:** CI now asserts both `unknown_entries == 0` and `unresolved_entries == 0`. A classifier run cannot publish a closed ledger while either count is non-zero.

### TI-006 — Shared concurrency lane discarded distinct pending workflows

**State:** FIXED

The earlier hardening used one shared concurrency group, `forensic-generated-main-writes`, with `cancel-in-progress: false`. GitHub concurrency still permits only one running and one pending run per group; newer pending runs can therefore replace older pending runs even when they belong to different workflows.

Three distinct critical executions were proven discarded by that design:

- connection graph run `34712776661`;
- foundation validation run `34712784616`;
- note-normalization run `34712792316`.

Four cancelled classifier refreshes were redundant and later superseded by a complete history rebuild.

**Fix:** each workflow now has its own concurrency lane (`forensic-rebuild-ledger`, `forensic-rebuild-connection-graph`, `forensic-validate-foundation`, `forensic-normalize-note-metadata`, `forensic-classify-tooling-failures`). Cross-workflow write races are handled by the existing fetch/rebase/push retry path rather than by sharing one cancellation-prone queue.

### TI-007 — Cancelled runs were absent from the incident model

**State:** FIXED

The original classifier queried only failed runs, so orchestration defects expressed as cancellations were invisible.

**Fix:** classifier version 3 enumerates both `failure` and `cancelled`. Any future cancelled run that does not match a reconciled cancellation class becomes `CANCELLED_RUN_REQUIRES_REVIEW` and prevents closure.

### TI-008 — GitHub Actions Node runtime deprecation

**State:** FIXED

The previous workflow actions emitted warnings because older action majors targeted the deprecated Node runtime.

**Fix:** all research workflows now use `actions/checkout@v7.0.1` and `actions/setup-python@v7.0.0`. Successful proof runs show the upgraded actions executing on the current runner without the old Node deprecation warning.

### TI-009 — Classifier hardening transition failures

**State:** FIXED / RECONCILED

Two classifier runs failed while the incident model itself was being strengthened:

- run `34713138258`: classifier script emitted schema version 3 while the then-current workflow still asserted version 2 (`CLASSIFIER_SCHEMA_TRANSITION`);
- run `34713153565`: the new closure gate correctly refused to pass while the transition run above was still unresolved (`CLASSIFIER_CLOSURE_GATE`).

These are reconciled by exact run ID so future classifier validation failures are **not** automatically excused. The subsequent classifier run `34713382373` completed successfully and published the closed 85-incident ledger.

## Current workflow proof

The post-fix workflows have completed successfully under separate concurrency lanes:

| Workflow | Proof run | Result |
|---|---:|---|
| Rebuild master ledger | `34712959458` | SUCCESS |
| Rebuild connection graph | `34712966927` | SUCCESS |
| Validate forensic foundation | `34712981139` | SUCCESS |
| Normalize note metadata | `34712989578` | SUCCESS |
| Classify tooling failures/cancellations | `34713382373` | SUCCESS |

The latest foundation report remains **0 hard errors / 0 normalization warnings**, with **164/164 durable notes**, **164 READ**, and direct frozen-commit provenance for all 164 notes.

## What these incidents did not invalidate

No classified tooling incident changed the frozen source commit, changed source blob SHAs, deleted the durable per-file evidence set, or fabricated READ status. Phase 2 remains independently grounded by:

- frozen source commit `3cca18b368ae95cdbdebbff572ccafa662551015`;
- frozen tree `6e84c093fda2026396cea9fad6a924a6da0e1452`;
- exact 164-blob census;
- 164 durable per-file notes;
- successful deterministic ledger rebuild showing `164 READ / 0 UNREAD`;
- green foundation validation with zero hard errors.

## Integrity conclusion

The fresh recheck found additional real weaknesses in the audit tooling: stale incident accounting, a non-enforced classifier closure rule, missing cancellation accounting, a cancellation-prone shared concurrency design, and an impending Actions runtime deprecation. They are now fixed and mechanically exercised. The complete durable incident history is **85/85 classified, 0 unknown, 0 unresolved/review-required**, with no evidence-corruption incident found.

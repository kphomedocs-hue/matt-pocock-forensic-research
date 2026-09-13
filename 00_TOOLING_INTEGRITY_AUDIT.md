# Tooling Integrity Audit

Audit date: 2026-09-13

Scope: the forensic research repository itself (`kphomedocs-hue/matt-pocock-forensic-research`), not `mattpocock/skills`.

## Purpose

This audit checks whether our own automation could silently lose, stale, cancel, misclassify, or incompletely propagate durable forensic state. It began after the first Phase 3 graph workflow generated files successfully but failed to persist them, and it has been extended whenever later work exposed another automation assumption.

## Current closure state

The durable incident ledger (`00_TOOLING_FAILURE_LEDGER.md` / `.json`, classifier version 3) covers failed and cancelled Actions runs.

- Failed runs enumerated: **83**
- Cancelled runs enumerated: **7**
- Total incident runs: **90**
- Incident entries classified: **90**
- Unknown entries: **0**
- Unresolved / review-required entries: **0**
- Evidence-corruption failures found: **0**

Current classification totals:

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
| `CLASSIFIER_CLOSURE_GATE` | 3 |
| `PHASE3_PROMOTION_PROVENANCE_PARSER` | 1 |
| `PHASE3_QUALITY_RECHECK_GATE` | 1 |
| `PHASE4_BATCH_BOOTSTRAP_TRIGGER` | 1 |

## Confirmed tooling defects and fixes

### TI-001 — Untracked generated files ignored by `git diff --quiet`

**State:** FIXED

The first Phase 3 graph workflow generated `03_CONNECTION_EDGES.json` and `03_CONNECTION_INDEX.md` successfully but used `git diff --quiet` to decide whether to commit. New untracked files are invisible to that check.

**Impact:** generated Phase 3 outputs were temporarily absent. Frozen-source evidence and Phase 2 notes were not corrupted.

**Fix:** generated-file workflows use `git status --porcelain` and explicit output existence/non-empty checks.

### TI-002 — Non-fast-forward publication races

**State:** FIXED / MONITORED

The incident ledger classifies **61** historical runs as `PUSH_RACE`. Their logs show generation completing locally and publication losing a race to another write on `main`.

**Impact:** generated state could be temporarily stale relative to already-committed durable evidence.

**Fix:** relevant workflows synchronize latest `main` before generation and retry push after fetch/rebase up to five times.

### TI-003 — Durable-note status parser mismatch

**State:** FIXED

The incident ledger classifies **10** historical runs as `STATUS_PARSER`. The old ledger parser required the older bold syntax while newer notes used `- Status: READ`.

**Impact:** READ promotion was delayed. The workflow failed closed.

**Fix:** the parser accepts both durable status syntaxes and fails closed on malformed/invalid status.

### TI-004 — Historical failure ledger could become stale

**State:** FIXED

The first historical ledger closed at 71 failed runs, but later hardening created additional fail-closed runs.

**Fix:** the classifier reconstructs the ledger from GitHub run history and refreshes on non-success completion of monitored research workflows, classifier changes, or manual execution.

### TI-005 — Classifier closure rule was descriptive but not enforced

**State:** FIXED

Earlier classifier CI generated `unknown_entries` but did not require zero.

**Fix:** CI asserts both `unknown_entries == 0` and `unresolved_entries == 0`.

### TI-006 — Shared concurrency lane discarded distinct pending workflows

**State:** FIXED

A former shared concurrency group allowed newer pending workflow runs to displace older distinct pending runs even with `cancel-in-progress: false`.

Three critical runs were proven discarded:

- connection graph `34712776661`;
- foundation validation `34712784616`;
- note normalization `34712792316`.

**Fix:** independent workflows use workflow-specific concurrency lanes. Cross-workflow write races are handled by synchronization/rebase/retry rather than one shared queue.

### TI-007 — Cancelled runs were absent from the incident model

**State:** FIXED

The original classifier queried only failures, hiding orchestration defects expressed as cancellations.

**Fix:** classifier version 3 enumerates both `failure` and `cancelled`. Unrecognized cancellations block closure.

### TI-008 — GitHub Actions Node runtime deprecation

**State:** FIXED

Older action majors emitted runtime-deprecation warnings.

**Fix:** research workflows use `actions/checkout@v7.0.1` and `actions/setup-python@v7.0.0`.

### TI-009 — Classifier hardening transition failures

**State:** FIXED / RECONCILED

The classifier produced several self-referential fail-closed incidents while its own closure model was being strengthened. These include the schema-transition incident and later runs where classification succeeded but the zero-unresolved validation step correctly blocked publication until an earlier incident was reconciled.

**Fix:** exact known schema-transition history is retained, and the classifier now recognizes the specific successful-classification-followed-by-closure-assertion signature as `CLASSIFIER_CLOSURE_GATE`. Actual classifier execution defects remain review-required. Current count: **3 closure-gate incidents**, all reconciled.

### TI-010 — Workflow-to-workflow chaining assumed `GITHUB_TOKEN` pushes would retrigger Actions

**State:** FIXED

Phase 3 originally used separate graph, router, distribution, history-binding, and closure-index workflows. This implicitly assumed that when one Actions workflow committed generated output with its repository `GITHUB_TOKEN`, downstream push-triggered workflows would run. GitHub suppresses recursive workflow triggering for such pushes, so a successful upstream generator could leave downstream derived artifacts stale.

The defect became visible during formal Phase 3 promotion: all 164 notes were successfully committed as `CONNECTIONS TRACED`, but the separately generated ledger remained `READ` because the bot promotion commit did not trigger the ledger workflow.

**Impact:** internally valid artifacts could disagree in freshness even though no source evidence was corrupted.

**Fix:** dependent Phase 3 generation is now one ordered atomic authority, `.github/workflows/rebuild-phase3-state.yml`. Formal status promotion remains separate but atomically rebuilds ledger/census/closure/foundation before publishing promoted note state.

### TI-011 — First Phase 3 promoter rejected an accepted legacy provenance label

**State:** FIXED / RECONCILED

Run `34738911437` failed closed because `scripts/promote_phase3_connections.py` recognized `Blob SHA` but not the already-valid legacy alias `Frozen blob SHA` used by MP-0021 and accepted by the foundation validator.

**Impact:** none to durable evidence; the run stopped before committing note changes.

**Fix:** the promoter's blob-provenance regex mirrors the established validator. The historical incident is classified by exact run ID as `PHASE3_PROMOTION_PROVENANCE_PARSER`.

### TI-012 — Phase 3 completion lacked a second-order quality gate

**State:** FIXED / RECONCILED

A deliberate Phase 3 recheck exposed several proof-architecture weaknesses even though the underlying source evidence was intact: the master ledger did not consume graph Ref-in/Ref-out counts; history event definitions were duplicated inside the generator; human Phase 3 prose was stale; contextual backtick skill references needed weaker-confidence treatment; support-file ownership needed structural representation; and generated state lacked a cryptographic build fingerprint.

The first second-order quality run failed closed and is retained as `PHASE3_QUALITY_RECHECK_GATE`.

**Fix:** Phase 3 now includes:

- `03_PHASE3_QUALITY.md/.json`;
- `03_PHASE3_BUILD_MANIFEST.md/.json` with SHA-256 input/output fingerprints;
- history definitions derived from durable `05_HISTORY_LEDGER.md`;
- graph-derived Ref-in/Ref-out master-ledger enrichment;
- stable content-derived graph edge IDs;
- literal source-line provenance where applicable;
- weak-reference/orphan checks;
- extra Markdown/HTML/autolink scanning;
- exact-link README distribution checks;
- structural `SUPPORT_BINDING` edges that do not falsely imply operative consumption.

Current quality gate: **0 hard errors, 0 review items, 0 remaining improvements**.

### TI-013 — Human resume summaries could lag machine truth

**State:** FIXED / CONTROL ADDED

During the storage-integrity audit, `RESEARCH_STATUS.md` still described the older Phase 3 v4 / 530-edge state while `03_CONNECTION_EDGES.json` and `03_PHASE3_QUALITY.json` already held the newer v5 state. This did not lose research data, but it could mislead a future session that resumed from prose alone.

**Fix:** `RESEARCH_STATUS.md` was synchronized to v5 / 554 edges, `00_STORAGE_INTEGRITY_AUDIT.md` was added, and the manifest requires future sessions to load machine JSON artifacts for exact numerical state.

### TI-014 — Phase 4 batch importer triggered on its own bootstrap commit

**State:** FIXED / RECONCILED

Run `34745903691` was the first `Apply Phase 4 batch` execution. Creating the workflow matched the workflow's initial path filters (`scripts/apply_phase4_batch.py` and the workflow YAML itself), even though no `04_PHASE4_BATCH.json` existed. The importer failed closed at `Apply pending Phase 4 batch` with `Missing 04_PHASE4_BATCH.json`.

**Impact:** none to research data. No Phase 4 matrix, contradiction register, or generated artifact was modified by the failed run.

**Fix:** automatic execution now triggers only when `04_PHASE4_BATCH.json` is pushed. The exact historical run is classified as `PHASE4_BATCH_BOOTSTRAP_TRIGGER`; future importer failures remain review-required. The incident monitor now watches both `Validate Phase 4 behavior matrix` and `Apply Phase 4 batch`.

A second propagation issue was fixed at the same time: successful bot commits from the batch importer cannot be relied upon to trigger `Validate forensic foundation`, so the batch workflow now regenerates and validates foundation state inside the same atomic application before publishing.

## Current workflow proof and generated-state controls

Key durable controls now include:

- frozen source identity and 164-file denominator;
- 164 durable per-file notes;
- foundation integrity validation with current-contradiction parity checking;
- atomic Phase 3 rebuild;
- Phase 3 second-order quality validation;
- SHA-256 Phase 3 build manifest and verifier;
- formal Phase 3 promotion gate;
- Phase 4 behavior-matrix validation;
- Phase 4 37-current-skill coverage index;
- atomic Phase 4 batch application with same-run behavior, coverage, contradiction, and foundation reconciliation;
- historical failure/cancellation classifier with zero-unknown and zero-unresolved closure.

Current Phase 3 machine state is extraction rules v5 with **554 edges**, **554 stable edge IDs**, **490 literal source-line provenance edges**, **0 invocation-policy mismatches**, **0 illegal operative calls**, and a green second-order quality report.

## Current durable integrity state

- frozen source: commit `3cca18b368ae95cdbdebbff572ccafa662551015`, tree `6e84c093fda2026396cea9fad6a924a6da0e1452`;
- physical denominator: **164**;
- durable notes: **164**;
- formal note/ledger status: **164 CONNECTIONS TRACED**;
- foundation hard errors: **0**;
- foundation warnings: **0**;
- current contradiction parity: **CT-001…CT-020**;
- Phase 3 closure: **164/164 READY_CANDIDATE, 0 blockers**;
- Phase 3 quality: **0 hard errors, 0 review items, 0 remaining improvements**;
- tooling incidents: **90/90 classified, 0 unknown, 0 unresolved**;
- VERIFIED: **0**.

## What these incidents did not invalidate

No classified tooling incident changed the frozen source commit, changed source blob SHAs, deleted the durable per-file evidence set, or fabricated a higher forensic status. Failures that touched status or integrity gates failed closed, and formal Phase 3 promotion was only published after the complete 164-file closure index and provenance checks passed.

## Integrity conclusion

The audit infrastructure has had real defects, including silent untracked-output handling, publication races, parser incompatibilities, cancellation-prone orchestration, stale incident accounting, invalid workflow-chaining assumptions, insufficient second-order Phase 3 proof, stale human summaries, and an overbroad Phase 4 importer bootstrap trigger. Each discovered class is now durably recorded and either mechanically prevented or made fail-closed.

Current incident history is **90/90 classified, 0 unknown, 0 unresolved/review-required**, with no evidence-corruption incident found. GitHub remains the authoritative durable state; chat/GPT summaries are secondary only.

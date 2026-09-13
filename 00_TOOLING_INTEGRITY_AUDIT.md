# Tooling Integrity Audit

Audit date: 2026-09-13

Scope: the forensic research repository itself (`kphomedocs-hue/matt-pocock-forensic-research`), not `mattpocock/skills`.

## Purpose

This audit checks whether our own automation could silently lose, stale, cancel, misclassify, or incompletely propagate durable forensic state. It began after the first Phase 3 graph workflow generated files successfully but failed to persist them, and it has been extended whenever later work exposed another automation assumption.

## Current closure state

The durable incident ledger (`00_TOOLING_FAILURE_LEDGER.md` / `.json`, classifier version 3) covers failed and cancelled Actions runs.

- Failed runs enumerated: **79**
- Cancelled runs enumerated: **7**
- Total incident runs: **86**
- Incident entries classified: **86**
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
| `CLASSIFIER_CLOSURE_GATE` | 1 |
| `PHASE3_PROMOTION_PROVENANCE_PARSER` | 1 |

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

Two classifier runs failed while its own closure model was being strengthened:

- `34713138258`: schema v3 output under a workflow still asserting v2;
- `34713153565`: the new closure gate correctly blocked while the first incident remained unresolved.

They are reconciled by exact run ID so future classifier failures are not auto-excused.

### TI-010 — Workflow-to-workflow chaining assumed `GITHUB_TOKEN` pushes would retrigger Actions

**State:** FIXED

Phase 3 originally used separate graph, router, distribution, history-binding, and closure-index workflows. This implicitly assumed that when one Actions workflow committed generated output with its repository `GITHUB_TOKEN`, downstream push-triggered workflows would run. GitHub suppresses recursive workflow triggering for such pushes, so a successful upstream generator could leave downstream derived artifacts stale.

The defect became visible during formal Phase 3 promotion: all 164 notes were successfully committed as `CONNECTIONS TRACED`, but the separately generated ledger remained `READ` because the bot promotion commit did not trigger the ledger workflow.

**Impact:** internally valid artifacts could disagree in freshness even though no source evidence was corrupted.

**Fix:** dependent Phase 3 generation is now one ordered atomic authority, `.github/workflows/rebuild-phase3-state.yml`, which executes connection graph → router → distribution → history bindings → closure index, validates the complete set, and commits it together. The five superseded partial Phase 3 workflows were removed. Formal status promotion remains separate but atomically rebuilds ledger/census/closure/foundation before publishing the promoted state.

### TI-011 — First Phase 3 promoter rejected an accepted legacy provenance label

**State:** FIXED / RECONCILED

Run `34738911437` failed closed because `scripts/promote_phase3_connections.py` recognized `Blob SHA` but not the already-valid legacy alias `Frozen blob SHA` used by MP-0021 and accepted by the foundation validator.

**Impact:** none to durable evidence; the run stopped before committing any note changes.

**Fix:** the promoter's blob-provenance regex now mirrors the established validator. Promotion run `34738969932` then succeeded, and atomic proof run `34739027703` rebuilt and validated notes, ledger/census, Phase 3 closure, and foundation together. The historical incident is classified by exact run ID as `PHASE3_PROMOTION_PROVENANCE_PARSER`.

## Current workflow proof

Key post-fix proof runs:

| Workflow | Proof run | Result |
|---|---:|---|
| Rebuild master ledger | `34712959458` | SUCCESS |
| Validate forensic foundation | `34712981139` | SUCCESS |
| Normalize note metadata | `34712989578` | SUCCESS |
| Classify tooling failures/cancellations | later classifier rebuild | SUCCESS / 86 incidents closed |
| Promote Phase 3 connections | `34739027703` | SUCCESS |
| Rebuild Phase 3 state | `34739079695` | SUCCESS |

The Phase 3 promotion proof run succeeded through note promotion, ledger/census rebuild, closure rebuild, foundation validation, state validation, and atomic commit. The consolidated Phase 3 generator also completed its full ordered rebuild successfully.

## Current durable integrity state

- frozen source: commit `3cca18b368ae95cdbdebbff572ccafa662551015`, tree `6e84c093fda2026396cea9fad6a924a6da0e1452`;
- physical denominator: **164**;
- durable notes: **164**;
- formal note/ledger status: **164 CONNECTIONS TRACED**;
- foundation hard errors: **0**;
- foundation warnings: **0**;
- Phase 3 closure: **164/164 READY_CANDIDATE, 0 blockers**;
- VERIFIED: **0**.

## What these incidents did not invalidate

No classified tooling incident changed the frozen source commit, changed source blob SHAs, deleted the durable per-file evidence set, or fabricated a higher forensic status. Failures that touched status or integrity gates failed closed, and formal Phase 3 promotion was only published after the complete 164-file closure index and provenance checks passed.

## Integrity conclusion

The audit infrastructure has had real defects, including silent untracked-output handling, publication races, parser incompatibilities, cancellation-prone orchestration, stale incident accounting, and an invalid assumption about Actions workflow chaining. Each discovered class is now durably recorded and either mechanically prevented or made fail-closed. Current incident history is **86/86 classified, 0 unknown, 0 unresolved/review-required**, with no evidence-corruption incident found.

# Tooling Integrity Audit

Audit date: 2026-09-12

Scope: the forensic research repository itself (`kphomedocs-hue/matt-pocock-forensic-research`), not `mattpocock/skills`.

## Purpose

This audit checks whether our own automation could silently lose, stale, or misclassify durable forensic state. It was triggered after the Phase 3 graph workflow generated files successfully but failed to commit them because its change-detection gate ignored untracked files.

## Confirmed historical failure classes

### TI-001 — Untracked generated files ignored by `git diff --quiet`

**State:** FIXED

The first Phase 3 graph workflow generated `03_CONNECTION_EDGES.json` and `03_CONNECTION_INDEX.md` successfully (`204 edges`, `5 unresolved`), but the commit gate used `git diff --quiet`, which does not report newly-created untracked files. The workflow therefore printed `No graph changes` and exited successfully without persisting them.

**Impact:** generated Phase 3 outputs were temporarily absent even though extraction succeeded. Source evidence and Phase 2 notes were not corrupted.

**Fix:** graph workflow now uses `git status --porcelain` and explicitly requires generated outputs to exist and be non-empty.

### TI-002 — Concurrent writes causing non-fast-forward workflow push failures

**State:** FIXED / MONITORED

The complete historical failure ledger now classifies **61 runs** as `PUSH_RACE`. Their failed job logs contain the non-fast-forward/fetch-first push signature after generation succeeded locally.

**Impact:** generated ledger state could be temporarily stale relative to newly committed per-file notes. Durable notes remained committed.

**Fixes applied to generated-file workflows:**

- shared concurrency group `forensic-generated-main-writes`;
- `cancel-in-progress: false`;
- full-history checkout;
- `git pull --ff-only origin main` before generation;
- generated-output existence/non-empty checks;
- up to five push attempts with fetch/rebase after a race.

### TI-003 — Durable-note status parser format mismatch

**State:** FIXED

The complete historical failure ledger classifies **10 runs** as `STATUS_PARSER`. Their logs show the old parser rejecting notes such as `MP-0021.md` because it required the older `Status: **...**` form while newer notes used `- Status: READ`.

**Impact:** READ promotion was delayed. The workflow failed closed; no false promotion or source-evidence corruption occurred.

**Fix:** the current parser accepts both durable status formats and still fails closed for malformed or invalid statuses.

## Complete historical failure classification

`00_TOOLING_FAILURE_LEDGER.md` and `00_TOOLING_FAILURE_LEDGER.json` enumerate every historical failed workflow run and classify it from the actual failed step plus job-log signature.

- Failed runs enumerated: **71**
- `PUSH_RACE`: **61**
- `STATUS_PARSER`: **10**
- Unknown/unclassified: **0**

Impact classification:

- `TEMPORARILY_STALE`: **61**
- `DELAYED_PROMOTION`: **10**
- Evidence-corruption failures found: **0**

## Current workflow assessment

### `rebuild-ledger.yml`

- Exact source-tree denominator remains fail-closed at 164 blobs.
- Unique MP-ID and path counts are asserted.
- Generated files are tracked, so TI-001 did not apply.
- Concurrency/push handling is hardened.
- Hardened workflow has completed successfully.

### `rebuild-connection-graph.yml`

- TI-001 affected its first run and is fixed.
- Shares the serialized write lane.
- Validates generated outputs before commit.
- Preserves unresolved references for manual reconciliation.
- Hardened workflow has completed successfully.

### `classify-tooling-failures.yml`

- Enumerates all failed runs via GitHub API.
- Retrieves failed-job logs through GitHub's signed-log redirect.
- Writes a durable per-run classification ledger.
- Closure criterion is zero unknowns or explicit manual disposition.
- Current historical classification reached **0 unknowns**.

## What the failures did NOT invalidate

No classified historical failure changed the frozen source commit, altered source blob SHAs, deleted per-file notes, or fabricated READ status.

Phase 2's final result remains grounded by:

- frozen source commit `3cca18b368ae95cdbdebbff572ccafa662551015`;
- frozen tree `6e84c093fda2026396cea9fad6a924a6da0e1452`;
- exact 164-blob census;
- 164 durable per-file notes;
- successful deterministic rebuild showing `164 READ / 0 UNREAD`.

## Integrity conclusion

The historical tooling issue is now classified rather than open-ended. All **71 failed runs** have a concrete cause: **61 publication races** and **10 fail-closed parser mismatches**. No historical failed run remains UNKNOWN, and no evidence-corruption failure was found. The known automation defects have been hardened before deeper Phase 3 promotion work continues.

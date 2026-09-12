# Tooling Integrity Audit

Audit date: 2026-09-12

Scope: the forensic research repository itself (`kphomedocs-hue/matt-pocock-forensic-research`), not `mattpocock/skills`.

## Purpose

This audit checks whether our own automation could silently lose, stale, or misclassify durable forensic state. It was triggered after the Phase 3 graph workflow generated files successfully but failed to commit them because its change-detection gate ignored untracked files.

## Confirmed historical failure classes

### TI-001 — Untracked generated files ignored by `git diff --quiet`

**State:** FIXED

The first Phase 3 graph workflow generated `03_CONNECTION_EDGES.json` and `03_CONNECTION_INDEX.md` successfully (`204 edges`, `5 unresolved`), but the commit gate used:

```sh
git diff --quiet -- 03_CONNECTION_EDGES.json 03_CONNECTION_INDEX.md
```

`git diff` does not report newly-created untracked files, so the workflow incorrectly printed `No graph changes` and exited successfully without persisting them.

**Impact:** generated Phase 3 outputs were temporarily absent even though extraction succeeded. Source evidence and Phase 2 notes were not corrupted.

**Fix:** graph workflow now uses `git status --porcelain` for generated-file detection and explicitly requires both generated outputs to exist and be non-empty.

### TI-002 — Concurrent writes causing non-fast-forward workflow push failures

**State:** FIXED / MONITORED

GitHub Actions reports 71 failed runs in the repository's historical run set. A representative ledger failure was inspected in full. The workflow:

1. rebuilt the 164-file ledger successfully;
2. validated the exact denominator successfully;
3. created a local commit successfully;
4. failed only at `git push` because another write had reached `main` first:

```text
! [rejected] main -> main (fetch first)
error: failed to push some refs
```

This confirms that the many connector writes and automatic ledger commits could race each other.

**Impact:** a particular generated ledger commit could fail to publish, leaving the generated ledger temporarily behind the newest per-file notes. The durable notes themselves remained committed. A later successful rebuild generally reconciled the ledger, which is why the final Phase 2 gate still reached mechanically confirmed `164 READ / 0 UNREAD`.

**Fixes now applied to both generated-file workflows:**

- shared GitHub Actions concurrency group: `forensic-generated-main-writes`;
- `cancel-in-progress: false` so generated work is serialized, not silently discarded;
- `fetch-depth: 0`;
- `git pull --ff-only origin main` before generation;
- explicit generated-output existence/non-empty checks;
- up to five push attempts, fetching and rebasing onto the latest `main` after a push race.

Connector/API writes can still land while a workflow is running, so the retry/rebase path remains necessary even with workflow concurrency.

### TI-003 — Durable-note status parser format mismatch

**State:** FIXED earlier

Earlier in Phase 2, notes using `- Status: READ` were not recognized by a parser that expected the older bold form `Status: **READ**`. This caused rebuild failures rather than silent promotion.

The current parser accepts both forms and fails closed if a note exists but has no valid durable `Status:` line.

**Impact:** status promotion was delayed; evidence was not silently lost or falsely promoted.

## Current workflow assessment

### `rebuild-ledger.yml`

- Generated files are already tracked, so TI-001 did not apply to this workflow.
- Exact source-tree denominator remains fail-closed at 164 blobs.
- Unique MP-ID and path counts are asserted.
- Current historical risk was TI-002 push concurrency; hardened on 2026-09-12.
- First hardened run completed successfully.

### `rebuild-connection-graph.yml`

- TI-001 affected its first run and is fixed.
- It now shares the serialized write lane with the ledger workflow.
- It validates `03_CONNECTION_EDGES.json` and `03_CONNECTION_INDEX.md` exist and are non-empty before commit.
- It retains the raw unresolved queue rather than silently dropping unresolved internal-looking references.

## What the failures did NOT invalidate

The audit found no evidence that these workflow failures changed the frozen source commit, altered source blob SHAs, deleted per-file notes, or fabricated READ status.

Phase 2's final result remains grounded by:

- frozen source commit `3cca18b368ae95cdbdebbff572ccafa662551015`;
- frozen tree `6e84c093fda2026396cea9fad6a924a6da0e1452`;
- exact 164-blob census;
- 164 durable per-file notes;
- a later successful deterministic ledger rebuild showing `164 READ / 0 UNREAD`.

Therefore the historical workflow failures primarily affected **publication freshness and automation reliability**, not the underlying frozen-source reading evidence.

## Residual risks / follow-up

1. The 71 historical failed Actions runs are not yet individually classified one-by-one. At least one large failure class is confirmed as non-fast-forward push races; the exact distribution among push races, earlier parser failures, and any other causes should not be guessed.
2. Generated outputs should never be considered authoritative merely because a workflow run is green; existence, content invariants, and source provenance must remain explicit gates.
3. When new generated workflows are added, use `git status --porcelain`, output existence checks, the shared concurrency group, and push-retry/rebase behavior by default.
4. Periodically compare durable notes to generated ledger status so a successful-looking automation cannot become the sole source of truth.

## Integrity conclusion

The audit found real historical automation defects, including a silent-success persistence bug and confirmed concurrent-write failures. Both known classes are now hardened. The defects could make generated artifacts temporarily stale or absent, but the evidence reviewed so far does not indicate corruption of the frozen-source audit or loss of the durable per-file notes.

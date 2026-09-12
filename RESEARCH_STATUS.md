# Research Status

## Project state

**IN PROGRESS**

Source repository: `mattpocock/skills`
Frozen commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
Frozen tree: `6e84c093fda2026396cea9fad6a924a6da0e1452`
Physical denominator: **164 blobs/files**

## Current phase position

Primary phase focus: **Phase 2 — Full Physical Read**.

Phase 1 is complete. The exact frozen recursive tree is now materialized in `01_MASTER_FILE_LEDGER.md` and `01_FILE_CENSUS.json`, generated deterministically from the Git tree by `scripts/build_master_ledger.py`. The workflow `.github/workflows/rebuild-ledger.yml` validates 164 unique blobs, 164 unique paths, 164 unique MP-IDs, and rejects truncated source trees.

The Phase 2 ledger baseline is intentionally conservative: all rows begin `UNREAD`. Prior chat reading does not promote status automatically. A row moves to `READ` only after its full frozen contents are re-inspected and durable evidence is recorded in this repository.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic MP-IDs, paths, mode/type, size, blob SHA, category, runtime-risk class, and conservative status. |
| 2. Full Physical Read | **IN PROGRESS** | Starting conservative queue: 164 UNREAD. Read status will be promoted only from durable evidence. |
| 3. Connection Mapping | IN PROGRESS / evidence accumulated | Several operative/reference relationships traced; exhaustive graph not complete. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified. |
| 5. History | IN PROGRESS | Root CHANGELOG fully read; several high-impact PRs/commits traced. |
| 6. Contradictions & Orphans | IN PROGRESS | Register initialized with current and historical defects. |
| 7. Runtime & Distribution | IN PROGRESS | Plugin/Codex/local-link architecture partly reconstructed. |
| 8. Second Pass | NOT STARTED formally | Some rereads happened, but no formal high-impact second-pass gate yet. |
| 9. Red-Team Verification | NOT STARTED formally | Individual falsification checks exist, but no systematic red-team pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Preliminary synthesis exists but is not final. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- Promoted invocation split: **14 user-invoked / 11 model-invoked**
- Phase 2 conservative baseline: **164 UNREAD / 0 READ / 0 CONNECTIONS TRACED / 0 VERIFIED**

The Phase 2 counts will change only when the durable ledger is updated.

## Immediate next execution steps

1. Read files in deterministic MP-ID order from `MP-0001` onward.
2. For each file, inspect complete frozen contents; use fixed line windows when responses truncate.
3. Store a durable per-file note under `02_FILE_NOTES/` containing the blob SHA, read evidence, observations, references, unresolved questions, and any claim/contradiction IDs created.
4. Promote the corresponding ledger row only after the note exists.
5. Continue until `UNREAD = 0`.
6. Do not return to broad KP recommendations until source gates are satisfied.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

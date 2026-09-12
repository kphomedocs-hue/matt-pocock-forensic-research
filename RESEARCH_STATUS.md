# Research Status

## Project state

**IN PROGRESS**

Source repository: `mattpocock/skills`
Frozen commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
Frozen tree: `6e84c093fda2026396cea9fad6a924a6da0e1452`
Physical denominator: **164 blobs/files**

## Current phase position

Primary phase focus: **Phase 2 — Full Physical Read**.

Phase 1 is complete. The exact frozen recursive tree is materialized in `01_MASTER_FILE_LEDGER.md` and `01_FILE_CENSUS.json`, generated deterministically from the Git tree by `scripts/build_master_ledger.py`. The workflow `.github/workflows/rebuild-ledger.yml` validates 164 unique blobs, 164 unique paths, 164 unique MP-IDs, rejects truncated source trees, and derives READ-or-higher status from durable notes in `02_FILE_NOTES/`.

The Phase 2 queue remains conservative: prior chat reading does not promote status automatically. A row moves to `READ` only after its full frozen contents are re-inspected and a durable per-file note exists.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic MP-IDs, paths, mode/type, size, blob SHA, category, runtime-risk class, and conservative status. |
| 2. Full Physical Read | **IN PROGRESS** | **30 READ / 134 UNREAD**. Next deterministic file: `MP-0031`. |
| 3. Connection Mapping | IN PROGRESS / evidence accumulated | Several operative/reference relationships traced; exhaustive graph not complete. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified. |
| 5. History | IN PROGRESS | Root CHANGELOG now has a formal Phase 2 durable reread; several high-impact PRs/commits have also been traced. |
| 6. Contradictions & Orphans | IN PROGRESS | CT-001 and CT-002 are now directly grounded in frozen durable file notes; CT-003 has docs-side evidence and awaits operative router reread. |
| 7. Runtime & Distribution | IN PROGRESS | Plugin/Codex/local-link architecture partly reconstructed; MP-0017 through MP-0019 have durable READ notes. |
| 8. Second Pass | NOT STARTED formally | No formal high-impact second-pass gate yet. |
| 9. Red-Team Verification | NOT STARTED formally | Individual falsification checks exist, but no systematic red-team pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Preliminary synthesis exists but is not final. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Phase 2 READ: **30**
- Phase 2 UNREAD: **134**
- CONNECTIONS TRACED: **0** formally in the durable ledger
- VERIFIED: **0** formally in the durable ledger
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- Promoted invocation split: **14 user-invoked / 11 model-invoked**

## Most recent durable range

`MP-0001` through `MP-0030` are READ with notes in `02_FILE_NOTES/`.

The latest range added:
- all three `.out-of-scope` negative-memory files;
- `AGENTS.md` symlink blob;
- complete fixed-window reread of root `CHANGELOG.md`;
- `CLAUDE.md`, `CONTEXT.md`, `LICENSE`, and complete fixed-window reread of root `README.md`;
- complete fixed-window reread of `docs/engineering/ask-matt.md`.

Durable findings strengthened in this range:
- CT-001: root README is stale on TDD red-green-refactor after refactor was removed from TDD and moved to review;
- CT-002: ask-matt docs still say 22 plugin skills / 13 user-invoked while frozen manifest/census shows 25 / 14;
- CT-003: ask-matt docs require trace evidence of opening target `SKILL.md`; operative enforcement still awaits formal durable router-source reread;
- negative-memory files are an explicit mechanism for retaining rejected product decisions;
- `AGENTS.md` is physically a symlink blob containing `CLAUDE.md`.

Research tooling note: the ledger-note parser was fixed to accept both `Status: **READ**` and `- Status: READ`; the rebuild workflow is green again.

## Immediate next execution steps

1. Continue deterministic reading at `MP-0031` (`docs/engineering/code-review.md`).
2. Inspect complete frozen contents; use fixed line windows whenever output truncates.
3. Store one durable note per file before status promotion.
4. Continue until `UNREAD = 0`.
5. Update claims/contradictions/history only when directly supported by the current file, without interrupting deterministic read order.
6. Do not return to broad KP recommendations until source gates are satisfied.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

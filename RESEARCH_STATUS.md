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
| 2. Full Physical Read | **IN PROGRESS** | **40 READ / 124 UNREAD**. Next deterministic file: `MP-0041`. |
| 3. Connection Mapping | IN PROGRESS / evidence accumulated | Several operative/reference relationships traced; exhaustive graph not complete. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified. |
| 5. History | IN PROGRESS | Root CHANGELOG has a formal Phase 2 durable reread; several high-impact PRs/commits have also been traced. |
| 6. Contradictions & Orphans | IN PROGRESS | Current register includes CT-001 through CT-010; several are now directly grounded in frozen durable file notes. |
| 7. Runtime & Distribution | IN PROGRESS | Plugin/Codex/local-link architecture partly reconstructed; distribution files already have durable READ notes. |
| 8. Second Pass | NOT STARTED formally | No formal high-impact second-pass gate yet. |
| 9. Red-Team Verification | NOT STARTED formally | Individual falsification checks exist, but no systematic red-team pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Preliminary synthesis exists but is not final. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Phase 2 READ: **40**
- Phase 2 UNREAD: **124**
- CONNECTIONS TRACED: **0** formally in the durable ledger
- VERIFIED: **0** formally in the durable ledger
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- Promoted invocation split: **14 user-invoked / 11 model-invoked**

## Most recent durable range

`MP-0001` through `MP-0040` are READ with notes in `02_FILE_NOTES/`.

The latest ten-file range covered the human docs for:
- code-review;
- codebase-design;
- diagnosing-bugs;
- domain-modeling;
- grill-with-docs;
- implement;
- improve-codebase-architecture;
- prototype;
- research;
- resolving-merge-conflicts.

Durable findings strengthened in this range:
- CT-007: diagnosing-bugs docs say redaction is unimplemented even though frozen CHANGELOG records it shipped in 1.2.3;
- CT-009: diagnosing-bugs docs still describe an architecture handoff that frozen invocation-fix history says was removed;
- CT-010: implement says review-before-commit, while code-review's three-dot diff excludes uncommitted work;
- recursive subagent spawning is a documented risk in code-review and research;
- research artifacts are intentionally short-lived and require explicit reuse pointers;
- prototype artifacts are preserved as primary-source evidence on throwaway branches rather than merged into main;
- merge-conflict resolution is explicitly intent-first, using primary sources rather than ours/theirs text selection.

Connection check: both the research repository and frozen source repository were successfully read before this range, and GitHub writes succeeded. The automatic ledger rebuild is currently reflecting notes correctly.

## Immediate next execution steps

1. Continue deterministic reading at `MP-0041` (`docs/engineering/setup-matt-pocock-skills.md`).
2. Inspect complete frozen contents; use fixed line windows whenever output truncates.
3. Store one durable note per file before status promotion.
4. Continue until `UNREAD = 0`.
5. Update claims/contradictions/history only when directly supported by the current file, without interrupting deterministic read order.
6. Do not return to broad KP recommendations until source gates are satisfied.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

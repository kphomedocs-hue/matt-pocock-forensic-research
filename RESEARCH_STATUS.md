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
| 2. Full Physical Read | **IN PROGRESS** | **64 READ / 100 UNREAD**. Next deterministic file: `MP-0065`. |
| 3. Connection Mapping | IN PROGRESS / evidence accumulated | Several operative/reference relationships traced; exhaustive graph not complete. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified. |
| 5. History | IN PROGRESS | Root CHANGELOG has a formal Phase 2 durable reread; several high-impact PRs/commits have also been traced. |
| 6. Contradictions & Orphans | IN PROGRESS | CT-003 is now confirmed from both docs and operative router source; CT-004/009/010 were strengthened in the latest block. |
| 7. Runtime & Distribution | IN PROGRESS | High-risk package/runtime block MP-0055 through MP-0059 has been fully read and persisted. |
| 8. Second Pass | NOT STARTED formally | No formal high-impact second-pass gate yet. |
| 9. Red-Team Verification | NOT STARTED formally | Individual falsification checks exist, but no systematic red-team pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Preliminary synthesis exists but is not final. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Phase 2 READ: **64**
- Phase 2 UNREAD: **100**
- CONNECTIONS TRACED: **0** formally in the durable ledger
- VERIFIED: **0** formally in the durable ledger
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- Promoted invocation split: **14 user-invoked / 11 model-invoked**

## Most recent durable range

`MP-0001` through `MP-0064` are READ with notes in `02_FILE_NOTES/`.

The latest range covered:
- package-lock root metadata and full dependency graph;
- package.json release/version scripts;
- maintainer link/list executables;
- plugin-version synchronization script;
- deprecated and engineering bucket docs;
- ask-matt phase-boundary support file;
- operative ask-matt router and Codex metadata.

Durable findings strengthened in this range:
- package-lock retains root version 0.0.0 while package.json is 1.2.3; sync tooling does not touch the lockfile;
- link-skills.sh destructively removes an existing non-symlink per-skill directory with `rm -rf` before symlinking, so isolated runtime testing is required;
- list-skills.sh enumerates all current SKILL.md files, not the promoted or local-link subsets;
- CT-003 is confirmed: ask-matt human docs demand primary-source target-skill verification, but the operative router contains no mandatory verification step;
- ask-matt operative router still repeats the removed diagnosing-bugs → improve-codebase-architecture handoff, reinforcing CT-009;
- ask-matt and Engineering README both preserve the implement → code-review-before-commit ordering implicated in CT-010;
- Engineering README remains stale on TDD red-green-refactor, strengthening CT-001.

## Immediate next execution steps

1. Continue deterministic reading at `MP-0065` (`skills/engineering/code-review/SKILL.md`).
2. Read operative engineering skills and their metadata/support files in path order.
3. Store one durable note per file before status promotion.
4. Continue until `UNREAD = 0`.
5. Promote contradictions from candidate to confirmed only when operative sources close both sides.
6. Do not return to broad KP recommendations until source gates are satisfied.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

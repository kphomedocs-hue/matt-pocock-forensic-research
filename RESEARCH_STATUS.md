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
| 2. Full Physical Read | **IN PROGRESS** | **20 READ / 144 UNREAD**. Next deterministic file: `MP-0021`. |
| 3. Connection Mapping | IN PROGRESS / evidence accumulated | Several operative/reference relationships traced; exhaustive graph not complete. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified. |
| 5. History | IN PROGRESS | Root CHANGELOG fully read historically; several high-impact PRs/commits traced. Formal Phase 2 durable reread will occur at its MP-ID. |
| 6. Contradictions & Orphans | IN PROGRESS | Register initialized with current and historical defects. |
| 7. Runtime & Distribution | IN PROGRESS | Plugin/Codex/local-link architecture partly reconstructed; MP-0017 through MP-0019 now have durable READ notes. |
| 8. Second Pass | NOT STARTED formally | No formal high-impact second-pass gate yet. |
| 9. Red-Team Verification | NOT STARTED formally | Individual falsification checks exist, but no systematic red-team pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Preliminary synthesis exists but is not final. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Phase 2 READ: **20**
- Phase 2 UNREAD: **144**
- CONNECTIONS TRACED: **0** formally in the durable ledger
- VERIFIED: **0** formally in the durable ledger
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- Promoted invocation split: **14 user-invoked / 11 model-invoked**

## Most recent durable range

`MP-0001` through `MP-0020` are READ with notes in `02_FILE_NOTES/`.

The most recent batch covered:
- invocation and docs governance;
- all current active changeset files through `wait-what-context-map`;
- Claude marketplace/plugin manifests;
- release workflow;
- root `.gitignore`.

Key later-phase candidates surfaced in this range include:
- official marketplace SHA pin can lag source/main state;
- plugin and skills.sh install routes are mutually exclusive because dual installation duplicates skills;
- em-dash prose cleanup caused invalid YAML in six skill frontmatters, and skills.sh silently skipped them;
- explicit Skill-tool invocation refactor violated the user-invoked-target invariant until the follow-up fix;
- release workflow has no explicit checks for several repository-wide invariants before version/tagging.

These remain READ-level observations until their connections/enforcement/history are formally promoted in later phases.

## Immediate next execution steps

1. Continue deterministic reading at `MP-0021`.
2. Inspect complete frozen contents; use fixed line windows whenever output truncates.
3. Store one durable note per file before status promotion.
4. Continue until `UNREAD = 0`.
5. Update claims/contradictions/history only when directly supported by the current file, without interrupting deterministic read order.
6. Do not return to broad KP recommendations until source gates are satisfied.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

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
| 2. Full Physical Read | **IN PROGRESS** | **111 READ / 53 UNREAD**. Next deterministic file: `MP-0112`. |
| 3. Connection Mapping | IN PROGRESS / evidence accumulated | Several operative/reference relationships traced; exhaustive graph not complete. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified; CT-010 confirmed from operative sources. |
| 5. History | IN PROGRESS | Root CHANGELOG has a formal Phase 2 durable reread; several high-impact PRs/commits have also been traced. |
| 6. Contradictions & Orphans | IN PROGRESS | CT-001, CT-003, CT-007, CT-008, CT-009 and CT-010 now have strong frozen-source evidence. |
| 7. Runtime & Distribution | IN PROGRESS | High-risk package/runtime block is complete; operative engineering skills are now read through triage. |
| 8. Second Pass | NOT STARTED formally | No formal high-impact second-pass gate yet. |
| 9. Red-Team Verification | NOT STARTED formally | Individual falsification checks exist, but no systematic red-team pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Preliminary synthesis exists but is not final. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Phase 2 READ: **111**
- Phase 2 UNREAD: **53**
- CONNECTIONS TRACED: **0** formally in the durable ledger
- VERIFIED: **0** formally in the durable ledger
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- Promoted invocation split: **14 user-invoked / 11 model-invoked**

## Most recent durable range

`MP-0001` through `MP-0111` are READ with notes in `02_FILE_NOTES/`.

The latest range covered:
- improve-codebase-architecture report/source/metadata;
- prototype logic/UI/source/metadata;
- research and resolving-merge-conflicts source/metadata;
- setup source plus GitHub/GitLab/local tracker/domain/triage-label templates;
- TDD source/metadata/mocking/tests;
- to-spec and to-tickets source/metadata;
- triage agent-brief/out-of-scope/source/metadata.

Durable findings strengthened in this range:
- CT-008 is source-confirmed: architecture report is a single self-contained file but requires Tailwind/Mermaid CDNs;
- prototype preserves validated design evidence on throwaway branches while removing prototype implementation from main;
- setup source confirms CLAUDE.md-first file selection regardless of harness and maps labels without creating them;
- the GitHub tracker template contains the external-PR `authorAssociation` command that docs identify as failing;
- operative TDD source explicitly says red → green only, while its Codex short description still says red-green-refactor, strengthening CT-001 into a docs/metadata drift;
- to-tickets formalizes tracer-bullet vertical slices and expand–migrate–contract for wide refactors;
- triage makes the agent brief the authoritative durable execution contract and `.out-of-scope/` the persistent negative product-memory layer.

## Immediate next execution steps

1. Continue deterministic reading at `MP-0112` (`skills/engineering/wayfinder/SKILL.md`).
2. Finish remaining engineering files, then in-progress, misc, productivity, and remaining support/metadata in path order.
3. Store one durable note per file before status promotion.
4. Continue until `UNREAD = 0`.
5. Update claims/contradictions/history only when directly supported by the current file, without interrupting deterministic read order.
6. Do not return to broad KP recommendations until source gates are satisfied.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

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
| 2. Full Physical Read | **IN PROGRESS** | **81 READ / 83 UNREAD**. Next deterministic file: `MP-0082`. |
| 3. Connection Mapping | IN PROGRESS / evidence accumulated | Several operative/reference relationships traced; exhaustive graph not complete. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified; CT-010 now confirmed from operative sources. |
| 5. History | IN PROGRESS | Root CHANGELOG has a formal Phase 2 durable reread; several high-impact PRs/commits have also been traced. |
| 6. Contradictions & Orphans | IN PROGRESS | CT-003, CT-007, CT-009 and CT-010 now have operative-source closure on their relevant sides. |
| 7. Runtime & Distribution | IN PROGRESS | High-risk package/runtime block MP-0055 through MP-0059 is complete; operative engineering skills are now being read in path order. |
| 8. Second Pass | NOT STARTED formally | No formal high-impact second-pass gate yet. |
| 9. Red-Team Verification | NOT STARTED formally | Individual falsification checks exist, but no systematic red-team pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Preliminary synthesis exists but is not final. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Phase 2 READ: **81**
- Phase 2 UNREAD: **83**
- CONNECTIONS TRACED: **0** formally in the durable ledger
- VERIFIED: **0** formally in the durable ledger
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- Promoted invocation split: **14 user-invoked / 11 model-invoked**

## Most recent durable range

`MP-0001` through `MP-0081` are READ with notes in `02_FILE_NOTES/`.

The latest range covered:
- operative `code-review` source and Codex metadata;
- codebase-design support files, source, and metadata;
- operative diagnosing-bugs source, metadata, and HITL template;
- domain-modeling ADR/CONTEXT formats, source, and metadata;
- grill-with-docs source and metadata;
- implement source and metadata.

Durable findings strengthened in this range:
- CT-010 is confirmed from operative sources: implement invokes code-review before commit, while code-review only inspects `<fixed-point>...HEAD` and fails on an empty committed diff;
- CT-007 is confirmed as stale human docs: operative diagnosing-bugs source has explicit redaction behavior;
- CT-009 is confirmed on the operative side: current diagnosing-bugs source contains no architecture handoff, while docs/router still describe it;
- grill-with-docs is a one-line wrapper whose correct behavior depends on loading both `grilling` and `domain-modeling`;
- codebase-design formalizes exact vocabulary and progressive-disclosure support files;
- diagnosing-bugs treats lack of a correct regression-test seam as an architectural finding rather than fabricating a shallow test;
- HITL capture explicitly warns against capturing credentials because values are echoed for agent parsing.

## Immediate next execution steps

1. Continue deterministic reading at `MP-0082` (`skills/engineering/improve-codebase-architecture/HTML-REPORT.md`).
2. Continue operative engineering skills and support/metadata files in path order.
3. Store one durable note per file before status promotion.
4. Continue until `UNREAD = 0`.
5. Update claims/contradictions/history only when directly supported by the current file, without interrupting deterministic read order.
6. Do not return to broad KP recommendations until source gates are satisfied.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

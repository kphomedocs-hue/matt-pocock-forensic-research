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
| 2. Full Physical Read | **IN PROGRESS** | **54 READ / 110 UNREAD**. Next deterministic file: `MP-0055`. |
| 3. Connection Mapping | IN PROGRESS / evidence accumulated | Several operative/reference relationships traced; exhaustive graph not complete. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified. |
| 5. History | IN PROGRESS | Root CHANGELOG has a formal Phase 2 durable reread; several high-impact PRs/commits have also been traced. |
| 6. Contradictions & Orphans | IN PROGRESS | Current register includes CT-001 through CT-010; several are directly grounded in frozen durable file notes. |
| 7. Runtime & Distribution | IN PROGRESS | Plugin/Codex/local-link architecture partly reconstructed; high-risk package/script block begins at MP-0055. |
| 8. Second Pass | NOT STARTED formally | No formal high-impact second-pass gate yet. |
| 9. Red-Team Verification | NOT STARTED formally | Individual falsification checks exist, but no systematic red-team pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Preliminary synthesis exists but is not final. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Phase 2 READ: **54**
- Phase 2 UNREAD: **110**
- CONNECTIONS TRACED: **0** formally in the durable ledger
- VERIFIED: **0** formally in the durable ledger
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- Promoted invocation split: **14 user-invoked / 11 model-invoked**

## Most recent durable range

`MP-0001` through `MP-0054` are READ with notes in `02_FILE_NOTES/`.

The latest range completed the remaining engineering/productivity human docs, including setup, TDD, to-spec, to-tickets, triage, wayfinder, wizard, grill-me, grilling, handoff, teach, to-questionnaire, wait-what, and writing-for-agents.

Durable findings strengthened in this range:
- TDD docs explicitly confirm red → green with refactoring moved to code-review, strengthening CT-001;
- setup docs acknowledge label-creation and harness-file-selection gaps;
- to-tickets docs acknowledge missing native GitHub sub-issue/blocking behavior despite `gh` support;
- wayfinder docs expose a control weakness where agent-authored Notes can override the default plan-don't-do rule;
- handoff docs explicitly classify summaries as secondary sources and warn that unverified assumptions become contracts;
- teach docs corroborate the glossary orphan/workspace-root ambiguity already tracked in CT-005/CT-006;
- writing-for-agents reinforces single-source, pointer, no-op, and anti-duplication principles that shape this forensic audit.

## Immediate next execution steps

1. Continue deterministic reading at `MP-0055` (`package-lock.json`).
2. Treat `MP-0055` through `MP-0059` as a high-risk package/runtime block and inspect completely.
3. Store one durable note per file before status promotion.
4. Continue until `UNREAD = 0`.
5. Update claims/contradictions/history only when directly supported by the current file, without interrupting deterministic read order.
6. Do not return to broad KP recommendations until source gates are satisfied.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

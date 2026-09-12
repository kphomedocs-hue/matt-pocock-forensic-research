# Research Status

## Project state

**IN PROGRESS**

Source repository: `mattpocock/skills`
Frozen commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
Frozen tree: `6e84c093fda2026396cea9fad6a924a6da0e1452`
Physical denominator: **164 blobs/files**

## Current phase position

Primary phase focus: **Phase 3 — Connection Mapping**.

Phase 1 and Phase 2 are complete. The exact frozen recursive tree is materialized in `01_MASTER_FILE_LEDGER.md` and `01_FILE_CENSUS.json`, generated deterministically from the Git tree by `scripts/build_master_ledger.py`. Every frozen physical blob has a durable per-file note and is mechanically marked READ.

Phase 3 now has a manually curated semantic graph (`03_CONNECTION_GRAPH.md`), a deterministic extractor (`scripts/build_connection_graph.py`), generated machine/index artifacts (`03_CONNECTION_EDGES.json`, `03_CONNECTION_INDEX.md`), and semantic reconciliation (`03_CONNECTION_RECONCILIATION.md`). The extractor reads all 164 frozen blobs by SHA from the census rather than relying on ranked search.

The first complete extraction produced **204 explicit/structural edges** and **5 unresolved internal-looking references**. All five were manually reconciled: three are consumer-repo example CONTEXT paths, one is Wayfinder's literal `(link)` template placeholder, and one is the generated `src/packages/README.md` target used by setup-ts-deep-modules. Therefore the first unresolved-reference batch is **5/5 reconciled, 0 confirmed broken repository links, 0 semantically unresolved cases**. The raw extractor still reports five by design so original machine evidence remains auditable.

The first workflow run also exposed a research-tooling bug: `git diff --quiet` ignored newly generated untracked graph files. The commit gate was corrected to use `git status --porcelain`, and the corrected workflow completed successfully and persisted the generated graph artifacts. This was an audit-repo tooling defect, not a source-repository finding.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic MP-IDs, paths, mode/type, size, blob SHA, category, runtime-risk class, and conservative status. |
| 2. Full Physical Read | **COMPLETE** | **164 READ / 0 UNREAD**. Every physical blob has a durable note in `02_FILE_NOTES/`. |
| 3. Connection Mapping | **IN PROGRESS** | Deterministic 164-blob extraction produced 204 explicit/structural edges. Its 5 unresolved-looking references are now 5/5 semantically reconciled with no broken repo links in that queue. Aggregate/plain-text/history/distribution/invocation joins still remain. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified; CT-010 confirmed from operative sources. |
| 5. History | IN PROGRESS | Root CHANGELOG has a formal durable reread; several high-impact PRs/commits have also been traced. |
| 6. Contradictions & Orphans | IN PROGRESS | Multiple current and historical contradictions have frozen-source evidence; exhaustive orphan/incoming-reference analysis remains. |
| 7. Runtime & Distribution | IN PROGRESS | Package/release/linking/plugin/Codex paths partly reconstructed; isolated runtime validation remains. |
| 8. Second Pass | NOT STARTED formally | No formal high-impact second-pass gate yet. |
| 9. Red-Team Verification | NOT STARTED formally | Individual falsification checks exist, but no systematic red-team pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Preliminary synthesis exists but is not final. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Phase 2 READ: **164**
- Phase 2 UNREAD: **0**
- Deterministic Phase 3 extracted edges: **204**
- Raw extractor unresolved internal-looking references: **5**
- Semantically reconciled from that queue: **5/5**
- Confirmed broken repository links from that queue: **0**
- Semantically unresolved from that queue: **0**
- CONNECTIONS TRACED: **0** formally promoted in the durable ledger
- VERIFIED: **0** formally promoted in the durable ledger
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- Promoted invocation split: **14 user-invoked / 11 model-invoked**

## Phase 3 extraction coverage

The deterministic extractor currently handles:
- internal relative Markdown links as `DOC_LINK`;
- explicit Skill-tool calls as `OPERATIVE_CALL`;
- `agents/openai.yaml` ownership as `CONFIG_BINDING`;
- Claude plugin skill entries as `DISTRIBUTION_ENTRY`;
- Git symlink targets as `SYMLINK`;
- exact per-file incoming/outgoing counts against the full 164-file census;
- an explicit unresolved-reference queue rather than silently dropping unresolved targets.

The semantic reconciliation layer records why machine-unresolved cases are or are not real repository defects without mutating the raw extraction evidence.

This extraction layer is evidence collection, not final semantic verification. Aggregate/plain-text references, history edges, installer/linker set semantics, invocation-policy joins, and false-positive/false-negative review still require closure before any file is promoted to `CONNECTIONS TRACED`.

## Immediate next execution steps

1. Expand aggregate relationships (especially ask-matt and setup templates) into exact per-target edges.
2. Join every `OPERATIVE_CALL` target against user/model invocation classification and flag illegal current calls.
3. Add deterministic plain-text/unique-filename reference scanning so orphan claims such as CT-005 do not depend only on Markdown links.
4. Build exact distribution symmetry across plugin, linker, list-skills, docs, router, and Codex metadata.
5. Add history-reference edges for behavior-shaping changes already identified in changesets/CHANGELOG/PR history.
6. Promote a file to `CONNECTIONS TRACED` only after outgoing, incoming, links, invocation class, and unresolved relationships are closed.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

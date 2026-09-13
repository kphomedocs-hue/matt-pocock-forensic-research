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

A foundation-hardening pass is complete before formal Phase 3 status promotion. `00_RESEARCH_SCHEMA.md` defines canonical evidence classes, issue origins, file-note fields, contradiction/history schemas, distribution truth, tooling integrity rules, and exact READ / CONNECTIONS TRACED / VERIFIED gates. `scripts/validate_foundation.py` plus `.github/workflows/validate-foundation.yml` mechanically validate the durable foundation and persist `00_FOUNDATION_INTEGRITY.json` / `.md` before enforcing the gate.

The latest foundation report is GREEN: **0 hard integrity errors / 0 normalization warnings**. It confirms **164/164 census rows**, **164/164 durable notes**, **164 READ**, direct frozen-commit metadata on all 164 notes, exact blob-SHA reconciliation, no missing contradiction/history references, and generated distribution invariants of **37 current skills / 25 Claude-plugin promoted / 33 locally linked / 37 Codex metadata owners**.

Legacy note metadata was normalized non-destructively by `scripts/normalize_note_metadata.py`: only missing canonical `Frozen commit` and `Category` lines were inserted from the authoritative census. Existing Status, evidence prose, observations, connections, and conclusions were not rewritten.

The contradiction register has a normalized closure overlay with `Origin`, `Defect state`, `Impact`, and `Resolution test / next evidence`; source-repository defects are explicitly separated from audit-tooling defects. The history ledger uses explicit lineage states `RECONCILED / PARTIAL / NOT MATERIAL`; H-002/H-003/H-004/H-009 remain PARTIAL rather than being overstated as complete.

Phase 3 has a manually curated semantic graph (`03_CONNECTION_GRAPH.md`), a deterministic extractor (`scripts/build_connection_graph.py`), generated machine/index artifacts (`03_CONNECTION_EDGES.json`, `03_CONNECTION_INDEX.md`), and semantic reconciliation (`03_CONNECTION_RECONCILIATION.md`). The extractor reads all 164 frozen blobs by SHA from the census rather than relying on ranked search.

Extraction rules version 3 now produces **305** current explicit/structural/passive edges: **37 CONFIG_BINDING, 25 DISTRIBUTION_ENTRY, 104 DOC_LINK, 15 OPERATIVE_CALL, 123 PASSIVE_REFERENCE, and 1 SYMLINK**. The passive-reference layer exhaustively scans exact repository-relative paths plus filenames whose basename is globally unique in the 164-file census. It found **104 exact-path + 19 unique-filename** passive references.

The five raw unresolved internal-looking references remain unchanged and are all semantically reconciled: three consumer-repo CONTEXT examples, Wayfinder's literal `(link)` template placeholder, and the generated `src/packages/README.md` target. They remain in raw extraction output for auditability, but **0/5 are confirmed broken repository links and 0/5 remain semantically unresolved**.

CT-005 has been sharpened by the passive scan. MP-0152 `GLOSSARY-FORMAT.md` has exactly **1 incoming reference**, from MP-0051 `docs/productivity/teach.md`; therefore it is **not a source-tree orphan**. The human docs explicitly state that Teach ships the file but `SKILL.md` no longer links to it. CT-005 remains OPEN as a confirmed **operative linkage gap**, not an unresolved orphan hypothesis.

The invocation-policy join is also complete at the current frozen source. Only current `SKILL.md` workflow instructions are now allowed to produce `OPERATIVE_CALL` edges; governance/history prose mentioning the Skill tool is no longer misclassified as executable dependency. All **37/37** current skills agree between Claude and Codex invocation policy: **22 user-invoked / 15 model-invoked overall, 0 policy mismatches**. There are **15 current operative Skill-tool calls and 0 illegal calls to user-invoked targets**.

A fresh audit-tooling recheck is complete. The incident model covers both failed and cancelled Actions runs. The durable ledger contains **78 failed + 7 cancelled = 85 incident runs**, **85/85 classified**, **0 unknown**, and **0 unresolved/review-required**. Every research workflow has its own concurrency lane and current Node-24-compatible action versions; successful proof runs exist for ledger, graph, foundation, note normalization, and incident classification. Full details are in `00_TOOLING_INTEGRITY_AUDIT.md`.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic MP-IDs, paths, mode/type, size, blob SHA, category, runtime-risk class, and conservative status. Foundation validator confirms durable provenance. |
| 2. Full Physical Read | **COMPLETE** | **164 READ / 0 UNREAD**. Every physical blob has a durable note in `02_FILE_NOTES/`; all notes carry direct canonical frozen-commit metadata. |
| 3. Connection Mapping | **IN PROGRESS** | Foundation/tooling gates green. v3 extraction = 305 edges; passive literal scan complete; 5 raw unresolved cases are 5/5 reconciled; invocation-policy join = 37/37 consistent and 0 illegal current operative calls. Router/distribution/history joins remain before promotion. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified; CT-010 confirmed from operative sources. |
| 5. History | IN PROGRESS | 9 durable entries; lineage state explicit. H-001/H-005/H-006/H-007/H-008 reconciled; H-002/H-003/H-004/H-009 partial. |
| 6. Contradictions & Orphans | IN PROGRESS | 11 current + 3 historical contradiction IDs. CT-005 source-tree orphan hypothesis disproved; operative glossary linkage gap confirmed. Broader exhaustive orphan/semantic-reference analysis remains. |
| 7. Runtime & Distribution | IN PROGRESS | Generated distribution truth confirms 37/25/33/37 core sets; full symmetry and runtime validation remain. |
| 8. Second Pass | NOT STARTED formally | No formal high-impact second-pass gate yet. |
| 9. Red-Team Verification | NOT STARTED formally | Individual falsification checks exist, but no systematic red-team pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Preliminary synthesis exists but is not final. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Phase 2 READ: **164**
- Phase 2 UNREAD: **0**
- Foundation hard errors: **0**
- Foundation normalization warnings: **0**
- Historical failed Actions runs classified: **78/78**
- Historical cancelled Actions runs classified: **7/7**
- Total tooling incident runs classified: **85/85**
- Tooling incidents unknown: **0**
- Tooling incidents unresolved/review-required: **0**
- Deterministic Phase 3 extracted edges: **305**
- PASSIVE_REFERENCE edges: **123**
- Current OPERATIVE_CALL edges: **15**
- Invocation policies joined: **37/37**
- Invocation-policy mismatches: **0**
- Illegal current operative calls: **0**
- Overall invocation split: **22 user-invoked / 15 model-invoked**
- Raw extractor unresolved internal-looking references: **5**
- Semantically reconciled from that queue: **5/5**
- Confirmed broken repository links from that queue: **0**
- Semantically unresolved from that queue: **0**
- CONNECTIONS TRACED: **0** formally promoted in the durable ledger
- VERIFIED: **0** formally promoted in the durable ledger
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- Codex metadata owners: **37**
- Promoted invocation split: **14 user-invoked / 11 model-invoked**

## Note-schema measurement

The foundation validator measures older note structure without rewriting evidence merely for formatting:
- read-evidence section family present: **144 / 164**;
- source-facts/observations section family present: **162 / 164**;
- explicit connections section family present: **27 / 164**;
- explicit unresolved/later-check section family present: **20 / 164**.

These are normalization/coverage measurements, not Phase 2 failures. Phase 3 will populate connection state through the graph and promotion evidence rather than mass-editing notes with empty headings.

## Immediate next execution steps

1. Expand aggregate/router relationships, especially ask-matt, into exact per-target skill edges and compare router coverage to the promoted skill set.
2. Build exact distribution symmetry across plugin, link-skills, list-skills, top/bucket READMEs, router, and Codex metadata.
3. Add history-reference edges for behavior-shaping changes already identified in changesets/CHANGELOG/PR history.
4. Expand setup aggregate/template relationships where exact per-support-file edges remain implicit.
5. Encode the CONNECTIONS TRACED promotion gate in Phase 3 automation using the canonical schema; do not promote files merely because extraction exists.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

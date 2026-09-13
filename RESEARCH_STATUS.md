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

The latest foundation report is GREEN: **0 hard integrity errors / 0 normalization warnings**. It confirms **164/164 census rows**, **164/164 durable notes**, **164 READ**, direct frozen-commit metadata on all 164 notes, exact blob-SHA reconciliation, and no missing contradiction/history references.

Phase 3 now has a manually curated semantic graph (`03_CONNECTION_GRAPH.md`), deterministic connection extraction (`scripts/build_connection_graph.py`), generated graph/index (`03_CONNECTION_EDGES.json`, `03_CONNECTION_INDEX.md`), semantic reconciliation (`03_CONNECTION_RECONCILIATION.md`), an ask-matt router matrix (`03_ROUTER_MATRIX.md` / `.json`), and a distribution symmetry matrix (`03_DISTRIBUTION_MATRIX.md` / `.json`). All frozen-source extraction is SHA-grounded against the 164-file census rather than ranked search.

Extraction rules version 3 produces **305** current explicit/structural/passive edges: **37 CONFIG_BINDING, 25 DISTRIBUTION_ENTRY, 104 DOC_LINK, 15 OPERATIVE_CALL, 123 PASSIVE_REFERENCE, and 1 SYMLINK**. The passive layer exhaustively scans exact repository-relative paths plus filenames whose basename is globally unique in the census: **104 exact-path + 19 unique-filename** references.

The five raw unresolved internal-looking references are all semantically reconciled: three consumer-repo CONTEXT examples, Wayfinder's literal `(link)` template placeholder, and the generated `src/packages/README.md` target. They remain in raw output for auditability, but **0/5 are confirmed broken repository links and 0/5 remain semantically unresolved**.

CT-005 has been sharpened by the passive scan. MP-0152 `GLOSSARY-FORMAT.md` has exactly **1 incoming reference**, from MP-0051 `docs/productivity/teach.md`; therefore it is **not a source-tree orphan**. The docs explicitly state that Teach ships the file but `SKILL.md` no longer links to it. CT-005 remains OPEN as a confirmed **operative linkage gap**.

The invocation-policy join is complete for the frozen source. Only current `SKILL.md` workflow instructions produce `OPERATIVE_CALL` edges; governance/history prose is no longer misclassified as executable dependency. All **37/37** current skills agree between Claude and Codex invocation policy: **22 user-invoked / 15 model-invoked overall, 0 policy mismatches**. There are **15 current operative Skill-tool calls and 0 illegal calls to user-invoked targets**.

The ask-matt router join is also complete at the exact-target level. Against the **25 promoted plugin skills**, ask-matt is expected to route to the other **24**; it mentions **24/24**, with **0 missing promoted targets and 0 extra non-promoted targets**. This means the historical router-completeness defect CT-H02 is not recurring in the frozen target set, although route semantics can still be stale (for example CT-009).

Distribution symmetry is now generated per skill across plugin promotion, maintainer local linking, list-skills visibility, root README, bucket README, docs page, ask-matt, and Codex metadata. The result has **0 automated symmetry anomalies**. Dimension counts are: **25 plugin promoted / 33 locally linked / 37 list-visible / 25 root-README visible / 37 bucket-README visible / 25 docs pages / 24 ask-matt targets / 37 Codex metadata owners**. The differing 25/33/37 sets are therefore intentional distribution tiers, not unexplained drift.

The audit-tooling incident model covers both failed and cancelled Actions runs and remains closed at its last durable classification: **85/85 classified, 0 unknown, 0 unresolved/review-required**. New Phase 3 router/distribution workflows completed successfully and introduced no failure incident.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic MP-IDs, paths, mode/type, size, blob SHA, category, runtime-risk class, and conservative status. |
| 2. Full Physical Read | **COMPLETE** | **164 READ / 0 UNREAD**. Every physical blob has a durable note with canonical frozen provenance. |
| 3. Connection Mapping | **IN PROGRESS** | Literal/passive scan complete; invocation-policy join complete; ask-matt router coverage 24/24; distribution symmetry complete with 0 anomalies; 5 raw unresolved cases 5/5 reconciled. History-reference edges and formal per-file promotion remain. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified; CT-010 confirmed from operative sources. |
| 5. History | IN PROGRESS | 9 durable entries; lineage state explicit. H-001/H-005/H-006/H-007/H-008 reconciled; H-002/H-003/H-004/H-009 partial. |
| 6. Contradictions & Orphans | IN PROGRESS | 11 current + 3 historical contradiction IDs. CT-005 source-tree orphan hypothesis disproved; operative glossary linkage gap confirmed. |
| 7. Runtime & Distribution | IN PROGRESS | Exact 37/25/33 distribution tiers reconstructed with 0 automated symmetry anomalies; deeper runtime validation remains. |
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
- Tooling incident runs classified at last full incident rebuild: **85/85**
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
- Ask-matt expected promoted targets: **24**
- Ask-matt promoted targets covered: **24/24**
- Ask-matt extra non-promoted targets: **0**
- Distribution symmetry anomalies: **0**
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- List-skills visible set: **37**
- Codex metadata owners: **37**
- CONNECTIONS TRACED: **0** formally promoted in the durable ledger
- VERIFIED: **0** formally promoted in the durable ledger

## Note-schema measurement

The foundation validator measures older note structure without rewriting evidence merely for formatting:
- read-evidence section family present: **144 / 164**;
- source-facts/observations section family present: **162 / 164**;
- explicit connections section family present: **27 / 164**;
- explicit unresolved/later-check section family present: **20 / 164**.

These are normalization/coverage measurements, not Phase 2 failures. Phase 3 will populate connection state through generated evidence and promotion gates rather than mass-editing notes with empty headings.

## Immediate next execution steps

1. Add deterministic `HISTORY_REFERENCE` edges for behavior-shaping changes already identified in changesets, CHANGELOG, and durable history entries.
2. Reconcile the remaining setup/template aggregate relationships where exact support-file relationships are not already covered by DOC_LINK/PASSIVE_REFERENCE.
3. Build a per-file Phase 3 closure index combining outgoing/incoming edges, invocation legality, distribution/router membership, unresolved disposition, and relevant history state.
4. Encode the `CONNECTIONS TRACED` promotion gate mechanically and promote only files whose full connection obligations are satisfied.
5. Keep `VERIFIED = 0` until behavior/history/runtime reconciliation is separately complete.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

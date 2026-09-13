# Research Status

## Project state

**IN PROGRESS**

Source repository: `mattpocock/skills`
Frozen commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
Frozen tree: `6e84c093fda2026396cea9fad6a924a6da0e1452`
Physical denominator: **164 blobs/files**

## Storage authority

This GitHub repository is the authoritative project state. ChatGPT conversation history, memory, summaries, scratchpads, or transient tool output are **not authoritative storage** and must never be required to resume the audit.

Any fact needed to continue the project must be recoverable from committed GitHub artifacts. If chat prose and committed machine artifacts disagree, the committed source/provenance artifacts win and the human summary must be repaired.

## Current phase position

Primary phase focus: **Phase 4 — Behavior & Enforcement**.

Phases 1–3 are complete. The project is **not VERIFIED**: Phase 4 behavior/enforcement, remaining history lineage, contradiction resolution, runtime observation, second pass, and red-team verification remain before Phase 10 synthesis.

## Foundation state

Latest foundation report is GREEN:

- **164/164** census rows;
- **164/164** durable per-file notes;
- **164/164 CONNECTIONS TRACED**;
- direct frozen-commit metadata on all 164 notes;
- exact blob-SHA reconciliation;
- **0 hard integrity errors**;
- **0 warnings**;
- no missing contradiction/history references;
- formal `VERIFIED`: **0/164**.

`00_RESEARCH_SCHEMA.md` is the canonical status/gate definition.

## Phase 3 — COMPLETE

Authoritative generated state:

- semantic supplement: `03_CONNECTION_GRAPH.md`;
- deterministic extractor: `scripts/build_connection_graph.py`;
- machine graph/index: `03_CONNECTION_EDGES.json`, `03_CONNECTION_INDEX.md`;
- reference reconciliation: `03_CONNECTION_RECONCILIATION.md`, `03_REFERENCE_DISPOSITIONS.json`;
- orphan/zero-incoming reconciliation: `03_ORPHAN_RECONCILIATION.md`, `03_ORPHAN_DISPOSITIONS.json`;
- router matrix: `03_ROUTER_MATRIX.md/.json`;
- distribution matrix: `03_DISTRIBUTION_MATRIX.md/.json`;
- history bindings: `03_HISTORY_BINDINGS.md/.json`;
- per-file closure gate: `03_PHASE3_CLOSURE_INDEX.md/.json`;
- second-order quality report: `03_PHASE3_QUALITY.md/.json`;
- cryptographic build provenance: `03_PHASE3_BUILD_MANIFEST.md/.json`.

### Connection graph v5

Extraction rules version **5** reads all 164 frozen blobs by exact census blob SHA and currently produces **554 edges**:

- `CONFIG_BINDING`: **37**
- `DISTRIBUTION_ENTRY`: **25**
- `DOC_LINK`: **104**
- `OPERATIVE_CALL`: **15**
- `PASSIVE_REFERENCE`: **123**
- `SKILL_REFERENCE`: **223**
- `SUPPORT_BINDING`: **26**
- `SYMLINK`: **1**

Graph integrity/provenance:

- stable content-derived edge IDs: **554/554**;
- edges with literal source-line provenance: **490/554**;
- invocation policies joined: **37/37**;
- Claude↔Codex policy mismatches: **0**;
- illegal operative calls to user-invoked targets: **0**;
- weak backtick-only skill references tracked separately: **129**;
- files relying only on weak backtick references as orphan proof: **0**;
- extra Markdown/HTML/autolink syntax producing unmapped internal links: **0**;
- support-owner gaps: **0**.

The five raw unresolved internal-looking references remain **5/5 semantically reconciled**, with **0** confirmed broken repository links and **0** semantically unresolved cases.

Router join:

- promoted plugin skills: **25**;
- expected ask-matt targets other than itself: **24**;
- covered: **24/24**;
- missing: **0**;
- non-promoted extras: **0**.

Distribution symmetry:

- plugin promoted: **25**;
- maintainer local-linked: **33**;
- list-skills visible: **37**;
- root README visibility is checked by exact Markdown link, not name-token presence;
- bucket README visibility is checked by exact Markdown link;
- Codex metadata owners: **37**;
- automated distribution anomalies: **0**.

History bindings derive H-event definitions from durable `05_HISTORY_LEDGER.md`, not a duplicated hardcoded event table. H-001…H-009 state/ref/area parity is **9/9 green** in the Phase 3 quality gate.

Formal Phase 3 closure:

- files: **164**;
- READY_CANDIDATE: **164**;
- blockers: **0**;
- formal `CONNECTIONS TRACED`: **164/164**;
- formal `VERIFIED`: **0/164**;
- Phase 3 quality hard errors: **0**;
- Phase 3 quality review items: **0**;
- Phase 3 quality remaining improvements: **0**.

The Phase 3 build manifest records SHA-256 fingerprints for the generator/acceptance inputs and authoritative generated outputs so a future session can verify that the committed state belongs together.

## Phase 4 — Behavior & Enforcement

Structured working evidence is already durable in GitHub:

- `04_BEHAVIOR_MATRIX.json`;
- `04_BEHAVIOR_MATRIX.md`;
- `04_BEHAVIOR_INTEGRITY.json`;
- `04_CONTRADICTION_REGISTER.md`;
- `scripts/validate_behavior_matrix.py`;
- `.github/workflows/validate-phase4-behavior.yml`.

Current validated matrix contains **20 behavior rows** with **0 hard integrity errors**. Runtime observed remains **0/20**, intentionally preventing static analysis from being overstated as end-to-end proof.

Current contradiction/enforcement register contains **13 current IDs** plus **3 historical IDs**. CT-012 records the setup-ts-deep-modules prose/config rule-count mismatch; CT-013 records Wayfinder's self-authored planning-override authority weakness. Detailed evidence is in the contradiction register and behavior matrix rather than relying on chat prose.

## Tooling state

Current durable incident ledger:

- failed Actions runs: **82**;
- cancelled Actions runs: **7**;
- total incident runs: **89**;
- classified: **89/89**;
- unknown: **0**;
- unresolved/review-required: **0**;
- evidence-corruption incidents found: **0**.

Phase 3 generation is consolidated into `.github/workflows/rebuild-phase3-state.yml`, which rebuilds dependent state in one ordered atomic pipeline and runs manifest/quality validation before publication. Formal status promotion remains separate and fail-closed.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic IDs/provenance and durable ledger rows. |
| 2. Full Physical Read | **COMPLETE** | Full contents of 164/164 physical blobs inspected; UNREAD = 0. |
| 3. Connection Mapping | **COMPLETE** | **164/164 CONNECTIONS TRACED**; 554-edge v5 graph; quality hard errors/review items/improvements = 0. |
| 4. Behavior & Enforcement | **IN PROGRESS — PRIMARY FOCUS** | Validated 20-row behavior matrix; runtime observed remains 0/20. |
| 5. History | IN PROGRESS | 9 durable H-events; remaining partial lineage is kept in `05_HISTORY_LEDGER.md`. |
| 6. Contradictions & Orphans | IN PROGRESS | 13 current + 3 historical CT IDs; Phase 3 orphan questions closed. |
| 7. Runtime & Distribution | IN PROGRESS | Static distribution topology reconstructed; deeper runtime/end-to-end observation remains. |
| 8. Second Pass | NOT STARTED formally | High-impact second-pass gate not yet executed systematically. |
| 9. Red-Team Verification | NOT STARTED formally | No complete systematic absolute/numerical-claim falsification pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Final synthesis waits for verification gates. |

## Resume instruction

Future sessions must reload this GitHub repository first. Minimum starting set:

1. `00_RESEARCH_MANIFEST.md`
2. `00_RESEARCH_SCHEMA.md`
3. `00_STORAGE_INTEGRITY_AUDIT.md`
4. `RESEARCH_STATUS.md`
5. `00_FOUNDATION_INTEGRITY.md`
6. `00_TOOLING_INTEGRITY_AUDIT.md`
7. `00_TOOLING_FAILURE_LEDGER.json`
8. `01_FILE_CENSUS.json`
9. `01_MASTER_FILE_LEDGER.md`
10. `03_CONNECTION_EDGES.json`
11. `03_PHASE3_CLOSURE_INDEX.json`
12. `03_PHASE3_QUALITY.json`
13. `03_PHASE3_BUILD_MANIFEST.json`
14. `04_BEHAVIOR_MATRIX.json`
15. `04_BEHAVIOR_INTEGRITY.json`
16. `04_CONTRADICTION_REGISTER.md`
17. `05_HISTORY_LEDGER.md`

Do **not** resume from ChatGPT memory or chat summaries as authoritative state.

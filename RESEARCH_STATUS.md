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

Formal Phase 3 closure:

- files: **164**;
- READY_CANDIDATE: **164**;
- blockers: **0**;
- formal `CONNECTIONS TRACED`: **164/164**;
- formal `VERIFIED`: **0/164**;
- Phase 3 quality hard errors: **0**;
- Phase 3 quality review items: **0**;
- Phase 3 quality remaining improvements: **0**.

## Phase 4 — Behavior & Enforcement

Structured working evidence is durable in GitHub:

- `04_BEHAVIOR_MATRIX.json`;
- `04_BEHAVIOR_MATRIX.md`;
- `04_BEHAVIOR_INTEGRITY.json`;
- `04_CONTRADICTION_REGISTER.md`;
- `scripts/validate_behavior_matrix.py`;
- `.github/workflows/validate-phase4-behavior.yml`.

The current validated matrix contains **29 behavior rows** with **0 hard integrity errors**. Runtime observed remains **0/29**, intentionally preventing static analysis from being overstated as end-to-end proof.

Current state counts:

- `CONFIRMED_DRIFT`: **5**
- `CONFIRMED_GAP`: **5**
- `CONFIRMED_MATCH`: **5**
- `CONFIRMED_WEAKNESS`: **2**
- `RUNTIME_UNKNOWN`: **4**
- `STATICALLY_ENFORCED`: **8**

Machine-enforcement classification:

- `True`: **8**
- `PARTIAL`: **2**
- `False`: **19**

The current contradiction/enforcement register contains **14 current IDs** plus **3 historical IDs**. CT-014 records a newly established `implement-spec` workflow gap: after the only required final `/code-review`, all findings are fixed by one implementer subagent and the PR is then marked ready without a required second review, finding-by-finding verification, or equivalent post-fix acceptance gate.

The latest Phase 4 expansion also records:

- setup's explicit draft-before-write human checkpoint;
- setup's intentionally prompt-driven verify/check design;
- diagnosing-bugs' strict red-capable feedback-loop gate;
- triage's prompt-only one-category/one-state invariant and its normal verification-before-grilling sequence;
- implement-spec frontier scheduling as runtime-dependent rather than mechanically scheduled;
- domain-modeling's inline CONTEXT/ADR capture discipline;
- release workflow version/tag wiring as statically enforced.

Validation proof: GitHub Actions run `34743483922` — **SUCCESS** for the 29-row matrix and CT-014 cross-reference set.

## Tooling state

Current durable incident ledger remains closed:

- failed Actions runs: **82**;
- cancelled Actions runs: **7**;
- total incident runs: **89**;
- classified: **89/89**;
- unknown: **0**;
- unresolved/review-required: **0**;
- evidence-corruption incidents found: **0**.

The successful Phase 4 expansion introduced no new failed/cancelled incident.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic IDs/provenance and durable ledger rows. |
| 2. Full Physical Read | **COMPLETE** | Full contents of 164/164 physical blobs inspected; UNREAD = 0. |
| 3. Connection Mapping | **COMPLETE** | **164/164 CONNECTIONS TRACED**; 554-edge v5 graph; quality hard errors/review items/improvements = 0. |
| 4. Behavior & Enforcement | **IN PROGRESS — PRIMARY FOCUS** | Validated **29-row** behavior matrix; **14 current CT IDs**; runtime observed remains **0/29**. |
| 5. History | IN PROGRESS | 9 durable H-events; remaining partial lineage is kept in `05_HISTORY_LEDGER.md`. |
| 6. Contradictions & Orphans | IN PROGRESS | **14 current + 3 historical CT IDs**; Phase 3 orphan questions closed. |
| 7. Runtime & Distribution | IN PROGRESS | Static distribution topology reconstructed; deeper runtime/end-to-end observation remains. |
| 8. Second Pass | NOT STARTED formally | High-impact second-pass gate not yet executed systematically. |
| 9. Red-Team Verification | NOT STARTED formally | No complete systematic absolute/numerical-claim falsification pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Final synthesis waits for verification gates. |

## Immediate next execution steps — Phase 4

1. Continue promoted-workflow coverage through `to-spec`, `to-tickets`, `codebase-design`, `research`, `prototype`, and remaining engineering/productivity workflows.
2. Test cross-skill setup assumptions, especially whether configured triage-label names are actually materialized/usable on external trackers rather than merely written into mapping docs.
3. Continue separating prompt-only completion criteria from executable/CI enforcement and from runtime-dependent behavior.
4. Create targeted runtime-test plans only where static analysis cannot settle the claim; do not manufacture runtime evidence by inference.
5. Continue Phase 5 separately for H-003/H-004/H-009 and current contradiction lineages.
6. Keep `VERIFIED = 0` until applicable Phase 4–9 gates are satisfied per file/claim.

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

# Research Status

## Project state

**IN PROGRESS**

Source repository: `mattpocock/skills`
Frozen commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
Frozen tree: `6e84c093fda2026396cea9fad6a924a6da0e1452`
Physical denominator: **164 blobs/files**

## Storage authority

This GitHub repository is the authoritative project state. ChatGPT conversation history, memory, summaries, scratchpads, or transient tool output are **not authoritative storage** and must never be required to resume the audit.

If chat prose and committed machine artifacts disagree, the committed source/provenance artifacts win and the human summary must be repaired.

## Current phase position

Primary phase focus: **Phase 4 — Behavior & Enforcement**.

Phases 1–3 are complete. The project is **not VERIFIED**: Phase 4 runtime/enforcement depth, remaining history lineage, contradiction resolution, runtime/distribution observation, second pass, and red-team verification remain before Phase 10 synthesis.

## Foundation state

Latest foundation report is GREEN:

- **164/164** census rows;
- **164/164** durable per-file notes;
- **164/164 CONNECTIONS TRACED**;
- direct frozen-commit metadata on all notes;
- exact blob-SHA reconciliation;
- **0 hard integrity errors**;
- **0 warnings**;
- current contradiction register recognized through **CT-020** plus CT-H01…CT-H03;
- current contradiction parity is exact and contiguous;
- formal `VERIFIED`: **0/164**.

## Phase 3 — COMPLETE

Current durable Phase 3 state:

- extraction rules: **v5**;
- graph edges: **554**;
- stable edge IDs: **554/554**;
- literal source-line provenance: **490/554**;
- invocation policies joined: **37/37**;
- Claude↔Codex mismatches: **0**;
- illegal operative calls: **0**;
- weak-only orphan proofs: **0**;
- unmapped extra-link syntax: **0**;
- support-owner gaps: **0**;
- Phase 3 quality hard errors/review items/improvements: **0 / 0 / 0**;
- formal `CONNECTIONS TRACED`: **164/164**.

Authoritative generated artifacts are the graph/index, router/distribution/history matrices, closure index, Phase 3 quality report, and SHA-256 build manifest.

## Phase 4 — Behavior & Enforcement

Authoritative working artifacts:

- `04_BEHAVIOR_MATRIX.json`
- `04_BEHAVIOR_MATRIX.md`
- `04_BEHAVIOR_INTEGRITY.json`
- `04_BEHAVIOR_COVERAGE.json`
- `04_BEHAVIOR_COVERAGE.md`
- `04_RUNTIME_OBSERVATION_QUEUE.json`
- `04_RUNTIME_OBSERVATION_QUEUE.md`
- `04_RUNTIME_EXECUTION_EVIDENCE.json`
- `04_RUNTIME_EXECUTION_EVIDENCE.md`
- `04_CONTRADICTION_REGISTER.md`
- `scripts/validate_behavior_matrix.py`
- `scripts/build_phase4_coverage.py`
- `scripts/build_phase4_runtime_queue.py`
- `scripts/run_phase4_local_runtime_checks.py`
- `scripts/apply_phase4_batch.py`
- `.github/workflows/validate-phase4-behavior.yml`
- `.github/workflows/apply-phase4-batch.yml`
- `.github/workflows/phase4-local-runtime-checks.yml`

Current validated state:

- behavior rows: **65**;
- hard integrity errors: **0**;
- runtime observed: **7/65**;
- runtime/evidence queue classified: **65/65**;
- current CT coverage: **20/20**;
- uncovered current CT IDs: **0**;
- current `SKILL.md` denominator: **37**;
- current skills with at least one behavior contract: **37/37**;
- uncovered current skills: **0**;
- high-risk non-SKILL denominator: **71**;
- high-risk non-SKILL surfaces with at least one behavior contract: **71/71**;
- uncovered high-risk non-SKILL surfaces: **0**.

Behavior-matrix state counts:

- `CONFIRMED_DRIFT`: **5**
- `CONFIRMED_GAP`: **10**
- `CONFIRMED_MATCH`: **30**
- `CONFIRMED_WEAKNESS`: **3**
- `RUNTIME_UNKNOWN`: **9**
- `STATICALLY_ENFORCED`: **8**

Machine-enforcement counts:

- `True`: **8**
- `PARTIAL`: **7**
- `False`: **50**

Evidence-depth queue:

- `EXECUTION_OBSERVATION`: **30 total / 7 observed / 23 pending**
- `EXTERNAL_DEPENDENCY_VALIDATION`: **7 / 0 / 7**
- `MACHINE_CONSUMER_VALIDATION`: **4 / 0 / 4**
- `PROMPT_REDTEAM_LATER`: **24 / 0 / 24**
- total pending: **58**.

The first deterministic local-runtime batch directly observed **B-015, B-018, and B-056** against the exact frozen source commit. All acceptance checks passed. The report records only benign synthetic fixtures: wizard template first-run/rerun behavior, plugin-version drift detection/repair, and HITL capture behavior. It does not use real credentials or claim broader prompt/harness verification.

The **37/37 skill** and **71/71 high-risk non-SKILL** results are breadth denominators only. They prove that no current operative skill or behavior-relevant high-risk non-SKILL surface is completely absent from the Phase 4 matrix. They do **not** prove that every behavior is exhausted, that machine-readable policy is honored at runtime, or that any file is VERIFIED.

### Current contradiction/enforcement register

The register contains **20 current IDs** plus **3 historical IDs**.

Newest source/audit findings:

- **CT-019 — audit false-positive correction:** exact frozen-command reproduction showed that `grep -r " as [A-Z]"` does find the advertised `as unknown as Type` form because the later ` as Type` substring matches. CT-019 is retained as a **RESOLVED audit correction**, not a source defect.
- **CT-020 — scaffold-exercises variant/linter contract:** prose permits a solution-only exercise while the same source's linter summary requires a primary variant from problem/explainer/explainer.1, excluding solution-only. This remains OPEN.

Earlier Phase 4 findings CT-014…CT-018 remain durable in the contradiction register and behavior matrix.

No Phase 4 row is treated as sufficient for `VERIFIED` by itself.

## Tooling state

Latest closed incident ledger:

- failed runs: **83**;
- cancelled runs: **7**;
- total incidents: **90**;
- classified: **90/90**;
- unknown: **0**;
- unresolved/review-required: **0**;
- evidence-corruption incidents found: **0**.

Run `34745903691` was the first Phase 4 batch-importer bootstrap run. It failed closed because the workflow initially triggered on its own creation before a batch file existed. No research data changed. Automatic importer execution is now limited to actual `04_PHASE4_BATCH.json` pushes, and the exact run is classified as fixed.

The tooling classifier now monitors Phase 4 validation, batch application, prior runtime smoke, and the deterministic **Phase 4 local runtime checks** workflow. Unknown future runtime-workflow failures will fail the classifier closure gate until adjudicated rather than being silently categorized.

Because bot commits cannot be relied upon to retrigger downstream Actions, Phase 4 mutation workflows refresh behavior validation, breadth coverage, runtime/evidence queue, and foundation parity inside the same atomic workflow before publication.

The first local runtime evidence workflow run **34749869035** completed successfully and published the runtime evidence plus regenerated Phase 4 state.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic IDs/provenance and durable ledger rows. |
| 2. Full Physical Read | **COMPLETE** | 164/164 physical blobs inspected; UNREAD = 0. |
| 3. Connection Mapping | **COMPLETE** | **164/164 CONNECTIONS TRACED**; 554-edge v5 graph; quality errors/review items/improvements = 0. |
| 4. Behavior & Enforcement | **IN PROGRESS — PRIMARY FOCUS** | Validated **65-row** matrix; **20/20 current CTs**, **37/37 current skills**, **71/71 high-risk non-SKILL surfaces** represented; evidence queue **65/65 classified**; runtime observed **7/65**. |
| 5. History | IN PROGRESS | 9 durable H-events; partial lineage remains explicitly partial. |
| 6. Contradictions & Orphans | IN PROGRESS | **20 current + 3 historical CT IDs**; CT-019 is a resolved audit correction, CT-020 remains open. |
| 7. Runtime & Distribution | IN PROGRESS | Static topology reconstructed; deterministic local runtime observation has begun; deeper harness/external/end-to-end observation remains. |
| 8. Second Pass | NOT STARTED formally | High-impact second-pass gate not yet executed systematically. |
| 9. Red-Team Verification | NOT STARTED formally | No complete systematic falsification pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Final synthesis waits for verification gates. |

## Immediate next execution steps — Phase 4

1. Continue the deterministic runtime/evidence queue: **23 pending EXECUTION_OBSERVATION** rows remain after the first local-runtime batch.
2. Prioritize additional safe local executable/config contracts before external services: repository scripts, skill scripts/config, dependency/package behavior, and the remaining `RUNTIME_UNKNOWN` rows that can be isolated without live credentials.
3. Keep machine-consumer, external-dependency, and prompt-red-team classes separate; do not promote them using evidence from the wrong layer.
4. Trace history for CT-020 and remaining partial H-events; CT-019 history should preserve that it was an audit false positive, not a source regression.
5. Keep `VERIFIED = 0` until applicable Phase 4–9 gates close per file/claim.

## Resume instruction

Future sessions must reload this GitHub repository first, beginning with:

1. `00_RESEARCH_MANIFEST.md`
2. `00_RESEARCH_SCHEMA.md`
3. `00_STORAGE_INTEGRITY_AUDIT.md`
4. `RESEARCH_STATUS.md`
5. `00_FOUNDATION_INTEGRITY.json`
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
16. `04_BEHAVIOR_COVERAGE.json`
17. `04_RUNTIME_OBSERVATION_QUEUE.json`
18. `04_RUNTIME_EXECUTION_EVIDENCE.json`
19. `04_CONTRADICTION_REGISTER.md`
20. `05_HISTORY_LEDGER.md`

Do **not** resume from ChatGPT memory or chat summaries as authoritative state.

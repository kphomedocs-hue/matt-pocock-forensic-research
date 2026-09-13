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

Phases 1–3 are complete. The project is **not VERIFIED**: Phase 4 behavior/enforcement, remaining history lineage, contradiction resolution, runtime observation, second pass, and red-team verification remain before Phase 10 synthesis.

## Foundation state

Latest foundation report is GREEN:

- **164/164** census rows;
- **164/164** durable per-file notes;
- **164/164 CONNECTIONS TRACED**;
- direct frozen-commit metadata on all notes;
- exact blob-SHA reconciliation;
- **0 hard integrity errors**;
- **0 warnings**;
- current contradiction register recognized through **CT-018** plus CT-H01…CT-H03;
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
- `04_CONTRADICTION_REGISTER.md`
- `scripts/validate_behavior_matrix.py`
- `.github/workflows/validate-phase4-behavior.yml`

Current validated state:

- behavior rows: **38**;
- hard integrity errors: **0**;
- runtime observed: **0/38**;
- current CT coverage: **18/18**;
- uncovered current CT IDs: **0**.

State counts:

- `CONFIRMED_DRIFT`: **5**
- `CONFIRMED_GAP`: **9**
- `CONFIRMED_MATCH`: **8**
- `CONFIRMED_WEAKNESS`: **2**
- `RUNTIME_UNKNOWN`: **6**
- `STATICALLY_ENFORCED`: **8**

Machine-enforcement counts:

- `True`: **8**
- `PARTIAL`: **2**
- `False`: **28**

Latest strengthened validator proof: GitHub Actions run `34744189799` — **SUCCESS**. The validator now fails closed if any current CT is not represented by a behavior row.

### Current contradiction/enforcement register

The register contains **18 current IDs** plus **3 historical IDs**.

Recent findings:

- **CT-014 — implement-spec post-review fix closure:** repair changes after the only required `/code-review` are not required to be revalidated before PR readiness.
- **CT-015 — to-spec parent routing:** parent specs use the same `ready-for-agent` surface as executable tickets; human docs explicitly warn AFK dispatchers can pick the wrong unit.
- **CT-016 — to-tickets acceptance criteria:** ticket criteria have no operative red-at-base/falsifiability requirement.
- **CT-017 — implement ticket lifecycle/frontier:** `/implement` does not close/reconcile its ticket, so dependency-frontier progression can require manual tracker repair.
- **CT-018 — triage agent-brief invariant:** the normal `ready-for-agent` path requires an authoritative Agent Brief, but quick state override can apply the state and leave the brief optional.

Additional durable behavior coverage includes setup confirmation/verification and label materialization, diagnosing-bugs red-loop gating, triage normal-path verification, implement-spec frontier scheduling, domain-modeling discipline, release wiring, to-tickets approval, research provenance, prototype branch isolation, and codebase-design vocabulary discipline.

No Phase 4 row is treated as sufficient for `VERIFIED` by itself.

## Tooling state

Latest closed incident ledger remains:

- failed runs: **82**;
- cancelled runs: **7**;
- total incidents: **89**;
- classified: **89/89**;
- unknown: **0**;
- unresolved/review-required: **0**;
- evidence-corruption incidents found: **0**.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic IDs/provenance and durable ledger rows. |
| 2. Full Physical Read | **COMPLETE** | 164/164 physical blobs inspected; UNREAD = 0. |
| 3. Connection Mapping | **COMPLETE** | **164/164 CONNECTIONS TRACED**; 554-edge v5 graph; quality errors/review items/improvements = 0. |
| 4. Behavior & Enforcement | **IN PROGRESS — PRIMARY FOCUS** | Validated **38-row** matrix; **18/18 current CTs covered**; runtime observed **0/38**. |
| 5. History | IN PROGRESS | 9 durable H-events; partial lineage remains explicitly partial. |
| 6. Contradictions & Orphans | IN PROGRESS | **18 current + 3 historical CT IDs**; Phase 3 orphan questions closed. |
| 7. Runtime & Distribution | IN PROGRESS | Static topology reconstructed; deeper runtime/end-to-end observation remains. |
| 8. Second Pass | NOT STARTED formally | High-impact second-pass gate not yet executed systematically. |
| 9. Red-Team Verification | NOT STARTED formally | No complete systematic falsification pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Final synthesis waits for verification gates. |

## Immediate next execution steps — Phase 4

1. Continue remaining engineering/productivity workflow coverage without duplicating already-adjudicated contracts.
2. Build targeted runtime-test plans for the six `RUNTIME_UNKNOWN` rows.
3. Trace history for CT-014…CT-018 and remaining partial H-events before any verification promotion.
4. Continue separating prompt-level policy from executable/CI guarantees and runtime observations.
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
16. `04_CONTRADICTION_REGISTER.md`
17. `05_HISTORY_LEDGER.md`

Do **not** resume from ChatGPT memory or chat summaries as authoritative state.

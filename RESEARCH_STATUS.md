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

Phases 1–3 are complete. The project is **not VERIFIED**: Phase 4 runtime/enforcement depth, remaining contradiction-specific history lineage, contradiction resolution, runtime/distribution observation, second pass, and red-team verification remain before Phase 10 synthesis.

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
- runtime observed: **8/65**;
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

- `EXECUTION_OBSERVATION`: **30 total / 8 observed / 22 pending**
- `EXTERNAL_DEPENDENCY_VALIDATION`: **7 / 0 / 7**
- `MACHINE_CONSUMER_VALIDATION`: **4 / 0 / 4**
- `PROMPT_REDTEAM_LATER`: **24 / 0 / 24**
- total pending: **57**.

The deterministic local-runtime harness now directly observes **B-004, B-015, B-018, and B-056** against the exact frozen source commit. The latest accepted workflow run is **34752990655** and all acceptance checks passed. B-004 reproduced the frozen `package.json`/`package-lock.json` version drift, demonstrated that `npm pack --dry-run` takes version `1.2.3` from `package.json`, and demonstrated that offline `npm install --package-lock-only` normalizes both root lockfile version fields to `1.2.3`. The remaining release/CI path is still separate under B-029. The other local observations cover wizard-template first-run/rerun behavior, plugin-version drift detection/repair, and HITL capture behavior. No real credentials are used and none of these observations are generalized into prompt/harness verification.

The **37/37 skill** and **71/71 high-risk non-SKILL** results are breadth denominators only. They prove that no current operative skill or behavior-relevant high-risk non-SKILL surface is completely absent from the Phase 4 matrix. They do **not** prove that every behavior is exhausted, that machine-readable policy is honored at runtime, or that any file is VERIFIED.

### Current contradiction/enforcement register

The register contains **20 current IDs** plus **3 historical IDs**.

Newest source/audit findings:

- **CT-019 — audit false-positive correction:** exact frozen-command reproduction showed that `grep -r " as [A-Z]"` does find the advertised `as unknown as Type` form because the later ` as Type` substring matches. CT-019 is retained as a **RESOLVED audit correction**, not a source defect.
- **CT-020 — scaffold-exercises variant/linter contract:** prose permits a solution-only exercise while the same source's linter summary requires a primary variant from problem/explainer/explainer.1, excluding solution-only. This remains OPEN. Its introduction lineage is **RECONCILED** as H-010: the mismatch was present in the file's sole path-history commit and the creation blob is identical to the frozen blob.

Earlier Phase 4 findings CT-014…CT-018 remain durable in the contradiction register and behavior matrix.

No Phase 4 row is treated as sufficient for `VERIFIED` by itself.

## Phase 5 — History

All ten currently registered high-impact H-events are now `RECONCILED`; no H-entry remains `PARTIAL`.

Recent closures:

- **H-003 — Claude plugin promoted-set lineage:** reconciled from the original 21-skill native-plugin manifest through the exact member mutations to the frozen 25-skill manifest.
- **H-004 — Codex metadata lineage:** reconciled the exact owner-count evolution from the initial 39 `agents/openai.yaml` files to the frozen 37/37 owner set: `39 + to-questionnaire + wait-what - six deprecated/personal + implement-spec + retro = 37`. The count-neutral `writing-great-skills` → `writing-for-agents` move is separated from membership changes. The `wizard` model-invocation change and the later `writing-for-agents` stale-Codex-policy regression/fix are also traced explicitly.
- **H-009 — local-linking policy:** reconciled PR #1025’s exact reason and change from every non-deprecated skill to the frozen engineering + productivity + in-progress 33-skill local-link set, while deliberately excluding misc.
- **H-010 — CT-020 introduction:** reconciled the scaffold-exercises mismatch to its sole path-history commit.

Phase 5 remains IN PROGRESS because remaining high-impact current contradictions still require introduction/fix/recurrence lineage where materially relevant; closing the registered H-events is not the same as proving every open defect’s history is exhausted.

## Tooling state

Latest **published closed** incident ledger still records:

- failed runs: **83**;
- cancelled runs: **7**;
- total incidents: **90**;
- classified: **90/90**;
- unknown: **0**;
- unresolved/review-required: **0**;
- evidence-corruption incidents found: **0**.

Two post-ledger workflow events are not yet folded into that published 90-incident snapshot, so tooling closure is **temporarily awaiting refresh** rather than being claimed current:

- run **34752972889**: all four frozen-source runtime checks and every Phase 4 validator passed; the run failed only because the older queued acceptance step still asserted the previous three-ID evidence list. A narrow classifier entrypoint now adjudicates this exact run as `PHASE4_RUNTIME_ACCEPTANCE_SCHEMA_TRANSITION / NO_RESEARCH_DATA_CHANGE_FIXED`. The corrected run **34752990655** passed and published the validated state.
- classifier refresh run **34753536022** was cancelled before execution while a newer workflow-triggered classifier refresh occupied the serialized classifier lane. Classifier cancellations are already modeled as superseded refreshes; the newer refresh must publish before the closed-ledger counts are advanced.

The tooling classifier uses `scripts/classify_tooling_failures_entrypoint.py` for narrow run-ID adjudications and delegates every other case to the existing historical classifier. Its workflow monitors Phase 4 validation, batch application, prior runtime smoke, and deterministic local runtime checks. Unknown future runtime-workflow failures still fail the closure gate rather than being silently categorized.

Because bot commits cannot be relied upon to retrigger downstream Actions, Phase 4 mutation workflows refresh behavior validation, breadth coverage, runtime/evidence queue, and foundation parity inside the same atomic workflow before publication.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic IDs/provenance and durable ledger rows. |
| 2. Full Physical Read | **COMPLETE** | 164/164 physical blobs inspected; UNREAD = 0. |
| 3. Connection Mapping | **COMPLETE** | **164/164 CONNECTIONS TRACED**; 554-edge v5 graph; quality errors/review items/improvements = 0. |
| 4. Behavior & Enforcement | **IN PROGRESS — PRIMARY FOCUS** | Validated **65-row** matrix; **20/20 current CTs**, **37/37 current skills**, **71/71 high-risk non-SKILL surfaces** represented; evidence queue **65/65 classified**; runtime observed **8/65**. |
| 5. History | IN PROGRESS | **10/10 registered H-events RECONCILED**; remaining work is contradiction-specific lineage expansion where materially relevant. |
| 6. Contradictions & Orphans | IN PROGRESS | **20 current + 3 historical CT IDs**; CT-019 is a resolved audit correction, CT-020 remains open with introduction lineage reconciled. |
| 7. Runtime & Distribution | IN PROGRESS | Static topology reconstructed; deterministic local runtime observation has begun; deeper harness/external/end-to-end observation remains. |
| 8. Second Pass | NOT STARTED formally | High-impact second-pass gate not yet executed systematically. |
| 9. Red-Team Verification | NOT STARTED formally | No complete systematic falsification pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Final synthesis waits for verification gates. |

## Immediate next execution steps — Phase 4

1. Finish the tooling-ledger refresh so the post-ledger Phase 4 acceptance transition and superseded classifier refresh are durably closed at zero unknown/unresolved.
2. Continue the evidence queue: **22 pending EXECUTION_OBSERVATION** rows remain after B-004 joined the local-runtime evidence set.
3. Only promote rows when the evidence exercises the behavior itself. Do not call a prompt-mediated skill runtime-observed merely because an underlying Git/npm/shell operation can be reproduced independently.
4. Keep machine-consumer, external-dependency, and prompt-red-team classes separate; do not promote them using evidence from the wrong layer.
5. Continue contradiction-specific history lineage for materially high-impact open defects even though the current H-001…H-010 register is fully reconciled.
6. Keep `VERIFIED = 0` until applicable Phase 4–9 gates close per file/claim.

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

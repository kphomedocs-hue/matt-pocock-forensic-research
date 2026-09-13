# Research Status

## Project state

**IN PROGRESS**

Source repository: `mattpocock/skills`
Frozen commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
Frozen tree: `6e84c093fda2026396cea9fad6a924a6da0e1452`
Physical denominator: **164 blobs/files**

## Current phase position

Primary phase focus: **Phase 4 — Behavior & Enforcement**.

Phases 1–3 are complete. The project is **not VERIFIED**: Phase 4 behavior/enforcement, remaining history lineage, contradiction resolution, runtime observation, second pass, and red-team verification remain before Phase 10 synthesis.

## Foundation state

The latest foundation report is GREEN:

- **164/164** census rows;
- **164/164** durable notes;
- **164 CONNECTIONS TRACED**;
- direct frozen-commit metadata on all 164 notes;
- exact blob-SHA reconciliation;
- **0 hard integrity errors**;
- **0 warnings**;
- no missing contradiction/history references.

`00_RESEARCH_SCHEMA.md` remains the canonical status/gate definition. Chat history is not authoritative state.

## Phase 3 — completed connection state

Phase 3 now has both semantic and deterministic evidence:

- curated semantic graph: `03_CONNECTION_GRAPH.md`;
- deterministic extraction: `scripts/build_connection_graph.py`;
- machine graph/index: `03_CONNECTION_EDGES.json`, `03_CONNECTION_INDEX.md`;
- semantic unresolved-reference reconciliation: `03_CONNECTION_RECONCILIATION.md`, `03_REFERENCE_DISPOSITIONS.json`;
- semantic zero-incoming/orphan reconciliation: `03_ORPHAN_RECONCILIATION.md`, `03_ORPHAN_DISPOSITIONS.json`;
- ask-matt target matrix: `03_ROUTER_MATRIX.md/.json`;
- distribution symmetry matrix: `03_DISTRIBUTION_MATRIX.md/.json`;
- current-file history bindings: `03_HISTORY_BINDINGS.md/.json`;
- per-file closure gate: `03_PHASE3_CLOSURE_INDEX.md/.json`.

### Connection graph v4

Extraction rules version **4** reads all 164 frozen blobs by exact census blob SHA and produces **530** current edges:

- `CONFIG_BINDING`: **37**
- `DISTRIBUTION_ENTRY`: **25**
- `DOC_LINK`: **104**
- `OPERATIVE_CALL`: **15**
- `PASSIVE_REFERENCE`: **123**
- `SKILL_REFERENCE`: **225**
- `SYMLINK`: **1**

The passive layer includes **104 exact repository-path mentions + 19 globally unique-filename mentions**. The v4 skill-reference layer adds **225** exact `/skill`, `$skill`, or backticked-skill references while stripping external URL bodies before slash-label scanning.

### Raw unresolved references

The extractor still preserves **5** internal-looking raw unresolved references for auditability. They are **5/5 semantically reconciled**:

- three domain-modeling consumer-repo CONTEXT example paths;
- Wayfinder's literal `(link)` template placeholder;
- setup-ts-deep-modules' generated consumer `./src/packages/README.md` target.

Confirmed broken repository links from this queue: **0**. Semantically unresolved from this queue: **0**.

### Invocation-policy join

- current skills joined: **37/37**;
- overall invocation split: **22 USER_INVOKED / 15 MODEL_INVOKED**;
- Claude ↔ Codex policy mismatches: **0**;
- current operative Skill-tool calls: **15**;
- illegal current operative calls to user-invoked targets: **0**.

Historical illegal-cross-call defect CT-H01 is therefore not recurring in the frozen current graph.

### Router join

Against the **25 promoted plugin skills**, ask-matt is expected to route to the other **24**:

- promoted targets covered: **24/24**;
- missing promoted targets: **0**;
- extra non-promoted targets: **0**.

Historical router-completeness defect CT-H02 is not recurring as a target-set omission, although route semantics can still be stale under current contradictions such as CT-009.

### Distribution symmetry

Automated anomalies: **0**.

Dimension counts:

- plugin promoted: **25**
- maintainer local-linked: **33**
- list-skills visible: **37**
- root README visible: **25**
- bucket README visible: **37**
- human docs pages: **25**
- ask-matt targets: **24**
- Codex metadata owners: **37**

The 25/33/37 sets are therefore intentional distribution tiers in the frozen source, not unexplained drift.

### Teach glossary / CT-005

MP-0152 `skills/productivity/teach/GLOSSARY-FORMAT.md` is **not** a source-tree orphan. The exhaustive literal scan found one incoming reference from MP-0051 `docs/productivity/teach.md`, whose text explicitly states that Teach ships the support file but `SKILL.md` no longer links it.

CT-005 remains OPEN as an **operative linkage gap**, not an orphan claim.

### History bindings relevant to Phase 3

`03_HISTORY_BINDINGS` maps all nine durable H-events onto the frozen current tree:

- current files with one or more bindings: **69**;
- current-file bindings: **88**;
- H-001: RECONCILED
- H-002: RECONCILED
- H-003: PARTIAL
- H-004: PARTIAL
- H-005: RECONCILED
- H-006: RECONCILED
- H-007: RECONCILED
- H-008: RECONCILED
- H-009: PARTIAL

H-002 is now exact: `e81f97660af0bebfdbf2e23db6a71f7dfcb9a659` reshaped TDD into a reference-only/pre-agreed-seam form, followed by `80e9dcc6857f16cc08b8e5b190393ee7591517e0`, which explicitly removed the refactor stage and moved refactoring to review.

History binding means an event changed a current file; it does not upgrade PARTIAL lineage to reconciled and does not satisfy Phase 5 by itself.

### Zero-incoming / orphan closure

After structural-role evaluation, five files still required explicit semantic disposition:

- MP-0001 — intentional standalone ADR;
- MP-0021 — intentional standalone out-of-scope policy record;
- MP-0022 — intentional standalone out-of-scope policy record;
- MP-0023 — intentional standalone out-of-scope policy record;
- MP-0058 — standalone maintainer `list-skills.sh` entrypoint.

All five preserve their true zero-incoming graph state. The dispositions close the Phase 3 orphan question without inventing edges or claiming the files are actively consumed.

### Formal Phase 3 closure

`03_PHASE3_CLOSURE_INDEX.json` now reports:

- files: **164**;
- READY_CANDIDATE: **164**;
- blockers: **0**;
- explicit semantic zero-incoming dispositions consumed: **5**.

Formal promotion then passed the separate fail-closed gate. All 164 notes now contain a standardized Phase 3 evidence block and are durably `CONNECTIONS TRACED`. `01_MASTER_FILE_LEDGER.md`, `01_FILE_CENSUS.json`, the closure index, and foundation report were rebuilt and validated atomically around the promoted state.

**CONNECTIONS TRACED: 164 / 164.**

**VERIFIED: 0 / 164.**

## Tooling state

Current durable incident ledger:

- failed Actions runs: **79**;
- cancelled Actions runs: **7**;
- total incident runs: **86**;
- classified: **86/86**;
- unknown: **0**;
- unresolved/review-required: **0**;
- evidence-corruption incidents found: **0**.

The latest added incident is the first Phase 3 promotion run, which failed closed because its provenance parser did not recognize the already-valid legacy `Frozen blob SHA` label. No note changes were committed; the parser was aligned with the foundation validator and later promotion succeeded.

A deeper workflow architecture issue was also corrected: Actions commits made with the workflow's ordinary `GITHUB_TOKEN` cannot be relied upon to trigger downstream workflows. Phase 3 generation is therefore consolidated into `.github/workflows/rebuild-phase3-state.yml`, which rebuilds graph → router → distribution → history bindings → closure in one ordered atomic pipeline. The five superseded partial Phase 3 rebuild workflows were removed. Formal promotion uses its own atomic rebuild of notes + ledger/census + closure + foundation.

Successful proof runs include:

- Phase 3 promotion / atomic status proof: `34739027703` — SUCCESS;
- consolidated Phase 3 generated-state proof: `34739079695` — SUCCESS.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic IDs/provenance and durable ledger rows. |
| 2. Full Physical Read | **COMPLETE** | Full contents of 164/164 physical blobs inspected; UNREAD = 0. |
| 3. Connection Mapping | **COMPLETE** | **164/164 CONNECTIONS TRACED**; 530-edge v4 graph; raw unresolved 5/5 reconciled; router 24/24; distribution anomalies 0; closure blockers 0. |
| 4. Behavior & Enforcement | **IN PROGRESS — PRIMARY FOCUS** | Existing evidence includes multiple current enforcement gaps; systematic documented-vs-operative-vs-machine-enforced matrix now required. |
| 5. History | IN PROGRESS | 9 durable H-events; H-003/H-004/H-009 remain PARTIAL. |
| 6. Contradictions & Orphans | IN PROGRESS | 11 current + 3 historical CT IDs; Phase 3 orphan questions closed, but current contradictions remain for behavior/runtime adjudication. |
| 7. Runtime & Distribution | IN PROGRESS | Static distribution topology is reconstructed; deeper runtime/end-to-end observation remains. |
| 8. Second Pass | NOT STARTED formally | High-impact second-pass gate not yet executed systematically. |
| 9. Red-Team Verification | NOT STARTED formally | No systematic absolute/numerical-claim falsification pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Final synthesis waits for verification gates. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Formal `CONNECTIONS TRACED`: **164**
- Formal `VERIFIED`: **0**
- Foundation hard errors: **0**
- Foundation warnings: **0**
- Phase 3 graph edges: **530**
- `SKILL_REFERENCE` edges: **225**
- `PASSIVE_REFERENCE` edges: **123**
- current `OPERATIVE_CALL` edges: **15**
- invocation policies joined: **37/37**
- invocation-policy mismatches: **0**
- illegal current operative calls: **0**
- raw unresolved internal-looking references: **5**
- semantically reconciled raw unresolved: **5/5**
- Phase 3 closure blockers: **0**
- router promoted coverage: **24/24**
- distribution symmetry anomalies: **0**
- history current-file bindings: **88 across 69 files**
- current SKILL.md files: **37**
- promoted skills: **25**
- local-linked skills: **33**
- list-skills visible skills: **37**
- Codex metadata owners: **37**
- tooling incidents classified: **86/86**
- tooling incidents unknown: **0**
- tooling incidents unresolved/review-required: **0**

## Immediate next execution steps — Phase 4

1. Build a durable **behavior/enforcement matrix** that separates documented claims, operative `SKILL.md` instructions, executable/config enforcement, static verification, runtime dependence, and known contradiction IDs.
2. Start with high-impact current contradiction areas rather than re-reading the entire tree blindly: TDD, implement/code-review, setup, diagnosing-bugs, Teach, Wayfinder, wizard, setup-ts-deep-modules, distribution/release scripts.
3. Adjudicate the setup-ts-deep-modules **“Four rules” vs five error-level config rules** question as either genuine source contradiction or defensible grouping, with exact source evidence.
4. Adjudicate the Wayfinder `Notes` execution-override concern: determine whether planning-only behavior is actually enforceable or self-overridable by the same agent.
5. For every behavior claim, record enforcement class such as `PROSE_ONLY`, `PROMPT_GATED`, `STATIC_CONFIG`, `EXECUTABLE_CHECK`, `RUNTIME_DEPENDENT`, or `NOT_ENFORCED` rather than saying simply “works.”
6. Continue Phase 5 separately for H-003/H-004/H-009 and current contradiction lineages.
7. Keep `VERIFIED = 0` until applicable Phase 4–9 gates are satisfied per file/claim.

## Resume instruction

Future sessions must load this GitHub repository first, beginning with `00_RESEARCH_MANIFEST.md`, `00_RESEARCH_SCHEMA.md`, and this status file. Do not use ChatGPT memory or chat summaries as authoritative audit state.

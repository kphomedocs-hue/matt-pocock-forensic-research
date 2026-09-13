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

## Phase 3 — COMPLETE

Phase 3 has both semantic and deterministic evidence:

- curated semantic graph: `03_CONNECTION_GRAPH.md`;
- deterministic extraction: `scripts/build_connection_graph.py`;
- machine graph/index: `03_CONNECTION_EDGES.json`, `03_CONNECTION_INDEX.md`;
- unresolved-reference reconciliation: `03_CONNECTION_RECONCILIATION.md`, `03_REFERENCE_DISPOSITIONS.json`;
- zero-incoming/orphan reconciliation: `03_ORPHAN_RECONCILIATION.md`, `03_ORPHAN_DISPOSITIONS.json`;
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

The passive layer includes **104 exact repository-path mentions + 19 globally unique-filename mentions**. The skill-reference layer adds **225** exact `/skill`, `$skill`, or backticked-skill references while stripping external URL bodies before slash-label scanning.

The five raw unresolved internal-looking references are **5/5 semantically reconciled**, with **0** confirmed broken repository links and **0** semantically unresolved cases.

Invocation-policy join:
- **37/37** current skills joined;
- **22 USER_INVOKED / 15 MODEL_INVOKED** overall;
- **0** Claude↔Codex policy mismatches;
- **15** current operative Skill-tool calls;
- **0** illegal operative calls to user-invoked targets.

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
- root README visible: **25**;
- bucket README visible: **37**;
- human docs pages: **25**;
- ask-matt targets: **24**;
- Codex metadata owners: **37**;
- automated anomalies: **0**.

History bindings map nine durable H-events onto **69** current files with **88** current-file bindings. H-001/H-002/H-005/H-006/H-007/H-008 are RECONCILED; H-003/H-004/H-009 remain PARTIAL.

Five true zero-incoming files required semantic disposition and are durably classified as intentional standalone ADR/policy/maintainer entrypoint roles without fabricating incoming edges.

Formal Phase 3 closure:
- files: **164**;
- READY_CANDIDATE: **164**;
- blockers: **0**;
- explicit semantic zero-incoming dispositions consumed: **5**;
- formal `CONNECTIONS TRACED`: **164/164**;
- formal `VERIFIED`: **0/164**.

## Phase 4 — Behavior & Enforcement

Phase 4 now has a structured working evidence layer:

- structured source: `04_BEHAVIOR_MATRIX.json`;
- rendered view: `04_BEHAVIOR_MATRIX.md`;
- integrity result: `04_BEHAVIOR_INTEGRITY.json`;
- validator: `scripts/validate_behavior_matrix.py`;
- CI gate: `.github/workflows/validate-phase4-behavior.yml`.

The first validated matrix contains **20 behavior rows** with **0 hard integrity errors**. Current state counts:

- `CONFIRMED_DRIFT`: **5**
- `CONFIRMED_GAP`: **4**
- `CONFIRMED_WEAKNESS`: **1**
- `RUNTIME_UNKNOWN`: **3**
- `STATICALLY_ENFORCED`: **7**

Enforcement-layer coverage currently includes documentation, prompt, static config, executable scripts, CI, runtime dependencies, external dependencies, and explicitly absent enforcement. **Runtime observed: 0/20**, intentionally preventing static analysis from being overstated as end-to-end proof.

### New Phase 4 adjudication — CT-012

`setup-ts-deep-modules/SKILL.md` says **“Four rules, all error”**, describes intra-package freedom as a package's own files importing one another freely, says existing configs should merge “the four rules,” and says the config step is done when “the four forbidden rules are present.”

The shipped `dependency-cruiser.config.cjs` contains **five** separate `forbidden` rules with `severity: "error"`. The fifth, `tests-folder-is-private`, blocks any non-test importer from a package's `tests/` folder, including same-package implementation files. This is therefore not merely a harmless split of one conceptual rule: it adds a separately named enforcement rule and an exception to the prose's unconditional intra-package-freedom claim.

CT-012 is OPEN as `OPERATIVE / CONFIG CONTRACT MISMATCH`.

### New Phase 4 adjudication — CT-013

Wayfinder says planning is the default and absent an override it should produce decisions, not deliverables. It explicitly allows an effort to override that default in map `Notes`, carrying execution into the map. The same charting workflow instructs the agent to create the map with `Destination and Notes filled in`, but contains no independent rule requiring an execution-carrying Notes override to be supplied or confirmed by the human.

This is not a direct contradiction because the override is documented. It is an enforcement-authority weakness: the same agent subject to the planning guard can author the field that relaxes it.

CT-013 is OPEN as `PROMPT ENFORCEMENT WEAKNESS / SELF-AUTHORED OVERRIDE`.

### Initial non-defect enforcement rows

The Phase 4 matrix also records strong or partial controls so the audit does not become defect-only. Initial examples include:

- setup-ts-deep-modules' required pass → deliberate fail → revert → pass boundary proof;
- wizard's `bash -n` / shellcheck static verification, distinguished from end-to-end execution;
- git-guardrails' executable exit-2 blocking, classified as heuristic regex enforcement rather than semantic shell parsing;
- setup-pre-commit's real-commit hook smoke test requirement;
- plugin version synchronization through `sync-plugin-version.mjs` and the release path;
- local-link and list-skills executable selection semantics.

These rows remain below VERIFIED until later applicable runtime/history/red-team gates are satisfied.

## Tooling state

Current durable incident ledger:

- failed Actions runs: **79**;
- cancelled Actions runs: **7**;
- total incident runs: **86**;
- classified: **86/86**;
- unknown: **0**;
- unresolved/review-required: **0**;
- evidence-corruption incidents found: **0**.

Phase 3 generation is consolidated into `.github/workflows/rebuild-phase3-state.yml`, which rebuilds graph → router → distribution → history bindings → closure in one ordered atomic pipeline. Formal promotion uses its own atomic rebuild of notes + ledger/census + closure + foundation. This avoids relying on ordinary `GITHUB_TOKEN` workflow commits to retrigger downstream workflows.

Successful proof runs include:
- Phase 3 promotion / atomic status proof: `34739027703` — SUCCESS;
- consolidated Phase 3 generated-state proof: `34739079695` — SUCCESS;
- initial Phase 4 behavior-matrix validation: `34739624908` — SUCCESS.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic IDs/provenance and durable ledger rows. |
| 2. Full Physical Read | **COMPLETE** | Full contents of 164/164 physical blobs inspected; UNREAD = 0. |
| 3. Connection Mapping | **COMPLETE** | **164/164 CONNECTIONS TRACED**; 530-edge v4 graph; raw unresolved 5/5 reconciled; router 24/24; distribution anomalies 0; closure blockers 0. |
| 4. Behavior & Enforcement | **IN PROGRESS — PRIMARY FOCUS** | Validated 20-row behavior matrix; 13 current contradiction/enforcement IDs represented; systematic coverage is expanding. Runtime observed remains 0. |
| 5. History | IN PROGRESS | 9 durable H-events; H-003/H-004/H-009 remain PARTIAL. |
| 6. Contradictions & Orphans | IN PROGRESS | **13 current + 3 historical CT IDs**; Phase 3 orphan questions closed; behavior/runtime contradictions remain. |
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
- Phase 4 behavior rows: **20**
- Phase 4 behavior-matrix hard errors: **0**
- Phase 4 runtime-observed rows: **0/20**
- current contradiction/enforcement IDs: **13**
- historical contradiction IDs: **3**
- tooling incidents classified: **86/86**
- tooling incidents unknown: **0**
- tooling incidents unresolved/review-required: **0**

## Immediate next execution steps — Phase 4

1. Expand the matrix beyond current contradictions into the remaining high-impact behavioral contracts: setup, implement-spec, triage/Wayfinder ticket state transitions, diagnosing-bugs HITL loop, domain-modeling writes, and release/distribution enforcement.
2. For each row, distinguish `DOCUMENTATION`, `PROMPT`, `STATIC_CONFIG`, `EXECUTABLE_SCRIPT`, `CI`, `RUNTIME`, `EXTERNAL_DEPENDENCY`, or `NONE` rather than saying simply “works.”
3. Identify where completion criteria are actually executable/fail-closed versus merely prose requests.
4. Create targeted runtime-test plans only for rows whose truth cannot be resolved statically; do not manufacture runtime evidence by inference.
5. Continue Phase 5 separately for H-003/H-004/H-009 and current contradiction lineages.
6. Keep `VERIFIED = 0` until applicable Phase 4–9 gates are satisfied per file/claim.

## Resume instruction

Future sessions must load this GitHub repository first, beginning with `00_RESEARCH_MANIFEST.md`, `00_RESEARCH_SCHEMA.md`, and this status file. Do not use ChatGPT memory or chat summaries as authoritative audit state.

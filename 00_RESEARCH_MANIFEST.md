# Research Manifest

## Project

Forensic analysis of `mattpocock/skills`.

Frozen commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
Frozen tree: `6e84c093fda2026396cea9fad6a924a6da0e1452`
Physical blob/file denominator: **164**

## Durable-storage authority

The authoritative project state lives in this GitHub repository: `kphomedocs-hue/matt-pocock-forensic-research`.

`00_STORAGE_INTEGRITY_AUDIT.md` records the current durability audit and storage controls.

ChatGPT conversation history, model memory, summaries, scratchpads, hidden reasoning, and transient tool output are **not authoritative storage**. No project phase may depend on information that exists only there.

## Non-negotiable hard rule

Every physical file in the frozen repository must be accounted for, every relevant line read, every meaningful internal connection traced, and every major behavioral claim reconciled against implementation/config/distribution/history where applicable.

No percentage, subsystem-complete claim, or VERIFIED status may be inferred from conversational memory.

## Evidence classes

- SOURCE FACT
- STRUCTURAL INFERENCE
- KP INTERPRETATION
- KP RECOMMENDATION

Never mix these classes.

## File status pipeline

- UNREAD: full contents not fetched/inspected.
- READ: full contents inspected.
- CONNECTIONS TRACED: meaningful outgoing/incoming/config/distribution/invocation/orphan relationships reconciled under the canonical Phase 3 gate.
- VERIFIED: current file + connected implementation/config/distribution + relevant behavior/history/contradictions/runtime/second-pass/red-team evidence reconciled as applicable.

Status transitions require durable evidence and must satisfy `00_RESEARCH_SCHEMA.md`.

Current formal file state: **164/164 CONNECTIONS TRACED; 0 VERIFIED**.

## Verification dimensions

Track separately where relevant:

- PRESENT
- WIRED
- STATICALLY VERIFIED
- TESTED
- RUNTIME OBSERVED
- END-TO-END OBSERVED

Do not collapse these into a single vague `works` state.

## Phases and gates

### Phase 1 — Census & Ledger
Gate: all 164 blobs receive an MP-ID, path, SHA, mode/type, size/category and conservative status.

### Phase 2 — Full Physical Read
Gate: UNREAD = 0. Large files must be read in complete fixed/ranged windows if connector output truncates.

### Phase 3 — Connection Mapping
Gate: operative calls, passive/path/skill-label references, docs links, distribution entries, config bindings, support ownership, history bindings and symlinks are mapped; unresolved/generated targets are explicitly reconciled; zero-incoming/orphan claims use exhaustive evidence or explicit semantic dispositions; per-file gate evidence is durable; second-order quality checks and build provenance pass.

**Current state: COMPLETE — 164/164 CONNECTIONS TRACED.**

### Phase 4 — Behavior & Enforcement
Gate: documented behavior vs operative prompt/config/script/CI behavior reconciled; machine-checkable vs prose-only rules identified; runtime dependence remains explicitly separate from static adjudication.

Working authority:
- `04_BEHAVIOR_MATRIX.json` — structured Phase 4 behavior claims/adjudications;
- `04_BEHAVIOR_MATRIX.md` — deterministic human-readable view;
- `04_BEHAVIOR_INTEGRITY.json` — cross-reference/schema integrity result;
- `scripts/validate_behavior_matrix.py` + `.github/workflows/validate-phase4-behavior.yml` — fail-closed validator/render path.

### Phase 5 — History
Gate: high-impact files/subsystems have creation, major semantic changes, regressions, fixes and current-state provenance traced.

### Phase 6 — Contradictions & Orphans
Gate: stale docs, dead references, orphan files, duplicated sources, naming drift and unresolved defects registered and classified.

### Phase 7 — Runtime & Distribution Paths
Gate: Claude plugin, Codex metadata, local linking, installer/release/versioning and harness-specific behavior reconstructed separately.

### Phase 8 — Second Pass
Gate: all high-impact files reread after graph/history context is known.

### Phase 9 — Red-Team Verification
Gate: counterexamples actively searched for all `all / never / always / exactly` claims and every numerical claim.

### Phase 10 — System Reconstruction & KP Comparison
Gate: only after source-audit gates are satisfied; synthesize architecture/workflows and then derive KP interpretations/recommendations.

## Phase 3 generated-state authority

Phase 3 automated state is rebuilt in dependency order by `.github/workflows/rebuild-phase3-state.yml`:

1. `scripts/build_connection_graph.py`
2. `scripts/build_router_matrix.py`
3. `scripts/build_distribution_matrix.py`
4. `scripts/build_history_bindings.py`
5. `scripts/build_phase3_closure_index.py`
6. `scripts/enrich_master_ledger_connections.py`
7. `scripts/build_phase3_manifest.py`
8. `scripts/verify_phase3_manifest.py`
9. `scripts/validate_phase3_quality.py`

The workflow validates the complete generated set and commits it atomically. Do not rely on chained workflow commits to trigger downstream rebuilds.

Authoritative Phase 3 machine artifacts include:

- `03_CONNECTION_EDGES.json`
- `03_ROUTER_MATRIX.json`
- `03_DISTRIBUTION_MATRIX.json`
- `03_HISTORY_BINDINGS.json`
- `03_PHASE3_CLOSURE_INDEX.json`
- `03_PHASE3_QUALITY.json`
- `03_PHASE3_BUILD_MANIFEST.json`

Formal status promotion is separate: `scripts/promote_phase3_connections.py` plus `.github/workflows/promote-phase3-connections.yml` fail closed and atomically rebuild ledger/census/closure/foundation around the promoted note state.

## Tooling-integrity rule

Research automation is part of the audit surface. A green workflow alone is not authoritative proof. Generated state must retain explicit source provenance and invariants, and tooling incidents must remain durably classified.

Current controls include:

- `00_FOUNDATION_INTEGRITY.md` / `.json` for frozen-source and durable-note invariants;
- `00_TOOLING_INTEGRITY_AUDIT.md` for automation defect analysis and fixes;
- `00_TOOLING_FAILURE_LEDGER.md` / `.json` for failed and cancelled workflow incidents;
- `03_PHASE3_BUILD_MANIFEST.md` / `.json` for SHA-256 build provenance;
- `03_PHASE3_QUALITY.md` / `.json` for second-order Phase 3 quality checks;
- workflow-specific concurrency lanes;
- no implicit dependence on `GITHUB_TOKEN` workflow-commit chaining;
- ordered atomic rebuilding for dependent Phase 3 artifacts;
- fail-closed Phase 4 behavior-matrix cross-reference validation;
- fetch/rebase/push retry for independent cross-workflow write races;
- zero-unknown and zero-review-required closure gates for the tooling incident ledger.

## Resume rule

At the start of every new session or after major context compression, reload from this GitHub repository first. Minimum authoritative resume set:

1. `00_RESEARCH_MANIFEST.md`
2. `00_RESEARCH_SCHEMA.md`
3. `00_STORAGE_INTEGRITY_AUDIT.md`
4. `RESEARCH_STATUS.md`
5. `00_FOUNDATION_INTEGRITY.md`
6. `00_TOOLING_INTEGRITY_AUDIT.md`
7. `00_TOOLING_FAILURE_LEDGER.json`
8. `01_MASTER_FILE_LEDGER.md`
9. `01_FILE_CENSUS.json`
10. `03_CLAIM_REGISTER.md`
11. `03_CONNECTION_GRAPH.md`
12. `03_CONNECTION_EDGES.json`
13. `03_CONNECTION_RECONCILIATION.md`
14. `03_REFERENCE_DISPOSITIONS.json`
15. `03_ORPHAN_RECONCILIATION.md`
16. `03_ROUTER_MATRIX.json`
17. `03_DISTRIBUTION_MATRIX.json`
18. `03_HISTORY_BINDINGS.json`
19. `03_PHASE3_CLOSURE_INDEX.json`
20. `03_PHASE3_QUALITY.json`
21. `03_PHASE3_BUILD_MANIFEST.json`
22. `04_BEHAVIOR_MATRIX.json`
23. `04_BEHAVIOR_INTEGRITY.json`
24. `04_CONTRADICTION_REGISTER.md`
25. `05_HISTORY_LEDGER.md`

When exact numerical/per-edge Phase 3 state matters, load the generated JSON artifacts rather than relying on prose summaries. When exact Phase 4 row state matters, load `04_BEHAVIOR_MATRIX.json` as the structured source.

Never resume from chat memory alone.

## Source-state rule

Frozen-state evidence must be fetched explicitly at commit `3cca18b368ae95cdbdebbff572ccafa662551015` or via its tree/blob SHA. Default-branch searches are discovery only unless explicitly tagged as later/current evidence.

## Truncation rule

Successful retrieval does not mean complete retrieval. Any truncated response remains incomplete until all omitted ranges are inspected.

## History rule

Issues/PRs are evidence reports, not automatic truth. Classify issue evidence as REPORTED / REPRODUCED / FIXED / WONTFIX / UNCONFIRMED.

## ChatGPT limitation control

ChatGPT conversation/context is not authoritative storage. Summaries are secondary sources. Durable facts, statuses, contradictions, claims, graph changes, tooling incidents, phase progress, and verification results must be committed here.

If useful analysis appears in chat but has not yet been committed, it is **NOT DURABLE** and must not be relied upon after the session.

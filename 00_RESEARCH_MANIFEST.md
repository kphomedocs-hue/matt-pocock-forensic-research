# Research Manifest

## Project

Forensic analysis of `mattpocock/skills`.

Frozen commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
Frozen tree: `6e84c093fda2026396cea9fad6a924a6da0e1452`
Physical blob/file denominator: **164**

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
Gate: operative calls, passive/path/skill-label references, docs links, distribution entries, config bindings, history bindings and symlinks are mapped; unresolved/generated targets are explicitly reconciled; zero-incoming/orphan claims use exhaustive evidence or explicit semantic dispositions; per-file gate evidence is durable.

**Current state: COMPLETE — 164/164 CONNECTIONS TRACED.**

### Phase 4 — Behavior & Enforcement
Gate: documented behavior vs operative prompt/config/script/CI behavior reconciled; machine-checkable vs prose-only rules identified.

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

The workflow validates the complete set and commits it atomically. Do not rely on chained workflow commits to trigger downstream rebuilds.

Formal status promotion is separate: `scripts/promote_phase3_connections.py` plus `.github/workflows/promote-phase3-connections.yml` fail closed and atomically rebuild ledger/census/closure/foundation around the promoted note state.

## Tooling-integrity rule

Research automation is part of the audit surface. A green workflow alone is not authoritative proof. Generated state must retain explicit source provenance and invariants, and tooling incidents must remain durably classified.

Current controls include:

- `00_FOUNDATION_INTEGRITY.md` / `.json` for frozen-source and durable-note invariants;
- `00_TOOLING_INTEGRITY_AUDIT.md` for automation defect analysis and fixes;
- `00_TOOLING_FAILURE_LEDGER.md` / `.json` for failed and cancelled workflow incidents;
- workflow-specific concurrency lanes;
- no implicit dependence on `GITHUB_TOKEN` workflow-commit chaining;
- ordered atomic rebuilding for dependent Phase 3 artifacts;
- fetch/rebase/push retry for independent cross-workflow write races;
- zero-unknown and zero-review-required closure gates for the tooling incident ledger.

## Resume rule

At the start of every new session or after major context compression, reload from this GitHub repository first. Minimum authoritative resume set:

1. `00_RESEARCH_MANIFEST.md`
2. `00_RESEARCH_SCHEMA.md`
3. `RESEARCH_STATUS.md`
4. `00_FOUNDATION_INTEGRITY.md`
5. `00_TOOLING_INTEGRITY_AUDIT.md`
6. `00_TOOLING_FAILURE_LEDGER.md`
7. `01_MASTER_FILE_LEDGER.md`
8. `01_FILE_CENSUS.json`
9. `03_CLAIM_REGISTER.md`
10. `03_CONNECTION_GRAPH.md`
11. `03_CONNECTION_RECONCILIATION.md`
12. `03_REFERENCE_DISPOSITIONS.json`
13. `03_ORPHAN_RECONCILIATION.md`
14. `03_ROUTER_MATRIX.md`
15. `03_DISTRIBUTION_MATRIX.md`
16. `03_HISTORY_BINDINGS.md`
17. `03_PHASE3_CLOSURE_INDEX.md`
18. `04_CONTRADICTION_REGISTER.md`
19. `05_HISTORY_LEDGER.md`

When exact numerical or per-edge Phase 3 state matters, also load `03_CONNECTION_EDGES.json`, `03_ROUTER_MATRIX.json`, `03_DISTRIBUTION_MATRIX.json`, `03_HISTORY_BINDINGS.json`, and `03_PHASE3_CLOSURE_INDEX.json` rather than relying on prose summaries.

Never resume from chat memory alone.

## Source-state rule

Frozen-state evidence must be fetched explicitly at commit `3cca18b368ae95cdbdebbff572ccafa662551015` or via its tree/blob SHA. Default-branch searches are discovery only unless explicitly tagged as later/current evidence.

## Truncation rule

Successful retrieval does not mean complete retrieval. Any truncated response remains incomplete until all omitted ranges are inspected.

## History rule

Issues/PRs are evidence reports, not automatic truth. Classify issue evidence as REPORTED / REPRODUCED / FIXED / WONTFIX / UNCONFIRMED.

## ChatGPT limitation control

ChatGPT conversation/context is not authoritative storage. Summaries are secondary sources. Durable facts, statuses, contradictions, claims and phase progress must be committed here.

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
- CONNECTIONS TRACED: meaningful outgoing/incoming references checked and recorded.
- VERIFIED: current file + connected implementation/config/distribution + relevant history reconciled.

Status transitions require evidence.

## Verification dimensions

Track separately where relevant:

- PRESENT
- WIRED
- STATICALLY VERIFIED
- TESTED
- RUNTIME OBSERVED
- END-TO-END OBSERVED

Do not collapse these into a single vague 'works'.

## Phases and gates

### Phase 1 — Census & Ledger
Gate: all 164 blobs receive an MP-ID, path, SHA, mode/type, size/category and conservative status.

### Phase 2 — Full Physical Read
Gate: UNREAD = 0. Large files must be read in complete fixed/ranged windows if connector output truncates.

### Phase 3 — Connection Mapping
Gate: operative calls, passive references, docs links, distribution entries, config bindings, history references and symlinks are mapped; inbound-reference claims use exhaustive scanning, not ranked search alone.

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
Gate: counterexamples actively searched for all 'all/never/always/exactly' claims and every numerical claim.

### Phase 10 — System Reconstruction & KP Comparison
Gate: only after source audit gates are satisfied; synthesize architecture/workflows and then derive KP interpretations/recommendations.

## Resume rule

At the start of every new session or after major context compression, reload from this GitHub repository first. Minimum resume set:

1. `00_RESEARCH_MANIFEST.md`
2. `01_MASTER_FILE_LEDGER.md`
3. `03_CLAIM_REGISTER.md`
4. `04_CONTRADICTION_REGISTER.md`
5. `05_HISTORY_LEDGER.md`
6. `RESEARCH_STATUS.md`

Never resume from chat memory alone.

## Source-state rule

Frozen-state evidence must be fetched explicitly at commit `3cca18b368ae95cdbdebbff572ccafa662551015` or via its tree/blob SHA. Default-branch searches are discovery only unless explicitly tagged as later/current evidence.

## Truncation rule

Successful retrieval does not mean complete retrieval. Any truncated response remains incomplete until all omitted ranges are inspected.

## History rule

Issues/PRs are evidence reports, not automatic truth. Classify issue evidence as REPORTED / REPRODUCED / FIXED / WONTFIX / UNCONFIRMED.

## ChatGPT limitation control

ChatGPT conversation/context is not authoritative storage. Summaries are secondary sources. Durable facts, statuses, contradictions, claims and phase progress must be committed here.

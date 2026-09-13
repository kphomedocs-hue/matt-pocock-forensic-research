# Storage Integrity Audit

## Purpose

This file records where the authoritative research state for the forensic audit of `mattpocock/skills` is stored.

**Authoritative durable storage:** GitHub repository `kphomedocs-hue/matt-pocock-forensic-research`.

**Non-authoritative/transient storage:** ChatGPT conversation history, model memory, summaries, scratchpads, hidden reasoning, temporary tool output, or any other GPT-local context.

No project phase may depend on information that exists only in GPT/chat context.

## Repository ownership and visibility

- Repository: `kphomedocs-hue/matt-pocock-forensic-research`
- Owner: `kphomedocs-hue`
- Default branch: `main`
- Connected account has admin/maintain/push permissions.
- Repository visibility at the time of this audit: **PUBLIC**.

The repository being public is a GitHub visibility choice, not a storage-integrity defect. If the research should not be publicly readable, change the repository to private in GitHub settings.

## Frozen source identity

- Source repository: `mattpocock/skills`
- Frozen commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
- Frozen tree: `6e84c093fda2026396cea9fad6a924a6da0e1452`
- Physical denominator: **164 blobs/files**

## Durable coverage confirmed

### Project control / resume state

Stored in GitHub:

- `00_RESEARCH_MANIFEST.md`
- `00_RESEARCH_SCHEMA.md`
- `RESEARCH_STATUS.md`
- `00_STORAGE_INTEGRITY_AUDIT.md`

These define the hard rule, gates, current phase state, resume procedure, and the rule that chat memory is not authoritative.

### Phase 1–2 — census and physical evidence

Stored in GitHub:

- `01_FILE_CENSUS.json`
- `01_MASTER_FILE_LEDGER.md`
- `02_FILE_NOTES/MP-0001.md` through `MP-0164.md`
- `00_FOUNDATION_INTEGRITY.md/.json`
- deterministic rebuild/validation tooling under `scripts/` and `.github/workflows/`

Current foundation state proves:

- census rows: **164/164**;
- durable notes: **164/164**;
- formal state: **164 CONNECTIONS TRACED**;
- direct frozen-source provenance on all notes;
- hard integrity errors: **0**;
- warnings: **0**.

Therefore physical-read evidence does not depend on chat history.

### Phase 3 — connection mapping

Stored in GitHub:

- `03_CONNECTION_GRAPH.md`
- `03_CONNECTION_EDGES.json`
- `03_CONNECTION_INDEX.md`
- `03_CONNECTION_RECONCILIATION.md`
- `03_REFERENCE_DISPOSITIONS.json`
- `03_ORPHAN_RECONCILIATION.md`
- `03_ORPHAN_DISPOSITIONS.json`
- `03_ROUTER_MATRIX.md/.json`
- `03_DISTRIBUTION_MATRIX.md/.json`
- `03_HISTORY_BINDINGS.md/.json`
- `03_PHASE3_CLOSURE_INDEX.md/.json`
- `03_PHASE3_QUALITY.md/.json`
- `03_PHASE3_BUILD_MANIFEST.md/.json`

Current machine state:

- extraction rules version: **5**;
- graph edges: **554**;
- stable edge IDs: **554/554**;
- literal source-line provenance: **490/554**;
- `CONFIG_BINDING`: 37;
- `DISTRIBUTION_ENTRY`: 25;
- `DOC_LINK`: 104;
- `OPERATIVE_CALL`: 15;
- `PASSIVE_REFERENCE`: 123;
- `SKILL_REFERENCE`: 223;
- `SUPPORT_BINDING`: 26;
- `SYMLINK`: 1;
- invocation-policy mismatches: **0**;
- illegal operative calls: **0**;
- weak-only orphan proof count: **0**;
- unmapped extra-link-syntax count: **0**;
- support-owner gap count: **0**;
- history H-001…H-009 parity: **all green**;
- master-ledger blank Ref-in/Ref-out rows: **0**;
- Phase 3 quality hard errors/review items/improvements: **0 / 0 / 0**.

The Phase 3 build manifest stores SHA-256 fingerprints for authoritative generator/acceptance inputs and generated outputs. Phase 3 can therefore be reconstructed and checked from GitHub without GPT memory.

### Contradictions and history

Stored in GitHub:

- `04_CONTRADICTION_REGISTER.md`
- `05_HISTORY_LEDGER.md`
- `03_HISTORY_BINDINGS.md/.json`

The current contradiction register contains **CT-001 through CT-014** plus historical **CT-H01 through CT-H03**. CT-014 records the `implement-spec` post-review repair revalidation gap. History definitions are durable and the Phase 3 binding generator derives event definitions from the durable history ledger rather than a duplicate hardcoded table.

### Phase 4 working state

Stored in GitHub:

- `04_BEHAVIOR_MATRIX.json`
- `04_BEHAVIOR_MATRIX.md`
- `04_BEHAVIOR_INTEGRITY.json`
- `04_CONTRADICTION_REGISTER.md`
- `scripts/validate_behavior_matrix.py`
- `.github/workflows/validate-phase4-behavior.yml`

Current validated working state:

- behavior rows: **29**;
- hard integrity errors: **0**;
- runtime observed: **0/29**;
- current contradiction IDs represented: **14/14**;
- latest validator proof: run `34743483922` — **SUCCESS**.

State counts:

- `CONFIRMED_DRIFT`: 5
- `CONFIRMED_GAP`: 5
- `CONFIRMED_MATCH`: 5
- `CONFIRMED_WEAKNESS`: 2
- `RUNTIME_UNKNOWN`: 4
- `STATICALLY_ENFORCED`: 8

The newest durable rows include setup confirmation/verification behavior, diagnosing-bugs' red-loop gate, triage invariants and verification order, implement-spec frontier scheduling and post-review revalidation, domain-modeling write discipline, and release version/tag wiring.

Phase 4 remains intentionally in progress; no row is treated as sufficient to promote a file to VERIFIED.

### Tooling integrity / incident history

Stored in GitHub:

- `00_TOOLING_INTEGRITY_AUDIT.md`
- `00_TOOLING_FAILURE_LEDGER.md/.json`
- `scripts/classify_failed_workflows.py`
- `.github/workflows/classify-tooling-failures.yml`

Current closed incident state:

- failed runs: **82**;
- cancelled runs: **7**;
- total incidents: **89**;
- classified: **89/89**;
- unknown: **0**;
- unresolved/review-required: **0**;
- evidence-corruption incidents found: **0**.

### Reproducibility / automation

GitHub contains the scripts and workflows required to rebuild or validate census/ledger state, Phase 3 graph/router/distribution/history/closure/provenance/quality state, Phase 3 promotion, Phase 4 behavior validation, note normalization, foundation validation, and tooling-incident classification.

## GPT/chat storage rule

ChatGPT may temporarily contain copies, explanations, or summaries of project information as part of a live conversation. This audit does **not** claim that the ChatGPT service stores zero conversational data internally.

The enforceable project rule is:

> **No important or useful project datum may exist only in GPT/chat context.**

For this project:

1. all authoritative facts required to resume work must be committed to GitHub;
2. any new material finding, contradiction, status change, graph change, tooling defect, or verification result must be written to GitHub in the same working session when feasible;
3. chat summaries are secondary conveniences only;
4. a future session must reload GitHub before continuing;
5. no READ / CONNECTIONS TRACED / VERIFIED / phase-complete claim may be promoted from conversational memory;
6. when chat and GitHub disagree, GitHub source/provenance artifacts control and stale human summaries must be repaired;
7. useful analysis produced in chat but not committed is **NOT DURABLE** and must not be relied upon after the session.

## Current storage-integrity conclusion

**PASS, with the visibility caveat that the repository is public.**

At the time of this audit, no known important project state required to resume Phases 1–4 exists only in GPT/chat context. The authoritative census, 164 file notes, Phase 3 graph/closure/quality/provenance evidence, CT-001…CT-014 contradiction evidence, history ledger, 29-row Phase 4 working matrix, tooling incident history, scripts, workflows, and current status are all stored in the user's GitHub repository.

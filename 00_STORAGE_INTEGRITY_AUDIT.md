# Storage Integrity Audit

## Purpose

This file proves where the authoritative research state for the forensic audit of `mattpocock/skills` is stored.

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
- this file, `00_STORAGE_INTEGRITY_AUDIT.md`

These files define the hard rule, gates, current phase state, resume procedure, and the rule that chat memory is not authoritative.

### Phase 1 — census and ledger

Stored in GitHub:

- `01_FILE_CENSUS.json`
- `01_MASTER_FILE_LEDGER.md`
- deterministic rebuild tooling under `scripts/`
- CI/rebuild workflows under `.github/workflows/`

Current foundation report proves **164/164** census rows.

### Phase 2 — full physical read evidence

Stored in GitHub:

- `02_FILE_NOTES/MP-0001.md` through `02_FILE_NOTES/MP-0164.md`
- `00_FOUNDATION_INTEGRITY.md/.json`

Current foundation report proves:

- durable notes: **164/164**;
- formal state: **164 CONNECTIONS TRACED**;
- frozen source provenance present for all notes;
- hard integrity errors: **0**;
- warnings: **0**.

Therefore the full physical-read evidence does not depend on chat history.

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

Current machine state at this audit:

- extraction rules version: **5**;
- graph edges: **554**;
- stable edge IDs: **554/554**;
- literal source-line provenance edges: **490/554**;
- `CONFIG_BINDING`: 37;
- `DISTRIBUTION_ENTRY`: 25;
- `DOC_LINK`: 104;
- `OPERATIVE_CALL`: 15;
- `PASSIVE_REFERENCE`: 123;
- `SKILL_REFERENCE`: 223;
- `SUPPORT_BINDING`: 26;
- `SYMLINK`: 1;
- invocation-policy mismatches: **0**;
- illegal operative calls: **0**.

Current second-order Phase 3 quality report proves:

- weak-only orphan proof count: **0**;
- unmapped extra-link-syntax count: **0**;
- support-owner gap count: **0**;
- history H-001…H-009 parity: **all green**;
- master-ledger blank Ref-in/Ref-out rows: **0**;
- hard errors: **0**;
- review items: **0**;
- remaining improvements: **0**.

The Phase 3 build manifest stores SHA-256 fingerprints for the authoritative generator/acceptance inputs and generated outputs.

Therefore Phase 3 can be reconstructed and checked from GitHub without GPT memory.

### Contradictions and history

Stored in GitHub:

- `04_CONTRADICTION_REGISTER.md`
- `05_HISTORY_LEDGER.md`
- `03_HISTORY_BINDINGS.md/.json`

Current contradiction register retains the evidence and resolution tests for CT-001 through CT-013 plus historical CT-H01 through CT-H03. History definitions are durable and no longer duplicated as an independent hardcoded truth inside the Phase 3 history generator.

### Phase 4 working state

Stored in GitHub:

- `04_BEHAVIOR_MATRIX.json`
- `04_BEHAVIOR_MATRIX.md`
- `04_BEHAVIOR_INTEGRITY.json`
- `scripts/validate_behavior_matrix.py`
- `.github/workflows/validate-phase4-behavior.yml`

Current validated working state contains **20 behavior rows**, **0 hard integrity errors**, and **0/20 runtime-observed rows**. Phase 4 is intentionally still in progress.

### Tooling integrity / incident history

Stored in GitHub:

- `00_TOOLING_INTEGRITY_AUDIT.md`
- `00_TOOLING_FAILURE_LEDGER.md`
- `00_TOOLING_FAILURE_LEDGER.json`
- `scripts/classify_failed_workflows.py`
- `.github/workflows/classify-tooling-failures.yml`

Current incident ledger at this audit:

- failed runs: **82**;
- cancelled runs: **7**;
- total incidents: **89**;
- classified: **89/89**;
- unknown: **0**;
- unresolved/review-required: **0**.

Tooling failures and fixes therefore have durable history outside chat.

### Reproducibility / automation

GitHub contains the scripts and workflows required to rebuild or validate the durable state, including census/ledger generation, Phase 3 graph/router/distribution/history/closure generation, Phase 3 build-manifest verification, Phase 3 quality validation, Phase 3 promotion, Phase 4 behavior validation, note normalization, foundation validation, and tooling-incident classification.

## Discrepancy found and corrected during this audit

Before this storage audit, `RESEARCH_STATUS.md` still described the older Phase 3 v4 / 530-edge state while the authoritative machine artifacts already contained the newer v5 state.

This was a **human-summary synchronization defect**, not missing research data. The newer useful data was already stored in GitHub in `03_CONNECTION_EDGES.json`, `03_PHASE3_QUALITY.json`, and `03_PHASE3_BUILD_MANIFEST.json`.

`RESEARCH_STATUS.md` was corrected during this audit to the current v5 / 554-edge state and current tooling incident counts.

## GPT/chat storage rule

ChatGPT may temporarily contain copies, explanations, or summaries of project information as part of a live conversation. This audit does **not** claim that the ChatGPT service stores zero conversational data internally.

The enforceable project rule is stronger and practical:

> **No important or useful project datum may exist only in GPT/chat context.**

For this project:

1. all authoritative facts required to resume work must be committed to GitHub;
2. any new material finding, contradiction, status change, graph change, tooling defect, or verification result must be written to GitHub in the same working session when feasible;
3. chat summaries are secondary conveniences only;
4. a future session must reload GitHub before continuing;
5. no READ / CONNECTIONS TRACED / VERIFIED / phase-complete claim may be promoted from conversational memory;
6. when chat and GitHub disagree, GitHub source/provenance artifacts control and the stale human summary must be repaired;
7. if useful analysis is produced in chat but not yet committed, it is considered **NOT DURABLE** and must not be relied upon after the session.

## Current storage-integrity conclusion

**PASS, with the visibility caveat that the repository is public.**

At the time of this audit, no known important project state required to resume Phases 1–4 exists only in GPT/chat context. The authoritative census, 164 file notes, connection graph, closure/quality/provenance evidence, contradictions, history ledger, current Phase 4 working matrix, tooling incident history, scripts, workflows, and current status are all stored in the user's GitHub repository.

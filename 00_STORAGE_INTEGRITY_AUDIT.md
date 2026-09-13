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
- Repository visibility at this audit: **PUBLIC**.

## Frozen source identity

- Source repository: `mattpocock/skills`
- Frozen commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
- Frozen tree: `6e84c093fda2026396cea9fad6a924a6da0e1452`
- Physical denominator: **164 blobs/files**

## Durable coverage confirmed

### Control and resume state

Stored in GitHub: `00_RESEARCH_MANIFEST.md`, `00_RESEARCH_SCHEMA.md`, `RESEARCH_STATUS.md`, and this file. These define the hard rule, gates, current phase state, resume procedure, and the rule that chat memory is not authoritative.

### Phase 1–2

GitHub stores `01_FILE_CENSUS.json`, `01_MASTER_FILE_LEDGER.md`, all `02_FILE_NOTES/MP-0001.md` through `MP-0164.md`, foundation reports, scripts and workflows.

Current foundation state proves **164/164** census rows, **164/164** durable notes, **164 CONNECTIONS TRACED**, direct frozen-source provenance on all notes, **0 hard errors** and **0 warnings**.

### Phase 3

GitHub stores the graph/index, reference/orphan dispositions, router/distribution/history matrices, closure index, Phase 3 quality report and SHA-256 build manifest.

Current machine state: extraction rules v5, **554 edges**, **554/554** stable edge IDs, **490/554** literal source-line provenance, 0 invocation-policy mismatches, 0 illegal operative calls, 0 weak-only orphan proofs, 0 unmapped extra-link syntax, 0 support-owner gaps, H-001…H-009 parity green, 0 blank master-ledger connection rows, and Phase 3 quality hard errors/review items/improvements = **0/0/0**.

Phase 3 can be reconstructed and checked from GitHub without GPT memory.

### Contradictions and history

GitHub stores `04_CONTRADICTION_REGISTER.md`, `05_HISTORY_LEDGER.md`, and `03_HISTORY_BINDINGS.md/.json`.

The current contradiction register contains **CT-001 through CT-018** plus historical **CT-H01 through CT-H03**. Recent findings include:

- CT-014: implement-spec post-review repair changes lack a mandatory post-fix acceptance pass;
- CT-015: parent spec `ready-for-agent` routing can be consumed as executable AFK work;
- CT-016: to-tickets has no operative falsifiability/red-at-base acceptance-criteria gate;
- CT-017: implement does not publish ticket completion needed for dependency-frontier progression;
- CT-018: triage quick override can apply `ready-for-agent` without the authoritative Agent Brief required by the normal state contract.

History definitions remain durable and machine-linked.

### Phase 4 working state

GitHub stores:

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
- uncovered current CT IDs: **0**;
- strengthened validator proof: run `34744189799` — **SUCCESS**.

State counts: `CONFIRMED_DRIFT` 5, `CONFIRMED_GAP` 9, `CONFIRMED_MATCH` 8, `CONFIRMED_WEAKNESS` 2, `RUNTIME_UNKNOWN` 6, `STATICALLY_ENFORCED` 8.

The Phase 4 validator now fails closed if any current contradiction ID lacks a behavior row. Phase 4 remains in progress and no row alone promotes a file to VERIFIED.

### Tooling integrity / incidents

GitHub stores `00_TOOLING_INTEGRITY_AUDIT.md`, `00_TOOLING_FAILURE_LEDGER.md/.json`, classifier tooling and workflow configuration.

Latest closed incident state remains **89/89 classified**, with **0 unknown**, **0 unresolved/review-required**, and no evidence-corruption incident found.

## GPT/chat storage rule

ChatGPT may temporarily contain copies, explanations, or summaries of project information during a live conversation. This audit does **not** claim that the ChatGPT service stores zero conversational data internally.

The enforceable project rule is:

> **No important or useful project datum may exist only in GPT/chat context.**

1. All authoritative facts needed to resume work must be committed to GitHub.
2. New material findings, contradictions, statuses, tooling defects and verification results must be made durable in GitHub in the same working session when feasible.
3. Chat summaries are secondary conveniences only.
4. Future sessions must reload GitHub before continuing.
5. No READ / CONNECTIONS TRACED / VERIFIED / phase-complete claim may be promoted from conversational memory.
6. When chat and GitHub disagree, committed source/provenance artifacts control and stale human summaries must be repaired.
7. Useful analysis produced only in chat is **NOT DURABLE** and must not be relied upon after the session.

## Current conclusion

**PASS, with the visibility caveat that the repository is public.**

No known important state required to resume Phases 1–4 exists only in GPT/chat context. The census, 164 file notes, Phase 3 graph/closure/quality/provenance evidence, CT-001…CT-018, history, the 38-row Phase 4 matrix, tooling incident history, scripts, workflows, and current status are stored in the user's GitHub repository.

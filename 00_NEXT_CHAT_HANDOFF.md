# Next Chat Handoff — Matt Pocock Skills Forensic Research

## Authority

This repository is the authoritative durable project state:

`kphomedocs-hue/matt-pocock-forensic-research`

Do **not** resume from ChatGPT memory, summaries, or this handoff alone when machine artifacts disagree.

Source repository under study:

`mattpocock/skills`

Frozen source commit:

`3cca18b368ae95cdbdebbff572ccafa662551015`

Frozen source tree:

`6e84c093fda2026396cea9fad6a924a6da0e1452`

All frozen-source claims must be fetched at that exact commit/tree/blob. Default-branch source reads are discovery only unless explicitly treated as later/current evidence.

## Current durable state

- Physical denominator: 164 files/blobs.
- Durable per-file notes: 164/164.
- CONNECTIONS TRACED: 164/164.
- VERIFIED: 0/164.
- Foundation hard errors: 0.
- Foundation warnings: 0.
- Phase 3: COMPLETE.
- Phase 3 graph edges: 554.
- Phase 4 behavior rows: 65.
- Phase 4 runtime observed: 15/65.
- Phase 4 pending stronger evidence: 50.
- Pending EXECUTION_OBSERVATION rows: 16.
- Pending EXTERNAL_DEPENDENCY_VALIDATION rows: 6.
- Pending MACHINE_CONSUMER_VALIDATION rows: 4.
- Pending PROMPT_REDTEAM_LATER rows: 24.
- Current contradiction coverage: 20/20.
- Skill breadth coverage: 37/37.
- High-risk non-SKILL surface coverage: 71/71.
- Phase 4 hard errors: 0.
- Tooling incident ledger: 179 entries from 143 failed + 36 cancelled runs.
- Tooling unknown entries: 0.
- Tooling unresolved/review-required entries: 0.

Important epistemic rules:

- CONNECTIONS TRACED is not VERIFIED.
- Breadth coverage is not runtime verification.
- Runtime-observed behavior rows do not by themselves promote files to VERIFIED.
- VERIFIED remains 0/164 until all applicable later gates close.

## Important work already completed

### Foundation / Phase 3

- 164/164 file census and durable notes completed.
- Exact blob-SHA reconciliation completed.
- 554-edge connection graph completed.
- Invocation policies completed for 37/37 skills.
- Claude↔Codex mismatches: 0.
- Illegal operative calls: 0.
- Weak-only orphan proofs: 0.
- Unmapped extra-link syntax: 0.
- Support-owner gaps: 0.
- Phase 3 generated-state build provenance and quality gates are durable.

### Phase 4 runtime evidence already promoted

Runtime-observed rows include:

- B-004 package/plugin/lock version truth.
- B-012 deep-module public-entrypoint enforcement.
- B-014 deep-module tests-folder privacy enforcement.
- B-015 wizard generated-script verification.
- B-016 git-guardrails dangerous-command blocking.
- B-017 setup-pre-commit functional hook path.
- B-018 plugin version synchronization.
- B-019 local skill linking set.
- B-020 list-skills enumeration.
- B-046 migrate-to-shoehorn assertion discovery / CT-019 correction.
- B-056 diagnosing-bugs HITL capture helper.
- B-008 architecture-report self-containment / external-dependency observation.
- B-010 implement-review pre-commit visibility observation.
- B-047 scaffold-exercises solution-only linter observation (CT-020 remains open).
- B-029 release version/tag workflow execution observation.

### Important contradiction/runtime findings

- CT-019 is RESOLVED as an audit correction: the frozen grep behavior did catch the later ` as Type` substring; B-046 is runtime observed.
- CT-020 remains OPEN: scaffold-exercises prose permits a solution-only exercise, but the pinned external ai-hero-cli v0.2.8 linter rejects that shape in a synthetic fixture while an explainer-only control passes.
- CT-012 remains OPEN: the deep-module skill prose says four rules and allows own-package files to import freely, while the shipped config has five error rules including `tests-folder-is-private`.
- B-017 preserved a real Husky 9.1.7 drift: `.husky/pre-commit` itself is not executable, while the executable `.husky/_/pre-commit` shim runs it through `sh -e`. Functional commit-hook behavior was successfully observed; the stale frozen executable-bit predicate was not hidden with chmod.
- B-008 was republished by successful GitHub Action 34930416829 after its workflow gained retry-on-push-race publication handling. B-010 was durably observed by Action 34929107528. B-047 was durably observed by Action 34930009546; its result records frozen source provenance, the exact external linter commit/version, named tests, and the public course lock evidence.
- B-029 is durably recorded from upstream Release workflow run 33854812658 at the exact frozen source commit. The Version job, including the configured Create Version Pull Request step, succeeded. This establishes execution of the configured route, not confirmed tag publication; the retained job metadata has no action output proving a pending changeset, created PR, or tag.
- The generic GitHub-label fixture for B-024 is retained as supporting-only evidence. It did not create the frozen skill's exact custom canonical state labels, so B-024 remains unobserved and must not be promoted from that fixture.

## Persistence/control repairs completed before this handoff

The GitHub research pipeline was hardened so project state does not depend on chat history or later workflow chaining:

- `RESEARCH_STATUS.md` is generated from machine-readable artifacts by `scripts/build_research_status.py`.
- The Phase 4 main guard fails if committed status is stale.
- Phase 4 producers commit evidence plus `RESEARCH_STATUS.md` atomically in the same GitHub commit.
- Tooling-ledger publication and checkpoint publication are atomic.
- Runtime smoke, local runtime, deep-module, pre-commit, Phase 4 batch, and related producers no longer rely on a second workflow being triggered by a bot commit.
- The tooling classifier preserves a previously closed historical classification when GitHub temporarily cannot return an old log, but genuinely new incidents still fail closed.
- Deep-module and pre-commit result files are part of Phase 4 validation trigger coverage.
- The tooling classifier watches active Phase 4 workflows. Push-triggered and workflow-triggered classifier refreshes use separate concurrency lanes so a successful main-guard completion cannot cancel a required direct reconciliation refresh.
- Current branch protection remains disabled; the main guard detects bad state but is not GitHub administrative prevention.

## Required first reads in the new chat

Before doing any new research, fetch the latest `main` of this repository and inspect at minimum:

1. `00_RESEARCH_MANIFEST.md`
2. `00_RESEARCH_SCHEMA.md`
3. `RESEARCH_STATUS.md`
4. `00_FOUNDATION_INTEGRITY.json`
5. `00_TOOLING_FAILURE_LEDGER.json`
6. `01_FILE_CENSUS.json`
7. `03_CONNECTION_EDGES.json`
8. `03_PHASE3_QUALITY.json`
9. `04_BEHAVIOR_MATRIX.json`
10. `04_BEHAVIOR_INTEGRITY.json`
11. `04_BEHAVIOR_COVERAGE.json`
12. `04_RUNTIME_OBSERVATION_QUEUE.json`
13. `04_CONTRADICTION_REGISTER.md`
14. `05_HISTORY_LEDGER.md`
15. this file, `00_NEXT_CHAT_HANDOFF.md`, as a convenience pointer only.

For exact Phase 4 state, prefer `04_BEHAVIOR_MATRIX.json` and `04_RUNTIME_OBSERVATION_QUEUE.json` over prose summaries.

## Where the new chat should get source files

Do not ask the user to manually upload the 164 source files if GitHub access is available.

Use the GitHub connection directly:

- Research/evidence files: `kphomedocs-hue/matt-pocock-forensic-research` on current `main`.
- Frozen source files under study: `mattpocock/skills` at commit `3cca18b368ae95cdbdebbff572ccafa662551015`.

When testing a behavior, fetch the exact source/config/script files named in that behavior row from the frozen commit. Do not silently substitute the current upstream default branch.

Fallback only if the new chat cannot access GitHub: upload the minimum resume files listed above plus the exact frozen source files needed for the next selected behavior. Do not build a new independent source-of-truth ZIP unless necessary.

## Immediate next execution

1. Re-read current `04_RUNTIME_OBSERVATION_QUEUE.json` from latest `main`.
2. Continue the 16 pending `EXECUTION_OBSERVATION` rows in small deterministic batches. Do not manufacture execution evidence when a supported agent runtime is unavailable; move only to independently runnable evidence classes.
3. Prefer isolated local/synthetic tests with no live-user repository side effects.
4. Keep execution observations separate from machine-consumer, external-dependency, and prompt-red-team evidence classes.
5. For each promoted row, record exact frozen source provenance, package/tool versions where applicable, named tests, workflow run ID, and durable result file.
6. Rebuild/validate behavior matrix, integrity, coverage, runtime queue, foundation, runtime provenance, and research status before promotion.
7. If any harness/workflow run fails or is cancelled, reconcile it into `00_TOOLING_FAILURE_LEDGER.json` before moving to the next behavior.
8. Do not promote any file to VERIFIED merely because a Phase 4 runtime test passed.

## Suggested new-chat opening instruction

"Resume the Matt Pocock skills forensic research from GitHub. Treat `kphomedocs-hue/matt-pocock-forensic-research` current `main` as the durable authority and `mattpocock/skills` commit `3cca18b368ae95cdbdebbff572ccafa662551015` as the frozen source. Read `00_NEXT_CHAT_HANDOFF.md`, `00_RESEARCH_MANIFEST.md`, `RESEARCH_STATUS.md`, and the minimum resume artifacts listed there before doing any work. Then inspect the current runtime observation queue and continue Phase 4 with the next small deterministic EXECUTION_OBSERVATION batch. Do not rely on chat memory, do not advance VERIFIED, and reconcile every failed/cancelled tooling run before proceeding."

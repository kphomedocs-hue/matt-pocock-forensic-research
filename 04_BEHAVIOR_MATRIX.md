# Phase 4 Behavior & Enforcement Matrix

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

Working rows: **29**. Matrix state: **IN_PROGRESS**.

This is a Phase 4 working artifact, not a VERIFIED-status ledger. It separates documented claims, prompt behavior, static/executable enforcement, runtime dependence, and contradiction state.

## Enforcement vocabulary

- `DOCUMENTATION` — secondary/human-facing description only.
- `PROMPT` — operative agent instruction; adherence is not deterministic by itself.
- `STATIC_CONFIG` — declarative machine-readable rule/configuration.
- `EXECUTABLE_SCRIPT` — executable code/check/hook enforces or verifies behavior.
- `CI` — enforcement is wired into an automated repository workflow.
- `RUNTIME` — behavior depends on actual harness/consumer execution.
- `EXTERNAL_DEPENDENCY` — behavior depends on an external service/network/tool.
- `NONE` — claimed guard/behavior has no corresponding operative enforcement found.

## Matrix

| ID | Area | State | Layers | Machine enforced | Runtime observed | CT | Adjudication |
|---|---|---|---|---|---|---|---|
| B-001 | TDD loop semantics | CONFIRMED_DRIFT | PROMPT, DOCUMENTATION, STATIC_CONFIG | False | False | CT-001 | Operative SKILL.md plus changelog agree on red->green; README/bucket/Codex descriptions retain red-green-refactor. Prompt behavior is not machine-enforced. |
| B-002 | ask-matt promoted/invocation counts | CONFIRMED_DRIFT | DOCUMENTATION, STATIC_CONFIG | False | False | CT-002 | Generated frozen distribution truth is 25 promoted with 14 user-invoked/11 model-invoked; ask-matt human docs retain 22/13 wording. |
| B-003 | ask-matt target-source verification | CONFIRMED_GAP | DOCUMENTATION, PROMPT, NONE | False | False | CT-003 | Human docs demand trace evidence of target-source reading; operative ask-matt has no mandatory target-source-read step. The documented verification criterion is not enforced in the operative prompt. |
| B-004 | package/plugin/lock version truth | RUNTIME_UNKNOWN | STATIC_CONFIG, EXECUTABLE_SCRIPT, CI | PARTIAL | False | CT-004 | package.json -> plugin.json synchronization is executable/release-wired, but package-lock root metadata remains 0.0.0 and is outside the sync script. |
| B-005 | Teach glossary format linkage | CONFIRMED_GAP | DOCUMENTATION, PROMPT, NONE | False | False | CT-005 | The support format exists and human docs describe it, but operative Teach does not load/reference it. The file is not a source-tree orphan; the operative linkage is missing. |
| B-006 | Teach workspace-root resolution | RUNTIME_UNKNOWN | PROMPT, RUNTIME | False | False | CT-006 | Frozen source mixes co-located support references and relative workspace paths; reported issue evidence exists, but source inspection alone cannot settle harness working-directory resolution. |
| B-007 | diagnosing-bugs redaction | CONFIRMED_DRIFT | PROMPT, DOCUMENTATION | False | False | CT-007 | Operative skill and changelog contain shipped redaction instructions while human docs still call the behavior unimplemented. Enforcement remains prompt-level, not a deterministic sanitizer. |
| B-008 | architecture HTML report portability | RUNTIME_UNKNOWN | PROMPT, EXTERNAL_DEPENDENCY, RUNTIME | False | False | CT-008 | The artifact is a single HTML file but loads Tailwind/Mermaid from CDNs. Packaging self-containment is statically true; dependency independence is not. |
| B-009 | diagnosing-bugs architecture handoff | CONFIRMED_DRIFT | DOCUMENTATION, PROMPT | False | False | CT-009 | The autonomous handoff was deliberately removed and is absent from diagnosing-bugs, but human docs and ask-matt retain it. |
| B-010 | implement -> code-review visibility | CONFIRMED_GAP | PROMPT, EXECUTABLE_SCRIPT, RUNTIME | False | False | CT-010 | Implement orders code-review before commit, while code-review scopes its comparison to fixed-point...HEAD and fails on an empty committed diff. Without interim commits, the cross-skill contract can hide working-tree implementation changes from review. |
| B-011 | retro maturity | CONFIRMED_DRIFT | DOCUMENTATION, PROMPT | False | False | CT-011 | Bucket README says STUB/nonfunctional; operative retro source contains a substantial multi-step workflow and cross-skill call. |
| B-012 | setup-ts-deep-modules rule contract | CONFIRMED_GAP | PROMPT, STATIC_CONFIG, EXECUTABLE_SCRIPT | True | False | CT-012 | SKILL.md says four error rules, unconditional intra-package freedom, and four forbidden rules at completion. The shipped config has five error-level forbidden entries; tests-folder-is-private separately blocks non-test files from importing tests/, including within the same package. |
| B-013 | Wayfinder planning-only authority | CONFIRMED_WEAKNESS | PROMPT | False | False | CT-013 | The planning default explicitly permits an execution-carrying Notes override, while charting instructs the same agent to create the map with Notes filled in. No independent user-confirmation/authority check is specified for that override. |
| B-014 | setup-ts-deep-modules proof-of-enforcement | STATICALLY_ENFORCED | PROMPT, STATIC_CONFIG, EXECUTABLE_SCRIPT, RUNTIME | True | False | — | The workflow explicitly requires pass -> deliberate violating deep import -> fail with tests-through-entrypoints -> revert -> pass. This is a strong runtime completion criterion encoded in prompt instructions around an executable checker, although this audit has not run it in a consumer repo. |
| B-015 | wizard generated-script verification | STATICALLY_ENFORCED | PROMPT, EXECUTABLE_SCRIPT | PARTIAL | False | — | Wizard requires bash -n and shellcheck when available, but explicitly does not require an end-to-end agent execution. Static syntax/lint proof is stronger than prose-only but weaker than runtime observation. |
| B-016 | git-guardrails dangerous-command blocking | STATICALLY_ENFORCED | PROMPT, EXECUTABLE_SCRIPT, RUNTIME | True | False | — | The hook exits 2 on its regex-matched command patterns and setup requires a synthetic blocked-command test. Enforcement is executable but heuristic string matching, not parsed shell/Git semantics. |
| B-017 | setup-pre-commit hook smoke test | STATICALLY_ENFORCED | PROMPT, EXECUTABLE_SCRIPT, RUNTIME | True | False | — | The skill's completion path includes a real commit through Husky/lint-staged hooks, which is stronger than config existence alone. This audit has not executed that consumer-repo smoke test. |
| B-018 | plugin version synchronization | STATICALLY_ENFORCED | STATIC_CONFIG, EXECUTABLE_SCRIPT, CI | True | False | — | npm run version invokes sync-plugin-version.mjs and the release workflow uses that command; --check detects drift. This closes plugin/package drift statically while leaving package-lock outside the mechanism (B-004/CT-004). |
| B-019 | local skill linking set | STATICALLY_ENFORCED | EXECUTABLE_SCRIPT | True | False | — | The executable find expression explicitly excludes deprecated and misc and otherwise discovers SKILL.md under skills/, yielding the generated 33-skill local-link set. |
| B-020 | list-skills enumeration | STATICALLY_ENFORCED | EXECUTABLE_SCRIPT | True | False | — | The script runs find from the repository root for SKILL.md, excluding only node_modules, and sorts the result; frozen generated distribution truth therefore treats all 37 current skills as list-visible. |
| B-021 | setup confirmation-before-write boundary | CONFIRMED_MATCH | PROMPT | False | False | — | The operative setup workflow explicitly requires showing the Agent skills block plus docs/agents drafts and letting the user edit them before the write step. This is a clear human checkpoint, but it is prompt-level rather than mechanically enforced. |
| B-022 | setup verification mode | CONFIRMED_MATCH | PROMPT, NONE | False | False | — | The negative-memory policy explicitly rejects a separate verify/check mode and says maintainers should invoke setup with a natural-language verification request. The operative skill is explicitly prompt-driven, so this is intentional design rather than a missing implementation accidentally presented as deterministic validation. |
| B-023 | diagnosing-bugs red-loop gate | CONFIRMED_MATCH | PROMPT, RUNTIME | False | False | — | The operative skill repeatedly states no red-capable command means no Phase 2, requires one command already run with output, and instructs the agent to stop if it starts theorizing first. This is unusually strong prompt gating, but there is no external machine state preventing a model from skipping it. |
| B-024 | triage exclusive state/category invariant | CONFIRMED_WEAKNESS | PROMPT, EXTERNAL_DEPENDENCY | False | False | — | Triage explicitly states the one-category/one-state invariant and tells the agent to stop on pre-existing state-role conflicts. However, ordinary issue trackers permit multiple labels, and the quick state-override path says to apply the requested role directly without an explicit remove-other-state-label step. The invariant therefore depends on prompt adherence rather than tracker-level exclusivity. |
| B-025 | triage verification-before-grilling | CONFIRMED_MATCH | PROMPT, RUNTIME, EXTERNAL_DEPENDENCY | False | False | — | The operative sequence is gather context -> recommend/wait -> verify claim -> grill if needed -> apply outcome. Bugs should be reproduced; PRs should be checked out and tested. A separately documented maintainer quick override intentionally bypasses grilling and normal verification, so this row applies to the normal triage path only. |
| B-026 | implement-spec frontier scheduling | RUNTIME_UNKNOWN | PROMPT, RUNTIME | False | False | — | The skill explicitly defines tickets as a blocking task graph, dispatches implementer subagents from the frontier, and asks for more dispatch when merges change that frontier. There is no executable scheduler or machine check of dependency legality; correctness depends on agent interpretation of ticket relationships at runtime. |
| B-027 | implement-spec post-review fix revalidation | CONFIRMED_GAP | PROMPT, RUNTIME, NONE | False | False | CT-014 | Implement-spec requires one final /code-review, then delegates all review fixes to a single implementer subagent and immediately advances to marking the PR ready. No second review, finding-by-finding check, test gate, or equivalent post-fix acceptance step is required for the changed branch. |
| B-028 | domain-modeling inline capture discipline | CONFIRMED_MATCH | PROMPT | False | False | — | The operative skill distinguishes active model changes from passive vocabulary reading, requires immediate CONTEXT.md updates when a term is resolved, constrains CONTEXT.md to glossary content, and offers ADRs only when all three stated criteria are met. All of these controls are prompt-level. |
| B-029 | release version/tag path | STATICALLY_ENFORCED | CI, EXECUTABLE_SCRIPT, STATIC_CONFIG | True | False | — | The release workflow runs on main pushes, invokes changesets/action with version: npm run version and publish: npx changeset tag, while package.json's version command runs changeset version followed by sync-plugin-version.mjs. This gives a concrete static/CI path for package/plugin version propagation and tag creation, distinct from the stale package-lock issue. |

## Current counts

- states: `{'CONFIRMED_DRIFT': 5, 'CONFIRMED_GAP': 5, 'CONFIRMED_MATCH': 5, 'CONFIRMED_WEAKNESS': 2, 'RUNTIME_UNKNOWN': 4, 'STATICALLY_ENFORCED': 8}`
- enforcement layers: `{'CI': 3, 'DOCUMENTATION': 7, 'EXECUTABLE_SCRIPT': 11, 'EXTERNAL_DEPENDENCY': 3, 'NONE': 4, 'PROMPT': 23, 'RUNTIME': 10, 'STATIC_CONFIG': 7}`
- runtime observed rows: **0 / 29**
- integrity hard errors: **0**

## Phase 4 rule

A row can be statically adjudicated without being runtime-observed. No file becomes `VERIFIED` from this matrix alone; later applicable history, contradictions, runtime/distribution, second-pass, and red-team gates still apply.

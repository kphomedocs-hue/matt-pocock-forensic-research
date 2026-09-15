# Phase 4 Evidence-Depth Queue

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

This is an evidence-depth queue, not a breadth denominator. Every behavior row is assigned to exactly one evidence class. `runtime_observed: false` means the stronger evidence has not yet been recorded; it does not erase static findings already established in the behavior matrix.

Behavior denominator: **65**.
Classified: **65/65**.
Runtime-observed rows: **13/65**.
Pending stronger evidence: **52**.

## Evidence classes

| Class | Total | Observed | Pending | Meaning |
|---|---:|---:|---:|---|
| EXECUTION_OBSERVATION | 30 | 13 | 17 | Executable/runtime/CI contract; isolate and execute or obtain equivalent runtime evidence. |
| EXTERNAL_DEPENDENCY_VALIDATION | 7 | 0 | 7 | Behavior depends on an external service/tool/asset; validate the dependency assumption. |
| MACHINE_CONSUMER_VALIDATION | 4 | 0 | 4 | Static machine-readable config; prove the intended consumer loads/obeys it. |
| PROMPT_REDTEAM_LATER | 24 | 0 | 24 | Prompt/docs judgment contract; test adversarially in second-pass/red-team work. |

## Queue

| Behavior | Evidence class | State | Observed | Source MPs | Area | Next evidence |
|---|---|---|---|---|---|---|
| B-001 | MACHINE_CONSUMER_VALIDATION | CONFIRMED_DRIFT | NO | MP-0025, MP-0100, MP-0029, MP-0061, MP-0101 | TDD loop semantics | Later current-state comparison and runtime adherence belong to later verification gates. |
| B-002 | MACHINE_CONSUMER_VALIDATION | CONFIRMED_DRIFT | NO | MP-0018, MP-0030 | ask-matt promoted/invocation counts | No runtime reproduction needed to prove frozen numerical drift; later compare post-frozen current docs if relevant. |
| B-003 | PROMPT_REDTEAM_LATER | CONFIRMED_GAP | NO | MP-0030, MP-0063 | ask-matt target-source verification | Determine whether this is intentional accepted design or should become an operative gate. |
| B-004 | EXECUTION_OBSERVATION | RUNTIME_UNKNOWN | YES | MP-0055, MP-0056, MP-0059, MP-0019, MP-0018 | package/plugin/lock version truth | Release-path observation remains separate under B-029; local npm behavior shows the stale root lock version is normalized and does not control npm pack versioning. |
| B-005 | PROMPT_REDTEAM_LATER | CONFIRMED_GAP | NO | MP-0051, MP-0152, MP-0156 | Teach glossary format linkage | Classify optional/manual behavior as accepted design or wire/retire the support format. |
| B-006 | EXECUTION_OBSERVATION | RUNTIME_UNKNOWN | NO | MP-0156 | Teach workspace-root resolution | Reproduce in a supported harness or obtain equivalent direct runtime evidence. |
| B-007 | PROMPT_REDTEAM_LATER | CONFIRMED_DRIFT | NO | MP-0025, MP-0033, MP-0071 | diagnosing-bugs redaction | Runtime adherence is a later verification question; frozen docs drift is already established. |
| B-008 | EXECUTION_OBSERVATION | RUNTIME_UNKNOWN | YES | MP-0037, MP-0082, MP-0083 | architecture HTML report portability | Runtime closure covers the frozen CDN dependency boundary only. Define whether the product intends packaging self-containment or offline/locked-down portability; a real-browser rendering check can broaden compatibility evidence later. |
| B-009 | PROMPT_REDTEAM_LATER | CONFIRMED_DRIFT | NO | MP-0015, MP-0033, MP-0063, MP-0071 | diagnosing-bugs architecture handoff | Secondary surfaces should be aligned or explicitly historical. |
| B-010 | EXECUTION_OBSERVATION | CONFIRMED_GAP | YES | MP-0065, MP-0080 | implement -> code-review visibility | Frozen behavior is runtime-observed. A source correction would require committing before review or teaching code-review an explicit working-tree review mode. |
| B-011 | PROMPT_REDTEAM_LATER | CONFIRMED_DRIFT | NO | MP-0117, MP-0124 | retro maturity | Align maturity description; end-to-end quality remains a separate runtime question. |
| B-012 | EXECUTION_OBSERVATION | CONFIRMED_GAP | YES | MP-0126, MP-0128 | setup-ts-deep-modules rule contract | Source-side correction remains: document five rules plus the tests/ exception, or change the config/prose so the four-rule model is exact. Frozen runtime behavior is now observed. |
| B-013 | PROMPT_REDTEAM_LATER | CONFIRMED_WEAKNESS | NO | MP-0112 | Wayfinder planning-only authority | Require/identify an independent override authority or classify self-authored override as accepted design. |
| B-014 | EXECUTION_OBSERVATION | STATICALLY_ENFORCED | YES | MP-0126, MP-0128 | setup-ts-deep-modules proof-of-enforcement | Representative runtime completion semantics are closed. Broader compatibility across package managers and unusual repository layouts remains a separate generalization question. |
| B-015 | EXECUTION_OBSERVATION | STATICALLY_ENFORCED | YES | MP-0114, MP-0116 | wizard generated-script verification | Red-team generated wizard variants and browser-step accuracy later; this runtime observation covers the shipped template library/example only. |
| B-016 | EXECUTION_OBSERVATION | STATICALLY_ENFORCED | YES | MP-0136, MP-0138 | git-guardrails dangerous-command blocking | Red-team equivalent/wrapped commands and false-positive strings in Phase 9/runtime testing. |
| B-017 | EXECUTION_OBSERVATION | STATICALLY_ENFORCED | YES | MP-0143 | setup-pre-commit hook smoke test | Representative npm end-to-end smoke is closed. Preserve the executable-bit predicate mismatch as toolchain drift; package-manager variants and future upstream Husky/lint-staged compatibility remain separate generalization/current-state questions. |
| B-018 | EXECUTION_OBSERVATION | STATICALLY_ENFORCED | YES | MP-0018, MP-0019, MP-0056, MP-0059 | plugin version synchronization | Observe a live Changesets release/version-PR path later; B-004 separately tracks package-lock version truth. |
| B-019 | EXECUTION_OBSERVATION | STATICALLY_ENFORCED | YES | MP-0057 | local skill linking set | Filesystem symlink behavior can be runtime-observed later; static selection semantics are closed. |
| B-020 | EXECUTION_OBSERVATION | STATICALLY_ENFORCED | YES | MP-0058 | list-skills enumeration | No separate runtime verification is needed for static selection semantics unless environment-specific find behavior becomes material. |
| B-021 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0093 | setup confirmation-before-write boundary | Later runtime observation can test whether supported harnesses consistently honor the checkpoint. |
| B-022 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0023, MP-0093 | setup verification mode | A later runtime pass can test verification quality, but static design intent is reconciled. |
| B-023 | EXECUTION_OBSERVATION | CONFIRMED_MATCH | NO | MP-0071 | diagnosing-bugs red-loop gate | Runtime/red-team testing should attempt to induce premature hypothesis generation and measure adherence. |
| B-024 | EXTERNAL_DEPENDENCY_VALIDATION | CONFIRMED_WEAKNESS | NO | MP-0099, MP-0110 | triage exclusive state/category invariant | Runtime-test a transition from an already-state-labeled issue and determine whether prior state labels are reliably removed. |
| B-025 | EXECUTION_OBSERVATION | CONFIRMED_MATCH | NO | MP-0110 | triage verification-before-grilling | Later runtime observation can test whether the normal path actually performs the requested reproduction/checkout before grilling. |
| B-026 | EXECUTION_OBSERVATION | RUNTIME_UNKNOWN | NO | MP-0120 | implement-spec frontier scheduling | Run a representative dependency graph with at least one blocked branch and verify that no blocked ticket starts early. |
| B-027 | EXECUTION_OBSERVATION | CONFIRMED_GAP | NO | MP-0065, MP-0120 | implement-spec post-review fix revalidation | Add or identify a post-fix acceptance gate; runtime reproduction can demonstrate whether review-fix regressions can reach the ready state. |
| B-028 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0074, MP-0075, MP-0076 | domain-modeling inline capture discipline | Second-pass/runtime testing should look for implementation-detail leakage into CONTEXT.md and over-eager ADR creation. |
| B-029 | EXECUTION_OBSERVATION | STATICALLY_ENFORCED | NO | MP-0019, MP-0056, MP-0059 | release version/tag path | Observe an actual release/version-PR run later; static wiring is closed. |
| B-030 | EXTERNAL_DEPENDENCY_VALIDATION | CONFIRMED_GAP | NO | MP-0043, MP-0104, MP-0106 | to-spec parent ready-for-agent routing | Use a distinct parent/spec state, strip ready-for-agent during ticketization, or make dispatchers mechanically distinguish parent specs from executable tickets. |
| B-031 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0044, MP-0106 | to-tickets pre-publication approval | Runtime-test whether ambiguous or AFK prompts can cause publication before explicit approval. |
| B-032 | PROMPT_REDTEAM_LATER | CONFIRMED_GAP | NO | MP-0044, MP-0106 | to-tickets acceptance-criteria falsifiability | Require every criterion to name a falsifying observation and verify it is false at base unless explicitly justified. |
| B-033 | EXTERNAL_DEPENDENCY_VALIDATION | CONFIRMED_GAP | NO | MP-0036, MP-0080, MP-0106 | implement ticket lifecycle and frontier closure | Add an explicit completion step that reconciles acceptance criteria and closes/updates the ticket before frontier recomputation. |
| B-034 | EXECUTION_OBSERVATION | CONFIRMED_MATCH | NO | MP-0089 | research primary-source discipline | Runtime/red-team should inject plausible secondary sources and unsupported claims to measure adherence. |
| B-035 | EXECUTION_OBSERVATION | RUNTIME_UNKNOWN | NO | MP-0085, MP-0086, MP-0087 | prototype throwaway isolation and capture | Runtime-verify branch isolation, pointer creation, and decision capture on representative logic and UI prototypes. |
| B-036 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0067, MP-0068, MP-0069 | codebase-design vocabulary discipline | Second-pass/red-team should look for internal examples or linked support guidance that violate the stated vocabulary/seam rules. |
| B-037 | EXTERNAL_DEPENDENCY_VALIDATION | RUNTIME_UNKNOWN | NO | MP-0093, MP-0096, MP-0097, MP-0099 | setup triage-label materialization | Runtime-test setup on a tracker lacking the default labels and observe whether later triage operations fail, create labels, or recover. |
| B-038 | EXTERNAL_DEPENDENCY_VALIDATION | CONFIRMED_GAP | NO | MP-0108, MP-0110 | triage ready-for-agent brief invariant | Require the brief before or atomically with ready-for-agent, or explicitly redefine the quick-override state and downstream consumer contract. |
| B-039 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0078, MP-0076, MP-0148 | grill-with-docs aggregate delegation | Runtime observation can later test whether both delegated workflows are actually invoked and preserve their respective contracts in one session. |
| B-040 | EXECUTION_OBSERVATION | CONFIRMED_MATCH | NO | MP-0091 | resolving-merge-conflicts intent-preservation workflow | Red-team a conflict where intents are genuinely incompatible and a rebase with multiple conflict stops; verify the skill neither invents behavior nor exits prematurely. |
| B-041 | EXECUTION_OBSERVATION | RUNTIME_UNKNOWN | NO | MP-0118 | claude-handoff background-agent privacy and launch | Runtime-test launch, working-directory inheritance, name propagation, artifact references, and deliberate secret/PII injection before treating the handoff as verified. |
| B-042 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0122, MP-0148 | loop-me workflow-spec completion | Runtime/red-team with an underspecified workflow and verify the session refuses to declare done while implementation questions remain. |
| B-043 | EXECUTION_OBSERVATION | CONFIRMED_MATCH | NO | MP-0129 | writing-beats grounded incremental authorship | Runtime-test an attempted ungrounded beat and an external edit between turns; verify the candidate is blocked or grounded first and the edit is preserved. |
| B-044 | EXECUTION_OBSERVATION | CONFIRMED_MATCH | NO | MP-0131 | writing-fragments explore-only append discipline | Runtime-test whether the agent resists outlining pressure and preserves reordered/deleted fragments made outside the conversation. |
| B-045 | EXECUTION_OBSERVATION | CONFIRMED_MATCH | NO | MP-0133 | writing-shape raw-input immutability | Runtime-test with external edits to both raw and output files and verify the raw source is never modified while article edits are preserved. |
| B-046 | EXECUTION_OBSERVATION | CONFIRMED_MATCH | YES | MP-0139 | migrate-to-shoehorn assertion discovery coverage | If deeper verification is needed, test the actual edit/import/type-check migration on representative single- and double-assertion files; discovery coverage itself is closed. |
| B-047 | EXTERNAL_DEPENDENCY_VALIDATION | CONFIRMED_GAP | NO | MP-0141 | scaffold-exercises variant/linter contract | Run a solution-only fixture against the actual linter and then align the operative variant rule to the observed acceptance set. |
| B-048 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0146, MP-0148 | grill-me delegation wrapper | Runtime observation only needs to confirm the alias actually delegates rather than diverging in the host harness. |
| B-049 | EXECUTION_OBSERVATION | CONFIRMED_MATCH | NO | MP-0148 | grilling frontier and authority discipline | Red-team with dependent questions and unavailable facts; verify downstream questions wait while unrelated frontier questions continue. |
| B-050 | EXECUTION_OBSERVATION | RUNTIME_UNKNOWN | NO | MP-0150 | handoff temporary-storage and redaction contract | Runtime-test platform-specific temp resolution plus seeded secrets/PII and verify the workspace remains untouched. |
| B-051 | EXECUTION_OBSERVATION | CONFIRMED_MATCH | NO | MP-0158 | questionnaire send-focused completeness | Runtime-test a multi-gap request and verify no requested gap disappears and no compound questions merge independent decisions. |
| B-052 | EXECUTION_OBSERVATION | RUNTIME_UNKNOWN | NO | MP-0160 | wait-what controlled-language repitch | Runtime-test in single-context, multi-context, and no-CONTEXT repositories; decide whether missing context needs an explicit fallback contract. |
| B-053 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0162, MP-0163 | writing-for-agents information-hierarchy discipline | Second-pass/red-team should apply the doctrine back onto the repository itself and record where shipped skills violate their own writing guidance. |
| B-054 | MACHINE_CONSUMER_VALIDATION | CONFIRMED_MATCH | NO | MP-0064, MP-0066, MP-0070, MP-0072, MP-0077, MP-0079, MP-0081, MP-0084, MP-0088, MP-0090, MP-0092, MP-0094, MP-0101, MP-0105, MP-0107, MP-0111, MP-0113, MP-0115, MP-0119, MP-0121, MP-0123, MP-0125, MP-0127, MP-0130, MP-0132, MP-0134, MP-0137, MP-0140, MP-0142, MP-0144, MP-0147, MP-0149, MP-0151, MP-0157, MP-0159, MP-0161, MP-0164 | Codex per-skill invocation metadata | Runtime-observe representative user-invoked and model-invoked skills in Codex, then sample boundary cases if the harness behavior differs from the static contract. |
| B-055 | MACHINE_CONSUMER_VALIDATION | CONFIRMED_MATCH | NO | MP-0017 | Claude marketplace distribution descriptor | Exercise marketplace discovery/install against the frozen-compatible distribution path during Phase 7 runtime verification. |
| B-056 | EXECUTION_OBSERVATION | CONFIRMED_WEAKNESS | YES | MP-0073 | diagnosing-bugs human-in-the-loop shell template | Red-team secret/PII misuse and shell-input edge cases later; do not use real credentials. |
| B-057 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0062 | ask-matt phase-boundary context routing | Later compare real routing decisions against this ordered tree during red-team verification, especially ambiguous boundaries. |
| B-058 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0095 | setup skill domain-document consumption | Observe a setup/exploration run in repos with present, absent, and conflicting domain docs. |
| B-059 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0098 | local Markdown issue-tracker contract | Runtime-test concurrent/duplicate claiming and malformed status files before treating the local tracker as robust coordination machinery. |
| B-060 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0102 | TDD mocking boundary policy | Red-team the TDD workflow with codebases that already use internal mocks and see whether the operative skill follows or overrides this support rule. |
| B-061 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0103 | TDD test-quality policy | Use adversarial examples during Phase 9 to test whether the operative TDD skill rejects brittle tests that still pass. |
| B-062 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0109 | triage out-of-scope institutional memory | Test near-duplicate and superficially similar requests to measure false-positive/false-negative semantic matching during red-team verification. |
| B-063 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0153 | Teach learning-record persistence | Observe Teach across repeated sessions, including a corrected misconception and concurrent/new record numbering edge case. |
| B-064 | PROMPT_REDTEAM_LATER | CONFIRMED_MATCH | NO | MP-0154 | Teach mission steering contract | Runtime-observe mission creation and a mid-course mission change to verify downstream teaching actually reorients. |
| B-065 | EXTERNAL_DEPENDENCY_VALIDATION | CONFIRMED_MATCH | NO | MP-0155 | Teach curated-resource epistemic contract | Test Teach on a topic with incomplete resources to verify it surfaces gaps rather than filling them from unsupported model guesses. |

Hard errors: **0**.

# Contradiction Register

Statuses: `OPEN / RESOLVED / ACCEPTED DESIGN / UNKNOWN`.
Defect-state labels: `CURRENT / FIXED / PARTIALLY FIXED / DOCS STALE / UNKNOWN`.

## Current contradictions / enforcement gaps

| ID | Area | Evidence A | Evidence B | Classification | Status | Notes |
|---|---|---|---|---|---|---|
| CT-001 | TDD description | Frozen `CHANGELOG.md` (MP-0025) records that v1.1.0 removed refactor from TDD and moved it to review; frozen operative `tdd/SKILL.md` (MP-0100) explicitly says red → green and that refactoring is not part of the loop. | Frozen root `README.md` (MP-0029), Engineering README (MP-0061), and Codex metadata `tdd/agents/openai.yaml` (MP-0101) still describe TDD as red-green-refactor. | DOCS / METADATA STALE | OPEN | Historical intent and current operative source agree; multiple user/distribution-facing descriptions remain stale. |
| CT-002 | ask-matt counts | Frozen plugin manifest (MP-0018) lists 25 promoted skills; metadata census established 14 user-invoked / 11 model-invoked. | Frozen `docs/engineering/ask-matt.md` (MP-0030) says “Thirteen of the plugin's twenty-two skills carry the flag.” | DOCS STALE | OPEN | Quantitative statement is directly stale in the frozen docs. |
| CT-003 | ask-matt verification behavior | Frozen `docs/engineering/ask-matt.md` (MP-0030) says success means behavior claims show trace evidence of reading the target `SKILL.md`, and calls the router a secondary source. | Frozen operative `skills/engineering/ask-matt/SKILL.md` (MP-0063) contains no mandatory step to open/read the target skill source before making load-bearing claims. | ENFORCEMENT GAP | OPEN | Both sides are now durably evidenced at the frozen commit. Router summaries can therefore function as unchecked secondary-source assertions. |
| CT-004 | package lock version | Frozen package.json MP-0056 is version 1.2.3. | Frozen package-lock.json MP-0055 retains root version 0.0.0 in both top-level and root-package metadata. | METADATA DRIFT | PARTIALLY RESOLVED | History shows lockfile was never regenerated after bootstrap; runtime effect still UNKNOWN. Version sync MP-0059 does not touch package-lock. |
| CT-005 | teach glossary linkage | Frozen support file MP-0152 `GLOSSARY-FORMAT.md` exists and defines a substantial canonical glossary format. Exhaustive literal-reference extraction now finds exactly one incoming reference, from frozen human docs MP-0051 `docs/productivity/teach.md`. | Frozen operative Teach source MP-0156 discusses glossaries as essential but does not reference `GLOSSARY-FORMAT.md`; MP-0051 explicitly says the skill ships the file but `SKILL.md` no longer links to it, so a glossary appears only if the user asks. | OPERATIVE LINKAGE GAP / DOCUMENTED STALE SUPPORT | OPEN | The exhaustive 164-blob literal scan disproves the stronger “repository orphan” hypothesis: the file is referenced by human docs. The functional problem remains: the canonical format is not wired into the operative Teach workflow. |
| CT-006 | teach workspace root | Teach source uses relative paths both for co-located support and user workspace state. | Issue #377 reports files being written into installed skill directory. | RUNTIME AMBIGUITY | OPEN | Needs harness/runtime reproduction to move beyond reported evidence. |
| CT-007 | diagnosing-bugs redaction | Frozen operative diagnosing-bugs source MP-0071 contains an explicit `Redact` section requiring `<REDACTED>`, env-var-based loops, and minimal quoted artifact lines; frozen CHANGELOG MP-0025 records the same behavior shipping in v1.2.3. | Frozen `docs/engineering/diagnosing-bugs.md` (MP-0033) still says artifact/output redaction is open and unimplemented. | DOCS STALE | OPEN | Current operative source and release history agree; human docs are stale. |
| CT-008 | architecture report portability | Frozen `HTML-REPORT.md` MP-0082 and operative architecture skill MP-0083 call the artifact a self-contained HTML file but load Tailwind and Mermaid from CDNs. | Frozen human docs report silent degradation offline/locked-down. | RUNTIME PORTABILITY GAP | OPEN | Self-contained in file packaging, not dependency independence. |
| CT-009 | diagnosing-bugs architecture handoff | Frozen changeset MP-0015 says the autonomous `diagnosing-bugs` → `improve-codebase-architecture` handoff was removed outright; frozen operative diagnosing-bugs source MP-0071 contains no such handoff. | Frozen diagnosing-bugs docs MP-0033 and operative ask-matt router MP-0063 still describe that handoff. | DOCS / ROUTER STALE | OPEN | Operative source confirms removal; two secondary surfaces retain removed behavior. |
| CT-010 | implement → code-review ordering | Frozen operative implement source MP-0080 explicitly says run `/code-review` once done, then commit. | Frozen operative code-review source MP-0065 reviews only `git diff <fixed-point>...HEAD` and fails early on empty diff; staged/working-tree-only changes are outside that comparison. | WORKFLOW ENFORCEMENT GAP | OPEN | Both operative sources now confirm the mismatch. A run with no interim commit can invoke review before the implementation exists in HEAD. |
| CT-011 | retro maturity description | Frozen `skills/in-progress/README.md` MP-0117 labels `retro` as `STUB: design notes only, not functional yet`. | Frozen operative `retro/SKILL.md` MP-0124 contains a complete multi-step retrospective workflow, categories, file guidance, and an operative call to `writing-for-agents`. | BUCKET DOCS STALE | OPEN | Current bucket README materially understates the implemented behavior of the in-progress skill. |

## Normalized closure overlay

This overlay adds the canonical fields defined in `00_RESEARCH_SCHEMA.md` without redefining primary contradiction IDs.

| Ref | Origin | Defect state | Impact | Resolution test / next evidence |
|---|---|---|---|---|
| ↳ CT-001 | SOURCE_REPO | DOCS STALE | User-facing and Codex-facing TDD semantics can disagree with operative behavior. | Confirm all frozen/current secondary surfaces describe red → green only, or document an intentional semantic split. |
| ↳ CT-002 | SOURCE_REPO | DOCS STALE | Router documentation reports wrong plugin/invocation counts. | Recompute promoted/invocation counts mechanically and verify the docs match the generated set. |
| ↳ CT-003 | SOURCE_REPO | CURRENT | Router can make behavior claims without proving the target source was read. | Show an operative mandatory target-source verification step, or classify the gap as accepted design. |
| ↳ CT-004 | SOURCE_REPO | PARTIALLY FIXED | Package metadata contains two version truths; downstream tooling effect is uncertain. | Trace package-lock consumers/runtime and determine whether stale root version has practical effect. |
| ↳ CT-005 | SOURCE_REPO | CURRENT | A substantial canonical glossary format exists and is documented, but Teach does not load/reference it operatively; behavior depends on the user asking for a glossary. | Wire `GLOSSARY-FORMAT.md` into the operative Teach workflow, intentionally retire the support file, or explicitly accept the optional/manual behavior. |
| ↳ CT-006 | SOURCE_REPO | UNKNOWN | Relative-path ambiguity may cause writes into installed skill state. | Reproduce in supported harness/runtime or obtain equivalent direct evidence of workspace-root resolution. |
| ↳ CT-007 | SOURCE_REPO | DOCS STALE | Human docs understate shipped redaction safeguards. | Verify current docs align with operative redaction behavior and release history. |
| ↳ CT-008 | SOURCE_REPO | CURRENT | “Self-contained” report can degrade when CDN access is unavailable. | Define self-contained semantics and test offline/locked-down rendering behavior. |
| ↳ CT-009 | SOURCE_REPO | DOCS STALE | Removed architecture handoff remains advertised by docs/router. | Verify all current secondary surfaces remove the deleted handoff or explicitly mark it historical. |
| ↳ CT-010 | SOURCE_REPO | CURRENT | Review can run before implementation exists in HEAD, yielding an empty committed diff. | Reproduce ordering path and verify either interim commit requirement or review support for staged/working-tree changes. |
| ↳ CT-011 | SOURCE_REPO | DOCS STALE | Bucket README materially misstates `retro` maturity. | Compare current bucket README against operative skill state and align the description. |

## Resolved historical defects retained for pattern analysis

| ID | Area | Defect | Resolution | State |
|---|---|---|---|---|
| CT-H01 | Cross-skill invocation | PR #878 mechanically rewrote soft references into Skill-tool calls including user-invoked targets. | PR #880 restored human-run preconditions and added invocation-type carve-out. | FIXED |
| CT-H02 | Router completeness | ask-matt historically missed multiple shipped skills. | Later coherence passes added missing routes and governance rule to re-check router on skill changes. | FIXED, recurrence risk remains |
| CT-H03 | Plugin/package version | plugin.json manually advanced while package.json lagged. | `sync-plugin-version.mjs` + release workflow now make package.json authoritative for plugin version. | FIXED |

Historical entries above are all `SOURCE_REPO` origin. Audit-tooling defects are tracked separately in `00_TOOLING_INTEGRITY_AUDIT.md` and `00_TOOLING_FAILURE_LEDGER.md`.

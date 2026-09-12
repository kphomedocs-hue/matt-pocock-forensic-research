# Contradiction Register

Statuses: `OPEN / RESOLVED / ACCEPTED DESIGN / UNKNOWN`.
Defect-state labels: `CURRENT / FIXED / PARTIALLY FIXED / DOCS STALE / UNKNOWN`.

## Current contradictions / enforcement gaps

| ID | Area | Evidence A | Evidence B | Classification | Status | Notes |
|---|---|---|---|---|---|---|
| CT-001 | TDD description | Frozen `CHANGELOG.md` (MP-0025) records that v1.1.0 removed refactor from TDD and moved it to review. | Frozen root `README.md` (MP-0029) and Engineering README (MP-0061) still describe TDD as red-green-refactor. | DOCS STALE | OPEN | Historical intent and current stale wording are durably evidenced from the frozen commit; TDD docs MP-0042 explicitly describe red→green only. |
| CT-002 | ask-matt counts | Frozen plugin manifest (MP-0018) lists 25 promoted skills; metadata census established 14 user-invoked / 11 model-invoked. | Frozen `docs/engineering/ask-matt.md` (MP-0030) says “Thirteen of the plugin's twenty-two skills carry the flag.” | DOCS STALE | OPEN | Quantitative statement is directly stale in the frozen docs. |
| CT-003 | ask-matt verification behavior | Frozen `docs/engineering/ask-matt.md` (MP-0030) says success means behavior claims show trace evidence of reading the target `SKILL.md`, and calls the router a secondary source. | Frozen operative `skills/engineering/ask-matt/SKILL.md` (MP-0063) contains no mandatory step to open/read the target skill source before making load-bearing claims. | ENFORCEMENT GAP | OPEN | Both sides are now durably evidenced at the frozen commit. Router summaries can therefore function as unchecked secondary-source assertions. |
| CT-004 | package lock version | Frozen package.json MP-0056 is version 1.2.3. | Frozen package-lock.json MP-0055 retains root version 0.0.0 in both top-level and root-package metadata. | METADATA DRIFT | PARTIALLY RESOLVED | History shows lockfile was never regenerated after bootstrap; runtime effect still UNKNOWN. Version sync MP-0059 does not touch package-lock. |
| CT-005 | teach glossary | `skills/productivity/teach/GLOSSARY-FORMAT.md` exists. | Current teach skill/support flow does not reference it; issue #559 reports orphaning. | ORPHAN / POSSIBLE STALE SUPPORT FILE | OPEN | Needs incoming-reference exhaustive scan before final orphan classification. |
| CT-006 | teach workspace root | Teach source uses relative paths both for co-located support and user workspace state. | Issue #377 reports files being written into installed skill directory. | RUNTIME AMBIGUITY | OPEN | Needs harness/runtime reproduction to move beyond reported evidence. |
| CT-007 | diagnosing-bugs redaction | Frozen CHANGELOG MP-0025 records that v1.2.3 shipped a Redact section and redacted capture behavior. | Frozen `docs/engineering/diagnosing-bugs.md` (MP-0033) still says artifact/output redaction is open and unimplemented and tells users to treat redaction as their own job. | DOCS STALE | OPEN | Both sides are now directly evidenced at the frozen commit. Operative SKILL reread will confirm current implementation details. |
| CT-008 | architecture report portability | Skill expects self-contained temp HTML but relies on Tailwind/Mermaid CDNs. | Docs report silent degradation offline/locked-down. | RUNTIME PORTABILITY GAP | OPEN | Self-contained in file packaging, not dependency independence. |
| CT-009 | diagnosing-bugs architecture handoff | Frozen changeset MP-0015 says the autonomous `diagnosing-bugs` → `improve-codebase-architecture` handoff was removed outright. | Frozen diagnosing-bugs docs MP-0033 and operative ask-matt router MP-0063 still describe that handoff. | DOCS / ROUTER STALE | OPEN | Two current secondary surfaces retain behavior explicitly removed by the invocation-fix changeset. Diagnosing-bugs SKILL reread at MP-0071 will close the operative-source side. |
| CT-010 | implement → code-review ordering | Frozen implement docs MP-0036 and ask-matt router MP-0063 say the run performs `code-review` and then commits. | Frozen code-review docs MP-0031 say review uses `<fixed-point>...HEAD`, excluding staged and working-tree changes, and explicitly warn that implement's pre-commit review can therefore see none of the work. | WORKFLOW ENFORCEMENT GAP candidate | OPEN | Human docs and router describe the mismatch as current/unfixed. Confirm exact operative implement/code-review source ordering before final defect classification. |

## Resolved historical defects retained for pattern analysis

| ID | Area | Defect | Resolution | State |
|---|---|---|---|---|
| CT-H01 | Cross-skill invocation | PR #878 mechanically rewrote soft references into Skill-tool calls including user-invoked targets. | PR #880 restored human-run preconditions and added invocation-type carve-out. | FIXED |
| CT-H02 | Router completeness | ask-matt historically missed multiple shipped skills. | Later coherence passes added missing routes and governance rule to re-check router on skill changes. | FIXED, recurrence risk remains |
| CT-H03 | Plugin/package version | plugin.json manually advanced while package.json lagged. | `sync-plugin-version.mjs` + release workflow now make package.json authoritative for plugin version. | FIXED |

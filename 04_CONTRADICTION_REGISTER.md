# Contradiction Register

Statuses: `OPEN / RESOLVED / ACCEPTED DESIGN / UNKNOWN`.
Defect-state labels: `CURRENT / FIXED / PARTIALLY FIXED / DOCS STALE / UNKNOWN`.

## Current contradictions / enforcement gaps

| ID | Area | Evidence A | Evidence B | Classification | Status | Notes |
|---|---|---|---|---|---|---|
| CT-001 | TDD description | Frozen `CHANGELOG.md` (MP-0025) records that v1.1.0 removed refactor from TDD and moved it to review. | Frozen root `README.md` (MP-0029) still says red-green-refactor is critical, says `/tdd` encourages red-green-refactor, and labels the TDD reference row as a red-green-refactor loop. | DOCS STALE | OPEN | Historical intent and current stale wording are both now durably evidenced from the frozen commit. |
| CT-002 | ask-matt counts | Frozen plugin manifest: 25 promoted skills; metadata audit: 14 user-invoked. | ask-matt docs still mention 22 skills / 13 user-invoked in missing-skill discussion. | DOCS STALE | OPEN | Quantitative statement is stale. |
| CT-003 | ask-matt verification behavior | Human docs say load-bearing behavior claims should show trace evidence of reading target SKILL.md. | Operative `ask-matt/SKILL.md` has no required verification step. | ENFORCEMENT GAP | OPEN | Docs describe safer behavior than prompt enforces. |
| CT-004 | package lock version | `package.json` / plugin current release version 1.2.3. | `package-lock.json` root remains 0.0.0. | METADATA DRIFT | PARTIALLY RESOLVED | History shows lockfile was never regenerated after bootstrap; runtime effect still UNKNOWN. |
| CT-005 | teach glossary | `skills/productivity/teach/GLOSSARY-FORMAT.md` exists. | Current teach skill/support flow does not reference it; issue #559 reports orphaning. | ORPHAN / POSSIBLE STALE SUPPORT FILE | OPEN | Needs incoming-reference exhaustive scan before final orphan classification. |
| CT-006 | teach workspace root | Teach source uses relative paths both for co-located support and user workspace state. | Issue #377 reports files being written into installed skill directory. | RUNTIME AMBIGUITY | OPEN | Needs harness/runtime reproduction to move beyond reported evidence. |
| CT-007 | diagnosing-bugs docs/history | v1.2.3 shipped Redact behavior. | Some human-facing discussion still frames redaction as open rough edge. | DOCS STALE candidate | OPEN | Need exact current docs line reconciliation before final classification. |
| CT-008 | architecture report portability | Skill expects self-contained temp HTML but relies on Tailwind/Mermaid CDNs. | Docs report silent degradation offline/locked-down. | RUNTIME PORTABILITY GAP | OPEN | Self-contained in file packaging, not dependency independence. |

## Resolved historical defects retained for pattern analysis

| ID | Area | Defect | Resolution | State |
|---|---|---|---|---|
| CT-H01 | Cross-skill invocation | PR #878 mechanically rewrote soft references into Skill-tool calls including user-invoked targets. | PR #880 restored human-run preconditions and added invocation-type carve-out. | FIXED |
| CT-H02 | Router completeness | ask-matt historically missed multiple shipped skills. | Later coherence passes added missing routes and governance rule to re-check router on skill changes. | FIXED, recurrence risk remains |
| CT-H03 | Plugin/package version | plugin.json manually advanced while package.json lagged. | `sync-plugin-version.mjs` + release workflow now make package.json authoritative for plugin version. | FIXED |

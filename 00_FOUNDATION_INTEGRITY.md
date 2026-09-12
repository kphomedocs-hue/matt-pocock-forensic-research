# Foundation Integrity Report

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`

Hard integrity errors: **20**

Warnings / normalization gaps: **21**

## Durable provenance

- Census rows: **164 / 164**
- Durable notes found: **164 / 164**
- Status counts: `{'READ': 164}`

## Note-schema coverage

These are normalization measurements, not Phase 2 failures. Existing evidence is preserved.

| Recommended field group | Notes containing it | Total |
|---|---:|---:|
| read_evidence | 144 | 164 |
| source_facts | 154 | 164 |
| connections | 20 | 164 |
| unresolved | 20 | 164 |

## Register cross-checks

- Current contradiction IDs: **11**
- Historical contradiction IDs: **3**
- History entries: **9**
- Note contradiction refs missing from register: **0**
- Note history refs missing from ledger: **0**

## Generated distribution truth

- Current skills: **37**
- Claude plugin promoted: **25**
- Maintainer local-linked: **33**
- Skills with Codex metadata owner: **37**

| Skill | Bucket | Plugin | Local link | Codex metadata |
|---|---|---|---|---|
| `skills/engineering/ask-matt` | engineering | YES | YES | YES |
| `skills/engineering/code-review` | engineering | YES | YES | YES |
| `skills/engineering/codebase-design` | engineering | YES | YES | YES |
| `skills/engineering/diagnosing-bugs` | engineering | YES | YES | YES |
| `skills/engineering/domain-modeling` | engineering | YES | YES | YES |
| `skills/engineering/grill-with-docs` | engineering | YES | YES | YES |
| `skills/engineering/implement` | engineering | YES | YES | YES |
| `skills/engineering/improve-codebase-architecture` | engineering | YES | YES | YES |
| `skills/engineering/prototype` | engineering | YES | YES | YES |
| `skills/engineering/research` | engineering | YES | YES | YES |
| `skills/engineering/resolving-merge-conflicts` | engineering | YES | YES | YES |
| `skills/engineering/setup-matt-pocock-skills` | engineering | YES | YES | YES |
| `skills/engineering/tdd` | engineering | YES | YES | YES |
| `skills/engineering/to-spec` | engineering | YES | YES | YES |
| `skills/engineering/to-tickets` | engineering | YES | YES | YES |
| `skills/engineering/triage` | engineering | YES | YES | YES |
| `skills/engineering/wayfinder` | engineering | YES | YES | YES |
| `skills/engineering/wizard` | engineering | YES | YES | YES |
| `skills/in-progress/claude-handoff` | in-progress | NO | YES | YES |
| `skills/in-progress/implement-spec` | in-progress | NO | YES | YES |
| `skills/in-progress/loop-me` | in-progress | NO | YES | YES |
| `skills/in-progress/retro` | in-progress | NO | YES | YES |
| `skills/in-progress/setup-ts-deep-modules` | in-progress | NO | YES | YES |
| `skills/in-progress/writing-beats` | in-progress | NO | YES | YES |
| `skills/in-progress/writing-fragments` | in-progress | NO | YES | YES |
| `skills/in-progress/writing-shape` | in-progress | NO | YES | YES |
| `skills/misc/git-guardrails-claude-code` | misc | NO | NO | YES |
| `skills/misc/migrate-to-shoehorn` | misc | NO | NO | YES |
| `skills/misc/scaffold-exercises` | misc | NO | NO | YES |
| `skills/misc/setup-pre-commit` | misc | NO | NO | YES |
| `skills/productivity/grill-me` | productivity | YES | YES | YES |
| `skills/productivity/grilling` | productivity | YES | YES | YES |
| `skills/productivity/handoff` | productivity | YES | YES | YES |
| `skills/productivity/teach` | productivity | YES | YES | YES |
| `skills/productivity/to-questionnaire` | productivity | YES | YES | YES |
| `skills/productivity/wait-what` | productivity | YES | YES | YES |
| `skills/productivity/writing-for-agents` | productivity | YES | YES | YES |

## Hard errors

- 02_FILE_NOTES/MP-0021.md: frozen commit missing/mismatch
- 02_FILE_NOTES/MP-0021.md: blob SHA missing/mismatch against census
- 02_FILE_NOTES/MP-0022.md: frozen commit missing/mismatch
- 02_FILE_NOTES/MP-0022.md: blob SHA missing/mismatch against census
- 02_FILE_NOTES/MP-0023.md: frozen commit missing/mismatch
- 02_FILE_NOTES/MP-0023.md: blob SHA missing/mismatch against census
- 02_FILE_NOTES/MP-0024.md: frozen commit missing/mismatch
- 02_FILE_NOTES/MP-0024.md: blob SHA missing/mismatch against census
- 02_FILE_NOTES/MP-0025.md: frozen commit missing/mismatch
- 02_FILE_NOTES/MP-0025.md: blob SHA missing/mismatch against census
- 02_FILE_NOTES/MP-0026.md: frozen commit missing/mismatch
- 02_FILE_NOTES/MP-0026.md: blob SHA missing/mismatch against census
- 02_FILE_NOTES/MP-0027.md: frozen commit missing/mismatch
- 02_FILE_NOTES/MP-0027.md: blob SHA missing/mismatch against census
- 02_FILE_NOTES/MP-0028.md: frozen commit missing/mismatch
- 02_FILE_NOTES/MP-0028.md: blob SHA missing/mismatch against census
- 02_FILE_NOTES/MP-0029.md: frozen commit missing/mismatch
- 02_FILE_NOTES/MP-0029.md: blob SHA missing/mismatch against census
- 02_FILE_NOTES/MP-0030.md: frozen commit missing/mismatch
- 02_FILE_NOTES/MP-0030.md: blob SHA missing/mismatch against census

## Normalization warnings

- 02_FILE_NOTES/MP-0021.md: category line missing
- 02_FILE_NOTES/MP-0022.md: category line missing
- 02_FILE_NOTES/MP-0023.md: category line missing
- 02_FILE_NOTES/MP-0024.md: category line missing
- 02_FILE_NOTES/MP-0025.md: category line missing
- 02_FILE_NOTES/MP-0026.md: category line missing
- 02_FILE_NOTES/MP-0027.md: category line missing
- 02_FILE_NOTES/MP-0028.md: category line missing
- 02_FILE_NOTES/MP-0029.md: category line missing
- 02_FILE_NOTES/MP-0030.md: category line missing
- 02_FILE_NOTES/MP-0031.md: category line missing
- 02_FILE_NOTES/MP-0032.md: category line missing
- 02_FILE_NOTES/MP-0033.md: category line missing
- 02_FILE_NOTES/MP-0034.md: category line missing
- 02_FILE_NOTES/MP-0035.md: category line missing
- 02_FILE_NOTES/MP-0036.md: category line missing
- 02_FILE_NOTES/MP-0037.md: category line missing
- 02_FILE_NOTES/MP-0038.md: category line missing
- 02_FILE_NOTES/MP-0039.md: category line missing
- 02_FILE_NOTES/MP-0040.md: category line missing
- Could not mechanically confirm all expected link buckets from script text; detected ['in-progress', 'misc', 'deprecated']

## Gate

Phase 3 file promotion must not begin if this report has any hard integrity errors. Schema-coverage gaps are tracked for normalization but do not invalidate the completed physical read by themselves.

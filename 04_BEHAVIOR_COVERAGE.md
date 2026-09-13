# Phase 4 Behavior Coverage

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

Coverage means a file participates in at least one explicit Phase 4 behavior contract. It does **not** mean the file is VERIFIED or that every behavior has been exhausted.

## Current skills

Current `SKILL.md` denominator: **37**.
Skills with at least one Phase 4 behavior row: **37/37**.
Uncovered current skills: **0**.

| MP-ID | Skill | Covered | Behavior rows | States | CTs |
|---|---|---|---|---|---|
| MP-0063 | `skills/engineering/ask-matt/SKILL.md` | YES | B-003, B-009 | CONFIRMED_DRIFT, CONFIRMED_GAP | CT-003, CT-009 |
| MP-0065 | `skills/engineering/code-review/SKILL.md` | YES | B-010, B-027 | CONFIRMED_GAP | CT-010, CT-014 |
| MP-0069 | `skills/engineering/codebase-design/SKILL.md` | YES | B-036 | CONFIRMED_MATCH | — |
| MP-0071 | `skills/engineering/diagnosing-bugs/SKILL.md` | YES | B-007, B-009, B-023 | CONFIRMED_DRIFT, CONFIRMED_MATCH | CT-007, CT-009 |
| MP-0076 | `skills/engineering/domain-modeling/SKILL.md` | YES | B-028, B-039 | CONFIRMED_MATCH | — |
| MP-0078 | `skills/engineering/grill-with-docs/SKILL.md` | YES | B-039 | CONFIRMED_MATCH | — |
| MP-0080 | `skills/engineering/implement/SKILL.md` | YES | B-010, B-033 | CONFIRMED_GAP | CT-010, CT-017 |
| MP-0083 | `skills/engineering/improve-codebase-architecture/SKILL.md` | YES | B-008 | RUNTIME_UNKNOWN | CT-008 |
| MP-0086 | `skills/engineering/prototype/SKILL.md` | YES | B-035 | RUNTIME_UNKNOWN | — |
| MP-0089 | `skills/engineering/research/SKILL.md` | YES | B-034 | CONFIRMED_MATCH | — |
| MP-0091 | `skills/engineering/resolving-merge-conflicts/SKILL.md` | YES | B-040 | CONFIRMED_MATCH | — |
| MP-0093 | `skills/engineering/setup-matt-pocock-skills/SKILL.md` | YES | B-021, B-022, B-037 | CONFIRMED_MATCH, RUNTIME_UNKNOWN | — |
| MP-0100 | `skills/engineering/tdd/SKILL.md` | YES | B-001 | CONFIRMED_DRIFT | CT-001 |
| MP-0104 | `skills/engineering/to-spec/SKILL.md` | YES | B-030 | CONFIRMED_GAP | CT-015 |
| MP-0106 | `skills/engineering/to-tickets/SKILL.md` | YES | B-030, B-031, B-032, B-033 | CONFIRMED_GAP, CONFIRMED_MATCH | CT-015, CT-016, CT-017 |
| MP-0110 | `skills/engineering/triage/SKILL.md` | YES | B-024, B-025, B-038 | CONFIRMED_GAP, CONFIRMED_MATCH, CONFIRMED_WEAKNESS | CT-018 |
| MP-0112 | `skills/engineering/wayfinder/SKILL.md` | YES | B-013 | CONFIRMED_WEAKNESS | CT-013 |
| MP-0114 | `skills/engineering/wizard/SKILL.md` | YES | B-015 | STATICALLY_ENFORCED | — |
| MP-0118 | `skills/in-progress/claude-handoff/SKILL.md` | YES | B-041 | RUNTIME_UNKNOWN | — |
| MP-0120 | `skills/in-progress/implement-spec/SKILL.md` | YES | B-026, B-027 | CONFIRMED_GAP, RUNTIME_UNKNOWN | CT-014 |
| MP-0122 | `skills/in-progress/loop-me/SKILL.md` | YES | B-042 | CONFIRMED_MATCH | — |
| MP-0124 | `skills/in-progress/retro/SKILL.md` | YES | B-011 | CONFIRMED_DRIFT | CT-011 |
| MP-0126 | `skills/in-progress/setup-ts-deep-modules/SKILL.md` | YES | B-012, B-014 | CONFIRMED_GAP, STATICALLY_ENFORCED | CT-012 |
| MP-0129 | `skills/in-progress/writing-beats/SKILL.md` | YES | B-043 | CONFIRMED_MATCH | — |
| MP-0131 | `skills/in-progress/writing-fragments/SKILL.md` | YES | B-044 | CONFIRMED_MATCH | — |
| MP-0133 | `skills/in-progress/writing-shape/SKILL.md` | YES | B-045 | CONFIRMED_MATCH | — |
| MP-0136 | `skills/misc/git-guardrails-claude-code/SKILL.md` | YES | B-016 | STATICALLY_ENFORCED | — |
| MP-0139 | `skills/misc/migrate-to-shoehorn/SKILL.md` | YES | B-046 | CONFIRMED_MATCH | CT-019 |
| MP-0141 | `skills/misc/scaffold-exercises/SKILL.md` | YES | B-047 | CONFIRMED_GAP | CT-020 |
| MP-0143 | `skills/misc/setup-pre-commit/SKILL.md` | YES | B-017 | STATICALLY_ENFORCED | — |
| MP-0146 | `skills/productivity/grill-me/SKILL.md` | YES | B-048 | CONFIRMED_MATCH | — |
| MP-0148 | `skills/productivity/grilling/SKILL.md` | YES | B-039, B-042, B-048, B-049 | CONFIRMED_MATCH | — |
| MP-0150 | `skills/productivity/handoff/SKILL.md` | YES | B-050 | RUNTIME_UNKNOWN | — |
| MP-0156 | `skills/productivity/teach/SKILL.md` | YES | B-005, B-006 | CONFIRMED_GAP, RUNTIME_UNKNOWN | CT-005, CT-006 |
| MP-0158 | `skills/productivity/to-questionnaire/SKILL.md` | YES | B-051 | CONFIRMED_MATCH | — |
| MP-0160 | `skills/productivity/wait-what/SKILL.md` | YES | B-052 | RUNTIME_UNKNOWN | — |
| MP-0163 | `skills/productivity/writing-for-agents/SKILL.md` | YES | B-053 | CONFIRMED_MATCH | — |

### Uncovered current-skill queue

- None.

## High-risk non-skill surfaces

Included categories: `ci-release`, `codex-metadata`, `dependency-lock`, `distribution`, `package-config`, `repo-executable`, `skill-executable-config`, `skill-support`.

Surface denominator: **71**.
Surfaces with at least one Phase 4 behavior row: **71/71**.
Uncovered high-risk surfaces: **0**.

| MP-ID | Category | Surface | Covered | Behavior rows | CTs |
|---|---|---|---|---|---|
| MP-0017 | distribution | `.claude-plugin/marketplace.json` | YES | B-055 | — |
| MP-0018 | distribution | `.claude-plugin/plugin.json` | YES | B-002, B-004, B-018 | CT-002, CT-004 |
| MP-0019 | ci-release | `.github/workflows/release.yml` | YES | B-004, B-018, B-029 | CT-004 |
| MP-0055 | dependency-lock | `package-lock.json` | YES | B-004 | CT-004 |
| MP-0056 | package-config | `package.json` | YES | B-004, B-018, B-029 | CT-004 |
| MP-0057 | repo-executable | `scripts/link-skills.sh` | YES | B-019 | — |
| MP-0058 | repo-executable | `scripts/list-skills.sh` | YES | B-020 | — |
| MP-0059 | repo-executable | `scripts/sync-plugin-version.mjs` | YES | B-004, B-018, B-029 | CT-004 |
| MP-0062 | skill-support | `skills/engineering/ask-matt/PHASE-BOUNDARIES.md` | YES | B-057 | — |
| MP-0064 | codex-metadata | `skills/engineering/ask-matt/agents/openai.yaml` | YES | B-054 | — |
| MP-0066 | codex-metadata | `skills/engineering/code-review/agents/openai.yaml` | YES | B-054 | — |
| MP-0067 | skill-support | `skills/engineering/codebase-design/DEEPENING.md` | YES | B-036 | — |
| MP-0068 | skill-support | `skills/engineering/codebase-design/DESIGN-IT-TWICE.md` | YES | B-036 | — |
| MP-0070 | codex-metadata | `skills/engineering/codebase-design/agents/openai.yaml` | YES | B-054 | — |
| MP-0072 | codex-metadata | `skills/engineering/diagnosing-bugs/agents/openai.yaml` | YES | B-054 | — |
| MP-0073 | skill-executable-config | `skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh` | YES | B-056 | — |
| MP-0074 | skill-support | `skills/engineering/domain-modeling/ADR-FORMAT.md` | YES | B-028 | — |
| MP-0075 | skill-support | `skills/engineering/domain-modeling/CONTEXT-FORMAT.md` | YES | B-028 | — |
| MP-0077 | codex-metadata | `skills/engineering/domain-modeling/agents/openai.yaml` | YES | B-054 | — |
| MP-0079 | codex-metadata | `skills/engineering/grill-with-docs/agents/openai.yaml` | YES | B-054 | — |
| MP-0081 | codex-metadata | `skills/engineering/implement/agents/openai.yaml` | YES | B-054 | — |
| MP-0082 | skill-support | `skills/engineering/improve-codebase-architecture/HTML-REPORT.md` | YES | B-008 | CT-008 |
| MP-0084 | codex-metadata | `skills/engineering/improve-codebase-architecture/agents/openai.yaml` | YES | B-054 | — |
| MP-0085 | skill-support | `skills/engineering/prototype/LOGIC.md` | YES | B-035 | — |
| MP-0087 | skill-support | `skills/engineering/prototype/UI.md` | YES | B-035 | — |
| MP-0088 | codex-metadata | `skills/engineering/prototype/agents/openai.yaml` | YES | B-054 | — |
| MP-0090 | codex-metadata | `skills/engineering/research/agents/openai.yaml` | YES | B-054 | — |
| MP-0092 | codex-metadata | `skills/engineering/resolving-merge-conflicts/agents/openai.yaml` | YES | B-054 | — |
| MP-0094 | codex-metadata | `skills/engineering/setup-matt-pocock-skills/agents/openai.yaml` | YES | B-054 | — |
| MP-0095 | skill-support | `skills/engineering/setup-matt-pocock-skills/domain.md` | YES | B-058 | — |
| MP-0096 | skill-support | `skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md` | YES | B-037 | — |
| MP-0097 | skill-support | `skills/engineering/setup-matt-pocock-skills/issue-tracker-gitlab.md` | YES | B-037 | — |
| MP-0098 | skill-support | `skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md` | YES | B-059 | — |
| MP-0099 | skill-support | `skills/engineering/setup-matt-pocock-skills/triage-labels.md` | YES | B-024, B-037 | — |
| MP-0101 | codex-metadata | `skills/engineering/tdd/agents/openai.yaml` | YES | B-001, B-054 | CT-001 |
| MP-0102 | skill-support | `skills/engineering/tdd/mocking.md` | YES | B-060 | — |
| MP-0103 | skill-support | `skills/engineering/tdd/tests.md` | YES | B-061 | — |
| MP-0105 | codex-metadata | `skills/engineering/to-spec/agents/openai.yaml` | YES | B-054 | — |
| MP-0107 | codex-metadata | `skills/engineering/to-tickets/agents/openai.yaml` | YES | B-054 | — |
| MP-0108 | skill-support | `skills/engineering/triage/AGENT-BRIEF.md` | YES | B-038 | CT-018 |
| MP-0109 | skill-support | `skills/engineering/triage/OUT-OF-SCOPE.md` | YES | B-062 | — |
| MP-0111 | codex-metadata | `skills/engineering/triage/agents/openai.yaml` | YES | B-054 | — |
| MP-0113 | codex-metadata | `skills/engineering/wayfinder/agents/openai.yaml` | YES | B-054 | — |
| MP-0115 | codex-metadata | `skills/engineering/wizard/agents/openai.yaml` | YES | B-054 | — |
| MP-0116 | skill-executable-config | `skills/engineering/wizard/template.sh` | YES | B-015 | — |
| MP-0119 | codex-metadata | `skills/in-progress/claude-handoff/agents/openai.yaml` | YES | B-054 | — |
| MP-0121 | codex-metadata | `skills/in-progress/implement-spec/agents/openai.yaml` | YES | B-054 | — |
| MP-0123 | codex-metadata | `skills/in-progress/loop-me/agents/openai.yaml` | YES | B-054 | — |
| MP-0125 | codex-metadata | `skills/in-progress/retro/agents/openai.yaml` | YES | B-054 | — |
| MP-0127 | codex-metadata | `skills/in-progress/setup-ts-deep-modules/agents/openai.yaml` | YES | B-054 | — |
| MP-0128 | skill-executable-config | `skills/in-progress/setup-ts-deep-modules/dependency-cruiser.config.cjs` | YES | B-012, B-014 | CT-012 |
| MP-0130 | codex-metadata | `skills/in-progress/writing-beats/agents/openai.yaml` | YES | B-054 | — |
| MP-0132 | codex-metadata | `skills/in-progress/writing-fragments/agents/openai.yaml` | YES | B-054 | — |
| MP-0134 | codex-metadata | `skills/in-progress/writing-shape/agents/openai.yaml` | YES | B-054 | — |
| MP-0137 | codex-metadata | `skills/misc/git-guardrails-claude-code/agents/openai.yaml` | YES | B-054 | — |
| MP-0138 | skill-executable-config | `skills/misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh` | YES | B-016 | — |
| MP-0140 | codex-metadata | `skills/misc/migrate-to-shoehorn/agents/openai.yaml` | YES | B-054 | — |
| MP-0142 | codex-metadata | `skills/misc/scaffold-exercises/agents/openai.yaml` | YES | B-054 | — |
| MP-0144 | codex-metadata | `skills/misc/setup-pre-commit/agents/openai.yaml` | YES | B-054 | — |
| MP-0147 | codex-metadata | `skills/productivity/grill-me/agents/openai.yaml` | YES | B-054 | — |
| MP-0149 | codex-metadata | `skills/productivity/grilling/agents/openai.yaml` | YES | B-054 | — |
| MP-0151 | codex-metadata | `skills/productivity/handoff/agents/openai.yaml` | YES | B-054 | — |
| MP-0152 | skill-support | `skills/productivity/teach/GLOSSARY-FORMAT.md` | YES | B-005 | CT-005 |
| MP-0153 | skill-support | `skills/productivity/teach/LEARNING-RECORD-FORMAT.md` | YES | B-063 | — |
| MP-0154 | skill-support | `skills/productivity/teach/MISSION-FORMAT.md` | YES | B-064 | — |
| MP-0155 | skill-support | `skills/productivity/teach/RESOURCES-FORMAT.md` | YES | B-065 | — |
| MP-0157 | codex-metadata | `skills/productivity/teach/agents/openai.yaml` | YES | B-054 | — |
| MP-0159 | codex-metadata | `skills/productivity/to-questionnaire/agents/openai.yaml` | YES | B-054 | — |
| MP-0161 | codex-metadata | `skills/productivity/wait-what/agents/openai.yaml` | YES | B-054 | — |
| MP-0162 | skill-support | `skills/productivity/writing-for-agents/SKILL-MECHANICS.md` | YES | B-053 | — |
| MP-0164 | codex-metadata | `skills/productivity/writing-for-agents/agents/openai.yaml` | YES | B-054 | — |

### Uncovered high-risk surface queue

- None.

Hard errors: **0**.

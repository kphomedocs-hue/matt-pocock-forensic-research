# Phase 3 Per-File Closure Index

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

This index applies the mechanical parts of the canonical `CONNECTIONS TRACED` gate. **READY_CANDIDATE is not a status promotion.** Notes remain READ until the candidate is explicitly promoted with durable evidence.

Files: **164**. READY_CANDIDATE: **159**. BLOCKED: **5**.

Files with zero incoming graph edges: **77**. Zero incoming is not treated as proof of orphan; conventional structural roles close some cases, and the rest require semantic orphan review.

## Blocker summary

| Blocker | Files |
|---|---:|
| SEMANTIC_ORPHAN_REVIEW | 5 |

## Per-file state

| MP-ID | Path | Incoming | Outgoing | Orphan evaluation | Gate state | Blockers |
|---|---|---:|---:|---|---|---|
| MP-0001 | `.agents/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md` | 0 | 0 | ZERO_INCOMING_REQUIRES_SEMANTIC_ORPHAN_REVIEW | BLOCKED | SEMANTIC_ORPHAN_REVIEW |
| MP-0002 | `.agents/adr/0002-ship-as-a-claude-code-plugin.md` | 3 | 6 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0003 | `.agents/install-block.md` | 3 | 3 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0004 | `.agents/invocation.md` | 4 | 2 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0005 | `.agents/writing-docs.md` | 2 | 4 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0006 | `.changeset/README.md` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CHANGESETS_INPUT_OR_GUIDE | READY_CANDIDATE | — |
| MP-0007 | `.changeset/add-implement-spec-skill.md` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CHANGESETS_INPUT_OR_GUIDE | READY_CANDIDATE | — |
| MP-0008 | `.changeset/config.json` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CHANGESETS_CONFIG | READY_CANDIDATE | — |
| MP-0009 | `.changeset/domain-modeling-trigger-context-adr.md` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CHANGESETS_INPUT_OR_GUIDE | READY_CANDIDATE | — |
| MP-0010 | `.changeset/fix-yaml-frontmatter-colons.md` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CHANGESETS_INPUT_OR_GUIDE | READY_CANDIDATE | — |
| MP-0011 | `.changeset/grilling-add-hr-between-questions.md` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CHANGESETS_INPUT_OR_GUIDE | READY_CANDIDATE | — |
| MP-0012 | `.changeset/grilling-remove-em-dashes.md` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CHANGESETS_INPUT_OR_GUIDE | READY_CANDIDATE | — |
| MP-0013 | `.changeset/remove-em-dashes-repo-wide.md` | 0 | 3 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CHANGESETS_INPUT_OR_GUIDE | READY_CANDIDATE | — |
| MP-0014 | `.changeset/skill-tool-invocation-terminology.md` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CHANGESETS_INPUT_OR_GUIDE | READY_CANDIDATE | — |
| MP-0015 | `.changeset/user-invoked-skill-invocation.md` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CHANGESETS_INPUT_OR_GUIDE | READY_CANDIDATE | — |
| MP-0016 | `.changeset/wait-what-context-map.md` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CHANGESETS_INPUT_OR_GUIDE | READY_CANDIDATE | — |
| MP-0017 | `.claude-plugin/marketplace.json` | 3 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0018 | `.claude-plugin/plugin.json` | 5 | 25 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0019 | `.github/workflows/release.yml` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:GITHUB_ACTIONS_ENTRYPOINT | READY_CANDIDATE | — |
| MP-0020 | `.gitignore` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:GIT_CONFIGURATION | READY_CANDIDATE | — |
| MP-0021 | `.out-of-scope/mainstream-issue-trackers-only.md` | 0 | 0 | ZERO_INCOMING_REQUIRES_SEMANTIC_ORPHAN_REVIEW | BLOCKED | SEMANTIC_ORPHAN_REVIEW |
| MP-0022 | `.out-of-scope/question-limits.md` | 0 | 0 | ZERO_INCOMING_REQUIRES_SEMANTIC_ORPHAN_REVIEW | BLOCKED | SEMANTIC_ORPHAN_REVIEW |
| MP-0023 | `.out-of-scope/setup-skill-verify-mode.md` | 0 | 0 | ZERO_INCOMING_REQUIRES_SEMANTIC_ORPHAN_REVIEW | BLOCKED | SEMANTIC_ORPHAN_REVIEW |
| MP-0024 | `AGENTS.md` | 14 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0025 | `CHANGELOG.md` | 2 | 23 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0026 | `CLAUDE.md` | 19 | 10 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0027 | `CONTEXT.md` | 30 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0028 | `LICENSE` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0029 | `README.md` | 6 | 29 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0030 | `docs/engineering/ask-matt.md` | 0 | 3 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0031 | `docs/engineering/code-review.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0032 | `docs/engineering/codebase-design.md` | 0 | 2 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0033 | `docs/engineering/diagnosing-bugs.md` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0034 | `docs/engineering/domain-modeling.md` | 0 | 2 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0035 | `docs/engineering/grill-with-docs.md` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0036 | `docs/engineering/implement.md` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0037 | `docs/engineering/improve-codebase-architecture.md` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0038 | `docs/engineering/prototype.md` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0039 | `docs/engineering/research.md` | 1 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0040 | `docs/engineering/resolving-merge-conflicts.md` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0041 | `docs/engineering/setup-matt-pocock-skills.md` | 0 | 5 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0042 | `docs/engineering/tdd.md` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0043 | `docs/engineering/to-spec.md` | 1 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0044 | `docs/engineering/to-tickets.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0045 | `docs/engineering/triage.md` | 0 | 2 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0046 | `docs/engineering/wayfinder.md` | 1 | 2 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0047 | `docs/engineering/wizard.md` | 1 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0048 | `docs/productivity/grill-me.md` | 0 | 2 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0049 | `docs/productivity/grilling.md` | 0 | 3 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0050 | `docs/productivity/handoff.md` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0051 | `docs/productivity/teach.md` | 0 | 2 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0052 | `docs/productivity/to-questionnaire.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0053 | `docs/productivity/wait-what.md` | 0 | 2 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0054 | `docs/productivity/writing-for-agents.md` | 0 | 4 | NON_ORPHAN_BY_STRUCTURAL_ROLE:PROMOTED_HUMAN_DOC_PAGE | READY_CANDIDATE | — |
| MP-0055 | `package-lock.json` | 1 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0056 | `package.json` | 6 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0057 | `scripts/link-skills.sh` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0058 | `scripts/list-skills.sh` | 0 | 0 | ZERO_INCOMING_REQUIRES_SEMANTIC_ORPHAN_REVIEW | BLOCKED | SEMANTIC_ORPHAN_REVIEW |
| MP-0059 | `scripts/sync-plugin-version.mjs` | 1 | 2 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0060 | `skills/deprecated/README.md` | 0 | 0 | NON_ORPHAN_BY_STRUCTURAL_ROLE:BUCKET_SKILL_CATALOG | READY_CANDIDATE | — |
| MP-0061 | `skills/engineering/README.md` | 0 | 19 | NON_ORPHAN_BY_STRUCTURAL_ROLE:BUCKET_SKILL_CATALOG | READY_CANDIDATE | — |
| MP-0062 | `skills/engineering/ask-matt/PHASE-BOUNDARIES.md` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0063 | `skills/engineering/ask-matt/SKILL.md` | 5 | 3 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0064 | `skills/engineering/ask-matt/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0065 | `skills/engineering/code-review/SKILL.md` | 4 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0066 | `skills/engineering/code-review/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0067 | `skills/engineering/codebase-design/DEEPENING.md` | 3 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0068 | `skills/engineering/codebase-design/DESIGN-IT-TWICE.md` | 3 | 3 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0069 | `skills/engineering/codebase-design/SKILL.md` | 9 | 2 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0070 | `skills/engineering/codebase-design/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0071 | `skills/engineering/diagnosing-bugs/SKILL.md` | 4 | 2 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0072 | `skills/engineering/diagnosing-bugs/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0073 | `skills/engineering/diagnosing-bugs/scripts/hitl-loop.template.sh` | 3 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0074 | `skills/engineering/domain-modeling/ADR-FORMAT.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0075 | `skills/engineering/domain-modeling/CONTEXT-FORMAT.md` | 1 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0076 | `skills/engineering/domain-modeling/SKILL.md` | 8 | 3 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0077 | `skills/engineering/domain-modeling/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0078 | `skills/engineering/grill-with-docs/SKILL.md` | 4 | 2 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0079 | `skills/engineering/grill-with-docs/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0080 | `skills/engineering/implement/SKILL.md` | 4 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0081 | `skills/engineering/implement/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0082 | `skills/engineering/improve-codebase-architecture/HTML-REPORT.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0083 | `skills/engineering/improve-codebase-architecture/SKILL.md` | 4 | 5 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0084 | `skills/engineering/improve-codebase-architecture/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0085 | `skills/engineering/prototype/LOGIC.md` | 2 | 2 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0086 | `skills/engineering/prototype/SKILL.md` | 7 | 2 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0087 | `skills/engineering/prototype/UI.md` | 2 | 2 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0088 | `skills/engineering/prototype/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0089 | `skills/engineering/research/SKILL.md` | 5 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0090 | `skills/engineering/research/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0091 | `skills/engineering/resolving-merge-conflicts/SKILL.md` | 4 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0092 | `skills/engineering/resolving-merge-conflicts/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0093 | `skills/engineering/setup-matt-pocock-skills/SKILL.md` | 4 | 9 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0094 | `skills/engineering/setup-matt-pocock-skills/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0095 | `skills/engineering/setup-matt-pocock-skills/domain.md` | 3 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0096 | `skills/engineering/setup-matt-pocock-skills/issue-tracker-github.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0097 | `skills/engineering/setup-matt-pocock-skills/issue-tracker-gitlab.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0098 | `skills/engineering/setup-matt-pocock-skills/issue-tracker-local.md` | 1 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0099 | `skills/engineering/setup-matt-pocock-skills/triage-labels.md` | 6 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0100 | `skills/engineering/tdd/SKILL.md` | 4 | 4 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0101 | `skills/engineering/tdd/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0102 | `skills/engineering/tdd/mocking.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0103 | `skills/engineering/tdd/tests.md` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0104 | `skills/engineering/to-spec/SKILL.md` | 4 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0105 | `skills/engineering/to-spec/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0106 | `skills/engineering/to-tickets/SKILL.md` | 4 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0107 | `skills/engineering/to-tickets/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0108 | `skills/engineering/triage/AGENT-BRIEF.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0109 | `skills/engineering/triage/OUT-OF-SCOPE.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0110 | `skills/engineering/triage/SKILL.md` | 4 | 5 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0111 | `skills/engineering/triage/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0112 | `skills/engineering/wayfinder/SKILL.md` | 4 | 4 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0113 | `skills/engineering/wayfinder/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0114 | `skills/engineering/wizard/SKILL.md` | 4 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0115 | `skills/engineering/wizard/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0116 | `skills/engineering/wizard/template.sh` | 4 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0117 | `skills/in-progress/README.md` | 0 | 8 | NON_ORPHAN_BY_STRUCTURAL_ROLE:BUCKET_SKILL_CATALOG | READY_CANDIDATE | — |
| MP-0118 | `skills/in-progress/claude-handoff/SKILL.md` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0119 | `skills/in-progress/claude-handoff/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0120 | `skills/in-progress/implement-spec/SKILL.md` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0121 | `skills/in-progress/implement-spec/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0122 | `skills/in-progress/loop-me/SKILL.md` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0123 | `skills/in-progress/loop-me/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0124 | `skills/in-progress/retro/SKILL.md` | 2 | 3 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0125 | `skills/in-progress/retro/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0126 | `skills/in-progress/setup-ts-deep-modules/SKILL.md` | 2 | 5 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0127 | `skills/in-progress/setup-ts-deep-modules/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0128 | `skills/in-progress/setup-ts-deep-modules/dependency-cruiser.config.cjs` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0129 | `skills/in-progress/writing-beats/SKILL.md` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0130 | `skills/in-progress/writing-beats/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0131 | `skills/in-progress/writing-fragments/SKILL.md` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0132 | `skills/in-progress/writing-fragments/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0133 | `skills/in-progress/writing-shape/SKILL.md` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0134 | `skills/in-progress/writing-shape/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0135 | `skills/misc/README.md` | 0 | 4 | NON_ORPHAN_BY_STRUCTURAL_ROLE:BUCKET_SKILL_CATALOG | READY_CANDIDATE | — |
| MP-0136 | `skills/misc/git-guardrails-claude-code/SKILL.md` | 2 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0137 | `skills/misc/git-guardrails-claude-code/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0138 | `skills/misc/git-guardrails-claude-code/scripts/block-dangerous-git.sh` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0139 | `skills/misc/migrate-to-shoehorn/SKILL.md` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0140 | `skills/misc/migrate-to-shoehorn/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0141 | `skills/misc/scaffold-exercises/SKILL.md` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0142 | `skills/misc/scaffold-exercises/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0143 | `skills/misc/setup-pre-commit/SKILL.md` | 2 | 2 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0144 | `skills/misc/setup-pre-commit/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0145 | `skills/productivity/README.md` | 1 | 10 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0146 | `skills/productivity/grill-me/SKILL.md` | 4 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0147 | `skills/productivity/grill-me/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0148 | `skills/productivity/grilling/SKILL.md` | 9 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0149 | `skills/productivity/grilling/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0150 | `skills/productivity/handoff/SKILL.md` | 4 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0151 | `skills/productivity/handoff/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0152 | `skills/productivity/teach/GLOSSARY-FORMAT.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0153 | `skills/productivity/teach/LEARNING-RECORD-FORMAT.md` | 1 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0154 | `skills/productivity/teach/MISSION-FORMAT.md` | 2 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0155 | `skills/productivity/teach/RESOURCES-FORMAT.md` | 1 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0156 | `skills/productivity/teach/SKILL.md` | 5 | 3 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0157 | `skills/productivity/teach/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0158 | `skills/productivity/to-questionnaire/SKILL.md` | 4 | 0 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0159 | `skills/productivity/to-questionnaire/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0160 | `skills/productivity/wait-what/SKILL.md` | 4 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0161 | `skills/productivity/wait-what/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |
| MP-0162 | `skills/productivity/writing-for-agents/SKILL-MECHANICS.md` | 3 | 1 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0163 | `skills/productivity/writing-for-agents/SKILL.md` | 6 | 4 | NON_ORPHAN_BY_INCOMING_EDGE | READY_CANDIDATE | — |
| MP-0164 | `skills/productivity/writing-for-agents/agents/openai.yaml` | 0 | 1 | NON_ORPHAN_BY_STRUCTURAL_ROLE:CODEX_METADATA_CONVENTION | READY_CANDIDATE | — |

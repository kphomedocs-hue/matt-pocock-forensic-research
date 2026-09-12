# Connection Graph

Phase 3 artifact for exhaustive internal relationship mapping at frozen commit `3cca18b368ae95cdbdebbff572ccafa662551015`.

## Edge schema

Each edge is typed. Current allowed types:

- `OPERATIVE_CALL` — source instructs the running agent to invoke/use another skill or executable behavior.
- `PASSIVE_REFERENCE` — source names another internal artifact without requiring invocation.
- `DOC_LINK` — explicit relative/internal documentation link.
- `DISTRIBUTION_ENTRY` — manifest/installer/linker exposes a skill or artifact to an installation path.
- `CONFIG_BINDING` — metadata/config binds behavior, invocation policy, release/versioning, or runtime wiring.
- `HISTORY_REFERENCE` — history/changeset/changelog records a semantic change to another artifact.
- `SYMLINK` — physical symlink relationship.

Inferred relationships must be marked `INFERRED` and kept separate from source-explicit edges.

A file is not `CONNECTIONS TRACED` until its outgoing edges and all discovered incoming edges are reconciled against the full 164-file frozen census.

## Confirmed explicit edges — initial set

| Edge ID | From | Type | To | Evidence / meaning | Status |
|---|---|---|---|---|---|
| EG-0001 | MP-0001 `.agents/install-block.md` | PASSIVE_REFERENCE | `.claude-plugin/plugin.json` / skills.sh install path | Install instructions distinguish plugin vs skills.sh and warn against installing both. | CONFIRMED |
| EG-0002 | MP-0002 `.agents/invocation.md` | CONFIG_BINDING | user-invoked/model-invoked skill classes | Governs when Skill-tool calls are valid versus when the human must invoke the target. | CONFIRMED |
| EG-0003 | MP-0003 ADR-0001 | PASSIVE_REFERENCE | `to-tickets`, `to-spec`, `triage`, `diagnosing-bugs`, `tdd`, `improve-codebase-architecture` | Records hard/soft setup dependency decisions. | CONFIRMED |
| EG-0004 | MP-0004 ADR-0002 | DISTRIBUTION_ENTRY | Claude plugin / skills.sh / Codex strategy | Defines accepted plugin path, universal installer role, and deferred Codex native plugin path. | CONFIRMED |
| EG-0005 | MP-0018 `.claude-plugin/plugin.json` | DISTRIBUTION_ENTRY | 25 promoted skill directories | Plugin manifest explicitly enumerates the promoted skill set. | CONFIRMED |
| EG-0006 | MP-0017 `.claude-plugin/marketplace.json` | DISTRIBUTION_ENTRY | local plugin source `./` | Marketplace exposes one plugin rooted at the repository. | CONFIRMED |
| EG-0007 | MP-0059 `scripts/sync-plugin-version.mjs` | CONFIG_BINDING | `package.json` → `.claude-plugin/plugin.json` | Package version is copied into plugin manifest; `--check` verifies equality. | CONFIRMED |
| EG-0008 | MP-0057 `scripts/link-skills.sh` | DISTRIBUTION_ENTRY | engineering + productivity + in-progress SKILL directories | Maintainer local-link path excludes deprecated and misc, links to Claude/Codex skill dirs. | CONFIRMED |
| EG-0009 | MP-0058 `scripts/list-skills.sh` | DISTRIBUTION_ENTRY | every `SKILL.md` except node_modules | Listing universe is broader than promoted/local-link universes. | CONFIRMED |
| EG-0010 | MP-0027 `AGENTS.md` | SYMLINK | MP-0026 `CLAUDE.md` | Physical symlink blob contains `CLAUDE.md`. | CONFIRMED |
| EG-0011 | MP-0063 `ask-matt/SKILL.md` | DOC_LINK | MP-0062 `PHASE-BOUNDARIES.md` | Router explicitly links the phase-boundary decision tree. | CONFIRMED |
| EG-0012 | MP-0063 `ask-matt/SKILL.md` | PASSIVE_REFERENCE | all other promoted skills | Router names the full promoted workflow/skill universe as secondary summaries. | CONFIRMED; expand to per-target edges |
| EG-0013 | MP-0078 `grill-with-docs/SKILL.md` | OPERATIVE_CALL | MP-0148 `grilling/SKILL.md` | Explicitly calls the Skill tool for `grilling`. | CONFIRMED |
| EG-0014 | MP-0078 `grill-with-docs/SKILL.md` | OPERATIVE_CALL | MP-0076 `domain-modeling/SKILL.md` | Explicitly calls the Skill tool for `domain-modeling`. | CONFIRMED |
| EG-0015 | MP-0146 `grill-me/SKILL.md` | OPERATIVE_CALL | MP-0148 `grilling/SKILL.md` | Thin wrapper whose only behavior is calling `grilling`. | CONFIRMED |
| EG-0016 | MP-0083 `improve-codebase-architecture/SKILL.md` | OPERATIVE_CALL | MP-0069 `codebase-design/SKILL.md` | Loads architecture vocabulary/reference. | CONFIRMED |
| EG-0017 | MP-0083 `improve-codebase-architecture/SKILL.md` | OPERATIVE_CALL | MP-0148 `grilling/SKILL.md` | Starts the candidate grilling loop after selection. | CONFIRMED |
| EG-0018 | MP-0083 `improve-codebase-architecture/SKILL.md` | OPERATIVE_CALL | MP-0076 `domain-modeling/SKILL.md` | Updates glossary/ADRs as decisions crystallize. | CONFIRMED |
| EG-0019 | MP-0100 `tdd/SKILL.md` | OPERATIVE_CALL | MP-0069 `codebase-design/SKILL.md` | Calls reference when seam/interface shape is in question. | CONFIRMED |
| EG-0020 | MP-0110 `triage/SKILL.md` | OPERATIVE_CALL | MP-0148 `grilling/SKILL.md` | Calls grilling when issue/request needs fleshing out. | CONFIRMED |
| EG-0021 | MP-0110 `triage/SKILL.md` | OPERATIVE_CALL | MP-0076 `domain-modeling/SKILL.md` | Calls domain-modeling alongside grilling. | CONFIRMED |
| EG-0022 | MP-0112 `wayfinder/SKILL.md` | OPERATIVE_CALL | MP-0148 `grilling/SKILL.md` | Used to name destination and resolve grilling tickets. | CONFIRMED |
| EG-0023 | MP-0112 `wayfinder/SKILL.md` | OPERATIVE_CALL | MP-0076 `domain-modeling/SKILL.md` | Paired with grilling for destination/domain decisions. | CONFIRMED |
| EG-0024 | MP-0112 `wayfinder/SKILL.md` | OPERATIVE_CALL | MP-0089 `research/SKILL.md` | Research tickets dispatch research subagents. | CONFIRMED |
| EG-0025 | MP-0112 `wayfinder/SKILL.md` | OPERATIVE_CALL | MP-0086 `prototype/SKILL.md` | Prototype ticket type explicitly calls prototype. | CONFIRMED |
| EG-0026 | MP-0124 `retro/SKILL.md` | OPERATIVE_CALL | MP-0163 `writing-for-agents/SKILL.md` | Retrospective first loads agent-writing guidance. | CONFIRMED |
| EG-0027 | MP-0126 `setup-ts-deep-modules/SKILL.md` | OPERATIVE_CALL | MP-0069 `codebase-design/SKILL.md` | Uses deep-module vocabulary as shared reference. | CONFIRMED |
| EG-0028 | MP-0163 `writing-for-agents/SKILL.md` | DOC_LINK | MP-0162 `SKILL-MECHANICS.md` | Skill-specific mechanics disclosed behind an explicit pointer. | CONFIRMED |
| EG-0029 | MP-0069 `codebase-design/SKILL.md` | DOC_LINK | MP-0067 `DEEPENING.md` | Deepening dependency/testing guidance is progressive-disclosure support. | CONFIRMED |
| EG-0030 | MP-0069 `codebase-design/SKILL.md` | DOC_LINK | MP-0068 `DESIGN-IT-TWICE.md` | Alternative-interface workflow is progressive-disclosure support. | CONFIRMED |
| EG-0031 | MP-0086 `prototype/SKILL.md` | DOC_LINK | MP-0085 `LOGIC.md` | Logic/state prototype branch. | CONFIRMED |
| EG-0032 | MP-0086 `prototype/SKILL.md` | DOC_LINK | MP-0087 `UI.md` | UI prototype branch. | CONFIRMED |
| EG-0033 | MP-0093 `setup-matt-pocock-skills/SKILL.md` | DOC_LINK | MP-0095/0096/0097/0098/0099 support templates | Setup writes generated repo config using these seed templates. | CONFIRMED; expand per-file |
| EG-0034 | MP-0110 `triage/SKILL.md` | DOC_LINK | MP-0108 `AGENT-BRIEF.md` | Agent-ready brief format/reference. | CONFIRMED |
| EG-0035 | MP-0110 `triage/SKILL.md` | DOC_LINK | MP-0109 `OUT-OF-SCOPE.md` | Persistent rejected-feature knowledge-base behavior. | CONFIRMED |
| EG-0036 | MP-0156 `teach/SKILL.md` | DOC_LINK | MP-0154 `MISSION-FORMAT.md` | Mission workspace format. | CONFIRMED |
| EG-0037 | MP-0156 `teach/SKILL.md` | DOC_LINK | MP-0155 `RESOURCES-FORMAT.md` | Curated resource format. | CONFIRMED |
| EG-0038 | MP-0156 `teach/SKILL.md` | DOC_LINK | MP-0153 `LEARNING-RECORD-FORMAT.md` | Durable learning-record format. | CONFIRMED |

## High-priority missing/negative-edge checks

These are not absence claims yet; they are explicit Phase 3 checks:

1. Does anything in the frozen tree directly reference MP-0152 `GLOSSARY-FORMAT.md`? If exhaustive census-based scan says no, CT-005 can become a confirmed orphan support file.
2. Expand ask-matt's aggregate router edge into exact per-target edges and compare the 24 named targets against plugin/promoted census.
3. Join every `OPERATIVE_CALL` target against invocation metadata; flag any current call to a user-invoked target.
4. Resolve every relative Markdown link across all 164 blobs and record broken/internal/external status.
5. Build exact incoming-edge lists for support files (`DEEPENING`, `DESIGN-IT-TWICE`, prototype branches, setup templates, TDD support, triage support, Teach formats).
6. Map every `agents/openai.yaml` to its owning SKILL and compare invocation policy to Claude frontmatter.
7. Map plugin entries, link-skills set, list-skills set, docs pages, README/router visibility, and Codex metadata into one distribution matrix.
8. Treat external URLs/CLIs as external boundaries, not recursively audited source trees unless needed to validate a repository claim.

## Promotion rule

No MP row is promoted to `CONNECTIONS TRACED` merely because one or more edges are known. Promotion requires:

- all explicit outgoing internal references classified;
- all incoming internal references reconciled against the full frozen census;
- relative links resolved;
- operative calls checked against invocation class;
- unresolved or inferred relationships recorded explicitly.

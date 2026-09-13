# Phase 3 Connection Reconciliation

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

This artifact records semantic review of machine-extracted references and targeted reconciliation of important connection questions. Raw extractor output remains preserved in `03_CONNECTION_EDGES.json` / `03_CONNECTION_INDEX.md` so machine evidence stays auditable.

## Batch 01 — five unresolved internal-looking references

| Source | Raw target | Extractor candidate | Resolution | Classification |
|---|---|---|---|---|
| `skills/engineering/domain-modeling/CONTEXT-FORMAT.md` | `./src/ordering/CONTEXT.md` | `skills/engineering/domain-modeling/src/ordering/CONTEXT.md` | Example path inside the **consumer repo structure** shown by the CONTEXT template; it is not intended to exist inside `mattpocock/skills`. | GENERATED/TEMPLATE TARGET — NOT BROKEN |
| `skills/engineering/domain-modeling/CONTEXT-FORMAT.md` | `./src/billing/CONTEXT.md` | `skills/engineering/domain-modeling/src/billing/CONTEXT.md` | Example path inside the **consumer repo structure** shown by the CONTEXT template; it is not intended to exist inside `mattpocock/skills`. | GENERATED/TEMPLATE TARGET — NOT BROKEN |
| `skills/engineering/domain-modeling/CONTEXT-FORMAT.md` | `./src/fulfillment/CONTEXT.md` | `skills/engineering/domain-modeling/src/fulfillment/CONTEXT.md` | Example path inside the **consumer repo structure** shown by the CONTEXT template; it is not intended to exist inside `mattpocock/skills`. | GENERATED/TEMPLATE TARGET — NOT BROKEN |
| `skills/engineering/wayfinder/SKILL.md` | `link` | `skills/engineering/wayfinder/link` | Literal placeholder in the map-body Markdown template (`[<closed ticket title>](link)`), not a repository file reference. | TEMPLATE PLACEHOLDER — NOT BROKEN |
| `skills/in-progress/setup-ts-deep-modules/SKILL.md` | `./src/packages/README.md` | `skills/in-progress/setup-ts-deep-modules/src/packages/README.md` | Example **consumer-repo context pointer** that the skill instructs the agent to create after generating the packages README. | GENERATED TARGET — NOT BROKEN |

### Batch 01 result

- Machine-extracted unresolved internal-looking references: **5**
- Semantically reconciled: **5/5**
- Confirmed broken repository links from this queue: **0**
- Remaining unresolved from this extraction queue: **0**

## Batch 02 — exhaustive literal passive-reference expansion

Extraction rules version 2 added two deterministic scans across all 164 already-frozen blob texts:

1. exact repository-relative path mentions;
2. exact filename mentions only when the basename is globally unique across the 164-file census.

The weaker `PASSIVE_REFERENCE` edge is not added when the same source→target pair already has a stronger explicit/structural edge.

### Machine result

- `PASSIVE_REFERENCE` edges: **123**
- Exact-path passive mentions: **104**
- Unique-filename passive mentions: **19**
- Globally unique basenames eligible for the filename scan: **83**
- Raw unresolved internal-looking references remain: **5**, unchanged from Batch 01 and already semantically reconciled there.

### CT-005 / Teach glossary result

`skills/productivity/teach/GLOSSARY-FORMAT.md` (MP-0152) has **1 incoming reference**, overturning the stronger source-tree-orphan hypothesis.

The incoming literal reference is from frozen human documentation `docs/productivity/teach.md` (MP-0051), which explicitly states that the skill ships `GLOSSARY-FORMAT.md` but `SKILL.md` no longer links to it. Frozen operative `skills/productivity/teach/SKILL.md` (MP-0156) still has no reference to that support file.

Therefore:

- **repository orphan:** NO — disproved by exhaustive literal scan;
- **operative Teach linkage:** MISSING;
- **current classification:** operative linkage gap / documented stale support behavior;
- **CT-005:** remains OPEN, but its orphan question is resolved.

## Batch 03 — operative-call semantics and invocation-policy join

Extraction rules version 3 corrected an over-broad earlier rule: a line mentioning the `Skill tool` is an `OPERATIVE_CALL` only when it occurs in a current `SKILL.md`. Mentions in governance docs, changesets, human docs, or history are references about behavior, not executable workflow dependencies.

This correction reduced machine-labeled operative calls from **37** to **15** without removing literal/passive evidence.

Every one of the 37 current skills was then joined against both harness policies:

- Claude: `disable-model-invocation: true` means `USER_INVOKED`; omission means `MODEL_INVOKED`.
- Codex: `policy.allow_implicit_invocation: false` means `USER_INVOKED`; omission means `MODEL_INVOKED`.

### Machine result

- Current skills joined: **37 / 37**
- Overall invocation split: **22 USER_INVOKED / 15 MODEL_INVOKED**
- Claude ↔ Codex invocation-policy mismatches: **0**
- Current `SKILL.md` operative Skill-tool calls: **15**
- Illegal current operative calls targeting user-invoked skills: **0**
- Total graph edges after semantic correction: **305**

This is consistent with the repository's invocation governance: only model-invoked skills may be reached through the Skill tool. It also confirms that the historical illegal-cross-call defect represented by CT-H01 is not present in the frozen current workflow graph.

## Batch 04 — ask-matt router expansion

`03_ROUTER_MATRIX.md` / `.json` deterministically scan exact `/skill-name` labels in the frozen ask-matt source and compare them with the frozen Claude plugin's promoted set.

### Machine result

- Current skills: **37**
- Promoted plugin skills: **25**
- Expected promoted router targets excluding ask-matt itself: **24**
- Exact promoted targets mentioned by ask-matt: **24 / 24**
- Missing promoted router targets: **0**
- Extra non-promoted router targets: **0**

Therefore the historical router-completeness defect CT-H02 is **not recurring in the frozen current router target set**. This does not resolve semantic staleness inside individual routes: CT-009 still shows ask-matt describing a removed diagnosing-bugs → improve-codebase-architecture handoff.

## Batch 05 — distribution symmetry

`03_DISTRIBUTION_MATRIX.md` / `.json` compares every current skill across the frozen distribution and visibility surfaces: Claude plugin, maintainer local linking, list-skills visibility, root README, bucket README, docs page, ask-matt router, and Codex metadata.

### Machine result

- Current skills: **37**
- Claude plugin promoted: **25**
- Maintainer local-linked: **33**
- `list-skills.sh` visible: **37**
- Root README visible: **25**
- Bucket README visible: **37**
- Docs page exists: **25**
- Ask-matt router visible: **24** (all promoted targets except ask-matt itself)
- Codex metadata exists: **37**
- Automated symmetry anomalies: **0**

The 25/33/37 counts therefore represent intentional distribution tiers rather than an unexplained mismatch: promoted engineering/productivity skills are fully surfaced, in-progress skills remain locally linked but not promoted, and misc skills remain discoverable in their bucket/listing without entering the daily-driver local link set.

## Scope caution

The literal, invocation, router, and distribution joins materially improve connection coverage but still do **not** prove that every semantic relationship is mapped. History-reference edges and the formal per-file `CONNECTIONS TRACED` promotion gate remain major Phase 3 work.

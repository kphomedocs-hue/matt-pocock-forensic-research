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

Extraction rules version 2 adds two deterministic scans across all 164 already-frozen blob texts:

1. exact repository-relative path mentions;
2. exact filename mentions only when the basename is globally unique across the 164-file census.

The weaker `PASSIVE_REFERENCE` edge is not added when the same source→target pair already has a stronger explicit/structural edge.

### Machine result

- Total extracted edges: **327**
- `PASSIVE_REFERENCE` edges: **123**
- Exact-path passive mentions: **104**
- Unique-filename passive mentions: **19**
- Globally unique basenames eligible for the filename scan: **83**
- Raw unresolved internal-looking references remain: **5**, unchanged from Batch 01 and already semantically reconciled there.

### CT-005 / Teach glossary result

`skills/productivity/teach/GLOSSARY-FORMAT.md` (MP-0152) now has **1 incoming reference**, overturning the stronger source-tree-orphan hypothesis.

The incoming literal reference is from frozen human documentation `docs/productivity/teach.md` (MP-0051), which explicitly states that the skill ships `GLOSSARY-FORMAT.md` but `SKILL.md` no longer links to it. Frozen operative `skills/productivity/teach/SKILL.md` (MP-0156) still has no reference to that support file.

Therefore:

- **repository orphan:** NO — disproved by exhaustive literal scan;
- **operative Teach linkage:** MISSING;
- **current classification:** operative linkage gap / documented stale support behavior;
- **CT-005:** remains OPEN, but its orphan question is resolved.

## Scope caution

The expanded literal scan materially improves incoming-reference coverage but still does **not** prove that every semantic relationship is mapped. Aggregate router relationships, invocation-policy legality, distribution symmetry, and history-reference edges remain separate Phase 3 joins.

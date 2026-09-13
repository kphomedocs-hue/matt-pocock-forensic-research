# Phase 3 Connection Reconciliation

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

This file records semantic adjudications layered over the deterministic graph. Raw machine evidence remains in `03_CONNECTION_EDGES.json` / `03_CONNECTION_INDEX.md`; per-file gate state lives in `03_PHASE3_CLOSURE_INDEX.json/.md`.

## Batch 01 — five unresolved internal-looking references

| Source | Raw target | Resolution | Classification |
|---|---|---|---|
| `skills/engineering/domain-modeling/CONTEXT-FORMAT.md` | `./src/ordering/CONTEXT.md` | Consumer-repository example path inside the generated CONTEXT structure, not a repository-local file target. | GENERATED/TEMPLATE TARGET — NOT BROKEN |
| same | `./src/billing/CONTEXT.md` | Consumer-repository example path. | GENERATED/TEMPLATE TARGET — NOT BROKEN |
| same | `./src/fulfillment/CONTEXT.md` | Consumer-repository example path. | GENERATED/TEMPLATE TARGET — NOT BROKEN |
| `skills/engineering/wayfinder/SKILL.md` | `link` | Literal placeholder in `[<closed ticket title>](link)`. | TEMPLATE PLACEHOLDER — NOT BROKEN |
| `skills/in-progress/setup-ts-deep-modules/SKILL.md` | `./src/packages/README.md` | Consumer-repository file the skill instructs the agent to create. | GENERATED TARGET — NOT BROKEN |

Result: **5/5 reconciled, 0 confirmed broken repository links, 0 remaining unresolved from this queue.** Machine-readable dispositions: `03_REFERENCE_DISPOSITIONS.json`.

## Batch 02 — exhaustive literal passive references

The graph scans all frozen blob texts for:

1. exact repository paths;
2. exact filenames only when the basename is globally unique in the 164-file census.

A weaker passive edge is not added when the same source→target relationship already has a stronger explicit/structural edge.

This pass disproved the stronger CT-005 orphan hypothesis: `skills/productivity/teach/GLOSSARY-FORMAT.md` has a human-doc incoming reference. The operative Teach skill still does not reference it, so CT-005 remains an **operative linkage gap**, not an orphan finding.

## Batch 03 — operative-call semantics and invocation policy

Only current `SKILL.md` workflow instructions can create `OPERATIVE_CALL` edges. Governance/history/docs prose about invocation is not executable dependency evidence.

All current skills are joined against both harness policies:

- Claude `disable-model-invocation: true` → `USER_INVOKED`;
- Codex `allow_implicit_invocation: false` → `USER_INVOKED`;
- omission → `MODEL_INVOKED`.

The frozen current graph has **0 Claude↔Codex policy mismatches** and **0 illegal operative calls to user-invoked targets**.

## Batch 04 — ask-matt router coverage

`03_ROUTER_MATRIX.json/.md` compares exact `/skill-name` router labels with the promoted Claude-plugin set.

The current router covers every promoted target other than ask-matt itself and contains no non-promoted target. This closes historical router-completeness recurrence for the frozen target set; it does **not** prove every route description is semantically current (for example CT-009 remains a route-content staleness finding).

## Batch 05 — distribution symmetry

`03_DISTRIBUTION_MATRIX.json/.md` checks every current skill across plugin promotion, maintainer local linking, list-skills visibility, root README, bucket README, docs page, ask-matt and Codex metadata.

The 25/33/37 universes are intentional tiers, not one expected identical set:

- promoted engineering/productivity;
- maintainer-linked engineering/productivity/in-progress;
- all current skills in list-skills/Codex metadata.

Automated distribution anomaly count is required to remain zero for Phase 3 closure.

## Batch 06 — exact skill-label references

Extraction rules v4 add exact `/skill`, `$skill`, and backticked skill-name references as `SKILL_REFERENCE` edges while stripping external URL bodies before slash scanning.

A second-order quality gate (`03_PHASE3_QUALITY.json/.md`) treats backticked names as contextual/weak evidence. They remain visible relationships, but a file is not allowed to rely solely on contextual backticks as proof of non-orphan status.

## Batch 07 — history bindings

`03_HISTORY_BINDINGS.json/.md` maps each durable H-event to current files by intersecting exact commit/PR changed-file sets with the frozen 164-file census.

The binding builder now parses H-ID, area, lineage state and event evidence directly from `05_HISTORY_LEDGER.md`; those definitions are no longer duplicated in Python. A history binding is connection evidence only and does not turn a PARTIAL history lineage into RECONCILED.

## Batch 08 — zero-incoming semantic review

Files remaining at true zero incoming are not auto-labelled orphan. Explicit dispositions preserve the zero count and explain the repository role. The reviewed set and machine-readable classifications live in `03_ORPHAN_RECONCILIATION.md` / `03_ORPHAN_DISPOSITIONS.json`.

## Batch 09 — formal closure and promotion

`03_PHASE3_CLOSURE_INDEX.json/.md` combines graph state, unresolved-reference dispositions, orphan evaluation, router/distribution obligations, invocation legality, config ownership and symlink checks into a per-file gate.

Formal status promotion is a separate fail-closed operation. Every promoted note receives a Phase 3 evidence block and the master ledger/foundation are rebuilt around the promoted state. `CONNECTIONS TRACED` never implies `VERIFIED`.

## Batch 10 — quality/red-team recheck

`03_PHASE3_QUALITY.json/.md` independently checks assumptions not covered by the primary builders, including:

- contextual backtick references as sole orphan proof;
- Markdown reference-definition / HTML / autolink syntax missed by the inline-link extractor;
- skill-support ownership gaps;
- durable history-ledger ↔ generated history-binding parity;
- master-ledger Ref-in / Ref-out population;
- build-fingerprint coverage.

`03_PHASE3_BUILD_MANIFEST.json/.md` SHA-256 fingerprints the Phase 3 generator/acceptance inputs and authoritative generated outputs, and `scripts/verify_phase3_manifest.py` verifies them byte-for-byte.

## Closure statement

Phase 3 is complete only when the atomic rebuild, closure index, build manifest and quality gate are simultaneously green. Numerical counts are authoritative only in generated artifacts; this human reconciliation file intentionally avoids maintaining a competing copy of volatile counts.

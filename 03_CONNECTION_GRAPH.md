# Phase 3 Connection Graph — Semantic Supplement

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

## Authority

This file is **not** the exhaustive edge ledger. The authoritative machine graph is:

- `03_CONNECTION_EDGES.json` — every extracted edge and raw unresolved reference;
- `03_CONNECTION_INDEX.md` — per-file incoming/outgoing counts and invocation-policy summary;
- `03_PHASE3_CLOSURE_INDEX.json/.md` — per-file closure gate;
- `03_PHASE3_BUILD_MANIFEST.json/.md` — SHA-256 binding of Phase 3 inputs and outputs;
- `03_PHASE3_QUALITY.json/.md` — second-order quality/red-team checks.

This document is the human semantic supplement: it records how important relationship classes are interpreted and which apparent gaps were manually adjudicated. It intentionally does not maintain a second hand-written copy of all generated edges.

## Current edge model

The generated graph recognizes these relationship classes:

- `OPERATIVE_CALL` — a current `SKILL.md` instructs the running agent to invoke another skill through the Skill tool;
- `PASSIVE_REFERENCE` — exact repository path or globally unique filename reference without operative invocation;
- `SKILL_REFERENCE` — exact `/skill`, `$skill`, or backticked skill-name reference; backticked names are treated as contextual/weak evidence by the Phase 3 quality gate and cannot be the sole proof of non-orphan status;
- `DOC_LINK` — explicit internal Markdown link;
- `DISTRIBUTION_ENTRY` — manifest/distribution exposure;
- `CONFIG_BINDING` — Codex metadata ownership/binding;
- `SYMLINK` — physical Git symlink target.

History-to-current-file relationships are generated separately in `03_HISTORY_BINDINGS.json/.md` from the durable `05_HISTORY_LEDGER.md`.

## Semantic adjudications

### Invocation legality

Only current `SKILL.md` workflow instructions create `OPERATIVE_CALL` edges. Governance docs, changesets and human docs that discuss the Skill tool are references about policy/history, not executable workflow calls.

Every operative-call target is joined against both Claude and Codex invocation policy. The frozen graph has no policy mismatch and no illegal current operative call to a user-invoked target.

### Unresolved-looking references

The five machine-unresolved references are all intentionally non-repository targets and remain preserved in raw output for auditability:

1. three `domain-modeling/CONTEXT-FORMAT.md` consumer-repository example paths;
2. Wayfinder's literal `(link)` template placeholder;
3. setup-ts-deep-modules' generated consumer-repository `src/packages/README.md` target.

Their exact dispositions live in `03_REFERENCE_DISPOSITIONS.json` and are explained in `03_CONNECTION_RECONCILIATION.md`.

### Zero-incoming files

Zero incoming does not automatically mean orphaned. Files with no incoming graph edge are closed only through a recognized structural role or an explicit semantic disposition.

The five explicit zero-incoming dispositions are recorded in `03_ORPHAN_DISPOSITIONS.json` / `03_ORPHAN_RECONCILIATION.md`; no fake incoming edge is added to make them appear connected.

### Teach glossary

`skills/productivity/teach/GLOSSARY-FORMAT.md` is **not** a source-tree orphan: human Teach documentation references it. The operative Teach `SKILL.md` does not wire it into the workflow, so CT-005 remains an operative linkage gap rather than an orphan finding.

### Router and distribution

Ask-matt router coverage is generated independently in `03_ROUTER_MATRIX.json/.md`. Distribution/visibility symmetry across plugin promotion, local linking, list-skills, root/bucket READMEs, docs pages, ask-matt and Codex metadata is generated in `03_DISTRIBUTION_MATRIX.json/.md`.

The differing 25/33/37 universes are intentional distribution tiers, not one expected set:

- 25 plugin-promoted engineering/productivity skills;
- 33 maintainer-local-linked engineering/productivity/in-progress skills;
- 37 current skills visible to list-skills and carrying Codex metadata.

## Phase 3 closure rule

A file reaches `CONNECTIONS TRACED` only after applicable outgoing/incoming references, internal links, cross-skill calls, config/distribution bindings, invocation policy, unresolved/generated targets and orphan state are closed in the generated closure index.

`CONNECTIONS TRACED` does **not** mean behavior, history, runtime or end-to-end behavior is verified. Those remain later phases.

## Current state

Phase 3 is formally complete only when the generated closure index, build manifest and Phase 3 quality gate are green together. Current numerical counts must always be read from those generated artifacts rather than copied manually into this semantic supplement.

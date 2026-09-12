# Canonical Research Schema

This file defines the durable research structure for the forensic audit of `mattpocock/skills`.

The schema is prospective and non-destructive: older notes may use legacy headings/syntax as long as `scripts/validate_foundation.py` can prove the same immutable provenance. New or materially revised records should use the canonical fields below.

## Evidence classes

Every substantive assertion should be distinguishable as one of:

- **SOURCE FACT** — directly supported by the frozen repository or traced GitHub history.
- **STRUCTURAL INFERENCE** — derived from multiple source facts without direct runtime observation.
- **KP INTERPRETATION** — analyst interpretation of significance.
- **KP RECOMMENDATION** — proposed improvement or adaptation, not a source claim.

## Issue origin

Every new contradiction/defect/integrity issue should identify one origin:

- `SOURCE_REPO` — defect, contradiction, drift, or ambiguity in `mattpocock/skills`.
- `AUDIT_TOOLING` — defect in this forensic research repository or its automation.
- `EXTERNAL_DEPENDENCY` — behavior depends on an external service/tool/repository outside the frozen source.

Do not mix audit-tooling failures into the Matt source contradiction register without explicit origin labeling.

## File-note canonical fields

A new or normalized `02_FILE_NOTES/MP-xxxx.md` should contain:

1. MP-ID and exact frozen path.
2. `Status` — one of `READ`, `CONNECTIONS TRACED`, `VERIFIED`.
3. `Frozen commit` — exact 40-character frozen commit SHA.
4. `Blob SHA` — exact census blob SHA.
5. `Category` — generated census category.
6. `Read evidence` — how the complete physical file was inspected.
7. `Source facts / observations` — file-local facts only.
8. `Connections` — outgoing/incoming/config/distribution/history relationships as they are reconciled.
9. `Contradictions / history IDs` — durable IDs where applicable.
10. `Unresolved / later-phase checks` — explicit remaining work.
11. `Verification state` — when promoted beyond READ, identify what was checked and by which evidence class.

Legacy notes are not rewritten merely for formatting. Schema normalization must not alter original evidence meaning.

## Status pipeline

`UNREAD → READ → CONNECTIONS TRACED → VERIFIED`

### READ gate

- exact file is in the frozen 164-blob census;
- durable file note exists;
- note maps to the exact frozen commit and blob SHA;
- complete physical contents were inspected.

### CONNECTIONS TRACED gate

A file may be promoted only after all applicable dimensions are closed:

- explicit outgoing internal references;
- incoming internal references against the full frozen census;
- Markdown/internal path links;
- operative cross-skill calls;
- config/metadata ownership and bindings;
- distribution membership;
- invocation policy of operative-call targets;
- unresolved/generated/template references reconciled;
- orphan status evaluated using negative searches, not ranked search alone;
- graph evidence persisted.

Automated edge extraction by itself does **not** satisfy this gate.

### VERIFIED gate

Requires CONNECTIONS TRACED plus applicable behavior/enforcement, history, contradiction, runtime/distribution, second-pass, and red-team checks. The exact verification dimensions are recorded per file or claim.

## Contradiction canonical fields

New contradiction records should contain or map cleanly to:

- ID
- Origin
- Area
- Claim / evidence A
- Claim / evidence B
- Classification
- Defect state (`CURRENT / FIXED / PARTIALLY FIXED / DOCS STALE / UNKNOWN` where applicable)
- Status (`OPEN / RESOLVED / ACCEPTED DESIGN / UNKNOWN`)
- Impact
- Resolution test / next evidence needed

A contradiction is not considered resolved merely because one source appears newer; the current operative truth and affected secondary surfaces must be reconciled.

## History canonical fields

History work is selective but explicit. High-impact files/claims require:

- history ID;
- date;
- subsystem/area;
- event;
- exact commit/PR/issue evidence;
- current significance;
- whether lineage is `RECONCILED`, `PARTIAL`, or `NOT MATERIAL`.

`NOT MATERIAL` must be an explicit determination, not absence of history work.

## Distribution truth

Counts and memberships must be generated or mechanically checked from the frozen source wherever possible. Current frozen invariants:

- physical blobs: 164;
- current `SKILL.md`: 37;
- Claude plugin promoted: 25;
- maintainer local-link set: 33;
- Codex `agents/openai.yaml` owners: 37.

Narrative documents may describe these sets but are not the authority.

## Tooling integrity

Generated research outputs must:

- use the shared `forensic-generated-main-writes` concurrency lane;
- sync latest `main` before generation;
- check generated files exist and are non-empty;
- detect untracked outputs with `git status --porcelain`, not only `git diff`;
- retry/rebase on push races;
- fail closed on provenance/count invariants;
- persist diagnostic reports before final gate failure where practical.

## Promotion rule

No file, phase, contradiction, or project-wide claim is promoted because it "looks complete." Promotion requires the explicit gate for that state to be satisfied and durable evidence to be present in GitHub.

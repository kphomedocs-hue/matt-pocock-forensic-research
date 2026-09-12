# Research Status

## Project state

**IN PROGRESS**

Source repository: `mattpocock/skills`
Frozen commit: `3cca18b368ae95cdbdebbff572ccafa662551015`
Frozen tree: `6e84c093fda2026396cea9fad6a924a6da0e1452`
Physical denominator: **164 blobs/files**

## Current phase position

Primary phase focus: **Phase 3 — Connection Mapping**.

Phase 1 and Phase 2 are complete. The exact frozen recursive tree is materialized in `01_MASTER_FILE_LEDGER.md` and `01_FILE_CENSUS.json`, generated deterministically from the Git tree by `scripts/build_master_ledger.py`. The workflow `.github/workflows/rebuild-ledger.yml` validates 164 unique blobs, 164 unique paths, 164 unique MP-IDs, rejects truncated source trees, and derives READ-or-higher status from durable notes in `02_FILE_NOTES/`.

Every frozen physical blob now has a durable per-file note and is mechanically marked READ. This closes physical coverage only; it does **not** mean the forensic audit is complete. Connection tracing, behavior/enforcement reconciliation, history closure, contradiction/orphan analysis, runtime/distribution validation, second pass, red-team verification, and final reconstruction remain.

## Phase status

| Phase | Status | Gate state |
|---|---|---|
| 1. Census & Ledger | **COMPLETE** | 164/164 frozen blobs have deterministic MP-IDs, paths, mode/type, size, blob SHA, category, runtime-risk class, and conservative status. |
| 2. Full Physical Read | **COMPLETE** | **164 READ / 0 UNREAD**. Every physical blob has a durable note in `02_FILE_NOTES/`. |
| 3. Connection Mapping | **IN PROGRESS** | Several relationships are already evidenced, but exhaustive incoming/outgoing typed-edge mapping is not complete. |
| 4. Behavior & Enforcement | IN PROGRESS / evidence accumulated | Multiple enforcement gaps and invariants identified; CT-010 confirmed from operative sources. |
| 5. History | IN PROGRESS | Root CHANGELOG has a formal durable reread; several high-impact PRs/commits have also been traced. |
| 6. Contradictions & Orphans | IN PROGRESS | Multiple current and historical contradictions have frozen-source evidence; exhaustive orphan/incoming-reference analysis remains. |
| 7. Runtime & Distribution | IN PROGRESS | Package/release/linking/plugin/Codex paths partly reconstructed; isolated runtime validation remains. |
| 8. Second Pass | NOT STARTED formally | No formal high-impact second-pass gate yet. |
| 9. Red-Team Verification | NOT STARTED formally | Individual falsification checks exist, but no systematic red-team pass yet. |
| 10. System Reconstruction & KP Comparison | BLOCKED by prior gates | Preliminary synthesis exists but is not final. |

## Authoritative counts

- Physical blobs/files: **164**
- Ledger rows: **164**
- Phase 2 READ: **164**
- Phase 2 UNREAD: **0**
- CONNECTIONS TRACED: **0** formally promoted in the durable ledger
- VERIFIED: **0** formally promoted in the durable ledger
- Current SKILL.md files: **37**
- Promoted skills: **25**
- Local link skill set: **33**
- Promoted invocation split: **14 user-invoked / 11 model-invoked**

## Most recent durable range

`MP-0001` through `MP-0164` are READ with notes in `02_FILE_NOTES/`.

The final Phase 2 range covered:
- remaining engineering Wayfinder/Wizard source, metadata, and wizard executable template;
- all in-progress bucket source, metadata, support, and dependency-cruiser config;
- complete misc bucket including the executable Git guardrail hook;
- complete productivity bucket including teaching formats/source and writing-for-agents source/mechanics.

Durable findings strengthened in the final range:
- Wayfinder's default `plan, don't do` constraint can be overridden from map Notes, so the constrained workflow can carry an authored exception;
- Wizard hides secret entry but deliberately persists captured values to plaintext `.env`; hidden input is not at-rest secrecy;
- `retro` is substantial operative behavior despite the in-progress README calling it a non-functional STUB;
- `setup-ts-deep-modules` has a strong enforcement proof gate: pass → deliberate violation must fail → revert → pass;
- dependency-cruiser config implements five error-level rules, including a private tests-folder rule in addition to the four-rule prose summary;
- Git guardrails are a real pre-execution gate but rely on regex command-string matching rather than parsed Git/shell semantics;
- writing-fragments is explicitly explore while writing-beats/writing-shape are exploit, with concept-grounding as a sequencing constraint;
- Teach's glossary format exists and is substantive, while the operative Teach skill does not directly link that support file;
- writing-for-agents treats environment/config as source of truth, duplicated prose as caches, and checkable/exhaustive completion criteria as a defense against premature completion.

## Immediate next execution steps

1. Start exhaustive Phase 3 connection mapping from the frozen source and durable file notes.
2. Build typed edges using: `OPERATIVE_CALL`, `PASSIVE_REFERENCE`, `DOC_LINK`, `DISTRIBUTION_ENTRY`, `CONFIG_BINDING`, `HISTORY_REFERENCE`, and `SYMLINK`; keep inferred edges separate.
3. For every MP file, record outgoing and incoming internal references; do not promote `CONNECTIONS TRACED` until both directions are reconciled.
4. Run negative/orphan searches after the graph is materialized; do not claim absence from ranked search alone.
5. Use the completed graph to drive Phase 4 behavior/enforcement reconciliation and Phase 5 targeted history.
6. Do not return to broad KP recommendations until prior gates are satisfied.

## Resume instruction

Future sessions must load this repository first. Do not use ChatGPT memory or chat summaries as the authoritative audit state.

# History Ledger

High-impact historical claims only move from sampled to reconciled when their specific commit/PR evidence is traced.

## Reconciled history entries

| ID | Date | Area | Event | Evidence | Current significance |
|---|---|---|---|---|---|
| H-001 | 2026-06-17 | Changesets / package metadata | Initial Changesets setup created `package.json` and `package-lock.json` at version `0.0.0`. | Commit `a0324014864317489b5958bf632d7ec8dbccbdcd`. | Establishes bootstrap origin of lockfile 0.0.0. |
| H-002 | 2026-07-08 | TDD | TDD reshaped to reference-only red → green; refactor removed from TDD and moved to review. | v1.1.0 changelog / commit family around `639df6e...`. | Confirms current README red-green-refactor wording is stale. |
| H-003 | 2026-07-13 | Claude plugin | Native Claude Code plugin added with curated promoted skill list. | Commit `42a5b70fcacc7baff1977b13f3919fb2f63af14e`. | Establishes promoted distribution path. |
| H-004 | 2026-07-13 | Codex metadata | `agents/openai.yaml` added beside every SKILL; AGENTS symlink added; user/model invocation mirrored across harnesses. | Commit `697d4ce9742da558fd1ba6697c8e9775e2e302dd`. | Establishes dual-harness invocation architecture. |
| H-005 | 2026-08-05 | Router/docs coherence | Coherence pass fixed missing ask-matt routes, missing TDD→codebase-design pointer, and stale README claims. | Commit `8a475c438d90a2f1d7d3710c12658b60dc701a13`. | Evidence of recurring sync drift. |
| H-006 | 2026-08-05 | Release versioning | Added `sync-plugin-version.mjs`; package.json made effective authority for plugin version; release action switched to `npm run version`. | Commit `f3554acafee0f1549d3f8f7881eca0634fd446d0`. | Fixes plugin/package drift; lockfile remains outside sync mechanism. |
| H-007 | 2026-08-15 | Cross-skill invocation | PR #878 standardized operative cross-skill calls on explicit Skill-tool phrasing. | PR #878, merge `bb1c760...`. | Solved unreliable bare `/skill` prose but introduced semantic regression. |
| H-008 | 2026-08-15 | Cross-skill invocation regression | PR #880 fixed calls to user-invoked targets and added target-invocation-type carve-out to policy. | PR #880, merge `068b6e0...`; commit `1dab982...`. | Canonical example of syntax-correct rewrite violating higher-level invariant. |
| H-009 | 2026-09-04 | Local linking | Frozen baseline merge PR #1025: `link-skills` stopped linking misc/ into local skill directories. | Frozen commit `3cca18b368ae95cdbdebbff572ccafa662551015`. | Current local link set = engineering + productivity + in-progress; misc excluded. |

## History work still required

- Trace plugin creation → subsequent promoted-set changes → current 25-skill manifest.
- Trace Codex metadata count evolution and invocation-mode corrections.
- Trace link-skills history including #1025 in detail.
- Trace current open defects that materially affect runtime behavior.
- For every high-impact current contradiction, identify introduction/fix/recurrence lineage where possible.

# History Ledger

High-impact historical claims only move from sampled to reconciled when their specific commit/PR evidence is traced.

Lineage states: `RECONCILED / PARTIAL / NOT MATERIAL`.

## Reconciled history entries

| ID | Date | Area | Event | Evidence | Current significance | Lineage state |
|---|---|---|---|---|---|---|
| H-001 | 2026-06-17 | Changesets / package metadata | Initial Changesets setup created `package.json` and `package-lock.json` at version `0.0.0`. | Commit `a0324014864317489b5958bf632d7ec8dbccbdcd`. | Establishes bootstrap origin of lockfile 0.0.0. | RECONCILED |
| H-002 | 2026-06-30 | TDD | TDD was first reshaped into a compact reference-only workflow with pre-agreed seams, then five minutes later the refactor stage was explicitly removed so TDD became red → green and refactoring moved to review. | Commits `e81f97660af0bebfdbf2e23db6a71f7dfcb9a659` and `80e9dcc6857f16cc08b8e5b190393ee7591517e0`; both directly change `skills/engineering/tdd/SKILL.md`, and the second deletes the old `refactoring.md`. | Establishes exact lineage for current red → green semantics and confirms red-green-refactor wording on secondary surfaces is stale rather than ambiguous. | RECONCILED |
| H-003 | 2026-07-13 | Claude plugin | Native Claude Code plugin added with curated promoted skill list. | Commit `42a5b70fcacc7baff1977b13f3919fb2f63af14e`. | Establishes promoted distribution path. | PARTIAL |
| H-004 | 2026-07-13 | Codex metadata | `agents/openai.yaml` added beside every then-current SKILL; AGENTS symlink added; user/model invocation mirrored across harnesses. | Commit `697d4ce9742da558fd1ba6697c8e9775e2e302dd`. | Establishes dual-harness invocation architecture; later skill additions/removals still need lineage reconciliation against the current 37-owner set. | PARTIAL |
| H-005 | 2026-08-05 | Router/docs coherence | Coherence pass fixed missing ask-matt routes, missing TDD→codebase-design pointer, and stale README/docs claims. | Commit `8a475c438d90a2f1d7d3710c12658b60dc701a13`. | Evidence of recurring sync drift. | RECONCILED |
| H-006 | 2026-08-05 | Release versioning | Added `sync-plugin-version.mjs`; package.json made effective authority for plugin version; release action switched to `npm run version`. | Commit `f3554acafee0f1549d3f8f7881eca0634fd446d0`. | Fixes plugin/package drift; lockfile remains outside sync mechanism. | RECONCILED |
| H-007 | 2026-08-15 | Cross-skill invocation | PR #878 standardized operative cross-skill calls on explicit Skill-tool phrasing. | PR #878, merge `bb1c760...`. | Solved unreliable bare `/skill` prose but introduced semantic regression. | RECONCILED |
| H-008 | 2026-08-15 | Cross-skill invocation regression | PR #880 fixed calls to user-invoked targets and added target-invocation-type carve-out to policy. | PR #880, merge `068b6e0...`; commit `1dab982...`. | Canonical example of syntax-correct rewrite violating higher-level invariant. | RECONCILED |
| H-009 | 2026-09-04 | Local linking | PR #1025 changed local linking from every non-deprecated current skill to engineering + productivity + in-progress only by adding an explicit `misc/` exclusion. The PR states that all four misc skills had previously been symlinked into both local harness directories, that `misc/README.md` already described them as rarely used/not promoted, and that `in-progress/` remained linked deliberately because it is public and feedback-seeking. The same PR updated `CLAUDE.md` so the governance prose no longer claimed the script links “every skill.” | PR #1025, merge/frozen commit `3cca18b368ae95cdbdebbff572ccafa662551015`; base `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`; head `8666e05d641f6922993616e92c0cf54a85080bd7`; exactly two changed files (`scripts/link-skills.sh`, `CLAUDE.md`). The PR test plan records a scratch-`$HOME` run where all four misc skills were absent from both destinations while engineering/productivity/in-progress still linked, plus `bash -n`. | Reconciles both the pre-frozen behavior and the rationale for the frozen 33-skill local-link set. The difference from the 25-skill plugin set is intentional: `in-progress/` is local-feedback surface, while `misc/` is excluded from both daily-driver local install and promoted plugin distribution. | RECONCILED |
| H-010 | 2026-04-28 | scaffold-exercises variant contract / CT-020 | `skills/misc/scaffold-exercises/SKILL.md` was introduced already containing both the broad “at least one of problem/solution/explainer” rule and the narrower linter summary requiring problem/explainer/explainer.1. The file has one path-history commit, and its creation blob SHA `d87df28e7d8abb4e57ecc6e47d71c274d16054c7` is identical to the frozen-baseline blob SHA. | Commit `62f43a18177be6ec82da242e59ffbc490a4c22ea`; GitHub path history returns only that commit; creation and frozen fetches return the same blob SHA. | CT-020 is an introduction-time internal contract mismatch that remained byte-for-byte unchanged through the frozen baseline, not a later regression. | RECONCILED |

## Coverage policy

History is not required uniformly for all 164 physical files. It is required when a file or claim is high-impact because it controls runtime/distribution behavior, participates in an open contradiction, changes invocation policy, or is necessary to establish introduction/fix/recurrence lineage.

A high-impact item may leave Phase 5 only when its lineage is explicitly `RECONCILED` or explicitly determined `NOT MATERIAL`. `PARTIAL` is durable progress but not closure.

## History work still required

- Trace plugin creation → subsequent promoted-set changes → current 25-skill manifest and move H-003 to RECONCILED.
- Trace Codex metadata count evolution and invocation-mode corrections after the initial 39-skill metadata commit, then move H-004 to RECONCILED.
- Trace remaining current open defects that materially affect runtime behavior. CT-020 introduction lineage is reconciled by H-010.
- For every high-impact current contradiction, identify introduction/fix/recurrence lineage where possible.

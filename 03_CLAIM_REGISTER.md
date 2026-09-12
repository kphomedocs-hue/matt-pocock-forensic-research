# Claim Register

Every major conclusion must have an evidence trail. Repetition never increases confidence.

## Schema

| Claim ID | Claim | Evidence Class | Evidence | Confidence | Contradictions | Status | What would prove this wrong? |
|---|---|---|---|---|---|---|---|

## Current confirmed claims

| Claim ID | Claim | Evidence Class | Evidence | Confidence | Contradictions | Status | What would prove this wrong? |
|---|---|---|---|---|---|---|---|
| CL-001 | Frozen physical repository denominator is 164 blobs/files. | SOURCE FACT | Frozen recursive tree `6e84c093fda2026396cea9fad6a924a6da0e1452`, complete/non-truncated. | High | None known | CURRENT | A second complete enumeration of the same frozen tree yielding a different blob count. |
| CL-002 | Promoted plugin set at frozen commit contains 25 skills. | SOURCE FACT | `.claude-plugin/plugin.json` at frozen commit lists 25 explicit skill paths. | High | Older docs mention 22. | CURRENT | Frozen manifest showing a different explicit list/count. |
| CL-003 | Current promoted invocation split is 14 user-invoked + 11 model-invoked. | SOURCE FACT | All 25 promoted `agents/openai.yaml` files inspected; user-invoked also carry Claude blocking metadata in SKILL frontmatter. | High | Older docs mention 13 user-invoked. | CURRENT | Re-audit of the same frozen metadata yielding a different split. |
| CL-004 | `AGENTS.md` is a symlink to `CLAUDE.md`, not an independently maintained governance document. | SOURCE FACT | Frozen tree mode `120000`; blob content `CLAUDE.md`. | High | Normal content fetch can dereference and look duplicated. | CURRENT | Frozen tree metadata showing normal file mode or different target. |
| CL-005 | `package-lock.json` version `0.0.0` is stale bootstrap metadata, not the current release authority. | SOURCE FACT + STRUCTURAL INFERENCE | Lockfile and package.json both created at 0.0.0; lockfile has exactly one historical commit; later package/plugin version sync does not touch lockfile. | High | Runtime impact not yet directly tested. | CURRENT, runtime effect UNKNOWN | Evidence that release tooling or `npm ci` reads lockfile root version as authoritative and fails/misbehaves. |
| CL-006 | Cross-skill operative calls to user-invoked targets are invalid by repository invocation policy. | SOURCE FACT | `.agents/invocation.md`; PR #880 corrective history. | High | PR #878 temporarily violated it. | CURRENT | Current policy explicitly allowing user-invoked targets to be called via Skill tool. |
| CL-007 | TDD’s current loop intentionally omits refactor; refactoring moved to review. | SOURCE FACT | v1.1.0 changelog history plus current TDD source. | High | Engineering README still says red-green-refactor. | CURRENT | Current TDD source reintroducing refactor as an operative stage. |
| CL-008 | `ask-matt` is a secondary source over skill behavior; underlying `SKILL.md` is authoritative on disagreement. | SOURCE FACT | `docs/engineering/ask-matt.md`. | High | Operative router does not require verification of every load-bearing claim. | CURRENT | Source docs or governance reversing authority order. |
| CL-009 | Repository maintenance has recurring synchronization/enforcement drift across router/docs/invocation metadata. | SOURCE FACT + STRUCTURAL INFERENCE | Historical commits/PRs: router missing skills, stale README claims, invocation rewrite regression, plugin/package version drift. | High | None known | Systematic automated checks demonstrating these classes are now fully prevented at frozen commit. |

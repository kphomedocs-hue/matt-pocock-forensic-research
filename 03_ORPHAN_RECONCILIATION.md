# Phase 3 Zero-Incoming / Orphan Reconciliation

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

This artifact records the explicit semantic review of files that remained at zero incoming graph edges after deterministic path, filename, config, distribution, symlink, operative-call, and skill-reference extraction.

A resolved disposition does **not** invent an incoming edge and does **not** assert that the file is actively consumed. It closes the Phase 3 orphan question by recording why a zero-incoming file still has a coherent repository role. Behavior staleness, historical drift, or usefulness can remain open in later phases.

| MP-ID | Path | Zero incoming? | Classification | Phase 3 disposition |
|---|---|---|---|---|
| MP-0001 | `.agents/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md` | YES | `INTENTIONAL_STANDALONE_ADR` | Retained architecture decision record. No operative consumer is required for its archival decision-record role. Naming/content drift remains separable from connection closure. |
| MP-0021 | `.out-of-scope/mainstream-issue-trackers-only.md` | YES | `INTENTIONAL_STANDALONE_POLICY_RECORD` | Maintainer-facing record of a rejected feature class and prior request context. |
| MP-0022 | `.out-of-scope/question-limits.md` | YES | `INTENTIONAL_STANDALONE_POLICY_RECORD` | Maintainer-facing record of a rejected feature class and prior request context. |
| MP-0023 | `.out-of-scope/setup-skill-verify-mode.md` | YES | `INTENTIONAL_STANDALONE_POLICY_RECORD` | Maintainer-facing record of a rejected feature class and prior request context. |
| MP-0058 | `scripts/list-skills.sh` | YES | `STANDALONE_MAINTAINER_ENTRYPOINT` | Directly invokable maintainer utility that enumerates every `SKILL.md`; an internal caller is not required for this role. |

## Result

- Files requiring semantic orphan review before this pass: **5**
- Reviewed: **5/5**
- Confirmed broken/missing internal consumers: **0**
- Zero-incoming files intentionally standalone by repository role: **5**
- Remaining semantic orphan-review blockers from this queue: **0**

These dispositions are machine-readable in `03_ORPHAN_DISPOSITIONS.json` and are consumed by the Phase 3 closure index. The underlying graph continues to show the real incoming-edge count as zero for these files.

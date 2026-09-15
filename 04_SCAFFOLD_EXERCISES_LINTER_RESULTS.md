# Phase 4 Scaffold-Exercises Linter Runtime Evidence

Frozen source: mattpocock/skills @ 3cca18b368ae95cdbdebbff572ccafa662551015.

Workflow run: 34930009546.

External linter: mattpocock/ai-hero-cli @ 5071b7d2d0e0514e134dadd26d9bed23c7c54365 (v0.2.8).

All exercised inputs were synthetic disposable fixtures. The frozen source, public course lockfile checkout, and external linter checkout were read only.

## SE-001 - frozen scaffold contract and pinned external linter provenance

Status: PASS.

- frozen skill permits a solution-only exercise in its variant rule
- the same frozen skill mandates the ai-hero-cli linter and describes a primary set excluding solution
- the tagged external linter implements that primary-set rejection
- the public course lock resolves ai-hero-cli@0.2.8, and the built package reports that exact version

## SE-002 - solution-only scaffold is rejected by the actual external linter

Status: PASS.

- fixture contains exactly one solution/readme.md variant with real content
- no problem, explainer, or explainer.1 directory exists
- the tagged external linter exits non-zero and names the missing primary-variant rule

## SE-003 - explainer-only control remains accepted

Status: PASS.

- fixture contains exactly one explainer/readme.md variant with real content
- the same tagged external linter accepts that primary variant

## Adjudication

The frozen skill allows solution-only. The tagged linter selected by the public course lock rejects that same shape while accepting an explainer-only control. This confirms CT-020 operationally and does not promote any source file to VERIFIED.

Hard errors: 0.

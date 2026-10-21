# Historical trace replay — completed forensic research cases

Status: **retrospective desk replay complete; no work records, projects, or source cases changed**.

Repository head examined: `deb711e72a3ae3c4c2ca7f84d2ae732844b20fdf`.
Frozen subject source: `mattpocock/skills` commit `3cca18b368ae95cdbdebbff572ccafa662551015`.
Purpose: assess whether durable records for three completed research tests can demonstrate the neutral method's controls. These cases were not originally operated under method v1.0; the replay is retrospective and cannot establish that the method caused their outcomes.

## Case selection

| Case | Why selected | Primary durable record |
|---|---|---|
| B-024 / GH-004–006 | Completed isolated test of an external tracker behavior, with setup, conflicting result, and cleanup | [04_B024_GITHUB_LABEL_RUNTIME_RESULTS.json](https://github.com/kphomedocs-hue/matt-pocock-forensic-research/blob/deb711e72a3ae3c4c2ca7f84d2ae732844b20fdf/04_B024_GITHUB_LABEL_RUNTIME_RESULTS.json) |
| B-047 / SE-001–003 | Paired rejected and accepted fixture tests exposed a documented contract/dependency mismatch | [04_SCAFFOLD_EXERCISES_LINTER_RESULTS.json](https://github.com/kphomedocs-hue/matt-pocock-forensic-research/blob/deb711e72a3ae3c4c2ca7f84d2ae732844b20fdf/04_SCAFFOLD_EXERCISES_LINTER_RESULTS.json) |
| B-046 / CT019-R1 | A concrete example of an audit hypothesis being disproved and the durable conclusion corrected | [04_CT019_REPRODUCTION.json](https://github.com/kphomedocs-hue/matt-pocock-forensic-research/blob/deb711e72a3ae3c4c2ca7f84d2ae732844b20fdf/04_CT019_REPRODUCTION.json), [04_CT019_REPRODUCTION.md](https://github.com/kphomedocs-hue/matt-pocock-forensic-research/blob/deb711e72a3ae3c4c2ca7f84d2ae732844b20fdf/04_CT019_REPRODUCTION.md) |

No matching historical BLOCKED→saved-state-resume or ACCEPTED→REOPENED work trace was present in these selected records. That is a scope gap, not evidence that such events never happened.

## Reconstructed traces and limits

### B-024 — tracker labels are additive

Observed sequence: isolated issue starts with `bug` + `needs-triage`; test adds `enhancement` + `ready-for-agent`; resulting labels contain two category roles and two canonical state roles; cleanup removes labels and closes the fixture issue. Tests GH-004–006; recorded workflow run 35992558197; source-side behavior claim remains separate from agent-prompt adherence.

Method comparison:

- Decision/question and observable result: present in the B-024 behavior claim and assertions.
- Small controlled test: present, synthetic inputs, and cleanup outcome documented.
- Frozen baseline: source commit/tree and two source blob hashes present; a project specification version/owner approval is not recorded.
- Named owner, contributor, reviewer, timestamps, append-only work-state transitions, three-axis review, and evidence retention agreement: **UNKNOWN / not represented**.
- Outcome: strong evidence for the narrow external-dependency claim; no evidence that the triage agent itself flags or repairs the conflict.

### B-047 — prose and mandatory linter disagree

Observed sequence: provenance check pins the external linter and course lock; solution-only fixture is rejected with a missing-primary-variant message; explainer-only control passes. Test IDs SE-001–003; workflow run 34930009546. The finding remains open pending a source-side correction and rerun.

Method comparison:

- Decision/question and falsifiable acceptance checks: present.
- Prototype-like fixture/control pair: **inferred from the test design**, not a recorded PROTOTYPING state or owner decision.
- Frozen source, external dependency version, fixture outcomes, command return codes, and next action: present.
- Named roles, approved numbered work baseline, timestamps, append-only transitions, independent three-axis review, and retained evidence agreement: **UNKNOWN / not represented**.
- Outcome: work correctly preserves an unresolved gap rather than treating a passing control as closure. No correction/revision was shown in this evidence set.

### B-046 / CT-019 — audit hypothesis corrected

Observed sequence: challenge the claim that the documented grep misses double assertions; execute the exact pattern over simple, double, and lowercase-control lines; observe both advertised forms returned and the lowercase control excluded; reverse the original discovery-gap hypothesis and retain it as a resolved audit false positive. The JSON records workflow run 34926350919; the behavior matrix also lists earlier reproductions (34748243021 and 34866017975), but this replay does not infer undocumented actor/state transitions from those IDs.

Method comparison:

- Question, controlled fixture, exact command, output, return code, and narrow conclusion: present.
- Decision reversal is explicit; durable correction is visible in CT-019's adjudication/history.
- Who owned, performed, reviewed, or authorized the correction; when each transition happened; an approved baseline version; review-axis evidence and append-only status events: **UNKNOWN / not represented**.
- Outcome: best evidence of correction discipline among the three cases, but not evidence of a formal REJECTED→IN PROGRESS→REVIEW→ACCEPTED route.

## Cross-case control matrix

| Method control | Replay finding |
|---|---|
| Decision and falsifiable acceptance criteria | Evident in the test claims/fixtures; not consistently captured as a distinct approved brief |
| Prototype only for material uncertainty, with owner decision | Small experiments exist; explicit owner-led prototype exit decision is not recorded |
| Numbered approved baseline | Frozen-source commits and dependency pins are good provenance; they are not equivalent to an owner-approved task specification baseline |
| Named owner, contributor, independent reviewer | Absent from these machine records; identity/independence cannot be replayed |
| Append-only state history and timestamps | Workflow IDs and final results exist, but transition timestamps/state changes are not recorded as a work-item ledger |
| Three evidence-backed review axes | Not recorded; passing tests are not a substitute for these axes |
| Blocked/resume and reopen guards | Not tested by these cases; a suitable historical trace was not found in the selected evidence |
| Durable evidence and boundary statements | Strong: exact frozen commit, result JSON, tests/commands and known limitations are preserved for these examples |

## Practical refinement conclusions

1. Keep source/version/test provenance and explicit “what this proves / does not prove” in the minimum record. The cases show these fields materially improve later interpretation.
2. For small, falsifiable research tests, use a lightweight trace: question, baseline/source, fixture, exact command, expected observation, observed result, decision, actor, timestamp, and durable result link. Do not require every generic work-record field when it adds no control value.
3. Preserve independent review and evidence-backed acceptance for work whose output will be adopted or used operationally. The records cannot tell us whether the three review axes would have improved these tests, so burden/value remains unvalidated.
4. Keep external-service results separate from agent adherence and source correctness. B-024 and B-047 show why a single “PASS” label can overstate what a test established.
5. Maintain UNKNOWN as a first-class retrospective result. Do not infer people, review, approval, dates, or state transitions from a workflow run ID or a final artifact.
6. Do not claim the blocked/resume or reopen rules have been replayed. Find an actual sufficiently documented case later, or mark that control untested; do not synthesize a historical example.

## Decision

This replay supports the method's emphasis on explicit decisions, controlled tests,
provenance, corrections, and bounded claims. It does **not** establish usability,
process efficiency, role independence, complete state-machine adherence, or
readiness for use on live Parkar projects. No trial, human participant, or live
project activity occurred. Next step: draft a minimum evidence schema and score it
against these gaps; keep the frozen method unchanged until separately reviewed.

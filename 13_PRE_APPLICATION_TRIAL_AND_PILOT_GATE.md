# Pre-Application Trial and Pilot Gate

Status: **READY FOR HUMAN TRIAL; NOT YET RUN**.

This plan tests whether two people can use the frozen neutral operating method without coaching. It is separate from the Matt Pocock source audit and does not alter any running project.

## Authority and boundary

- Method baseline: 11_NEUTRAL_OPERATING_METHOD.md, version v1.0-static-reviewed, Git blob 4f3dc9653e5a86456c079dc4a1faf5687aa41271.
- Static desk-check record: 12_NEUTRAL_METHOD_RED_TEAM.json. Its synthetic cases do not count as staff-use validation.
- The research status remains IN PROGRESS and formal VERIFIED remains 0/164.
- The trial uses a disposable example, no live project files, no agent runtime, and no automatic change to the baseline.

## Trial setup

Two people are enough:

- Person A is the owner and contributor. A defines and produces the work.
- Person B is the independent reviewer. B did not produce the output and alone records the review verdicts and acceptance.
- A records the work item and transitions. B checks the work record as well as the output.

Use a blank copy of the minimum work record in the method. Preserve the completed copy and the output only if the participants agree to retain them; otherwise record anonymized results. Use role labels in this test record, not private personal details.

Allow about 20 minutes without coaching. A facilitator may give the scenario and note questions but must not suggest a state or verdict.

## Disposable scenario

Create a one-page visitor guide for a fictional shared workroom. It must have a title, opening hours, three visitor rules, a placeholder contact, and a version/date. Deliver one PDF. Use fictional information only.

The starting decision is: “Can a visitor follow this one-page guide without asking staff for the basic rules?” The initial acceptance baseline is one page, all five required elements present, readable at normal zoom, no real personal data, and a PDF that opens.

### Card 1 — normal route

No uncertain rule requires prototyping. Person A records that reason, approves baseline v1, produces the PDF, and requests review. Person B records a separate verdict and evidence for specification fidelity, quality/standards, and operational readiness. The expected route is DEFINED → SPECIFIED → IN PROGRESS → REVIEW → ACCEPTED only if all three verdicts PASS.

### Card 2 — rejection and revision

Before acceptance, the facilitator supplies a variant missing the version/date. Person B must record a FAIL and REJECTED with the missing element as evidence. Person A revises under the same work ID and baseline v1, requests review again, and Person B can accept only after three new PASS verdicts. Keep the rejected version linked.

### Card 3 — block and reopening

During a second variant, the required opening hours are unavailable. Person A records BLOCKED with prior state, blocker owner, and next action. Once fictional hours are supplied, return to the saved state. After acceptance, the facilitator changes the approved opening hours. Person A requests reopening; Person B authorizes it, the accepted PDF remains preserved, and the owner decides whether v1 still applies or a new specification baseline is required. A changed acceptance requirement must return to DEFINED and receive a new version.

The cards are prompts for observing actual use. They are not evidence that these transitions occurred until completed records exist.

## Trial worksheet

Copy these fields for each card. Do not fill them with invented results before the people run the trial.

- Trial date/time:
- Card and work ID:
- Owner/contributor/reviewer role labels:
- Decision and approved baseline version:
- Prototype result or no-prototype reason:
- Output and evidence links:
- Current state, blocker/prior state if applicable:
- Next owner and action:

| From | To | Actor | Time | Reason | Evidence | Baseline |
|---|---|---|---|---|---|---|
| | | | | | | |

| Submission | Specification fidelity and evidence | Quality/standards and evidence | Operational readiness and evidence | Reviewer decision |
|---|---|---|---|---|
| | | | | |

Keep a new row for each transition and submission. Do not overwrite the rejection or first accepted snapshot when a later version appears.

## Record the observations

| Measure | Record |
|---|---|
| Participants and roles | A and B, with B independent of the output |
| Start/end time | Actual time used |
| State routes | Every transition with actor, time, reason, evidence, and baseline |
| Prototype decision | Explicit no-prototype reason or the question/result |
| Review | Three separate verdicts and evidence per submission |
| Defects | Missing fields, wrong state, unauthorized acceptance, overwritten baseline, lost rejection/snapshot |
| Questions | Exact terms participants could not interpret without help |
| Outcome | PASS, REVISE, or INCONCLUSIVE with reviewer and date |

A critical failure is any self-acceptance, acceptance without three PASS verdicts, a skipped review, a silent baseline edit, or lost rejected/accepted evidence. A trial passes only if all three cards can be completed without a critical failure and the participants can identify the current owner and next action from the record. Time and questions guide simplification; they are not concealed.

If the trial fails, keep v1.0-static-reviewed as the historical baseline, issue a revised method version, and repeat the failed card. Do not relabel synthetic desk checks as human validation.

## First live pilot gate

After a passing human trial, select exactly one small real change. The candidate shortlist is:

| Candidate | Why it fits | Evidence needed before touching it |
|---|---|---|
| A3351 Kiran Ji Residence project-control workflow | Clear owner/team review and existing assignment/completion rules | Current actual workbook or task record, frozen rules, and a disposable copy |
| Standard Jewellers facade change | Strong accepted visual baseline and visible change-control need | Governing source image, exact approved design constraints, and comparison output |
| Smart PDF Autofill benchmark gate | Measurable inputs, holdouts, and output QA | Frozen corrected baseline, evaluator and fixture versions, and isolated test environment |

**Draft recommendation:** A3351 is the smallest human handoff pilot, provided its current authoritative workbook is available. This is a recommendation, not an assertion that its present workbook has been inspected or changed.

Before a live pilot, the owner identifies the exact current source, chooses one bounded change, names an independent reviewer, makes a recoverable copy, fixes acceptance criteria, and identifies where the before/after evidence will live. The live file is not changed by this trial plan.

## Closure

The next durable result should be a completed human-trial record with its evidence and explicit PASS/REVISE/INCONCLUSIVE disposition. Only a PASS permits choosing and preparing the first live pilot. This file is preparation, not a claimed observation.

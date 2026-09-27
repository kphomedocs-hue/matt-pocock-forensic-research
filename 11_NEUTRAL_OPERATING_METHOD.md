# Neutral Operating Method

Version: **v1.0-static-reviewed**. Status: **frozen static baseline** after the ten desk checks and three synthetic scenario traces in `12_NEUTRAL_METHOD_RED_TEAM.json`. This freeze applies only to this method document; it does not promote the forensic research or claim staff-use/runtime validation. Amendments require a new version and a fresh review.

## Purpose

This is a project-independent method extracted from the forensic research. It is deliberately neutral: it does not assume Codex, Claude, SharePoint, a specific tracker, or a specific deliverable.

It makes work understandable, reviewable, reversible, and recoverable. It does not create runtime evidence or promote any file to VERIFIED.

## Operating loop

~~~mermaid
flowchart TD
  A["Decision"] --> B["Shared terms"]
  B --> C["Prototype if needed"]
  C --> D["Specification and acceptance"]
  D --> E["Vertical slice"]
  E --> F["Review and evidence"]
  F --> A
~~~

### 1. Define the decision

Record what must be decided or delivered, why it matters, who owns it, what is excluded, and what would make the decision reversible.

### 2. Freeze shared terms

For each important term, record its meaning, what it excludes, and its owner. A shared word must not silently mean different states to different people.

### 3. Prototype uncertainty

When a material assumption is uncertain, test one question with the smallest useful experiment:

- one representative input;
- one uncertain rule or interface;
- one observable output;
- one pass/fail condition;
- one recorded result.

A prototype removes uncertainty; it is not automatically the final deliverable. If no material uncertainty exists, the owner records a no-prototype reason and proceeds from DEFINED to SPECIFIED.

Prototype exit is explicit: record the question, result, decision (adopt, revise, or reject), and owner who authorizes moving to specification. If the result is inconclusive, keep the work in PROTOTYPING rather than silently proceeding.

### 4. Write the specification

State the input, work to be performed, output, constraints, exclusions, acceptance scenarios, review owner, and evidence location. The owner approves a numbered specification baseline before IN PROGRESS. A material change to scope, shared terms, or acceptance criteria returns work to DEFINED for a new baseline; prior versions and work remain evidence.

Acceptance must be falsifiable. “Looks good” is not sufficient; visible contents, scale, exclusions, and comparison rules are reviewable.

### 5. Split into vertical slices

Each slice produces a coherent, independently reviewable result. It has one outcome, named inputs and outputs, an acceptance check, an owner, dependencies, and a next state.

### 6. Work at observable seams

Test where another person or system receives the result:

- exported file;
- rendered sheet;
- tracker state;
- handoff note;
- folder or API boundary;
- approval record;
- comparison against the brief.

Internal effort is not proof of a usable result.

### 7. Review before completion

Review three separate axes:

| Axis | Question |
|---|---|
| Specification fidelity | Did we deliver what was agreed? |
| Quality and standards | Is it technically and visually acceptable? |
| Operational readiness | Can the next person use, approve, or maintain it? |

REVIEW is not ACCEPTED. The reviewer records a separate PASS or FAIL with evidence for each axis. All three must PASS for acceptance. Any FAIL requires REJECTED with reasons; missing evidence cannot count as PASS.

### 8. Preserve evidence

For every accepted result, preserve the decision or brief, source/reference, accepted output, acceptance check, reviewer/date, deviations, baseline or version where relevant, and next maintenance owner.

## State model

State names are work-item states. A specification baseline is a separate versioned record. Each transition appends one entry with from, to, actor, timestamp, reason, evidence link, and baseline version. No entry overwrites an earlier result.

| From | To | Authorizer and guard |
|---|---|---|
| DEFINED | PROTOTYPING | Owner records the uncertain question. |
| DEFINED | SPECIFIED | Owner records why no prototype is needed and approves the numbered specification baseline. |
| PROTOTYPING | SPECIFIED | Owner records a conclusive prototype result and approves the numbered baseline. |
| PROTOTYPING | DEFINED | Owner rejects the assumption; the decision must be revised. Inconclusive results stay in PROTOTYPING. |
| SPECIFIED | IN PROGRESS | Owner assigns a contributor and confirms the approved baseline and acceptance checks. |
| IN PROGRESS | REVIEW | Contributor submits output and evidence against the approved baseline; a named independent reviewer is available. |
| REVIEW | ACCEPTED | Reviewer, distinct from every contributor to the reviewed output, records PASS with evidence for all three axes. |
| REVIEW | REJECTED | Reviewer records at least one FAIL or missing evidence with reasons. |
| REJECTED | IN PROGRESS | Owner authorizes revision against the same baseline; retain the rejection and use the same work ID. |
| ACCEPTED | REOPENED | Owner requests, and an independent reviewer authorizes, reopening with the invalidated assumption or output and the accepted snapshot linked. |
| REOPENED | IN PROGRESS | Owner confirms the existing baseline still applies; output is corrected under the same ID. |
| REOPENED | DEFINED | Owner records a material decision/scope/acceptance change and prepares a new baseline. |
| PROTOTYPING, SPECIFIED, IN PROGRESS, or REVIEW | BLOCKED | Owner records the prior state, cause, blocker owner, and next unblock action. |
| BLOCKED | Prior state | Owner records resolution evidence; the work resumes at the saved state and cannot bypass review. |
| PROTOTYPING, SPECIFIED, IN PROGRESS, REVIEW, or REJECTED | DEFINED | Owner records a material baseline change; a new version is required before further work. |
| Any nonterminal state | CANCELLED | Owner records the reason and preserves the history; a replacement gets a new ID or an explicit link. |

The reviewer is a named person distinct from those who produced the reviewed output. The owner may review only if the owner did not contribute to that output. If no independent reviewer is available, hold the work in IN PROGRESS or BLOCKED until one is named; silence is never approval. A reviewer change is logged before review.

REJECTED is a review outcome, not deletion. ACCEPTED is a reviewed snapshot, not immunity from later reopening. REOPENED cannot return directly to ACCEPTED. A changed baseline never silently edits the accepted snapshot or prior transition entries.

## Minimum work record

| Field | Required content |
|---|---|
| ID | Stable identifier; keep the same ID for revision/reopening |
| Decision and context | Outcome, why it matters, accountable owner |
| Scope and terms | Included/excluded work; shared terms and version |
| Specification baseline | Version, approval actor/date, inputs, constraints, acceptance criteria, and source link |
| Prototype | Question/result/evidence and decision, or explicit no-prototype reason |
| Slice | Reviewable outcome, input, output, and dependency/blocker |
| People | Owner, contributors, independent reviewer, and any logged substitute |
| Current state | One state from the transition table; if BLOCKED, also prior state, cause, blocker owner, and unblock action |
| Review verdicts | Separate PASS/FAIL, evidence, and reason for specification fidelity, quality/standards, and operational readiness |
| Evidence | Links to source, submitted output, checks, rejected output, and accepted snapshot as applicable |
| Transition history | Append-only from/to, actor, timestamp, reason, evidence link, and baseline version for every change |
| Revision/reopen | What changed, why, authorizer, and link to the prior version or accepted snapshot |

This record is a minimum logical schema, not a requirement to buy software or create a separate form for every field. The reviewer and owner check the actual output, not merely a status label.

## Controls retained from the research

- Prompts are instructions, not automatic enforcement.
- Human documentation can drift from operative instructions.
- Parent specs, executable tickets, and completed work need distinct states.
- Support files need deliberate links to the workflow that uses them.
- Metadata needs a real consumer before its behavior is claimed.
- Static proof is not live proof.
- Human review remains necessary.

## Adoption boundary

### Adopt

Decision-first work, shared terms, small prototypes, observable acceptance criteria, vertical slices, public-seam checks, independent review, and durable evidence.

### Adapt

Templates, checklists, role assignments, state names, and evidence locations. Adapt them to the actual project and staff capacity.

### Defer

Codex/Claude invocation behavior, marketplace behavior, prompt adherence, and any claim that requires an unavailable agent runtime.

### Reject

Treating a prompt as enforcement, marking work complete without review, deleting rejected evidence, or copying unresolved source contradictions into a project as if they were settled truths.

## Pre-application gate

Before adapting this method to any project:

1. Name the decision and accountable owner.
2. Define the minimum deliverable and observable acceptance criteria.
3. Select only relevant principles.
4. Define the human review gate.
5. Define the durable evidence location.
6. Exclude mechanisms that depend on unavailable agent-runtime behavior.
7. Record every project-specific deviation as an explicit adaptation.

This method is the controlled bridge between the research findings and any later project implementation. The three examples in `12_NEUTRAL_METHOD_RED_TEAM.json` are synthetic desk checks; they are not staff-use validation or proof that a tool enforces these rules.

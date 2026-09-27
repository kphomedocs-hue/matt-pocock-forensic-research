# Neutral Operating Method

## Purpose

This is a project-independent method extracted from the forensic research. It is deliberately neutral: it does not assume Codex, Claude, SharePoint, a specific tracker, or a specific deliverable.

It makes work understandable, reviewable, reversible, and recoverable. It does not create runtime evidence or promote any file to VERIFIED.

## Operating loop

~~~mermaid
flowchart TD
  A["Decision"] --> B["Shared terms"]
  B --> C["Prototype uncertainty"]
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

Test one uncertain question with the smallest useful experiment:

- one representative input;
- one uncertain rule or interface;
- one observable output;
- one pass/fail condition;
- one recorded result.

A prototype removes uncertainty; it is not automatically the final deliverable.

### 4. Write the specification

State the input, work to be performed, output, constraints, exclusions, acceptance scenarios, review owner, and evidence location.

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

REVIEW is not ACCEPTED.

### 8. Preserve evidence

For every accepted result, preserve the decision or brief, source/reference, accepted output, acceptance check, reviewer/date, deviations, baseline or version where relevant, and next maintenance owner.

## State model

~~~
DEFINED → PROTOTYPING → SPECIFIED → IN PROGRESS → REVIEW → ACCEPTED
                                      ↘ BLOCKED
~~~

Rules:

- Only the owner or reviewer may move work to ACCEPTED.
- BLOCKED states the cause and next unblock action.
- A revision returns to IN PROGRESS without silently creating a new identity.
- Rejected results remain evidence; they are not deleted.

## Minimum work record

| Field | Required content |
|---|---|
| ID | Stable identifier |
| Decision | Outcome being pursued |
| Context | Why it matters |
| Scope | Included and excluded work |
| Terms | Relevant vocabulary |
| Acceptance | Observable pass conditions |
| Slice | Current reviewable outcome |
| Owner | Person responsible for progress |
| Reviewer | Person who accepts or rejects |
| Evidence | Links to source, output, and checks |
| State | One state from the model |
| Blocker | Cause and next action, if blocked |
| Revision | What changed and why |

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

This method is the controlled bridge between the research findings and any later project implementation.

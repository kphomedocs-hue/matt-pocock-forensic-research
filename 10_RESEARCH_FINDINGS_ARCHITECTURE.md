# Research Findings Architecture

## Purpose

This is the controlled synthesis of the forensic research into Matt Pocock's skills repository. It makes the evidence understandable before any method is adapted to Kartik Verma's running projects.

It does not modify the frozen source, create runtime evidence, or promote any file to VERIFIED.

## Authority and evidence boundary

- Durable authority: this repository's latest main branch.
- Source studied: mattpocock/skills at frozen commit 3cca18b368ae95cdbdebbff572ccafa662551015 and tree 6e84c093fda2026396cea9fad6a924a6da0e1452.
- Machine-readable artifacts outrank this summary.
- Every conclusion is one of: source fact, structural inference, or future KP adaptation recommendation.
- A written instruction is not treated as a guaranteed behavior unless an appropriate enforcement or runtime evidence layer proves it.

## What has been fully studied statically

| Control | Result | Primary durable evidence |
|---|---:|---|
| Frozen physical files | 164/164 | 01_FILE_CENSUS.json; 00_FOUNDATION_INTEGRITY.json |
| Durable per-file connections | 164/164 | 03_CONNECTION_EDGES.json; 03_PHASE3_CLOSURE_INDEX.json |
| Connection graph | 554 edges | 03_PHASE3_QUALITY.json |
| Current skills | 37/37 | 04_BEHAVIOR_COVERAGE.json |
| High-risk non-skill surfaces | 71/71 | 04_BEHAVIOR_COVERAGE.json |
| Current contradictions represented | 20/20 | 04_BEHAVIOR_INTEGRITY.json; 04_CONTRADICTION_REGISTER.md |
| History lineage | complete for all 20 current contradictions | 05_HISTORY_LEDGER.md |
| Formal second static reread | 164/164 matching frozen blobs | 06_SECOND_PASS_STATIC_RED_TEAM.json |
| Static prompt red-team coverage | 24/24 behaviors; 28 tests | 09_STATIC_RED_TEAM_LOG.json |

The research-control system itself is clean: foundation hard errors 0, warnings 0, and the tooling ledger has no unknown or unresolved entries.

## The architecture discovered

~~~mermaid
flowchart TD
  A["Decision / task"] --> B["Primary skill and support material"]
  B --> C["Metadata, scripts, tracker, distribution"]
  C --> D["Observable acceptance and review"]
  D --> E["Durable record and later improvement"]
~~~

The repository has five distinct control layers. They must be evaluated separately.

| Layer | Role | Audit conclusion |
|---|---|---|
| Operative skill | Defines the intended procedure | Primary source for workflow intent |
| Support material | Supplies formats, examples, briefs, and checklists | Useful only when explicitly connected and maintained |
| Metadata/configuration | Declares invocation, installation, and policy | Machine-readable, but not necessarily runtime-enforced |
| External host | Tracker, marketplace, package manager, or platform behavior | Must be independently validated; source files cannot guarantee it |
| Runtime agent | Selects, reads, and obeys the skill | The only layer that can prove agent adherence |

## Refined working principles

These are portable principles extracted from the source architecture. They are not claims that Codex or Claude has executed them here.

1. Start with a decision, not a vague task.
2. Define shared terms before handover.
3. Prototype the uncertainty first with a small vertical test.
4. Write observable acceptance criteria.
5. Split work into coherent vertical slices.
6. Test public seams and handoff points.
7. Review against the original specification.
8. Preserve durable evidence of decisions, sources, tests, changes, and exceptions.

## Critical cautions discovered

| Caution | Evidence-led meaning |
|---|---|
| Documentation can drift | Human docs can conflict with operative skills or metadata; use the primary source for load-bearing claims. |
| Prompt is not enforcement | A skill may instruct an action without any script, config, or host control that guarantees it. |
| Ready and done need explicit state changes | Parent specs, executable tickets, and completed work can be confused if the tracker state is not mechanically distinct. |
| Support files need deliberate links | A valuable template or glossary can exist without being used by the operating workflow. |
| Metadata needs a real consumer | Invocation/distribution metadata can be internally consistent while a real runtime has not been observed loading or obeying it. |
| Static proof is not live proof | File existence, content, and cross-reference checks cannot establish agent adherence. |

## What is reliable for later adaptation

| Decision | Status | Reason |
|---|---|---|
| Adopt the eight working principles | ADOPT | Portable process controls; no Codex/Claude runtime is needed. |
| Use templates, checklists, and named review gates | ADAPT | Retain only when they match the actual Parkar workflow and have a clear owner. |
| Treat agent prompts as automatic enforcement | REJECT | The audit found that prompt text alone does not guarantee execution. |
| Reproduce Claude/Codex invocation or marketplace behavior | DEFER | Requires the named runtime and real observed behavior. |
| Carry source contradictions forward as fixed | REJECT | They remain evidence findings until upstream changes and is independently reassessed. |

## Remaining boundary

The repository has 65 behavior rows. 16 have durable runtime observations; 49 remain pending:

- 16 EXECUTION_OBSERVATION
- 5 EXTERNAL_DEPENDENCY_VALIDATION
- 4 MACHINE_CONSUMER_VALIDATION
- 24 PROMPT_REDTEAM_LATER

No configured Codex CLI or Claude Code harness is available for this research. Therefore the pending rows remain pending, and formal VERIFIED remains 0/164.

## Use before any project application

1. Name the decision and accountable owner.
2. Define the minimum deliverable and observable acceptance criteria.
3. Select only the relevant portable principles.
4. State the human review gate and durable location for evidence.
5. Exclude mechanisms that depend on unavailable agent-runtime behavior.
6. Record every project-specific deviation as an explicit adaptation, not as if it were Matt Pocock's original method.

## Evidence index

- Research contract and status: 00_RESEARCH_MANIFEST.md; 00_RESEARCH_SCHEMA.md; RESEARCH_STATUS.md
- Integrity and file study: 00_FOUNDATION_INTEGRITY.json; 01_FILE_CENSUS.json
- Connections and distributions: 03_CONNECTION_EDGES.json; 03_PHASE3_QUALITY.json; 03_DISTRIBUTION_MATRIX.json
- Behavior and gaps: 04_BEHAVIOR_MATRIX.json; 04_BEHAVIOR_INTEGRITY.json; 04_BEHAVIOR_COVERAGE.json; 04_CONTRADICTION_REGISTER.md
- Runtime boundary: 04_RUNTIME_OBSERVATION_QUEUE.json
- History and reread: 05_HISTORY_LEDGER.md; 06_SECOND_PASS_STATIC_RED_TEAM.json
- Static red-team: 09_STATIC_RED_TEAM_LOG.json
- Tooling integrity: 00_TOOLING_FAILURE_LEDGER.json

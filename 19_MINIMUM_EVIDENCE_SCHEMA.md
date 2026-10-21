# Minimum evidence record — draft 0.1

**DRAFT, NOT ADOPTED.** A documentary record for small research tests, not a
replacement for the frozen neutral operating method, an approval engine, or a
staff-facing form. This draft does not waive any method control.

## Purpose and scope

Capture enough information to answer: what was questioned, which inputs were
used, what check was recorded, what result was reported, what follows from it,
and what remains unknown?

The examples map retained records for B-024, B-047 and B-046 at research commit
`48dcfb47a8153e69316d9f6d47bee02b8b44ae8e`. They are new retrospective records,
not contemporaneous work logs. Reading a historical result is not rerunning its
experiment. The original evidence class is unchanged.

## Smallest useful human-readable view

| Field group | What to record | Why |
|---|---|---|
| ID and question | New record ID, linked behavior/work ID, exact question or claim being tested | Prevents mixing the research question with its eventual conclusion |
| Inputs and source version | Source snapshot, fixture, command or operation, dependency versions where applicable | Makes the result interpretable against the inputs actually documented |
| Check | Test ID and recorded criterion/assertion | Makes the result falsifiable; preapproval is assessed separately |
| Observation and outcome | Actual recorded output plus the source's reported pass/fail or conclusion | Distinguishes expected failure of a fixture from failure of the research test |
| Interpretation | Bounded conclusion and its evidence basis | Prevents a narrow result becoming an unsupported general claim |
| Evidence locator | Repository, immutable commit, file blob hash, precise field pointer | Lets another reader find and compare the exact retained value |
| Method evidence | Named roles, approval, event times/history and three review axes, or explicit UNKNOWN | Prevents absence of evidence becoming silent approval |
| Limits | What this record does not establish | Keeps source truth, service behavior and agent adherence separate |
| Next action | Remaining work or explicit disposition; no implied authorization | Provides a handoff without relabeling the task complete |

Evidence locators are shared in the machine record; a future user interface need
not make staff repeatedly type hashes or JSON. No usability or time-saving claim
has been tested here.

## Statement contract

Each substantive field is an object with exactly four keys:
`basis`, `value`, `evidence`, `reason`.

| Basis | Value | Evidence | Interpretation |
|---|---|---|---|
| RECORDED | Exact JSON value from the source | Exactly one source ID and field pointer | The retained source says this; not proof the source is true |
| INFERRED | Nonblank explanation string | One or more relevant source pointers | Analyst interpretation, explicitly distinct from a recorded fact |
| UNKNOWN | JSON null | Empty list | Not established by the reviewed sample; reason identifies the gap/scope |

Every reason is nonblank. Unknown is not FAIL and not NOT_APPLICABLE.
An unknown value cannot simultaneously contain a claim or evidence.
Do not infer authorization, identities, timestamps, independence or review verdicts.
For method-evidence fields only RECORDED or UNKNOWN is permitted.

For example, a recorded linter exit of 1 can support an expected-rejection test
whose reported outcome is true. Neither value means the work item was ACCEPTED
or REJECTED under the operating method.

## Machine record contract

`19_EVIDENCE_RECORD_EXAMPLES.json` is the populated draft, not a standards-based
JSON Schema. `scripts/validate_evidence_draft.py` implements the bounded local
contract below with the Python standard library; it is not a general-purpose
schema validator.

The bundle has exactly:

- `artifact: MINIMUM_EVIDENCE_DRAFT_EXAMPLES`
- `version: 0.1-draft`
- `status: DRAFT_NOT_ADOPTED`
- `snapshot`: repository and exact research commit (not the upstream subject commit)
- `source_catalog`: source IDs mapped to paths and Git blob hashes
- `records`: nonempty list of retrospective records

Each record has exactly:

- `record_id`, `subject_id`: nonblank strings; record IDs are unique.
- `mode: RETROSPECTIVE`.
- `question`, `conclusion`, `next_action`: statement objects.
- `inputs`: nonempty list of statement objects.
- `checks`: nonempty list with unique nonblank `check_id` values and statement
  objects for `criterion`, `observation`, `reported_outcome`.
- `limits`: nonempty list of nonblank strings; these are analyst-authored
  cautions, not newly verified source facts.
- `method_evidence`: exactly the ten statement fields below.
- `adoption_status: NOT_ESTABLISHED`, always. This draft has no ACCEPTED status.

The ten method-evidence fields are:
`owner`, `contributors`, `reviewer`, `specification_approval`,
`criteria_preapproval`, `event_times`, `transition_history`,
`specification_fidelity_review`, `quality_and_standards_review`,
`operational_readiness_review`.

The source catalog is pinned to this snapshot for these examples. Source
references use `{source, pointer}`; pointers navigate exact JSON fields/array
indices, with `~0` for a literal tilde and `~1` for a literal slash.
The checker rejects invalid/dangling pointers and duplicate JSON keys.

## Rules that prevent misleading completion claims

1. A source commit or dependency pin is input provenance, not approval of a task specification.
2. A criterion recorded in a final result does not establish that it was approved before execution. Keep `criteria_preapproval` UNKNOWN without dated approval evidence.
3. A GitHub commit identity or workflow actor is not automatically the task owner or independent reviewer.
4. A workflow run ID is a reference, not an event timestamp or an independently inspected log.
5. Three passing tests are not the three method review axes.
6. A retained result describing a correction is not proof of an authorized REOPENED state.
7. A positive schema check means a documentary mapping is well-formed and matches the pinned source. It does not authenticate the source's claims, judge the field's relevance, or prove control compliance.
8. A copied value under an unrelated pointer can be mechanically equal yet semantically irrelevant. That relationship still requires review. The checker is not a safeguard against a malicious author who controls the code and data.

## Review against the three cases

| Case | What the draft can preserve | What it must leave unresolved |
|---|---|---|
| B-024 | GH-004–006 labels and reported outcomes; exact source pins; limited tracker conclusion | Whether a triage agent obeyed instructions; independent approvals; actual cleanup beyond the retained record |
| B-047 | SE-002 solution-only rejection and SE-003 explainer-only control; linter/course versions | Source-gap closure; owner-approved prototype exit; whether criteria were set beforehand |
| B-046 / CT-019 | Documented grep, fixture, output and corrected discovery conclusion | Approval and event sequence; later migration correctness; original-run log authenticity |

The B-046 check criterion is explicitly INFERRED from the retained command and
fixture. It is not presented as a recovered original brief.
All ten method-evidence fields remain UNKNOWN in each example: **30 field
occurrences, not 30 newly discovered failures**. No source-record verdict was
altered. The draft makes the gaps visible; it does not fill them.

Blocked/resume and reopen routes remain uncovered by these selected cases.
Do not fabricate histories to demonstrate coverage.

## Validation and source preservation

From a full repository checkout with the snapshot commit available:

```sh
python scripts/validate_evidence_draft.py
python -m unittest discover -s tests -p 'test_evidence_draft.py' -v
```

The checker reads source files with `git show <snapshot>:<path>` and verifies
their blob hashes. It does not use newer working-tree versions, fetch the network,
modify sources, or fall back when a Git snapshot is missing. Outside a Git
checkout it accepts a directory of fetched source files only if their bytes match
the same pinned hashes. This file mode was used for local testing; CI uses Git.

The source catalog contains four files: the behavior matrix and the three
existing result JSON files. A changed current behavior matrix does not invalidate
this historical draft, because the check reads the pinned snapshot.

Local review: the three example records and six selected checks mapped without
errors, with all 30 unknown method-evidence fields retained. Twenty new regression
test methods passed, alongside the existing 36 pre-trial methods (56 total).
Captured results and file hashes are in `19_EVIDENCE_SCHEMA_REVIEW.json`.
This was an author self-review and local execution, not independent approval.

## Adoption boundary and review decision

The representation addresses the replay's recording gaps structurally but does
not supply missing evidence. This is ready for **field-set review**, not adoption.

Before operational use, a separate prospective design must capture authorized
baseline approval, actual actor and event times, contributor/reviewer identity
and independence, per-axis output evidence, and conditional blocked/reopen guards.
An append-only audit store needs independent retention/integrity controls; JSON
and Git history alone do not enforce them. The frozen method's requirements
remain in force.

Keep the next decision bounded: review whether this field set is useful and small
enough, then approve or revise a prospective template if desired. Do not add more
generic audit cycles or label this draft a completed human trial.

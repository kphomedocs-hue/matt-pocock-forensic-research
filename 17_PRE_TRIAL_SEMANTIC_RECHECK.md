# Pre-trial semantic recheck

Status: **local synthetic checks passed; not human or agent-runtime validation**.

## Scope and provenance

Research parent: `03c7d59acf0c39de97e65725896b67bf9e8d26d2`.
Frozen upstream: `3cca18b368ae95cdbdebbff572ccafa662551015`.
Method blob remains `4f3dc9653e5a86456c079dc4a1faf5687aa41271`.
Historical red-team blob remains `55fc598a8628a6b93be39e7780bf449718239265`.

No frozen method, historical synthetic fixture, live project, runtime queue,
contradiction register, or verification status was changed. No human trial,
historical work replay, external AI simulation, or agent harness was run.

## Correction to earlier assurance

The previous validator's zero-error output meant its implemented checks passed.
It checked the four negative controls' `observed: REJECT` labels; it did not
execute the attempts. It checked review-axis keys but not their PASS/FAIL values,
and did not enforce reviewer authority, saved blocked state, or baseline continuity.
The earlier handoff's reference to four validated negative controls was therefore
too broad. The original records remain available unchanged as historical evidence.

## Changes and evidence matrix

| Gap | Executable check now | Regression evidence |
|---|---|---|
| Recorded rejection mistaken for execution | Apply all four attempt payloads to valid trace prefixes; require the intended error code | Four executed rejections; benign attempt does not count as rejection; historical labels do not decide results |
| Failed or malformed verdict accepted | All three axes must be PASS for ACCEPTED; strict PASS/FAIL values | Each failed axis, missing axis, wrong types, and all-PASS rejection tested |
| Unauthorized review or submission | Explicit owner adapter, contributor submission, designated reviewer, independence from every contributor | Unauthorized actor mutations on all 24 transitions; noncontributing owner-review positive control |
| Blocked work skips a state | Save actual origin, validate blocker fields, resume only there with resolution reference | Saved-state bypass and missing block/resolution metadata tested |
| Silent baseline changes | Numbered approval, unchanged version during execution/revision/reopening, unused version on respecification | Drift, invalid versions, reused version rejected; new v2 approval accepted |
| Reopening lacks authority | Prior acceptance, owner request, independent reviewer, snapshot reference | Missing/wrong authorization and direct reacceptance tested |
| Trace malformed or discontinuous | Required metadata, UTC timestamps, time order, ID consistency, legal edges and terminal state | 1,448 wrong-type/empty-field variants, 68 forbidden state pairs, metadata deletion and route tests |
| Manifest omission bypasses integrity | Exact required file set, hash syntax, raw-byte Git blob hashes, path allowlist and symlink rejection | Missing/empty entries, drift, bad hashes, traversal, absolute path, symlink guard, and newline differences tested |

## Architecture

- `scripts/pretrial_semantics.py` contains the synthetic state/guard checker and executable control replay. It has no network or mutation capability.
- `scripts/validate_pretrial_package.py` checks package integrity before reading the case data, then runs semantic checks and reports executed results separately from historical labels.
- `tests/test_pretrial_package.py` exercises valid cases, adversarial mutations, failure codes, and the package command. No third-party test dependency was added.
- Manifest schema 2 pins the checker and tests alongside the unchanged six baseline documents/data files. The previous package commit is retained explicitly. The manifest does not hash itself; Git commit history is the provenance boundary, not protection against someone authorized to rewrite both code and manifest.
- The existing main guard now runs this regression suite. This report records local execution, not a claim that remote CI passed.

## Reproduction and observed results

Run from the repository root with Python 3.12:

```sh
python scripts/validate_pretrial_package.py
python -m unittest discover -s tests -p 'test_pretrial*.py' -v
```

Local environment: Python 3.12.14. Final results: 36 unittest methods passed;
3 historical positive traces / 24 transitions passed; 4 negative attempts
executed and rejected for their intended reasons; package hard errors: 0.
The 1,448 malformed variants and 68 forbidden pairs are subcases inside the
36 methods, not extra independent studies. Full captured output and input hashes
are in `17_PRE_TRIAL_SEMANTIC_RESULTS.json`.

Development checks initially failed because the modified validator/test files
still had the old manifest pins; the pins were updated only after implementation.
An exploratory sweep also incorrectly treated arbitrary nonempty prose as invalid:
`reason: UNKNOWN` passes the structural text check. The final type/empty-value
sweep deliberately excludes that invalid test assumption. No natural-language
truth checker is claimed.

## Still not established

This is a checker for the historical synthetic schema, **not a complete executable
implementation of the operating method**. Specifically:

1. `Owner-A` is explicitly supplied for the three fixtures because they lack an owner field. Identities and approvals are not authenticated. Role substitution history is not modeled.
2. `synthetic://` references are placeholders, not retained artifacts. The checker does not inspect per-axis evidence, prove output quality, or verify that a snapshot reference names the earlier accepted output. Real evidence URLs are rejected by this synthetic-only interface.
3. Prototype conclusiveness, materiality, invalidated assumptions, acceptance criteria, and reason quality remain prose judgments. The baseline syntax `vN` is a deliberately narrow fixture convention, not a new rule imposed on all human records.
4. The frozen review fixture format models rejection through FAIL verdicts. The method's separate missing-evidence rejection route needs a richer schema before real work can be validated.
5. A trace is evaluated as supplied. Append-only storage, deleted history, cross-record evidence retention, concurrency and tamper resistance are not established. There is no exhaustive proof over all possible traces.
6. The trial kit still requires actual separate participant/observer materials and defective PDF/sealed prompts before use. Document headings alone do not establish concealment or fixture readiness.
7. The broader research still has 49 pending behavior rows and VERIFIED remains 0/164. These tests do not close source contradictions or prove previously classified tooling causes fixed.

**Decision:** validator-hardening step complete within this scope. Do not claim
all errors solved or approve deployment/human use from this report alone.
The next separate step is read-only replay of selected completed work with an
explicit evidence schema and unknowns recorded, not a fabricated participant trial.

# Pre-Trial Desk Recheck — 2026-09-27 UTC

## Scope and authority

This is a static recheck of the current research synthesis, frozen neutral method, synthetic red-team report, and pre-application human-trial plan. It does not record a human trial, Codex/Claude runtime execution, or a new full line-by-line reread of all 164 frozen upstream source files. The research repository remains the durable authority; machine-readable artifacts outrank this note.

Reviewed: `10_RESEARCH_FINDINGS_ARCHITECTURE.md`, `11_NEUTRAL_OPERATING_METHOD.md` at Git blob `4f3dc9653e5a86456c079dc4a1faf5687aa41271`, `12_NEUTRAL_METHOD_RED_TEAM.json`, `13_PRE_APPLICATION_TRIAL_AND_PILOT_GATE.md`, `00_NEXT_CHAT_HANDOFF.md`, `RESEARCH_STATUS.md`, and the referenced foundation, Phase 3/4, history, static red-team, and tooling JSON artifacts.

## Findings and disposition

| ID | Original defect | Disposition |
|---|---|---|
| P-01 | Trial retention was optional even though the method requires preserved transition, review, rejected, and accepted evidence. | Corrected `13`: minimum redacted/restricted retention is a PASS condition; refusal stops as INCONCLUSIVE. |
| P-02 | Card 2 could be read as continuing from Card 1's ACCEPTED state before a rejection. | Corrected `13`: three fresh work IDs, with same-ID revision/reopening only within each card. |
| P-03 | Card 3's changed hours did not determine whether the approved baseline still applied. | Corrected `13`: withheld regular hours are an input under v1; a later new holiday-hours criterion triggers independent reopening and a new v2 baseline. |
| P-04 | PASS could be awarded despite illegal transitions or incomplete minimum records. | Corrected `13`: fully recorded legal transitions, independent evidenced verdicts, complete retained records, and snapshots are mandatory. |
| P-05 | The synthesis diagram mixed process steps with the five-layer architecture; “clean” controls could be mistaken for resolved causes. | Corrected `10`: five layers are a structural inference in one table; integrity and tooling classification are bounded claims. |
| P-06 | The prior trial script exposed expected states and verdicts while claiming uncoached use. | Corrected `13`: participant prompts are separate from a concealed observer scoring key. |
| P-07 | The worksheet could be mistaken for the method's full minimum record. | Corrected `13`: it explicitly supplements, and cannot replace, the complete method record. |

The frozen `11` method and its `12` red-team record were not rewritten. A method amendment would require a new version and review.

## Static checks performed

- Reconciled physical files 164/164, per-file connection notes 164/164, Phase 3 graph edges 554, skills 37/37, high-risk surfaces 71/71, behavior rows 65, observed rows 16, pending rows 49 (16 execution, 5 external dependency, 4 machine consumer, 24 prompt), and formal VERIFIED 0/164.
- Reconciled contradiction coverage 20/20, second static reread 164/164 frozen blobs, static prompt coverage 24/24 with 28 tests (18 PASS, 9 FAIL, 1 audit correction), and tooling ledger 192 classified incidents (154 failed, 38 cancelled; 0 UNKNOWN/UNRESOLVED classifications).
- Parsed all three synthetic cases and checked their 24 transitions for a continuous state route, membership in the recorded transition model, nonempty actor/time/reason/evidence/baseline fields, and expected terminal state: no discrepancies found. Synthetic `synthetic://` references are illustrative, not actual retained trial output.
- Checked that the edited trial plan pins the unchanged method blob, keeps the human trial NOT YET RUN, separates cards, requires preservation, conceals the observer key, enforces independent review, and defines the v2 route and complete PASS gate.

These checks are static consistency checks of the cited artifacts. No human use, live application, or agent adherence is established. The 9 failed static claims and 49 pending behavior rows are not “all errors solved.”

## Gate

The written trial plan is ready for a disposable human trial. After actual use, retain the completed records and outputs, score PASS/REVISE/INCONCLUSIVE from the observer key, and revise only the affected method or trial script if evidence warrants it. A live pilot remains gated on a PASS and a fresh inspection of the selected project's authoritative source.

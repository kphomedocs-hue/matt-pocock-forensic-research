# Phase 4 Deep-Module Runtime Evidence

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

Workflow run: `35988745407`.

Installed dependency-cruiser version: `18.4.0`.

Only a disposable synthetic TypeScript consumer was used; the frozen source and user/live repositories were not modified.

## DM-001 — required pass/fail/pass proof with the exact frozen config

Status: **PASS**.

- clean example passes the skill's exact lint:boundaries command
- temporary tests/example.test.ts -> ../lib/impl deep import fails
- both auto-config and explicit-config runs name tests-through-entrypoints
- reverting the deep import restores a clean pass

## DM-002 — fifth shipped rule constrains claimed intra-package freedom

Status: **PASS**.

- exact frozen config exposes five forbidden rules, all severity=error
- tests-folder-is-private is the separately named fifth rule
- same-package non-test code importing its own tests/ fixture fails
- both auto-config and explicit-config runs name tests-folder-is-private
- removing the violating file restores a clean pass

## Adjudication

B-014 closes only if the exact frozen completion proof is observed: clean pass, deliberate test deep import fails specifically under `tests-through-entrypoints`, revert, clean pass.

B-012 closes as runtime-observed only if the exact copied config exposes five error rules and the fifth `tests-folder-is-private` rule is observed rejecting same-package non-test access to `tests/`. CT-012 remains open because runtime evidence confirms the mismatch rather than repairing it.

Hard errors: **0**.

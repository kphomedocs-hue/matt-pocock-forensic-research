# Phase 4 Setup-Pre-Commit Runtime Evidence

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

Workflow run: `35992690366`.

Resolved packages: `{"husky": "9.1.7", "lint-staged": "17.5.1", "prettier": "3.9.9"}`.

Only a disposable synthetic npm/git repository was used; no user or live repository was touched.

## Frozen verification predicate vs current Husky

Executable-bit predicate: **MISMATCH**. User hook executable: **False**; Husky shim executable: **True**; `core.hooksPath`: `.husky/_`.

The mismatch is preserved as evidence rather than repaired with `chmod`: current Husky dispatches through its executable `.husky/_` shim, which invokes the user hook with `sh -e`.

## PC-001 — end-to-end hook smoke

Status: **PASS**.

The harness follows the frozen functional contract: unversioned Husky/lint-staged/Prettier installation, `husky init`, exact hook body, manual `lint-staged` verification, then an actual Git commit with the documented message. A second unformatted file is staged only after manual verification so its committed formatting proves the commit hook executed lint-staged; typecheck/test markers prove the later hook commands executed too.

Hard errors: **0**.

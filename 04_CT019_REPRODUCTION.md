# CT-019 Exact Reproduction

Frozen source: `mattpocock/skills` @ `3cca18b368ae95cdbdebbff572ccafa662551015`.

Workflow run: `34866017975`.

The frozen skill documents `grep -r " as [A-Z]" --include="*.test.ts" --include="*.spec.ts"`. A minimal fixture containing both `as Request` and `as unknown as Request` was searched with the same grep pattern.

- simple assertion found: **True**
- double assertion found: **True**
- lowercase target control found: **False**
- grep exit: **0**

## Adjudication

The original CT-019 reasoning was incorrect. Regex matching is not anchored to the first `as` token. In `as unknown as Request`, the later substring ` as Request` matches ` as [A-Z]`, so the documented discovery command does find the advertised double-assertion line. CT-019 is retained as a resolved audit false positive so the correction remains visible. This reproduction does not prove the later migration edits are always correct; it closes only the discovery claim that CT-019 challenged.

Hard errors: **0**.

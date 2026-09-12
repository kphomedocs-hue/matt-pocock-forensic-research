# Master File Ledger

Source: frozen recursive tree of `mattpocock/skills` at tree `6e84c093fda2026396cea9fad6a924a6da0e1452`.

Physical denominator: **164 blobs/files**.

## Status rules

`UNREAD → READ → CONNECTIONS TRACED → VERIFIED`

A chat summary does not qualify as evidence for a status transition. Each row must eventually carry evidence sufficient to justify its current status.

## Ledger construction status

The exact 164-file tree is confirmed, but the MP-ID row-by-row census has not yet been reconstructed in this durable repository. Until that is done:

- no exact READ percentage is authoritative;
- no exact UNREAD count is authoritative;
- previously read files should be treated as `RECONCILE` until their evidence is recorded here.

## Known physical identity special case

- `AGENTS.md` is a Git symlink (`mode 120000`) whose blob content is `CLAUDE.md`. Record it as a distinct physical blob but one logical maintained source: `CLAUDE.md`.

## Required row schema

| MP-ID | Path | Mode/Type | Size | Blob SHA | Category | Status | Evidence | Ref-out | Ref-in | Runtime Risk | Notes |
|---|---|---:|---:|---|---|---|---|---|---|---|---|

Rows will be generated from the frozen tree in deterministic path order.

# cases/ — behavioral cases with stable ids

`cases.json` is the accumulating test asset (owner: "라이브러리 적용되는거 test case를 쌓아가는건 좀 흥미로워서 적용해보자").
Each case: `id`, `surface` (a `units.json` key), `rule` (anchors in `reference/review-rules.md` or `process.md`),
`summary`, `input` (minimal preconditions), `expected` (observable outcome), and per-host `tests` (the host test that carries the id, or `todo`). A case is written BEFORE the
fix that satisfies it, named in the host test, and never weakened to pass (`reference/spec-authoring.md § 4`).

Seed: C1–C7 are codex's process-lifecycle cases from its adoption spike; C8–C18 came out of the document gate r1 and the second pass; C19–C24 from the fresh-eye check of rev-0; C25 from codex's R2 reconciliation. Each case carries `input` (minimal preconditions) and `expected` (observable outcome). The `expected` column is the contract; the host columns are bookkeeping. A host test that
exists today is named where the leader knows it; `todo` means the host has no test yet; `codex-fill` means codex names it.
Unrun handling: `reference/spec-authoring.md § 4`.

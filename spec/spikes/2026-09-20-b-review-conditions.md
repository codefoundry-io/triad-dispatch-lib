# B P3b: bind conditions, renderer/schema and policy bytes

Status: CLOSED in source `7a2fdf3ed65aaa008a70c5bfecd2d0b824834216` after
`triad-b-p3b-r2` returned all four SAFE and ADMITTED_SAFE with matching integrity.
[B PR 30](https://github.com/codefoundry-io/triad-codex-dispatch/pull/30).
Shared remote main fetched at planning and final closure:
`2eb883fee59e66556ee7c7f87189b38231136622`. B baseline after P3a merge:
`d15becea515635429d21533580e2816526884fb9`. A remains read-only at
`92c8afd500499d8736afcc28b39a87a4f87fed50`.

## Evidence and current behavior

R-PREPARE includes rules, schemas, prompt clauses and policies in behavioral
review scope. R-BIND preserves the current three binding fields until v2.
B `bin/review_round.py:1886` hashes prepared bytes and route receipts without
the objective, criteria, boundary, kind or path used by `render_review_prompt`
at line 1956. Guarded metadata at line 2110 already includes those dynamic
conditions, but neither route includes the renderer/schema source bytes.
Gemini preflight at `bin/gemini_wrapper.py:142` records the policy path but not
its bytes; receipt validation at `bin/review_round.py:432` does not pin them.

## B correction and impact

Hash all existing family-independent prepared conditions. Bind whole renderer
and schema file hashes in both existing routes. Whole-file hashing deliberately
over-invalidates and avoids adding a prompt-template extraction framework.
Add a B-private policy hash to the existing Gemini preflight record, computed
from the same read bytes validated by the producer. Rendering and dispatch
reject an older receipt if current packaged policy bytes differ. Existing
ephemeral receipts require regeneration; no installed revision is adopted.

Preserve current wire, family equality, paired Pro/Flash basis, route/auth checks,
canonical-file checks, snapshot/fingerprint protocol, raw investigation and all
existing policy enforcement. This does not choose new Gemini policy bytes or
resolve D-B1. No AGY policy abstraction or rev2 schema work is included.

## A-specific comparison and later handoff

A `.claude/skills/triad-cross-family-review/lib/review_scratch.py:1588–1597`
folds packet file hashes. Its worktree route at `:4394–4418` hashes metadata and
four delivered artifact bodies; the family prompts are rendered only afterwards
at `:4423–4425`. Those statements do not themselves bind the exact renderer or
validator implementation bytes. A's brief already carries some conditions, so
do not claim that every B dynamic-condition omission is identical on A.

Claude's later same-commit review should trace its current binding inputs,
preserve delivery write ordering and cleanup ownership proofs, and add only
missing rule/schema/prompt/policy inputs through its existing digest mechanism.
Do not copy B's private receipt format or create a shared v2 contract implicitly.

## Verification

Independent fresh Terra/high RED: 17 intended failures and five controls passed.
GREEN: 22 focused and 1150 macOS passes; Ubuntu 24.04: 1148 passes, two filesystem
skips. Validator/lifecycle passed, matching source hashes and four exact roots
absent. Coverage includes changed condition axes, family equality, copied-toolkit
mutations on both routes, exact policy producer bytes, malformed/stale receipt
refusal at render/dispatch and regenerated common basis.

R1 preparation stopped before review inference on the AGY temporary-lock sandbox
boundary. Its source was unchanged and exact owned roots were exported/removed.
R2 used scoped runtime permission with the existing settings restore lifecycle
and autoapprove opt-out; no source/configuration guard was weakened. All four
started before result consumption. Final digest
`4d8c1eeb12be89e0669ba12b4da54875b3ee6247d960306399794a459647713b`;
unchanged fingerprint `df005bf09cc2220ea03a2a6da1ff4d37119e1109b8db68594f003a0a4b420cee`.
The exact round custody was exported, hash checked and cleaned.

Two Minor suggestions remain unimplemented: removing dispatch TOML validation
would confuse hash equality with semantic validity; reordering the test-module
imports addresses a hypothetical future import cleanup, while focused and full
collection currently pass. Reviewed bytes remained unchanged. Production delta
is 28 additions/25 deletions across two Python files.

No runtime enforcement, V1–V5, shared publication, adoption or deployment is claimed.

# Codex integration tests owned by the library repository

The owner selected isolated integration testing and clarified that all work and
tests belong in `triad-dispatch-lib`, not the existing Codex host. Existing hosts
are read-only references. Do not run their suites, change their runtime,
bootstrap, dependencies or configuration, or claim host adoption.

Extend the existing repository Codex adapter; do not copy the host lifecycle or
add a second validator. Keep library version `0.1.0.dev1`, dependencies and pinned
assets unchanged. Current spec main `396a04dac310d5ff91dbe0a36982f7679aa00428`
adds packet availability guidance, with no change to the pinned schemas or prompt
clauses from `fcd96a15d18f3131c1f0111bdb10c3faceae34f8`.

## Deterministic installed-package matrix

Keep the `tools/codex_smoke.py ... self-test` interface, installed package identity
checks, raw-byte admission and neutral isolated subprocess. Expand its synthetic
report to include `cases`, each with `review_kind`, `name` and `outcome`.
Preserve `capture_method=synthetic` and the existing `checks` summary.

For each of `formal-plan`, `implementation-review` and `pre-merge`, render the
canonical clauses and exercise:

- SAFE, concrete must-fix negative, uncertainty-only negative and minor-only
  negative. All are admitted unchanged; negative results do not become approval.
- Changed review_id, family, content_digest, leg_name and attempt: binding refusal.
  A non-null Codex route violates the schema and is refused as such.
- Duplicate and nested duplicate members, invalid UTF-8, Markdown fences,
  trailing prose, and numeric overflow: preserve the original bytes and refuse.
- Changed saved prompt and packet: refuse before verdict admission.

Use fixed expected outcomes independently of the result. A missing rejection or
wrong return/error is a failed self-test, never a passed report. Restore the
temporary fixture after a mutation case. The tests and packets stay under the
library repository or invocation-owned temporary directories. No provider runs
in CI. Resolve the known missing-wheel input case before attempting installation:
the CLI must return 2 without starting an environment or pip operation.

## Fresh native Codex observations

The existing pre-merge control/defect observation remains valid and is not rerun
without a change to its prompt or validator. Add separate formal-plan and
implementation-review control/defect pairs. Each child gets only the current
rendered prompt and synthetic packet, never expected answers or sibling results.
Use fresh requested Sol/medium sessions without inherited turns. Preserve raw
final text without reserialization, label parent-transcribed capture, and run
installed-wheel admission. Do not retry a disappointing answer invisibly.

For plan fixtures, the good plan implements the required discount formula and
tests both percentage endpoints; the bad plan uses the discount amount as the
price. Paths described for future implementation do not exist and must not be
reported as inspected. Implementation fixtures use the existing correct/defective
pure function and instruction-like comments as review data.

## Evidence and completion

Record source commit, artifact and prompt hashes, requested versus exposed child
identity, actual verdicts and capture limits. Run source tests, source-distribution
tests and installed probes on native Ubuntu/macOS CI. Use the library project's
ordinary independent review profile. No host execution, formal TRIAD round,
global installation, merge or release belongs to this test slice.

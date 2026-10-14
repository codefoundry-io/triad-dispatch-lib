# B Gemini version floor and observed-version custody

Status: source correction and full fresh review complete; deployment not claimed.
Source `5e8b9fba195b3b5134690f7578c9e0635d206543`,
[B PR 31](https://github.com/codefoundry-io/triad-codex-dispatch/pull/31).
Integration: PR31 merged after Analyze/CodeQL passed; merge
`71388383de307fbccdf593f913bc36d562ee2e41` matches origin/main and live remote main.
Shared remote main fetched before this slice:
`2eb883fee59e66556ee7c7f87189b38231136622`.
B baseline `d3ae06894658e3c7a7ea8ac6560233147957a187`.

## Requirement, source and bounded behavior

C16 already requires Gemini CLI >=0.34.0. C27/R-GOOGLE separately requires the
observed CLI version in the frozen route record. The deferred common rev2 receipt
schema does not defer this existing private receipt obligation.

Before the change, B's `bin/gemini_wrapper.py::_run_preflight` checked help and
policy without a version probe. The current slice probes the selector-pinned
binary's `--version` first, in the same cwd and scrubbed environment, capped at
15 seconds. It refuses failed, ambiguous, malformed and unsupported output before
help/provider work. Existing policy validation and help checks remain required.

One Gemini-specific validator in `bin/review_round.py` serves both producer and
receipt consumers. Standard [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html)
puts 0.34.0 prereleases below the stable floor and ignores build metadata for
precedence; higher-core prereleases still need the help capabilities. Exact
accepted version text is stored as `gemini_version`. The existing receipt hash
binds it into the common review digest without new public wire/dataclass fields.
Older receipts regenerate. The installed executable reported 0.60.0 during a
provider-free metadata check; this is not policy/auth/model enforcement proof.

## Preserved features and host comparison

Raw/custom invocations, canonical receipt checks, selected binary/route/auth
scrubbing, semantic policy validation, exact policy hash binding, provider-free
preparation and all other review paths remain. No shared policy-byte adoption,
model migration, rev2 schema, Codex subprocess, AGY hook or global setting change.

A was read-only rechecked at `92c8afd500499d8736afcc28b39a87a4f87fed50`:
`3rd-Agent/wrappers/gemini_wrapper.py:158` resolves the selected binary;
`:168-180` builds its command and `:183` submits it, with no intervening Gemini
version/help preflight. A's generic wrapper/admission architecture differs; do
not blindly port B's private receipt layout. On A resumption, implement its own
provider-free floor/capability check and observed-version custody, preserving
existing read-only/permissive route boundaries and raw optional schemas.

## Verification

Fresh dedicated Terra/high RED: 19 intended failures, 4 controls passed, no setup
failure, unchanged source fingerprint and exact fixture cleanup. Related source
tests after the bounded patch: 359 passed. Fresh dedicated GREEN: 23 focused,
1173 macOS passed; validator valid, provider-free lifecycle SUCCESS and
ROUND_INTEGRITY_OK, unchanged source fingerprint and exact fixture cleanup.
Ubuntu 24.04: 1171 passed, 2 existing filesystem skips, terminal exit0.
Production delta: 39 additions, 0 deletions; tests 134 additions/12 deletions;
documentation 66 additions/3 deletions. No generic framework added.

Round `triad-b-c16-r1`: Claude, Google Pro, Google Flash and fresh Codex all
SAFE with no open questions. Digest
`4b2b5dac16594af1f5228535d401e140f78621a1a9fbedd9133bd71484f5edc9`;
pre/post fingerprint
`582c646fc02e1dfbaa8895e9cbbf72682c89965fe3b2af0dca2f6cbc35352289`.
Final ledger ADMITTED_SAFE; exact custody export hash-checked and owned roots
removed. Claude's optional output-size cap and extra consumer-level field test
were checked against source and deferred without a byte change: no current
failure or missing consumer validator was shown, and a post-capture size check
would not bound subprocess allocation. This does not assert trusted/bounded
vendor stdout. The acceptance is all-leg SAFE on unchanged Minor-only code.

V1–V5 remain NOT RUN; C16's runtime authentication requirement is not proved by
the CLI version, and the full C27 route case retains any other outstanding limits.

## Claude leader handoff

Review this containing shared-authoring commit when relayed and refresh remote
main first. This is a settled C16/C27 adaptation, not a shared contract revision.
A remains unchanged until the B completion handoff. Reproduce the cases for below,
equal and above floor, malformed/multiple/nonzero/timeout output, pinned executable,
scrubbed environment, preserved missing-help refusals and changed-version custody.
Report A source/test evidence independently; B tests do not supply A conformance.

# B: restore the authorized AGY investigation evidence procedure

> **Historical record; its REVIEW no-web statements are superseded on 2026-10-03.** REVIEW web now follows the owner's
> standing authorization in current [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](../decisions/owner-register.md#D-REVIEW-LEGS-20261003)); the no-web posture applies only to a false
> condition.

## Basis and ownership

Remote `main` fetched on 2026-09-20: `2eb883fee59e66556ee7c7f87189b38231136622`.
Shared authoring basis: `1fb2de9e974e050804dcd4f3ec2adb629f83b6a9`.
B: `56f0f6657084f81516217ee51698f9b18cfc71dc`.
A (read-only): `92c8afd500499d8736afcc28b39a87a4f87fed50`.
The owner reaffirmed that yesterday's AGY page-fetch defect is delegated to B
for repair and testing. The clarification does not request an audit-redaction
change. This implements existing C29/R-INVEST, not a REVIEW web exception.

## Evidence and current behavior

The [original spike](2026-09-19-google-web-evidence.md) records search-only
answers, unfetched citations and one bounded before/after experiment showing
improvement with the shared clause. That experiment does not prove B behavior
or a general failure rate. B `bin/antigravity_wrapper.py:402-448` lacks `--web`
and the clause. Its dispatch at `:652-676` and custody call at `:704-711` use
the same local prompt. A already appends its clause after validation at
`3rd-Agent/wrappers/antigravity_wrapper.py:1381-1393`; its clause is at `:294`.

## B change and preserved functionality

- Add explicit `--web` for raw INVESTIGATION only; require `--sandbox read-only`.
- Reject blank caller prompts and formal/preflight combinations before provider
  work. Load the single fenced clause from a byte-identical vendored
  `prompts/investigation.md` only for the authorized operation; append one blank
  line and that clause without trimming caller bytes.
- Pin the vendored document and digest in a separate prompt provenance manifest;
  do not alter the independently pinned candidate schema bundle or revision adoption.
- Reuse existing command construction, guard, schema, audit and failure-log paths.
  They receive the final prompt. Hardened masking and failure-only run-log behavior
  remain unchanged. Do not claim that redacted success logs retain full prompt bytes.
- Preserve no-flag behavior, arbitrary optional schemas, read-only mutation denies,
  existing owner denies, auth, process cleanup and REVIEW no-web behavior.

No common normative clause or case expectation changes. D-B2's proposed new
custody destination is not implemented; complete C29 durable-custody conformance
is not claimed by this behavioral repair.

## Verification and Claude handoff

Before production edits: dedicated fresh Terra/high RED; then smallest fix and
separate fresh GREEN, full macOS/Ubuntu 24.04 regressions, packaged byte equality,
and required full-scope multi-family review. A live AGY 1.2.7 Pro/high investigation
will retain the sent prompt and raw stream in the explicitly scoped spike output.
The leader compares completed page-fetch events with every answer citation and
independently checks the cited source. Prompt instructions alone are not proof.

Claude leader: review this same shared commit and the subsequent B evidence.
Keep A unchanged while B leads. A's existing append is already present; compare
the live fetch/citation result and any new failure cause before applying changes.
Do not copy B's native plan-mode adapter into A's custom research-agent route.
The initial section records the plan before B changed its source. The following
observations are subsequent evidence, not whole-contract completion.

## Live paired result on AGY 1.2.7

One pair used the same 805-character caller prompt, Pro/high, existing native
plan/read-only route and timeout. The after arm added only `--web`; its sent
prompt was 1,667 characters (805 + two newlines + the exact 860-character shared
clause). Wrapper/provider exit status was zero for both. These are one-run
observations, not a reliability or comparative speed benchmark.

| Observation | Before | After |
|---|---:|---:|
| Elapsed seconds | 203.491 | 503.4 |
| Completed `search_web` events | 12 | 11 |
| Completed `read_url_content` events | 1 | 12 |
| Failed `read_url_content` events | 5 | 16 |
| Completed `view_file` events | 2 | 27 |

Before, the answer cited repository/site roots that had no matching page fetch
and guessed a policy priority. After, asserted web facts cited fetched tagged
source URLs; the answer explicitly left the policy and local-file questions
UNSURE. Completed tool events establish execution, not full page delivery or
correct interpretation. The local question lacked an absolute fixture path in
both prompts; guessed paths failed. That fixture limitation is separate from
the page-fetch behavior and proves no C28 or containment regression.

### Residual: delivered page artifacts can be incomplete

The leader inspected only the after run's generated page artifacts and compared
them with direct reads of the same official version-tagged URLs:

| Source | Direct source | AGY delivered body | Comparison |
|---|---|---|---|
| [`read-only.toml`](https://raw.githubusercontent.com/google-gemini/gemini-cli/v0.60.0/packages/core/src/policy/policies/read-only.toml) | 2,246 bytes, 56 lines | 996 characters, 18 lines | Strict prefix; actual tool rule omitted |
| [`non-interactive.toml`](https://raw.githubusercontent.com/google-gemini/gemini-cli/v0.60.0/packages/core/src/policy/policies/non-interactive.toml) | 158 bytes, 7 lines | 148 characters, 7 lines | Strict prefix; final `interactive = false` cut |

The first artifact ended inside a comment; the second ended at `interactiv`.
Both had a DONE page-fetch event. The model's truncation uncertainty is supported
by the actual artifact; a wrapper success must not be described as complete
research. Raw source SHA-256 values were respectively
`4899746262c3beedce94ca90fdcbb50028e52232747288e5bff73c523db05bfb` and
`721978c4f1153b7abb5ea24d647dd6acb7093b264ee8f5438b07ee014da369da`.

The [official tool reference](https://www.antigravity.google/docs/hooks) exposes
`read_url_content(Url)`; it does not supply a verified CLI pagination or
untruncated-fetch switch. No such switch or global settings change is invented.
Root cause inside the vendor fetch/render path remains unisolated. The current
repair fixes the omitted C29 invocation procedure; it does not fix this distinct
provider-content truncation. Keep it as a shared A/B investigation item, with
UNSURE on incomplete evidence. A's custom-agent route needs its own reproduction;
the native B result alone cannot establish identical A behavior.

Task-scoped raw diagnostics are retained locally for this requested spike only.
No new permanent evidence store is added; see the
[owner's D-B2 decision](../decisions/2026-09-20-owner-follow-up.md).

## Implemented B source and verification

B source: [`ce68780e8a29cb7455dbc94e660486fcea8c0679`](https://github.com/codefoundry-io/triad-codex-dispatch/commit/ce68780e8a29cb7455dbc94e660486fcea8c0679).
The loader is at `bin/antigravity_wrapper.py:53-60`, option declaration at
`:419-423`, and pre-provider validation/append at `:459-473`. The final prompt
continues into unchanged command/audit/failure paths. A remains unchanged at
`92c8afd` with the existing append at `:1381-1393`; do not replace its distinct
custom-agent invocation with B's native plan-mode route.

- Fresh dedicated Terra/high RED: 18 expected failures before implementation.
- Focused C29/no-web/preflight checks: 37 passed; skill validator valid and
  provider-free lifecycle SUCCESS with matching integrity and exact cleanup.
- Three initial whole-suite failures were synthetic distribution fixtures
  missing the newly hashed prompt assets. Only their two inventory entries
  changed; a separate fresh GREEN passed all 1,348 macOS tests.
- Ubuntu 24.04: 1,346 passed, two existing filesystem skips.
- Required round `triad-b-agy-web-r2`: Claude Opus/xhigh, AGY Pro/high, AGY
  Flash/high and fresh Codex Terra/xhigh all SAFE, matching source integrity,
  `ADMITTED_SAFE`, verified export and exact owned staging cleanup. Claude's
  confirmed Minor unused test import at `tests/test_agy_web_evidence.py:4` is
  deferred to the next reviewed change; no reviewed bytes changed afterward.
- Earlier preparation r1 failed before any producer at the temporary AGY lock
  because the root invocation used the filesystem sandbox. Evidence was kept,
  allocated staging was cleaned, and r2 used the existing authorized host guard
  lifecycle. This was an execution-context mistake, not a vendor/model failure.

This verifies the bounded AGY invocation repair. Gemini policy V1-V5, public-v2
runtime integration, complete page delivery, A conformance and deployment remain
separate claims.

Clean archive verification for `ce68780` passed all 1,348 tests and all 29
source/archive SHA-256 comparisons. Archive SHA-256:
`35daf210d6b0b223de64222777df432d12ae78d99893ad928442d2f5cb9dd888`.
The first archive run had 1,346 passes and two `ps` permission failures because
the leader again used the filesystem sandbox for process-inspection regressions.
Its receipt is retained; the unchanged commit passed the canonical verifier under
authorized host execution. No source workaround, permission-policy weakening or
test expectation change was used.

[B pull request 37](https://github.com/codefoundry-io/triad-codex-dispatch/pull/37)
contains the reviewed source; CodeQL passed. This handoff does not merge, install,
tag or release it. Claude leader should inspect these exact B lines and this
shared evidence before its own implementation resumes.

# B cross-site URL evidence and v2 producer compatibility

Status: measured observations for both maintainers, not a normative amendment,
revision adoption, complete P3 implementation, or live-policy conformance claim.
Remote main was fetched at `2eb883fee59e66556ee7c7f87189b38231136622`;
the existing shared candidate is `6f0f2746f0bd74e16cf6df7c9ee5e0750d42d7d5`.
Claude host A remained read-only at `92c8afd500499d8736afcc28b39a87a4f87fed50`.

## C29: incomplete AGY URL bodies are not GitHub-only

Disposition: **KI-AGY-URL-BODY-PREFIX — known external issue, non-fatal to
dispatch**. The [owner disposition](../decisions/2026-09-20-owner-follow-up.md#ki-agy-url-body-prefix-non-fatal-known-issue)
defines failure accounting and preserves evidence-quality limits. This is not
an open B implementation failure or a claim that AGY has been repaired.

AGY 1.2.7 was invoked through B's existing raw read-only `--web` path, requesting
`gemini-3.1-pro-high` and `high`, with a fresh call for each URL. Requested settings
are not actual effort attestation. Direct source bytes were captured before and
after each call and matched exactly. All provider and wrapper exits were zero.

| URL | Direct bytes | Normalized source / saved body characters | Observation |
|---|---:|---:|---|
| https://www.iana.org/robots.txt | 24 | 23 / 23 | Exact body match |
| https://www.python.org/robots.txt | 537 | 536 / 297 | Strict prefix; 239 trailing characters missing |
| https://www.rfc-editor.org/rfc/rfc20.txt | 18504 | 18497 / 18497 | Exact body match, including page breaks and final page |

The comparison removes the artifact metadata header and edge CR/LF framing;
the direct source's CRLF is normalized to LF. It does not collapse internal
whitespace, remove form feeds or reconstruct missing text. All three sources
are ASCII. A fresh independent native reviewer rechecked the direct-before/after
hashes, stream artifact references, copied artifact lengths and strict-prefix
comparison. This is a three-sample reproduction, not a prevalence estimate or
cryptographic chain of custody from the provider service.

The Python saved body ends at `Disallow: /~guido`; the direct source continues
`/orlijn/` and further rules. Its adjacent provider output calls the stored body
full content. The earlier 158-byte Gemini CLI v0.60.0 `non-interactive.toml`
reproduction ends at byte 148 and omits `e = false\n`, including when the raw URL
is supplied directly and when plan mode is omitted. See the prior
[C29 spike](2026-09-20-b-agy-web-evidence.md) for its original context.

The missing suffix already exists in the provider's saved artifact, before B's
stdout collection. These observations exclude a GitHub-only explanation and a
universal small fixed-size cutoff. They do not isolate origin response handling,
fetch service, cache, extraction or artifact persistence. No verified CLI repair
or truncation setting was found. Do not describe B's evidence-clause change as
fixing AGY body delivery.

Local retained evidence: B leader workspace
`_runs/infra/20260920-agy-web-evidence/cross-site-{iana,python,rfc}/` contains
direct bytes/digests, actual argv, streams, terminal receipts, copied tool
artifacts and comparisons. These task-scoped diagnostics do not introduce a
permanent production page/prompt archive (D-B2 remains unchanged).

Both-host impact: A `3rd-Agent/wrappers/antigravity_wrapper.py:294-308,1382-1393`
already appends the common evidence clause; B's explicit trigger is in
`bin/antigravity_wrapper.py`, commit `8f12bd58e401d061ba4a9bc889791e24718fb915`.
Neither wrapper can recover bytes absent from the upstream artifact. Preserve A's
custom research agent and B's existing raw route. A should reproduce the same
URLs through its own wrapper before claiming identical host behavior; that A run
is NOT RUN. No A change or vendor issue submission was performed.

## C13/C14/C30: Claude CLI generation schema versus local admission

Three bounded synthetic echo calls used Claude Code 2.1.271, `--print`, text stdin,
JSON output, `--no-session-persistence`, Plan permissions, and an empty tool list.
Requested model/effort was Opus/high. The fixed synthetic object was not a review
of source, and none of these calls is admission evidence.

| Schema sent to `--json-schema` | Actual terminal observation |
|---|---|
| Complete shared Draft 2020-12 schema plus exact binding constants | Exit 1; CLI rejected the draft declaration: no schema registered for that dialect URI |
| Only `$schema` and `$id` omitted | Exit 1; API error 400 rejected top-level `allOf` |
| Exactly `$schema`, `$id`, top-level `allOf` omitted | Exit 0; structured output present, 8.5 seconds; the returned object passes the unchanged complete local schema and all six bindings |

This supports the already specified narrow producer projection in
[rev-2 implementation specification](../decisions/rev-2-implementation-spec.md#libraries-and-supported-interfaces).
The normative schema and local admission validation remain unchanged. All field
definitions, references, types and required members are taken from that schema;
the producer projection is only a generation aid. Invalid conditional combinations
still fail the full local validator. It is not a general schema translator.

Evidence: B leader workspace
`_runs/infra/20260920-transport-contract/claude-v2-schema-probe{,-without-dialect,-producer}/`.
The full invocation, synthetic input, stdout/stderr and terminal receipt are
retained. The zero exit is a compatibility result for this exact fixture/version,
not proof of every possible generated result or actual effort identity.

B impact: the Claude subprocess path at `bin/claude_wrapper.py:374-407` currently
generates its schema directly from Pydantic. P3 will use the canonical-backed v2
adapter and demonstrated generation projection only on the explicit v2 path,
while retaining complete post-generation validation and legacy isolation.
A's native Claude leg is a different route; do not apply this B-only CLI finding
as an instruction to alter A's native agent or Codex CLI schema. Other producer
CLIs need their own compatibility evidence. Preserve original JSON duplicate
rejection, six-axis binding, raw investigation/custom schemas and existing
read-only controls.

The independent B producer scenario observed 33 intended missing-adapter RED
failures. Root focused checks after the initial adapter pass 33 cases. Full P3
producer/consumer integration, fresh final GREEN, both-platform regressions and
plan review remain unfinished; no v2 runtime completion is claimed.

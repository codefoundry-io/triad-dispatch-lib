# B P3a: original JSON before verdict normalization

Status: source `bc9ff6949d165e1c11edb44ef1ad519bdaeb40dc`, full review
`triad-b-p3a-r2` ADMITTED_SAFE, all four legs SAFE with matching integrity and
verified custody cleanup. [B PR 29](https://github.com/codefoundry-io/triad-codex-dispatch/pull/29).
Shared remote main checked: `2eb883fee59e66556ee7c7f87189b38231136622`.
A was inspected read-only at `92c8afd500499d8736afcc28b39a87a4f87fed50`.

## Existing requirement and source evidence

P3a implements C14's original-text duplicate rejection and the existing reserved
three-field binding contract. It does not implement deferred C19 attempt/leg
identity or replace the public wire schema. Original duplicate fields cannot be
proved absent after a decoder has retained only their last value.

B's direct verdict-file reader already performs a duplicate-members scan before
strict validation (`bin/verdict_schema.py:198-218` at merged P1). Its wrapper
validation (`bin/_common.py:874-884`) and envelope/event extraction can discard
the original duplicates first. Claude's native envelope, Gemini object-valued
response and AGY terminal structured output all require coverage. AGY's reserved
schema also accepts an entirely missing expected-binding triple, unlike its
Claude/Gemini peers.

## Smallest B correction and preservation

Reuse the direct-file duplicate scanner before canonical verdict bytes are
normalized and before final answer validation. Add literal malformed-binding
fixtures whose last values match, including escaped member names; dict-created
fixtures cannot represent this failure. Bind AGY's reserved schema before any
binary resolution. Preserve arbitrary raw responses, custom schemas, ordinary
investigation, malformed stream-noise handling, timeout/transport/vendor failure
precedence and one-call formal review. No new general JSON framework or repair
loop is needed.

## A differences for later adoption

| A location | Confirmed current behavior | Later maintainer action |
|---|---|---|
| `3rd-Agent/wrappers/_common.py:1590-1601` | Semantic validation returns success before the failure-only `_content_nonrepairable` probe | Prove lexical integrity before successful canonical admission; preserve A's non-repairable arm/content diagnostics. |
| `_common.py:1874-1885` | Claude parses then reserializes `structured_output` | Retain/check original nested members before normalization. |
| `_common.py:409-418` | AGY parses NDJSON into ordinary dicts | Preserve the newline-only framing and malformed/noise behavior while checking canonical review input. |
| `3rd-Agent/wrappers/antigravity_wrapper.py:748-752` | Structured object is reserialized before `validate_response_with_trigger` | A semantic success cannot recover duplicate fields already lost upstream. |

A's binding boundary and repair contract differ from B. Do not mechanically
port B's reserved CLI argument validation or remove A's refusal/diagnostic
features. A remains unchanged until B completes.

## Verification and handoff

Fresh dedicated RED reproduced 24 duplicate-admission cases and the AGY missing
binding guard. A further two-case RED proved that duplicate hooks can fire before
the decoder detects a malformed suffix or incomplete outer object. B therefore
checks complete AGY JSON-line syntax before applying its duplicate scanner; this
preserves the parser's existing malformed/noise behavior. A must preserve that
same distinction when it adds its own lexical admission check.

Fresh dedicated Terra/high GREEN: 34 focused tests and 1115 full macOS tests
passed. Ubuntu 24.04.4/Python 3.12.3: 1113 passed, two filesystem-specific skips.
The source skill validator and fixed provider-free lifecycle passed; lifecycle
source hashes matched and four exact owned roots were absent. Canonical B HEAD
was `26ef666886305b5c352b6b508fa84e0608713139` plus the P3a working diff;
the pre/post fingerprint was
`db419d052ec7675ab486837cad795d1d8d851df696e6bb920f3909228a55bac1`.
These are source verification results, not distribution or authenticated Gemini
V1-V5 evidence. Record the final gate and source commit before closure.

The first full round returned Claude/Pro/Flash SAFE and Codex NOT-SAFE. Codex
identified that B's supported dotted `verdict_schema.LegVerdict` spelling skips
the colon-only Claude/AGY binding gate; Claude also noted the AGY case as Minor.
The leader accepts both as missing required pre-provider binding validation.
The bounded correction recognizes both existing spellings through one reserved
set and B's existing package-file-anchored loader, retaining arbitrary schemas'
hardened import opt-in. An optional AGY parser restructuring was not adopted:
the reviewer confirmed equal current acceptance and described a hypothetical
future framing change, without a current failing case.

A's generic loader (`3rd-Agent/wrappers/_common.py:1350-1382`) also accepts both
spellings, and AGY uses it at `antigravity_wrapper.py:1410-1417`. A enforces
review binding elsewhere, so these lines are not proof of the identical B
wrapper defect. Trace A's own final admission and preserve its custom-schema
contract before choosing a correction. A's source was rechecked, not edited.

Claude's later same-commit review should challenge the diagnosis, verify the
preserved behavior and propose only the smallest A-specific correction.

## Final correction evidence

The alias RED observed six intended failures and eight passing controls.
Both reserved spellings now share B's file-anchored loader and complete binding
and formal-route guards. Import shadows cannot replace the packaged model.
Fresh dedicated Terra/high GREEN: 47 focused /1128 full macOS passes. Ubuntu
24.04: 1126 passes and two filesystem skips. Validator and provider-free lifecycle
passed with exact cleanup. Final unchanged worktree fingerprint:
`235b781f0e585c7cefdc57cadfe8c558f79a6231377deb012976f68524d3fe16`.
Round digest: `c753eea124078c484bcf58e6b899cdf08174b2af1a2cd2a3d536d95bc0980220`.

Claude's two remaining Minor observations propose centralizing a repeated hook
name and unifying equivalent missing/partial-binding predicates. The leader
verified current behavior and regression coverage and retained both as optional
maintenance observations without changing reviewed bytes. The reported test-line
numbers were not valid source anchors; actual tests were checked at lines 70,
122 and 133. No current defect was established by those suggestions.

This closes the two original P3a findings only. Other plans, V1–V5, installed
revision adoption, shared publication and deployment remain separate.

# Owner follow-up: host policies, investigation logging and roster location

> **Historical record; its REVIEW no-web statements are superseded on 2026-10-03.** REVIEW web now follows the owner's
> standing authorization in current [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](owner-register.md#D-REVIEW-LEGS-20261003)); the no-web posture applies only to a false
> condition.

Remote main re-fetched at `2eb883fee59e66556ee7c7f87189b38231136622`.
These answers resolve the owner choices raised by the B contract audit. They do
not claim implementation, runtime conformance, a revision tag or A acknowledgement.
The following English applications are the B leader's interpretation; the Korean
answers are verbatim. Claude leader should review this exact published commit.

## D-B1: preserve separate policies where usage differs

Owner: “사용법이 다르면 분리 유지”

A and B have different Gemini invocation and validation profiles: A's wrapper
`3rd-Agent/wrappers/gemini_wrapper.py:131-180` at `92c8afd` consumes the shared
100/200 policy, while B `bin/gemini_wrapper.py:56-121` at `56f0f665` validates its
existing 999/998 profile and additional tool/Plan Mode restrictions.

Keep host-specific profiles separate. Preserve common REVIEW no-web behavior and
B's existing protections; do not replace both profiles with a uniform file merely
for symmetry. The exact payload/digest/composition amendment still needs a
source-backed same-commit cross-host check before implementation. This answer
does not authorize weakening the current validator or marking V1-V5 passed.

## D-B2: no new permanent web-investigation evidence store

Owner: “수정하고 나서 정상 기능하면 별도 로그할 필요 없음 웹 검색은 너무 많이 남지 않아?”

Do not add the proposed private evidence-directory interface or a new permanent
full-prompt/page-fetch log. Preserve ordinary host masking, failure-only run logs
and retention. Use narrowly scoped temporary evidence for tests or an explicitly
requested investigation. Successful invocation alone does not establish successful
page interpretation; unresolved fetch/interpretation failures remain visible.

Proposed common wording change: the actual sent prompt must end with the shared
clause and use the existing host audit/redaction policy. Verify exact prompt
assembly in tests and inspect fetch/citation evidence in bounded live checks;
do not require a separate persistent exact-text store for every research call.
Affected locations are `prompts/investigation.md` order, R-INVEST, C29 and the
investigation unit. This proposal supersedes the earlier private-store proposal;
it does not erase already collected diagnostic evidence or silently change
adopted prompt bytes. C28's masked resolved-path representation is a remaining
implementation detail, not permission to log unmasked paths.

## D-5: B project roster location

Owner: “.agents/triad-review-legs.json (권장)”

B project discovery uses `.agents/triad-review-legs.json` under the target project
root. An absent file uses the common defaults. Existing schema, merge-by-name,
validation and adapter boundaries remain. A's host-specific location need not
change. This selects the location; runtime discovery is not yet implemented.

## Claude handoff and verification

Review the quoted answers and proposed applications against A `92c8afd` without
modifying A. Compare policy semantics rather than filenames; enumerate retained
denies and the exact profile inputs/digests. For D-B2, preserve masking and verify
the shared clause still reaches the actual vendor argv; do not add a storage
subsystem. For D-5, verify absent/invalid/override cases with the common schema.
Report any conflicting retained requirement at its source line before a host
implements a changed common contract. No owner question in these three topics
remains unanswered; implementation and cross-host review remain separate work.

## KI-AGY-URL-BODY-PREFIX: non-fatal known issue

Owner: “Known issue 로 기록하고 실패로 잡지말도록해”

B leader application: the reproduced AGY 1.2.7 `read_url_content` saved-body
suffix loss is a known external limitation. Its
[cross-site evidence](../spikes/2026-09-20-b-cross-site-and-producer-spikes.md#c29-incomplete-agy-url-bodies-are-not-github-only)
already records successful provider and wrapper exits. The exact internal
component remains unconfirmed.

Do not turn this observation alone into a TRIAD skill/dispatch failure, a failed
implementation obligation, or an automatic repair/retry trigger. Preserve the
actual terminal outcome; there is no new error token or permanent failure log
for this issue. No per-call repeat investigation is required solely because this
known issue exists.

This disposition does not declare incomplete web evidence complete. Report the
affected source/claim as incomplete or UNSURE when it matters. Independent
timeouts, nonzero provider outcomes, invalid final output/schema, identity or
integrity failures retain their existing handling. It does not waive review
admission or claim a vendor repair. Existing D-B2 masking and retention remain.
Future re-verification needs a relevant provider change or a requested probe,
not an automatic retry loop for each occurrence.

# Reflected error text is not a vendor failure signal

This clarifies the existing R-CLASSIFY/R-AUTH exclusion of answer/tool text and
preserves existing admission. It introduces no authentication route, native leg,
new vendor field or channel. C74 is written before dependent B correction.

B U2b R1 (632f426 plus dirty candidate) produced two verified regressions. Its
AGY authentication helper scanned `permission check failed for command "..."`
as vendor prose; a command naming `credentials-review.json` or containing `login`
became oauth-env/65. B already supports this reflected command shape in
`bin/antigravity_wrapper.py`'s `denied_post_completion` path and
`tests/test_antigravity_stream_json.py:test_plan_mode_admits_valid_verdict_after_denied_post_completion_write`.
The new classifier ran before that path and discarded its previously usable
verdict. Both plan and ordinary paths are covered by synthetic controls, not a
claim that these exact commands occurred in a vendor capture.

Separately, changing Claude extraction promotion from the extracted error text
to the full envelope made `permission_denials.tool_input` classify as token-limit,
server-capacity or schema-rejected. The authentication predicate needs original
streams to select the true error field; other classifications must retain their
previous restricted input. B tests reproduce all six ordinary/structured-route
combinations. Combined C74 RED: 10 failed, before correction.

A source inspected read-only at 2f91e8c: `3rd-Agent/wrappers/_common.py`
`_auth_carrier_stop` (1877 onward; AGY arm 1950 onward) has the schema reflection
exception but otherwise scans result.error. Its AGY driver checks this before
admission (`antigravity_wrapper.py:869`). `t13-agy-stream-digest.sh:394-415` also
uses the permission-denial command shape. A runtime outcome is NOT RUN; the
maintainer should verify its own admission path. A has no Claude CLI route, so
the Claude promotion regression is B-only. Neither native mechanism changes.

Required behavior: treat the command content as reflected text; keep genuine
own-stderr banner STOP, existing permission/admission controls and usable answers.
The entire permission-denial result error is excluded from authentication,
including any banner quoted inside that command. Only the separately measured
schema-report reflection has the own-line-banner exception. B R2 incorrectly
reused that exception for denied commands; two multi-line command-content
controls reproduce the overbroad STOP. No capture establishes whether AGY prints
the full denied command body. That uncertainty does not authorize a new carrier:
the unused/false-positive banner scan is removed in either case, before R3.
Do not broaden raw failure matching to unrelated JSON envelope fields. Unknown
vendor shapes remain unknown; these command-content controls do not establish
a new carrier or justify guessing AGY credit output location or exit.

Claude maintainer request: review this same spec commit and verify C74 against
your current AGY helper/driver. Report a source-backed disagreement or the exact
test and outcome; do not transpose the B-only Claude CLI change to your native
leg. B proceeds under the already settled no-reflected-tool-text contract.

Recorded non-blocking B limit from R2: classify_extraction retains the legacy
classify fallback after checking original authentication carriers. Gemini could
re-read derived error text as stderr on an exit-zero error envelope; the measured
failure basis is nonzero and no such exit-zero capture exists. No new parser or
fixture is added for that constructed shape. Revisit the helper split with a
measured failure or the separately planned classifier cleanup, not a speculative
vendor-shape expansion.

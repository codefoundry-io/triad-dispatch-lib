# Remaining U3 result-carrier assessment

2026-10-10; main3afc4d7, sharedc495b1b, B632f426 plus verified candidate;
read-only A1ea9cb3e. DL-113 recovery and DL-102 turn-timeout are completed B
candidate units. This note is assessment, not a new rule or implementation.

## DL-102 truncation: identify the answer channel before code

R-CLASSIFY says an answer carrying an own-line `<truncated N bytes>` or
`<truncated N lines>` marker is withheld, while a mid-sentence quote does not
count. B returns result.response on its raw route, but its schema route validates
and emits result.structured_output. Existing B tests deliberately preserve a
valid structured result independently of response transport decoration.

A1ea9cb3e antigravity_wrapper.py:905-934 selects response as the local `answer`
string and separately detects a structured-output dict. Its marker check at
1013 runs on that response before the structured-output handling at1023-1040.
Thus the source would also withhold a valid structured object if the separate
response carries an own-line marker. This is a source-derived boundary question,
not a measured vendor incident or a claim that current AGY produces that pair.

Please confirm whether the common marker rule applies to the answer channel
actually emitted, leaving an intact schema-validated structured_output usable
when only incidental response text is folded, or identify the existing rule and
capture that require discarding both channels. B will not guess a JSON-field
scan or copy A's response check into its schema path without resolving this.
No fresh paid failure generation or search for the expired September log is asked.

## DL-101 network error: existing measured row, separate unit

The frozen row records `There was a network issue connecting to the server,
please try again.` in the ERROR/empty-response/raw1 result; the ledger identifies
result.error. B currently classifies only stderr/status. A uses its typed
agy_classify_signals input, labelled before classification
(antigravity_wrapper.py:135-165), not raw output/answer/tool text.

An implementation must retain authentication and host/transport priority, known
vendor exit-map priority and the existing non-auth class order. Passing every
terminal error to broad phrase matching would also change unmeasured quota
placement; that is not authorized by this row. No implementation chosen here.
This independent row does not require resolving the truncation channel question.

## Independent follow-up: answer-channel investigation

Owner correction, 2026-10-10: B must investigate directly; A's explanation is
evidence, not a prerequisite for investigation or independent development.

Primary vendor documentation checked on 2026-10-10:
[AGY headless output](https://www.antigravity.google/docs/cli/headless/#structured-output-with-a-schema)
defines response as text and structured_output as parsed schema output, and
instructs consumers to read the parsed value from structured_output. It does
not document how a fold affects both fields or require discarding both.

Read-only A bc8a8a74 provides additional historical evidence:
- docs/agy-vendor-workarounds.md:174 records a 7.8KB live LegVerdict on the
  structured channel without folding. This is a retained report, not a fresh
  capture or proof that every current output is fold-exempt.
- The same document:458 and tests/e2e/wrappers/agy-stream/s1-real-stream.sh:36-42
  record two intact 26–27KB plain outputs on AGY1.1.9 on 2026-07-31. Therefore
  the older approximate 4KB observation is not a universal current size limit.
- A wrapper:909-934 itself calls structured_output the answer on structured
  routes, but :1013 checks response before selecting that channel. The latter
  ordering is not sufficient evidence that both channels must be discarded.
- B wrapper:422-471 and test_plan_mode_admits_native_structured_output_independent_of_response
  already use locally validated structured_output on schema routes.

B's conclusion from these sources: apply the marker rule to the selected answer
channel; an incidental response-only marker is not proof that a valid structured
answer was lost. Preserve existing schema, binding and original-JSON checks.
Do not invent recursive JSON-field scans or infer a fold solely from byte count.
The mixed-channel pair remains an unobserved vendor shape; a constructed test
can check channel selection but cannot prove vendor behavior. A's review of
this evidence is requested for cross-host coordination, not passive blocking.

A reply [6092564483](https://github.com/codefoundry-io/triad-dispatch-spec/pull/13#issuecomment-6092564483)
agrees with this channel interpretation and confirms that its response-first
refusal was a conservative host choice, not a shared rule or measured mixed pair.
R-CLASSIFY now states the selected-channel boundary; C43 records its controls.
A's present behavior remains an A fact; no paid failure generation is requested.

Owner follow-up: if the issue is AGY's web-search bug, ignore that vendor bug.
The reply concerns terminal answer selection, not a web-search failure. Tool
output is outside this answer check; no web-tool truncation scan, retries or
workaround is added. This is a bounded interpretation, not a new error catalog.

## Own-line CRLF boundary found by B implementation review

B review triad-agy-answer-truncation-20261010-r1 found a deterministic gap in
the candidate raw matcher: it accepts an LF-terminated marker line but misses
the same line ending in CRLF. Its `[ \t]*$` tail does not consume CR before LF.
The decoded response retains embedded line endings; B therefore returns ok/0.
B reproduced the exact source pattern with Python's standard regex engine.
Read-only A bc8a8a74 has the same pattern at wrapper:183 and uses it at:1013,
so the same constructed input exposes an A matcher gap as well. A's full CLI
path was not rerun. This is not a new captured vendor failure or web-search bug.

The existing own-line rule has no LF-only restriction. C43 now names LF and
CRLF positive controls for both byte and line markers; surrounding answer and
raw evidence bytes remain unchanged. B will minimally accept the line-ending CR
in its raw branch. A should apply the corresponding matcher correction in its
own host when implementing this row. No schema/tool scan, CR normalization of
the returned text, size limit or new recovery policy follows. This is a bounded
conformance correction, not a new design or native-leg requirement.

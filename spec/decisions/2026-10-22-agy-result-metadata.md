# Accept AGY result metadata without weakening verdict validation

## Authority and evidence

Owner, 2026-10-22, verbatim:

> 끄지 못하면 그냥 놔둬야지 왜 집착해 그거 쓸데마다 실패로 한정지으면 agy leg는 없애야해?

The leader proposed preserving `toolAction` and `toolSummary` in original output,
treating them as provider metadata rather than verdict fields, and retaining
failures for missing or invalid actual verdicts. The owner approved: `진행`.
This supersedes the earlier task-local instruction to reject these two fields
without a transport projection. It does not authorize accepting a missing or
invalid verdict, changing provider settings, or rewriting historical reviews.

Remote `main` was fetched at `f043c257ccd748371c34e9d1f23e32064e139354`.
Direct AGY 1.4.5 / `gemini-4-argon-high` / high diagnostics returned undeclared
top-level `toolAction`/`toolSummary` in both json and stream-json terminal outputs.
Input JSON Schema was valid and disallowed extra fields. Required `toolAction`
caused a finish toolbox duplicate-required error; a required string `toolSummary`
succeeded once. These establish compatibility needs, not identical behavior of
the two names or a universal vendor failure. The exact native insertion cause
is unconfirmed. Do not add these fields to the canonical verdict schema.

Official contract accessed 2026-10-22:
<https://www.antigravity.google/docs/cli/headless/>. It places schema output in
terminal `structured_output`; the host must preserve terminal/error precedence.

## Agreed behavior

`R-AGY-METADATA` / C80 is the normative rule. Parse original JSON strictly before
separation. Separate only the two known top-level names, only when not declared
as payload fields. Preserve all raw input and both metadata values. Validate the
projected payload with all existing schema and invocation-binding checks. Other
extras and nested fields are not removed. Missing results remain failures.

The library supplies `separate_agy_metadata(raw, *, declared_fields=())`, returning
fresh payload and metadata dictionaries. It accepts str/bytes original JSON and
an explicit tuple of declared top-level field names. Metadata values may be any
valid finite JSON values; they do not determine the verdict. It performs no
terminal, schema or binding admission. `extract_final` keeps its original-span
contract. `admit_output` uses separation only for the AGY carrier, then performs
the unchanged canonical validation. `validate_verdict` stays strict.

## Host effects and preservation

Codex owns its adapter integration. Its wrapper currently validates serialized
terminal structured output at `bin/antigravity_wrapper.py::_interpret_run` after
terminal recovery and original-JSON guards. Use separation at this boundary,
preserving existing denied-post-completion and finish-resubmission handling.
Legacy and v2 share it. Caller-declared metadata names remain ordinary validated
payload fields. A custom schema whose top-level declarations cannot be resolved
by the host may retain its existing validation behavior rather than discard data.

Claude and AGY hosts adopt independently; their current code is not changed by
this decision. Request review of this commit through their existing follow-up
PRs, with implementation/verification and release status recorded separately.
The common deterministic rule is shared; native execution and custody remain
host-owned. Canonical schema identities, all six bindings, negative verdicts,
duplicate/non-finite refusals, terminal failures, provider permissions and raw
receipts must survive.

## Verification and bounded plan

One functional unit: shared separation plus Codex adapter adoption. Expected
production delta: approximately +70/-5 lines, net +65; novel core below 50 lines,
excluding mechanically vendored library files. Tests/fixtures/docs are separate.
Library changes: output helper, AGY admission, root export and focused regressions.
Host changes: wrapper seam and regression coverage; exact verified wheel/pin
migration. Version, adoption documentation and provenance follow the changed bytes.

Measured candidate delta: authored library production +28/-3 lines and Codex
wrapper +61/-15 lines, excluding mechanical vendoring and identity pins. The
host's declared-field/alias discovery and strict original terminal-span parsing
explain the growth from the initial estimate; they implement the same approved
preservation rules. Tests, fixtures and documentation are counted separately.

1. Record C80 and the common rule before implementation; request host review.
2. Write failing positives for metadata-bearing actual verdicts; preserve strict
   negatives, custom declared names, original bytes and non-AGY behavior.
3. Implement and verify source, API compatibility, spec generation, sdist/rebuilt
   wheel and host wrapper/custody paths. Record native CI separately.
4. Exercise one fresh AGY call through the candidate adapter; retain raw and
   admitted payload. Do not repeat the field-disable investigation.
5. Run the required fresh complete project review on the candidate and rerun the
   previously blocked documentation review after the compatible route is verified.

No merge, publication or workstation installation is implied by this candidate.

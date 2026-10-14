# U1T parser evidence, 2026-10-10

Basis: B5f5dda5b; shared7fb5bb2f, remote main3afc4d7e; PR12
11934f11. A's model transport implementation is 9e16880d, inspected read-only.
PR13 agreement: comments6073991579 and6074188589. No new reply after6094950337
at this session's check. DL-148 is A-only brief handling, not a new model task.

The initial parser harness failed on an import before invoking any vendor.
Its failure is retained under parser/failure.md; successful commands and exact
stdout/stderr/argv are under parser-r2/*.json.

AGY1.3.3: separate `--model --help` exits0 with CLI help. Equals
`--model=--help` exits1 with JSON ERROR naming the exact model `--help`,
duration_seconds0, num_turns0 and zero usage. This directly establishes the
option interpretation difference, without paid review inference. The vendor's
invalid-model message happens to include its catalog; the harness did not call
a model-list command or use catalog membership for admission.

Claude2.1.289: `--model=opus` with `/model opus` exits0 and selects Opus5.5.
Both equals and separate `--help` model arguments with `/model --help` exit0,
emit a warning naming the unknown model, and return slash-command usage rather
than top-level CLI help. This confirms acceptance of both argv spellings in
this measured command, not model availability or eventual inference identity.
Do not change Claude's existing native argv solely for spelling uniformity.

Previously retained Gemini0.63.0 actual bundled yargs/parseArguments evidence
and 24 Python-wrapper parser cases remain authoritative for their measured
boundaries; no repeat provider call or installed0.60 substitution. Gemini's
separate option-shaped pin is misparsed; equals preserves the tested values.
Evidence: ../spec-plan-20261009/model-argv (relative to _runs), documented in
docs/status/2026-10-09-spec-investigations.md. NUL, arbitrary controls and future
vendor versions are not certified. No shell-injection/permission escalation
claim, new model grammar, model catalog, agent resolver or native-leg change.

Proposed bounded correction: equals-form model values at B's Python invocation
and Google preflight boundaries, AGY `_route_args`, and Gemini raw/formal
`build_cmd`. Preserve Claude native option construction, legacy Gemini auto,
model/effort settings, existing preflight/identity/binding and one provider call.
Related receipt builders/validators must agree with the emitted AGY route args.
Independent diagnosis, shared cases, fresh executor RED/GREEN and a complete
fresh implementation review precede a completion claim.

Primary sources: https://www.antigravity.google/docs/cli/headless/ documents
pre-inference invalid-model errors; https://code.claude.com/docs/en/cli-reference
documents --model and print/session controls but does not prove parser grammar.


## Shared disposition and ownership

This finalizes the observable requirement agreed by A in PR13 comment6073991579
and implemented at A9e16880d. It does not prescribe A's native leg or require a
Claude --agent. A's wrapper source uses equals-form model values; its full
tests are A-reported, not rerun here. B's dependent implementation is pending.
Both hosts should report C18/C34 coverage against this same rule; no new A code
port is requested. Existing schema type/nonblank rules remain unchanged.

## B implementation scope after independent diagnosis

Claude opus/xhigh, Google Pro/high and fresh Codex Astra/high independently
reviewed the source/evidence. B narrows AGY equals encoding to model values
starting with `-`. Ordinary and legacy AGY pins keep their existing spelling;
no legacy receipt validator or CLI floor change follows. This avoids asserting
unmeasured ordinary-pin compatibility on older AGY releases. The previously
broken option-shaped path is measured on AGY1.3.3; older/future versions are not
certified. A's ordinary AGY1.3.2 equals dispatch is A-reported evidence.

B uses long equals encoding at generated Python-wrapper and Google preflight
boundaries and Gemini raw/v2 dispatch. Both v2 receipt builders describe the
actual transport. Claude native argv and legacy Gemini `-m auto` remain.
String concatenation preserves type failures; no guessed null-model fallback is
added. Current candidate is +8/-9 production lines across five files.
Fresh bounded RED:20failed/76passed/4skipped; GREEN and formal review pending.
The earlier RED22/74/4 included unnecessary ordinary-AGY spelling assertions;
that evidence is retained, and the revised RED precedes product changes.

This is a host encoding choice within the settled common result contract, not
a requirement for A to copy B's conditional spelling. Both hosts must preserve
the same model value. No additional A native or wrapper change is requested.

Features preserved: opaque user pins, defaults, native ownership, preflight
capabilities/authentication, original model and effort settings, exact receipts,
one terminal rejection, and no catalog or fallback. Verification: real Python
wrapper consumers plus vendor argv capture; retain pinned actual-parser evidence
separately from provider-free fixtures. Fresh dedicated RED/GREEN and host review
are required before B claims the correction. No adoption or release is implied.

## Older CPython parser finding from B review

U1T R1 returned all-four SAFE and matching integrity, with one Minor finding
subsequently reproduced. CPython issue109475 documents `--model=--` becoming
an empty list before the argparse fix. Official tagged argparse modules
v3.12.1 and v3.12.2 were loaded on B's Python3.12.13: the first returns `[]`,
the second the exact string `--`. Both preserve `--help` and an ordinary pin.
This is actual parser-module evidence, not a full old-interpreter/provider run.
SHA256: v3.12.1 `97e4748d9dd71994c979ddd3245bc84a209cf18e683a6c5a663886224f01d752`;
v3.12.2 `a2014aea48aa2260b7bafb4c64642da67bdb1dadb47046652c941b30972243a7`.
Primary source: https://github.com/python/cpython/issues/109475 and
https://github.com/python/cpython/blob/v3.12.1/Lib/argparse.py .

B's raw wrappers test the parsed model for truthiness, so this malformed value
can be omitted. Its documented Python3.12+ floor includes the affected release.
Bounded correction: refuse a non-None non-string parsed model before prompt or
provider I/O. Preserve the Python floor, normal/default behavior, opaque string
pins and vendor argv; do not guess the lost value or add a model-name grammar.
R-MODEL and C18/C34 now state the no-omission boundary explicitly. New fresh
RED/GREEN and a complete review are required; R1 does not approve new bytes.

A59fbfd1 source: Gemini checks `args.model.strip()` immediately after parsing;
AGY also validates model before dispatch. A is asked to check its behavior on
this malformed parser result, not to copy B's native leg or raise a version
floor. B has not executed A's wrappers or proved their old-interpreter outcome.
Any A fix remains A-owned. No installation, revision adoption or release.


## B implementation and final verification

B source `ed8b76f13f03d96d35f7b795159a528aa061622c` is pushed and verified against
`origin/codex/opus-5-5-default`. Production +17/-9, net8, six files: generated
Python-wrapper/Google-preflight model tokens, Gemini raw/v2 vendor tokens,
conditional AGY option-shaped tokens, matching v2 receipt fields and immediate
three-wrapper non-string refusal. No native argv/spawning/model/effort change,
new grammar, model-catalog gate, fallback or user-environment change.

Final dedicated GREEN-compat:82 affected tests with current argparse and46
transport tests with the SHA256-checked official3.12.1 argparse module passed;
four source-skill validators passed. Source/status and existing logs unchanged;
exact invocation-owned fixture removed. Python3.12.13/pytest9.0.3 on macOS.
The full2326passed/4skipped run uses identical production and predates the final
test-only compatibility correction. No post-correction full run, full old
interpreter, Ubuntu or live model-availability certification is claimed.

R2 identified that new literal-double-hyphen tests wrongly required old-parser
success. RED-compat11failed/35passed reproduced it; the tests now verify actual
preservation or pre-I/O refusal with no skips or version guessing. Earlier
RED/failed review evidence remains retained; approvals were not carried forward.
Fresh complete `triad-model-transport-20261010-r3`: all four selected reviewers
SAFE, ALL_SELECTED_APPROVED / ROUND_INTEGRITY_OK. Claude's optional future
encoder-drift suggestion identifies no current mismatch; the existing both-route
dispatch/receipt test checks parity. No new abstraction or required backlog.
All producers terminal, bindings verified, findings adjudicated, custody exported
and exact review stage/cwd cleaned. Hidden runtime settings remain UNEXPOSED.

Current main3afc4d7, PR12 11934f11, read-only A0be173bf clean. A's later changes
are documentation/comments; its old-parser handling remains A-owned and not
executed by B. Source completion is separate from adopted revision, installation,
merge, release and the unfinished whole spec-to-code task.

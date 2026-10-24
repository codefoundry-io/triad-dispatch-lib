# Python library API contract

This reference describes the published `0.1.0.dev7` implementation of the 41
package-root exports in `triad_dispatch_lib`: 23 functions, nine dataclasses and
nine exception types. It records existing Python behavior; it does not change
the package's version. The adopted [compatibility policy and gate](../../docs/api-compatibility.md)
protect this public surface from the declared dev4 floor. Wire fields, allowed roster
values, phases and canonical clauses remain authoritative in their respective
[sources](README.md#one-source-per-fact). See the [conformance map](library-conformance.md)
for rule/case/test coverage and [host adoption](../../docs/host-adoption.md)
for execution and custody responsibilities.

The runtime performs no provider execution or remote schema retrieval. It checks
packaged resource manifests and payload digests on use; those checks establish
consistency, not authenticity or a complete host/spec revision identity. Callers
must bound input sizes and supply ordinary finite JSON-like configuration data.
Type annotations describe accepted values but dataclass construction itself does
not validate them. Validation occurs at the operations described below.

The additive [common runtime compatibility API](runtime-compatibility-api.md)
defines strict immutable descriptions, explicit/legacy binding selection and
conservative retention decisions. Artifact authentication, actual compatibility
verification, native execution and installation remain host responsibilities.

## Original JSON and invocation admission

```python
parse_json(raw: str | bytes) -> object
validate_binding(expected: dict) -> None
validate_verdict(raw: str | bytes, *, expected: dict) -> dict
```

`parse_json` returns a fresh decoded JSON value, including scalar values. Bytes
must be UTF-8. Duplicate decoded object-member names at every depth, nonfinite
numbers (including floating-point overflow), malformed JSON and decoder nesting
limits refuse with `AdmissionError`. It performs no fence stripping, repair,
substring selection or coercion. Python integer-conversion limit failures are
reported as `invalid_json`.

`validate_binding` requires exactly `review_id`, `family`, `content_digest`,
`leg_name`, `attempt` and `route`, with the constraints in
[`leg-verdict.schema.json`](../contracts/leg-verdict.schema.json). Google routes
are `agy` or `gemini`; other families use null. Success returns `None` and does
not mutate the supplied binding. Invalid bindings raise `invalid_expected`;
packaged validation faults raise `ContractError`.

`validate_verdict` strictly parses original text, validates the complete v2 wire
schema, validates `expected`, then compares all six binding values. It returns
the parsed verdict dictionary, preserving all fields and schema-valid negative
verdicts. Schema refusal precedes expected-binding refusal when both are bad.
Admission is not an agreement decision. Schema integer semantics apply, rather
than an additional Python `type(value) is int` rule. The operation neither
mutates `expected` nor returns shared schema state; nested result members remain
ordinary mutable dictionaries/lists.

`AdmissionError(code)` retains its constructor, fixed message, `.args` and
`.code`. Every instance also has `.field: str | None`,
`.path: tuple[str | int, ...] | None` and `.missing: str | None`, initially `None`.
Library-generated
`binding_mismatch` sets only `.field` to the first mismatch in the six-field
order above. `schema_violation` sets `.path` to
`tuple(validation_error.absolute_schema_path)`: jsonschema's schema diagnostic
path produced while evaluating the trusted canonical schema, including keyword
names and possible composition indexes. Reference (`$ref`) and conditional (`if`)
traversal hops may be omitted; it is not necessarily a JSON Pointer into the
source schema document.
It is never the instance path and does not contain arbitrary provider property
names or values. An empty tuple denotes the schema root. Which violation wins
among simultaneous schema failures is not a stable diagnostic contract. Other
codes leave these attributes `None`; no raw validator error enters the message.

Only the selected canonical `required` violation may set `.missing`. When its
`validator_value` is a list of strings and its `instance` is a dictionary, the
first name in that required-list order absent from that object is returned.
Otherwise it remains `None`, including selected non-required violations even
when other required data is absent. Names come only from the trusted schema;
the instance is consulted only for membership. This does not change violation
selection or validation order. Root required paths are `("required",)`; finding
required paths are `("properties", "findings", "items", "required")`, without
a finding instance index. `.missing` never extends `.path`.

Duplicate provider-chosen names remain undisclosed: no `.member` API is provided.
The owner settled these separate boundaries in the
[approved adoption design](../../docs/design/2026-10-15-adoption-apis.md). Hosts
retain ownership of any strict-parser deviation and consumer adaptation.

The value-free diagnostic guarantee covers `.code`, `.field`, `.path`, `.missing`,
and the fixed message/`.args`. Python exception internals, including `__context__` and
tracebacks, retain their existing behavior and may reference validator errors
or input data. `raise ... from None` suppresses displayed chaining, not those
internal references.

## Rosters and contract loading

```python
load_roster_contract() -> dict
merge_roster(defaults: dict, overrides: str | bytes | None = None) -> dict
validate_resolved(roster: dict) -> None
resolve_roster(defaults: dict, overrides: str | bytes | None = None) -> dict
select_entries(roster: dict) -> list[dict]
```

`load_roster_contract` returns fresh verified Draft 2020-12 schema data with the
canonical roster schema identity. The schema root validates override documents;
`$defs.resolvedRoster` validates complete rosters. It neither supplies defaults
nor validates a caller roster. Unreadable, inconsistent or invalid packaged
schema data raises `ContractError`; there is no resource cache or remote lookup.

`merge_roster` validates the supplied complete defaults against the resolved
schema, then checks exact duplicate names, before parsing an optional override.
It validates the override schema, then exact duplicate names, and returns an
independent merge without final validation. Defaults refuse before override
parsing, and schema refusal precedes duplicate-name refusal at each stage.
All entries validate, including disabled entries. Python `None` means no
override; original JSON `null` is an invalid override document. Any override
parser refusal becomes `RosterError("invalid_json")`. Schema, duplicate-name
and validation nesting refusals have their respective roster codes.

`validate_resolved` independently loads the verified offline schema, validates
the complete resolved schema, then checks exact duplicate names. It returns
`None` without mutation. `resolve_roster` preserves its dictionary return and
performs input merge and final validation using one verified schema snapshot.
The split composition is merge, validate, then return the merged dictionary.

An intermediate merge is not resolved or runnable data: it may contain
incomplete new entries or incompatible inherited vendor blocks. Host capability,
route, preset, collision and custom diagnostic checks must safely handle these
and remain host-owned. Validate the exact document before consumption; any later
mutation requires revalidation. Neither function prunes inherited vendor blocks.

Names match exactly and case-sensitively. Matching entries retain their original
slot; new names append in override order. Dictionaries merge recursively;
non-dictionary values replace with independent copies, including schema-allowed
null. Missing members inherit. Top-level override fields other than `legs`
replace their counterparts. There is no deletion operation. A vendor change
that leaves incompatible inherited vendor blocks refuses final validation.
The returned envelope is independent of caller data. An empty schema-valid
roster can resolve successfully.

`select_entries` revalidates a complete roster and returns independent deep
copies of enabled entry dictionaries in roster order. It refuses an empty enabled
selection with `empty_selection`. It does not filter on family or acceptance,
sort entries, resolve routes or check native capabilities. Model/effort strings
and nulls remain opaque requested configuration; no provider defaults are added.

`RosterError(code)` keeps its constructor, stable codes, fixed messages and
`.args`. Every instance initializes `.path: tuple[str | int, ...] | None`,
`.instance_path: tuple[str | int, ...] | None`, `.missing: str | None` and
`.document: str | None` to `None`. The additive `.instance_path` was published
in dev7; the other three attributes were published in dev4. Only a
library-raised `schema_violation` sets them: `.path` is the first selected validator error's
`absolute_schema_path`, `.instance_path` copies `tuple(absolute_path)` from that
same error, and `.missing` is the first absent schema-defined name
in that selected `required` list, using the guarded rule described for admission.
No child-error search or second validation pass is performed. A non-required
winner leaves `.missing=None` even if another violation concerns missing data.
Parser, duplicate-name, empty-selection and nesting refusals keep all four `None`.

`.document` identifies the evaluated document: `defaults`, `override`, or
`resolved`. The last covers standalone validation, final resolution and selection
revalidation; it does not attribute a merged property to an original input.
Overrides evaluate from the schema document root; defaults and resolved rosters
evaluate through `$defs/resolvedRoster`. An empty tuple denotes that evaluation
root. `$ref` and `if` hops may be omitted: `.path` is neither an instance pointer
nor necessarily a JSON Pointer into the source schema. Do not invent a prefix.

`.instance_path` locates the failing instance within `.document`: a fourth-entry
timeout is `("legs", 3, "timeout_s")`. Here `()` means the evaluated document root;
`None` means unavailable. Resolved indices refer to final merged order, including
preserved default slots and appended entries, not override provenance. This is a
tuple of canonical field names and integer indices, not a rendered JSON Pointer.

For a Google leg with `route="agy"` and neither `agy` nor `gemini` block, the
selected path is `("properties", "legs", "items", "allOf", 1, "allOf", 2,
"then", "anyOf")` and `.missing=None`. Adding `gemini={}` instead selects
`("properties", "legs", "items", "allOf", 1, "allOf", 2, "then", "allOf", 0,
"then", "required")`
with `.missing="agy"`. These are the tested route-block vectors, not a promise
that all combinations of simultaneous failures select the same error.
Both errors have `.instance_path=("legs", index)`: required and aggregate errors
identify the containing object, without searching child errors for a leaf.

The value-free roster guarantee covers these attributes, `.code`, fixed text
and `.args`. `.path` and `.missing` use trusted schema metadata; `.instance_path`
uses canonical instance field names and indices. The verified canonical roster
schema has fixed properties and closed objects, so paths disclose no input values,
entry names or arbitrary unknown-key spelling. Additional-property errors identify
the containing root, entry or adapter object. Arbitrary dynamic-key schemas are
outside this API; future schema extensions must reassess this guarantee. Python
exception internals,
including `__context__` and tracebacks, may retain validator/input references;
suppressed displayed chaining is not internal erasure. No `.member`, `.unknown`
or raw validator-error API is added. Issue #9 is
[closed/completed for its requester](https://github.com/codefoundry-io/triad-dispatch-lib/issues/9#issuecomment-6373642690)
with dev7 instance locations. Arbitrary unknown-key spelling remains outside
this release; a new concrete diagnostic need may receive a later owner decision.
Exact host diagnostic formatting remains host-owned.

## Transport-object shape validation

```python
validate_transport_receipt(doc: dict) -> None
```

Supply the already parsed nested `transport` object, not a whole host receipt.
The operation returns `None` without mutation for the unchanged canonical
[`receipt-fields.json`](../contracts/receipt-fields.json) shape. Wrong JSON
types, missing/extra members, invalid vocabulary and native-route constraints
raise `ReceiptError("schema_violation")`. Schema integer semantics permit
integral floats; binary/version may be null when unobserved and observed CLI
versions remain opaque strings. No model policy or version-equality gate is added.

`ReceiptError(ValueError)` has `.code` and fixed messages:
`Transport receipt violates the canonical schema.` (`schema_violation`) and
`Transport receipt nesting exceeds the validation limit.` (`nesting_limit`).
Neither interpolates caller data. Python exception-internal limits described
above still apply. Missing, inconsistent or invalid packaged resources raise
`ContractError`; unresolved references never retrieve remote data. The verified
receipt bundle retains the canonical schema identity and six-field manifest.

This API performs no parsing, caller-path reading, execution or authenticity
check. Hosts still compare invocation identity and `wrapper_cmd`, bind the actual
route/binary/observed version and current attempt, validate envelopes, and enforce
stdin/execution observations, ownership, seals, reads and collection. Shape-valid
data is neither authentic evidence nor approval; selective adoption needs no
coordinator or native execution change.

## Prompt rendering

```python
render_review_clauses(
    *, family: str, host: str, review_date: str,
    review_web_authorized: bool, replacements: dict,
    review_kind: str = "pre-merge", route: str | None = None,
    agy_hook_active: bool = False, with_manifest: bool = False,
) -> str | tuple[str, list[dict[str, str]]]
render_data(value: str) -> str
render_investigation_prompt(
    prompt: str, *, family: str, route: str | None = None,
    web_authorized: bool = False,
) -> str
```

Supported profiles are `codex`, `claude` and `google`, on hosts `A` and `B` for
formal clauses. Google requires explicit `agy` or `gemini`; other families require
`route=None`. `review_date` is an explicit valid `YYYY-MM-DD` calendar date.
Web/hook flags must be actual booleans. `review_kind` must satisfy the canonical
phase schema. A true hook flag is accepted only for Google/AGY on host A.

`replacements` must contain exactly `worktree`, `brief-file`, `packet-files`,
`review-id`, `content-digest`, `leg-name` and `attempt`; Google additionally
requires `gated-patch-file`. Values are caller-encoded strings without literal
CR/LF. Empty strings and placeholder-looking values are accepted. Encoding,
path validity and correspondence to the actual invocation remain caller duties.
The library owns the phase/date/web-policy substitutions and Google route.

`render_review_clauses` selects canonical fenced blocks in canonical order,
omits host-inapplicable and inactive-hook clauses, selects the phase purpose and
joins blocks with one blank line. Substitution is one pass; inserted caller data
is never interpreted again as a placeholder. Canonical Claude shape literals
remain literal. The result is the clause portion, not a complete packet or
objective/criteria/residual assembly. Invalid arguments raise `PromptError`;
detected asset, schema, order or placeholder faults raise `ContractError`.

`with_manifest` must be an actual boolean. Its default `False` returns the
same rendered string. `True` returns `(text, manifest)`, with the identical
text and a fresh mutable list of fresh `{ "name": str, "sha256": str }` rows.
Rows follow canonical rendered clause order, retaining the `common:` prefix
and resolving the phase-purpose name before recording. Inactive hooks and
other-host clauses are omitted. Each SHA-256 hashes the selected fenced
clause's UTF-8 bytes after the parser's trailing-LF removal, before date,
phase, route or caller substitutions, and without joining blank lines.
Immediately after the first selected parent containing `<review-web-policy>`,
one row records the selected `common:review-web-permission` or
`common:review-no-web` clause using its own unexpanded source bytes. This
dependency row is not another top-level emitted block. Literal caller data
cannot create rows; replacement changes do not change hashes, and mutation
of a returned manifest cannot affect later calls. Both modes use the same
verified bundle load and rendering path. Clause hashes describe selected
source clauses, not final-prompt identity, bundle identity, execution
attestation or custody proof. No additional package-root export is introduced.

`render_data` accepts any string and returns the canonical data caveat followed
by an adaptive backtick text fence containing its `json.dumps(...,
ensure_ascii=True)` representation. The fence is at least three backticks and
longer than every input backtick run. The input can be recovered by JSON decoding
the fenced payload. This function performs no placeholder substitution or
once-only packet assembly check. Non-text input raises `PromptError`.

`render_investigation_prompt` validates profile/text/web arguments. It returns
the input unchanged unless the profile is Google and web is authorized; that
case appends two LF and the canonical web-evidence suffix last. Gemini uses the
canonical Gemini tool names. It does not deduplicate an existing suffix or add
formal ballot clauses. Invalid arguments raise `PromptError`; detected suffix
or bundle faults raise `ContractError`.

These renderers consume trusted canonical assets, not arbitrary Markdown.
Deliberate asset checks do not promise normalization of every possible malformed
bundle into one exception type. They grant no execution or web authority; hosts
bind the actual date, permissions, encoded values and final assembled prompt.

## Provider carriers and agreement

```python
extract_final(output: ProviderOutput) -> str | bytes
admit_output(output: ProviderOutput, *, expected: dict) -> dict
evaluate_agreement(
    expected_by_leg: dict[str, dict], outputs: dict[str, ProviderOutput],
    *, integrity_ok: bool,
) -> AgreementResult
```

`extract_final` first checks carrier/metadata types, completion, timeout,
transport failure, successful exit and text/bytes stdout, in that order.
Metadata booleans must be actual booleans; exit code must be an actual integer,
or `None` only for `native-final`. A successful exit is zero or native null.
It then applies these carrier rules:

| Carrier | Extraction contract |
| --- | --- |
| `native-final` | Return original stdout unchanged, without JSON parsing or marker removal. |
| `claude-json` | Strict object envelope; `structured_output` must be an object. Return its original JSON source span, retaining str/bytes carrier type. |
| `gemini-json` | Strict object envelope; `response` must be a string. Return that decoded string intact, including when stdout was bytes. |
| `agy-stream-json` | Strict UTF-8 and LF-delimited JSON objects, ignoring blank lines and non-result objects. Exactly one `event="result"` record must contain object `result`, `status="SUCCESS"` and object `structured_output`. Return that structured output's original source span. Malformed records/tails or multiple terminals refuse. |

Claude/Gemini envelopes reject a present non-boolean `is_error`, true `is_error`,
or any non-null `error` value (including false or empty containers). Claude also
rejects non-null non-string `subtype`, `error`/`error_*` subtypes,
`terminal_reason` of `error`/`api_error`, and status
`ERROR`/`FAILED`/`error`/`failed`. Missing/null subtype is allowed. Gemini does
not apply those additional Claude-specific predicates. The strict AGY carrier
does not implement C23 same-run finish recovery. Parsing errors may raise
`AdmissionError`; carrier/terminal errors raise `OutputError`.

`admit_output` validates `expected` first, checks metadata and carrier/binding
compatibility, extracts original final JSON, and runs full verdict admission.
For `agy-stream-json` only, it first separates undeclared top-level AGY metadata
using the canonical schema's property names. The original `ProviderOutput` and
`extract_final` result stay unchanged; the returned verdict contains the validated
payload. Generic `validate_verdict` and all other carriers remain strict.
Claude, Gemini and AGY carriers require their matching family/route. Generic
`native-final` can carry any valid binding, trusting the host's supplied final
JSON and truthful observations. It performs no metadata separation. For C23
recovered AGY output, hosts retain original bytes and metadata, apply C80 separation
when needed, then serialize the projected payload for this strict carrier.
Extraction alone is not admission and cannot establish provider execution,
attempt currency or packet custody.

`evaluate_agreement` requires an actual boolean integrity result and a nonempty
expected-binding dictionary. Selected keys must be nonempty strings matching
each binding's `leg_name`; every binding must share review ID/content digest.
`outputs` must be a dictionary with string keys, no unselected names and only
`ProviderOutput` values. Invalid caller maps raise `AgreementError`.

Every selected entry counts, including repeated families and informational
entries. The reducer re-admits each supplied original output. Missing output,
`AdmissionError` or `OutputError` becomes a per-leg reason; valid negative
verdicts are retained with `negative_verdict`. `ContractError` propagates.
Agreement requires true integrity and no reasons. False integrity alone leaves
`reasons` empty. Output maps follow selection iteration order. Inputs are not
modified; result maps are fresh and mutable, and `agreed` is a computed snapshot
that does not recompute after callers mutate them. Collector host faults and
selection-deviation records remain host responsibilities.

### AGY metadata separation

```python
separate_agy_metadata(
    raw: str | bytes, *, declared_fields: tuple[str, ...] = (),
) -> tuple[dict, dict]
```

Strictly parse the original JSON before any separation, preserving duplicate,
escaped-duplicate, non-finite, encoding and nesting refusals. Non-object input
raises `OutputError("invalid_envelope")`; a non-tuple or non-string member in
`declared_fields` raises `OutputError("invalid_output")`. Parsing errors retain
their `AdmissionError` codes and precede argument/shape checks.

Return fresh payload and metadata dictionaries. Only undeclared top-level
`toolAction` and `toolSummary` move to metadata, with their exact parsed values.
Any valid finite JSON value is metadata; it does not determine the verdict.
Declared names, other unknown names and nested members remain payload. Input
text/bytes is never changed. The function does not validate a caller schema,
bindings, terminal state or whether the payload is a verdict. Hosts retain
the original provider output and validate the payload afterward. See
[R-AGY-METADATA](review-rules.md#R-AGY-METADATA).

## Bounded host callbacks

```python
async def run_review(
    requests, invoke, *, preflight, integrity_check, max_concurrency: int,
) -> ReviewRun: ...
async def run_investigations(
    requests, invoke, *, preflight, max_concurrency: int,
) -> tuple[CallOutcome, ...]: ...
```

`requests` is consumed into a nonempty tuple and deep-copied before dispatch.
`max_concurrency` must be an actual positive integer and callbacks callable.
Requests must have the appropriate request type, string prompt and complete
canonical entry dictionary. Entries must be uniquely named, enabled and have
resolved Google routes. Formal expected bindings must match entry name/vendor/
route and share review ID/content digest. Invalid coordination inputs raise
`DispatchError` before invocation; package failures can raise `ContractError`.
Copying arbitrary custom Python objects is outside the ordinary JSON-like input
contract and is not a general exception-sanitization boundary.

Each callback receives an independent deep copy of its prepared request.
Callbacks must be awaitable when called. All preflights settle successfully
before any invoke callback starts. Each successful preflight returns exactly
`None`; ordinary exception, self-cancellation, non-None result or timeout yields
aggregate `DispatchError("preflight_failed")`, without per-entry diagnostics.
Invoke runs once per entry without retry. Both stages use bounded concurrency
and each entry's `timeout_s`, starting after acquiring that stage's slot.
Outcome order is request order, independent of completion order.

A formal invoke must return `ProviderOutput`; any other return is a failed
outcome. Callback return establishes delivery, not admission. After invokes,
`run_review` calls `integrity_check()` once without arguments or a built-in
timeout. Only exact `True` permits agreement; ordinary exception,
self-cancellation, false or non-boolean result blocks agreement while preserving
outcomes. Fresh integrity and classification of collector faults are host-owned.

Investigations first apply `render_investigation_prompt` to each prepared prompt
and then use the same preflight/concurrency/lifecycle model. Invoke values may
be arbitrary objects; they are returned without verdict admission or a vote.
The library does not copy callback-returned values into outcomes.

Ordinary callback exceptions and callback self-cancellation become `failed`;
expired calls become `timed_out`, even if cancellation cleanup later returns a
value. `ContractError` propagates after owned peers settle, including when a
timed-out callback raises it during cleanup. Parent cancellation propagates only
after owned callback tasks settle; repeated cancellation does not abandon
cleanup. If parent cancellation is observed while draining, cancellation takes
precedence over a competing callback contract failure. The contract does not
promise a total ordering for unrelated asynchronous exceptions.

Wait-setup errors after task creation also cancel and settle the created
callback before propagating. There is no operational timeout maximum beyond the
schema; unschedulable values can raise runtime scheduling errors. Callbacks must
cooperate with cancellation and await their own native cleanup. The library
cannot force termination or bound cleanup time for uncooperative callbacks.

## Exported dataclasses

All nine are `frozen=True`: ordinary field reassignment is refused, but nested
objects are not deeply immutable. Constructors perform no schema/admission
checks. Fields below are in constructor order; only shown defaults are optional.

| Type | Fields | Meaning |
| --- | --- | --- |
| `ProviderOutput` | `carrier: str`, `stdout: str \| bytes`, `exit_code: int \| None`, `completed: bool`, `timed_out: bool = False`, `transport_failed: bool = False` | Host-observed terminal carrier; validated on extraction/admission. |
| `ReviewRequest` | `entry: dict`, `expected: dict`, `prompt: str` | Formal entry, six-field binding and complete caller prompt. |
| `InvestigationRequest` | `entry: dict`, `prompt: str`, `web_authorized: bool = False` | Ordinary perspective request; no formal binding or ballot. |
| `CallOutcome` | `name: str`, `status: str`, `value: object \| None`, `error_code: str \| None` | Coordinator emits `completed` with returned value and null error; `failed` with null value/`callback_failed`; or `timed_out` with null value/`timed_out`. A completed investigation can itself return null. |
| `ReviewRun` | `outcomes: tuple[CallOutcome, ...]`, `agreement: AgreementResult` | Ordered callback delivery plus independently computed admission/agreement. |
| `AgreementResult` | `agreed: bool`, `verdicts: dict[str, dict]`, `reasons: dict[str, str]`, `integrity_ok: bool` | Snapshot result; nested maps/verdicts remain mutable. |
| `ConsumerBinding` | `schema: str`, `consumer: str`, `baseline_digest: str`, `library_digest: str`, `adapter: str`, `capabilities: tuple[str, ...]`, `commands: tuple[str, ...]`, `context_digest: str`, `binding_id: str` | Exact consumer context; validation derives its identity and normalizes collections to sorted tuples. |
| `RuntimeDescriptor` | `schema: str`, `artifact_digest: str`, `commands: tuple[str, ...]`, `capabilities: tuple[str, ...]`, `supported_bindings: tuple[str, ...]` | Host-authenticated runtime declaration; operations revalidate tuple fields and exact declared support. |
| `RuntimeRetention` | `retain: tuple[str, ...]`, `remove: tuple[str, ...]`, `diagnostic: str` | Sorted retention/removal decision; performs no lifecycle operations. |

The [common runtime API](runtime-compatibility-api.md) defines the new records'
validation, identity, selection and conservative retention behavior. Their public
constructors do not validate inputs; every consuming operation revalidates them.

## Exported exception families and emitted codes

These inventories describe codes emitted by current operations, not permission
to construct exceptions with arbitrary strings. Human-readable messages are
not a payload channel or a parsing interface. Coded exceptions have `.code`;
`AdmissionError`, `RosterError`, `ReceiptError` and `RuntimeCompatibilityError`
explicitly declare it stable. Runtime compatibility refusals use fixed,
value-free messages. `ContractError`
and `PromptError` have no library-defined `.code`. The adopted compatibility
floor also protects selected actual operational outcomes, including
`extract_final` emitting `OutputError` codes `invalid_carrier` and `timed_out`,
and agreement reasons `missing_output` and `negative_verdict`. Constructor checks
preserve `.code` for tested constructor inputs; constructing
`AgreementError('empty_selection')` or `DispatchError('invalid_requests')` alone
does not establish which operations emit those codes. This inventory alone
adds no blanket code/version stability promise beyond the scoped
[compatibility policy](../../docs/api-compatibility.md).

| Exception | Base | Current emitted codes / role |
| --- | --- | --- |
| `AdmissionError` | `ValueError` | `invalid_json`, `invalid_utf8`, `duplicate_member`, `nonfinite_number`, `invalid_input_type`, `nesting_limit`, `schema_violation`, `invalid_expected`, `binding_mismatch` |
| `RosterError` | `ValueError` | `invalid_json`, `schema_violation`, `duplicate_name`, `empty_selection`, `nesting_limit` |
| `ReceiptError` | `ValueError` | `schema_violation`, `nesting_limit` |
| `RuntimeCompatibilityError` | `ValueError` | `invalid_descriptor`, `invalid_binding`, `unsupported_schema`, `invalid_selector`, `missing_context`, `unknown_binding`, `ambiguous_binding`, `unsupported_binding`, `command_mismatch`, `capability_mismatch`, `invalid_inventory`, `incomplete_inventory` |
| `OutputError` | `ValueError` | `invalid_output`, `invalid_carrier`, `not_completed`, `timed_out`, `transport_failed`, `nonzero_exit`, `invalid_envelope`, `terminal_failure`, `missing_terminal`, `multiple_terminals`, `carrier_mismatch` |
| `AgreementError` | `ValueError` | `invalid_expected_map`, `invalid_binding`, `invalid_outputs_map`, `invalid_output`, `empty_selection`, `name_mismatch`, `mixed_basis`, `extra_output`, `invalid_integrity` |
| `DispatchError` | `ValueError` | `invalid_concurrency`, `invalid_callback`, `invalid_requests`, `empty_selection`, `invalid_entries`, `disabled_entry`, `unresolved_route`, `invalid_binding`, `binding_mismatch`, `mixed_basis`, `preflight_failed` |
| `PromptError` | `ValueError` | Invalid rendering arguments; no code inventory. |
| `ContractError` | `RuntimeError` | Unavailable, inconsistent or invalid packaged validation/prompt contract; not a reviewer verdict. |

Agreement per-leg reasons are `missing_output`, `negative_verdict`, or a
propagated admission/output refusal code. Coordinator outcome error codes are
only `callback_failed` and `timed_out`; they do not expose callback exception
messages or classify a native CLI failure. Coded input/terminal errors use fixed
messages without interpolating untrusted provider contents. Callers should not
infer error precedence beyond the explicit operation ordering above.

## Internal mechanisms and host boundary

Module helpers such as `json_member_span`, `parse_clauses`, bundle-manifest
functions and private coordinator helpers are implementation mechanisms, not
additional package-root API exports. Repository `tools/*smoke.py`, asset
generation and wheel verification are test/authoring support with their own
documented inputs; their filesystem receipt protocol is not a runtime library
transport API.

Hosts retain native spawning and subprocess custody, capability/model/effort
resolution, permissions/authentication, provider/version compatibility, Google
route discovery and existing Gemini workarounds, original carrier capture and
native marker removal, AGY recovery and failure classification, packet/attempt
sealing and currency, fresh integrity checks, collector host-fault handling,
deviation evidence, installation and release. This API neither supplies those
guarantees nor substitutes synthetic tests for real host/platform evidence.

# Approved remaining adoption APIs

Date: 2026-10-15. Owner approved implementation of the roster split and safe
`.missing`, and explicitly retained duplicate `.member` non-disclosure.
This is the approved library contract; implementation and verification are
separate recorded outcomes.

## Outcome and boundaries

Give host adopters a validated-input merge seam and a safe missing-property
diagnostic without changing existing admission or roster resolution decisions.
These are additive compatibility APIs for issues #3 and #4. Existing behavior
is not a demonstrated correctness defect. Keep unpublished `0.1.0.dev4`, Python
>=3.12 and current dependency floors. No wire schema, schema identity, generated
payload, prompt, provider, host integration, release or global installation change.
The separate issue #6 documentation unit must complete its formal gate first.

## Roster merge and validation

Export from the package root and `triad_dispatch_lib.roster`:

```python
merge_roster(defaults: dict, overrides: str | bytes | None = None) -> dict
validate_resolved(roster: dict) -> None
```

Preserve `resolve_roster(defaults: dict, overrides: str | bytes | None = None) -> dict`.
The split composition merges, validates the merged document, then returns it.
The validator returns `None`, not the resolved dictionary. Internally the existing
resolver loads one verified schema snapshot and shares it across all three stages.

`merge_roster` validates defaults against the resolved schema, then checks exact
duplicate names, before parsing overrides. `None` means absent; every other value
passes through the existing strict original-JSON parser. Map its `AdmissionError`
to existing fixed `RosterError("invalid_json")`. JSON null remains a schema error.
Validate overrides against the override schema, then exact duplicate names, then
merge. The returned independent document is not finally resolved or runnable.

`validate_resolved` independently loads the verified offline contract, checks the
resolved schema, then exact duplicate names; it neither mutates nor returns a copy.
Keep error codes/text, schema-before-duplicate precedence, nesting behavior and
unresolved-reference `ContractError` with no network retrieval. Host capability,
route, preset, selection, collision and custom diagnostic checks remain host-owned.

Names are case-sensitive. Existing names retain their slots; new names append in
override order. Dictionaries recursively merge, other values replace by independent
copies, including schema-allowed null. Missing members inherit; top-level fields
other than `legs` replace. Inputs and nested objects remain independent of output,
including no override. Do not delete inherited vendor blocks or add case folding.
The intermediate result may contain incomplete entries or incompatible inherited
blocks; host inspection must handle those safely and validate the exact document
before consumption. Later mutation requires revalidation. `select_entries` keeps
resolved revalidation, selection copies and empty-selection refusal unchanged.

## Safe missing-name diagnostic

Every `AdmissionError(code: str)` initializes `.missing: str | None = None`.
Keep its signature, `.code`, fixed message/args, `.field`, `.path` and displayed
chaining behavior unchanged. `validate_verdict` populates `.missing` only for its
already selected canonical `ValidationError` whose validator is `required`.

Use that error's `validator_value` only when it is a list of strings, and its
`instance` only when it is a dictionary. Select the first name in that trusted
schema list absent from that object; otherwise leave `None`. The instance is used
only for membership. The string comes from the schema, never provider keys or
values. An empty required name would be a string, distinct from `None`.

Keep the current validator call and selected violation. Do not revalidate, rank
or sort errors, inspect descendant context, parse messages, scan the whole input,
or navigate the source schema through `.path`. With a selected non-required error,
`.missing` is `None` even if another field is absent. Multiple missing names at the
selected rule follow its schema order. Selection among independent violations
remains unspecified by the public contract; this change does not alter it.

`.path` remains the selected schema diagnostic tuple and is not extended with
`.missing`: root required is `("required",)`; finding required is
`("properties", "findings", "items", "required")`, without an instance index.
The path is not a source-document JSON Pointer. Keep parse → schema → expected →
binding precedence and six-field binding order.

The value-free public diagnostic surface is `.code`, message/args, `.field`,
`.path` and `.missing`. Exception context and traceback frames remain outside
that guarantee. Do not expose the raw validation error or its data as new fields.
Do not add `.member`, opt-in flags, length caps or a duplicate pre-pass. A host
needing original duplicate-key diagnostics may retain its own strict parser as a
documented deviation; full parse delegation is not claimed.

## Evidence and completion

Pin combined/split roster parity, copies, defaults-before-override and
schema-before-duplicate refusals, intermediate inherited blocks, incomplete new
entries, empty/disabled/case-sensitive rosters, offline schema refusal and one
snapshot within the existing resolver. Exercise the new APIs through the existing
installed-wheel four-route driver, including a failing-validator control.

Pin every root/finding missing field, later finding selection, multiple missing
schema order, competing non-required failures, existing parse/binding precedence,
constructor defaults, and provider-data non-disclosure. Extend the raw replay
corpus and installed-wheel verifier with root/finding diagnostics and an injected
wrong-diagnostic control. Preserve all original raw fixtures.

Verify the combined source, neutral unpacked sdist and rebuilt wheel. Native CI
must measure Ubuntu/macOS and Python3.12/3.14 before corresponding claims. Formal
review uses three required Opus5.5/xhigh, Sol6.1/xhigh, Argon/high entries and a
separate nonvoting Astra/high comparison, each2400 seconds, current official web
research authorized. No prior vote transfers. Merge, publication and host adoption
remain separate owner decisions.

## Request disposition

Issue #4's library seam is addressed only after implementation and verification;
Claude's own `_check_required`/`_check_blocks` ordering and adoption test stay in
its independently owned project. Issue #3 gains safe missing-name diagnostics;
the arbitrary duplicate-name request is explicitly declined for the shared API.
Issue #5 remains proposals only: typed shared semantics need explicit contracts
and measured inputs; process/provider/custody state remains host-owned.

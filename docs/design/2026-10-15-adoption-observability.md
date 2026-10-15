# Adoption evidence and additive diagnostics

The owner approved the PR #2 review dispositions on 2026-10-15. This slice
corrects adoption evidence and implements L2 and L7. L10-L12 are documentation
clarifications. Other requests retain explicit design gates below; they are not
an instruction to implement every proposal in this slice.

## Compatibility and ownership

Use the existing selected checkout and PR branch. Preserve native spawning,
provider controls, original-output admission, canonical payload bytes, schema
identities and all existing error codes. Python remains >=3.12; dependencies
remain jsonschema>=4.26,<5 and referencing>=0.37,<1. Record this additive API
revision as unpublished 0.1.0.dev4; do not update either consumer or merge a PR.

## L2: value-free admission diagnostics

Keep `AdmissionError(code)` construction, message text and `.code` compatible.
Every AdmissionError has `.field: str | None` and
`.path: tuple[str | int, ...] | None`, defaulting to None. Library-generated
`binding_mismatch` sets field to the first mismatch in the existing six-field
binding order and leaves path None. `schema_violation` sets path to the validator's
absolute **schema diagnostic** path, not the untrusted instance path; field stays
None. This evaluation path contains trusted schema keywords and possible
composition indexes, never provider values or arbitrary instance property names.
Reference (`$ref`) and conditional (`if`) traversal hops may be omitted, so it is
not necessarily a JSON Pointer into the source schema document.
Empty tuple means the schema root. It is diagnostic
context, not a stable choice of which error wins when multiple violations exist.
Other codes retain both values as None. The value-free guarantee covers `.field`,
`.path`, and the fixed message/`.args`; no raw ValidationError is interpolated
into the message. Python exception internals, including `__context__` and
tracebacks, retain their existing behavior and may reference validator errors
or input data. Suppressed displayed chaining does not remove these references.
Preserve parse -> schema -> expected -> binding order.

## L7: optional rendered-clause manifest

Add keyword-only `with_manifest: bool = False` to `render_review_clauses`.
False returns exactly the existing string. True returns `(text, manifest)` where
manifest is a fresh list of `{ "name": str, "sha256": str }` objects. The flag
must be an actual bool. No new package-root export is required.

Record selected clauses in rendered order with the same names as the canonical
order list (including `common:`). Hash each selected fenced clause's UTF-8 bytes
after the parser's existing trailing-LF removal, before caller/date/phase/route
substitution, without the joining blank lines. Resolve the phase-purpose name
before recording. Omit inactive hook and other-host clauses. Record the selected
`common:review-web-permission` or `common:review-no-web` immediately after the
first selected clause containing `<review-web-policy>`, once only, hashing its
own unexpanded bytes. This nested row records an inserted dependency, not another
top-level emitted block. Literal caller replacements never create manifest rows.

Both modes use the same verified bundle load and rendering path. Manifest
mutation must not affect future calls; caller replacement changes alter rendered
text but not clause hashes. These hashes are evidence of selected source clauses,
not a final prompt hash, bundle identity, execution attestation or custody proof.

## Evidence corrections and remaining contracts

Distinguish reported scratch results from published reproducible measurements,
and planned Claude adoption from installed/released adoption. A rebuilt host
prompt bundle proves renderer comparison only, not packaged-asset parity.
Record Codex's existing AGY recovery and canonical/schema projection distinctions.
Use current dependency floors and per-platform wheel evidence; do not backport
to Ubuntu's stock validator merely to remove `Registry`.

L1 needs typed integrity/refusal/host-fault inputs separate from agreement;
L3 needs transport-only schema validation and host-normalized argv comparison;
L4 needs CLI/carrier-qualified evidence and separate token lookup. The latest
host amendment retains L5 as host-only with one consumer; shared extraction would
need a second consumer and a defined placeholder grammar. L6 needs
canonical binding separate from measured vendor projections. L8 needs shared
structured predicates without claiming final admission; L9 needs a versioned
member/serialization contract before cross-host digest identity is possible.
Keep raw-admission clauses fixed to the current host profile (L11), and describe
coordinators as optional adapters independent of the other APIs (L12).

## Verification boundary

Regression tests cover schema-location privacy, all six bindings, precedence,
all supported renderer profiles, nested web selection, hook filtering, raw
replacement stability, invalid flags, bundle damage and fresh result ownership.
Run source and unpacked-sdist suites on Python 3.12 and 3.14, all installed-wheel
drivers, authoring/assets checks, native CI, and the project's three-family review
with separate Astra comparison. Provider behavior and consumer adoption remain
separate evidence.

## Concurrent host amendments

Remote commits `477eee8` and `53790e5` arrived during implementation. They narrowed
Claude's first slice to four named functions and added issues #3-#5. Later
amendments `e8ea66d`/`b18da1b` reduced that slice to `render_review_clauses` and
`validate_binding`; the [request record](../requests/2026-10-15-claude-host-adoption-requests.md)
preserves this supersession. Amendment `e763df8` further narrows issue #3: the
requester accepts implemented `.field` and trusted schema `.path`, withdraws
decoder-detail and instance-pointer expectations, and leaves only `.member`
requested. Exposing a provider-chosen duplicate name needs a separate diagnostic
and privacy decision. Issue #4's L13 merged-but-unvalidated roster API is also new
design work. Neither remaining request is claimed complete or unblocking full
Claude admission/roster delegation. Claude withdrew L7/L11 as its
own requests; the owner's separate approval of this manifest API and fixed-profile
documentation remains the scope here. No additional runtime was introduced while
resolving the concurrent documentation edits.

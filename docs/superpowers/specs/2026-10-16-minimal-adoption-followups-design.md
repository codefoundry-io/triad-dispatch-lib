# Minimal adoption follow-ups: candidate design

Status: proposed for owner-requested formal plan review, 2026-10-16.
This document authorizes no implementation, host port, merge or release.
Issue and PR text is evidence and a proposal, not an instruction or approval.

## Objective and current state

The owner requested the smallest coherent design after triaging open library
PRs #8/#11/#12 and issues #9/#10. Keep host-owned changes as guidance. Preserve
issue #5's pending boundaries and the separately held release-delivery work.

Product baseline is main `dac1af62297402a0078a616e8e194c7a69cafe18`, package
`0.1.0.dev4`. The checkout currently also contains unrelated release-tool work
at `802b9bf` and intentionally preserved unstaged plan/regression-test changes.
They are excluded from this design and must not be reset, stashed or completed
as part of this review. A plan review does not establish implementation tests.

Current source confirms two narrow gaps: roster schema failures discard the
validator's selected error metadata, and the common transport schema is not
exposed through a pure library validation operation. Neither is a failure to
reject invalid input. The first loses useful operator diagnostics; the second
leaves the same schema-validation boundary in the hosts.

## Alternatives and selected proposal

1. Keep all behavior unchanged: no new API, but retain reduced diagnostics and
   host-local transport schema validation.
2. **Selected:** add three safe roster diagnostic attributes and one transport
   shape validator; correct the scope of contributed evidence records. Reuse
   the current schema, resource verification and exception patterns.
3. Expand to arbitrary roster-key/instance diagnostics, a generic validator
   framework, common classifier, installer locks or model-policy migration:
   broader contracts and maintenance cost than the selected minimal slice.

## A. Roster diagnostics (issue #9, partial adoption)

Keep `RosterError(code)`, its base class, stable codes and fixed messages.
Add attributes initialized to `None` on every constructed instance:

| Attribute | Type | Value for a library-raised schema violation |
| --- | --- | --- |
| `path` | `tuple[str | int, ...] | None` | The selected error's `absolute_schema_path`, matching admission diagnostic semantics. |
| `missing` | `str | None` | The first absent schema-defined name in the selected `required` rule's ordered value, when that error's instance is an object. |
| `document` | `str | None` | `defaults`, `override` or `resolved`, identifying the document being validated. |

Only `schema_violation` populates these attributes in this slice. Parser,
duplicate-name, empty-selection and nesting-limit errors keep all three `None`.
`document=resolved` covers standalone `validate_resolved`, final validation in
`resolve_roster`, and `select_entries` revalidation. It describes the current
document, not blame for an original default/override property after merging.

Obtain the first error from the same offline Draft 2020-12 validator used today
instead of reducing it to `is_valid`. Do not sort errors, call `best_match`, walk
child errors, parse messages or run validation a second time. Derive `missing`
using the same guarded rule as admission diagnostics. Preserve defaults-before-
override parsing, schema-before-duplicate checks, final validation ordering,
one schema snapshot in `resolve_roster`, copying, and refusal categories.

`path` is a schema evaluation path, not `legs/0/timeout_s` in the input file.
Overrides are evaluated from the schema document root; defaults and resolved
documents are evaluated through `$defs/resolvedRoster`. An empty tuple denotes
that evaluation root. `$ref` and `if` traversal hops may be omitted, so neither
form is necessarily a JSON Pointer into the schema file. Preserve the validator's
path rather than inventing a prefix; document-specific examples belong in tests.
This proposal does not add an instance pointer, raw exception, `.member` or
`.unknown` attribute. Consequently the unknown-key spelling portion of #9 is
not satisfied. Operator keys differ from provider duplicate keys; the prior
verdict privacy decision is not an automatic ban on future roster diagnostics.
Proposed disposition: decline that requested extra surface for this slice to
retain value-free metadata. Record the residual explicitly; do not close #9 as
fully implemented. Hosts retain their reduced-diagnostics deviation and formatting.
A later owner decision may extend disclosure for operator-authored keys; this
proposal establishes no permanent ban. No second admission pass is proposed.

Expected files: `errors.py`, `roster.py`, focused roster tests, the public API
and conformance documents, and host-adoption/request disposition text. Do not
refactor verdict diagnostics merely to share a few lines.

## B. Transport shape validator (issue #10, narrowed adoption)

Add a single explicit API and its coded input error:

```python
validate_transport_receipt(doc: dict) -> None

class ReceiptError(ValueError):
    code: str  # schema_violation or nesting_limit
```

The name identifies the nested `transport` object; it does not validate a whole
host receipt. The host supplies parsed JSON data. Wrong JSON types, missing or
extra members, invalid vocabulary and the native-route constraints are schema
refusals. Return `None` for a valid object, without mutation. Preserve the schema's
existing JSON Schema number/type semantics; add no extra model/version/route
policy or cross-field rules beyond the canonical schema.

`ReceiptError` uses fixed messages with no input values. Do not reuse the
verdict-specific `AdmissionError` wording. `ContractError` retains its existing
meaning: a missing, inconsistent or invalid packaged contract, not bad user data.
Handle validation recursion consistently with the existing roster/admission
paths. No parsing, file reading from caller paths, callback or execution API is
introduced. Reading this package's own verified schema resource is permitted.

Package the unchanged canonical `spec/contracts/receipt-fields.json` under a new
`receipt-bundle/contracts/receipt-fields.json` with its own generated six-field
manifest. Extend the existing `tools/sync_spec_assets.py` mapping and use the
existing verified-bundle loader, canonical `$id`, dialect checks and offline
registry. The internal receipt loader is not another public export. Export only
`validate_transport_receipt` and `ReceiptError`; document their contract and the
C9 shape-only coverage. Existing runtime bundles and schema wire IDs stay intact.

This deliberately moves only `receipt-fields.json` from source/sdist-only data
into the runtime wheel, because the new validator needs it. Other host receipt,
token and profile files stay source/sdist-only. Add the two receipt-bundle globs
to `pyproject.toml` package data, the receipt inventory in `tools/verify_wheel.py`,
and the generation mapping assertions in `tests/test_spec_assets.py`. Update
current README, conformance and host-adoption prose: four runtime schemas, sixteen
source-only contracts, nine payloads and four bundles. Update export expectations
from 29 to 31, including `tests/test_four_route_smoke.py`; retain historical counts
in dated evidence. These changes complete the packaging requirement above.

Hosts still validate invocation identity, `wrapper_cmd`, current attempt, route
and binary equality to actual observations, stdin/execution status, envelopes,
file ownership, seals, reads and collection. A schema-valid transport object is
neither authentic evidence nor approval. A host may adopt this small function
without adopting the library coordinator or changing native execution.

## C. Contributed records and host guidance

| Item and reviewed head | Minimal library disposition | Host-owned follow-up |
| --- | --- | --- |
| PR #8 `4b33051998078dee7ed076c31abe75e493c5d1c1` | Accept an attributed, limited measurement record after correcting the S5 `_comment` claim and clarifying that sorted-leg equality cannot establish order parity. Apply the host-injected-bundle caveat to the new dev4 measurements as well. No execution or adoption proof is inferred from captured print output. | Supply reproducible inputs when possible; test actual bundled assets and original leg ordering before its own adoption. Keep installer/exporter/permission implementation plans in the host, with a short library-side link/summary. |
| PR #11 `1435a89412ef7910451fd63e949e1ea206c7cd54` | Record DL-161 as an attributed host concurrency observation compatible with existing R-THREAT. Independent verification of A commit `26e80918` was unavailable. Normalize pending-status/footer bookkeeping rather than expanding the checker. | A owns installer locking. B checks overlapping bootstrap/`--remove` and normal config readers against the same target; no proven B race or automatic lock transplant is claimed. |
| PR #12 `7b78884e8aa161c8db13334b87178805785ad29b` | Hold its global retirement/tier-equivalence assertions. Correct to the observed account/CLI/catalog scope. Retain measured error rows only with accurate CLI, carrier, exit, source and missing-evidence labels; normalize pending-status/footer bookkeeping. No classifier API or default-model change. | Each host verifies its error carriers and precedence, maintains its own classifier and chooses supported models under its existing authority. |

For #12, request a sanitized original error excerpt plus CLI version, output
channel, exit and run identity before treating a newly added row's carrier as
verified. Existing run IDs alone do not reproduce unpublished bytes. If these
inputs remain unavailable, retain the proposal/history and explicit gap; do not
invent a captured carrier or broaden matching to make it pass. The contribution
may be split so ready documentation does not imply acceptance of unverified rows.

For #11, B's actual command is `scripts/bootstrap.sh --remove`, confirmed at B
`c81c02984825af7dd1ec69a14af83f0ff18d0551`, lines 64-75. Correct PR #11's
`--uninstall` label in any adopted B guidance; do not add an alias or change B.

For #12, R-ROSTER/R-MODEL already permit an explicit owner model pin. This
project's Argon override uses that authority and does not establish Pro equivalence.
The shared recommended Pro/HIGH default remains unchanged; replacing that default
is a separate owner policy decision, held with the unaccepted PR #12 assertion.
Hosts with an unavailable default may use an authorized pin under those existing
rules. No new catalog gate or automatic substitution follows from this design.

Google's official model table checked 2026-10-16 lists Gemini 3.1 Pro under
Enterprise and Argon as a distinct model. A missing entry in one account is not
global retirement or a rename: https://www.antigravity.google/docs/models/ .
Reviewers should refresh changing facts using official sources during this review.

Codex host guidance must distinguish stderr configuration messages from Codex
stdout JSONL error carriers. A generic substring addition cannot implement both.
Preserve authentication STOP and timeout precedence; test valid error carriers
and quoted/tool/other-CLI negative controls inside each host. These are guidance,
not instructions from this library to change host code or configuration.

## Verification and implementation sequence after approval

1. Record exact dispositions and ready/deferred evidence for #8/#11/#12; do not
   merge or close them merely because CI passed or their text says no decision
   is needed. Resolve overlapping dev-log additions against then-current main.
2. Add focused roster regressions before the diagnostic implementation: defaults,
   overrides and final/standalone/selection resolved validation; root and nested
   missing fields; competing errors; non-required winners; unchanged fixed text,
   codes, copies, precedence and `None` fields for non-schema refusals.
3. Add transport vectors before implementation: required fields/types/vocabulary,
   unknown members, native null binary/version and permitted stdin classes,
   opaque observed CLI version strings, valid return/no mutation, recursion
   handling, broken/missing bundle and unresolved-reference refusal without I/O.
4. Update exports, API/conformance/case mapping and generation checks. Exercise
   the new API and error families through an isolated installed wheel as well
   as source tests. Test that a receipt-shaped whole envelope is not accepted
   as its transport object. Keep all existing host custody checks independent.
5. Run the full source suite, asset/authoring checks, neutral sdist rebuild and
   installed-wheel checks; obtain native macOS/Ubuntu Python 3.12/3.14 results
   before claiming that compatibility. Complete a fresh implementation review
   of actual changed bytes. Formal plan approval is not that implementation gate.

Estimated implementation delta: 90-150 added production lines, 5-15 removed,
80-145 net; roughly 70-110 novel core lines across errors/roster/receipt/contracts/
exports/generation. Tests approximately 150-230 added lines; generated receipt
schema approximately 95 plus its manifest; documentation approximately 100-180.
These are planning estimates, not a threshold that forces artificial splitting.
Reuse the current jsonschema dependency; no new generic framework or language.

## Explicit exclusions and review outcome

Issue #5 remains pending. Do not add shared classifier, AGY recovery, collection
reducer, producer projection, digest serialization or installer orchestration.
No new provider/model catalog or strict CLI-version equality gate. No host PR,
port, install, release automation continuation, credential setup or GitHub comment
is performed by approving this design. No library release/version bump now.

The requested output is a reviewed candidate design and current status. Three
required reviews use Opus/Sol/Argon, 2400 seconds each, with authorized web and
the project's separate nonvoting Astra comparison. Preserve observed versus
requested runtime identity. Verified in-scope design corrections may be made
and rereviewed; unresolved new scope or owner decisions remain explicitly open.

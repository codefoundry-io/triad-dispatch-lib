# Strict JSON and v2 admission design

Date: 2026-10-12. The owner requested a plan followed by implementation in
this repository. This is the first executable slice of the research direction.

## Contract and scope

Implement `triad-dispatch-lib` (import `triad_dispatch_lib`) in Python 3.12+.
Use `jsonschema>=4.26,<5` and `referencing>=0.37,<1`, with a committed `uv.lock`
for development. Build a standard wheel and sdist with setuptools. Initial
development version: `0.1.0.dev0`; no package-index release in this slice.

The authority is shared-spec commit
[`fcd96a15d18f3131c1f0111bdb10c3faceae34f8`](https://github.com/codefoundry-io/triad-dispatch-spec/tree/fcd96a15d18f3131c1f0111bdb10c3faceae34f8),
specifically `contracts/leg-verdict.schema.json` and the
[validation decision](https://github.com/codefoundry-io/triad-dispatch-spec/blob/fcd96a15d18f3131c1f0111bdb10c3faceae34f8/decisions/rev-2-implementation-spec.md).
This is a candidate contract pinned by commit, not a newly published spec tag.
Package the schema byte-for-byte, plus a manifest containing repository, commit,
candidate status and SHA-256. Verify provenance and digest when loading it.
Hashes detect inconsistent packaging, not malicious replacement of the package.

## Public interface

```python
parse_json(raw: str | bytes) -> object
validate_verdict(raw: str | bytes, *, expected: dict) -> dict
```

`parse_json` accepts original JSON only. Bytes must decode as UTF-8. Reject
duplicate object members at every depth, including escaped equivalent names;
NaN/Infinity constants; floating-point overflow to infinity; malformed JSON;
invalid UTF-8; and decoder recursion/integer limits. Preserve standard Python
JSON values and do not strip Markdown fences, select a substring, coerce values,
or accept already parsed dictionaries. JSON scalars are legal parsing results;
verdict admission separately requires the canonical object schema. Float
overflow is rejected explicitly even where an existing host parser lets it pass.
No configurable resource limit is introduced; callers own input size limits.

`validate_verdict` parses once, applies `Draft202012Validator` with an explicit
empty offline registry, validates the expected binding, then compares all six
fields: `review_id`, `family`, `content_digest`, `leg_name`, `attempt`, `route`.
The expected dictionary must contain exactly these six schema-valid fields;
Google requires `agy` or `gemini`, other families require null. Keep canonical
JSON Schema integer semantics (e.g. `1.0` is an integer, `true` is not).
Return the parsed verdict unchanged. A valid negative verdict is still admitted;
admission does not mean agreement or permission to merge.

`AdmissionError(ValueError)` exposes a stable `code`: `invalid_json`,
`invalid_utf8`, `duplicate_member`, `nonfinite_number`, `invalid_input_type`,
`nesting_limit`, `schema_violation`, `invalid_expected`, `binding_mismatch`.
`ContractError(RuntimeError)` indicates broken packaged contracts or unresolved
schema references. Errors expose fixed messages without payload values or JSON
paths, since attacker-controlled keys may themselves contain sensitive data.
No public mutable schema object or hidden input mutation is allowed.

## Verification and integration

1. Unit tests exercise raw parsing, canonical verdict constraints and every
   binding field. Raw replay fixtures preserve malformed bytes and original
   duplicate members. They are explicitly synthetic, not provider observations.
2. Tests fault the packaged manifest/schema boundary and disallow network
   retrieval. Copy neither the hosts' `conftest.py` nor their installation setup.
3. Build an sdist and a wheel rebuilt from that sdist. Install the wheel with
   dependencies in a fresh environment, outside the source tree. Replay the same
   fixtures, verify the loaded package path and embedded source digest. Record
   the wheel hash and runtime/platform identity.
4. CI runs the tests and installed-wheel replay on native Ubuntu 24.04 x86-64
   and macOS ARM64 runners, Python 3.12. These runs establish only those tested
   combinations. Rust is not required by this repository's source; transitive
   dependencies can contain native Rust code. A binary-only install checks wheel
   availability for each selected platform.

The review profile for this slice is a fresh independent Codex whole-branch
review plus automated checks. It is not formal multi-family TRIAD admission.
Final merge and release remain separate owner decisions.

## Next slices and the Codex prompt question

The next design should cover failure classification and aggregation against
shared contract cases, then a scoped adapter in each consumer. Keep native
spawning, model/effort, provider execution, custody and installation in the hosts.

For Codex integration, use a small external test driver with an explicit wheel
path and version. Record `triad_dispatch_lib.__file__`, distribution version and
artifact hash, and prove the host admission entrypoint actually calls it.
Use pinned canonical prompt clauses and render cases to test prompt construction;
do not fork the complete Codex skill or copy its runtime as the library oracle.
The existing read-only reviewer prompt forbids tests/scripts and cannot serve as
the test runner. A separate fresh Codex session can later produce a real raw
verdict for the driver; record its prompt/spec/runtime provenance and distinguish
it from deterministic replay. Start with an isolated integration fixture, then
change the real consumer only in its own scoped work. This slice makes no real
provider calls and does not establish either host's adoption.

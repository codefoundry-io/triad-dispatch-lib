# Pinned clauses and Codex response smoke

The owner approved continuation after the first admission slice. This slice
implements the proposed prompt/driver/fresh-session path before consumer adoption.
Continue in the current repository and draft PR; do not merge, release, or edit
either existing host. Classification and aggregation remain separate later work.

## Shared implementation

Pin `prompts/common-clauses.md`, `prompts/leg-codex.md` and
`contracts/review-kind.schema.json` byte-for-byte from shared-spec
`fcd96a15d18f3131c1f0111bdb10c3faceae34f8` (remote main rechecked unchanged).
The canonical clause format is specified in that revision's `prompts/README.md`.
Use a separate manifest with the same repository/commit/status/digest convention
as the existing schema bundle. Share the manifest integrity helper with admission.

Add `render_review_clauses(*, family, host, review_date,
review_web_authorized, replacements, review_kind="pre-merge") -> str`.
Initially accept only `family="codex"`, `host="B"`; unsupported combinations
fail explicitly. This is shared deterministic rendering, not spawning or a full
copy of the Codex host renderer. Future profiles can reuse the clause engine.

Render fenced text only, in canonical order. Select plan-purpose for formal-plan,
code-purpose for pre-merge/implementation-review. Validate phase using its pinned
schema, strict boolean web permission, and an explicit ISO calendar date. Omission
defaults to pre-merge; explicit null is invalid. Never read a clock. Exclude
host-inapplicable clauses by header marker, not a hard-coded clause blacklist.

Require exactly these caller replacements: worktree, brief-file, packet-files,
review-id, content-digest, leg-name, attempt. Values are strings encoded by the
caller and must have no literal CR/LF. The caller cannot override library-owned
phase/date/web selection. Substitute once, so values containing placeholder text
are not interpreted again. Invalid arguments raise `PromptError(ValueError)` with
fixed messages; broken assets raise `ContractError`.

Expose `validate_binding(expected: dict) -> None` using the existing canonical
binding validation, without adding another model or schema. Existing verdict
validation retains its current ordering and behavior. Add `render_data(value: str)
-> str` to transport residual data with JSON quoting and an adaptive backtick
fence, preceded by the canonical data-fence caveat.

## Test adapter and custody

`tools/codex_smoke.py` is a repository test adapter, not a runtime host adapter.
It takes an explicit wheel and expected distribution version, installs in a fresh
temporary venv, and runs an isolated (`-I`) child outside the checkout. Reuse the
environment helper in `tools/verify_wheel.py`. Verify both module and actual
`validate_verdict` implementation paths are in that venv's site-packages.

The driver's context JSON supplies expected bindings, review_kind/date, absolute
worktree/brief/packet paths, objective, criteria, approved_boundary and residual.
Reject invalid binding/scope, non-regular or symlink packet files and paths outside
the worktree. Record SHA-256 of every packet, input context, rendered prompt and
wheel, plus package version, schema/prompt provenance and runtime platform.
The test packet digest is SHA-256 of the sorted JSON list of relative paths and
their file hashes. Require expected.content_digest to match it. This is a fixture
digest convention, not the existing hosts' formal round-basis algorithm.

Render mode writes one new prompt file; admit mode requires that exact prompt
file to equal the current rendering, reads raw response bytes, and calls installed
`validate_verdict`. No fence stripping, repair, retry or reserialization of the
response before admission. Admission failure is distinct from a valid negative
verdict. Exit 2 indicates rejection/input error; no successful report is emitted.

The driver assembles metadata, scope, residual and canonical output schema around
the library clauses. It does not launch Codex or select models. The parent uses
native collaboration to start two fresh read-only Codex children: a correct
control and an explicitly defective synthetic example with instruction-like
source data. Record expected behavior before dispatch, without giving children
the expected verdict. Native reviewer prompts prohibit tests/scripts/spawning.

Persist each final response as text without JSON reserialization and label it
`parent-transcribed-final-text`. Record observed child identifier, requested
model/effort, terminal event and prompt hash; hidden runtime settings are
`UNEXPOSED`. This establishes a fresh native response reaching the installed
validator, not machine-attested original provider bytes, complete formal custody,
or actual consumer adoption. Synthetic CI replay and live evidence stay distinct.

## Packaging and verification

Use version `0.1.0.dev1`, keeping Python/dependency/platform choices. Include test
fixtures and tools in the sdist now that the driver depends on them; verify the
unpacked source can run its tests. This resolves the previous deferred packaging
minor as part of the required distribution work.

TDD covers clause ordering, phase/web choice, manifest damage, hostile strings,
binding validation, driver call-through, packet/prompt changes and raw rejection.
Native Ubuntu/macOS CI repeats installed-wheel synthetic prompt/admission smoke.
Fresh native smoke is a separate bounded manual operation, not automatic CI.
Finish with ordinary independent whole-branch Codex review and an updated draft PR.

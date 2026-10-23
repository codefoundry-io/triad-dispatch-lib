# Public API compatibility

This project adopts a compatibility floor at `0.1.0.dev4`, commit
`087af94a7078de0ae9701fb057840b5492f51f66`, for the 31 package-root exports in
the [library API contract](../spec/reference/library-api.md). This is an explicit
project policy during pre-1.0 development, not an automatic SemVer guarantee.
After 1.0, deliberate incompatible public changes are expected to use a major
version. At any version, a version bump alone does not waive this gate.

## Run the gate

This Python API gate does not certify a common installed launcher or CLI.
[R-SHARED-RUNTIME-COMPAT](../spec/reference/review-rules.md#R-SHARED-RUNTIME-COMPAT)
separately governs backward compatibility and reuse across consuming hosts.

```sh
uv sync --locked
uv run --locked python tools/check_api_compatibility.py
uv run --locked pytest -q
```

The structural command requires a Git source checkout with the full declared
baseline and floor commit objects available. CI fetches full history in a
dedicated PR/main compatibility workflow; the four native OS/Python jobs remain
independent in the unchanged reusable package workflow. Historical release-tag
retries do not require tooling introduced after their source commit. Publication
consumes the reviewed release source; the static gate runs on PR and main heads.
The command compares the immutable baseline source to the actual candidate
`src/` bytes, including local edits. Missing source, objects, explicit exports or
unresolvable aliases fail the check. It never falls back to an installed package
or an empty baseline. Relative cwd lookup is disabled and the loaded package
initializer origin must match the requested source. The metadata in
[api-compatibility.json](../api-compatibility.json)
records the original floor, current structural baseline and advancement history.
It does not automatically follow tags, main or the latest release.
Full commit IDs are the authoritative comparison identities. `version` values
are descriptive release or transition labels reviewed with the metadata; the
checker does not authenticate releases or derive the baseline from mutable
tags. Maintainers verify labels and the approved source when advancing it.

The locked development dependency Griffe statically resolves root aliases and
generates dataclass constructor signatures. The wrapper projects each exported
function or class constructor into a synthetic module before invoking
`find_breaking_changes`; it does not recurse through implementation modules or
class helpers. A stable public synthetic callable name prevents a private
implementation alias from suppressing checks. Constructor projections omit the
bound implicit receiver, while
preserving a static constructor's first public argument and ordinary function
parameters. It rejects removed exports, changed object/sync-async kind,
existing argument removal/positional reorder, incompatible kind changes, optional
argument
default changes, optional-to-required changes, newly
required arguments and loss of supported resolved ancestry (including documented
exception bases). Griffe's MRO supplies resolved ancestors; their canonical base
references resolve through Griffe's final targets across re-export hops. These
identities preserve exported root bases and external leaves while allowing
non-exported intermediate classes to be inserted or renamed. All public aliases
of a base retain their identities regardless of export order. This does not
establish arbitrary inheritance equivalence. Existing argument names remain
protected even when variadic
arguments could swallow them. Added exports, optional keyword arguments,
private helpers and internal implementation moves remain allowed.
Variadic additions and local `*args`/`**kwargs` variable renames are allowed;
removing a variadic kind or a real named argument remains a break. Projected
variadic names use spaced kind identities that cannot collide with legal
ordinary parameter names.
Static checks do not detect positional capture rebinding, such as adding an
optional positional parameter before existing `*args`. Dev4 declares no variadic
parameters; introducing variadic APIs requires targeted consumer tests for
captured-argument behavior.
Safe argument widening (required to optional, positional-only or keyword-only
to positional-or-keyword) also remains allowed through Griffe's compatibility rules.

The implementation uses the supported [Griffe loading API](https://mkdocstrings.github.io/griffe/guide/users/loading/),
[API checks](https://mkdocstrings.github.io/griffe/reference/api/checks/) and
[built-in dataclass extension](https://mkdocstrings.github.io/griffe/extensions/built-in/dataclasses/).
Griffe 2.3.2's comparison iterates module members; the projection deliberately
retains only callable shape and excludes annotations. Static analysis cannot
prove return values, type compatibility, validation behavior, generated/dynamic
APIs or arbitrary semantic equivalence. No custom type/schema engine is used.
Declared defaults are compared as static expressions, so equivalent expression
rewrites may require preserving their existing spelling or a reviewed decision.

## Consumer evidence and releases

`tests/test_public_api_consumers.py` uses only package-root imports and standard
library test tools. It protects export availability, six frozen dataclass
constructors, exception bases/constructor code preservation and selected emitted
codes/diagnostics, strict JSON and all
six bindings, roster order/copy/opaque model values, receipt shape/opaque CLI
versions, prompt default/manifest shape and carrier/negative/timeout/agreement
safety, plus the additive dev5 AGY metadata-separation contract. It does not
freeze exact prompt text. The full existing conformance and
async/lifecycle suites remain the deeper regression evidence.

These tests run in source and unpacked sdist test suites without `.git`.
`tools/verify_wheel.py` runs the same consumer file through the fresh installed
wheel's isolated interpreter from a neutral directory, asserting its import
origin is the environment's `site-packages` and its distribution version matches
the candidate project. This adds installed consumer evidence to the existing
raw-corpus/bundle checks; it is not exhaustive behavioral equivalence.

For routine compatible releases, maintainers may advance `baseline` to a full
reviewed release commit after retaining existing checks and adding checks for
newly public behavior. Record the previous baseline and advancement decision
in `history`; preserve the original floor identity and historical export list.

An incompatible transition requires an explicit reviewed owner decision,
updated contract/tests and migration notes naming affected calls and remedies.
For that approved transition only, maintainers may manually set `baseline` to
an existing reviewed API-source commit before release, and update the active
`floor_exports` and affected checks for the specifically approved differences.
Preserve the previous baseline and protected export list in `history`; retain
all unaffected protections. Commit the API source before the metadata that
references its full SHA. The final candidate must match that reviewed source
plus separately checked compatible edits. This requires no failing-gate merge
or automatic waiver. A version bump alone authorizes none of these changes.

Keep an approved pre-release API-source SHA reachable in fresh full-history
checkouts after integration, via a merge that retains it or a retained tag.
Squash/rebase without a retained reference may lose that source object.

No fixed pre-1.0 deprecation window is promised. After 1.0, the major-version
expectation above applies. There is no automatic refresh, rewrite or waiver flag.

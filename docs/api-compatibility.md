# Public API compatibility

This project adopts a compatibility floor at `0.1.0.dev4`, commit
`087af94a7078de0ae9701fb057840b5492f51f66`, for the 31 package-root exports in
the [library API contract](../spec/reference/library-api.md). This is an explicit
project policy during pre-1.0 development, not an automatic SemVer guarantee.
After 1.0, deliberate incompatible public changes are expected to use a major
version. At any version, a version bump alone does not waive this gate.

## Run the gate

```sh
uv sync --locked
uv run --locked python tools/check_api_compatibility.py
uv run --locked pytest -q
```

The structural command requires a Git source checkout with the full declared
baseline and floor commit objects available. CI fetches full history in a
dedicated compatibility job; the four native OS/Python jobs remain independent.
The command compares the immutable baseline source to the actual candidate
`src/` bytes, including local edits. Missing source, objects, explicit exports or
unresolvable aliases fail the check. It never falls back to an installed package
or an empty baseline. The metadata in [api-compatibility.json](../api-compatibility.json)
records the original floor, current structural baseline and advancement history.
It does not automatically follow tags, main or the latest release.

The locked development dependency Griffe statically resolves root aliases and
generates dataclass constructor signatures. The wrapper projects each exported
function or class constructor into a synthetic module before invoking
`find_breaking_changes`; it does not recurse through implementation modules or
class helpers. It rejects removed exports, changed object/sync-async kind,
existing argument removal/positional reorder, incompatible kind changes, optional argument
default changes, optional-to-required changes, newly
required arguments and removed declared class bases (including documented
exception bases). Existing argument names remain protected even when variadic
arguments could swallow them. Added exports, optional keyword arguments,
private helpers and internal implementation moves remain allowed.
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
constructors, exception bases/codes/selected diagnostics, strict JSON and all
six bindings, roster order/copy/opaque model values, receipt shape/opaque CLI
versions, prompt default/manifest shape and carrier/negative/timeout/agreement
safety. It does not freeze exact prompt text. The full existing conformance and
async/lifecycle suites remain the deeper regression evidence.

These tests run in source and unpacked sdist test suites without `.git`.
`tools/verify_wheel.py` runs the same consumer file through the fresh installed
wheel's isolated interpreter from a neutral directory, asserting its import
origin is the environment's `site-packages` and its distribution version matches
the candidate project. This adds installed consumer evidence to the existing
raw-corpus/bundle checks; it is not exhaustive behavioral equivalence.

On release, maintainers may advance `baseline` to a full reviewed release commit
only after preserving the existing consumer/regression checks and adding checks
for newly public behavior. Append the previous baseline and advancement decision
to `history`; retain `floor` and its export list. Keep the old tests when advancing,
so a later baseline does not silently erase the original behavioral floor.
A deliberate incompatibility requires an explicit reviewed owner decision,
updated contract/tests and migration notes explaining affected calls and remedies.
There is no automatic refresh, rewrite or waiver flag.

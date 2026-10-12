# Shared dispatch library assessment

Date: 2026-10-12. This handoff records the completed read-only research and the
authorized repository initialization. It does not accept a detailed library API.

## Owner authorization and current scope

- Repository name: `triad-dispatch-lib`.
- GitHub destination: `codefoundry-io/triad-dispatch-lib`.
- Visibility: public, explicitly authorized by the owner.
- Future shared-library development belongs in this independent repository.
- Current work is initialization and documentation following read-only research.
- No runtime code, packaging, dependency installation, tests, host integration,
  or release is part of this initialization.

Public repository authorization and the development destination do not settle
the package name, API, backend, dependency policy, or versioning policy.

## Evidence snapshots

The assessment uses fixed source snapshots, rather than an assumption that
different working directories or distributions have the same current contents.

| Evidence | Snapshot | Meaning |
| --- | --- | --- |
| A | [`e4cadf2`](https://github.com/codefoundry-io/triad-dispatch/tree/e4cadf2f751308d1ab75e4199b08d89849bb93b3) | Exported distribution examined in the comparison |
| B | [`b42bf2f`](https://github.com/codefoundry-io/triad-codex-dispatch/tree/b42bf2fbb8f6a0e69b4765002a535ff0c702e40f) | Source snapshot examined in the comparison |
| B remote main | [`6cc7271`](https://github.com/codefoundry-io/triad-codex-dispatch/tree/6cc7271f29e51353932b66fcd3c9cea29b16783d) | Tree identical to the inspected B source snapshot |
| Shared specification | [`fcd96a1`](https://github.com/codefoundry-io/triad-dispatch-spec/tree/fcd96a15d18f3131c1f0111bdb10c3faceae34f8) | Contract basis for the assessment |

The Claude implementation source is separate from its public export, as described
in the [shared-spec README](https://github.com/codefoundry-io/triad-dispatch-spec/blob/fcd96a15d18f3131c1f0111bdb10c3faceae34f8/README.md#L41).
Commit identity, tree equality, distribution contents, and runtime behavior are
different evidence claims.

## Confirmed overlap and candidate responsibilities

The three v2 schemas are byte-identical in the inspected comparison. A 47-line
strictification/Markdown helper is also identical in the distribution comparison.
These are bounded duplication findings; they establish no whole-repository clone
percentage and do not prove that every similarly named helper is equivalent.
See the [A v2 implementation](https://github.com/codefoundry-io/triad-dispatch/blob/e4cadf2f751308d1ab75e4199b08d89849bb93b3/skills/triad-cross-family-review/lib/verdict_v2.py),
[B validator](https://github.com/codefoundry-io/triad-codex-dispatch/blob/b42bf2fbb8f6a0e69b4765002a535ff0c702e40f/bin/validate_v2.py), and [B contracts](https://github.com/codefoundry-io/triad-codex-dispatch/tree/b42bf2fbb8f6a0e69b4765002a535ff0c702e40f/contracts).

The following are candidates for a shared deterministic implementation:

1. Strict raw JSON parsing, preserving duplicate-key and nonfinite-number rejection.
2. Canonical v2 validation, including all six existing bindings.
3. Failure classification, preserving typed-carrier priority.
4. Agreement evaluation: every enabled reviewer must be `SAFE TO MERGE`, with no blockers
   or questions.
5. Same-basis retry decisions under the current shared contract.
6. Shared prompt clauses whose text and semantics are contract-owned.

These candidates need a design decision and contract vectors before extraction.
Similarity alone does not authorize moving code or changing observable behavior.

## Contract and ownership boundary

Recommendation: keep common data and schemas in one pinned shared-spec source;
implement deterministic common behavior once in this library. Consumers should
identify the exact contract revision they use and reject incompatible inputs.

Host adapters retain native agent spawning, model and effort selection, install
mechanisms, capability discovery, and custody-related I/O. A host must not import
another host's native internals merely to obtain common decision logic.

Keep v1 and v2 boundaries explicit. Do not silently convert between them or infer
that a v1 payload has acquired v2 admission guarantees through conversion.

## Latest terminal behavior takes precedence

The latest [`R-TERMINAL` rule](https://github.com/codefoundry-io/triad-dispatch-spec/blob/fcd96a15d18f3131c1f0111bdb10c3faceae34f8/reference/review-rules.md#R-TERMINAL) supersedes the older automatic capacity/schema
full-CLI retry and descendant-group cleanup behavior. The inspected A exported distribution
still contains that older behavior in its [public export helper](https://github.com/codefoundry-io/triad-dispatch/blob/e4cadf2f751308d1ab75e4199b08d89849bb93b3/bin/_common.py).

This is a source-versus-current-contract observation. It is not a new undecided
retry design, and this research did not establish a complete runtime finding.
Any extraction must preserve the latest contract rather than promote the older
source behavior into the shared library. Same-basis retry remains bounded by
the current contract and must not become automatic terminal full-CLI replay.

## Recommended implementation direction

Recommendation: start with a Python 3.12+ deterministic core. Do not begin with
a Rust rewrite. The existing contract and Python boundaries provide a smaller
path to behavioral parity and language-neutral verification vectors.

The shared specification explicitly makes `python-jsonschema` Draft 2020-12
validation authoritative, with an offline registry and Pydantic 2 at existing
boundaries. This is an existing specification decision, not a new suggestion
to replace validation with Pydantic or to introduce vendor SDK dependencies.

Candidate dependencies are the standard library, `jsonschema`, and `referencing`,
with Pydantic retained where the existing boundary requires it. Recommend `uv`
for reproducible development and release dependency pinning; tooling adoption
and final runtime requirements remain design decisions.

Python-first does not mean a fully pure-Python dependency graph: `jsonschema`
transitively uses `rpds-py`, which includes Rust native code. Wheel availability
and source-build requirements must therefore be measured for chosen platforms.

Rust is an optional later choice if measured bottlenecks or an explicit
Python-free deployment requirement justify it. A native extension would add
build, ABI, packaging, and platform obligations; PyO3 is an option to assess,
not an adopted backend.

## Portability and verification limits

macOS and Ubuntu 24.04 are supported environments in the contract, but this
assessment did not test either platform. Contract support is not a certification
of this new library, any architecture, or native dependency wheel availability.

Measure supported architecture and wheel combinations in CI before making
implementation support claims. No runtime tests, host integration checks,
packaging checks, or release validation were performed for this initialization.

## Proposed first design slice

Recommendation: design raw JSON handling plus v2 admission first, with shared
language-neutral vectors for valid input, duplicate keys, nonfinite values,
schema rejection, and all six bindings. Require exact rejection and admission
semantics across consumers before expanding into orchestration decisions.

Final APIs, package layout and identity, backend choice, dependency constraints,
version policy, migration path, and host adoption order remain unresolved.
The next step is an explicit design slice, not runtime implementation or release.

## Reference basis

- [Existing authoritative validation decision](https://github.com/codefoundry-io/triad-dispatch-spec/blob/fcd96a15d18f3131c1f0111bdb10c3faceae34f8/decisions/rev-2-implementation-spec.md#L26).
- [JSON Schema validation documentation](https://python-jsonschema.readthedocs.io/en/stable/validate/).
- [Referencing and registries](https://referencing.readthedocs.io/en/stable/).
- [uv project synchronization](https://docs.astral.sh/uv/concepts/projects/sync/).
- [Rust platform support](https://doc.rust-lang.org/rustc/platform-support.html).
- [PyO3 documentation](https://pyo3.rs/main/).

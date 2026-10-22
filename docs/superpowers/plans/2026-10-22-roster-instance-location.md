# Roster Instance Location Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let a caller locate the failing roster entry without changing validation or existing diagnostics.

**Architecture:** Copy the first selected validator error's instance path into one additional `RosterError` attribute. The verified canonical schema's fixed properties and closed objects bound the disclosed strings; hosts own formatting.

**Tech Stack:** Python 3.12+, locked jsonschema/referencing, pytest, uv/setuptools.

**Spec:** [Roster instance location design](../specs/2026-10-22-roster-instance-location-design.md).

## Global Constraints

- Add only `RosterError.instance_path: tuple[str | int, ...] | None`; `None` by default, `()` for a schema error at the evaluated root.
- Preserve `RosterError(code)`, all existing attributes/codes/fixed messages/args, first-error ordering, schema bytes and copy behavior.
- Populate from that same selected error only. No child search, second validation, new parser, pointer renderer or raw key/value API.
- `.document` identifies defaults/override/resolved; resolved indices identify the merged roster, not override provenance.
- Keep schema IDs, acceptance semantics, native/host adapters and issue #5 unchanged.
- Preserve the selected checkout and all existing work. Use `/bin/zsh -lic` with `sandbox_permissions="require_escalated"` for Python, tests, builds, Git/GitHub mutations and provider CLIs, from the workspace host cwd then enter the project.
- Design review precedes implementation. Exact-head CI and the project Opus/Sol/Argon review plus separate Astra comparison precede implementation admission. Merge/publication require a concrete owner decision.

## Review Focus

- Index zero mistaken for no location: explicitly compare tuple paths at index 0 and 3.
- Final order mistaken for override order: a changed existing third entry stays at 2; an appended incomplete entry goes to 3.
- Missing Google adapter mistaken for a leaf property: both first-error cases point at the leg object, preserving existing `.missing`.
- Unknown properties disclosed in diagnostics: root/entry/adapter errors expose only the parent location and fixed text.
- Installed package lacks the additive property: a package-root consumer regression runs in source, archive and isolated wheel.

Estimated delta: production +2 to +5 / -0 / net +2 to +5 in two files; novel core at most 5 lines; tests roughly +60 to +100; docs roughly +50 to +90 excluding this plan/design. Version preparation is metadata, not a new feature. Record any actual growth and its reason.

### Task 1: Add and document the instance-location property

**Files:** modify `src/triad_dispatch_lib/errors.py`, `src/triad_dispatch_lib/roster.py`, `tests/test_roster_diagnostics.py`, `tests/test_public_api_consumers.py`, `spec/reference/library-api.md`, `README.md`, and current `docs/status.md`; add a dated verification record. Prepare `pyproject.toml` and `uv.lock` for `0.1.0.dev5` only after checking that version remains unused. Historical records retain their dates and meaning.

**Interfaces:** consumes the existing first `ValidationError.absolute_path`, verified roster schema and `RosterError(code)`; produces the tuple-valued property alongside the unchanged schema-path diagnostics. No new root export.

- [ ] Extend direct-construction and non-schema tests to assert `error.instance_path is None`, including invalid JSON, duplicate names, empty selection and nesting.
- [ ] Add parameterized invalid-timeout tests for defaults, overrides, standalone validation and selection, at index 0 and 3. Assert `('legs', index, 'timeout_s')`, unchanged code/text/args/schema path/missing/document, and unchanged input.
- [ ] Add root missing/type/extra-property cases asserting `instance_path == ()`; add entry/adapter extra-property cases asserting their parent path. Keep sentinel unknown names and values absent from the public diagnostics.
- [ ] Extend both Google route-block vectors at index 0 and 3: `instance_path == ('legs', index)` with existing `anyOf`/`missing=None` and `required`/`missing='agy'` results preserved.
- [ ] Add final-resolution tests: overriding an existing entry preserves its default slot and appending an incomplete entry after three defaults reports `('legs', 3)`. Assert resolved attribution, tuple type and that later caller mutation does not alter the captured path.
- [ ] Add a public-package consumer assertion that invalid entry index 1 exposes `('legs', 1, 'timeout_s')` while the existing schema diagnostics remain available. This file is already exercised by archive and wheel verification.
- [ ] Run `uv run --locked pytest -q tests/test_roster_diagnostics.py tests/test_public_api_consumers.py`; retain expected RED from the absent property, without changing assertions to match implementation.
- [ ] Add the typed `None` initialization in `RosterError.__init__` and assign `tuple(validation_error.absolute_path)` next to the existing `.path` assignment in `_validate`. No other runtime behavior changes.
- [ ] Rerun the focused tests; require GREEN. Recheck the canonical schema's fixed-property/closed-object invariant against unknown-key regressions. Unsupported future dynamic schemas are outside this API and require a future design review, not a speculative current fallback engine.
- [ ] Document all four attributes together, distinguishing trusted schema metadata from canonical instance field names/indices. Explain root versus unavailable, document-relative indices, selected aggregate/required behavior, fixed disclosure and exception-internal limits. Mark the property as the unreleased candidate; preserve dev4's published capabilities and remaining unknown-key request.
- [ ] Run full source tests, `tools/sync_spec_assets.py --check`, `spec/tools/check_authoring.py`, `tools/check_api_compatibility.py` and `git diff --check` after `uv sync --locked`. Require all pass, no test exclusions and no asset drift.
- [ ] Build and normalize the exact sdist with the existing release helper, extract to a new neutral temporary directory, run locked archive tests/assets/authoring checks and rebuild the wheel. Run `verify_wheel.py`, `codex_smoke.py ... self-test`, `four_route_smoke.py` (its default synthetic matrix), and `native_codex_smoke.py ... --self-test` against that rebuilt wheel, with exact version/path arguments. Retain logs and digests; no real provider or installation claim follows from synthetic drivers.
- [ ] Commit only this unit, push a scoped draft PR and attach it. Require successful Ubuntu 24.04/macOS 15 × Python 3.12/3.14 package jobs and separate API CI at the exact head.
- [ ] Complete the project formal implementation review of the frozen candidate and separate Astra comparison, reproduce findings, and rerun changed evidence as required. Preserve requested versus observed model settings and exact lifecycle export/cleanup evidence.
- [ ] Post the reviewed result and PR link to issue #9. Prepare an exact publication packet with source/version/diff/CI/review/artifact and release-note evidence for the owner's merge/publication decision. Keep current host pins and published dev4 assets intact until a subsequent authorized release and host-owned adoption.

Self-review: one functional unit covers the complete design; all five review-focus conditions have explicit tests. Current canonical validation always provides a location for schema errors; `None` remains the direct/non-schema fallback. No broader diagnostics, migration, automation or host implementation is implied.

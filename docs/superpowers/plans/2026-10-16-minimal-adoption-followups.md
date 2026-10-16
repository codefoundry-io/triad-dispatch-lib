# Minimal Adoption Follow-ups Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the two approved deterministic APIs, pin the two Minor review cases,
and document precise contribution dispositions without changing either host.

**Architecture:** Reuse the existing offline validator, coded errors and verified
resource bundles. Keep transport shape separate from receipt authenticity and
retain existing roster validation order and copy behavior.

**Tech Stack:** Python 3.12+, existing locked jsonschema/referencing, pytest, setuptools.

**Spec:** [Reviewed design](../specs/2026-10-16-minimal-adoption-followups-design.md)
and [R2 checklist](../../verification/2026-10-16-minimal-adoption-design-review.md#accepted-r2-implementation-checklist).
The owner approved implementation and GitHub updates on 2026-10-16.

## Global Constraints

- Keep `RosterError(code)`, its fixed messages/codes and existing validation/copy order.
- Add `.path`, `.missing`, `.document`, initially `None`; populate schema failures only.
- Keep first-error selection and one offline validation pass; no child-error search.
- Add only `validate_transport_receipt(doc: dict) -> None` and `ReceiptError` exports.
- Keep the canonical transport schema unchanged; model/version strings remain opaque.
- Keep native execution, custody, installation, classifier and model defaults host-owned.
- Keep version `0.1.0.dev4`; issue #5 and release-delivery work remain held.
- Preserve the existing checkout and dirty release plan/tests; no reset, stash or separating checkout.
- Run Python/tests/builds/Git-GitHub mutations/provider CLIs through literal
  `/bin/zsh -lic` with `sandbox_permissions="require_escalated"` from the workspace
  host cwd, then enter this repository. Read-only file/Git inspection may use default.
- Complete native macOS/Ubuntu Python 3.12/3.14 CI and full public v2 review:
  Opus 5.5/xhigh, Sol 6.1/xhigh, Argon/high; separate Astra/high; 2400 seconds each,
  web authorized. Merge and publication remain separate owner decisions.

## Review Focus

- Wrong document attribution after merging: defaults/override/resolved tests in Task 1.
- Missing route blocks select `anyOf`: both neither-block and alternate-block controls in Task 1.
- Installed resource missing despite source success: installed API/error probe and wheel inventory in Task 1.
- Bad caller input confused with broken packaged contract: distinct exception tests in Task 1.
- PR #12 prose claims held measurements: bounded record consistency regression and guide in Task 2.

Estimated delta: production 90-150 added / 5-15 removed / 80-145 net, 70-110 novel
core lines; tests 150-230 lines; generated schema about 95 plus manifest; docs
100-180 lines. Record justified growth rather than adding generic infrastructure.

### Task 1: Implement diagnostics, transport validation and package delivery

**Files:** `src/triad_dispatch_lib/{errors,roster,contracts,__init__}.py`, new
`src/triad_dispatch_lib/receipt.py`, generated `data/receipt-bundle/`,
`tools/sync_spec_assets.py`, `tools/verify_wheel.py`, `pyproject.toml`,
`tests/test_roster_diagnostics.py`, `tests/test_receipt.py`, affected
`tests/test_spec_assets.py`, `tests/test_four_route_smoke.py` and wheel-driver tests.
Do not edit the held `tests/test_release_artifacts.py`.

**Interfaces:** Consumes existing `load_verified_bundle`, canonical schema and
guarded admission diagnostics. Produces the reviewed roster attributes,
`ReceiptError(code)` (`schema_violation`/`nesting_limit`) and
`validate_transport_receipt(doc: dict) -> None`; private receipt loader only.

- [ ] Write focused regressions before implementation: direct error defaults,
  defaults/override/final/standalone/selection attribution, schema paths, selected
  required names, competing/non-required winners, fixed messages, existing copy
  and precedence rules, and non-schema `None` attributes.
- [ ] Include the two R2 vectors: Google `route=agy` with neither vendor block
  selects `anyOf`, path `properties/legs/items/allOf/1/allOf/2/then/anyOf`,
  `.missing=None`; adding `gemini={}` selects route-required `.missing="agy"`.
- [ ] Add transport tests for valid/no-mutation, required/type/vocabulary/extra
  members, native null binary/version/stdin constraints, integral-float semantics,
  opaque version text, whole-envelope refusal, recursion, missing/corrupt bundle,
  wrong identity/dialect and unresolved references without network access.
- [ ] Run focused tests and retain expected RED evidence (missing attributes/API).
  Use `uv run --locked pytest -q tests/test_roster_diagnostics.py tests/test_receipt.py`.
- [ ] Implement the smallest changes, preserving schema bytes and selection order.
  Fixed ReceiptError text: `Transport receipt violates the canonical schema.` and
  `Transport receipt nesting exceeds the validation limit.` No input interpolation.
- [ ] Extend generation mapping, package-data globs, bundle inventory and exports.
  Generate assets with `uv run --locked python tools/sync_spec_assets.py --write`.
  Extend the installed wheel probe to actually call the new API and exercise
  the new error families/roster diagnostics; test a wrong-behavior control.
- [ ] Run focused tests and existing roster/contract/assets/wheel-driver tests.
  Expected: all pass; generator `--check` passes; exports are 31, four bundles,
  nine payloads, four runtime schemas and sixteen source-only contracts.
- [ ] Run the checkout suite with only the six already-held collision cases
  excluded: `uv run --locked pytest -q -k 'not test_cli_refuses_output_collision_and_preserves_artifacts'`.
  This is explicitly not a claim that the held release regression passes.
- [ ] Self-review, commit only owned files and write RED/GREEN evidence/report.
  Obtain independent task review for spec compliance and code quality.

### Task 2: Record adoption boundaries, contribution dispositions and Minor 2

**Files:** `README.md`, `docs/host-adoption.md`,
`docs/requests/2026-10-15-claude-host-adoption-requests.md`,
new `docs/requests/2026-10-16-adoption-followups-disposition.md`,
`spec/reference/{library-api,library-conformance,library-case-coverage}.md`,
`spec/tests/test_spec_records.py`; parent owns `docs/status.md` and verification records.

**Interfaces:** Consumes Task 1 API/error/installed-probe outcomes and the reviewed
PR #8/#11/#12 dispositions. Produces user-facing contracts and host guidance,
with no host edits, unverified contract rows, wholesale PR cherry-pick or issue closure.

- [ ] Document new API contracts, evaluation roots, selected-required-only missing
  metadata, Python exception-internal limits, and both R2 route-block examples.
  Keep issue #9 partial; explain the declined arbitrary-key surface without
  claiming permanent prohibition or exact host diagnostic-message parity.
- [ ] Update current package/export/count prose and C9 shape-only coverage.
  Preserve dated historical counts and host adoption status.
- [ ] Record #8's corrected comment/order and host-injected-asset limits; #11's
  attributed concurrency observation and actual B `--remove` option; #12's held
  retirement/equivalence assertions and missing original carrier evidence.
  Keep contributed branches open for their owners to amend rather than treating
  their text as implementation instructions. Link host-owned checks as guidance.
- [ ] Add a bounded regression for the concrete PR #12 contradiction: record
  prose must not claim measured AGY/Codex model-refusal rows absent from the
  measured contract, and cannot claim none when the corresponding rows exist.
  Exercise both mismatch directions with test-only fixtures and the live records.
  Do not add a runtime classifier or pin current model IDs/CLI versions as gates.
- [ ] Keep current R-GOOGLE measurement wording unchanged while all proposed
  rows remain held; document conditional coordinated updates upon later acceptance.
- [ ] Run `uv run --locked pytest -q spec/tests/test_spec_records.py` and
  `uv run --locked python spec/tools/check_authoring.py`; expected: pass.
- [ ] Commit owned documentation/tests; obtain independent task review.

## Integration, review and GitHub delivery (parent)

- [ ] Verify source plus asset/authoring checks, neutral sdist rebuild, isolated
  wheel and four existing drivers on local Python 3.12/3.14. Preserve logs.
- [ ] Build an exact publication branch from `origin/main` plus only this slice's
  selected file blobs using an alternate index; keep the active checkout and held
  release edits in place. Exclude the earlier release-helper commits/files.
- [ ] Push that scoped branch and create a draft PR with change/install/adoption
  boundaries and test evidence. Attach it to this chat. Run all four native CI jobs.
- [ ] Freeze the verified candidate; complete the required fresh formal review and
  separate Astra comparison. Fix reproduced findings and reverify changed bytes.
- [ ] Update issues #9/#10 and PRs #8/#11/#12 with reviewed dispositions, new PR
  link and remaining host guidance. No auto-closing #9 or merging existing PRs.
- [ ] Record exact reviewed commit, CI, exports/cleanup, held state and limits;
  stop before main merge or library/host release.

# Specification and Library Consolidation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Develop shared specification and deterministic library in one repository while retaining independently distributed native hosts.

**Architecture:** Import the complete upstream spec into `spec/`; generate existing packaged resources from its canonical files. Replace external commit pinning with strict content-derived bundle manifests and preserve original import ancestry separately.

**Tech Stack:** Python 3.12, jsonschema, referencing, pytest, uv, setuptools, GitHub Actions.

**Spec:** `docs/design/2026-10-13-spec-library-consolidation.md`

## Global Constraints

- `spec/contracts/` and `spec/prompts/` are the only editable sources of the runtime schema and prompt bytes.
- No Markdown/JSON normalization or line-ending conversion is allowed.
- Existing canonical schema `$id` values stay unchanged, including their old repository namespace.
- Do not require Git or network access to generate, test or build.
- Keep Python 3.12, current dependencies, four configurable routes and native host callback contracts.
- Bump the unpublished package to `0.1.0.dev3` for the changed resource provenance format.
- Existing host projects and the old specification repository are not rewritten as a side effect.
- This migration changes no canonical prompt behavior, Gemini workaround, MCP integration, SDK TODO, provider permissions or real-host deployment.
- Preserve the selected checkout and existing work. Run Python, tests, builds and Git/GitHub mutations through `/bin/zsh -lic` with `sandbox_permissions="require_escalated"` from the first invocation.

## Review Focus

- A well-formed but false bundle ID must be rejected (Task 1 malformed-manifest tests).
- Unexpected or symlinked generated assets must not silently enter a distribution (Task 1 generator tests).
- A source archive without Git history or the original checkout must regenerate the same bytes (Task 2 archive verification).
- Old schema namespace URLs must continue resolving offline after repository provenance changes (Task 1 schema identity tests; Task 2 installed probe).
- The source suite passing must not conceal absent canonical TOML/case/authoring files in the sdist (Task 2 full source-archive suite and checker).

---

### Task 1: Consolidate source and enforce deterministic bundle identities

**Files:**
- Create: `spec/` from `_runs/spec-consolidation/upstream/`, plus `spec/import-origin.json`.
- Create: `src/triad_dispatch_lib/bundle_manifest.py`, `tools/sync_spec_assets.py`, `tests/test_spec_assets.py`.
- Modify: `src/triad_dispatch_lib/contracts.py`, all three generated `source-manifest.json` files, `tests/test_contracts.py`, affected prompt tests if required.
- Preserve byte-for-byte: all packaged schema and prompt payloads.

**Interfaces:**
- Consumes upstream commit `396a04dac310d5ff91dbe0a36982f7679aa00428`, downloaded in `_runs/spec-consolidation/upstream/`.
- Produces `bundle_manifest.contract_id(digests: dict[str, str]) -> str`, using the exact serialization defined in the design; source constants and strict shared manifest helpers can live in that small module.
- Produces `tools/sync_spec_assets.py --check` and `--write`, usable with `uv run --locked python`; exit zero means byte equality or successful generation, nonzero means invalid input or drift.
- Keeps `load_verified_bundle(root, names: tuple[str, ...]) -> dict[str, bytes]` and public APIs unchanged.
- Produces import ancestry record with `source_repository`, `source_commit`, and `sha256` (all original imported relative files); it is not current bundle provenance.

- [x] Write tests for identity serialization, valid generated bundles, strict manifest fields, Boolean/unknown versions, malformed digests, mismatched ID and altered payloads. Assert `ContractError` for invalid bundles.
- [x] Write generator tests using temporary trees: canonical byte preservation, deterministic repeated generation, nonwriting check, missing/changed/extra outputs and symlink refusal. Assert failure leaves existing outside-target bytes untouched.
- [x] Run focused tests before implementation and record expected RED output; distinguish a missing implementation from an unrelated environment failure.
- [x] Import the complete upstream tree and generate the original file digest record. Verify the original package payloads equal corresponding upstream bytes; if any differ, report before replacing them. Historical files remain byte-identical at this task.
- [x] Implement the shared identity function, generator with explicit mapping and owned-tree validation, and strict runtime manifest validation. Use the exact six-field manifest from the design. Decouple `SCHEMA_NAMESPACE` from current source repository. Preserve error boundaries and fresh schema returns.
- [x] Update existing provenance tests for the new format and add assertions preserving verdict, roster and review-kind schema IDs. Include duplicate/non-finite JSON tests already present; do not weaken them.
- [x] Run focused tests, `uv run --locked pytest -q`, `uv run --locked pytest -q spec/tests`, `uv run --locked python spec/tools/check_authoring.py`, generator `--check`, and `git diff --check`. Record import/payload equality and results.
- [x] Self-review and commit only owned files. Report tests and any integration obligations for Task 2; wheel metadata reporting and normal nested test discovery belong to Task 2.

### Task 2: Ship verifiable source archives and document independent host adoption

**Files:**
- Modify: `pyproject.toml`, `uv.lock`, `MANIFEST.in`, `.github/workflows/test.yml`, `tools/verify_wheel.py`, root `AGENTS.md`, `README.md`, `docs/status.md`.
- Modify active migration guidance only: `spec/README.md`, `spec/reference/README.md`, `spec/reference/spec-authoring.md`, `spec/authoring/README.md`, `spec/AGENTS.md`, `spec/CLAUDE.md`, `spec/GEMINI.md` if needed for consistent links.
- Create: `spec/MIGRATION.md`, `docs/host-adoption.md`, `docs/verification/2026-10-13-spec-library-consolidation.md`.
- Test: extend appropriate packaging/driver tests under `tests/`; add `tests/test_packaged_spec.py` only if needed for focused behavior coverage.

**Interfaces:**
- Consumes Task 1 generator flags, import ancestry and six-field bundle manifests. Each `contract_id` identifies an individual runtime bundle.
- Produces normal root pytest discovery of `tests` and `spec/tests` with importlib mode retained.
- Produces `0.1.0.dev3` sdist and wheel; the existing `verify_wheel.py <wheel>` interface now reports all bundle identities and verifies all three installed bundles from its isolated interpreter.
- Keeps all existing isolated replay/Codex/four-route/native drivers and their public arguments.

- [x] Add a focused failing test for installed probe metadata/all-bundle verification or archive inputs, exercising behavior rather than grepping implementation. Record RED.
- [x] Update package version and lock, include canonical source/checkers/tests/TOML inputs in the sdist, and discover both test suites. Exclude `_runs`, temporary outputs, caches and VCS metadata from built artifacts.
- [x] Update installed wheel verification to exercise verdict, roster, review-kind and all five prompt resources, validate each manifest ID/digest, and report new metadata instead of the removed `source_commit`. Preserve isolated import-origin checks and strict failure behavior.
- [x] Update CI for generator check, imported authoring checker, combined source and unpacked-sdist tests, rebuild-from-sdist and all four isolated drivers at dev3. Use existing Ubuntu/macOS matrix and dependency pins.
- [x] Update active authoring instructions to `spec/` as canonical source within this repository, distinguish historical import ancestry from current content IDs, and preserve historical decisions/changelog/cases without rewriting their past assertions. Explain that repository cutover awaits PR merge and old repository notice; do not claim remote retirement.
- [x] Document independent host release/adoption metadata, shared-content versus host-native boundaries, generated-asset ownership, managed-file hash/preservation recommendations for each host installer, static versus real-host verification, and a copy-ready old-spec migration notice for use after merge. No consumer or old-spec mutations in this task.
- [x] Run `uv sync --locked`, both suites, authoring checker, generator check and `git diff --check`. Build sdist, unpack outside source, rebuild wheel from sdist, run combined tests/checker/generator there, and run all four existing installed-wheel drivers on the rebuilt wheel using current README commands. Record exact paths/results and actual platform.
- [x] Update current status and verification evidence without claiming remote CI or actual providers not observed in this slice. Self-review and commit owned files.

## Controller completion

- Review each task independently, then perform the final whole-branch review with a fresh Astra reviewer. Fix verified findings through the responsible implementer.
- Update the existing draft PR branch after successful local verification; inspect native CI before making Ubuntu/macOS claims. Do not merge, publish, tag, globally install, archive the old repository or port either host.
- Preserve review and verification outcomes in tracked evidence; retain any required operator decisions in the final response.

## Plan self-review

Both tasks map to the design: Task 1 owns source identity and runtime consistency;
Task 2 owns distribution, authoring and adoption boundaries. Task 2 consumes Task
1's exact manifest/CLI interfaces, without changing them. All five review-focus
conditions have explicit tests or archive probes. Historical source is imported
before narrowly updating active guidance; import hashes remain ancestry only.

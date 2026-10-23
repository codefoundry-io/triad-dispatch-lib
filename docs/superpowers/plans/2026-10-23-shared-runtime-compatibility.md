# Shared Runtime Compatibility Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish deterministic common-runtime compatibility, explicit consumer selection and conservative retention APIs, then adopt them in the Codex host under its own implementation plan.

**Architecture:** The library validates immutable consumer descriptions and a host-verified runtime support declaration. It chooses only an explicit binding or an established legacy binding, and computes retention without performing filesystem or provider operations. Codex owns trusted provenance, immutable storage, transactional launcher publication and execution of each consumer's original hardened launcher.

**Tech Stack:** Python 3.12+, existing setuptools/uv/pytest toolchain; no new dependency.

**Spec:** `spec/decisions/2026-10-23-shared-runtime-compatibility.md`, `spec/reference/review-rules.md#R-SHARED-RUNTIME-COMPAT`, C81-C83.

## Global Constraints

- Owner authorized implementation, merge and publication on 2026-10-23, then selected scope 1 and 2: library plus Codex; Claude/AGY receive adoption work.
- Preserve dev4 public API floor and every existing runtime schema/prompt. New APIs are additive in `0.1.0.dev6`.
- No filesystem, subprocess, authentication, model/default discovery, environment inference or native spawning in this module.
- The host authenticates artifacts and compatibility evidence before constructing a runtime descriptor. A digest or declaration alone is not authentication or a behavioral test.
- Old unqualified calls retain the established legacy binding. New consumers may select a complete content digest. No default inferred from installer, list order or host environment.
- Retain unknown dependencies; existing/active references prevent removal. Host transactions and actual lifecycle evidence remain independently required.
- Work in the selected checkout; preserve all unrelated state. Commands use `/bin/zsh -lic` with `sandbox_permissions="require_escalated"`, host cwd `/Users/chaniri/codex_workspace` then the repository.
- Complete the library's three-required-family public-v2 review plus separate Astra comparison before beginning the Codex implementation plan. Use 2400-second review budgets.

## Size and review boundary

Expected production addition: 220-320 lines, 0-10 deletions, net 210-320; novel core about 180-250 lines across the new module, errors and exports. Tests/consumer verification add about 250-400 lines; documentation is counted separately. One coherent library implementation unit covers all three deterministic decisions. Codex implementation is a subsequent host-owned plan, not silently included in this package's conformance claim.

## Review Focus

- A forged or malformed descriptor must refuse without echoing untrusted values; the host must still authenticate its provenance.
- An empty/unknown explicit selector must refuse rather than fall back to an established legacy default.
- Equivalent binding documents with different mapping/set order must have one identity; changed baseline/library/adapter/context must change identity.
- An in-use old runtime and an unknown dependency inventory must survive retention planning.
- Installed-wheel callers must exercise the new behavior without importing the source checkout.

## Task 1: Implement and distribute the common decision APIs

**Files:**
- Create `src/triad_dispatch_lib/runtime_compat.py` and `tests/test_runtime_compat.py`.
- Modify `src/triad_dispatch_lib/errors.py`, `src/triad_dispatch_lib/__init__.py`, `tests/test_receipt.py`, `tests/test_four_route_smoke.py` for additive exports.
- Extend `tests/test_public_api_consumers.py` for the same selection/refusal/retention behavior in source and installed-wheel verification.
- Update `pyproject.toml`, `uv.lock`, `spec/reference/library-api.md`, coverage/conformance/unit/case records, status, release notes and host adoption guidance.

**Interfaces:**

All digests are lowercase 64-character SHA-256 strings. Public dataclass construction does not validate; every operation validates its inputs. Collections returned in records are immutable sorted tuples. Dictionary inputs contain exactly the documented keys; unknown keys, booleans in place of strings, duplicate set entries and invalid types refuse.

`ConsumerBinding` fields: `schema`, `consumer`, `baseline_digest`, `library_digest`, `adapter`, `capabilities`, `commands`, `context_digest`, `binding_id`. Identifiers/capabilities match `[a-z][a-z0-9._:-]{0,127}`; command basenames match `[A-Za-z0-9][A-Za-z0-9_.-]{0,127}`. No slash, NUL or path traversal is accepted.
`validate_consumer_binding(document: dict) -> ConsumerBinding` consumes all fields except `binding_id`; schema is `triad-consumer-binding.v1`. The ID is SHA-256 over UTF-8 canonical JSON (sorted keys, compact separators, ASCII escaping) of validated input with sorted command/capability lists. `consumer` and `adapter` are bounded nonempty identifiers, not new canonical roster host literals. Commands are nonempty safe basenames; capabilities may be empty. No executable path or environment value is interpreted here.

`RuntimeDescriptor` fields: `schema`, `artifact_digest`, `commands`, `capabilities`, `supported_bindings`.
`validate_runtime_descriptor(document: dict) -> RuntimeDescriptor` consumes these fields; schema is `triad-runtime-compat.v1`. Supported bindings are a nonempty set of exact consumer binding IDs for which the host has verified compatibility with this exact runtime artifact. Commands are nonempty; capabilities may be empty.

`check_consumer_compatibility(runtime: RuntimeDescriptor, binding: ConsumerBinding) -> None` requires exact supported binding membership and availability of every required command/capability. It revalidates both records, including computed binding identity. It does not infer compatibility from equal version strings.

`select_consumer_binding(runtime: RuntimeDescriptor, bindings: sequence[ConsumerBinding], *, explicit_binding: str | None, legacy_binding: str | None) -> ConsumerBinding` validates the complete inventory, refuses duplicate IDs, selects the explicit ID when present, otherwise only the supplied established legacy ID, then applies compatibility checking. Neither selector means refusal even for a single inventory member. An empty explicit selector is invalid, never fallback. Inventory order has no effect.

`RuntimeRetention` fields: `retain`, `remove`, `diagnostic`.
`plan_runtime_retention(artifacts: sequence[str], *, consumer_references: sequence[str], active_references: sequence[str], dependencies_known: bool) -> RuntimeRetention` validates digest inventories. Duplicate artifact identities and references outside the complete artifact inventory refuse. Repeated references are harmless. With unknown dependencies, retain every artifact, remove none and report `dependencies_unknown`. Otherwise retain the union of consumer/active references and report `references_preserved`; only unreferenced artifacts are removable. This is a decision, not an instruction to bypass host provenance or transaction checks.

`RuntimeCompatibilityError(ValueError)` has stable `.code` and fixed value-free messages. Codes: `invalid_descriptor`, `invalid_binding`, `unsupported_schema`, `invalid_selector`, `missing_context`, `unknown_binding`, `ambiguous_binding`, `unsupported_binding`, `command_mismatch`, `capability_mismatch`, `invalid_inventory`, `incomplete_inventory`. No raw values in messages.

- [ ] Write focused positive and refusal tests first; observe failure because the public APIs are absent before implementation.
- [ ] Implement the pure interfaces and nine additive exports (41 root exports total); preserve existing exports and positional/default contracts.
- [ ] Run the focused suite, then extend the dependency-free public consumer driver with explicit selection, unchanged legacy selection, unknown-selector refusal and active/unknown retention assertions.
- [ ] Document exact shapes/trust boundaries and distinguish library API RUN from host C81-C83 NOT RUN. Update version and lock to dev6; preserve unrelated status proposals.
- [ ] Run `uv sync --locked`, `uv run --locked pytest -q`, `uv run --locked python spec/tools/check_authoring.py`, `uv run --locked python tools/sync_spec_assets.py --check`, `uv run --locked python tools/check_api_compatibility.py`, and `git diff --check`. Expected: all tests/checks pass, generated assets unchanged, dev4 API structurally compatible.
- [ ] Build an sdist, rebuild its wheel, run the existing wheel verifier outside the checkout. Expected: new consumer behavior passes from installed site-packages and all original bundle identities remain verified.
- [ ] Commit/push the complete candidate to PR #28. Complete native CI and formal project review on its final basis; correct reproduced findings and rerun the required round after source changes.
- [ ] Merge the approved exact head, publish `v0.1.0.dev6` through the existing release workflow, verify immutable wheel/sdist/manifest assets, then start the Codex host plan. Deliver pinned adoption work to the three host PRs after publication and Codex integration.

## Implementation rulings and host handoff

The explicit selector is the planned host ingress `TRIAD_RUNTIME_BINDING=<binding_id>`, consumed and removed by the neutral launcher before executing the saved host launcher. That environment name and filesystem layout are Codex mechanisms, not new library environment discovery. Shared storage will retain immutable generations and bindings; unknown active use is conservatively retained. Existing AGY launchers can be imported only after full template/group and immutable baseline provenance checks. Codex lifecycle may preserve the AGY tree, but independent older AGY installers/removal cannot be certified by this task. Claude's current direct plugin-wrapper invocation likewise remains unchanged until its maintainer adopts the common interface.

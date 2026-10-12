# Four-route core implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Configure named review entries for all four routes, share output admission/agreement, and coordinate bounded host callbacks plus separate perspective investigations.

**Architecture:** Pure roster, rendering and admission functions form the core. A separate async coordination module calls supplied host functions; provider spawning, capability discovery, cancellation of real processes and host custody remain outside this package. Existing strict admission remains the single verdict validation path.

**Tech Stack:** Python 3.12+, stdlib asyncio, existing jsonschema/referencing; no new runtime dependencies.

**Spec:** [Approved direction](../../design/2026-10-12-configurable-four-leg-library.md). Canonical snapshot in `_runs/four-route-implementation/spec/`, freshly fetched main `396a04dac310d5ff91dbe0a36982f7679aa00428`; unchanged assets retain package pin `fcd96a15d18f3131c1f0111bdb10c3faceae34f8`.

## Global Constraints

- All work/tests in this lib repo and current selected feature branch; existing hosts/spec read-only. No installs into hosts, global configuration, merge or release.
- No openai-codex SDK, MCP integration, CLI upgrades, Gemini plan replacement/retest, Claude quota retries, or unmeasured AGY typed-error mapping.
- Any nonempty selected roster; three canonical families with Gemini/AGY routes under Google. No majority rule or informational exemption. Model/effort opaque; host-native exceptions remain host-owned.
- Original JSON only; no fence repair, coercion, duplicate loss, or phrase-based provider error classification. Contract failures remain distinct from rejected provider/verdict data.
- Literal canonical prompt text stays byte-preserved in assets; renderer respects host/route conditions and literal shape metavariables.
- ALL Python/tests/builds/Git mutations/GitHub/provider CLI via `/bin/zsh -lic`, `sandbox_permissions=require_escalated`, tool cwd `/Users/chaniri/codex_workspace` then cd this repo. Record python3 path/version/tool preflight. Consume terminal exec status. No recursive delegation.
- Workers are not alone; preserve others' changes. Each task owns only listed files and its SDD report. Stage exact owned files. Use TDD and record real RED then GREEN evidence.

## Review Focus

- Callback mutation cannot change bindings after preparation: Task 3 snapshots and mutation test.
- Cancellation must finish child cleanup; timeout is cooperative, not a process-kill claim: Task 3 cancellation/finally tests.
- A successful-looking answer with failed transport must never approve: Task 2 terminal failure matrix.
- Inner structured JSON must keep duplicate/escaped-member evidence: Task 2 strict span tests.
- Additional same-family results cannot swap or escape agreement by informational label: Tasks 1/2/3 renamed sibling tests.

### Task 1: Roster and complete canonical rendering

**Files:** create `src/triad_dispatch_lib/roster.py`, `tests/test_roster.py`; modify `contracts.py`, `prompts.py`, `errors.py`, `__init__.py`, `tests/test_contracts.py`, `tests/test_prompts.py`; add canonical roster schema in its own `data/roster-bundle/` with manifest, Claude/Google/investigation files to existing prompt bundle+manifest; update package-data/MANIFEST.in only if required.

**Interfaces:**
- `resolve_roster(defaults: dict, overrides: str | bytes | None = None) -> dict`: defaults validated as resolved canonical roster; strict-parse override document then merge by name (existing order, append new names), recursive object merge and scalar/array replacement; explicit null preserved; duplicate names/unknown or wrong-family fields refused. Validate resolved disabled entries too. No provider/model defaults are invented. No mutation/aliasing of caller inputs.
- `select_entries(roster: dict) -> list[dict]`: validate resolved roster, return copied enabled entries in order, refuse empty selection.
- `load_roster_contract() -> dict`; fixed-message `RosterError.code` for caller errors; preserve `ContractError` for broken pinned data.
- Extend `render_review_clauses` backward-compatibly to families codex/claude/google and hosts A/B; optional `route: str | None = None`, `agy_hook_active: bool = False`. Google requires explicit agy/gemini route and `gated-patch-file` replacement; derive `google-route` from route argument. Existing seven replacement keys remain exact for other families. Active-hook true allowed only Google/A/AGY. Preserve Claude shape metavariables and `<END-VERDICT>`; unknown placeholders in canonical text still fail by recognizing allowed literal metadata, not deleting every guard.
- `render_investigation_prompt(prompt: str, *, family: str, route: str | None = None, web_authorized: bool = False) -> str`: validate family/route/boolean; custom prompt unchanged except Google+web appends canonical web-evidence LAST separated by blank line, using Gemini native names for gemini. No formal clauses/verdict requirement.

- [ ] Write RED tests: strict override JSON, partial/null merge, duplicate/default/override names, same-family and four-route selection, disabled invalid entries, empty selection, no mutation. Rendering all 3 families x 2 hosts x 3 phases, Google two routes and hook on/off, literal Claude marker/metavariables, one-pass substitutions, Google investigation suffix/tool names, no suffix in formal prompt.
- [ ] Run named tests showing missing behavior; retain terminal RED evidence.
- [ ] Implement minimal APIs/assets with verified provenance. Use offline reference registry for roster schema fragments. Preserve old Codex API output.
- [ ] Run full `uv run --locked pytest -q`, diff check; self-review and commit exact owned files. Report commits/commands/results/concerns to task report.

### Task 2: Provider output admission and unanimous agreement

**Files:** create `src/triad_dispatch_lib/output.py`, `agreement.py`, `tests/test_output.py`, `tests/test_agreement.py`; modify `json_input.py`, `errors.py`, `__init__.py` as needed; existing verdict API stays compatible.

**Interfaces:**
- Frozen `ProviderOutput(carrier: str, stdout: str | bytes, exit_code: int | None, completed: bool, timed_out: bool = False, transport_failed: bool = False)`. Carriers exactly `native-final`, `claude-json`, `gemini-json`, `agy-stream-json`. None exit allowed only native; completed must be explicit true. Booleans strict, bool is not a valid integer exit. No stderr phrase classification.
- `extract_final(output: ProviderOutput) -> str | bytes`: terminal guards first; native returns original raw value. Claude formal requires native object `structured_output`, object envelope, no explicit is_error/error subtype/error terminal status. Gemini requires string response and no error carrier. AGY strict JSONL requires exactly one object `event=result` with object result, status SUCCESS and native object structured_output; reject malformed/duplicate/missing/non-success terminal. Ignore only well-formed nonterminal records/blank lines. Require structured-output objects, no string coercion or fallback.
- Raw object extraction validates full envelope through existing strict parser, then locates original JSON member span without re-encoding; keys with JSON escapes work. Preserve original bytes/string representation where feasible. Inner decoded Gemini string is passed intact. Existing `AdmissionError` retains duplicate/nonfinite codes; `OutputError.code` covers transport/envelope problems.
- `admit_output(output: ProviderOutput, *, expected: dict) -> dict`: validate binding, ensure CLI carrier matches expected family/Google route; native allowed for host-supplied native final from any family (Claude A marker stripping remains explicit host duty), then existing validate_verdict.
- Frozen `AgreementResult(agreed: bool, verdicts: dict[str, dict], reasons: dict[str, str], integrity_ok: bool)`. `evaluate_agreement(expected_by_leg: dict[str, dict], outputs: dict[str, ProviderOutput], *, integrity_ok: bool) -> AgreementResult`. Reject invalid caller maps, empty selection, key/name mismatches, mixed review_id/content_digest, extra output names via `AgreementError.code`; missing/invalid/failed/negative outputs populate per-leg reasons and prevent agreement. All bindings rechecked, all selected count; host integrity false blocks even if all answers safe. Do not catch ContractError as a review failure. No trust in pre-parsed verdict dicts.

- [ ] RED tests: all four carriers with valid/negative verdict; native Claude host-stripped raw; duplicate outer/inner/escaped keys; nonfinite/UTF8/truncation; failure plus valid answer; quota-looking ordinary evidence accepted; AGY exit3 partial/multiple terminal/malformed tail; wrong carrier/route; repeated same-family bindings. Agreement all approved, missing, negative informational equivalent, invalid/stale/swap, extra names, mixed bases, integrity false, broken contract propagation.
- [ ] Observe RED, implement and run focused GREEN then full suite; no CLI inference/host imports. Commit and report exact evidence.

### Task 3: Bounded async review and investigation coordination

**Files:** create `src/triad_dispatch_lib/dispatch.py`, `tests/test_dispatch.py`; modify exports/errors if needed. This task consumes Tasks 1/2 public APIs.

**Interfaces:**
- Frozen `ReviewRequest(entry: dict, expected: dict, prompt: str)` and `InvestigationRequest(entry: dict, prompt: str, web_authorized: bool = False)`; entry is one enabled canonical resolved leg. Perspective is caller-authored prompt; no new roster fields or formal personas.
- Frozen `CallOutcome(name: str, status: str, value: object | None, error_code: str | None)`; statuses completed/failed/timed_out. Frozen `ReviewRun(outcomes: tuple[CallOutcome, ...], agreement: AgreementResult)`.
- `async run_review(requests, invoke, *, preflight, integrity_check, max_concurrency: int) -> ReviewRun`: invoke async accepts one ReviewRequest, returns ProviderOutput. preflight async accepts the prepared request and returns None or raises; every selected request preflight succeeds before any invoke. Host preflight validates actual options/model/effort/capabilities. integrity_check async takes no args and returns strict bool after calls settle. No default integrity=True.
- `async run_investigations(requests, invoke, *, preflight, max_concurrency: int) -> tuple[CallOutcome, ...]`: async callbacks receive InvestigationRequest with canonical investigation prompt suffix resolved. Return ordinary callback values without verdict admission, roster voting or an agreement flag. Model/effort from entry reaches callbacks unchanged.
- Validate entire request list before callbacks: nonempty, distinct names, enabled canonical entries, positive exact-int concurrency, formal binding name/family/pinned route match and one review basis. Google unresolved route is refused for invocation until host resolves it; no route fallback. Snapshot input/callback copies so callback mutation cannot alter later binding or final agreement.
- Bound simultaneous invokes and preserve input result order despite completion order. timeout_s applies to each preflight/invoke after scheduling, not time waiting for concurrency. A callback that returns after catching deadline cancellation still has a timed_out outcome. One call per request, no retries. Exceptions yield fixed failure code without exception text; self-cancelled child is a failed outcome, parent cancellation cancels and awaits active children and propagates CancelledError. No process/signal API. Document callbacks must cooperate with cancellation and reap their own native processes.
- [ ] RED concurrency tests use Events/barriers, not timing thresholds: four routes overlap, ceiling respected, output order stable, repeated-family siblings, mixed-basis/disabled/invalid/empty refusal before callbacks, preflight fail prevents any invoke, mutation attempt cannot change expected basis; one timeout/exception doesn't erase peers; parent cancel waits cleanup; no retries; investigations carry custom prompts/settings and cannot become agreement. Include integrated carrier→admission→agreement example with synthetic host callbacks.
- [ ] Observe RED; implement; focused GREEN and full suite. Commit and report.

### Task 4: Installed-package proof, compatibility and documentation

**Files:** create `tools/four_route_smoke.py`, `tests/test_four_route_smoke.py`, `docs/verification/2026-10-12-four-route-core.md`; modify `tools/verify_wheel.py`, `tools/codex_smoke.py` only where needed to consume compatible APIs; modify `.github/workflows/test.yml`, README, docs/status and earlier four-route direction to describe delivered APIs/limits. Bump project to `0.1.0.dev2` and update lock/expected version references together.

**Interfaces:** repository smoke driver `--wheel PATH --expected-version VERSION` installs wheel in isolated temp environment, proves site-packages imports, then synthetic all-four-route roster/render/output/admission/agreement and bounded-callback/investigation behavior. Runtime code must come from installed wheel, not repo source; test fixture/harness labels synthetic. Existing 10 raw replay and 54 Codex adapter cases must keep passing.

- [ ] RED installed-feature smoke invocation, then implement driver and test complete four-route success, dissent, sibling swap/failure/integrity block and independent investigations; cover all prompt profiles from wheel. Avoid duplicating package implementation in driver.
- [ ] Update public examples with asyncio host callbacks, explicit integrity/preflight responsibilities and cancellation limits, output carrier strictness, host marker handling; no claim host adoption, actual provider success, SDK execution or release. Historical reports remain historical.
- [ ] Run `uv sync --locked`, full pytest, sdist build, wheel rebuilt from sdist, full unpacked-sdist tests, `verify_wheel.py`, Codex smoke and four-route smoke, diff/link checks. Preserve exact output identities and distinguish local/macOS from native CI.
- [ ] Commit; root performs final whole-branch review and its bounded fix lifecycle, then normal feature-branch push/draft PR update and native Ubuntu24.04/macOS15 CI. Do not merge or publish. Verification doc records actual latest CI results only after observed success.

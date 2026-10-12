# Native Codex callback verification implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development. Steps use checkbox syntax for tracking.

**Goal:** Verify the installed dev2 callback path with fresh actual Codex responses, bounded parallel formal review, and separate perspective investigations inside this repository.

**Architecture:** Extend the existing repository test drivers with a supervised file exchange. The installed library calls async callbacks that publish bound requests; the root Codex task creates native children and atomically publishes their observed final-response receipts. This is a test harness, not a library transport or production custody implementation.

**Tech Stack:** Python 3.12, existing stdlib/pytest/uv helpers, existing dev2 wheel; no new dependencies.

**Spec:** [Four-route design](../../design/2026-10-12-configurable-four-leg-library.md), especially approved execution shape, plus the owner's approval of briefing items 1 and 2. Existing [callback contract](../../../README.md#async-host-callbacks) is unchanged.

## Global Constraints

- All implementation and integration tests stay in this library repository. Existing consumers and spec are not modified or executed.
- Keep package `0.1.0.dev2`, runtime APIs, canonical assets and dependency versions unchanged; this slice extends repository verification tools only.
- Use current installed wheel runtime with `-I`, a neutral child cwd and verified site-packages paths. Reuse existing driver helpers without adding repository package source to imports.
- No SDK, MCP, provider CLI, credentials, global settings, plugin installation, merge or release. Native children are root-supervised through collaboration tools only.
- All formal reviewers see the complete same scope for their round. Each fresh round has a unique review ID; repeated Codex entries have distinct leg names and one common digest.
- Return every actual result without repairing the verdict or re-prompting toward an expected answer. Investigation values are ordinary data and never approval ballots.
- Native spawn/capture/cancellation remain parent responsibilities. Native exit code is None. Requested settings and effective UNEXPOSED settings are distinct. Parent-captured final strings are not raw model wire bytes.
- Run Python/tests/builds/Git mutations/GitHub via `/bin/zsh -lic` with `sandbox_permissions="require_escalated"` from `/Users/chaniri/codex_workspace`, then enter this repository. Read-only file/Git inspection may use default sandbox.
- Preserve selected checkout/branch and unrelated state. One source writer; no recursive delegation by implementers/reviewers.

## Review Focus

- Receipt from another request or altered final bytes must not be accepted: Task 1 negative exchange tests.
- A changed packet/prompt/receipt after callback completion must block agreement: Task 1 fresh-integrity test.
- A queued third entry must not start before a slot opens: Task 1 barrier test and controller native trace.
- Cancellation must not leave an unacknowledged native child: Task 1 supervisor cleanup handshake tests; report native cancellation untested unless actually exercised.
- A valid dissent or a perspective answer must not be promoted to approval: Task 1 end-to-end tests and actual defect/investigation evidence.

### Task 1: Supervised installed-wheel native response driver

**Files:** create `tools/native_codex_smoke.py`, `tests/test_native_codex_smoke.py`; modify README with a short repository-driver protocol/reproduction section; add a synthetic exchange self-test CI step in `.github/workflows/test.yml` if supported by the same driver. Do not modify `src/`, other drivers, project metadata, schemas or dependencies.

**Interfaces and decisions:**
- CLI: `--wheel PATH --expected-version VERSION --config PATH --run-dir PATH`. Like existing drivers, outer command creates an isolated installation then forwards to a hidden installed-prefix child with neutral cwd; fail early on missing wheel/config or existing run-dir. Add `--self-test` as the alternative to config/run-dir for a provider-free exchange test from the installed wheel.
- Config: strict JSON object containing `mode` (`review` or `investigation`), `run_id` (fresh safe ASCII identifier), `max_concurrency` (positive exact int), `host` and nonempty `requests`. Each request contains canonical `entry` and existing codex-smoke `context`; investigations also contain nonempty `perspective`. Use the existing renderer/context validation. Require all entries Codex, enabled, unique safe names, explicit requested model/reasoning and bounded positive timeout_s. Review entries share one basis/scope/packet (except their leg_name). Investigation context provides bounded packet evidence but its output has no verdict schema.
- `host` is parent-supplied availability evidence: `supervisor="codex-parent"`, `native_tool="collaboration.spawn_agent"`, `supported_settings` list of `{model, reasoning}`, `capture_method="parent-tool-final-string"`, `cleanup="interrupt-and-await-terminal"`, `effective_settings="UNEXPOSED"`. Preflight verifies all requested settings against this declared capability list and packet/prompt paths before any request is published; it does not claim provider-enforced containment or measured effective settings.
- All run state belongs in a new canonical run directory. Write `manifest.json` with config/wheel/package identities and per-entry bindings/packet/prompt hashes. Each entry directory contains exact `prompt.txt` and `request.json`; publish request readiness last and atomically. No overwrite/reuse of a run directory or preexisting receipt. Safe names and canonical regular-file reads prevent path traversal/symlink input surprises; refuse malformed config before request publication.
- During `invoke`, record monotonic callback start/finish events and active/peak counts in one ordered in-memory trace, publish a request only after acquiring the library invoke slot, then await `receipt.json` with async polling. Parent first writes exact final UTF-8 bytes as `response.txt`, then atomically posts the receipt. Receipt must bind `run_id`, `leg_name`, `request_sha256`, `prompt_sha256`, `response_sha256`, unique nonempty `agent_id`, terminal `status` (`completed`, `failed`, `cancelled`), `capture_method`, requested settings matching entry, effective settings UNEXPOSED, and observed parent spawn/terminal timestamps. Required receipt fields/types are exact; duplicate JSON members are refused. Failed/cancelled receipts cannot become a successful output; completed receipt requires the original regular response file and hash.
- Native `ProviderOutput("native-final", original_bytes, None, True)` is created only for a matching observed completed receipt. No invented exit code, marker/fence stripping, response normalization or fallback. Parent stores original returned string verbatim; unexpected formatting is a failed observation.
- On invoke cancellation, publish `cancel-request.json`, await a matching terminal receipt/cleanup acknowledgement from the parent, then re-raise. This may wait indefinitely if the parent fails; document cooperative supervision. A completed receipt after cancellation is cleanup evidence only, never late success. Parent interrupts its owned child if needed and confirms terminal status before acknowledgement. Never invoke process/signal/native APIs in the driver.
- The final integrity callback freshly verifies config/wheel/packet/prompt/request and consumed response/receipt hashes and unique agent mappings. Ordinary mismatch preserves outcomes and sets integrity false. Investigations perform the same evidence recheck in the driver and report it separately; no agreement field is invented for investigations.
- Output `report.json` includes installed API paths/version/wheel hash, mode/run_id, capture label, full ordered callback trace/peak, per-leg original-response/receipt hashes and observations, dataclass outcomes (bytes represented only by hash/length), and real library agreement for review only. Report failed outcomes honestly; report creation is not a success verdict. Record actual raw verdicts via the library result rather than replacing them with expectations.
- Reuse `codex_smoke` helpers for packet/context/rendering and `four_route_smoke.identity` for all exported runtime import paths. Repository tools may load each other by explicit path; no duplication of admission, roster or concurrency algorithms.
- Expose a small async runner callable to tests so an async synthetic supervisor can service published requests. Synthetic self-test must be labelled synthetic and use this same file/callback path; cover three named formal entries with max2 and valid dissent plus a separate ordinary investigation. No provider calls in CI/tests.

- [x] Write meaningful RED tests: absent driver; actual callback path safe/negative; duplicate/wrong/stale receipt or altered bytes; input/packet/prompt mutation; canonical name/path validation; all preflight before publish; max2 with third queued and stable ordering; duplicate agent identity; cancel waits supervisor cleanup and late completion remains timeout/cancel; investigations preserve ordinary text without agreement.
- [x] Observe RED, implement minimal driver and focused GREEN; test harness detects an always-approve agreement mutation or bypassed receipt/hash validation.
- [x] Run full source suite; build sdist and wheel from it; run old 10/54/four-route drivers and new installed synthetic self-test; run unpacked-sdist suite; diff check. Retain logs under `_runs/native-codex-callbacks/` and report exact artifact hashes/import paths.
- [x] Self-review and commit exact owned files; report to the root for an independent task review and bounded fixes.

## Controller execution and completion

- [x] Prepare isolated correct and defective arithmetic fixtures and expected observations before native dispatch; no expected verdict in reviewer prompts. Correct: `cents * (100 - percent) // 100`; defective: `cents * percent // 100`. Inputs are nonnegative integer cents and integer percent in 0..100; no behavior outside that domain is required.
- [x] Correct round: three fresh independent native Codex/B full-scope reviewers, max_concurrency=2. Preserve actual answers. Native tool trace must show first two running together and no third spawn before its request is published after a receipt releases a slot. Target normal unanimous approval, without forcing it.
- [x] Defect round: one fresh native Codex/B full-scope reviewer; admit actual negative verdict and verify agreement blocks. A different observation is reported as such, never replaced by a crafted answer.
- [x] Investigation round: two fresh native Codex entries, max2, one boundary-case perspective and one test-design perspective on the same defective fixture. Preserve ordinary text, ensure no approval ballot or mutation of prior formal reports.
- [x] Root supervises all children, atomically captures original final strings/receipts, and retains tool snapshots/times/agent IDs. Finish or interrupt/await every owned child. Distinguish callback overlap, observed native running overlap and unexposed backend scheduling.
- [x] Write `docs/verification/2026-10-12-native-codex-callbacks.md` and update `docs/status.md` with measured results/limits; no migration guide (briefing item3) in this slice.
- [ ] Final independent review, normal branch push/draft PR update, native Ubuntu/macOS CI. Record exact implementation and final documentation heads; no merge/publication. Complete only after current checks and evidence review pass.

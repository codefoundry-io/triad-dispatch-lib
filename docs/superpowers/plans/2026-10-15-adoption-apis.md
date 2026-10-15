# Remaining Adoption APIs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the two approved library adoption seams while preserving existing decisions, copy contracts and privacy boundaries.

**Architecture:** Split validated-input roster merging from final resolved validation while the original resolver retains one schema snapshot. Annotate only the already selected canonical required-property error, then exercise both additions through existing installed-wheel drivers.

**Tech Stack:** Python >=3.12, jsonschema>=4.26,<5, referencing>=0.37,<1, uv/pytest and existing packaging tools.

**Spec:** [approved adoption API design](../../design/2026-10-15-adoption-apis.md). The owner approved roster implementation and `.missing`, and selected no public `.member` on 2026-10-15. Implementation is already authorized; no further design decision is pending.

## Global Constraints

- Work in the selected `codex/lib-adoption-followups` checkout, preserving all existing work. Start implementation only after the provenance/request-sync plan completes its required formal gate.
- Keep unpublished/source-pinned `0.1.0.dev4`; no version bump, dependency floor change, schema/prompt/generated-payload change, provider/config/default change or host port.
- All Python/tests/builds/Git/GitHub mutations/provider CLI calls use literal `/bin/zsh -lic` with `sandbox_permissions="require_escalated"`, host cwd `/Users/chaniri/codex_workspace`, then enter this repository. Read-only inspection can use default sandbox.
- Read current repository AGENTS/status and relevant workspace policies. Record Python/module preflight before tooling; permission failures are not test RED evidence.
- Preserve original error codes/text, parse → schema → expected → binding precedence, one schema snapshot within `resolve_roster`, independent copies and exact case-sensitive names.
- No `.member`, capture flags, duplicate pre-pass, raw validator exposure or host-specific diagnostic messages.
- Tasks are sequential: task1 owns shared API/conformance/README edits first, task2 updates them after task1 review; no concurrent writers to those files.
- Each implementer reports scoped files, RED/GREEN commands/output and commits. Fresh task review precedes the next task. The leader owns combined verification, PR updates and final project review; no final merge or publication.

## Review Focus

- An inherited vendor block or incomplete appended entry must survive merge but fail final validation; task1 pins both and keeps host checks separate.
- Invalid defaults plus malformed overrides must retain refusal precedence; task1 pins codes, same schema resource and no network retrieval.
- Mutating returned nested entries must not affect caller defaults; task1 exercises both combined and split paths.
- Later nested findings and multiple missing properties must report the selected object's canonical required name; task2 pins these and competing non-required errors.
- Installed source-vs-wheel confusion or ignored diagnostics must not produce false success; both tasks add actual installed behavior plus fault-injection controls.

## Size and files

Estimated production/runtime/export/verification-driver delta: +70–115 / -20–35,
net +50–80; approximately 30–50 novel core lines. Tests/fixtures: +230–350 lines;
documentation: +70–120 lines excluding this plan/design. These are estimates, not
caps; record actual additions/deletions/net and explain in-scope growth.

Task1: roster runtime/exports/tests, four-route driver, API/conformance/README.
Task2: admission runtime/tests, replay fixtures/driver, API/conformance/adoption/status.
Task3: bounded nonblocking provenance R2 followups in policy tests/migration docs;
approximately +15–30/-10–16 test lines and +2–4/-1 documentation lines, no runtime.
Leader: source/archive/wheel verification evidence, issue5 boundary proposal doc,
current PR description and complete project review. Issue5 remains proposals only.

Preceding plan gate: `20261015-lib-provenance-r2-b5ed9d` completed `AGREED`
on743e52a with all three required approvals and no Astra finding. Native CI
38697006277 passed four environments (953 source/archive tests each). Opus retained
three nonblocking followups: full parsed-rule pin, migration historical scope and
latest owner-decision wording. Tasks3 and2 explicitly close them here. No votes
transfer; the final combined tree receives fresh CI and full project review.

---

### Task 1: Add the merge-only roster seam

**Files to modify:**

- `src/triad_dispatch_lib/roster.py`: additive public seam, shared private merge.
- `src/triad_dispatch_lib/__init__.py`: imports and two `__all__` entries.
- `tests/test_roster.py`: split/combined parity and stage-boundary regressions.
- `tests/test_contracts.py`: existing roster identity test through new APIs.
- `tools/four_route_smoke.py`: actual new-API behavior in installed-wheel smoke.
- `tests/test_four_route_smoke.py`: smoke assertions, failure control, export count.
- `spec/reference/library-api.md`, `spec/reference/library-conformance.md`,
  `README.md`: current API/counts and exact coverage references after implementation.
- Adoption/status/evidence documents: coordinate with the root leader's combined
  unit; do not overwrite concurrent documentation work.

**Interfaces:**

```python
merge_roster(defaults: dict, overrides: str | bytes | None = None) -> dict
validate_resolved(roster: dict) -> None
resolve_roster(defaults: dict, overrides: str | bytes | None = None) -> dict
```
Both new functions must be callable at the package root and in its `roster` module.
Keep `resolve_roster`'s dictionary return. Its semantic sequence is merge, validate,
return merged; do not return the validator's `None`.

**Hard contracts:** Defaults resolved schema then exact duplicate names; override
strict parsing then override schema then exact duplicate names; merge; optional
final resolved schema then exact duplicate names. Defaults refuse before override
parsing. Existing parser refusals map to fixed `RosterError("invalid_json")`;
JSON `null` maps to `schema_violation`. Keep fixed error text, schema-first
precedence, offline reference refusal, existing nesting handling, exact case names,
recursive copy/merge/null/inheritance/order semantics, all-disabled/empty resolution,
and `select_entries`' validation/refusal behavior. Intermediate results are not
resolved/runnable data; host checks must safely handle incomplete entries and final
validation remains mandatory before consumption. No inherited block pruning,
case-folding, canonical schema changes, or host-specific diagnostic messages.

#### 1. Write the focused failing contract tests

- [ ] Add `test_roster_split_public_exports`: import the roster module, assert
  package-root `merge_roster`/`validate_resolved` are callable, are the module's
  same objects, and both names occur exactly once in `lib.__all__`.
- [ ] Add `test_merge_roster_preserves_inherited_block_until_validation`: use
  `defaults = roster(entry('claude', 'claude'))` and JSON override
  `roster({'name': 'claude', 'vendor': 'codex'})`. Assert merged vendor is codex,
  `claude == {}` remains, `codex` is absent, defaults are unchanged, and both
  `validate_resolved(merged)` and `resolve_roster(defaults, raw)` raise
  `RosterError` with `code == 'schema_violation'` and fixed text
  `Roster violates the canonical schema.`. Also assert `select_entries(merged)`
  refuses; do not demand any inherited-block message from the library.
- [ ] Add `test_merge_roster_returns_incomplete_append`: override the existing
  default with a new `{'name': 'new', 'vendor': 'codex'}`. Assert merge returns
  names `['c', 'new']` and the appended dict unchanged; final validation and the
  existing resolver refuse with `schema_violation`.
- [ ] Add `test_merge_roster_input_refusal_codes_and_precedence` with these rows
  (use `roster`/`entry` helpers, JSON-encode dictionary overrides):

  | Defaults | Override | Expected code |
  | --- | --- | --- |
  | `roster(entry(unknown=True))` | `'{'` | `schema_violation` |
  | `roster(entry(), entry())` | `'{'` | `duplicate_name` |
  | `roster(entry(unknown=True), entry())` | `None` | `schema_violation` |
  | `roster(entry())` | `roster({'name':'c'}, {'name':'c'})` | `duplicate_name` |
  | `roster(entry())` | `roster({'name':'c','unknown':True}, {'name':'c'})` | `schema_violation` |
  | `roster(entry())` | `'null'` | `schema_violation` |

- [ ] Add `test_validate_resolved_returns_none_without_mutation`: a valid roster
  with nested model/reasoning; save a deepcopy, assert return `is None` and exact
  input equality. Parameterize separate direct refusal cases: schema-valid
  duplicate names -> `duplicate_name`; duplicate names plus unknown field ->
  `schema_violation`; disabled entry with foreign vendor block -> `schema_violation`.
- [ ] Add `test_merge_roster_no_override_is_independent`: mutate a nested returned
  model and append a returned leg, then assert defaults equal their saved deepcopy.
- [ ] Add `test_split_resolution_retains_empty_disabled_and_case_sensitive_names`,
  parameterized with `roster()`, `roster(entry(enabled=False))`, and
  `roster(entry('c'), entry('C'))`. Assert merged equals defaults, validation
  returns `None`, and combined resolution equals merged. Selection raises
  `empty_selection` for the first two and returns names `['c','C']` for the third.
- [ ] Add `test_resolve_roster_uses_one_schema_snapshot`: monkeypatch the roster
  module's `load_roster_contract` with a counted loader that returns one saved
  schema and raises an assertion if invoked twice. Observe `_validate` while
  delegating to its original body. For valid defaults plus a named partial
  override, assert one load and validation events
  `[(schema, True), (schema, False), (schema, True)]` by object identity; result
  retains the untouched nested sibling. This pins both resource consistency and
  stage order, rather than timing or performance.

#### 2. Extend existing parity and safety coverage

- [ ] Convert the existing `resolve` helper in `tests/test_roster.py` into a
  `@pytest.fixture(params=['combined', 'split'])` returning a callable. The split
  callable merges, validates, then returns merged; the combined callable invokes
  the existing resolver. Add the fixture argument to the eight existing tests
  using that helper: `test_recursive_partial_null_merge_and_copy`,
  `test_four_routes_same_family_order_and_selection_copy`,
  `test_strict_json_refusal_is_fixed_roster_error`,
  `test_invalid_even_disabled_entries_refused`,
  `test_empty_selection_and_select_validation`,
  `test_preserves_opaque_settings_and_null_route_without_defaults`,
  `test_multiple_codex_entries_retained_separately`, and
  `test_schema_reference_cannot_retrieve_remote`. Existing invalid-result vectors
  still fail the split composition at its final validation; do not incorrectly
  require every such vector to fail merge alone.
- [ ] Strengthen the existing strict-JSON parameterized test's code assertion to
  `invalid_json`, retaining its fixed-text/no-raw-data assertion. Add direct
  `merge_roster` coverage for its same raw vectors (`'{'`, duplicate JSON legs
  member, NaN, `b'\xff'`, integer `42`), expecting `invalid_json` for each.
- [ ] Extend the remote-reference test with direct `merge_roster` and
  `validate_resolved` entry points: change resolved schema to external `$ref`,
  monkeypatch `socket.socket.connect` to fail on use, expect `ContractError`.
- [ ] Parameterize `tests/test_contracts.py::test_roster_schema_identity_refused_before_resolution`
  over `resolve_roster`, `merge_roster`, `validate_resolved`, invoking each with
  the empty roster fixture; retain its existing direct loader refusal for missing,
  wrong, and non-string canonical identities.

#### 3. Observe RED before runtime implementation

- [ ] In the tool call use `workdir=/Users/chaniri/codex_workspace` and
  `sandbox_permissions="require_escalated"`, with literal `/bin/zsh -lic` on
  the first invocation for every Python/test/build/Git mutation command.
  Record `command -v python3`, `python3 --version`, and
  `uv run --locked pytest --version` through that shell before Python tooling.
- [ ] Run `/bin/zsh -lic 'cd /Users/chaniri/codex_workspace/workspace/triad-dispatch-lib && uv run --locked pytest -q tests/test_roster.py tests/test_contracts.py'`.
  Required RED evidence: new missing-export/API tests fail because the two functions
  do not exist; source lookup/import/setup or permission failures are not causal RED.
  The one-schema-snapshot test may already pass and is a preservation check.

#### 4. Implement the minimum additive seam, then observe GREEN

- [ ] Retain `_validate` and `_merge` semantics. Extract the current validated-input
  merge body into private
  `_merge_roster(defaults: dict, overrides: str | bytes | None, schema: dict) -> dict`,
  which returns before final validation. `merge_roster` loads one schema and calls
  that helper. `validate_resolved` loads one schema and calls
  `_validate(roster, schema, resolved=True)`. `resolve_roster` loads **one** schema,
  uses the helper, validates the returned result with that same schema, and returns
  it. Do not compose the two public wrappers literally and load twice.
- [ ] Export both functions through `src/triad_dispatch_lib/__init__.py`; retain
  all existing exports and behavior, including `select_entries`.
- [ ] Rerun the focused command above with the same shell/permission mode.
  Expected: all focused tests pass with the combined/split matrix and exact codes.

#### 5. Pin actual installed-wheel behavior and update the public map

- [ ] Extend `tools/four_route_smoke.py::synthetic_smoke` before dispatch scenarios:
  form its existing informational-acceptance override with `merge_roster`, assert
  `validate_resolved(merged) is None`, assert equality with `resolve_roster`, and
  select from merged. Also merge its Claude entry `a` to vendor codex, assert the
  inherited Claude block remains, and require `validate_resolved` to raise fixed
  `schema_violation`; explicitly raise `AssertionError` if it accepts. Return a
  top-level `roster_split` report with
  `{'validated_parity': True, 'inherited_block_refused': True}` only after assertions.
  Keep the existing scenario `cases` map unchanged.
- [ ] In `tests/test_four_route_smoke.py::test_synthetic_four_route_matrix`, assert
  that exact new report. Add `test_matrix_detects_skipped_resolved_validation`:
  monkeypatch `lib.validate_resolved` to return `None` for everything and require
  `synthetic_smoke` to raise `AssertionError` for accepting the inherited block.
  Observe this test fail before adding the smoke assertions, then pass afterward.
- [ ] Change the real hardcoded assertion at
  `tests/test_four_route_smoke.py:155` from `observed['exports'] == 27` to `29`.
  Retain dynamic origin verification: `tools/four_route_smoke.py::identity` already
  enumerates every `lib.__all__` export and verifies its isolated `site-packages`
  path, including the two additions; no origin-check bypass or count-only smoke.
- [ ] Update README's current API count `27 -> 29` and
  `spec/reference/library-api.md:3-5` from `27`/`14 functions` to `29`/`16 functions`.
  Add both signatures, split validation/error order, independent copies and the
  unvalidated-result warning. Explain unchanged resolver return and host-owned
  checks. Extend the R-ROSTER/C12 conformance row with the new functions and the
  exact new test names. Do not alter canonical cases/schema/generated payloads.
- [ ] Run focused roster/contracts/smoke tests with the required shell and mode:
  `/bin/zsh -lic 'cd /Users/chaniri/codex_workspace/workspace/triad-dispatch-lib && uv run --locked pytest -q tests/test_roster.py tests/test_contracts.py tests/test_four_route_smoke.py'`.
  Expected: passing behavioral, origin/count, and fault-injection checks.

**Completion evidence belongs to the combined plan:** retain version
`0.1.0.dev4`; run its required source/archive suite, authoring/assets checks,
sdist-to-wheel rebuild, and installed-wheel drivers. The new actual installed
coverage is exercised by
`uv run --locked python tools/four_route_smoke.py --wheel dist/triad_dispatch_lib-0.1.0.dev4-py3-none-any.whl --expected-version 0.1.0.dev4`
under the same required shell/mode, with `roster_split` exactly true/true and both
new `runtime_paths` under isolated site-packages. The existing CI job in
`.github/workflows/test.yml:81-82` already invokes this driver against the wheel
rebuilt from the unpacked sdist. No provider/authenticated run is needed for L13.
Coordinate the commit and required formal review with the root leader; do not
create a separate release, merge, installation, or host-adoption claim.

**Estimate:** runtime/export/smoke +55–85 / -20–35 lines, net +35–50;
approximately 20–35 novel core lines. Tests/fixtures approximately +140–220 lines;
documentation approximately +35–60 lines. These are planning estimates; record
actual additions/deletions/net with the combined unit and preserve concurrent work.

- [ ] Commit scoped task1 changes, report exact RED/GREEN evidence and wait for task review before task2.

### Task 2: Add safe missing-required diagnostics

**Files and responsibilities**

- Runtime: `src/triad_dispatch_lib/errors.py` adds the constructor attribute; `src/triad_dispatch_lib/verdict.py` annotates the selected violation only.
- Unit tests: extend `tests/test_verdict.py::test_missing_required`; extend/add cases in `tests/test_admission_diagnostics.py`.
- Installed verification: extend `tools/verify_wheel.py::replay` and the matching `tests/test_replay.py` assertions. Add two authored synthetic raw fixtures in `tests/fixtures/replay/`, with explicit expected diagnostics in its existing `cases.json`.
- Documentation: `spec/reference/library-api.md`, `spec/reference/library-conformance.md`, `docs/status.md`, and the combined plan/design/verification record owned by the leader. Touch `docs/host-adoption.md` and the current request record only to reconcile the settled library boundary with concurrent documentation, without claiming host adoption. No `AGENTS.md` or instruction/prompt changes.

**Interfaces and precise behavior**

Public signatures remain `AdmissionError(code: str)` and `validate_verdict(raw: str | bytes, *, expected: dict) -> dict`. Every `AdmissionError` initializes `missing: str | None = None`. Only a selected canonical `required` schema violation sets it.

The minimal structured-metadata checks are: `validation_error.validator == "required"`, `validator_value` is a list whose elements are strings, and `instance` is a dictionary. The latter two are inexpensive guards on optional diagnostic extraction, rather than new admission predicates. All names come from that trusted canonical rule's `validator_value`; the instance is consulted only for membership. Return the first name absent from that dictionary in **required-list order**, or leave `None` if metadata is unsuitable or no name is absent. Do not copy a provider key. No second schema lookup, schema traversal, duplicate metadata equality check, schema revalidation, public helper or new exception/code is necessary.

Keep this small extraction inline in the existing `except ValidationError` block after assigning `.path`. Do not sort/collect errors, inspect descendant `context`, parse `message`, expose raw errors, reconstruct an instance pointer, or look up a schema node using `.path`. If the existing winner is not `required`, `.missing` stays `None` even when other required data is absent. Global winner selection remains unspecified; this task preserves its implementation and annotates only the caught violation. For multiple missing names at that selected rule, the schema list fixes the name order.

Preserve `.field`, `.path`, `.code`, fixed `str(error)`/`.args`, suppressed displayed chaining and parse → schema → expected → binding order. Root `required` path is `("required",)`; finding required path is `("properties", "findings", "items", "required")`. The latter omits the finding instance index. `.missing` does not extend the path.

#### RED/GREEN 1 — runtime and focused diagnostics

- [ ] Write/extend the exact tests below before changing runtime files. Reuse `BASE`, `FINDING`, `BINDINGS` and `refusal()` already defined in the tests. Always pass the complete unmodified `BASE` expected binding when removing a binding field from test input, so test setup does not raise `KeyError` first.

| Exact test name | Input and exact assertions |
|---|---|
| `tests/test_verdict.py::test_missing_required` (extend existing 12 root cases) | Delete each `field` in `list(BASE)`; pass `{name: BASE[name] for name in BINDINGS}`. Assert `code == "schema_violation"`, `missing == field`, `field is None`, `path == ("required",)`, `args == ("Verdict violates the canonical schema.",)`. |
| `tests/test_admission_diagnostics.py::test_missing_nested_required_is_canonical` (new, 7 cases) | Parameterize argument `missing_parameter` with `("path", "line", "severity", "summary", "trigger", "evidence", "context_known")`. Use `BASE | {"verdict": "MERGE WITH FIXES", "findings": [{k: v for k, v in FINDING.items() if k != missing_parameter}]}`. Assert `error.code == "schema_violation"`, `error.missing == missing_parameter`, `error.field is None`, nested required path, fixed args. |
| `tests/test_admission_diagnostics.py::test_missing_uses_selected_finding_object` (new) | Negative verdict with `[dict(FINDING), FINDING without "severity"]`. Assert `missing == "severity"` and the nested required schema path; no finding index is added. A scan of the root/first finding would fail this test. |
| `tests/test_admission_diagnostics.py::test_multiple_missing_follow_selected_required_order` (new, 2 cases) | Root omit `review_id` and `family`: expect `missing == "review_id"`, path `("required",)`. Nested finding omit `severity` and `summary`: expect `missing == "severity"`, nested required path. Construct removals in reverse order to demonstrate input/removal order does not select the name. Assert schema code/fixed args in both cases. |
| `tests/test_admission_diagnostics.py::test_competing_schema_error_keeps_existing_winner` (new) | Remove root `review_id`, then add `PRIVATE_PROPERTY="PRIVATE_VALUE"`. Assert `code == "schema_violation"`, `path == ("additionalProperties",)`, `missing is None`, `field is None`, fixed args. This protects the present earlier non-required selection without declaring a general stable global winner rule. |
| `tests/test_admission_diagnostics.py::test_constructor_retains_message_args_and_empty_diagnostics` (extend existing 9 code cases) | Add `missing is None` and `not hasattr(error, "member")`; keep all existing code/args/field/path assertions. No opt-in member API is introduced. |
| `tests/test_admission_diagnostics.py::test_binding_field_is_canonical` (extend existing 6 cases) | Add `missing is None`; retain existing field, empty path and fixed binding args. |
| `tests/test_admission_diagnostics.py::test_schema_path_contains_only_trusted_schema_location` (extend existing 4 cases) | Add `missing is None`; preserve all current path, field, message/args and chaining assertions. |
| `tests/test_admission_diagnostics.py::test_parse_schema_expected_binding_precedence` (extend existing table) | Existing rows retain `.missing is None`. Add raw `"NaN"`, expected `{}` → `nonfinite_number`, `missing is None`; add serialized `BASE` without `review_id`, expected `{}` → `schema_violation`, `missing == "review_id"`, `path == ("required",)`; add serialized valid `BASE`, complete binding with changed `review_id` → `binding_mismatch`, `field == "review_id"`, `missing is None`, `path is None`. Keep existing duplicate → schema → invalid-expected cases; add expected field/missing/path columns rather than weakening their assertions. |
| `tests/test_admission_diagnostics.py::test_missing_guaranteed_surface_does_not_echo_provider_data` (new) | Negative verdict, remove root `review_id`, put `PRIVATE_VALUE` in the finding's summary and `PRIVATE_PROPERTY="PRIVATE_NESTED_VALUE"` on that later finding. Root required wins before validating findings. Assert `missing == "review_id"`, root required path, fixed args; assert `"PRIVATE"` absent from `repr((error.code, str(error), error.args, error.field, error.path, error.missing))`; assert no `member` attribute. Do not assert that `__context__` or traceback locals contain no input. |
| `tests/test_admission_diagnostics.py::test_duplicate_name_stays_out_of_guaranteed_surface` (new) | Call `validate_verdict('{"PRIVATE_KEY":1,"PRIVATE_KEY":2}', expected={})`; assert `code == "duplicate_member"`, `missing is None`, `field is None`, `path is None`, `args == ("Duplicate JSON object member.",)`, no `member` attribute, and `"PRIVATE"` absent from the same explicit guaranteed-surface projection. |

No synthetic malformed-`ValidationError` matrix is required: canonical schema validation and jsonschema's required keyword establish the ordinary metadata. The guarded `None` fallback must not add failure behavior. No new test framework or duplicated schema validator is needed.

- [ ] Run RED from the host cwd with `sandbox_permissions="require_escalated"`:

```sh
/bin/zsh -lic 'cd /Users/chaniri/codex_workspace/workspace/triad-dispatch-lib && uv run --locked pytest -q tests/test_admission_diagnostics.py tests/test_verdict.py'
```

Expected: newly extended assertions fail because `AdmissionError` lacks `.missing`. Preserve actual failures; diagnose environment/setup failures separately and do not label them the intended RED.

- [ ] Add `self.missing: str | None = None` in the existing constructor. Add only the guarded first-absent canonical-name extraction to the selected schema-violation handler. Do not change `parse_json`, validation order, error messages or version metadata.

- [ ] Run GREEN and neighboring original parser checks through the same shell/permission mode:

```sh
/bin/zsh -lic 'cd /Users/chaniri/codex_workspace/workspace/triad-dispatch-lib && uv run --locked pytest -q tests/test_admission_diagnostics.py tests/test_verdict.py tests/test_json_input.py'
```

Expected: all selected tests pass; root/nested missing metadata is additive, and duplicate/nonfinite/UTF-8 behavior stays unchanged.

#### RED/GREEN 2 — existing installed-wheel driver enforces the attribute

- [ ] Add authored synthetic raw fixtures `tests/fixtures/replay/missing-root.json` and `missing-finding.json`. Do not rewrite, format or normalize existing raw fixtures. Write complete new objects using the existing replay binding (`review_id="replay-1"`, family `codex`, digest `"a" * 64`, leg `codex-leg`, attempt `1`, route `null`): root fixture omits only `review_id` from an otherwise valid SAFE verdict; nested fixture is a `MERGE WITH FIXES` verdict containing a finding `{ "path": "src/main.py", "line": 1, "summary": "Summary", "trigger": "Input", "evidence": "Observed", "context_known": true }` with only `severity` absent. Keep all other required verdict fields valid as in `BASE`.

- [ ] Append manifest cases `missing-root`, then `missing-finding`, with `outcome: "schema_violation"`, complete expected replay bindings and a new optional **test-fixture** metadata field `diagnostics`: root `{"missing": "review_id", "path": ["required"]}`; nested `{"missing": "severity", "path": ["properties", "findings", "items", "required"]}`. This is replay-fixture metadata, not a wire/API schema change. Document it in `tests/fixtures/replay/README.md`.

- [ ] Extend `tests/test_replay.py::test_replay_vectors`: for a refused case carrying `diagnostics`, assert `caught.value.missing == case["diagnostics"]["missing"]` and `caught.value.path == tuple(case["diagnostics"]["path"])`, in addition to the current code assertion.

- [ ] Add `tests/test_replay.py::test_installed_probe_checks_missing_diagnostic`. Capture the real package-root `validate_verdict`; monkeypatch that export with a wrapper which calls it and, on `AdmissionError`, sets `error.missing = "wrong-required-name"` before re-raising. Call `verifier().replay(ROOT)` and require `pytest.raises(AssertionError, match="unexpected diagnostic: missing-root")`. Other corpus outcomes must remain intact; the first annotated case is `missing-root`. This proves the existing driver checks the attribute rather than merely continuing to replay admission codes.

- [ ] Run RED for that driver guard test before updating the driver:

```sh
/bin/zsh -lic 'cd /Users/chaniri/codex_workspace/workspace/triad-dispatch-lib && uv run --locked pytest -q tests/test_replay.py::test_installed_probe_checks_missing_diagnostic'
```

Expected: `DID NOT RAISE`, because the current `replay()` checks only the code. This RED differs from the runtime attribute RED and proves the verification gap.

- [ ] In `tools/verify_wheel.py::replay`, after checking an expected refusal code, compare `.missing` and `.path` to optional fixture `diagnostics`. On mismatch raise `AssertionError(f"unexpected diagnostic: {case['name']}") from None`; do not interpolate provider text, diagnostic objects or payloads. Keep the return list, report shape, CLI, isolated import check and installation lifecycle unchanged.

- [ ] Run GREEN:

```sh
/bin/zsh -lic 'cd /Users/chaniri/codex_workspace/workspace/triad-dispatch-lib && uv run --locked pytest -q tests/test_replay.py tests/test_admission_diagnostics.py tests/test_verdict.py tests/test_json_input.py'
```

Expected: all pass, including `test_installed_probe_checks_missing_diagnostic` and existing `test_installed_probe_replays_vectors`. During actual wheel verification, `probe()` already calls `replay()` only after proving the package loads from the isolated environment's `site-packages`; its `-I` child runs from a neutral temporary directory. Thus the newly annotated raw cases exercise the installed library rather than the source package or a host integration.

#### Documentation and combined-unit verification

- [ ] Update the API reference to define `.missing`, selected-required-list order, the non-required `None` cases and the existing winner-selection limit. Explicitly preserve duplicate-name non-disclosure and the documented exception-internal privacy limit. Record the owner decision as settled; leave consumer adaptation/strict-parser deviation with its owner. Add test anchors in the conformance map and current progress/verification evidence without changing historical claims.

- [ ] Hand this task's GREEN results and exact changed-file list to the leader of the combined remaining-adoption-APIs unit. Source, archive and package verification are performed once on that final combined tree, after the roster task is integrated; do not rerun full suites independently merely to accumulate duplicate evidence.


- [ ] Commit scoped task2 changes and report exact RED/GREEN evidence for fresh task review. Current exports remain29 after task1.

### Task 3: Close nonblocking provenance-review followups

**Files:** Modify `spec/tests/test_policy_profiles.py`, `spec/MIGRATION.md`;
record scoped verification in the task report. Do not change actual policy
payloads/digests or historical import ancestry.

**Interfaces:** Consumes R2's accepted Minor findings at candidate743e52a;
produces complete comment-independent rule preservation and unambiguous migration
history. No runtime API/export change. R2-M3 current decision wording belongs
to task2, which must replace pending `.missing`/`.member` decisions accurately.

- [ ] Read the R2 findings and current rule test. Replace or strengthen the
  tuple-only pin with a hand-authored literal complete parsed rule list: every
  existing toolName/decision/priority and the existing denyMessage are preserved.
  Include exact keys, array grouping and duplicate-row/order visibility so an
  added `modes`, `interactive` or `argsPattern` qualifier cannot pass unnoticed.
  Keep current manifest binding and the web/no-web comparison.
- [ ] Use only copied policy fixtures for controls. Add `modes = ["autoEdit"]`
  to the `run_shell_command` deny rule and show the old tuple test accepts the
  change but the strengthened assertion rejects it. Prepending a comment must
  still pass. Record actual command/output; do not temporarily alter canonical
  source policy bytes or manufacture a provider enforcement observation.
- [ ] In `spec/MIGRATION.md`, scope unchanged canonical payload/schema-identity
  wording to the original consolidation move; explain later authorized policy
  comment edits are tracked by adjacent manifests and require independent host
  re-vendoring. No wording test or host implementation change.
- [ ] Run `uv run --locked pytest -q spec/tests/test_policy_profiles.py`, authoring
  and assets checks, `git diff --check` through the required shell/mode. Confirm
  policy payloads/digests/import-origin equal task start. The combined final
  matrix supplies full source/archive/wheel coverage after all tasks.
- [ ] Commit only the two scoped files and report controls/checks for a fresh
  task review. All three R2 followups must appear in the final combined review
  packet; no R2 vote transfers to changed bytes.



## Combined verification and review (leader-owned)

- [ ] Read current README packaging commands and `.github/workflows/test.yml`.
  Run the source suite, authoring and asset checks on the completed combined tree.
- [ ] Create an exact owned neutral temporary directory using `tempfile.mkdtemp`.
  Build the sdist with `uv build --sdist`; extract with `tarfile` data filter into
  that directory and assert exactly one source root. Record its actual path.
  In the extracted source, unset VIRTUAL_ENV, `uv sync --locked`, run `uv run
  --locked pytest -q`, authoring/assets checks, and `uv build --wheel`. Run all
  four existing installed drivers from the checkout against that rebuilt wheel:
  `verify_wheel.py`, `codex_smoke.py ... self-test`, `four_route_smoke.py`, and
  `native_codex_smoke.py ... --self-test`, with version `0.1.0.dev4`.
- [ ] Record artifact hashes, platform/Python versions, exact test counts,
  new roster_split report and both diagnostic replay cases in
  `docs/verification/2026-10-15-adoption-apis.md`. Source/archive/wheel proof is
  synthetic library proof; no actual provider or consumer adoption is claimed.
- [ ] Add `docs/design/2026-10-15-adoption-boundary-proposals.md` from the reviewed
  issue5 proposal table. Link it from current requests/status; no L1/L4/L6/L8/L9
  runtime implementation is authorized by that proposal.
- [ ] Check API/export coverage and conformance test references; no stale claim
  that `.missing` remains undecided or `.member` will be added in this slice.
  Preserve historical dated records. Review `git diff --check`, commit scoped
  evidence/docs, rewrite draft PR title/body around the final combined change,
  push and wait for all four native macOS/Ubuntu Python3.12/3.14 CI jobs at HEAD.
- [ ] Freeze the current tree. Run the project public-v2 three required reviewers
  Opus5.5/xhigh, Sol6.1/xhigh and Argon/high, plus separate nonvoting Astra/high,
  each2400 seconds and official current web verification allowed. Inspect the
  whole combined branch including the already reviewed documentation unit.
  Save and adjudicate every result; await all producers before final integrity,
  export and cleanup. Changed reviewed bytes require a new complete round.
- [ ] Report the draft PR, precise verification/review results and remaining
  adoption/publication/merge boundaries. Do not merge or close issues by inference.

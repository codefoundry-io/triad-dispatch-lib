# Current library conformance map

`R-AGY-METADATA` / C80 is implemented by `separate_agy_metadata` and AGY-only
`admit_output`. `tests/test_output.py` and the installed public API consumer
probe verify metadata separation with original-byte, negative-verdict,
declared-name and strict-invalid controls. `extract_final` and generic
`validate_verdict` keep their prior contracts. Hosts retain provider execution,
terminal recovery, raw log custody and independent adapter adoption; library
tests alone do not certify those paths.

This map connects canonical rules/cases to current shared implementation and
tests. Each row maps only the named portion; it does not certify every axis of
a case or replace host conformance evidence. Paths are relative to the library
root. Rule anchors are in [review-rules.md](review-rules.md), cases in
[cases.json](../cases/cases.json), and host integration obligations in
[independent adoption](../../docs/host-adoption.md#required-adapter-contracts).

Keep the historical A/B pointers in cases and units intact. When changing shared
semantics, update the applicable library code, tests and this map together.
The reverse interface contract is [library-api.md](library-api.md). A helper's
internal signature is not a new provider wire requirement.
The [complete case disposition map](library-case-coverage.md) assigns all 58
actual cases to partial library evidence and remaining owners.

| Rules / cases | Implemented library portion | Evidence in current tests | Remaining host responsibility |
| --- | --- | --- | --- |
| R-BIND; C14, C30 | `json_input.parse_json`, `verdict.validate_verdict`: original JSON, duplicate/nonfinite refusal, schema | `tests/test_json_input.py::test_rejected_raw`, `test_decoder_limits`; `tests/test_verdict.py::test_original_members_reach_parser`, `test_schema_rejections` | Original response capture, input size limits, no v1 conversion |
| R-BIND; C14, C30, C66 (partial) | `verdict.validate_binding`, `validate_verdict`: six exact invocation fields | `tests/test_verdict.py::test_each_binding`, `test_expected_shape`; `tests/test_agreement.py::test_all_binding_fields_are_rechecked` | Attempt allocation, custody, seals and round invalidation |
| R-ROSTER, R-MODEL, R-GOOGLE; C12, C18, C22, C27, C33 (partial) | `roster.merge_roster`, `validate_resolved`, `resolve_roster`, `select_entries`: validated-input merge, resolved validation, selection, opaque settings | `tests/test_roster.py::test_recursive_partial_null_merge_and_copy`, `test_four_routes_same_family_order_and_selection_copy`, `test_preserves_opaque_settings_and_null_route_without_defaults`, `test_roster_split_public_exports`, `test_merge_roster_preserves_inherited_block_until_validation`, `test_merge_roster_returns_incomplete_append`, `test_merge_roster_input_refusal_codes_and_precedence`, `test_validate_resolved_returns_none_without_mutation`, `test_validate_resolved_refuses_invalid_rosters`, `test_merge_roster_no_override_is_independent`, `test_split_resolution_retains_empty_disabled_and_case_sensitive_names`, `test_resolve_roster_uses_one_schema_snapshot`, `test_merge_roster_strict_json_refusal`, `test_schema_reference_cannot_retrieve_remote`; `tests/test_contracts.py::test_roster_schema_identity_refused_before_resolution`; `tests/test_four_route_smoke.py::test_synthetic_four_route_matrix`, `test_matrix_detects_skipped_resolved_validation` | Safe inspection of incomplete intermediate entries, final validation before consumption, actual capability checks, native defaults and unresolved route selection |
| R-PROMPT; C60, C67 (partial) | `prompts.render_review_clauses`: review purpose and supplied date | `tests/test_prompts.py::test_phase_and_order`, `test_web_and_arguments`, `test_all_family_host_phase_profiles` | Compute/bind preparation UTC date and common scope; retain on retry |
| R-CONTEXT, R-REREVIEW; C61-C63 (partial) | `prompts.render_data`: safe residual encoding; `render_review_clauses`: one-pass substitution | `tests/test_prompts.py::test_residual_roundtrip`, `test_replacement_once`, `test_google_replacement_is_one_pass_and_extra_keys_refused` | Currentness, once-only insertion, evidence materialization and retention |
| R-PROMPT, R-CONTAIN, R-REVIEW-WEB; C32, C70-C73 (partial) | `prompts.render_review_clauses`: host/route/web clauses | `tests/test_prompts.py::test_web_selection_and_default`, `test_google_hook_route`, `test_invalid_routes_and_hook`, `test_order_skips_host_inapplicable_clause` | Tool permissions, read availability, containment and native agent configuration |
| R-INVEST; C25, C29, C31 (partial) | `prompts.render_investigation_prompt`, `dispatch.run_investigations`: ordinary results, no ballot | `tests/test_prompts.py::test_investigation_suffix_only_google_web`; `tests/test_dispatch.py::test_investigations_keep_prompts_settings_and_are_ordinary_data` | Actual tool authorization and fetched evidence verification |
| R-AGREE; C13, C21, C33, C64 (partial) | `agreement.evaluate_agreement`: every selected entry, fresh binding admission, unanimous affirmative and true integrity | `tests/test_agreement.py::test_every_same_family_leg_counts`, `test_negative_invalid_stale_and_swapped_block`, `test_host_integrity_blocks_unanimous_safe`, `test_four_carrier_round_counts_both_google_routes` | Complete selection, fresh integrity and host-fault handling; merge authorization |
| R-PREPARE, R-TERMINAL; C1, C2, C78 (partial) | `dispatch.run_review`: all preflights, bounded callbacks, one invocation, ordered outcomes | `tests/test_dispatch.py::test_four_routes_overlap_preserve_order_and_admit_carriers`, `test_all_preflights_finish_before_invoke_and_failure_aborts`, `test_queued_invoke_has_its_full_deadline_after_slot_acquisition` | Spawning, vendor retries, direct-child completion and process reaping |
| R-TERMINAL; C1, C78 (partial) | Callback deadline/cancellation ownership, including wait-setup exceptions | `tests/test_dispatch.py::test_parent_cancel_awaits_child_cleanup_and_propagates`, `test_parent_cancellation_during_deadline_cleanup_waits_without_recancelling`, `test_overflowing_timeout_does_not_leave_a_callback_after_coordinator_error` | Cooperative native cleanup; no forced termination guarantee |
| R-BIND, R-TERMINAL; C14, C30, C78 (partial) | `output.extract_final`, `admit_output`: typed terminal guards and original member spans | `tests/test_output.py::test_admit_all_carriers`, `test_extraction_preserves_original_representation`, `test_full_envelope_is_strict`, `test_terminal_guards_precede_payload`, `test_google_sibling_carrier_cannot_swap` | Truthful execution observations and unsupported envelope adaptation |
| R-CONTAIN; C23 (strict subset only) | Strict successful AGY stream admission; no finish-recovery analyzer | `tests/test_output.py::test_agy_missing_or_failed_result_refused`, `test_agy_exit_three_refuses_partial_valid_result_before_parse` | Preserve qualifying same-run recovery and all its structured evidence/guards |
| R-CLASSIFY, R-AUTH, R-TOKENS, R-NOCOST; C8, C11, C17, C37, C43, C74-C77 | No extracted classifier/auth/token API | `tests/test_output.py::test_quota_looking_evidence_is_ordinary_data` covers only the no-keyword-classification boundary | Vendor sentence carriers, credentials, STOP precedence, exit tokens and repair |
| R-PREPARE, R-BIND, R-RECEIPT, R-CLEANUP, R-PLATFORM (partial packaged-content portion) | `contracts` / `bundle_manifest`, `tools/sync_spec_assets.py`: packaged consistency and generation | `tests/test_contracts.py::test_manifest_and_digest`, `test_broken_contract`; `tests/test_spec_assets.py::test_generation_preserves_bytes_and_is_deterministic`, `test_check_never_writes_on_drift`, `test_symlinks_refused_without_touching_outside`, `test_symlink_status_errors_refuse_before_writes`, `test_tree_enumeration_errors_refuse_before_writes`, `test_unreadable_output_directory_refuses_before_following_link`, `test_output_root_observation_error_never_skips_inventory`, `test_output_root_missing_and_occupied_controls`, `test_following_metadata_errors_preserve_errno_before_writes`, `test_source_root_missing_and_file_preserve_diagnostics` | Packet custody, authenticity, host receipts/seals, deletion roots, installers, native platform evidence |

The additive dev4 observability APIs provide these partial contracts:

| Contract | Shared implementation and tests | Host boundary |
| --- | --- | --- |
| Issue #9; R-ROSTER diagnostics (partial) | `RosterError.path/missing/document`; `tests/test_roster_diagnostics.py` covers defaults/override/resolved attribution, selected required/non-required winners, both Google route-block vectors, ordering/copies and non-schema `None` metadata; installed diagnostic controls in `tests/test_replay.py` | Schema-only public metadata; arbitrary unknown-key spelling declined for this slice; Python exception internals and host formatting remain separate |
| Issue #10 / L3; R-RECEIPT, C9 (shape only) | `validate_transport_receipt`, `ReceiptError`; `tests/test_receipt.py` covers required/type/vocabulary/native constraints, no mutation, whole-envelope refusal, opaque versions, recursion and offline/broken contracts; installed probe in `tools/verify_wheel.py` and negative controls in `tests/test_replay.py` | Truthful input delivery/execution, command equality, attempt currency, envelopes, ownership/seals/reads and collection |
| L2; R-BIND diagnostic context | `AdmissionError.field/path/missing`; `tests/test_admission_diagnostics.py::test_binding_field_is_canonical`, `test_schema_path_contains_only_trusted_schema_location`, `test_missing_nested_required_is_canonical`, `test_missing_uses_selected_finding_object`, `test_multiple_missing_follow_selected_required_order`, `test_competing_schema_error_keeps_existing_winner`, `test_missing_guaranteed_surface_does_not_echo_provider_data`, `test_duplicate_name_stays_out_of_guaranteed_surface`, `test_parse_schema_expected_binding_precedence`; `tests/test_verdict.py::test_missing_required`; `tests/test_replay.py::test_replay_vectors`, `test_installed_probe_checks_missing_diagnostic` | Safe locations supplement existing admission codes; no operational diagnosis, raw payload or custody attestation |
| L7; R-PROMPT/R-PREPARE source-clause evidence | `render_review_clauses(with_manifest=True)`; `tests/test_prompt_manifest.py::test_profiles_have_exact_source_hashes_and_identical_rendering`, `test_manifest_is_fresh_and_independent_of_substitutions`, `test_manifest_still_refuses_tampered_verified_bundle` | Host binds final prompt/bundle identities and checks actual execution; manifest hashes are pre-substitution source evidence |

## Remaining normative groups and ownership

The first implementation table above names 20 of the 28 active review-rule groups.
The eight remaining groups and five process/authoring groups are assigned here,
so omission from a runtime table cannot be mistaken for an unimplemented library
feature. This inventories all 33 active unique groups, not every sentence or case
axis. Historical duplicate headings are not additional rules.

| Group / canonical location | Current implementation or explicit owner | Verification boundary |
| --- | --- | --- |
| [R-RETRY](review-rules.md#R-RETRY) | Host allocates/diagnoses retries and fresh rounds; coordinator invokes once | Callback tests do not certify host retry custody |
| [R-AGENT-ROLES](review-rules.md#R-AGENT-ROLES) | Host native presets, Claude definitions and AGY profiles | Opaque roster strings are not model availability or role-loader evidence |
| [R-SMELL](review-rules.md#R-SMELL) | Leader selects evidence-backed review criteria | Renderer transports criteria-related clauses; no automatic quality judgment |
| [R-STOP](review-rules.md#R-STOP) | Leader owns convergence, scope/design decisions and escalation | A stopping decision never turns dissent into approval |
| [R-THREAT](review-rules.md#R-THREAT) | Canonical deployment-context clause is rendered; leader applies the threat scope | Prompt transport does not enforce native containment |
| [R-VERIFY](review-rules.md#R-VERIFY) | Leader verifies claims and dispositions; developer owns bounded prompt checks | Synthetic tests do not prove live reviewer behavior |
| [R-CLI-VERSION](review-rules.md#R-CLI-VERSION) | Host observes binaries/versions and enforces justified route floors | No library CLI catalog, probe or auto-upgrade |
| [R-PARITY](review-rules.md#R-PARITY) | Common semantics live here; native exceptions and adoption belong to each host | Library tests plus each host's conformance evidence are needed |
| [R-DIAG](process.md#R-DIAG) | Leader diagnoses failures, retains evidence and makes scoped decisions | Typed parser/coordinator errors are not the operational diagnosis workflow |
| [R-PRD-SPEC](spec-authoring.md#R-PRD-SPEC) | Source authoring maps/schema/checker; `spec/tests/test_authoring.py::test_reference_metadata_error_refuses_before_read`, `test_local_reference_controls_preserve_missing_diagnostics` | Source development check; reference observation errors refuse before reads and missing-path diagnostics remain; absent from installed runtime intentionally |
| [R-AUTHORING-SYNC](spec-authoring.md#R-AUTHORING-SYNC) | Maintainers reconcile current sources and notify affected hosts | Runtime does not fetch mutable specification revisions |
| [R-DECISION-ORDER](spec-authoring.md#R-DECISION-ORDER) | Maintainers resolve shared gaps before host-specific implementation | New common semantics require a specification decision, not a private host fork |
| [R-DEV-LOG](../authoring/shared-dev-log.md#R-DEV-LOG) | Maintainers record common drift/defects and affected host/case ownership | Historical host records are not current library execution proof |

The canonical contract directory has 20 files excluding its README: four runtime
schemas and sixteen source-only host/development reference or profile files.
Five prompt payloads complete the nine packaged payloads in four bundles.
Only the unchanged transport-object `receipt-fields.json` joins the runtime
schemas; other host receipt/token/profile files stay in source/sdist deliberately.
The behavioral corpus
has 58 actual cases, with non-contiguous IDs; its largest ID is not its case count.

`spec/tests/test_spec_records.py::test_live_model_refusal_measurement_claims_match_vendor_rows`
checks the known R-GOOGLE measurement clauses against CLI/token model-refusal
rows, with both mismatch directions in test-only controls. It is a bounded record
consistency check, not a classifier, model-ID pin or CLI-version gate. Future
measurement prose forms require deliberate updates to this regression alongside
accepted rows; PR #12's proposed rows and rule replacement remain held.

## API limits that adoption must preserve

`run_review` blocks agreement on ordinary integrity callback failure, but does
not distinguish that failure from a completed negative check. The test
`tests/test_dispatch.py::test_integrity_failure_keeps_completed_outcomes_and_blocks`
establishes this API behavior, not full R-AGREE host-fault conformance.
`ContractError` remains separately propagated after callback cleanup.

`native-final` accepts host-adapted original final JSON for any family, with
truthful host-observed completion/transport fields. It retains strict schema
and binding checks; it does not attest execution, runtime identity or custody.
`tests/test_output.py::test_native_does_not_strip_host_markers` covers the
library's refusal to remove host markers itself.

The supervised driver in `tools/native_codex_smoke.py` is repository test support,
not an installed host adapter. Its cancellation acknowledgement regressions live
in `tests/test_native_codex_smoke.py`; they prove the file-exchange protocol with
synthetic parent evidence, not native backend termination.

`tests/test_native_codex_smoke.py::test_outer_cli_retains_child_and_environment_until_terminal_ack`
exercises the real outer/inner driver processes, PID/process-group SIGINT,
repeated interrupts and delayed synthetic acknowledgement. Its regression
fixture substitutes only installed-runtime bootstrap; separate CLI experiments
exercise wheel installation. `tests/test_native_codex_smoke.py::test_driver_refuses_casefold_name_collision_before_artifacts`
checks portable driver-name refusal before artifact creation while the shared
roster keeps exact-case identities.
`tests/test_native_codex_smoke.py::test_outer_cli_preserves_pending_interrupt_and_forwards_once_on_reentry`
covers interruption before child binding, repeated handler entry and restoration
of the prior signal handler.
`tests/test_native_codex_smoke.py::test_self_test_interrupt_drains_synthetic_supervisor_and_cleans_environment`
covers normal self-test completion and repeated PID/process-group interrupts
during review and investigation. A scheduler-only gate holds a published
request pending while the real outer/inner processes run; after release, the
synthetic supervisor drains before cancellation propagates and both temporary
directories are removed. This is synthetic lifecycle evidence, not provider
termination or a claim about ordinary scheduler frequency.
Two additional cases inject response/receipt failure while SIGINT cleanup is
already awaiting the scenario; they preserve the inner filesystem error while
the interrupted outer CLI retains exit 130.
`tests/test_native_codex_smoke.py::test_self_test_publication_failure_preserves_error_and_cleans_owned_work`
covers response/receipt EIO and ENOSPC after request publication in review and
investigation, preserving the original error and cleaning synthetic work without
a success result. `tests/test_native_codex_smoke.py::test_default_run_rejects_synthetic_abort_before_artifacts`
checks that the private synthetic abort signal is refused in default native
capture mode before artifacts; configured terminal-acknowledgement tests above
remain the real-path control.

`test_invalid_receipt_retains_slot_until_matching_ack` covers malformed/stale
acknowledgements, timestamp overflow and interruption while waiting for a valid
replacement. `test_matching_terminal_ack_does_not_wait_for_repaired_response`
covers the separate response-admission boundary after terminal custody is
established. `test_cancel_publication_failure_retains_custody_until_terminal_ack`
covers failed cancellation publication and repeated parent cancellation.
`test_cyclic_receipt_symlink_retains_custody_until_regular_ack` and
`test_regular_refuses_ancestor_symlink_loop` cover Python 3.12 cyclic-link
resolution failures without treating them as terminal acknowledgements.
`tests/test_native_codex_smoke.py::test_regular_never_reads_symlink_when_link_metadata_fails` covers failed
non-following observations at the leaf and ancestors, refusing before target
bytes are read. Its EIO/EACCES cases inject syscall errors; they do not establish
an ordinary permission arrangement or actual backend behavior.

`test_receipt_readiness_error_retains_custody` covers stat/lstat EACCES/EIO
before receipt consumption, including deadline and repeated parent cancellation.
The separate pre-publication context regressions in `tests/test_codex_smoke.py`
exercise cyclic worktree/packet paths and controlled CLI refusal without output
publication. These driver refusal tests do not establish installed host custody.
`tests/test_codex_smoke.py::test_context_alias_metadata_failure_refused_before_packet_read`
exercises canonical worktree, packet ancestor and packet leaf observation before
reading; `tests/test_codex_smoke.py::test_missing_context_paths_keep_canonical_refusal`
preserves missing-path diagnostics.
`tests/test_native_codex_smoke.py::test_run_parent_alias_refused_before_creating_artifacts`
checks canonical parent refusal before any run directory or artifact is created.
`tests/test_native_codex_smoke.py::test_run_parent_status_error_preserves_errno_before_artifacts`
preserves following status errors before creation, independently of alias checks.
`tests/test_native_codex_smoke.py::test_regular_following_status_failure_preserves_errno`
and `tests/test_codex_smoke.py::test_context_following_status_failure_preserves_errno`
cover the same diagnostic boundary for canonical file and context type checks;
these errors already refused access before the diagnostic correction.

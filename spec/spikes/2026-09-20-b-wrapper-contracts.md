# B wrapper input and exit-token contracts

Source: B candidate
[`6653bdc4d078dc947c9770660fe68c5690662799`](https://github.com/codefoundry-io/triad-codex-dispatch/commit/6653bdc4d078dc947c9770660fe68c5690662799),
based on the offline v2 foundation `ec3d0df`. Shared authoring input is
`055204c`; latest remote main was fetched before implementation and final review
and remained `2eb883fee59e66556ee7c7f87189b38231136622`.
This is implementation evidence, not a release or revision-adoption claim.

## C8: table parity with preserved producers

The shared contract declares 18 table rows. B lacked `admission-refused`,
`vendor-timeout` and `input-delivery-failed`; its mapper returned fallback exit 1
for them. The independent RED observed exactly those three failures. B now maps
them to terminal exit 65 at
[`bin/_common.py:69–91`](https://github.com/codefoundry-io/triad-codex-dispatch/blob/6653bdc4d078dc947c9770660fe68c5690662799/bin/_common.py#L69-L91).

They remain map-only entries on B. No producer, stdin phase, retry or classifier
repair target changed. `permission-unavailable` remains an inert compatibility
alias; AGY `route-mismatch` retains its explicit direct exit. The exact shared
fixture and tests are
[`tests/test_exit_token_contract.py`](https://github.com/codefoundry-io/triad-codex-dispatch/blob/6653bdc4d078dc947c9770660fe68c5690662799/tests/test_exit_token_contract.py).
The vacuous import-time `is not None` assertion was removed. The bounded literal
census is not an exhaustive data-flow proof: one accepted Minor suggests covering
bare local `classification` assignments. The leader checked the current missed
Claude literal, `extraction-error`, and verified it is already registered.

A already has the three map rows at
[`3rd-Agent/wrappers/_common.py:162–183`](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L162-L183).
A should add the shared membership tests while preserving its active producer
states and phase-specific direct exits. B's map-only assertions must not be
copied over A's active producers.

## C28: loader resolution, separate from evidence custody

B's two helpers formerly rejected relative paths. They now use `pathlib` and
one process-cwd snapshot captured by each wrapper after argument parsing. Both
paths resolve independently from that snapshot; the child's cwd never becomes
the prompt-file base. Existing root/type/existence/UTF-8/XOR/empty checks remain.

Source anchors:
[`_common.py:482–515`](https://github.com/codefoundry-io/triad-codex-dispatch/blob/6653bdc4d078dc947c9770660fe68c5690662799/bin/_common.py#L482-L515),
[`claude_wrapper.py:284–292`](https://github.com/codefoundry-io/triad-codex-dispatch/blob/6653bdc4d078dc947c9770660fe68c5690662799/bin/claude_wrapper.py#L284-L292),
[`gemini_wrapper.py:254–262`](https://github.com/codefoundry-io/triad-codex-dispatch/blob/6653bdc4d078dc947c9770660fe68c5690662799/bin/gemini_wrapper.py#L254-L262),
[`antigravity_wrapper.py:434–436`](https://github.com/codefoundry-io/triad-codex-dispatch/blob/6653bdc4d078dc947c9770660fe68c5690662799/bin/antigravity_wrapper.py#L434-L436).
Tests: `tests/test_wrapper_relative_paths.py`; distinct caller/child file
contents, snapshot stability, absolute/direct callers and pre-provider refusals.
The valid RED observed eight behavior failures and 30 passing controls.

A remains unchanged at `92c8afd500499d8736afcc28b39a87a4f87fed50`. Its matching
helpers still refuse relative paths at
[`_common.py:1148–1190`](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L1148-L1190).
The exact A entrypoints, test and documentation follow-up are linked in
[B's maintainer handoff](https://github.com/codefoundry-io/triad-codex-dispatch/blob/6653bdc4d078dc947c9770660fe68c5690662799/docs/reviews/2026-09-20-wrapper-contracts-claude-handoff.md).

C28 remains PARTIAL: its resolved-path summary/audit requirement and C29 exact
investigation evidence depend on D-B2. Current masking and canonical absolute
review-artifact paths are unchanged. D-B1, v2 dispatch activation, native-host
architecture and dormant B hooks are also unchanged.

## Verification and review

- Dedicated fresh Terra/high RED/GREEN at the canonical source: focused suites
  134 and 49 passed; macOS Python 3.12.13 full suite 1,330 passed.
- Ubuntu 24.04.4 / Python 3.12.3: 1,328 passed, two existing case-insensitive
  filesystem tests skipped. Source/root read-only, network disabled. An initial
  task container used noexec temporary storage; a tiny executable reproduced the
  fixture failure, then correcting that option restored the unchanged suite.
- Source skill validation passed. The fixed provider-free lifecycle ran once:
  SUCCESS, exit 0, all 14 internal commands exit 0, ROUND_INTEGRITY_OK, matching
  source hashes and exact owned-fixture cleanup. The original host completion
  event was recovered after executor display omitted metadata; no rerun was used.
- Round `triad-b-wrapper-contracts-r1`: Claude Opus/xhigh, AGY Pro/high,
  AGY Flash/high and fresh Codex Terra/xhigh all SAFE; canonical admission
  ADMITTED_SAFE with matching final fingerprint. One non-blocking test-census
  suggestion retained on unchanged bytes; no open questions or blocking findings.
  This is B's existing development composition, not a change to the public roster.
- Clean-HEAD Git archive at B `6653bdc`: 1,330 tests passed and all 27 packaged
  file hashes matched. Archive SHA-256:
  `3215c7ad81a9fab5c0c37d79ef5f4f41a25199b67b78155268a3571431d8cc69`.

No live Gemini V1–V5, new model entitlement, installation or release is claimed.
The shared schema/prompt bytes and behavioral expected results are unchanged.

## Integration and draft-to-implementation briefing

The owner approved the two implementation PRs for sequential merge. B
[PR 35](https://github.com/codefoundry-io/triad-codex-dispatch/pull/35) merged as
`2f379c7d1e5f51c263a35f2a718213f36f54dbf3`; after retargeting to main,
[PR 36](https://github.com/codefoundry-io/triad-codex-dispatch/pull/36) merged as
`56f0f6657084f81516217ee51698f9b18cfc71dc`. The development checkout and fetched
remote main now identify the latter commit. Its complete Git tree is identical
to reviewed source `6653bdc` (`01daefffd824f3bd37924f077f9360a2bda5fd52`).
The separate protected common checkout and its intentional AGENTS.md edits were
preserved. No tag, installation or release was performed in this integration.

The merge verification reran all 1,330 macOS tests successfully. The three B
contract payloads were also compared directly to shared authoring commit
`055204c`: all original bytes and recorded digests matched. Both plan-level
four-leg admissions above remain tied to their unchanged reviewed bytes.
PR 35's checks passed; PR 36 had no required branch checks or PR check runs after
retargeting. The final merged-main
[CodeQL run 35486551717](https://github.com/codefoundry-io/triad-codex-dispatch/actions/runs/35486551717)
completed successfully for `56f0f6657084f81516217ee51698f9b18cfc71dc`.

No target behavior was changed from the settled shared candidate by these two
PRs. The following distinctions explain what was concretized or staged:

| Topic | Implementation choice and reason | Contract boundary |
|---|---|---|
| Canonical validation | Use maintained `jsonschema` and `referencing`, with exact shared payloads and offline reference resolution; preserve existing Pydantic boundaries. Avoid maintaining a second editable schema or a vendor SDK. | [Foundation plan](https://github.com/codefoundry-io/triad-codex-dispatch/blob/ec3d0df9b134f96bf39bcee11bea695878389146/docs/superpowers/plans/2026-09-20-v2-offline-validation.md), [validator](https://github.com/codefoundry-io/triad-codex-dispatch/blob/ec3d0df9b134f96bf39bcee11bea695878389146/bin/validate_v2.py#L39-L99). This implements the shared candidate, not a new wire format. |
| v2 rollout | First expose an explicit offline validator. Keep current legacy dispatch working until validator, all shaped prompts, render binding and collectors can switch together. | [Shared integration boundary](../decisions/rev-2-implementation-spec.md#verdict-and-legacy-boundary). This is staged implementation, not permission to admit v2 through the old gate. |
| C8 | Add the missing map entries and a contract test; retain each existing producer and phase-specific exit. | The C8 section above distinguishes map parity from future common transport emission. No retry or repair eligibility was expanded. |
| C28 | Resolve both relative arguments with one process-cwd snapshot and the existing validation chain. Complete this independently of unresolved success-evidence custody. | The C28 section above identifies exact source lines. Existing masking remains; C28 is still partial, not silently weakened. |

During earlier shared-schema authoring, terminal-newline rejection and the
requirement for a pinned Google route's own configuration block were corrected
after reproduced failures and full re-review. Those corrections already exist
in the consumed `055204c` contract; they were not host-side reinterpretations.
See [authoring evidence](../decisions/rev-2-implementation-spec.md#authoring-evidence-and-cross-host-handoff).

Remaining work, grouped by functional outcome rather than a completion percentage:

| Outcome | Still needed |
|---|---|
| Named N-leg configuration | Shipped three-family defaults, named override resolution, adapter capability checks and exact invocation display; project-file discovery awaits D-5. |
| Public v2 activation | Integrate the validator, all shaped prompt clauses, render binding, wrapper adapters and collectors together; no legacy conversion. |
| Transport and evidence identity | Emit/admit the common transport object and exclusive evidence locations for each review/leg/family/digest/attempt/route tuple. |
| Retry and re-review | Retain successful siblings only on an unchanged failed-run retry; bind attempts, previous findings/rebuttals and every participating leg. Complete full re-review after any reviewed-basis change. |
| Google review route | Adopt Pro plus verifiable HIGH while preserving authentication and route selection; settle D-B1 before policy composition. |
| Investigation and path evidence | Complete C28 success evidence and the exact authorized C29 trigger, clause-last append and prompt/fetch custody under D-B2; retain raw/custom-schema investigation. |
| Conformance and adoption | Finish case mappings and both-platform checks; separately record unavailable live checks, revision tagging/adoption and the final A implementation handoff. |

The three pending choices are unchanged: [D-B1 policy composition](../decisions/host-b-gemini-policy-composition-proposal.md),
[D-B2 evidence custody](../decisions/host-b-evidence-custody-proposal.md), and
[D-5 project roster location](../decisions/host-b-roster-location-proposal.md).
The owner-approved merge does not select an option in those proposals.
V1–V5 remain NOT RUN. Shared PR 1 remains a candidate review, and A remains
read-only at `92c8afd`; the source-paired handoff above is still its starting point.

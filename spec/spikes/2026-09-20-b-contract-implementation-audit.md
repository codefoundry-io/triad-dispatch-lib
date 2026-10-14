# B contract implementation audit and remaining decisions

> **Historical record; its REVIEW no-web statements are superseded on 2026-10-03.** REVIEW web now follows the owner's
> standing authorization in current [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](../decisions/owner-register.md#D-REVIEW-LEGS-20261003)); the no-web posture applies only to a false
> condition.

## Evidence basis

B source: [`56f0f665`](https://github.com/codefoundry-io/triad-codex-dispatch/tree/56f0f6657084f81516217ee51698f9b18cfc71dc).
A read-only reference: [`92c8afd`](https://github.com/codefoundry-io/triad/tree/92c8afd500499d8736afcc28b39a87a4f87fed50).
Shared authoring basis: `59db77533d39e29b56b94447d28d2dc167b4b468`;
remote main fetched on 2026-09-20 at `2eb883fee59e66556ee7c7f87189b38231136622`.
Four independent fresh native children inspected C1-C10, C11-C20, C21-C30
and the cross-contract runtime consumers. The leader verified findings against
source and existing execution receipts. These audits did not run tests or providers
and are not a formal multi-family admission round.

Status below distinguishes shipped local behavior, missing integration and unrun
evidence. The original table is based on `56f0f665`; the explicit C29 follow-up
below uses source `ce68780e8a29cb7455dbc94e660486fcea8c0679` and its new evidence.
That follow-up is pushed source, not a merge, installed revision or deployment.

## Why C29 was left behind

The previous tracking grouped the authorized web trigger and clause insertion
with D-B2's unresolved exact-evidence custody question. Only custody depends on
that decision. The grouped dependency incorrectly deferred settled repair work.
Separately, the schema foundation deliberately supplied offline validation;
its completion did not wire the public-v2 dispatch lifecycle. Neither a merged
slice nor passing existing tests establishes whole-contract completion.

## Case-by-case B status

Paths and lines refer to the B source above unless prefixed A.

| Case | Status and remaining obligation | Implementation / test evidence |
|---|---|---|
| C1 | Implemented local terminal reconciliation; arbitrary external-signal behavior is not claimed by these receipts. | `bin/_common.py:1427-1507`; `tests/test_provider_wrappers.py:399,443,650`; `tests/test_terminal_transport.py:87` |
| C2 | Implemented partial-start cleanup and interruption propagation. | `bin/_common.py:1411-1468`; `tests/test_terminal_transport.py:161,200` |
| C3 | Implemented fresh-file age floor under count/byte overflow. | `bin/_common.py:2856-2903`; `tests/test_log_cleanup.py:898,920` |
| C4 | Implemented allocation/export-bound owned-copy cleanup; preserve original/unproven content. | `bin/review_round.py:1045-1059,1293-1349`; `tests/test_review_cleanup_custody.py:35,81` |
| C5 | Implemented allocation-bound resumable deletion. | `bin/review_round.py:1279-1290`; `tests/test_review_cleanup_custody.py:154` |
| C6 | Implemented post-transcript guard-release failure handling with transcript retained. | `bin/antigravity_wrapper.py:667-699`; `tests/test_antigravity_stream_json.py:1799` |
| C7 | Implemented verified export prerequisite and absent cleanup no-op. | `bin/review_round.py:1219-1274,1305-1309`; `tests/test_review_cleanup_custody.py:49,154` |
| C8 | Implemented shared exit-map parity and explicit exceptions. | `bin/_common.py:69-91`; `tests/test_exit_token_contract.py:20-89` |
| C9 | Missing common transport producer on actual native/CLI dispatch. A schema file alone is not an emitted receipt. | `contracts/receipt-fields.json`; private-only fields in `bin/_common.py:300-312` |
| C10 | Missing common transport/attempt integration into audit, failure IPC and admission. Existing host records remain. | `bin/_common.py:1966-2065,2702-2790`; `tests/test_claude_receipt.py` covers legacy records |
| C11 | Implemented injection scrubbing and route-specific formal removal sets; no OAuth-principal claim. | `bin/_common.py:1202-1217,1336-1345`; `bin/gemini_wrapper.py:43-53`; `tests/test_provider_wrappers.py:1770-1843` |
| C12 | Missing shipped default roster, merge-by-name resolver, display and runtime consumer. D-5 blocks automatic discovery only. | `contracts/README.md:16-19`; `bin/validate_v2.py:22` loads schema only |
| C13 | Partial: offline canonical verdict handling exists; public-v2 verdict selection/admission remains legacy. | `tests/test_validate_v2.py:83-89`; `bin/review_round.py:2061-2074` |
| C14 | Partial: original-JSON duplicate rejection and six-field offline validation exist; operational producer/collector still binds three fields. | `bin/validate_v2.py:30-36,74-91`; `bin/verdict_schema.py:214-230` |
| C15 | Partial: AGY and renderer REVIEW no-web exists; Gemini still permits web at 999. Shared-file composition waits D-B1. V1-V5 remain NOT RUN. | `tests/test_review_no_web.py:47-115`; `bin/policies/gemini-formal-readonly.toml:5-17`; `bin/gemini_wrapper.py:114-121` |
| C16 | Partial: version/help/policy preflight exists; actual subscription identity and effective runtime policy are unverified. | `bin/gemini_wrapper.py:151-190`; `tests/test_gemini_version_floor.py:42-81` |
| C17 | Implemented formal environment route scrubbing; does not attest the signed-in principal. | `bin/gemini_wrapper.py:43-53,151-169,402-413`; `tests/test_provider_wrappers.py:1774-1843` |
| C18 | Partial existing AGY Pro/high; missing roster-driven route validation and Gemini Pro/verifiable HIGH. Gemini remains Auto. | `bin/antigravity_wrapper.py:35-36`; `bin/gemini_wrapper.py:389-397`; `bin/review_round.py:249-255` |
| C19 | Missing public-v2 same-basis failed-entry retry and attempt-2 custody. Preserve the separate existing workspace legacy full-round gate. | `skills/triad-cross-family-review/references/convergence.md:62-87`; offline attempt field is not a retry consumer |
| C20 | Partial: changed conditions bind a new digest/full round; missing required fenced prior-findings/rebuttal delivery to every participating entry. | `bin/review_round.py:1919-1924,2009-2025,2195-2248`; `tests/test_review_conditions.py` |
| C21 | Partial fixed-family agreement; missing arbitrary participating/informational-leg blocker accounting. | `skills/triad-cross-family-review/SKILL.md:100-108` |
| C22 | Partial host-local model/effort arguments; missing resolved roster-to-argv/native-call matrix and unsupported-adapter refusal. | `skills/triad-cross-family-review/references/reviewer-routing.md:9-24` |
| C23 | Partial paired Pro/Flash custody; missing general leg-name/attempt/route identity and per-entry read-evidence binding. | `tests/test_four_leg_custody.py:41-56`; legacy result bindings above |
| C24 | Current committed tree has separate macOS/Ubuntu regression evidence; not all-provider/install conformance. | `56f0f665` and reviewed `6653bdc` both tree `01daefffd824f3bd37924f077f9360a2bda5fd52`; [completed slice](2026-09-20-b-wrapper-contracts.md) |
| C25 | Partial raw custom prompt/schema behavior; explicit web trigger is current C29 repair, authorized additional-read-root propagation still needs a route matrix. | `tests/test_provider_wrappers.py` raw routes; no extra-root dispatch contract is proved by changing cwd alone |
| C26 | Implemented local no-follow/link-text review evidence; prompt-controlled target boundary, not OS confinement. | `bin/review_round.py:1549-1578,2214-2219`; `tests/test_review_link_evidence.py:16-70` |
| C27 | Implemented local route/binary/version binding and no-fallback; authenticated runtime identity is a separate observation. | `bin/review_round.py:1949`; `bin/gemini_wrapper.py:142-205`; `tests/test_gemini_version_floor.py:42-114` |
| C28 | Partial: relative inputs resolve against process-entry cwd and keep existing validation. Complete success path-summary/audit semantics wait D-B2. | `bin/_common.py:482-515`; `tests/test_wrapper_relative_paths.py:74-154` |
| C29 | Partial at `ce68780`: AGY trigger/clause-last implemented and reviewed. Live calls increased, but provider page bodies can be truncated. Gemini integration remains. Owner rejects a new permanent evidence store; align common wording rather than implement that superseded proposal. | [bounded repair and live evidence](2026-09-20-b-agy-web-evidence.md); B `bin/antigravity_wrapper.py:53-60,419-423,459-473`; `tests/test_agy_web_evidence.py` |
| C30 | Offline candidate schema validation is implemented and tested; runtime roster/render/receipt/collector adoption is missing. | `bin/validate_v2.py:74-96`; `tests/test_validate_v2.py`; `contracts/README.md:17-23` |

## Leader adjudication of audit findings

- Rejected the claim that B has no normal-exit descendant regression:
  `tests/test_provider_wrappers.py:443` exercises both held and closed pipes.
  The interruption branch also has a `KeyboardInterrupt` test at `:650`.
  This is not evidence for arbitrary external SIGTERM/SIGHUP handling.
- Rejected the claim that the current committed B tree lacks Ubuntu evidence:
  the merged and reviewed commits have the same Git tree. Existing macOS results
  are 1,330 passed; Ubuntu 24.04 results are 1,328 passed and two documented
  case-insensitive-filesystem skips. New uncommitted C29 tests are not included.
- Accepted the runtime-integration gap. Passing offline schema tests cannot
  establish named-roster dispatch, per-attempt receipts or all-leg admission.
- Accepted stale shared descriptions of B cleanup/normal-exit reaping and stale
  grouping of all C29 work behind D-B2; update status without weakening cases.

## Owner decisions and remaining implementation

The [verbatim owner answers and applications](../decisions/2026-09-20-owner-follow-up.md)
supersede the earlier open-choice wording below and in historical audit snapshots:

1. **D-B1:** keep host-specific policies separate where usage differs; preserve
   common no-web requirements and B's existing controls. Exact composition and
   digest semantics still need cross-host contract review and implementation.
2. **D-B2:** no new permanent web-evidence store. Retain masking and failure logs;
   use bounded diagnostic/test capture. Align the common custody wording before
   claiming conformance; do not treat a log subsystem as an implementation gap.
3. **D-5:** B uses `.agents/triad-review-legs.json`. Discovery/resolution remains
   unimplemented, but no further owner location decision is needed.

Do not reask settled all-leg agreement, N-leg support, Pro/HIGH intent, full
re-review after code changes, selected investigation behavior or canonical v2 fields.
No answer is inferred from a recommendation or elapsed time.

## Claude-host follow-up

Keep A unchanged until the lead-host handoff. A already has the C29 append at
`3rd-Agent/wrappers/antigravity_wrapper.py:1381-1393`. Its transport reader paths
at `_common.py:1954-1965,2234-2308`, cap pruning at `:3319-3397`, and cleanup at
`.claude/skills/triad-cross-family-review/lib/review_scratch.py:720-731,1069-1080`
need A-native assessment against C1-C7. Do not assume different A guard architecture
is itself defective. Both hosts still need the shared v2 roster, transport and
collector integration. Review this exact shared audit commit and return source-
backed corrections; B tests or deployment never establish A conformance.

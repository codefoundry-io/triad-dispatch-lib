# DL-113 — Current-source evidence and admission boundary questions

Assessment date: 2026-10-10. Shared main freshly fetched at
3afc4d7e931e55d601dd74877bdbe65e610a8e59; PR13 basis389071a.
B632f426 plus its preserved candidate; read-only A
a5456b1324670117c445fef96d5b61f49c8955b6 plus concurrent work.
This records evidence and questions under R-AUTHORING-SYNC/R-DECISION-ORDER;
it does not revise R-CONTAIN, authorize a wider audit, or claim completion.

## Confirmed purpose and current behavior

The owner's D-OWNER-ANSWERS-20261008B item7 already retains same-run recovery:
an errored finish followed by a successful finish must not discard the final
review merely because the terminal status remains ERROR. DL-113 is real pending
B implementation, not a speculative new error class.

A's `docs/reviews/2026-09-27-simple-review-spike.md` item4 and retained
`main/legs/google/stderr.attempt1.log` record terminal ERROR/raw exit0, failed
finish submission and a recovered must-fix answer. The named original run-log
`20260927T121326Z-97952-3ad420dc.json` is absent at its recorded local path today.
The recovered answer remains; a full same-run raw-stream replay was NOT RUN.

The separate real capture
`docs/spikes/2026-08-22-agy-permission-ladder/out/adddir.stream.jsonl`
directly confirms successful view_file as tool/DONE with tool_info.output,
successful submission as finish/DONE without tool_name/tool_info, and a terminal
result with status, response and structured_output. It is a successful run,
not evidence that the September failed/resubmitted run had every same field.

A's `3rd-Agent/wrappers/antigravity_wrapper.py::_census/admit` implements the
ordering check. `tests/unit/wrappers/t15-agy-driver-decision.sh` axes30-37
cover recovery, allowed read errors, missing/reversed success, executed off-list
tools, other errors and invalid success shapes. These test sources were read;
A tests were NOT RUN. Their constructed inputs are not new vendor captures.

B's `bin/antigravity_wrapper.py::_interpret_run` returns before verdict
validation on nonzero vendor exit and rejects ERROR except its existing
post-completion permission-denial case. A provider-free constructed contract
probe confirms ordinary SUCCESS -> ok/0, ERROR with failed-then-successful finish
-> vendor-error/65 with answer withheld, no later success -> vendor-error/65,
and raw exit1 with the resubmission -> unknown/1 with answer withheld.
Source HEAD/status/two source hashes were unchanged and the exact temporary
fixture was removed. Evidence in B:
`_runs/spec-plan-20261010/u3/resubmit-characterization.json`.
This is characterization, not fresh dedicated RED/GREEN or live AGY proof.

## Initial questions sent to A (resolved below)

1. R-CONTAIN says the resubmission judgement uses structured fields, never
   message text. A's off-list denied-versus-executed distinction additionally
   calls `_common._agy_step_denied`, which reads tool_info.error.message.
   Captured Aprime/hookdeny permission failures both have generic type
   TOOL_ERROR; no distinct structured denial code is established by them.
   Please confirm whether "never message text" governs only identification
   and ordering of finish recovery, while the existing measured denial
   predicate remains a separate exception. If a structured denial discriminator
   exists in the current AGY route, supply the exact capture and field instead.
   Do not invent one or silently copy an error-message catalog into B.
2. The measured September failure had raw exit0. R-CLASSIFY labels A's broader
   nonzero-exit/errored-read admission as an A fact; DL-113's shared wording names
   terminal ERROR. Please confirm whether B should preserve its existing nonzero
   classifier boundary for this bounded change, or identify the existing common
   rule and evidence that require bypassing it. No new raw-exit policy is implied.
3. If the September same-run capture is still retained elsewhere, provide its
   path/revision or a sanitized structured excerpt and hash. No new paid failure
   generation is requested. Its absence is an evidence limit, not a new feature.

The first two questions concern the scope of the existing contract, not whether
to reapprove the owner's recovery decision. If a substantive new design choice
survives source/spec clarification, B will ask the owner before implementing it.

## Resolution — PR13 reply6092107935

A agrees that structured-only means identifying and ordering finish recovery;
the separate permission-denial predicate reads the measured message head. B
rechecked `_common.py:346-396` at a5456b13: state ERROR, first non-empty stripped
lowercased message line, the measured direct prefixes or permission-head/tail
combination. Generic TOOL_ERROR is not sufficient; DONE and mid-message quotes
do not count. R-CONTAIN and C23 now make the distinction explicit.

A confirms no shared rule requires B to override its nonzero classifier path.
B implements this recovery at raw exit0, leaving A's broader nonzero/errored-read
admission as a host fact. No owner design question remains on these two points.

A confirms the September raw log expired and is no longer retained. The stderr
and recovered answer are the evidence of record; no fresh paid failure generation
is needed. Retain this limit instead of reopening the capture search.

Reply: https://github.com/codefoundry-io/triad-dispatch-spec/pull/13#issuecomment-6092107935.
The two boundaries are resolved; B implementation and dedicated verification are
still pending. Finish the independent U3b turn-timeout unit's review before U3a.

## B implementation boundary and verification plan

Keep the correction at ERROR-result admission, using the existing stream and
final answer/schema/binding path. No routine successful-run tool/read audit,
path allowlist, per-file leader inspection, native-leg change, AGY settings
mutation, new error token or Claude agent-definition work. Existing auth,
timeout, transport, route and schema/binding checks remain effective.

Resolve the above boundaries in the normative R-CONTAIN/R-CLASSIFY text only
where needed, and add explicit resubmission axes to existing C23 before code.
C23 currently describes cross-leg binding but does not spell out DL-113's
success/negative examples. Do not mint a duplicate case or weaken that binding.

Then fresh dedicated RED/GREEN should exercise later valid finish, reversed or
missing finish, invalid finish shape, read-blind recovery, other execution/error,
web-profile distinctions, auth/transport priority and retained schema/binding
validation. Keep ordinary SUCCESS and existing post-completion denial controls.
Host source tests, regression and the required independent review precede any
completion claim. A owns its implementation; B changes only its own host.


## B candidate implementation and verification

B632f426 plus its preserved candidate implements the resolved DL-113 boundary.
bin/antigravity_wrapper.py adds an ERROR-only recovery predicate and the measured
denial-head helper; main forwards its already bound web flag. Existing final
structured_output validation, original JSON checks, model/review binding,
auth/host-timeout/transport priority and nonzero classification remain. No normal
SUCCESS census, per-file read audit, new retry or A's broader admission port.
Production delta75added/1removed; tests194added; EN/KO docs15added.

Fresh dedicated RED12failed/444passed/4skipped. First GREEN456passed/4skipped/2failed
found incorrect test expectations for schema-fail (B's established exit is66,
not4); those expectations alone were corrected. Final fresh GREEN458affected
and2213full tests passed/4skipped, four source validators passed. Five measured
hashes, HEAD/status and ten existing logs unchanged; exact fixture removed.
Platform macOS26.6.2 arm64/Python3.12.13/pytest9.0.3. Ubuntu NOT RUN; constructed
contract cases, not a fresh AGY failure capture. Main's bound web-profile
positive/negative behavior is covered by the real wrapper path with fake provider.

Independent review triad-agy-finish-resubmission-20261010-r1: all selected legs
SAFE (Claude opus/xhigh, AGY Pro/high, AGY Flash/high, fresh Codex Astra/high),
ALL_SELECTED_APPROVED/ROUND_INTEGRITY_OK. Digest
350ee9e1da26abf02c9ce0d5d56bfe6667eac0e8c572e92b2d36857d881d8ee3;
fingerprint1698369b4d63888828a330d01fb4a2e6585f819d97062f51245875b7be7fe4ec.
Custody exported, exact stage/cwd removed. Current A1ea9cb3e source was read;
A's native leg, implementation and tests remain A-owned. No installation,
merge, release, full C23 conformance or whole-revision adoption is claimed.

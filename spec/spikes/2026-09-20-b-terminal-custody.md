# B terminal custody and AGY read compatibility

Status: P1 implemented and reviewed at B `e29d820fb4fb35b64fc9e955aee5357377f23418`;
[integration PR 27](https://github.com/codefoundry-io/triad-codex-dispatch/pull/27).
This record does not adopt a
revision, publish the shared repository, close the original review, or prove
cross-host conformance. A remains unchanged until the owner's B-first handoff.

## Basis and existing requirements

- Shared remote main verified as `2eb883fee59e66556ee7c7f87189b38231136622`.
- Shared local authoring/audit: `d7ef76304b2cfcdb4bdb9a0f7991e0cd77b19982`.
- B starting HEAD: `ba6344be910307d9e05bad1396663f6227064467`.
- A inspected HEAD: `92c8afd500499d8736afcc28b39a87a4f87fed50`.
- Existing cases C1/C2/C6 and `reference/review-rules.md#R-TERMINAL`; no
  new contract, result vocabulary, retry policy, provider route or schema.
- Original diagnosis: `host-b-start-audit-r1`, digest
  `5872fdd162e44ae04aef5c8785427a7513fcd6e74988abc51eecb2aff7be6572`.

## Observation and causal chain

B's `_common._drain` logged a decoder failure without returning it to the
collector. `_run_once` selected success from the direct child's zero exit and
did not reconcile surviving descendants after normal exit. Thread starts also
preceded its exception-cleanup boundary. The adapters could therefore admit
intact terminal stdout despite corrupt stderr; a thread-start error could leave
the owned child alive. AGY's settings-exit handler separately returned before
preserving the raw completed provider result.

A fresh dedicated `triad-skill-executor`, requested Terra/high with no inherited
turns, ran the canonical B source and synthetic fixtures: **13 failed, 7 passed,
143 deselected in 12.11 seconds**. All 13 failures reproduced these implementation
paths. Its pre/post source/test fingerprint was identical:
`eead604d635b9a29e2b3ecd833c9c19af4a76be38bb49d260e92506863a82156`.
Runtime model metadata was UNEXPOSED. The executor's independent receipt-based
fixture cleanup found no remaining task-owned process.

Evidence directory on the owner workstation:
`/Users/chaniri/codex_workspace/_runs/infra/20260920-triad-p1/red-executor/`.
This is local evidence, not a publicly accessible attachment.

## B correction and preserved functionality

The bounded implementation keeps the current process-group helper and adapters:
record reader completion/error, include thread startup in cleanup, reconcile the
saved owned group after normal exit, reject local transport failure before
extraction/retry, and persist captured AGY output after a settings-release error.
The original timeout and genuine nonzero vendor-error priorities remain, including
existing capacity retry for genuine vendor failures. B uses strict UTF-8 output
decoding and content-free local error descriptions.

No process supervisor, new registry, public schema, timeout knob, authentication
change, Codex subprocess, permission bypass, or dormant hook is introduced.
Final dedicated GREEN passed 189 focused tests, 1042 macOS tests, the skill
validator and the provider-free lifecycle verifier. Ubuntu 24.04.4 under a
nonroot Python 3.12 container passed 1040 tests with two case-insensitive-filesystem
tests skipped. These are automated platform checks, not authenticated vendor
conformance or V1-V5 evidence.

## A counterpart and later handoff

All line references below use A `92c8afd` and `3rd-Agent/wrappers/`.

| Case | A source evidence | Actual difference and later action |
|---|---|---|
| C1 | `_common.py:1954-1970`, `2234-2277`; AGY `antigravity_wrapper.py:828-856`, `958-968` | Same missing reader outcome; complete stdout can hide a decoder error. A already pins UTF-8. Port the behavior and regression, preserving A's own adapter/exit conventions. |
| C2 | `_common.py:2150-2204`, `2211` | Saved PGID and abnormal cleanup exist, but workers start before protected wait. Extend the existing exception boundary; retain saved-group ownership and exact interrupt propagation. |
| C6 | `antigravity_wrapper.py:1241-1274`, `1480`, `1524` | A already preserves captured stream/read audit and reaches persistence after release failure. It nevertheless replaces an existing timeout/vendor failure with `config-conflict` at 1261-1271. Add both successful-call and combined-failure regressions; preserve the earlier failure while recording the release failure. Do not copy B's structure unnecessarily. |

Claude maintainer relay: inspect this record and B's final commit/test receipts
when B completes; reproduce C1/C2 against A, apply the smallest A-local fix,
retain C6's existing path and test it. Do not change A in parallel with B.

Independent P1 source review found the combined failure-priority problem in B's
first correction. Fresh dedicated RED observed **2 failed, 1 passed** in 0.14s
for timeout/nonzero vendor failure plus settings-release failure. B's next
correction interprets the captured result, preserves an existing failure, adds a
content-free secondary release diagnostic, and only converts success to
`config-conflict`. The final GREEN above includes that correction.

The first complete implementation round `triad-b-p1-r1` admitted NOT-SAFE with
matching final integrity. Google Pro, Google Flash and fresh Codex returned SAFE;
Claude identified a reproduced omission of the secondary reader diagnostic when
the provider had already failed. The bounded correction keeps failure and retry
precedence and emits the existing content-free stream/class diagnostic on every
outcome. A still logs in `_drain` at `_common.py:1969-1970`; this particular
regression was B-only, and A's later outcome-based implementation must retain
the diagnostic. Two Minor observations require no added runtime mechanism:
same-UID permission failure was not shown reachable, and group signaling is not
proof that orphan zombies have disappeared. A fresh complete round is required;
none of the three SAFE results is carried forward.

The correction's fresh dedicated RED observed 3 failures with the primary
failure assertions already passing. Fresh GREEN again passed 189 focused and
1042 macOS tests, the validator and complete provider-free lifecycle. Ubuntu
again passed 1040 tests with two filesystem skips. Full round `triad-b-p1-r2`
then admitted SAFE: Claude, Google Pro, Google Flash and fresh Codex all SAFE,
digest `040dc2790f904505306a0bea24a03a98c89854917161bcb46da64f450c0c8136`,
matching final fingerprint
`e861d3fff0075898809b5ce77e53ce10650ff83ff5984aad6e9bf119e893f0de`.
One Google Minor about diagnostic precedence when read and close both fail is
retained without a source change; false success remains prevented. All exact
reviewed files remained byte-identical when committed. Only the out-of-scope
narrative plan completion record changed after admission.

Local full-round evidence: `_runs/reviews/triad-b-p1-r1/` under the workspace root,
including all four results, the canonical admission ledger, integrity receipt,
leader adjudication, verified custody export and exact cleanup receipt.

## AGY 1.2.7 compatibility spike (separate from P1 fixes)

Installed version and official release notes identify AGY 1.2.7. Official
[headless permissions](https://www.antigravity.google/docs/cli/headless/) and
[execution modes](https://www.antigravity.google/docs/cli/modes/) do not establish
read-only enforcement from Plan Mode plus sandbox alone. See the
[official releases](https://github.com/google-antigravity/antigravity-cli/releases).

Two direct, bounded calls used `--mode plan --sandbox`,
`--model gemini-3.1-pro-high --effort high --output-format stream-json`,
`--print-timeout 120s`, and no `--dangerously-skip-permissions`. They did not use
B's settings lease, create a project, or activate a hook.

1. Relative-path prompt: exit 0, terminal SUCCESS, but **no successful read**.
   The tool rejected a relative path; the model guessed nonexistent paths and
   ultimately requested an absolute path. This is an inadequate probe prompt,
   not proof of permission rejection or read compatibility. Do not treat process
   success as task success.
2. Exact absolute-path prompt: one `view_file` DONE for the exact owned fixture;
   exit 0, terminal SUCCESS, expected fixture marker in the response, reported
   duration 11.352054 seconds. No other tool call appeared. The fixture remained
   unchanged. This proves this specific no-bypass file-read invocation worked;
   it does **not** prove REVIEW web denial, general containment, a B wrapper
   result, or formal admission.

Local raw evidence: `_runs/infra/20260920-triad-p1/agy-read-probe/` under the
workspace root. Provider logs are not included in external review packets.

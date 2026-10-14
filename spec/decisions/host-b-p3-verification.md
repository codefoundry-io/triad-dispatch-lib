# Codex-host B P3 verification and publication record

This is the current execution record for the B P3 candidate. It supersedes
completion labels in earlier restart snapshots and preserved release audits.
The separate implementation PRD describes functionality and interfaces.

## Source basis

| Surface | Recorded basis |
|---|---|
| B development branch | `codex/agy-web-evidence`, published commit `add5805d8dec70f5e133164c49bc0fe3bff75095` (review baseline `3d62b7cc370d2c72fc439a431d5f78ab76875b98`) |
| B main | `56f0f6657084f81516217ee51698f9b18cfc71dc` |
| A inspected read-only | `92c8afd500499d8736afcc28b39a87a4f87fed50` |
| Shared main fetched before final review | `2eb883fee59e66556ee7c7f87189b38231136622` |
| Shared authoring baseline | `aef3adee863fd90fdfab60ae2253717cf1b4d303` |
| Payload pins | Schema `055204c83e57bf87eeac5b2422f2b17340f7c53b`; review prompts `6bef14c0c42a13678594e8f2f039d1793b7cb127` |

## Internal completion checklist

- [x] Verify prior saved state: all 243 recorded files matched their saved
  hashes and modes before continuation. This proves disk state, not an editor's
  unsaved buffers. Preserve all intentional and unrelated changes.
- [x] Connect opt-in v2 roster, capability-checked native/CLI invocation,
  producer/renderer/validator, immutable entry/attempt evidence, all-entry
  collection, diagnosed failed-entry retry and changed-basis full review.
- [x] Correct F1 route delivery, F2 optional adapter selection/refusal and F3
  Gemini version provenance. Dedicated RED: ten failures and five controls;
  actual process/wrapper/run-log/collector regressions cover the missing paths.
- [x] Related-boundary leader verification: 96 passed.
- [x] Verify the final reserved-output input collision and malformed request
  type refusals, including no partial custody writes and same-attempt recovery.
- [x] Clean-input dedicated behavior verification: 27 focused / 1631 full macOS
  passed, validator and lifecycle exit 0, unchanged source and exact cleanup.
- [x] Independent Ubuntu 24.04: 1629 passed, 2 existing filesystem skips,
  exit 0; read-only source, network disabled, uid 65534, unchanged hashes and
  automatic container removal.
- [x] Reconcile C1–C30 tests, unit mappings and descriptive host snapshots;
  existing shared schema/policy checks: 80 passed. Normative case input/expected
  fields, schema, policy and prompt payloads are unchanged.
- [x] Independently inspect the PRD against B and A source; correct A function
  anchors and document exact default/refusal, delivery and version boundaries.
- [x] Complete `triad-b-transport-p3-r3`: four SAFE results, `ADMITTED_SAFE`, matching final integrity and exact export/cleanup.
- [x] Commit and publish the exact reviewed source `add5805d8dec70f5e133164c49bc0fe3bff75095`; clean archive: 1631 tests and 45 matching source/archive hashes.
- [x] Finalize the source-referenced [Claude implementation PRD](claude-host-v2-implementation-prd.md) and publication record. The PR 1 handoff comment identifies this document's published shared commit.

## Verification evidence

Current input-refusal verification is in `p3-input-refusals-red/` (12 intended
failures), `p3-input-refusals-leader/` (56 passed), `p3-input-refusals-green/`
(27 focused / 1631 full macOS, skill validator and lifecycle passed), and
`ubuntu-p3-input-refusals/` (1629 passed, 2 existing filesystem skips).
Both complete suites recorded terminal exit 0, unchanged source and exact
fixture/container cleanup. The subsequent paragraphs preserve earlier evidence.

Durable local evidence is under
`/Users/chaniri/codex_workspace/_runs/infra/20260920-transport-contract/`.
`p3-findings-red-r2/` records the dedicated RED. `p3-findings-leader-green-r2/`
records the 96 related tests. `ubuntu-p3-findings-r2/` records Ubuntu execution.
The `p3-findings-final-green-r2/` manifest passed 15 focused and 1619 full macOS
tests, validator and lifecycle, but is regression evidence only: its initial
task contained prior repair history. Clean-input certification uses the distinct
`p3-clean-green/` manifest, which passed with terminal exit 0 and source unchanged.
No source changed to address this instruction error.

The earlier `triad-b-transport-p3-r1` round is FAILED, with all started CLI
results retained, matching integrity and exact export/cleanup. Its missing
native start and reproduced findings grant no admission credit to a new round.

`triad-b-transport-p3-r2` subsequently returned four SAFE results, matching
integrity and `ADMITTED_SAFE`; its exact temporary roots were exported/cleaned.
The leader accepted two non-blocking input-handling findings for bounded
correction and declined two future-only changes after source inspection.
Changed bytes require a new full round; r2 grants no admission credit to them.

## Retained non-blocking review observations

Claude's r3 SAFE result includes two Minor suggestions. They remain visible in
the original result and leader adjudication; neither is represented as fixed.

- Generated B wrapper argv uses PATH-resolved `python3`, while Google preflight
  uses the creation interpreter. The documented procedure requires the same
  trusted Python runtime and dependencies. A current login-shell check confirms
  both resolve to Python 3.12.13; changed environments may refuse before a provider
  starts and require explicit proven-start-failure custody. Interpreter pinning
  remains a non-blocking portability improvement, not a claim about arbitrary
  host environments.
- The optional AGY `project` branch has no producer in the current v2 roster or
  adapters. It is unreachable through supported calls. Project behavior remains
  in existing legacy/raw routes; removal is optional dead-code cleanup and no
  new v2 project support is implied.

## Final source and distribution evidence

| Evidence | Result |
|---|---|
| Published reviewed source | [add5805d8dec70f5e133164c49bc0fe3bff75095](https://github.com/codefoundry-io/triad-codex-dispatch/commit/add5805d8dec70f5e133164c49bc0fe3bff75095); clean worktree, reviewed bytes equal committed bytes, remote feature SHA equal |
| Formal round | `triad-b-transport-p3-r3`; Claude Opus/xhigh, AGY Pro/high, AGY Flash/high, fresh native Terra/xhigh all SAFE |
| Review digest | `50a20583aabafa6fb0be7c2de17d3a37f462aafd2c149212043d7ae45b2e44b6` |
| Integrity and cleanup | `ROUND_INTEGRITY_OK`; unchanged fingerprint; canonical ledger `ADMITTED_SAFE`; exact owned staging/custody exported then removed |
| Clean committed archive | 1631 passed; 45 source/archive hash comparisons match |
| Archive SHA-256 | `795233770289321000d5c65a9aa4e7cf5e80ffe83112ed2e0dc7d9ade6f0fa04` |
| Shared checks | 80 existing schema/policy tests pass; all 30 case IDs resolve to B tests, with normative case inputs/expected and contract/prompt payloads unchanged |

The complete local ledger, original reviewer results, adjudication, integrity,
cleanup and commit receipt are retained at
`/Users/chaniri/codex_workspace/_runs/reviews/triad-b-transport-p3-r3/`.
The archive verification report is `/Users/chaniri/codex_workspace/workspace/triad-codex-dispatch-reliability/_runs/distribution/p3-r3-add5805/verification.json`.
The [source PR](https://github.com/codefoundry-io/triad-codex-dispatch/pull/37)
and [shared PR](https://github.com/codefoundry-io/triad-dispatch-spec/pull/1)
remain publication candidates. The final PRD links exact A/B source revisions;
its containing shared commit is identified by the PR handoff comment.

## External verification and operation boundaries

- B1–B3 and A V1–V5 authenticated policy checks are **NOT RUN**. Policy byte
  equality, test stand-ins and CLI capability probes do not establish merged
  effective policy, account entitlement or runtime service behavior.
- AGY 1.2.7 legacy-search compatibility remains unverified because the requested
  grep was not executed. The tool inventory and model prose do not prove a
  functional tool failure.
- `KI-AGY-URL-BODY-PREFIX` is the accepted non-fatal incomplete-source-evidence
  issue. No vendor fix, automatic retry, workaround or permanent web archive
  is claimed.
- Native runtime model/effort is `UNEXPOSED` unless supplied by the actual host.
  Requested and preflight values stay separate from runtime observations.
- Feature publication, formal admission, clean distribution, shared revision
  adoption, merge, installation, fresh-process exposure and release are distinct.
  Neither an `AGREED` v2 collection nor a formal SAFE review authorizes merge.
  This task makes no A implementation changes.

# Minimal adoption follow-ups: design review evidence

Date: 2026-10-16. The [candidate design](../superpowers/specs/2026-10-16-minimal-adoption-followups-design.md)
completed formal plan review. This establishes no library or host implementation,
GitHub disposition, merge, release or installation. Issue #5 and the separate
release-update-PR work remain held with existing edits preserved.

Product baseline: `dac1af62297402a0078a616e8e194c7a69cafe18`. Review checkout:
`codex/release-update-prs`, HEAD `802b9bf3078cd8447f3c519efbb54147d885a5db`, with
the candidate document and status edits explicitly included as working-tree data.
The final reviewed design SHA-256 is
`e2a8933fe3b74cf1411b59c98726bf52b80bcd81710f4d519a52e38cd396a527`.
This operational record and the final status update were written after closure;
they do not change the reviewed candidate's bytes or claim review of future code.

## Review result

Both rounds used the project public v2 profile, three required reviewers and
a separate nonvoting Astra comparison. Each had 2400 seconds and authorized
current official web research. Review inputs were frozen packets; native read
containment was prompt-controlled. Requested settings are shown below, not
independently established backend identities. Native runtime model/effort remain
`UNEXPOSED`; CLI selection/capability observations are retained separately.

| R2 reviewer | Requested setting | Result | Parent-observed elapsed |
| --- | --- | --- | --- |
| Claude | Opus 5.5 / xhigh | SAFE TO MERGE; two Minor checklist details | 11m 07s |
| Codex | Sol 6.1 / xhigh | SAFE TO MERGE; no findings | 5m 57s |
| Google | Argon / high | SAFE TO MERGE; no findings | 5m 51s |
| Comparison | Astra / high | No actionable finding; no vote | 2m 53s |

R2 `20261016-lib-minimal-plan-r2-e3b5e7`, digest
`28bce2bec9139894a24622896fcbc1b6d03684f9cf0ec961e80a79837db7e7e9`, ended
`AGREED` with no missing results, selection deviations or open questions.
All producers terminated before final collection, export and exact temporary-root
cleanup. The collector admitted current-round bindings and verified source integrity.
Preflight observed Claude CLI 2.1.299 and AGY 1.3.6; R1 observed AGY 1.3.5.
This task performed no CLI upgrade. Top-level retained CLI receipts expose no
usage totals or runtime model/effort, and native receipts provide no usage total;
this is not a cost comparison or calibrated model ranking.

## R1 corrections and checked claims

R1 `20261016-lib-minimal-plan-r1-bd2f8c`, digest
`7d8e3622f16f9fc4c6f5043b0c2e06f3d3cb73c8f309bf591c1822a95508093a`, also
ended `AGREED`. Opus reported six Minor findings and Argon one overlapping Minor;
Sol and Astra reported no actionable finding. Those votes did not transfer to R2.

| Finding | Verified disposition in the corrected candidate |
| --- | --- |
| Packaging inventory and counts | Named package-data globs, wheel inventory, generation/export checks and current documentation counts. Explicitly described moving only the transport schema into the runtime wheel. |
| Issue #9 residual | Acknowledged the requested unknown-member need and proposed declining that part for this slice, retaining the host deviation and partial issue status. No permanent disclosure ban. |
| Roster path root | Distinguished the override schema root from the defaults/resolved evaluation root and omitted reference/conditional hops. |
| B removal flag | The design's `--remove` was correct. Bound B `scripts/bootstrap.sh:64-75` at `c81c02984825af7dd1ec69a14af83f0ff18d0551` confirms it; PR #11's `--uninstall` label needs correction. |
| Argon/default policy | R-ROSTER/R-MODEL already allow explicit owner pins. B's shipped default remains `gemini-3.1-pro-high`; the project override does not establish Pro equivalence. Shared-default replacement remains a separate owner decision. |

## Accepted R2 implementation checklist

These two nonblocking details are accepted under existing design requirements.
They change neither the API nor error selection, model policy or verification
criteria. Keep them in the implementation and request-disposition checklist;
no proposed runtime behavior or new regression test is claimed implemented.

1. **Concrete non-required winner and issue #9 residual.** The parent reproduced
   both cases on current source. A Google leg with `google.route="agy"` and neither
   `agy` nor `gemini` block selects `anyOf`; the design's guarded extraction yields
   `missing=None`. Adding `gemini={}` selects the route-specific `required` error,
   yielding `missing="agy"`. Both are currently rejected as `schema_violation`.
   Add both vectors and their selected paths to step 2's already-required
   non-required-winner tests, and name this limit in #9's partial disposition.
   Preserve first-error selection; do not walk child errors or promise host
   diagnostic-message parity. The neither-block path observed was
   `properties/legs/items/allOf/1/allOf/2/then/anyOf`.
2. **PR #12 rule-text consistency.** Its diff also changes R-GOOGLE's sentence
   describing measured refused-model records. If all new rows stay held, keep
   that sentence unchanged. If evidence supports some rows, update the sentence
   only to the accepted CLI/version/carrier scope. Never adopt the unqualified
   replacement while holding the supporting rows. This implements section C's
   accurate-provenance and no-implied-acceptance requirement; no policy change.

## Verification and retained evidence

`git diff --check` passed. A focused two-case current-source validator probe
completed with both assertions passing; it does not exercise the proposed API.
No new implementation suite, build or native-platform validation was run for
this document-only review. The future source, sdist, isolated-wheel, native
macOS/Ubuntu Python 3.12/3.14 and fresh implementation-review gates remain.

The owner's workspace retains both complete rounds under
`_runs/20261016-lib-minimal-design/<review-id>/`: `final-collect-output.json`,
`adjudication.json`, native terminal observations, `astra-final.md`,
`managed-export/` and `closure.json`. R2 also retains
`roster-first-error-probe.json`; its probe script is in the parent directory.
The exports preserve exact inputs, original reviewer reports and host receipts.
Issue/PR snapshots remain proposals, with no GitHub comments, closure or merge
performed by this task.

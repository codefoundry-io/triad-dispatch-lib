# Project review trial

The owner selected this profile on 2026-10-14 for development of
`triad-dispatch-lib` only. It changes neither the public library's model defaults
nor either host distribution or the workspace-wide review composition.
The shared specification and implementation are developed together here;
the existing Codex host supplies execution, custody and provider adapters.

## Required reviews

Explicitly select the public v2 workflow in the Codex host and resolve this
repository's `.agents/triad-review-legs.json`. Retain the canonical names
`claude`, `codex` and `google` so host defaults are overridden instead of retained
as extra reviewers.

| Entry | Route | Requested model | Requested effort |
| --- | --- | --- | --- |
| `claude` | Claude CLI | `claude-opus-5-5` | `xhigh` |
| `codex` | Fresh native Codex child | `gpt-6.1-sol` | `xhigh` |
| `google` | AGY | `gemini-4-argon-high` | `high` |

All three are enabled and required. Give them the same frozen objective,
criteria and approved source boundary, with independent prompts and result
custody. Use the host's existing v2 lifecycle, capability preflight, terminal
checks, six-field bindings and integrity checks. Start independent reviewers
before consuming healthy-path results. A missing, invalid or negative required
result cannot be replaced by a comparison. Approval never authorizes merging.
Do not run this roster through the legacy fixed Pro/Flash workspace renderer.

The owner increased each entry's review timeout to 2400 seconds (40 minutes)
on 2026-10-14 because reviews can take 20 minutes. Use the same parent-observed
budget for native reviews and the Astra comparison; a short status-poll timeout
does not terminate a review. At a real deadline, interrupt an owned native child
and await its terminal state. Cancellation cleanup may exceed the review budget.

Model catalog or help output proves only selection/interface availability.
Check actual native capabilities when dispatching; retain requested versus
observed settings separately and report hidden runtime settings as `UNEXPOSED`.
Do not substitute another model, route or effort to make a check pass.

## Current external evidence

The owner explicitly authorizes web search for every review, including the
separate Astra comparison. Bind that authorization through the host's existing
review request; do not add it to the roster schema or global configuration.
For changing facts about AI models, provider CLIs, SDKs, authentication and
platform behavior, check current official documentation, release notes or the
official source repository during the review. Record the URL, access date and
applicable version; distinguish supported, installed and actually observed
versions. Do not reject a current model or feature using remembered availability
or an older benchmark alone. If current official evidence is unavailable, state
the unresolved limit instead of treating historical information as current.
Apply this guidance in each round's objective/criteria and comparison brief.
Web evidence supplements the frozen code and local observations; it cannot
establish that an unexecuted provider or platform path passed.

## Astra comparison

Use a separate fresh native Codex child with:

```json
{
  "model": "gpt-6-astra",
  "reasoning_effort": "high",
  "fork_turns": "none"
}
```

These are native spawn fields, not an additional persisted configuration schema.
No Custom Agent or model installation is required when the host already exposes
these settings. Keep Astra outside the formal roster, basis membership and
agreement inputs. In this trial, run it alongside the required reviewers over
the same frozen material and neutral criteria, without sibling findings or a
preferred conclusion. In this trial the parent dispatches Astra directly with
the native fields above and collects ordinary findings as comparison evidence.
The library's `InvestigationRequest` / `run_investigations` API is available
for a future host callback integration; this trial does not require that bridge.
The parent owns native spawning and cleanup in either case.

Do not add Astra with `acceptance: informational`: every enabled formal entry
counts under the shared contract. Its comparison output has no approval vote.
Resolve and await any started comparison before final source integrity checks.
Comparison failure is reported separately. A reproduced material defect from
any reviewer still needs correction and a fresh required review of changed bytes.

Record requested/observed settings, terminal outcome, elapsed time, exposed usage,
reproduced unique findings, refuted findings and important misses. This is a
project trial, not a calibrated model ranking or a change to other projects.

## Local setup verification

Use one known source or installed Codex toolkit consistently. The nonmutating
`resolve-roster --project-root <this repository>` command validates configuration
only; its `capabilities_checked: false` is expected. Provider-free adapter checks
and fresh native observations are separate evidence from a complete review.
See [setup evidence](verification/2026-10-14-review-profile.md).

# Codex + three Google legs: operating specification

This is the operating profile authorized by
[the agreement](2026-09-21-codex-google-four-leg-agreement.md). The shared rules and
schemas remain authoritative; this document supplies a concrete setup and
verification procedure. It introduces no new configuration or result fields.

<a id="SPEC-FOUR-LEG-SCOPE"></a>
## Topology and common review goal

The following names are a fixed-roster example chosen under
[R-ROSTER](../reference/review-rules.md#R-ROSTER), not a minimum topology or
additional owner ruling. The selected entries share the same phase goal, full
scope and criteria under [R-PROMPT](../reference/review-rules.md#R-PROMPT).

| Enabled entry | Family |
|---|---|
| `codex` | codex |
| `google-contracts` | google |
| `google-failures` | google |
| `google-state` | google |

All four independently inspect the same complete approved scope, relevant tests
and affected consumers. Their names are invocation identities, not separate
review personas or a task split. The leader applies R-SMELL when triaging
findings; no mandatory long first-review checklist is added.

On host B the Codex entry stays a fresh native Codex child. On host A, a Codex
entry uses A's existing Codex CLI route; A's native family is Claude. Do not add a
native Codex mechanism to A or silently substitute native Claude for the specified
Codex entry. Report that topology distinction in the resolved run description.

## Project roster example for B's Legacy Gemini CLI route

This example uses the existing B project file `.agents/triad-review-legs.json`.
It assumes the host's existing authentication and capability checks permit the
Gemini route. `null` uses the adapter's supported default; it is not proof of the
actual runtime model. Do not bypass a route, version, login or policy refusal.

```json
{
  "schema": "triad-review-legs.v2",
  "legs": [
    {"name": "claude", "enabled": false},
    {"name": "google", "enabled": false},
    {"name": "codex", "enabled": true},
    {
      "name": "google-contracts", "vendor": "google", "enabled": true,
      "acceptance": "participating", "timeout_s": 600,
      "google": {"route": "gemini"},
      "gemini": {"model": null, "effort": null}
    },
    {
      "name": "google-failures", "vendor": "google", "enabled": true,
      "acceptance": "participating", "timeout_s": 600,
      "google": {"route": "gemini"},
      "gemini": {"model": null, "effort": null}
    },
    {
      "name": "google-state", "vendor": "google", "enabled": true,
      "acceptance": "participating", "timeout_s": 600,
      "google": {"route": "gemini"},
      "gemini": {"model": null, "effort": null}
    }
  ]
}
```

Overrides merge by name. Disabling the shipped `google` entry avoids accidentally
running it alongside the three named replacements. Inspect the actual resolved
roster: it must contain exactly the four enabled names above, even if the existing
project configuration has other optional entries. Preserve unrelated owner
configuration; apply a reviewed project-local delta rather than replacing it.
For AGY, use its existing route/configuration and capability checks instead; never
copy a Gemini model identifier into an AGY control or change a started route.

Host A keeps its own project-roster location and adapter defaults. This B example
is not a command to copy B's installation paths or auth policy into A.

## B: bound common task

Put the same short phase goal in the common bound `TASK.md` before preparation.
The leader also records requirements, scope, supported environment, relevant
dependencies, observed test versions, unknowns and evidence in the existing
TASK/brief. The host binds and transports that material; it does not validate
the prose's meaning or Markdown format. For this code-review example, use:

```text
Independently review the complete bound code scope against its requirements and
target environment for correctness and completeness. Return one bound verdict
for your own leg and report only evidence you inspected.
```

Use `formal-plan` for plan review, and `pre-merge` or `implementation-review`
for code review; omitted stage defaults to `pre-merge`. The renderer supplies
`leg_name`; the roster's `note` is not a prompt override. Do not add unsupported
`lens`, `focus` or `prompt` keys or mutate a rendered prompt after allocation.
Changing the goal, criteria, roster or controls changes the basis and requires
every selected leg to review the current full scope again.

The B integration seams cited here are historical source references. A's
published legacy X legs do not prove named v2 behavior. Inspection of A's
current implementation is deferred until shared-spec adoption and separate
implementation planning; [the current-source handoff](claude-codex-google-four-leg-handoff.md)
is context, not current verification.

<a id="SPEC-FOUR-LEG-COLLECTION"></a>
## B: dispatch, collection and owner decision

Use B's existing explicit v2 workflow. Resolve and show the four entries,
prepare and bind the common packet, validate every adapter, and allocate all four
independent invocations. Start their native/CLI calls using the host's supported
concurrent dispatch; provider capacity or account failures remain observable
failures, not permission to drop a leg or weaken controls. No new scheduler is
needed. Preserve each name/attempt's prompt, result, read evidence and receipt.

Expected outcomes apply R-AGREE to this selected roster:

| Observed state | Target outcome after adoption |
|---|---|
| An enabled entry is missing or recorded as failed-to-run | `INCOMPLETE` on B; preserve the actual host outcome/evidence |
| Invalid verdict, binding or custody evidence | Validation refusal or a recorded failed attempt; never agreement |
| Any entry returns a non-affirmative verdict, including Minor-only negative, or has a blocking finding or open question | `BLOCKED` on B; no silent majority override |
| All four return explicit `SAFE TO MERGE`, with no blocker, open question or integrity gap | `AGREED` on B; two-family coverage is reported as receipt data |
| The owner records an exception to a non-passing round | Preserve the original machine result and record a separate owner decision against that round and digest; never call the exception `AGREED` or `PASS` |

Owner decisions use the existing channel. An exception identifies the
round/basis, actual entries and families, findings and their dispositions, and
the explicit decision. Do not rewrite a raw verdict or apply blanket approval
to future/changed bytes. Selecting this profile is not approval of an unrun
round. A failed selected leg cannot be dropped by the leader to obtain a pass;
only the owner can change the roster for a new basis.

A failed-to-run entry may retry only after diagnosis with unchanged conditions.
A completed negative review is not a transport retry. Evidence export, cleanup,
read-only containment remains unchanged; review web follows
[R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB) (the owner's standing authorization).

## Deferred host verification

[Case C33](../cases/cases.json) owns the profile's expected behavior; C12, C14,
C19 and C20 retain the underlying roster, binding and retry/re-review cases.
After shared-spec adoption and separate implementation planning, inspect A's
actual current implementation. For an A v2 port, use its approved migration
scope; do not treat published legacy X legs as proof that these checks pass:

1. Validate the override and resolve exactly four enabled entries/two families.
2. Confirm four exclusive invocation/result/read-evidence locations. Prove a
   same-family sibling's result or receipt cannot satisfy another entry.
3. Verify clean two-family completion reaches `AGREED` only when every selected
   leg explicitly returns `SAFE TO MERGE`; missing, invalid and blocking results
   remain distinguishable.
4. Check that the common phase goal and each leg's bound identity reach the
   actual prompt; do not claim semantic completeness from transport checks.
5. Verify failed-entry-only retry and full re-review when the goal or task changes.
6. Where the exact live route is available and a bounded run is authorized,
   execute the four invocations and retain terminal results and any owner decision.
   Otherwise record that live scenario as NOT RUN with a concrete run procedure.

This authoring change does not execute that live scenario. A single successful
Gemini call is not evidence of four concurrent calls, host policy enforcement
or a completed review/admission. Do not add an application
UI, automatic technology detection, a voting policy, or a new lens schema while
implementing this operating profile.

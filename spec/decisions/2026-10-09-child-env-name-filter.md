# Child environment name filtering — U2c

**Current disposition:** the additional model/effort selector investigation,
warning and verification proposal below is WITHDRAWN by the owner. Its earlier
hold/review requests are historical, not pending implementation requirements.
See [the cancellation record](2026-10-09-selector-proposal-withdrawn.md).
Independent credential/loader hygiene and C75 are outside that cancellation.

Latest B outcome: the bounded U2c implementation, including intermediate Gemini
preflight preservation, passed fresh focused370/full2029 tests with4skips and
the complete R2 review (all four SAFE, matching integrity). See
[current B evidence and remaining A request](2026-10-09-b-child-environment.md).
The earlier candidate/R1 pending statements below are historical. Full C37 and
the complete spec-to-code task remain open; no product release is implied.

Current rule reconciliation at PR13 `74d259c`: R-NOCOST/C11/C17/C37 preserve
GEMINI_MODEL, ANTHROPIC_MODEL and ANTHROPIC_SMALL_FAST_MODEL, together with user
effort settings. The current omission set is17 loader +46 credential/endpoint
names, plus four project names except on Gemini. Counts and A's matching-list
claim below describe the pre-withdrawal snapshot. At A `5531a663`, those three
obsolete model omissions and value-before-name filtering remain visible in
source; A runtime NOT RUN. PR13 comment6079317869 requests the equivalent
correction and C75 evidence. No native-leg or additional selector work is asked.

Basis: remote main3afc4d7, PR13 b8512b6; B632f426 plus preserved dirty candidate;
A af54fb82 (comment basis bb933c6b). This implements the existing R-NOCOST/C11/
C17/C37 agreement, not a new authentication design or native-leg mechanism.

Pre-implementation provider-free spike on 2026-10-09 extracted the existing
normative list: 17 loader names, 49 credential/endpoint/model-selector names,
four Google project names. B's ordinary shared helper retained all53 non-loader
names; formal Gemini retained40 forbidden names, formal AGY retained43. These
are synthetic mappings and presence checks, not real credentials or vendor
dispatches. B's Google diagnostics also applies the AGY list to Gemini, dropping
its required project exception. A's literal name sets match all70 agreed names.

Both helpers use `for k, v in src.items()` before filtering. A guarded synthetic
Mapping demonstrates that B retrieves an omitted value before rejecting its
name. A has the same source construct, but its helper was not executed here.
R-AUTH already says the values are never read: C75 makes the testable boundary
explicit before dependent implementation. Iterate names and retrieve only kept
values. This does not inspect or mutate credentials, provider settings or the
parent environment. It makes no billing-route attestation.

B correction: one common full list for every vendor child; route identity selects
only the existing four-name Gemini project exception. Apply it at the shared
spawn and standalone version/help/diagnostic probes. Keep PATH, configuration
pointers and GOOGLE_GENAI_USE_GCA, and preserve explicit extra removal callers.
The proposed interface is scrubbed_child_env(base=None, *, cli=None, remove=()).
No route identity defaults to removing the project group. Synthetic helper and
actual local subprocess tests cover normal/repair/formal consumers and probes,
without calling authenticated CLIs. Dedicated RED/GREEN and the existing review
gate precede any completion claim. No implementation completion is claimed yet.

A request: verify C75 on your helper and change name filtering if needed; keep
the already matching set and Gemini exception. No host-native change requested.
The shared rule remains authoritative; A is supporting source evidence only.

## PR13 maintainer reply 6078141262

The reply agrees with R-AGENT-ROLES/C73 and the AGY profile contract/C72.
Official Claude tools-reference (Glob tool behavior, read 2026-10-09) confirms
that a subagent listing Glob/Grep and omitting Bash regains its listed search
tools. A reports a Claude2.1.289 same-tool-shape probe; this is A-reported runtime
evidence, not rerun by B. B's previously measured null-agent CLI path stays.
https://code.claude.com/docs/en/tools-reference#glob-tool-behavior

A source af54fb82 confirms embedded AGENT_BODIES and check_agent_file's exact-byte
comparison. Its wrapper-digest binding is reported as planned Task6e, and search
event evidence as planned Phase12T4; neither is certified complete here. Keep
tests.A NOT RUN until its named conformance evidence arrives. No extra live
probe or B agent/default change is needed. C74's later request remains pending;
this comment explicitly covers earlier commits through b085a6e, not U2b.

## Historical precedence investigation — proposal subsequently withdrawn

The owner challenged the premise before continuing: explicit CLI model/effort
may already take precedence, so research and conflict spikes must come first.
B had applied an unadmitted candidate (local smoke59passed); no dedicated GREEN,
full-suite or review completion is claimed. The candidate is preserved on hold.
The preceding list-parity tests establish conformance to the current list, not
the necessity of every entry. C75's name-before-value question is independent.

Measured on Claude Code2.1.289 with isolated HOME/config and --bare:

| Conflict | Observation |
| --- | --- |
| ANTHROPIC_MODEL=haiku + --model opus | /model reports Opus5.5; env-only control reports Haiku4.5 |
| ANTHROPIC_DEFAULT_OPUS_MODEL=claude-haiku-4-5 + --model opus | /model reports Haiku4.5 |
| No effort environment + --effort xhigh | Loopback request output_config.effort=xhigh |
| CLAUDE_CODE_EFFORT_LEVEL=low + --effort xhigh | Loopback request output_config.effort=low |
| CLAUDE_CODE_EFFORT_LEVEL=xhigh + --effort low | Loopback request output_config.effort=xhigh |

The /model display followed the effort flag, while the generated request followed
the environment variable. A selection display alone does not attest effective
effort. The request probe used a synthetic key and a local HTTP stub returning
400 LOCAL_PRECEDENCE_CAPTURE_ONLY; all children ended with the expected exit1.
No live subscription inference or actual credential was used. This proves the
isolated API request-building path, not an observed subscription response.
Official documentation independently states these model/effort priorities:
https://code.claude.com/docs/en/env-vars#precedence
Alias remapping: https://code.claude.com/docs/en/model-config#model-aliases

Gemini0.63.0: three isolated executions of the exact official bundle's model
resolver chose flag over env/settings, env over settings, then settings alone.
Bundle SHA256 a64b06d8a06673cfae0134558e162e5b015d088a3751639c7d6dc4a88c67c1f8,
lines8455ff. This was vendor-code extraction, not full authenticated startup.
https://geminicli.com/docs/cli/model-routing/#model-selection-precedence
AGY1.3.2 exposes --model/--effort in official headless docs, but three isolated
/model probes stopped at authentication; its conflict precedence is UNMEASURED.
https://www.agy.dev/docs/cli/headless/#select-a-model-effort-or-agent

Disposition/request to A: diagnose direct model defaults, alias remapping,
effective effort and auth-route hygiene separately. R-NOCOST currently lists
ANTHROPIC_MODEL and GEMINI_MODEL, but not CLAUDE_CODE_EFFORT_LEVEL or
ANTHROPIC_DEFAULT_OPUS_MODEL. Do not infer that the current list enforces every
pin, or add/delete list entries from these observations without the shared
decision. Explain the purpose of default-model removals when explicit flags
already win, including omitted-option paths. Native legs stay host-owned;
no Claude agent definition is implied. This is evidence and a review request,
not a normative amendment or permission to change auth routing. Required design
diagnosis and owner decisions precede dependent implementation.


## U2c R1 — intermediate preflight boundary

B's narrowed candidate passed focused335/full2027 with4skips and both validators,
but triad-child-env-20261009-r1 is NOT_APPROVED with matching integrity. Claude
and native independently found that review_adapters_v2.probe starts the selected
Gemini wrapper through _run_once("preflight", ...). The new shared name filter
drops the project group at that outer boundary; the wrapper's later Gemini-aware
version/help calls cannot restore it. Source confirms the path at
bin/review_adapters_v2.py37-41,211-225 and bin/_common.py1451-1462,1641.

C75's existing every-probe/Gemini exception also applies through intermediate
adapter processes. Its input now names that chain explicitly; this is coverage
of the existing contract, not a new selector rule. Add a full adapter -> wrapper
-> synthetic vendor version/help regression, then carry the selected Google route
through the outer probe. Default/unknown/non-Gemini paths still omit project
names. No new environment name, runtime inspection or native-leg change.

A c57d6b60 still has the previously reported items() and three obsolete model
omissions. A runtime NOT RUN. Please verify the same preservation/filtering
contract and intermediate external-wrapper probe path if present; B's internal
adapter mechanism is not an instruction to copy host-specific code.

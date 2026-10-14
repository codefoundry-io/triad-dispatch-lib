# Actual native Codex lifecycle verification

Date: 2026-10-12. Tested checkout: `db16cd001dc3f965582e3b0d32f7d7fa239773aa`.
Package: unpublished `0.1.0.dev2`; runtime and driver unchanged.

## Scope

The owner requested Codex-host testing after the
[previous experiment](2026-10-12-native-codex-callbacks.md) disclosed that native
cancellation and timeout had only synthetic coverage. Three fresh actual native
Codex children were dispatched from the parent task inside this library
repository. Existing consumer repositories, installed TRIAD plugins, the shared
specification, provider CLIs, SDK/MCP integrations and global settings were not
executed or changed.

All children requested `gpt-6.1-sol` / `medium`, with no inherited conversation.
Two controlled lifecycle children read their bound packet and held their active
turn for interruption. The third independently reviewed the packet and returned
its actual final JSON. The parent owned native spawning, interruption, observed
terminal state and receipts. Scope restrictions were prompt-controlled.

Each driver installed the existing wheel in a fresh temporary environment,
executed Python `-I` from a neutral working directory and verified all 27 exported
runtime paths in isolated site-packages. Native platform: macOS 26.6.2 ARM64,
Python 3.12.13. Wheel SHA-256:
`b89d07594f7173393949eca07c5525cfa1709a36857c543c8259934b82c548eb`.

## Observed results

| Scenario | Actual native action | Observed library result |
| --- | --- | --- |
| Invocation timeout | 60-second deadline emitted a cancel request while the owned child was running; parent interrupted it and separately observed `interrupted` before acknowledging cleanup | `timed_out`, no output value, `cleanup_only=true`, integrity true, agreement false |
| Repeated parent cancellation | Two library task cancellations while a native child was running, before its terminal acknowledgement; parent then interrupted and observed the child terminal | Cleanup stayed pending after both cancellations; `CancelledError` propagated only after acknowledgement; queued second request never appeared; no review report or approval |
| Late final delivery | Actual final observed after the cancel request already existed; parent posted the original response with a completed terminal receipt | Response independently validated as `SAFE TO MERGE` with all six bindings, but the run remained `timed_out`, no output value, `cleanup_only=true`, agreement false |

For the two interrupted children, `interrupt_agent` returned the previous state
`running`; a later `list_agents` call for each exact task path returned
`interrupted`. The parent did not treat the interrupt call alone as completion.
Their cancelled receipts were published only after these observations. No final
response was received for either child; the required response hash is SHA-256 of
empty bytes, explicitly recording the absence of observed final bytes.

Parent cancellation used two selected entries with `max_concurrency=1` and
300-second entry timeouts. A disposable wrapper called the existing installed
`run()` API and cancelled its task twice after external control markers. It
observed the task still pending after each cancellation. After the native terminal
acknowledgement, the task raised `CancelledError`. The second entry's prepared
prompt existed, but its `request.json` never appeared, so it never acquired an
invoke slot. The cancelled run produced no `report.json`; the wrapper recorded
these observations separately without inventing an agreement result.

The late case originally planned to delay a receipt after early final delivery.
The actual final was first captured when `cancel-request.json` already existed,
so an additional artificial delay was unnecessary. This proves rejection of
late supervisor delivery, not the time at which the backend generated its answer.
Before acknowledging completion, a separate `-I` process in the same still-live
isolated installation validated the original JSON and its expected bindings.
Thus the withheld output was a valid affirmative response, rather than a malformed
answer that would have failed admission anyway.

The late original response is 916 UTF-8 bytes, SHA-256
`dd72223a9cc32305a082b2cad568ed8e7602b6556f4286721d5ec603dbbc1948`.
It was preserved without normalization or verdict rewriting.

## Evidence and reproduction

The existing [supervised protocol](../../README.md#supervised-native-callback-experiment)
was used without product changes. Timeout and late delivery use the existing
driver CLI. The disposable parent wrapper reuses `installed_wheel`, runtime
`identity` and `native_codex_smoke.run`; it supplies cancellation controls because
the ordinary CLI has no parent-cancellation test switch. It does not replace the
library's scheduler or cleanup algorithm.

Local evidence is retained under ignored
`_runs/native-codex-lifecycle/20261012T101355Z-fde3d90f/`: plan, bounded arithmetic
packet, configs, wrapper, original prompt/request/cancel-request/receipt artifacts,
native observations, parent control events, driver reports/logs and the original
late response. All three driver commands reached terminal exit zero (sessions
54208, 89502 and 95552), denoting recorded experiments rather than review approval.
All owned native children are terminal: two interrupted, one completed.

The fresh post-run checks verified config, wheel, packet, prompt, request and
receipt bindings; both completed timeout reports record integrity true. Parent
cancellation skips the formal integrity/agreement step, so its artifacts received
a separate consistency check and no agreement claim.

- `artifact-hashes.json`: 38 indexed files; SHA-256
  `d7a261e4d7dc48f02818300d6e986a770c73297432dd24f113480c9547c8d56b`.
- `summary.json`: SHA-256
  `22028bdd0b215ff9a672a89ac0825120218fd5c4f1121e4822ab80cffebd1b5d`.

An independent read-only Codex evidence audit checked all 38 indexed hashes,
receipt bindings, cancellation ordering and late-response correspondence. It
found no blocking inconsistency and confirmed the timing/attestation limits below.

Reproduction requires a supervising Codex session, fresh run directories and new
native children. These local artifacts are not package runtime dependencies.
The previous 399-test suite and native-platform CI remain the regression baseline;
this follow-up adds actual lifecycle observations and changes documentation only.

## Limits

Native termination means the supervisor-visible task reached `interrupted` or
`completed`. Effective backend model settings, remote processes and backend
generation timing remain unexposed. Captures are parent copies of tool-returned
strings, not independent provider wire-byte attestations.

The 60-second deadline requests cancellation; total run duration also includes
the parent's interruption, terminal observation and acknowledgement. Cleanup is
cooperative and can wait indefinitely if the supervisor does not respond. This
experiment does not establish a hard wall-clock termination guarantee.

These are actual Codex lifecycle observations on macOS. They do not prove native
agent behavior on Ubuntu, behavior of other providers, or adoption by either
existing host. No implementation fix, package rebuild, consumer change, merge,
release or global installation was required.

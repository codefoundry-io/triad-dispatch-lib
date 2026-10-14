# Cleanup corrections and review evidence

This records the correction work on `codex/strict-v2-admission`, based on
`81748d7` plus the preserved project review profile and current working-tree
changes. The package remains unpublished `0.1.0.dev3`.

## First correction snapshot

The R1 review (`20261014-lib-spec-r1-5754af`) ended BLOCKED. The owner approved
both reproduced defects, regression tests, adoption/spec mapping/documentation
work and a complete re-review with generous deadlines.

- The native test driver skipped terminal cleanup when writing a cancellation
  request failed. Three regressions failed before correction and passed after
  moving terminal cleanup into `finally`, including a broken diagnostic and
  repeated parent cancellation.
- An overflowing but schema-valid callback timeout could make `asyncio.wait`
  raise after callback creation. A live-loop regression exposed the leftover
  task. The coordinator now drains its child before propagating exceptional
  wait setup; it does not add an arbitrary canonical timeout maximum.

On macOS 26.6.2 ARM64 / Python 3.12.13 / pytest 9.1.1, the first corrected
source and unpacked-sdist suites each passed 637 tests. Authoring, generated
assets and diff checks passed. A wheel rebuilt from the unpacked sdist passed
the bundle probe and isolated Codex, four-route and native synthetic drivers.
These are library/driver tests, not effective provider identity or backend
termination evidence. No Ubuntu run was made for these corrected bytes.

The first corrected sdist SHA-256 was
`a3bbc924df9bf9eb59492cfae7d03dfe712ef51a4f565b624839adf272b4425e`;
its rebuilt wheel SHA-256 was
`fd90268932f96109da9e1cab85621184ce7f3bad804ba24c1766a143a94964ec`.
Those hashes describe that tested snapshot, not later documentation or code.

## R2 review and follow-up

Fresh round `20261014-lib-spec-r2-917b20` bound digest
`32d72dd18a7057f077845ba9c0edd1fed7e11a3dc3b72668f6859803f8e3a4d7`.
All three required entries completed: Opus 5.5/xhigh and Argon/high approved;
Sol 6.1/xhigh requested fixes. The collector returned BLOCKED. Astra/high was
a separate comparison, with no ballot. Every entry had a 2400-second budget;
short observation waits were not review deadlines. All results were preserved
and the exact managed review/staging roots were cleaned after export.

- Sol identified ordinary stale/nonterminal receipt refusal releasing native
  custody before a matching terminal acknowledgement. This is a driver defect,
  even though agreement remains blocked.
- Astra identified `math.isfinite(10**400)` raising `OverflowError` during
  receipt validation. A synthetic reproduction ended a timed-out call before
  valid replacement acknowledgement. It did not induce real provider leakage.
- Opus requested a repository record of the current verification and platform
  limits. This document supplies that record. Its claim that receipt validation
  could only raise ValueError/OSError was disproved by the overflow reproduction.

Follow-up tests exercise malformed acknowledgement replacement, cancellation
during that wait, and the distinction between terminal metadata and bad response
bytes. Timestamp conversion overflow uses the existing validation refusal.
Focused independent pre-review also found Python 3.12 cyclic-link resolution
raising `RuntimeError` before receipt refusal. Three RED/GREEN cases cover normal
and timeout-cleanup custody plus ancestor-link resolution; the regular-file
validator now converts that resolution failure into the existing refusal.
An original refusal cannot be rehabilitated into a successful review by a later
replacement receipt. Canonical schemas, dependencies, provider defaults and host
distribution remain unchanged.

## Final correction verification before R3

After the receipt and cyclic-link corrections, local macOS 26.6.2 ARM64 /
Python 3.12.13 source tests passed **654** cases; unpacked-sdist tests passed the
same **654** cases. This adds 21 cases to the 633-test baseline. The native driver
file passed 55 cases. Authoring, generated-asset and diff checks passed; all 52
unique test-function references in the conformance map resolve to current tests.

The rebuilt wheel passed the isolated bundle probe and Codex, four-route and
native synthetic drivers. The measured sdist SHA-256 was
`2aa473300ddccc94c926dd1e8b16a6a24853d949e378c9e267493de5f496a84f`;
its rebuilt wheel SHA-256 was
`331abf27d6d7600e2115bce9e6f168ab7d93f70e75a9d3ec07aec750272072b0`.
Those artifacts were measured before adding the documentation-only result
record used by R3. Runtime code, tests and canonical assets did not change between
that measurement and R3 preparation. Later corrections are recorded below.
Temporary build archives/environments were removed after recording the evidence.

No corrected-byte Ubuntu run, real native cancellation replay, effective model
identity attestation or host adoption is claimed. The R1/R2 votes remain historical.

## R3 review and bidirectional audit

Round `20261014-lib-spec-r3-b26100` bound digest
`8b7c7f7513a1429b514d4cf07c899cfc6387f4225a37866ad343958892966c91`.
All three required entries completed with no missing entries or deviations;
the collector returned BLOCKED. Sol requested the receipt-readiness correction;
Opus approved with a Minor finding for the same path, and Argon approved. Astra
independently reported the same defect. Severity differences did not remove the
accepted correction. Results were exported before exact review/staging cleanup.

Receipt stat/lstat readiness checks were outside the refusal guard. The driver
now guards the complete observation attempt, retaining custody and first-refusal
evidence on ordinary filesystem errors. Ten RED/GREEN cases cover stat/lstat,
EACCES/EIO, normal/timeout cleanup, deadline during refusal and repeated parent
cancellation. The native-driver suite passed 65 cases.

The owner then requested [bidirectional specification/interface auditing](2026-10-14-spec-contract-audit.md).
Four independent source audits found an additional pre-publication CLI refusal
gap for cyclic context paths. Eight cases failed before normalizing the two
path-resolution boundaries and passed afterward; the Codex driver suite passed
27 cases. Eight new controlled races establish current parent-cancellation
precedence over ContractError while awaiting all callback cleanup. Those already
implemented races passed without changing production behavior; no artificial
RED mutation was performed.

The current API reference covers all 27 exports and supplements the conformance
map's explicit rule ownership. Host/leader-only obligations remain outside the
library runtime. No provider wire schema, generated payload, dependency, timeout
limit or runtime version changed.

## Final verification before R4

Local macOS 26.6.2 ARM64 / Python 3.12.13 source and unpacked-sdist suites each
passed **680 tests** (47 above the original 633-test baseline). Authoring maps,
generated assets and diff checks passed. All 27 exported names appear in the API
reference; all 53 named conformance test references resolve; the case map contains
exactly the 58 canonical IDs. Current documentation links/anchors passed checks.

The wheel rebuilt from that sdist passed the installed bundle probe and isolated
Codex, four-route and supervised-native synthetic drivers. Measured hashes:

- sdist: `50a2442eb3b649773335f22f2adf059b37fda3e03e7d3d9c8b7dd2f890e51c2d`
- wheel: `39c6efe0eff4b8fdf8c5fbf99c140e7d2c864acc4e1b1e9e1bb77cfb7935deec`

The build includes the API and 58-case references. This result-recording paragraph
and the current-status update were added after measurement; runtime/tests/assets
are unchanged. Temporary build/archive environments were removed. Corrected-byte
Ubuntu execution and real native cancellation/backend termination remain unrun.
R4 (`20261014-lib-spec-r4-bf8144`) subsequently completed `AGREED`, with all
three required entries returning `SAFE TO MERGE`; Astra's separate comparison
found no concrete blocker. Two nonblocking CLI-input findings were retained.
The owner then authorized their correction and native Ubuntu verification;
see the [follow-up record](2026-10-14-cli-input-corrections.md). R4's approval
applies only to its frozen candidate, not the later correction.

## Evidence boundaries

The current conformance map names partial library coverage and retained host
obligations. AGY recovery, full failure classification, host-fault collection
semantics and real process custody remain host-owned. Earlier Ubuntu/macOS CI
and native dev2 observations retain their original source/build identities.
No merge, package publication, global installation or consumer port is claimed.
Formal approval applies only to its bound snapshot; old votes do not transfer
to corrected code.

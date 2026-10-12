# B Gemini authentication exit 41

This is implementation evidence for settled C37 / R-AUTH / DL-99, not a new
authentication design, a revision adoption or full C37 conformance.

Source: [Gemini CLI v0.63.0 exitCodes.ts](https://github.com/google-gemini/gemini-cli/blob/v0.63.0/packages/core/src/utils/exitCodes.ts),
fetched 2026-10-09, names FATAL_AUTHENTICATION_ERROR=41. The owner already accepts
vendor source as measured evidence. A's `_auth_carrier_stop` at 0e04d2a recognizes
it; B 632f426 plus dirty candidate previously treated 41 as unmeasured and lost
its authentication classification on timeout and late SIGTERM/SIGHUP.

B's bounded correction is in `bin/_common.py`: recognize only Gemini's raw code,
return oauth-env / 65 before other failed-run decisions, retain the code through
capture and signal handling, and preserve cancelled-answer withholding and
existing process cleanup. The existing browser-login remedy remains; no login
probe, credential reading, authentication fallback or automatic retry is added.
Actual production delta +26/-13 (net +13). Other CLI code 41 behavior is unchanged.
No native-leg changes or A implementation changes are requested.

Provider-free evidence: fresh dedicated source executor observed 7 failing Gemini
cases and 3 passing other-CLI controls. Leader reproduced RED after correcting
test-log isolation, then new and existing parent-signal modules passed 18 cases.
Separate dedicated GREEN passed six complete affected modules (179 passed,
4 skipped) and both source skill validators. The initial RED invoked historical
stale-log cleanup at an import-time default root; without a pre-run inventory its
deletion effects are unknown. The corrected fixture isolates that root and blocks
unrelated global temporary-log cleanup. This limitation is retained explicitly.

Full suite: **1925 passed, 4 skipped**, exit 0 (411.41s, Python 3.12.13,
Darwin arm64); measured source hashes, HEAD and Git status remained unchanged.
Fresh `triad-gemini-auth41-20261009-r1`: Claude opus/xhigh, AGY Pro/high,
AGY Flash/high and native Astra/high all SAFE; same-basis result/schema binding,
canonical re-render and ROUND_INTEGRITY_OK, outcome ALL_SELECTED_APPROVED.
Digest `e54c33c00da4c621a0d27950f8f924859c9c7c3b10694162412503e4b1efe013`.
All producers terminated; custody exported and exact temporary staging/cwd removed.
Three nonblocking suggestions were adjudicated: retain the current signal-helper
placement; defer stale classifier-header documentation and two extra engine-level
coverage cases to the remaining carrier unit. Current tests do not exercise an
actual timed-out child exiting 41 on TERM or capacity text through the retry loop;
source inspection supports those paths, not a claimed execution of them.
Local evidence: B `_runs/spec-plan-20261009/u2a/`; maintainer workspace
`_runs/reviews/triad-gemini-auth41-20261009-r1/`. The child exit fixtures establish
control flow, not authenticated Gemini runtime behavior. No logout/live failure
was manufactured, and installed Gemini below the 0.63.0 floor was not invoked.

Remaining U2 items: measured structured/text carriers, environment scrub parity,
raw-auth false positives and extension handling. AGY credits output carrier is
still unmeasured. Optional Claude-agent U1c remains deferred under C73.

Claude maintainer: no new behavior is requested from A for this item. Compare
your existing exit-41 handling with the same C37 rule at your next conformance
run; report any contrary source or carrier evidence through the shared spec.

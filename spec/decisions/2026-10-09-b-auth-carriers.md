# B measured authentication carriers — U2b

This records the local B implementation candidate for settled R-AUTH/R-CLASSIFY,
C37/C43 and clarified C74. Shared main was fetched at 3afc4d7; C74 was recorded
at dd85b52 and clarified at d5c5756 BEFORE the dependent B corrections. It does
not certify full C37/C43, adopt a revision or change either host's native leg.

B source is 632f426 plus the intentional dirty worktree. The shared carrier
predicate reads original vendor error fields before capacity/timeout decisions,
retains the observed STOP through signals, and keeps completed usable answers.
Claude extraction promotion selects authentication from the original envelope
while preserving the previous extracted-error input for other classifications.
AGY schema reflections and denied commands remain distinct: the ENTIRE denied
command is excluded from authentication, including a quoted banner. Existing
admission/permission checks still decide whether an answer is valid. The own
stderr banner remains an authentication carrier. Raw authentication phrases and
their extension proposals are removed/ignored/refused; typed exit-code extensions
and general extension validation are separate work. Production delta +157/-95,
net +62 across three files; tests +251/-1 and documentation +18.

Shared contracts/vendor-failure-lines.json and review-rules.md supply the measured
carrier basis. No new vendor field/channel or AGY credit carrier was invented.
In particular, no capture proves a full multiline denied command body; synthetic
command-content controls enforce input provenance, not a new vendor-shape claim.

Verification (macOS arm64, Python 3.12.13): initial dedicated RED39failed/34passed;
R1 corrections RED11failed/1passed; R2 correction RED2failed/4passed. Final fresh
dedicated GREEN: 437 passed/4 skipped across ten modules, both skill validators
passed, full suite 2005 passed/4 skipped. Source hashes, HEAD and Git status were
stable. The final deterministic executor disclosed reading instruction/memory
context before running the fixed manifest; this is not a blinded prompt-choice
probe. Synthetic child processes exercise actual retry/timeout/signal capture;
they do not prove authenticated vendor service behavior. Other OS checks NOT RUN.

Review `triad-auth-carriers-20261009-r3`: Claude opus/xhigh, AGY Pro/high, AGY Flash/high and fresh native
Astra/high all SAFE, same-basis schema/result binding and ROUND_INTEGRITY_OK,
outcome ALL_SELECTED_APPROVED. Digest `133cb3e3da1671ac54d0eca03df6ba77e4d60dbe3daa4bdd4e6fb198d654d3fc`.
All producer sessions terminated; custody exported, exact temporary stage/cwd
removed. R1/R2 failed rounds and their corrections remain preserved evidence.
Final adjudication is in the corresponding local review directory.

Current candidate hashes:
- `bin/_common.py`: `dc6d8a08e89c7a4db812f216fb73656a04441be0888d913a4f4b2c07e451588b`
- `bin/claude_wrapper.py`: `f6954258903eae7976b80e91af70ca92eb5980261c94dbc860b61e2477089852`
- `bin/antigravity_wrapper.py`: `b4d1e39e6378c5bfb533363ad06d24f5282b235ba7c4269f766042c88c3450f6`
- `tests/test_auth_carriers.py`: `f2bce5f5a3d5c1182a9bf80c22a799b110bbc37fcae20a9867a393360a2c61cc`

Evidence: B `_runs/spec-plan-20261009/u2b/` and maintainer workspace
`_runs/reviews/triad-auth-carriers-20261009-r3/`. The two retained U2a engine cases now execute capacity
stderr with Gemini raw exit41 and a timed-out child exiting41 on SIGTERM.

Bounded disposition: DL-75 and DL-95 implemented in this candidate; DL-92's raw
authentication phrase removal implemented, its remaining per-CLI non-auth lists
still OPEN. Child-environment parity, generic exception/record guarantees,
extension validation, other error carriers and complete C37/C43 remain pending.
The previously disclosed Gemini derived-error fallback observation remains a
nonblocking unmeasured exit-zero shape; revisit during classifier cleanup or on
measured evidence, without inventing a parser carrier.

R3 also retained two existing nonblocking gaps: formal Claude empty-answer
permission-denial summaries still feed reflected tool_input to non-auth lists
(the pre-U2b fallback behaves the same), and a sanitized typed extension code
mapped to oauth-env does not get the built-in code's timeout/signal precedence.
Track the former with non-auth/reflected-input cleanup and the latter with DL-97.
The leader reproduced all three Minor observations with isolated direct helper
calls and mocked capture, source unchanged and zero provider calls. These are
constructed controls, not vendor captures. C74's B Claude evidence covers the
is_error=true result path; it does not certify every permission-denial path.

A source2f91e8c was inspected read-only; C74 helper/driver verification was
requested through PR13. A runtime result remains NOT RUN and maintainer response
pending. The B-only external Claude CLI extraction fix does not apply to A's
native Claude leg. No install, product merge or release is claimed.

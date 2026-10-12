# Vendor responsibility audit — owner redirection

Status: assessment/proposals, not an adopted behavioral amendment.

On 2026-10-11 the owner called the pending work overengineering and asked for
every feature to be reconsidered on the basis that vendor CLIs manage their
execution and handles. B has paused U6b declaration migration and the proposed
U9 diagnostic patch. Existing completed work and evidence are retained.

Basis: B `b6868d8036ebe7fd55d975b896f587c8adb18300`; read-only A
`1de943af4436b3eca2aea903d05c223c8d56f92d`; freshly fetched spec main
`3afc4d7e931e55d601dd74877bdbe65e610a8e59`. B's complete
[feature inventory](https://github.com/codefoundry-io/triad-codex-dispatch/blob/482906e2777adf0301a6b6619df85116037e0af3/docs/status/2026-10-11-vendor-responsibility-audit.md)
is published in documentation-only commit `482906e2777adf0301a6b6619df85116037e0af3`.
Native host internals are excluded.

## Findings and proposed common boundary

- Vendor-owned: agent loop, tool processes, background tasks, native retries,
  settings interpretation and session lifecycle. TRIAD-owned: reviewer choices,
  review objective/diff/worktree, direct invocation observation, result bindings,
  agreement and exact cleanup of its own artifacts.
- R-TERMINAL's reader-thread/process-group wording embeds a mechanism. B's
  `_common._run_once_owned` probes remaining process-group members after normal
  CLI exit and can terminate them. A's `_kill_proc_group` and threaded transport
  also manage groups; A is comparative evidence, not justification for the design.
- Prefer native deadlines and ordinary process supervision. Do not infer a
  universal vendor no-orphan guarantee; the caller still observes/cancels its
  direct invocation. No new process manager or shell/SDK rewrite is selected.
- B raw Claude/Gemini capacity handling can restart the whole CLI after its
  native retries. Assess one call followed by evidence-based leader/repair retry.
  Formal Google/structured Claude have narrower paths; do not attribute a B
  outer capacity loop to AGY.
- Assess stderr mirroring, duplicate audit/run/debug records, repeated source/
  toolkit hashing and capability receipts by actual consumers. Retain review
  identity, schema validation and final integrity; neither vendor JSON nor exit0
  establishes cross-family agreement.
- U6b cleanup design depends on which TRIAD artifacts remain. Do not add a
  general deletion framework or new debug pruner first. Existing ownership
  protections remain until a bounded replacement is decided.

## Primary evidence and limits

[Claude headless](https://code.claude.com/docs/en/headless) documents native
background lifecycle and SIGTERM handling. [AGY headless](https://antigravity.google/docs/cli/headless/)
documents native print timeout and terminal outputs; its
[changelog](https://raw.githubusercontent.com/google-antigravity/antigravity-cli/main/CHANGELOG.md)
records pipe-inheritance fixes, daemon preservation and internal retry behavior.
It also records partial output/exit0 on print timeout, so verdict completeness
must remain checked. [Gemini0.63.0 retry source](https://raw.githubusercontent.com/google-gemini/gemini-cli/v0.63.0/packages/core/src/utils/retry.ts)
confirms native backoff. These do not prove identical cleanup on all versions.
B observed local versions Claude2.1.289/AGY1.3.3/Gemini0.60.0; no live inference
or new cancellation experiment was run for this audit. Gemini is below B's floor.

The earlier DL-88 synthetic failure and completed three-family diagnosis remain
valid evidence about the current wrapper, not proof that its added mechanism
should be maintained. No U9 production fix or new classification is implemented.

## Next decision and cross-host request

First choose the reduced invocation/transport contract; then the necessary
evidence artifacts; finally cleanup. R-TERMINAL, outer retry rules, R-RECEIPT,
repeated R-BIND checks and R-CLEANUP may need bounded amendments. No normative
text or case expectation changes in this note. Significant behavior removal
needs the owner's concrete design decision and applicable independent review.

A should assess the same vendor-versus-host boundary in its common CLI code,
without copying B internals or changing its native leg. Supply an actual missing
review outcome and primary evidence for any additional mechanism retained.
B does not wait for a reply, but neither silence nor this proposal changes the
settled contract. No adoption, merge, installation or release is claimed.

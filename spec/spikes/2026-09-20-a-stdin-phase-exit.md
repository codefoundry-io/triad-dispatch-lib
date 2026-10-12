# A pre-spawn stdin failure exit: rejected finding

A remains read-only at `92c8afd500499d8736afcc28b39a87a4f87fed50`. This record
records leader source verification; no A test or provider was executed and no
A file was modified.

The shared `contracts/exit-tokens.json` phase note requires
`input-delivery-failed` before provider spawn to exit 3, and incomplete delivery
after spawn to exit 65. A's `tests/unit/wrappers/t48-stdin-delivery-fail-closed.sh:92-99`
expects `EXIT_ARG_ERROR` before spawn. A's actual
`3rd-Agent/wrappers/_common.py:2103-2121` already does so: `EXIT_ARG_ERROR` at
2110 and `input-delivery-failed` at 2111. Its post-spawn path at `2269-2274`
retains the separate terminal failure code 65. Source and contract agree.

A read-only subagent mistakenly attributed B's `bin/_common.py:1327-1331`
encoding branch to A. At those line numbers A actually contains classifier
patterns. The root rejected the claim after inspecting both exact paths. No A
correction is supported. This record prevents the mistaken handoff being acted on.

## Claude handoff after B completion

No action requested for A's phase exit. Preserve the existing pre-spawn 3,
post-spawn 65, no-vendor-call assertion and content-free diagnostic. Recheck the
exact path and current source before accepting any future cross-host finding.

B currently reports its own documented stdin delta as `unknown`/1. Do not
silently change B to A's phase vocabulary while performing this A correction.
B's independent C8 work will test its actual map and declared exceptions.

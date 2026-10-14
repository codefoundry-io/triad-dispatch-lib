# B remaining terminal evidence: DL-88

Basis: B ed8b76f plus the unrelated U6a fallback-cleanup candidate. Current
`bin/_common.py` `log` and `run_cli_with_retry` were characterized without
product edits or live provider calls. Existing R-TERMINAL/C1 already requires
a failed diagnostic write to drop that line, not the answer or exit.

An invocation-owned fixture used the actual shared driver with a synthetic
Python child that wrote a completion marker and a valid Gemini-shaped answer.
Control: driver returns exit0 and `retained answer`. Negative: the diagnostic
sink raises BrokenPipeError only on the terminal `[wrapper]` line, after the
child completed. The driver raises and returns no result/answer. The source
hash matched; exact fixture was removed. This is a reproduced driver behavior,
not a real user incident or proof of every wrapper's outer exception behavior.

Evidence: B workspace `_runs/infra/20261010-spec-to-code/u9-stderr-spike.py`
and `.json`, terminal exit0. No actual stderr, provider, auth, user setting or
unrelated file was damaged. No U9 correction or classifier expansion is selected
by this record. Independent diagnosis/current A comparison and the smallest
existing-contract correction remain the next unit's work.

PR12 head0ccc7c1 DL-123..126 separately requires no new B port: plain probes
already conform; A removed its round-wide sibling census/retry guard, simplified
its stream handling and dropped an unused audit copy. Its per-attempt hook
attribution remains A-owned. Those rows do not justify rebuilding that machinery
on B. Current source also does not support reusing the old DL-87 assertion that
a second catchable signal necessarily raises out of B's group cleanup; runtime
verification remains separate from this static observation.

Read-only A refresh: e9960053 (clean) changes only test harness cwd/import paths
since d3906f5, not the relevant runtime. A's current `_common.log` at line901
already drops failed writes, prefers descriptor output and explicitly records
blocking-pipe limits; its no-descriptor harness path catches failed stream
writes. This supports the existing shared result, not blind transplantation of
all A implementation details. B did not execute A or modify its host code.

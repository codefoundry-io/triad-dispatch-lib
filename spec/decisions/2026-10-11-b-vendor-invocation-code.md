# B implementation of the vendor invocation replacement

Source: `ba1b6dcdb61ad6a0202917cb4476427e21433159` on `codex/opus-5-5-default`. Common behavioral authority:
[replacement contract](2026-10-11-vendor-invocation-boundary.md), R-TERMINAL
and C1/C2/C9 at shared877621c/fb7c962/c8812a5. Host evidence is separate from
the normative replacement. No adopted revision, installation, merge or release.

## Observable implementation

The host prepares full exact UTF-8 input, launches the CLI with anonymous streams,
and captures finite output after direct completion without changing inherited
output offsets. It neither waits for descendant EOF nor sweeps vendor descendants.
Timeout/cancellation stops and reaps the direct child with bounded waits. Invalid
capture cannot agree; real vendor/authentication failure priority and result
completeness/bindings remain. Failed human diagnostics drop the line without
replacing the result or later buffered replay. The existing metadata probe shares
these primitives. No native-leg, retry-policy or global-setting change.

The former public-v2/convergence instructions implied group cleanup and waiting
for every vendor writer. A dedicated pre-change scenario chose unnecessary waiting;
after the bounded correction it proceeds for a vendor-only stream holder and waits
for a TRIAD-owned result-writer control. Later descendant writes can keep an anonymous
file alive until descriptors close; they are outside captured evidence.

## Verification

- Original dedicated RED4failed/6passed, corrected mirror assertion separately1failed.
- Initial runtime GREEN238focused/2362full passed,4skipped, four validators.
- R1 all terminal/integrity matched, but NOT_APPROVED for stale shipped instructions.
  All five findings were verified and corrected in one bounded pass.
- Corrected instruction GREEN chose both expected actions.236focused passed;
  full2359passed/4skipped plus one obsolete distribution sentence assertion failed.
  Only that test expectation changed; a fresh full distribution module42passed and
  all four validators/diff check passed. The failed full run is retained, not
  relabelled as an all-green full-suite execution. Runtime/skill bytes stayed fixed.
- R2 was a leader preparation NameError before any provider start; exact stage/cwd
  cleanup completed. R3 fresh complete four-entry review: all SAFE,
  ALL_SELECTED_APPROVED/ROUND_INTEGRITY_OK. No prior verdict carried approval.
- Every executor's pre/post source manifests matched; final review fingerprint
  `534df6c3d82f246dcd990a1110f37ed449cb9451956b9970b0823da189fb9398`.
  Durable evidence under workspace `_runs/infra/20261011-vendor-boundary/` and
  `_runs/reviews/triad-vendor-invocation-20261011-r3/`.
- Native Darwin/arm64/Python3.12.13. Ubuntu not run. Synthetic wrapper behavior
  and one prior real Claude stdin marker are not universal vendor conformance.

## Disclosed nonblocking limits

R3 Claude reported two verified Minor observations; all four entries remained SAFE.
A wrapper started with sys.stderr=None fails on initial logging before provider
launch (provider-free fixture reproduced AttributeError). This absent-sink startup
case is not claimed supported; ordinary failed stream writes are covered. README
cleanup passages retain generic "all writers" wording, whereas the operational
skill and common rule explicitly name TRIAD-owned writers. These are deferred
limits under the owner's bounded substantial-defect review direction, not hidden
fixes, claimed absence of defects, or a request for either host to add machinery.

## Independent host implementation

Read-only A `1de943af4436b3eca2aea903d05c223c8d56f92d` still uses
`3rd-Agent/wrappers/_common.py::_run_once` group cleanup before reader joins
(lines2695-2727); its `log` already drops failed descriptor writes (line907).
These observations are evidence, not design authority or an A defect declaration
while it implements concurrently. A implements the same replacement outcome by its
own mechanism and records its own C1/C2/C9 tests. B's temporary-file details need
not be copied. Do not recreate descendant supervision, stdin-consumption auditing
or a lifecycle manager to satisfy the retired wording. Native legs stay host-owned.

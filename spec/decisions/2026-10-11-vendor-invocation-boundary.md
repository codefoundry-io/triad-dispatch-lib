# Direct vendor invocation boundary — replacement contract

Status: owner approved the recommended input-delivery meaning and implementation
on 2026-10-11. This replaces the draft's former transport prescription through
R-TERMINAL and C1/C2/C9; it is not a host correction request. Host implementation
and verification follow independently. No adopted revision or release changes.

Owner direction (verbatim): "권장 진행 스펙에도 언급 스펙에는 수정을 요규하기보다 새로운 스펙 교체나 지침처럼 넣을것"

## Basis and purpose

B `482906e`, read-only A `1de943af4436b3eca2aea903d05c223c8d56f92d`, shared
`1225d13`; remote main freshly fetched at `3afc4d7e931e55d601dd74877bdbe65e610a8e59`.
The owner's instruction to proceed follows the whole-feature
[responsibility audit](2026-10-11-vendor-responsibility-audit.md).

B `_common._run_once_owned` uses custom PIPE readers/writer, mirrors stderr,
and probes/terminates the saved process group after direct-child exit. Removing
only the sweep leaves reader completion dependent on descendant EOF. A's
`3rd-Agent/wrappers/_common.py` `_kill_proc_group`/`_run_once` has the same
coupling; this is comparative evidence, not a design requirement.

## Selected shared outcome

1. Vendor CLI owns descendants, internal retries/tools and native session cleanup.
   The host supervises its direct invocation and validates the review result.
2. Success requires observed direct-child completion, no local input/capture
   failure, and the existing complete result/schema/binding checks. Exit0 alone
   is not sufficient. No reader-thread or process-group mechanism is prescribed.
3. The host does not sweep or terminate descendants merely because the direct
   CLI exited. On timeout/cancellation it stops and reaps the direct child using
   ordinary bounded termination; no universal no-orphan or remote cancellation
   guarantee. A cancelled review cannot agree even when the child exits0.
4. The final capture ends at the observed direct-child completion. The host need
   not await later descendant writes. Missing/incomplete verdict still fails.
5. Live stderr mirroring is not required. Captured stderr remains available for
   existing classification. Failed best-effort display cannot replace the result.
   Identical records in every possible signal window are not a shared guarantee.

Completion guidance: wait for direct invocations and TRIAD-owned custody/result
writers before final integrity/admission/own cleanup. A vendor child holding only
CLI stream handles adds no completion gate. Such descriptors can keep an anonymous
output file alive; later writes are outside the finite captured result. B's first
unit review found old process-group/all-writers language in shipped skill references;
those instructions must follow this same replacement boundary. This is shared
implementation guidance, not a requirement to add a descendant supervisor.

Selected B mechanism: anonymous invocation-owned temporary files for stdin and
separate stdout/stderr, with ordinary direct-child wait. Snapshot stream sizes
after completion and read without changing the inherited file offset. These are
host implementation details, not new shared wire fields or an agent framework.
The same boundary applies to A's common CLI code; its native leg stays A-owned.

## Input-delivery decision

Approved meaning: `stdin_delivery=complete` means the exact complete UTF-8 input
was prepared and made available to the launched CLI. It does not attest vendor
consumption or understanding. Invalid encoding or failed file preparation prevents
launch. CLI failures remain failures; output validation remains mandatory.

Observable change: if a CLI reads one byte of a large input, closes stdin and
returns a complete success-shaped result, B's current PIPE writer detects a
BrokenPipe and refuses success. File stdin makes all bytes available without
that error; this specific refusal disappears. The current PIPE `complete` also
does not prove semantic consumption, and can succeed when a small unread prompt
fits in the pipe. No installed-vendor incident of false success is claimed.

Rejected alternative: retain PIPE delivery monitoring, and therefore some custom writer
lifecycle or another consumption check. Do not silently add file-offset auditing
or pretend standard `communicate()` preserves the old BrokenPipe observation.
This decision affects C1/C9 and the receipt's meaning, not its field names.

## Evidence and limits

- Python3.12.13, macOS: standard-library experiment with a2MB input succeeded
  through both transports. A finite fixture descendant inherited output handles:
  communicate waited1.548s; file capture returned0.048s after direct-child exit.
  Both standard transports accepted a fixture that closed stdin early and
  printed success-shaped output. This is a local transport characterization,
  not evidence of an actual vendor defect or universal lifecycle behavior.
- One real Claude CLI file-stdin call (`opus`, `xhigh`, Plan Mode, no tool request)
  returned the exact requested marker with exit0. This proves that input path
  for the installed executable, not cancellation, descendant cleanup, large
  vendor input or effective model/effort identity.
- [Python subprocess](https://docs.python.org/3.12/library/subprocess.html#subprocess.Popen.communicate)
  documents EOF collection, memory buffering and timeout behavior.
  [CPython3.12.13](https://raw.githubusercontent.com/python/cpython/v3.12.13/Lib/subprocess.py)
  ignores BrokenPipe in communicate's input handling.
- All three independent diagnoses completed: Google and fresh Codex recommend
  file capture with direct-child supervision; Claude also recommends file capture
  but retaining group termination on timeout. The latter cites the existing
  mechanism rather than a measured vendor need and is not selected under the
  owner's descendant-ownership direction; no universal no-orphan guarantee is
  retained. This disposition does not claim all vendors clean all descendants.
- Claude's requested real file-stdin feasibility probe is satisfied by the marker
  run above. Its suggestion of seek/read on shared output descriptors is replaced
  by offset-independent capture. Existing invalid-UTF-8 rejection stays, so the
  suggested additional owner choice about relaxing it is unnecessary. Google's
  characterization of that test as implementation-only is rejected: capture
  correctness is an observable behavior. These are leader dispositions, not
  formal review admission. The owner has now approved dropping early-close detection.

## Implementation and verification

Amend R-TERMINAL, its R-THREAT summary, C1/C2/C9 and the engine-transport unit
first, recording prior wording as superseded history. C2 covers partial resource
preparation/spawn/capture failure without requiring thread-start machinery.

B changes `_common.py` and its existing diagnostic termination-helper consumer,
updates affected English/Korean/security guidance, and uses dedicated RED/GREEN
plus the required unit review. Verify large exact input/output, inherited-output
descendant preservation, timeout/signal with child exit0, capture error,
nonzero/auth priority, incomplete verdict and wrong-round rejection. Remove only
obsolete mechanism-prescribing fixtures, not observable failure protections.

Outer retry changes, receipt/log consolidation and cleanup reduction remain
separate units. No new global setting, permission override, native-leg change,
installation, merge or release follows from this proposal.

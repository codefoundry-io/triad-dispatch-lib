# B: DL-101 measured network-error carrier

2026-10-10; main3afc4d7, B632f426 plus candidate; read-only A bc8a8a74.
This implements the existing vendor-failure-lines.json row and R-CLASSIFY/C43.

Evidence: the frozen row identifies the network sentence in an ERROR result,
empty response and raw exit1. DL-101 identifies result.error. Current B's
antigravity_wrapper.py:350-368 passes only stderr/status to classify and adds
the terminal error only to diagnostics afterward. Current A's wrapper:135-165
passes typed signals, and _common.py:156 includes the network phrase.

B will pass its parsed result to the existing classifier through an optional
internal argument and recognize this row at the server-capacity rung. It will
not feed all terminal errors into broad phrase matching. Preserve auth STOP,
host timeout, transport failures, strong vendor exit maps, subscription-cap
priority, captured output and diagnostics. No A change or native-leg change.

C43 examples before host code:
- ERROR, response exactly empty, raw1, string result.error containing
  `network issue connecting to the server` on AGY -> server-capacity/64,
  answer withheld; raw stream and exit retained.
- Same phrase in response, tool output, stderr alone, another CLI, an error
  object, another status/exit or a nonempty response does not gain this match.
- Original authentication, host timeout, transport failure, a strong learned
  vendor map or an earlier subscription-cap match keeps its precedence.
- A credits sentence in result.error alone remains unclassified here: its
  runtime carrier is still unmeasured. Stored-record replay uses the wrapper's
  interpreter and must agree without invoking a provider.

Verification plan: tests/test_agy_network_carrier.py plus the affected/full
B suites, fresh dedicated RED/GREEN, four source validators and independent
four-family review. Constructed inputs exercise the recorded contract; no
new vendor failure is claimed. Candidate verification is recorded below.


## B candidate verification

Fresh dedicated RED:3failed/492passed/4skipped (two wrapper positives and stored
record positive); final GREEN495affected/2237full passed,4skipped; four canonical
skill validators passed. macOS26.6.2 arm64,Python3.12.13,pytest9.0.3. Six source/
skill hashes,HEAD/full status and ten preexisting source run logs unchanged;
exact temporary root removed. Constructed contract cases, not a fresh vendor
capture; Ubuntu NOT RUN. B632f426 plus preserved candidate, no revision adoption.

Review triad-agy-network-carrier-20261010-r1: all four SAFE; two nonblocking Claude Minors recorded,
ALL_SELECTED_APPROVED and ROUND_INTEGRITY_OK. Digest
b67d7400603713bd2455d22cc389e3c13e2e56138fc4b9c34ff741400883a024; fingerprint
2b2f132af212afa2107c1666edfec5a9deb11d814f33e90cdac5ec0152a1e831.
Custody exported, exact stage/cwd removed. No install/merge/release. Only DL-101
is completed here; other C43 rows and DL-102 truncation remain separate.

Minor dispositions: a reflected command containing the network substring at
raw1/ERROR/empty response is unmeasured. Existing C74 permission-command examples
do not enter this carrier. Keep the settled substring rather than invent an
anchor or exclusion; reopen on actual relevant evidence. B's pre-existing exit64
legend says after retries although AGY makes one call; its factual wording
correction joins existing U5 documentation alignment. No runtime retry change.

Actual bounded production delta:12 additions/1 deletion (net+11), novel predicate
8 lines; tests+105, public documentation+12. Shared-spec/status/plan evidence is
counted separately. This is a candidate source change, not installed behavior.

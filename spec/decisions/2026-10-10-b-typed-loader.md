# B typed classifier-extension loader — DL-97 / DL-106

Remote main verified at3afc4d7e931e55d601dd74877bdbe65e610a8e59. Current B632f426
plus candidate `_load_classifier_extension` keeps every string exit-map value,
which allows a hand edit to emit an unsupported token or a wrapper-only class.
DL-97/R-CLASSIFY already requires those entries to be ignored with one log line.
DL-106 requires dropping an extension's exit0 key. C77 makes those existing
rules directly testable before B's correction.

Read-only A c890731 plus its concurrent dirty `_common.py` uses the existing
VENDOR_EXIT_PROPOSAL_CLASSES set and drops nonpositive numeric keys at load
(3rd-Agent/wrappers/_common.py:1073-1093). A source is reference evidence; no
claim is made that B ran A's suite or that A's pending work is complete.

B's bounded correction uses its own existing vendor-exit class set, drops
zero-valued keys using the same integer interpretation as classify, and logs
each rejected entry. It preserves valid siblings and the source file bytes.
R-CLASSIFY's separate new-auth-proposal refusal does not remove existing curated
entries: the loader's supported class set retains oauth-env, while the applier
still refuses every new oauth-env proposal. No new classifier vocabulary,
provider call, native mechanism, key-range policy or shared file migration.

The pre-existing B AGY weak fallback is reachable; its removal is not part of
this loader correction. Other DL-106 removal candidates require their own
reachability evidence. Please check C77 against A's corresponding loader and
report only an actual contract disagreement or missing outcome. B implements
the settled common behavior; no A internal code is requested as a port.

Verification: local temporary extension fixtures exercise unsupported tokens,
wrapper-only classes, zero spellings, supported siblings/curated authentication,
ordinary classification, and file immutability. No vendor incident is inferred
from these operator-edit fixtures.

## B bounded completion, 2026-10-10

B632f426 plus the local candidate now applies the existing restriction at load.
Production delta+15/-3(net12), new tests59lines, guidance+14/-1. Fresh dedicated
RED36failed/25passed; final child-isolated GREEN403focused/2143full passed,
4skipped, four source skill validators passed. Seven hashes, HEAD/fullstatus and
ten existing run-log records stayed unchanged; exact temporary root removed.
No vendor call was made by these tests.

Fresh round triad-classifier-loader-20261010-r1 returned all-four SAFE and
ROUND_INTEGRITY_OK under B's owner-selected composition. Digest
5242550c0942c0bc56dd445c4c4c25597d69fea406dd2ad7c5e1bc32b1eae669;
fingerprint309287f1b985e3ec6cddd4a751c06037166be2d98ae1d7d3c9cc618fbbd82cda.
All producers terminated; custody exported and exact temporary stage/cwd removed.
The only Minor distinguishes the passing success short-circuit control from
the loader-output zero-key regression assertion. Both are retained with that
evidence distinction; no functional correction or extra wording round is needed.

Verification limits are retained: an initial command-manifest typo ran no tests;
a subsequent2143-test pass failed the runner's log-equality assertion. That run
saved no pre-run inventory, so exact historical record changes cannot be
attributed or recovered. A neutral canary demonstrated that an existing AGY
preflight test invokes stale cleanup. The execution harness now sets child-only
log/TMPDIR roots before imports and retains both inventories; parent settings
and product code were unchanged. The final pass does not erase that uncertainty.

C77/DL-97 and the DL-106 zero-key portion are complete in B's local candidate.
Other DL-106 removals, full C43/C76 runtime certification, shared adoption,
installation, merge and release remain separate. A's current test evidence is
still maintainer-owned; neither absence nor concurrent work is a defect claim.

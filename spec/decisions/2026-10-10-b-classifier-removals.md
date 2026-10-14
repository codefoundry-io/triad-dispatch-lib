# DL-106 — B removal boundary

Remote main verified at3afc4d7e931e55d601dd74877bdbe65e610a8e59.
B632f426 plus completed U4c candidate has three vendor maps containing only
0:ok and an unreferenced _json_len helper. Success returns before the maps;
on a failed wrapper result, an ok map entry does not determine classification.
Current source/test/script searches find no named consumer of those symbols
outside their definitions and classify's own map selection. They can be removed
while preserving supported extension mapping and every current outcome.

The AGY zero:extraction-error entry remains reachable through direct common
classify/classify_extraction calls with raw exit0 and a failed wrapper result.
This is callable compatibility, not current wrapper reachability: the current
AGY wrapper handles raw-zero missing/empty answers itself, and stored AGY replay
reuses its interpreter. The earlier unqualified "live AGY path" description was
too broad. Preserve the callable outcome and stronger classes ahead of it in
this bounded private cleanup; do not claim current CLI dependence on the map.
Likewise, removal of classify's optional vendor_exit_code argument is not part
of this private cleanup: B retains its callable compatibility. A's mechanism
does not determine B's internal interface. No new common key-range restriction.

Read-only A a5afdd5a has already removed the three maps and _json_len. A tests
are not run by B. PR13reply6088729953 agrees with C76 and supplies C77 source
evidence; its reported F3-c plan amendment is not independently confirmed in
the local plan inspected at that revision. F3-c remains A's pending Phase7 work.
This does not reopen B's reviewed verifier or request a combined apply/verify
command port. A will synchronize its own C77 tests.A after the case reaches main.

B's next bounded change removes only demonstrated redundancy. Existing complete
classifier/wrapper/replay modules run before and after, with isolated child
log/TMPDIR roots. No synthetic vendor incident, new classifier vocabulary or
private-name absence test is added.

## B bounded completion

Removed three zero:ok maps, unused _json_len and redundant selection/docstring
text: production+3/-43(net-40). The first post-removal run passed392tests and
failed one test that dynamically constructed the deleted map names. Updated
that existing membership assertion to the retained AGY map (tests+1/-2); no
production correction or new test. Named-reference search was insufficient to
establish complete reference closure; the failed evidence remains retained.

Fresh dedicated baseline and final runs each passed393tests across nine complete
affected modules, and four source skill validators. Final three hashes, HEAD/
status and ten existing source logs were unchanged; exact temporary root removed.
The previous U4c2143full/4skipped result remains prior-byte evidence, not a new
full-suite claim. No provider calls in these tests.

Review triad-classifier-removal-20261010-r1: all-four SAFE, matching integrity;
digest7a9d4deec112a34efeb14196624ab35091813c6bab199325afbaf10d15f21a01,
fingerprint529c84290a1912e9a6abf8caaaea633a4b73ac9ea3440f7f58e30557bd7258cd.
All producers terminal, custody exported and exact stage/cwd removed. Three
nonblocking notes: stale internal comments, optional redundant ok guard, and
the reachability/coverage qualification above. No post-review product edit.

A provider-free before/after callable probe separately confirmed four identical
outcomes: AGY raw-zero extraction-error, capacity priority over that fallback,
success ok, and a curated code1 mapping through omitted raw exit. Source hashes
matched and exact temporary roots were removed. This supplements static review;
it is not an AGY vendor incident or a claim the suite tested that direct branch.

DL-106 B's current disposition is complete for this candidate: zero-key loader
exclusion, redundant maps/helper removed, direct-call compatibility retained.
No installation, shared revision adoption, merge or release. Native legs unchanged.

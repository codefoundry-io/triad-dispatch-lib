# Measurements at the library main `dac1af62` (2026-10-15, claude host)

Same harness as the parent folder, re-run against the PR #7 merge (`dac1af62297402a0078a616e8e194c7a69cafe18`, `0.1.0.dev4`) with the claude host's own bytes (host branch `impl/claude-host-2026-10`; the host files are unchanged since the parent record — same SHA-256 as `../input-identities.md`; the working-copy roster override is the same round override, hash `1f558d4b3666c82c342bab582627f4b8ea13e38df5883be40fbd22ad103f4a97`). Two new probes: S2'' (text AND ordered manifest of `render_review_clauses(with_manifest=True)` versus the host renderer) and S5 (`merge_roster` + `validate_resolved` versus the host merge). The library's own suite at this revision: `outputs/lib-tests.out`.

| probe | command | result |
|---|---|---|
| S2' | `scripts/s2b_compare.py` on a bundle rebuilt from the host bytes at dac1af62 | profiles=24 identical=24 different=0 |
| S2'' | `scripts/s2pp_manifest.py` (same bundle) | S2'' profiles=24 text+manifest identical=24 different=0 |
| S3' | `scripts/s3_verdict.py` | case                               A       A class          lib     lib code           same |
| S4' | `scripts/s4b_roster.py` | merged legs byte-identical (json, sorted keys): True |
| S5 | `scripts/s5_merge.py <host skill> <override>` | S5 merge_roster legs == host _merge_leg legs (sorted JSON): True |
| lib tests | `pytest tests spec/tests` at dac1af62 | 1020 passed in 53.04s |

Limits as in the parent README: print-based probes with the host's assets substituted into the bundle for S2'/S2''; S3' compares decisions, not reason text; S4'/S5 compare sorted-JSON merged legs and check the override `_comment`; the host branch stays unpublished.

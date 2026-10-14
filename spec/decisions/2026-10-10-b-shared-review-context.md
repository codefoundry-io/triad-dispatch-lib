# B shared v2 review context — U5a

2026-10-10, B179c7af plus bounded candidate; exact shared payloads copied from
ca3d990a107b24644fddcf6978a9655f8e106d4f, source manifest/hash checks retained.

DL-45: both web/no-web clauses are rendered from the common clause file. A-only
clauses are excluded through their header marker, not a historical name list.
The legacy renderer also consumes this shared helper for both web policies; permission
flags and authorization/digest controls retain their existing behavior.
DL-46: UTC preparation date is captured once inside the existing hashed basis;
all render/retry paths use that date. Date changes fail existing custody checks.
DL-56/93: all v2 legs receive the exact shared deployment/measured-shape context.
DL-61: public v2 guidance says to collect again before relying on AGREED when an
earlier retried leg may still be running. No new synchronization is claimed.

Native spawn/model/effort, explicit web authorization, wrapper containment and
public result schema remain unchanged. This is candidate prompt integration,
not adopted SPEC_REVISION, installation, merge or release. U5's standing-web
policy assessment (DL-39) stays separate; no native-leg port follows.

Read-only A7dbba148b75cda907f2609731c8b68d2936595ca corroborates date capture at
.claude/skills/triad-cross-family-review/lib/review_scratch.py:1952 and reuse
at:2739; lib/prompts_v2.py:399-427 validates date, resolves common web clauses
and applies host markers. A tests were not rerun. A's hook/raw-reply behavior
remains its own implementation; this unit requests no A code change.

Fresh dedicated RED9failed/288passed/4skipped. Fresh GREEN-r3 297 affected
passed,4skipped; four source skill validators passed. Full GREEN-r2 previously
passed 2273 tests,4 skipped on identical production/docs. Only the
clock fixture test differs afterward; source hashes confirm this boundary.
Initial GREEN retained six stale literal assertions (291passed/4skipped); their
expectations now independently extract the pinned shared clause. No production
change was made for that test-only correction.
macOS26.6.2 arm64/Python3.12.13/pytest9.0.3; Ubuntu NOT RUN. Seventeen source/skill
hashes,HEAD/full status and preexisting source logs unchanged; exact fixture
removed. Tests exercise real renderer/basis/retry/collector behavior with vendor
execution replaced, not live model-choice claims or a wording-quality benchmark.

Review triad-shared-review-context-20261010-r3: all four selected independent
reviewers SAFE, matching ROUND_INTEGRITY_OK. Digest 67725e8bd8b65a2c65af526dc40bcadd47391aa72b7aeb5cea632360b598a158.
R1 was NOT_APPROVED: a stale review-web reference, dead no-web constant and
missing upstream-byte evidence were verified. The reference now describes both
legacy/v2 shared policies and existing uncertainty routing; the unused constant
was removed. R2 binds git-show hashes and byte equality of all four payloads at
the upstream commit. No R1 approval is reused. Default web authorization is still
false; the legacy default clause wording/hash changes with the shared payload.
R2 then found the clock-dependent test: UTC2026-10-11 made the replacement equal
to the original. An actual injected-clock probe reproduced one failure; setting
the existing PreparationClock and asserting changed value fixes it (same probe
one pass). Production/docs were unchanged. R3 is a complete fresh review; no
R2 approval is reused. Its optional parser refactor is not a required change.
Findings and dispositions retained in the round adjudication. Custody exported
and exact temporary launcher stage/cwd removed. Earlier U3 tests/reviews remain
their own evidence; the new result does not certify all C19/C32/C60/C67/C68 axes.

R3 retained two nonblocking source-supported observations: a damaged prompt
bundle on legacy default rendering may fail closed with traceback/exit1 instead
of the handled exit2 diagnostic (no damaged-install runtime probe); the public
mechanical-fields table omits the prepared-date explanation, while runtime/retry
behavior is correct. Both reviewers and leader keep them nonblocking under the
owner three-pass bound. No fourth prompt round or new required backlog is added.

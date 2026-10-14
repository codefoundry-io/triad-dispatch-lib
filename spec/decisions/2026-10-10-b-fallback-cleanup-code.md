# B fallback IPC cleanup implementation: U6a

Source `a4fd93c6283349df67bdb5c4d718a52144ac4547` is pushed and matched to the remote source branch. This closes
the bounded fallback part of R-CLEANUP/C4/C5, not U6b/DL-77/C69 declarations.

The actual fallback writer preserves its usable IPC before publishing an exact
directory allocation record. Sweeping requires that proof and its age; old
unmarked residue stays. A complete deletion-start inventory survives stops and
only unchanged remaining entries are removed. The existing proof descriptor is
held under a nonblocking lock from before reading through cleanup, so another
ordinary sweep skips instead of replacing the durable start. Proof is last.
Own-call failed writes remove only their own empty new folder. Provider output
and failure classification remain unchanged; no new public cleanup API/service.

Final dedicated GREEN-concurrent:340 affected tests,29/29 standalone,2347 full
passed/4 skipped in410.97s, four validators. Captured source/Git/log integrity
matched and exact fixture was removed. macOS/Python3.12.13; Ubuntu NOT RUN.
Provider-free synthetic behavior, not a real user-data-loss incident.

Fresh `triad-fallback-ownership-20261010-r3`: all four selected reviewers SAFE,
ALL_SELECTED_APPROVED / ROUND_INTEGRITY_OK. Digest
`86946b322d791475674fc8679ca06255dd371f3f85e6f6f95db71db6812f6a25`. Adjudication, custody export and exact stage/cwd
cleanup completed. R1/R2 evidence remains; R2's NOT_APPROVED and the first
ineffective concurrency regression are retained. No prior approval was reused.
The corrected overlap regression first reproduced1failed/18passed before code.

Production+160/-19,net141,one file. The new focused test file is304lines;
existing log-test isolation and README EN/KO are included. Normal log caps,
review-packet export/custody, both native legs and user settings are unchanged.
No whole-task completion, installation, adopted revision, merge or release.

Remaining: U6b log-folder proof/declaration mapping, U7's explicit owner design
choice, U9's measured terminal questions and final reconciliation. U8 and unused
Claude-agent work stay withdrawn. Whole-task hook remains until completion.

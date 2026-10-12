# DL-91 — B retired task engine disposition

Shared main fetched at3afc4d7e931e55d601dd74877bdbe65e610a8e59, 2026-10-10.
DL-91 already authorizes removing task/fanout tokens and exits while retaining
Claude permission-denial task-blocked65. This note implements that settled rule;
it introduces no new token, interface, provider behavior or native-leg policy.

B632f426 plus the current candidate still carries fanout-spawn-error in its
classifier, repair registries and replay promotion. Its phrases can still emit
the retired token, so not every deletion is unreachable code. Remove those
memberships and exits68/69. The existing generic unknown result remains for a
failure with no supported diagnosis; do not invent a replacement error class.
Old extension pattern lists for retired fanout are ignored, and new proposals
for that retired class are refused. Valid entries remain effective.

B's production run_cli_with_retry callers are Claude and Gemini wrappers.
There is no B Codex CLI wrapper; native Codex dispatch is independent. Source,
test and script reference inspection finds no consumer of extract_codex_fanout
or extract_implementer_status and only the unused Codex retry arm calls
extract_codex_answer. Remove those extractors/status regex and that arm. Keep
the generic retry callable's parameters, existing wrappers, Claude task-blocked65,
shared locking and historical report-directory cleanup unchanged.

Read-only A3bb4f284 has already removed fanout support. Its active Codex CLI
answer extractor remains, correctly for that host. No A code change is requested;
please flag a concrete B consumer missed by this disposition. A runtime is NOT RUN.

B will refresh its C8 test fixture from exact shared-main token-table bytes,
with the original fixture preserved in pre-unit evidence. That is not whole
shared-revision adoption. Before code, fresh RED will show retired phrase/proposal
behavior and table membership; GREEN covers existing Claude permission denial,
classifier/wrapper/replay behavior, full regressions and four source validators.
No synthetic vendor incident, provider inference or prompt wording change is needed.

## B local candidate completion

Removed the inventoried task/fanout engine pieces: production+7/-189(net-182),
tests+42/-1, fixture/docs+9/-14. Retry signature, Claude task-blocked65, active
wrappers, native dispatch, locking and historical cleanup remain. The retired
names now occur only in negative controls/historical contract explanations.

Fresh dedicated RED12failed/443passed. Final affected suite: 455 passed in 13.95s.
Full suite: 2152 passed, 4 skipped in 411.46s (0:06:51). Four source skill validators passed on macOS/Python3.12.13.
Seven hashes/HEAD/full status and ten source logs unchanged; exact temporary
fixtures removed. Other-platform execution NOT RUN. Synthetic test phrases
are contract controls, not newly observed vendor failures.

Review triad-retired-task-20261010-r1: all four SAFE, matching integrity;
digest 25a3086321541c0271b967e5d6bd00178e40fbb4727f13aeead3a34ccf6bc486,
fingerprint 293bf2e586dd096b7341af91c41681a70b5176cd2a04a1128547a07e945487aa.
All producers terminal, custody exported and exact stage/cwd removed. Findings
and dispositions are retained in the round evidence; no whole-task, install,
merge, release or shared-revision adoption claim. DL-91 B is complete in this
local candidate; DL-119's prior B correction does not need duplicate work.

One verified Minor remains: retry/extraction and historical-cleanup comments
still describe removed Codex paths, and the unused retained last_msg_path
parameter needs a compatibility note. Runtime and the agreed signature are
correct. This is recorded comment debt, not a new implementation or review loop.

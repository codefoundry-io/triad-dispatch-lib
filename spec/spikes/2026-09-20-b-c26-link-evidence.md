# B scoped symlink evidence adaptation

Status: bounded C26/R-PREPARE source `f08e1e8` admitted by `triad-b-c26-r1`,
all four SAFE; [B PR 33](https://github.com/codefoundry-io/triad-codex-dispatch/pull/33).
No installation or OS-level runtime confinement claim. Shared origin/main freshly fetched at
`2eb883fee59e66556ee7c7f87189b38231136622`; B baseline
`14daa4da3755db5d5a70f203deb6b94bb5233e1b`.
PR 33 merged after Analyze (python)/CodeQL passed. B development HEAD, fetched
origin/main and live remote main matched
`51f8bfe6bd73fae525e546c83f3e53a9cceed19c`; the development tree is clean.

## Basis, current behavior and smallest adaptation

C26 requires link path, kind and exact link text to be fingerprinted and visible,
without implicit target reads. B already binds HEAD/index/diffs and untracked
link text, rejects symlinks during prepared copying and has no-follow cleanup
tests. A digest alone does not deliver link text to reviewers, especially an
unchanged tracked link that never appears in the diff. A path can also pass
through a symlink ancestor, so a leaf-only instruction is incomplete.

Use the existing leader-authored TASK and its current common-digest binding.
Record scoped link evidence before fingerprint capture, distinguishing HEAD,
index and working tree, absent/type-change states and exact JSON-escaped link
text. Inspect only explicit approved paths; do not parse approved-boundary prose
as a machine path grammar or enumerate the entire repository for a reviewer.
The common guarded renderer directs every family to these records, forbids
implicit link/ancestor traversal and discloses missing coverage. Independently
authorized target evidence is bound separately, never obtained by following the
link automatically. No new collector, schema, hook or review pipeline.

Preserve prepared-directory refusal, captured-fingerprint reuse, final integrity,
raw investigations, current providers and cleanup behavior. Instructions are a
prompt-controlled reviewer restriction, not a claim of OS-level path confinement.

## A comparison and handoff

A checked at `92c8afd500499d8736afcc28b39a87a4f87fed50`.
`.claude/skills/triad-cross-family-review/lib/review_scratch.py:1780-1787`
documents refusal of untracked symlinks; its inventory begins at `:1795-1797`.
Keep that safe refusal until A implements its own C26 admission and evidence.
Do not remove it just because B can fingerprint link text. The shared R-PREPARE
already calls for A to materialize text or prove no-follow through read audit.

Claude leader: at the B-completion handoff, review this containing commit and
B's final source/gate evidence. Check unchanged tracked links, staged/unstaged
differences, deleted/dangling links, symlink ancestors and escaped untrusted link
text. Preserve A's provider-native read audit and exact cleanup. Implement and
test A's own mechanism before changing its current refusal; B does not edit A.

## Verification plan

Fresh Terra/high provider-free preparation scenario plus deterministic contract,
TASK-digest and tracked-link fingerprint tests. Retain existing untracked-link,
prepared-copy refusal and cleanup tests. Full macOS/Ubuntu 24.04 regressions,
skill validation, lifecycle/cleanup, then a fresh complete required multi-family
round over identical current bytes. Pending checks remain pending.

Implementation: six common guarded-renderer string lines, a scoped TASK section
in the existing reference, a short SOT pointer and concise English/Korean/security
notes. No collector or new public interface. Fresh dedicated RED observed five
missing-contract failures and two preservation passes. An initial test task's
ambiguous metadata-only restriction excluded stored link text; that observation
is not evidence of a SOT behavioral defect. A separate fresh corrected-task RED
already prepared the link states safely against the baseline, while the explicit
source contracts remained absent. The patch codifies that behavior, not a claimed
runtime exploit.

Separate fresh GREEN covers unchanged tracked, staged/unstaged, deleted and
dangling links plus a symlink ancestor, with escaped link text and explicit target
coverage limitations. macOS 1201 passed; Ubuntu 24.04 1199 passed, 2 filesystem
skips; both validators and fixed provider-free lifecycle succeeded, exact owned
cleanup and source identity preserved. Fingerprint:
`cf147529d18a43b5547ad53b7c32f544d54fd1b491c7b5098acfc059490a6c95`.
Shared origin/main refreshed before formal review and remains the stated SHA.
Complete formal round `triad-b-c26-r1` returned SAFE from Claude opus/xhigh,
AGY Pro/high, AGY Flash/high and fresh native Terra/xhigh, no open questions.
Digest `513a23fe654cd4c4efe92dd39805708c69d38df6f4a63ad029bf73eababe8ad0`;
final fingerprint matched; ledger ADMITTED_SAFE. All producer terminals were
consumed, exact custody export hashes matched and all three owned roots were
removed. No reviewed bytes changed after that verdict.

Claude retained two Minor suggestions, source-verified by the leader: the new
section's Contents position differs from body order, with valid anchors; and the
renderer is stricter than the reference's final necessity qualifier when approved
link evidence is missing. The reference already requires each approved link's
record, and the renderer fails closed, so neither permits implicit target reads
or false coverage. The wording can cause an avoidable NOT-SAFE for an irrelevant
missing record; retain that operational cost and the alignment suggestion.
Do not describe either suggestion as fixed in this unchanged admitted source.

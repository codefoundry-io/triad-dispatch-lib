# B P2: allocation and evidence custody before cleanup

Status: implemented and full-scope review admitted; integration is tracked by
[B PR 28](https://github.com/codefoundry-io/triad-codex-dispatch/pull/28).
Source commit: `a85a8006c671da94c5a4f7c49a3c9e0acb12cc5c`. PR 28 merged as
`26ef666886305b5c352b6b508fa84e0608713139`; remote main equality and both CodeQL
checks were verified. No deployment.
Shared remote main fetched at this boundary: `2eb883fee59e66556ee7c7f87189b38231136622`.
B basis: merged P1 `a9e5b84b53f6b5db841b3b9fe81591dc2d1fd0a7`, branch
`codex/host-parity-p2-cleanup`. A inspected read-only at
`92c8afd500499d8736afcc28b39a87a4f87fed50`; no A edits.

## Evidence and existing contract

Existing C4/C5/C7 and R-CLEANUP require proven allocation and verified evidence
export before deletion, preservation of uncertain residue and idempotent cleanup.
Fresh dedicated Terra/high, fork-none RED reproduced four failures on unchanged
B source: same-UID foreign roots with/without a plausible activity marker were
deleted, allocated unexported evidence was deleted, and stale sweeping removed
unexported allocations. Terminal result: 4 failed, 12 deselected. Exact fixture
cleanup and pre/post source hashes are in the owner's
`_runs/infra/20260920-triad-p2/red-executor/` evidence directory.

Python 3.12 [rename](https://docs.python.org/3.12/library/os.html#os.rename)
can replace an empty destination directory on Unix. Its atomic namespace move
is not exclusive claim creation. [rmtree](https://docs.python.org/3.12/library/shutil.html#shutil.rmtree)
provides supported-platform symlink resistance, not allocation provenance or
export custody. These are local filesystem facts, not provider inference.

## B implementation and preservation boundary

The existing lifecycle helper adds private external allocation/export/claim
records and one export subcommand. It retains regular bytes, empty-directory
facts and literal link targets at a caller-selected durable destination outside
managed roots, then verifies copied evidence and original inventory. Cleanup
rechecks both, exclusively creates a private claim container, moves the root
into its reserved child and revalidates identity/inventory before deletion.
Partial deletion resumes only from the same proven claim and retained export.

Preserved: exact expected-root checks, source-copy no-follow guards, current
prepare/worktree routes, strict 30-day eligibility, requested-ID collision,
UID/type guards, external link targets, disappearance handling and propagation
of actual removal failures. Unknown or unexported residue is retained/reported.
One leader per allocation and terminal writers are preconditions; no malicious
same-UID forgery or open-FD concurrency containment is claimed. No registry,
daemon, capability, public permission bypass or host adoption is added.

The provider-free verifier embeds the actual small synthetic artifact bytes,
link facts and manifest in its report before disposing of its own fixtures.
If report retention fails, it preserves the fixture. This isolated test-fixture
fallback is not a production cleanup bypass.

## A line-level handoff

All paths below are in A `.claude/skills/triad-cross-family-review/lib/review_scratch.py`.

| Lines | Current behavior | Necessary follow-up after B handoff |
|---|---|---|
| 668–705 | `.active` fixed magic bytes are treated as minted ownership; no original inode/allocation binding | Preserve marker checks but require a provable allocation association before deletion; a plausible marker alone is insufficient under C4. |
| 720–732 | Any date-prefixed `.pruning` directory is reclaimed by name, without a surviving claim record | Preserve unknown claims. Resume only an allocation-bound claim whose external evidence export is verified. |
| 849–864 | Stale deletion renames to a predictable sibling then removes it; no exclusive destination proof or external export verification | Preserve eligible stale cleanup with proven allocation/export and an exclusive claim destination; do not copy name-only claim reclamation into B. |
| 995–1068, 1069–1082 | Close can proceed when the worktree is absent, warns about unverified evidence, then renames/deletes the packet | A warning is not export custody. Refuse destruction until evidence has been retained and verified. |
| 380–392, 757–848, 936–994 | Actual Git worktree registration checks and guarded detach/close protect registered trees | Preserve these A-specific guards. B's plain review-root adaptation does not replace them. |

A's maintainer should review the final B commit and these cases, then implement
the smallest A-specific equivalent. Do not mechanically copy B's filenames or
remove A worktree registration defenses. The owner has designated B to complete
first; this document does not request an A code change now.

## Verification and sharing

Separate fresh Terra/high RED/GREEN reproduced and fixed unsafe deletion and
failure-custody cases. Final focused custody: 36 passed. Full macOS: 1081 passed;
Ubuntu 24.04.4: 1079 passed, 2 case-insensitive-filesystem skips. Skill validator
and retained provider-free lifecycle passed; 179-file pre/post source inventory
matched. Actual synthetic artifacts and generated files were retained before
exact fixture cleanup. Initial invalid hash capture and an unretained extra
verifier invocation were recorded and excluded from the proof.

Round `triad-b-p2-r2` returned SAFE from Claude Opus/xhigh, Google Pro/high,
Google Flash/high and fresh Codex Terra/xhigh. Final fingerprint matched and
the canonical workspace ledger admitted SAFE. Round-owned custody bytes were
exported before exact temporary-root cleanup. Original findings claude-03,
google-01 and codex-03 are closed by this unchanged basis.

Non-blocking observations remain visible: avoid unmeasured traversal refactoring;
consider checking eligible age before expensive hashing while preserving recent
refusal diagnostics; add an explicit recovery example for an empty claim
container without a claim record if operational need arises. The existing rule
preserves unproven residue for owner inspection, never automatic adoption.
These Minor observations were not claimed fixed or used to conceal blockers.
V1–V5, shared revision adoption and deployment remain separate.

Review request for Claude at the final shared handoff commit: verify C4/C5/C7
preservation and the A source differences above; identify source-backed defects
or the smallest A-specific adaptation. Keep A unchanged until B's final handoff.

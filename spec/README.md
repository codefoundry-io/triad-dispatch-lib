# triad-dispatch-spec — shared specification for the TRIAD dispatch hosts

Shared specification for the two TRIAD dispatch hosts: the Claude-hosted `triad-dispatch` (source of truth `~/triad`) and
the Codex-hosted `triad-codex-dispatch`. This public repository is the owner-published
authoring source. `main` contains the current v2 implementation candidate and
subsequent amendments; rev-0 remains the only published revision tag.
The owner subsequently authorized Codex-host implementation first, using the shared schemas/specification before host
code. See `reference/spec-authoring.md#R-AUTHORING-SYNC` and `decisions/rev-2-implementation-spec.md`. This does not
authorize Claude-host edits, silently change a deployed revision, or create a tag.

**What this repository is (owner Q-V, verbatim):** "UI 요소가 없는 실험적 시도로 컨셉만 잡아서 Likec4 없이 스펙저장소를
가벼운 실험소처럼 쓰자" — a lightweight experiment lab for writing specs and accumulating behavioral cases. Concept level.
No UI, no LikeC4, no generated documentation, no cross-host release federation. Both hosts stay independently owned and
released; each host records the revision of this repository it conforms to.

## Layout

```
triad-dispatch-spec/
├── README.md                      this file: purpose, layout, how a host adopts a revision
├── AGENTS.md                      identical link map for Codex, Claude and Gemini
├── CLAUDE.md                      identical link map
├── GEMINI.md                      identical link map
├── authoring/                     PRD/Spec reference schema, guide and registered bundles
├── reference/                     common guidance, written ONCE — every host doc points here
│   ├── README.md                  index + the one-source-per-fact table
│   ├── spec-authoring.md          HOW specs are written in this lab (the method)
│   ├── review-rules.md            agreement, correction re-review, roster, Google leg, smell criterion, containment, no-cost
│   └── process.md                 the shared flow (one diagram) + the failure-diagnosis rules
├── prompts/                       review prompt text — the ONE editable copy (owner Q-U); hosts vendor at the adopted revision
├── contracts/                     machine-readable contracts (schemas, token tables, policy files)
├── cases/cases.json               behavioral cases with stable ids — the accumulating test asset
├── units.json                     surface → common shipped name → contract → preserved host exceptions → host paths
├── tests/test_schemas.py           provider-free canonical schema examples (python-jsonschema)
├── tools/check_authoring.py        offline PRD/Spec reference validation
├── requirements-dev.txt           authoring test dependencies
├── decisions/owner-register.md    owner rulings and their effect (site-neutral; verbatim record stays in the host plan)
└── CHANGELOG.md                   one entry per revision
```

## How a host uses a revision

1. A revision is a git tag `rev-N` on `main`. The owner tags it after the other leader has read the handed folder and its `CHANGELOG.md` entry (owner Q-T); no signature ceremony.
2. Each host repository records the revision it conforms to in one file (`SPEC_REVISION`, one line: `rev-N` + the tag's commit). The host vendors `reference/`, `prompts/*.md` and the `contracts/` files it consumes at that revision with the payload bytes UNCHANGED, recording revision and source digest in an adjacent small manifest (never inside the file — JSON has no comment syntax and byte equality is the check), so the adopted rules are available offline at the pinned revision; a live main-branch URL never changes installed behavior. It runs the `cases/` its `units.json` row maps to its own tests.
   A host that conforms to an untagged commit records that commit as a candidate, never as a revision. On A:
   `SPEC_REVISION:1` holds one line `candidate <commit> <repository> (branch <the branch the commit is on>[, <its
   publication state>]; <a note on adoption>; manifest: <path of the adjacent manifest>)` — at triad `faeb86b`, verbatim:

   ```
   candidate 1f907af552f848d3dc6175084297a98100eacd35 codefoundry-io/triad-dispatch-spec (branch claude/review-legs-astra-web, unpublished; re-vendored after the owner merges; manifest: .claude/skills/triad-cross-family-review/spec/SPEC_MANIFEST.json)
   ```

   On B: there is no `SPEC_REVISION` file; vendored payloads carry their own manifests
   (`source_commit`, `status: candidate`) — five manifest files over three spec commits:
   `prompts/review-v2/source-manifest.json` and `contracts/source-manifest.json` at `04245c7` (checked in code),
   `bin/policies/source-manifest.json` (gemini no-web policy) at `6f0f274` and `bin/policies/web-source-manifest.json`
   (gemini web policy) at `7f527ef` (both checked in code), and `prompts/source-manifest.json` (`investigation.md`) at
   `6f0f274`, checked only by B's distribution verifier and tests — a recorded departure from one revision
   (`authoring/shared-dev-log.md` DL-47).
3. A host may lag a revision. Drift BETWEEN hosts is a REPORT (which revision each conforms to), not a release block (owner Q-P settled the location, not the enforcement mode). A host's failed required check against the revision it ITSELF claims is a local defect of that host.
4. Authoring vs publication: either leader AUTHORS amendments here (a folder mirroring this layout, read by the other leader); only the OWNER publishes — pushes and tags. A review request or an attached maintainer instruction is never blanket authority to push or tag. Decisions that need the owner are asked in advance; the ruling and its effect land in `decisions/owner-register.md`.

## Reading order

Start at [the common map](reference/README.md), then load the linked sources
needed for the current task. For PRD/Spec edits, use
[the authoring guide](authoring/README.md) and
[the current Claude v2 bundle](authoring/maps/claude-host-v2.json).

Verify before handoff: `python3 tools/check_authoring.py`, then
`python3 -m pytest -q tests` (dependencies: `requirements-dev.txt`).

Historical 2026-09-21 operating profile (topology and setup context):
[Codex + three Google legs: historical agreement](decisions/2026-09-21-codex-google-four-leg-agreement.md),
[operating specification](decisions/codex-google-four-leg-operating-spec.md), and
[historical Claude handoff](decisions/claude-codex-google-four-leg-handoff.md).
Its family-count approval condition and per-leg review emphases are superseded by the current strategy.

Current review-strategy amendment (candidate, host adoption pending):
[2026-10-02 direction, evidence and verification](decisions/2026-10-02-review-strategy.md); its review-web and
codex-default preservation sentences are superseded by the
[2026-10-03 review-legs decision](decisions/owner-register.md#D-REVIEW-LEGS-20261003).
It updates agreement and default prompting for configurable rosters; the four-leg setup above is an example,
not a minimum count or mandatory set of review personas. Use the
[current Claude implementation handoff](decisions/claude-review-strategy-handoff.md) and normative
[R-AGREE](reference/review-rules.md#R-AGREE), [R-ROSTER](reference/review-rules.md#R-ROSTER) and
[R-PROMPT](reference/review-rules.md#R-PROMPT) for current work.

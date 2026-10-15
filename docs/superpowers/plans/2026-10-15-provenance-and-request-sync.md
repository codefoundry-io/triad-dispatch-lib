# Provenance and request synchronization implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve issue #6 and synchronize current adoption requests and merger facts without changing library or provider behavior.

**Architecture:** Canonical policy comments name this repository; verification hashes follow the new bytes while historical import ancestry remains immutable. Current documentation records both remaining issue #3 requests and the completed PR #2 boundary.

**Tech Stack:** Python 3.12+, TOML policy payloads, existing pytest and native CI.

**Spec:** `spec/MIGRATION.md`, `docs/host-adoption.md`, issues #3 and #6 including requester comments through 2026-10-15T05:53:24Z; owner-approved review recommendation followed by “진행”. This bounded documentation unit has no new runtime/API design.

## Global Constraints

- Policy rule tables, priorities and provider behavior remain unchanged.
- Preserve `spec/import-origin.json`, historical assertions, schema identities and runtime bundle payloads.
- Preserve existing code, error contracts, package version and both hosts' native execution.
- No consumer adoption, publication, issue closure or final merge is implied.
- Git/Python/tests/builds/provider CLIs run through `/bin/zsh -lic` with `sandbox_permissions="require_escalated"`; host cwd is `/Users/chaniri/codex_workspace` before entering this repository.
- Current review profile: required Opus 5.5/xhigh, Sol 6.1/xhigh, Argon/high, separate non-voting Astra/high; 2400 seconds per entry and official-source web research allowed.

## Review Focus

- Comment edits change file digests even when parsed TOML is unchanged.
- Current verification digests must follow edited policies; historical ancestry hashes must not.
- Issue #3's latest missing-required-name request is distinct from the provider-chosen duplicate-name request.
- A merged library revision is not proof of consumer adoption or package publication.
- Withdrawn diagnostic requests and completed review snapshots must retain their historical meaning.

### Task 1: Update canonical provenance and current request records

**Files:**
- Modify: `spec/contracts/gemini-readonly.toml`, `spec/contracts/gemini-readonly-web.toml` (header comments only).
- Modify: their adjacent `*.verify.toml` policy digests and `spec/tests/test_policy_profiles.py` fixed current-payload assertion.
- Modify: `spec/README.md`, `docs/status.md`, `docs/requests/2026-10-15-claude-host-adoption-requests.md`, `docs/host-adoption.md`.

**Interfaces:**
- Consumes: canonical policy bytes and the existing host byte-identity contract.
- Produces: newly pinned comment bytes with identical parsed TOML, accurate current request/merge records; no public Python API changes.

- [ ] Update both policy headers to name `triad-dispatch-lib/spec/contracts/` as current authoring source and preserve byte-for-byte host vendoring. Keep historical policy behavior/evidence comments.
- [ ] Recompute both current `policy_sha256` values. Replace the misleading current-file frozen-import test with a current-policy/manifest identity check; preserve the original import hash as historical evidence. Check the untouched import-origin file against the base Git blob.
- [ ] Correct the spec README's pending-consolidation statement to PR #1 at `9489543ee24f338e9c6d0e3b032a1aa389986429`. Separately record later adoption-observability PR #2 merge `ee8b4b4ab3c1440788733931874047a1821ee08e`, exact reviewed head `830942e05d3681e7ded04a91d60850d18ea00d10`, R5 AGREED and successful main CI run 38690043657 without implying a release or new host adoption.
- [ ] Synchronize current issue #3 descriptions: `.field` and trusted schema `.path` accepted; `.detail`, instance pointers and duplicate pre-pass withdrawn; duplicate `.member` and schema-defined missing-required-name diagnostics remain unimplemented design requests. Link the latest requester comment. Preserve historical slice records.
- [ ] Verify parsed TOML equality to base for both edited policies, current digest equality, unchanged import ancestry and runtime source/assets. Run `uv sync --locked`, `uv run --locked pytest -q`, authoring/assets checks and `git diff --check`. Record commands/results; do not add tests that merely assert wording.
- [ ] Commit only owned files. Have an independent task reviewer check specification compliance and quality. Push a draft PR, obtain native CI and a fresh complete project review before advancing the next implementation plan. Main merge remains a separate owner decision.

## Later units, not executable by this plan

1. Issue #4: specify merge-only and final-validation APIs, preserving the existing `resolve_roster` return/error/copy contracts, then implement with regression vectors.
2. Issue #3: specify trusted missing-required-name diagnostics separately from arbitrary duplicate-name disclosure; settle that disclosure decision before implementation.
3. Issue #5: develop individual L1/L4/L6/L8/L9 boundary proposals; no wholesale relocation or host/provider default changes.

# Release Update PRs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish versioned library artifacts and deliver release-change and library-acquisition guidance through idempotent Codex/Claude update PRs.

**Architecture:** Library-owned GitHub Actions orchestrate verified release assets and a small Python GitHub API client. Generated host notices preserve independent adoption and release authority. Publication and delivery are independently retryable.

**Tech Stack:** Python 3.12+ standard library, existing uv/pytest, GitHub Actions, GitHub App installation token, GitHub REST/Git Data APIs.

**Spec:** `docs/superpowers/specs/2026-10-16-release-update-prs-design.md`

**Resumption (2026-10-16):** The owner resumed this work after PR #13 merged
and requested completion through an AI-readable consumer installation guide.
Reconcile with main `fcc5072` in the existing branch; preserve the pending Task 1
collision regressions. AGY and Claude agents can use the common guide to adopt
the library in their host projects. This does not add a third delivery repository
or authorize changes to host implementations.

## Owner scope correction (2026-10-16)

The owner's subsequent direction supersedes the earlier vendor plugin
installation/update requirement. This plan distributes library wheel/sdist/manifest
assets and tells consumers where/how to obtain and verify them. Consumer projects
own integration and deployment; no plugin/bootstrap/permission/restart or host
rollback instructions belong in generated notices or this release guide. Existing
operator App configuration and publication/retry tooling remain in scope. Prior
implementation evidence remains historical; this correction changes the active
requirements without adding a new plan, feature or framework.

## Global Constraints

- Work on `codex/release-update-prs` in the existing lib checkout; preserve all other worktrees and dirty host files.
- Python/tests/builds/Git mutations/provider CLIs use literal `/bin/zsh -lic` with `sandbox_permissions="require_escalated"`, host cwd `/Users/chaniri/codex_workspace`, then enter the project.
- No new runtime dependency, runtime API/schema change, native host port, auto-merge, local install, secret copying or actual release for testing.
- Two target repos only: `codefoundry-io/triad-codex-dispatch` and `codefoundry-io/triad-dispatch`.
- Published release tags match `v` plus the wheel/package version. Never overwrite a released artifact with different bytes.
- Keep release data out of shell source. Tokens come from environment, never logs/arguments or generated PR content.
- Generated PR files live under `docs/library-updates/<tag>/`; source release identity and pending host adoption are explicit.

## Size and review scope

One cohesive release-delivery plan: expected 400-600 new production/tooling lines,
approximately 300 novel core lines; workflows/config 100-150 lines, tests 250-350,
docs 150-250. Estimate changes when evidence requires it, not as an automatic gate.
Task-level read-only review plus complete project formal review before integration.

Updated estimate after Tasks 1/2/4: 800-1,000 tooling lines (including API I/O,
identity checks, rendering and the bounded archive-normalization helper), about
400 novel core lines, 170-230 workflow lines, 1,050-1,150 test lines and 450-600 doc
lines. The increase covers required branch recovery/immutable retry refusals and
the explicitly requested executable consumer guide, not a new runtime feature.
Record actual additions/deletions at final verification.

## Review Focus

- A network interruption after branch creation must resume without losing edits.
- A closed/merged update PR must not be silently recreated or reopened.
- Missing cross-repo permissions must leave the published release and successful target intact.
- Release notes/tags must not become shell commands or claim unreleased host adoption.
- A wheel with mismatched identity or replaced published assets must fail before target writes.

### Task 1: Validate and describe release artifacts

**Files:** Create `tools/release_artifacts.py`, `tests/test_release_artifacts.py`.

**Interfaces:** `build_manifest(dist: Path, tag: str, source_commit: str, prerelease: bool = False) -> dict`; `validate_manifest(value: dict) -> dict`; `verify_artifact(path: Path, artifact: dict) -> None`. CLI accepts `--dist`, `--tag`, `--source-commit`, `--prerelease`, `--output`. Manifest keys are `schema_version=1`, `name="triad-dispatch-lib"`, `version`, `tag`, `source_commit`, `release_url`, `prerelease`, `artifacts` (each `name`, `size`, `sha256`, `url`). URLs bind to this repository and tag.

- [x] Write tests for wheel METADATA name/version and tag matching, exact wheel+sdist inventory, SHA-256/size and release URLs; reject traversal/unsafe tags, mismatched wheel name/version and invalid commit, and verify tampered artifact refusal. Include valid prerelease and fresh deterministic manifest cases.
- [x] Run `uv run --locked pytest -q tests/test_release_artifacts.py`; confirm RED for absent behavior.
- [x] Implement the stdlib helper and CLI; validate relevant metadata without recreating a full package installer.
- [x] Run focused tests; confirm GREEN. Record actual output and commit only owned files.

### Task 2: Render and deliver update-request PRs

**Files:** Create `tools/release_prs.py`, `tests/test_release_prs.py`.

**Interfaces:** Import `validate_manifest` and `verify_artifact` from Task 1. `render_notice(release: dict, manifest: dict, target: str, previous_version: str | None = None) -> str`; `deliver(api, release: dict, manifest: dict, target: str) -> dict`. CLI accepts `--tag`, optional `--target` (fixed choices), `--dry-run-dir`; reads `GH_TOKEN` for the hosts and `SOURCE_GH_TOKEN` for the library. The latter is the existing workflow token, not a new registered secret. API wrapper exposes `request(method, path, payload=None)` and only talks to GitHub's API; artifact download stays in the same release's approved URLs. The CLI may use `gh api` as a subprocess argument list, never a shell command string. Record the existing version from a target's `contracts/library-adoption.json` when present; absence means unrecorded, not an invented version or proof of no adoption.

- [x] Write rendering tests for both target notices, source notes, hashes, preview/published separation, pending adoption, prerelease marking and library-only acquisition guidance (superseding the prior host-guide requirement).
- [x] Write fake-API tests for create, existing open/closed/merged PR skip, matching branch-only recovery, conflicting branch refusal (including unrelated changes on that branch), no-force update and partial target failure. All cases assert affected paths and absence of writes in dry-run. Include present/absent previous-version records.
- [x] Implement two generated regular files (`release.json`, `README.md`) per release. Use Git Data blob/tree/commit/ref endpoints plus pull requests. Validate release identity and require non-draft published release. Query PRs before creating branch; inspect existing branch files before recovery.
- [x] Confirm RED then GREEN with `uv run --locked pytest -q tests/test_release_prs.py`; record results and commit owned files.

### Task 3: Connect verified releases, credentials and operator documentation

**Files:** Modify `.github/workflows/test.yml`; create `.github/workflows/release.yml`, `tools/publish_release.py`, tests covering publishing/retry, and `docs/releasing.md`; link README/status. Task 4 owns the independent consumer guide.

**Interfaces:** Reuse Task 1 manifest and Task 2 delivery CLI. Reusable test workflow accepts an exact ref and optional release artifact upload, defaulting to existing PR/main behavior. Release workflow verifies ref/version, waits for platform CI, publishes artifacts, then calls delivery for both targets independently using a scoped GitHub App token.

- [x] Test published asset replay: missing assets uploaded, identical existing assets reused, changed bytes/identity refused; incomplete upload resumes safely.
- [x] Normalize sdist archive timestamps/owner metadata deterministically before
  extraction/rebuild and manifest hashing, using the source commit epoch; build
  its wheel with the same `SOURCE_DATE_EPOCH`. A repeat-build probe found plain
  setuptools sdists differed solely from build metadata even with that variable.
  Preserve names, modes and payload bytes; keep exact-byte replay refusal. Record
  backend/compression changes as a reproducibility limit, not a reason to overwrite.
- [x] Add `release: published` and `workflow_dispatch` retry; no push trigger for notifications. Use pinned existing Actions plus `actions/create-github-app-token`, request only two target repositories and Contents/Pull requests write permission. Credential names: variable `TRIAD_RELEASE_APP_ID`, secret `TRIAD_RELEASE_APP_PRIVATE_KEY`.
- [x] Document GitHub App setup, exact release/retry commands, generated PR examples, no-live-delivery dry run, library acquisition links and remaining activation boundary. Do not register secrets automatically.
- [ ] Run focused delivery tests, full `uv run --locked pytest -q`, `uv run --locked python tools/sync_spec_assets.py --check`, `git diff --check`, workflow syntax check when available, and package/source archive checks if new tooling changes package contents.
- [ ] Commit/push the feature branch and create an attached Draft PR; collect native CI and complete formal project review using the existing 2400-second configuration. Report actual activation/credential limits separately from source/test completion.

### Task 4: Give consuming AI agents a complete installation path

**Files:** Create `docs/installing.md`; link it from `docs/host-adoption.md`.
This documentation task may run alongside Task 2: it consumes the completed
Task 1 manifest and existing runtime APIs, not the delivery implementation.
Task 3 owns README/status links and the final integration verification.

- [x] Write an AI-readable host-neutral guide: choose an explicit released tag and
  source commit, download its manifest/wheel, verify identity/size/SHA-256, install
  in an isolated Python >=3.12 environment, check actual installed version/path and
  verified bundle identities. Explain the source-pinned candidate fallback when
  no release exists without calling it a published release.
- [x] Cover library release discovery, wheel/sdist/manifest acquisition and per-platform
  dependency closure. Link public APIs and host-adoption contracts; leave integration,
  native adapters and deployment with consumers. Supersedes the prior host vendoring,
  plugin installation/update/restart and host rollback guidance requirement. No new
  installer, provider catalog or automatic host port.
- [x] Exercise the common install and smoke commands with the candidate wheel in
  a clean temporary environment and record outputs; published download and live
  host adoption remain explicitly unrun. Review documentation against executable
  APIs and library artifact contracts. Commit only owned documents.

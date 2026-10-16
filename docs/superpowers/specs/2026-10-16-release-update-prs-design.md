# Release delivery to independent host repositories

Status: implementation authorized by the owner on 2026-10-16 after the in-chat
release/PR design. Credential setup and the amount of automatic host adoption
remain explicit integration boundaries; neither blocks the release tooling.

## Intended outcome

A published library release produces a wheel/source distribution and opens one
update PR in each of `codefoundry-io/triad-codex-dispatch` and
`codefoundry-io/triad-dispatch`. The PR contains the release changes, artifact
identity, host-specific installation/update guidance, verification boundaries
and rollback guidance. Development builds do not send notifications. A retry
must not duplicate a PR or overwrite a maintainer's changes.

The owner explicitly requested a written plan followed by implementation in this
turn. This authorizes continuing without another design/plan approval exchange.
Meaningful review findings, including Minor findings, remain eligible for fixes.

## Current evidence and ownership

Library base: `dac1af62297402a0078a616e8e194c7a69cafe18`, Python >=3.12,
package `0.1.0.dev4`. Existing CI covers native macOS/Ubuntu and Python 3.12/3.14.
Codex v0.2.561 bundles dev3; its vendor tool restores the existing pin only.
Claude main `e4cadf2f751308d1ab75e4199b08d89849bb93b3` has no shared-library
adoption/pin/update interface. Its plugin is v0.2.1709 and retains host-local
implementations. A release notice cannot claim either host has adopted it.

Keep this change in the library repository. Native execution, host integration,
host release versions and local plugin installation remain independently owned.
The first delivery capability is a release proposal: a per-release Markdown
record plus machine-readable release identity in a target PR. It does not rewrite
native host implementations. A question to the owner distinguishes this from
adding a separate Codex bundle-upgrade mechanism; the latter is not a prerequisite
for publication and notification tooling.

## Components and flow

1. A GitHub Actions `release: published` workflow (and explicit manual retry by
   tag) verifies the tagged package with the existing four-environment CI before
   publishing assets. The tag must equal `v` plus package metadata version.
   Pre-releases are labelled as such, not represented as stable host releases.
2. Build standard wheel and sdist from the reviewed tag. Attach them and
   `triad-release.json` to that GitHub Release. The manifest records version,
   tag, resolved source commit, release URL and artifact filenames/SHA-256/size.
   Previously published assets are reused after verification rather than replaced.
3. Use a GitHub App installation token, limited to the two host repositories,
   with Contents and Pull requests write access. The source `GITHUB_TOKEN`
   publishes library assets; it is not a cross-repository credential. Store only
   App ID as a variable and private key as an Actions secret. Do not copy a
   developer's credential into automation.
4. For each target, render a Markdown notice and release identity under
   `docs/library-updates/<tag>/`. Use the GitHub Git Data API to add only these
   two regular files on `automation/triad-lib/<tag>`, based on the target's current
   default branch. Never execute code from a target checkout.
5. Open a PR with the same Markdown body and a machine marker for repository,
   release ID and target. Existing open/closed/merged PRs for that branch prevent
   duplicate creation. An interrupted branch-only attempt can resume when its
   generated files match; conflicting branch content is preserved and reported.
   Never force push, reopen a declined PR, auto-merge or auto-install.

## PR content

- Source release link, version, source commit and artifact hashes.
- Release notes copied as data; no shell interpolation of notes, tags or titles.
- Host-specific adoption status, impacts requiring review and API documentation.
- Separate pre-merge inspection/testing from post-host-release installation.
- Codex instructions link `docs/installation.md` and name marketplace/plugin
  commands and bootstrap, including the documented removal/reinstall sequence.
- Claude instructions link its README and name plugin install/update and project
  permission refresh. Gemini/AGY setup remains in those host instructions.
- Existing-host release rollback instructions; no promise that library release
  alone changes installed behavior. Pending host CI is reported as pending.

## Failure and retry behavior

Missing credentials prevent only delivery, with actionable setup diagnostics.
Release assets remain available. Process the two targets independently; preserve
successful delivery if the other fails. Re-running by release tag resumes safely.
Unknown release/artifact identities fail before writing a target branch. No
periodic polling service or cross-repository workflow dispatch is needed.

## Verification and completion

Unit tests exercise real rendering and artifact validation; a fake GitHub API
tests PR state transitions and partial failures without contacting real users.
Dry-run mode reads published metadata and writes local previews only. Native CI
checks the new tooling with the existing package suite; formal review retains
Opus/Sol/Argon plus independent Astra, 2400 seconds each and official web access.
No test release or test PR is sent to host repositories merely to exercise the
workflow. A successful dry run is not live delivery evidence. Activation requires
merging the workflow and registering the GitHub App credentials; final merge and
real package publication remain explicit owner-controlled actions.

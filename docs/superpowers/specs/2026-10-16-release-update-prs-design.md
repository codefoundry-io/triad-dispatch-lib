# Release delivery to independent host repositories

Status: implementation authorized by the owner on 2026-10-16 after the in-chat
release/PR design. Credential setup and the amount of automatic host adoption
remain explicit integration boundaries; neither blocks the release tooling.

## Intended outcome

A published library release produces a wheel/source distribution and opens one
update PR in each of `codefoundry-io/triad-codex-dispatch` and
`codefoundry-io/triad-dispatch`. The PR contains the release changes, artifact
identity, library acquisition/verification guidance and consumer ownership
boundaries. Development builds do not send notifications. A retry
must not duplicate a PR or overwrite a maintainer's changes.

The owner explicitly requested a written plan followed by implementation in this
turn. This authorizes continuing without another design/plan approval exchange.
Meaningful review findings, including Minor findings, remain eligible for fixes.

## Current evidence and ownership

The owner's subsequent scope correction supersedes the earlier vendor
installation/update requirement: distribute the library and explain where/how
to obtain and verify it. Host integration, plugin lifecycle and deployment
instructions belong to consuming projects. No new feature or framework is added.

Library base: `dac1af62297402a0078a616e8e194c7a69cafe18`, Python >=3.12,
package `0.1.0.dev4`. Existing CI covers native macOS/Ubuntu and Python 3.12/3.14.
A release notice cannot claim a consumer has adopted the library.

Keep this change in the library repository. Native execution, host integration,
host release versions and local plugin installation remain independently owned.
The first delivery capability is a release proposal: a per-release Markdown
record plus machine-readable release identity in a target PR. It does not rewrite
native host implementations. The consumer guide covers library acquisition and
verified Python installation only; host installation/update guidance is outside
this repository's scope.
A separate Codex bundle-upgrade mechanism is not part of publication and
notification tooling. AGY is a supported route and consumer of that guide; the
two named distribution repositories remain the only automatic delivery targets.

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
   publishes and reads library assets; it is not a cross-repository credential.
   Delivery passes it as `SOURCE_GH_TOKEN` for fixed library API requests and
   the App token as `GH_TOKEN` for the two host repositories. Do not depend on
   a host-only installation token falling back to anonymous source-repo access.
   This uses the existing workflow token, not another registered secret. Store only
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
- Previous recorded library version (or unrecorded), pending adoption and API links;
  the notice supplies no host verification evidence.
- Exact wheel/sdist/manifest acquisition and library verification guidance.
- Consumer ownership of integration, native adapters and deployment; no plugin
  installation/update commands or host rollback procedure.

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

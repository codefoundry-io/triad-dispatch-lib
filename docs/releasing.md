# Publishing a library release and proposing host updates

This repository owns library artifacts and release-notice tooling. Consuming
projects own integration and deployment. The [consumer guide](installing.md)
describes obtaining the GitHub Release wheel, sdist and manifest and verifying
library installation. Automatic notices target
only `codefoundry-io/triad-codex-dispatch` and
`codefoundry-io/triad-dispatch`.

As of the [2026-10-22 adoption check](host-adoption.md#current-recorded-adoption-2026-10-22),
`codefoundry-io/agy-triad-dispatch` also records the library, but it is not an
automatic notice target. The [historical 2026-10-22 release plan](requests/2026-10-22-triage-and-release-plan.md)
tracks all three consumers and separates manual notice delivery from a future
change to the automation allowlist and App scope.

## Current activation boundary

As of 2026-10-24 (KST), [dev7](https://github.com/codefoundry-io/triad-dispatch-lib/releases/tag/v0.1.0.dev7)
is published from `62c3a741b729c6359cc5079a0306fad1fdd1fac8` (merged PR #23),
with wheel SHA-256
`cc24c8d285927c9a874a54c0b72a01668eaf77abbf183e6cf3abb8771ea9b480`.
[Release run 40014779906](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/40014779906)
completed package verification and publication; automatic delivery separately
failed on missing App settings. Earlier
[dev6](https://github.com/codefoundry-io/triad-dispatch-lib/releases/tag/v0.1.0.dev6)
was published from `1872227abd42553635c733e0aa228548a577a732` (merged PR #28).
The dev7 follow-up was delivered manually to
[Codex #46](https://github.com/codefoundry-io/triad-codex-dispatch/pull/46#issuecomment-6373568489),
[Claude #1](https://github.com/codefoundry-io/triad-dispatch/pull/1#issuecomment-6373568959)
and [AGY #2](https://github.com/codefoundry-io/agy-triad-dispatch/pull/2#issuecomment-6373569416).
Codex 0.2.565 adopts dev7 with verified local installation and fresh skill
exposure; Claude [0.2.1987](https://github.com/codefoundry-io/triad-dispatch/releases/tag/v0.2.1987) adopts dev7 and renders the roster
locations (C81-C83 NOT RUN on A, DL-177); AGY has a dev7 request with no
completion reported. See
[dated host evidence and limits](host-adoption.md#latest-host-follow-up-2026-10-24).
Publication, automatic notices, manual requests and host completion remain
separate. This reconciliation does not change App settings or retry delivery.

### Earlier dev5 activation evidence

On 2026-10-23 (KST), [dev5](https://github.com/codefoundry-io/triad-dispatch-lib/releases/tag/v0.1.0.dev5)
was published from `859f27c07c1123e87b50344f587999a0cbc172a6`. The
[exact-tag release run](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/39852025988)
completed its four native verification jobs and publication. The separate
`deliver` job failed on missing GitHub App configuration; publication succeeded.
Manual release notes were delivered to
[Codex #46](https://github.com/codefoundry-io/triad-codex-dispatch/pull/46#issuecomment-6351093675),
[Claude #1](https://github.com/codefoundry-io/triad-dispatch/pull/1#issuecomment-6351096977)
and [AGY #2](https://github.com/codefoundry-io/agy-triad-dispatch/pull/2#issuecomment-6351099545).
Do not automatically retry this notice job: the branch-based deduplication does
not recognize those manual proposals. Host adoption remains independently owned;
no App settings or credentials were changed by that publication or this update.

### Earlier dev4 activation evidence

The source provides publication, retry and proposal tooling. The 2026-10-16
read-only audit found no library releases, repository-visible Actions variables
or secret names, or environments. In particular, `TRIAD_RELEASE_APP_ID` and
`TRIAD_RELEASE_APP_PRIVATE_KEY` were absent from the inspected repository and
applicable organization scopes. App registration/installation itself was not
inspected. That audit preceded the owner-authorized PR #14 merge and
[v0.1.0.dev4 publication](https://github.com/codefoundry-io/triad-dispatch-lib/releases/tag/v0.1.0.dev4).
The exact-tag four-platform verification and publication jobs succeeded with
wheel, sdist and manifest assets. The original delivery job refused missing App
settings and sent no host notices. Current App settings were not re-audited on
2026-10-22; check them before delivery of a future version. Publication does not
establish host adoption, and that failed delivery does not negate the later
independent adoption records linked above.

On 2026-10-22, the owner-requested dev4 change list was delivered manually to
[Codex #46](https://github.com/codefoundry-io/triad-codex-dispatch/pull/46#issuecomment-6331229801),
[Claude #1](https://github.com/codefoundry-io/triad-dispatch/pull/1#issuecomment-6331230108)
and [AGY #2](https://github.com/codefoundry-io/agy-triad-dispatch/pull/2#issuecomment-6331230380).
Do not automatically retry the old dev4 delivery job as unfinished work. A later
retry is a separate owner decision: automation deduplicates by its own
`automation/triad-lib/<tag>` branch and will not recognize these manual proposals.

The current helper reads prior adoption only from `contracts/library-adoption.json`.
Claude's export records adoption under
`skills/triad-cross-family-review/lib/lib-adoption.json`, so its automated notice
will report the prior version as `unrecorded`. That conservative fallback is not
evidence of no adoption. Changing record lookup belongs to a separately selected
automation update alongside any third-host support.

## Configure the GitHub App

An organization owner creates or selects a GitHub App and installs it on exactly
these repositories:

- `codefoundry-io/triad-codex-dispatch`
- `codefoundry-io/triad-dispatch`

Grant repository **Contents: Read and write** and **Pull requests: Read and
write**; GitHub supplies Metadata read access. No webhook, source-repository
write access, organization permission or user access token is needed for notice
delivery. Record the App ID as the source repository Actions variable
`TRIAD_RELEASE_APP_ID`. Register its private key as the source repository Actions
secret `TRIAD_RELEASE_APP_PRIVATE_KEY` using GitHub's settings interface. Do not
put a key or developer credential in Git, generated notices or workflow output.
This procedure does not register or rotate credentials automatically.

The pinned `actions/create-github-app-token` v3.3.0 accepts `app-id` (deprecated
in favor of `client-id`, but compatible with this App ID configuration). It
requests only the two named repositories and Contents/Pull requests write
permissions, after platform CI and source publication finish. An installation
token expires after one hour and cannot exceed installed App access. Source
`GITHUB_TOKEN` has Contents write permission only in the publication job; it
publishes assets in this repository. The delivery credential is separate.
In the delivery job, `SOURCE_GH_TOKEN` is the source workflow's read-capable
`GITHUB_TOKEN`, while `GH_TOKEN` is the two-host App token. Source release/tag/
asset API reads use the source token; host API calls use the App token. This
avoids assuming that a host-only installation token can access a noninstalled
source repository, even when that repository is public. No additional configured
secret or App installation on the source repository is needed.
See [GitHub's installation-token documentation](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
and the [pinned action inputs](https://github.com/actions/create-github-app-token/blob/v3.3.0/action.yml).

This published-event workflow requires GitHub's server-enforced immutable-release
setting to remain disabled for new releases: GitHub prevents adding assets after
an immutable release is published. The 2026-10-16 read-only repository check
reported `enabled: false` and `enforced_by_owner: false`; no setting was changed.
Our publisher preserves existing bytes through validation and refusal; it does
not enable GitHub immutability or create release attestations. A release reporting
`immutable: true` with missing assets is refused before uploads; complete matching
assets can still be verified/reused. Enabling the server setting later requires
a separately designed draft-build-publish flow. See
[GitHub's release management documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

## Prepare and publish

Choose a reviewed commit containing the publishing workflow and tools. Set the
version in `pyproject.toml` through the normal review process. The release tag
must be exactly `v` plus that version; the workflow checks the package metadata
on the resolved commit. Preserve development/prerelease labels: a `.dev`, alpha,
beta or release-candidate package is not a stable library release. For such a
package, mark its GitHub Release as a prerelease.
The resolver and publisher refuse these versions when GitHub's prerelease flag
is false. Set the flag correctly before publishing any assets, and do not change
it after verified assets exist: the manifest records GitHub's flag, so changing
it would conflict with the existing immutable release identity. Stable-version
tags may also be deliberately marked as prereleases; the recorded flag remains
the actual GitHub value. There is no automatic migration of published manifests.

Run the repository's locked tests, source-asset checks, sdist/wheel verification
and complete required native CI/review before choosing `SOURCE_COMMIT`. Final
merge, tag publication and actual release creation remain owner-controlled
actions. With those actions explicitly approved, use this sequence from a clean
checkout of the reviewed source (replace the example values):

```sh
SOURCE_COMMIT='<full reviewed 40-character commit SHA>'
TAG='v0.1.0.dev4'
NOTES='/absolute/path/to/reviewed-release-notes.md'
git tag -a "$TAG" "$SOURCE_COMMIT" -m "Library release $TAG"
git push origin "refs/tags/$TAG"
gh release create "$TAG" --repo codefoundry-io/triad-dispatch-lib \
  --verify-tag --title "$TAG" --notes-file "$NOTES" --prerelease
```

For a stable version, omit `--prerelease`. Do not attach locally rebuilt assets
to this command: the workflow selects the verified CI artifacts. Release notes
are read from a file and later rendered as inert data; they are never shell
source. On the owner's managed workstation, run development commands through
`/bin/zsh -lic` under the existing execution policy.

Publishing a non-draft GitHub Release triggers `release.yml`. It resolves the
actual tag (including annotated tags) to a full commit SHA, then calls the
reusable `test.yml` on that exact SHA. All four native Ubuntu 24.04/macOS 15 and
Python 3.12/3.14 jobs must pass source tests, archive tests and the installed-wheel
drivers. Only Ubuntu/Python 3.12 uploads its verified normalized sdist and wheel
rebuilt from that sdist. The artifact directory contains exactly these two files,
excluding `uv build`'s extra `.gitignore`. The publisher validates archive
name/version, source commit and release metadata before attaching the two
archives and `triad-release.json`, with the manifest last.

Source publication completes before cross-repository credentials are checked.
Missing App settings fail the delivery job with setup guidance while preserving
published assets. The delivery CLI processes both hosts independently and exits
unsuccessfully if either fails; a successful proposal remains intact.

## Retry and immutable assets

If source publication succeeded and only host delivery failed, correct the
reported credential or permission issue, then choose **Re-run failed jobs** on
the original Actions run. This preserves the successful verification/publication
jobs and their outputs/artifacts, and the delivery job mints a fresh App token.
The CLI equivalent is:

```sh
gh run rerun <original-run-id> --repo codefoundry-io/triad-dispatch-lib --failed
gh run watch <original-run-id> --repo codefoundry-io/triad-dispatch-lib --exit-status
```

Also prefer this original-run failed-jobs retry when verification succeeded but
publication uploaded only a subset of assets before failing. First address any
incomplete `starter` entry through the operator inspection/removal procedure
below, and confirm that the original `release-artifacts` from the successful
verification job is still available in that run's Artifacts section. The
retried publication job downloads the retained verified archives instead of
rebuilding them. The [pinned download action](https://github.com/actions/download-artifact/blob/v8.0.2/action.yml)
uses the current workflow run by default; [GitHub keeps the run ID unchanged on
re-run](https://docs.github.com/en/actions/reference/workflows-and-actions/variables#default-environment-variables).
This recovery requires the original artifact to remain accessible and neither
deleted nor expired. Repository/organization retention settings can expire it
before the re-run window ends; see [artifact availability](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts).
If it is unavailable, use the full tag-dispatch fallback below, which still
requires rebuilt bytes to match every already-published asset.

GitHub permits re-running a workflow for up to 30 days after its initial run,
using the original SHA/ref. See
[GitHub's re-run documentation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs)
and [`gh run rerun`](https://cli.github.com/manual/gh_run_rerun).

Use a full tag-dispatch retry when a new complete verification/publication
attempt is needed. The workflow must already exist on `main`:

```sh
TAG='v0.1.0.dev4'
gh workflow run release.yml --repo codefoundry-io/triad-dispatch-lib \
  --ref main -f tag="$TAG"
gh run list --repo codefoundry-io/triad-dispatch-lib --workflow release.yml
gh run watch <run-id> --repo codefoundry-io/triad-dispatch-lib --exit-status
```

Full tag-dispatch retries rebuild and run verification again. They depend on a
byte-identical rebuild of any already-published archives and can refuse after
backend/compression/runner drift, even when the source tag is unchanged. Prefer
the failed-job re-run above for delivery-only failures, or partial publication
when the original verified artifact remains available. Existing uploaded
assets are downloaded through
the source GitHub asset API and compared byte for byte, including the manifest.
Matching assets are reused; a valid partial subset uploads only missing files.
Different bytes, duplicate names, unexpected assets, wrong URLs/size/state or a
changed tag/source identity cause refusal. Nothing is overwritten or deleted.
An interrupted upload can leave a GitHub `starter` entry: an operator must inspect
it and explicitly remove that incomplete entry in GitHub before retrying. Never
remove a verified published asset to silence a mismatch; investigate the build
environment and issue a new version when the intended bytes changed.

The low-level publisher can also operate on the exact two archived CI files in
an otherwise empty local directory. Supply an authorized source Contents-write
token through `GH_TOKEN` in the environment, never an argument:

```sh
python3 tools/publish_release.py publish --tag "$TAG" \
  --source-commit "$SOURCE_COMMIT" --dist /absolute/path/to/verified-artifacts
```

That command performs live source writes and requires publication authorization.
It does not create a release or bypass the operator's CI/review responsibility.

## Build reproducibility limits

CI sets `SOURCE_DATE_EPOCH` to the source commit's timestamp for both builds.
Before extraction and hashing, `normalize_sdist` sorts tar members and sets
tar/gzip time plus owner metadata deterministically, removing corresponding PAX
time/owner overrides while preserving member names, types, modes and payload
bytes. The wheel is rebuilt from this normalized sdist with the same epoch.
Plain setuptools sdists varied in repeat-build probes despite
`SOURCE_DATE_EPOCH`; the bounded normalizer closes that observed metadata gap.

Repeated normalized sdist/wheel builds matched in the same environment. This is
not a guarantee across backend, Python, OS or compression changes. `uv.lock`
locks project dependencies, not the isolated build backend; `pyproject.toml`
currently allows `setuptools>=81,<82`. Actions and uv are pinned, while runner
images and the backend's allowed patch version can change. If rebuilding the
same tag produces different bytes, the publisher refuses them. Preserve the
original verified artifacts or publish a reviewed new version; do not weaken
the comparison or add automatic overwrite.

## Preview without delivering a notice

After a real source release has all three verified assets, supply approved
source read credentials through `SOURCE_GH_TOKEN` and host read credentials
through `GH_TOKEN`, then run from its source checkout. Set both environment
variables before invoking the CLI; token values never belong in arguments:

```sh
python3 tools/release_prs.py --tag "$TAG" --dry-run-dir /absolute/path/to/previews
```

This reads release/tag/assets and host default-branch/adoption metadata, verifies
the archives and writes only local previews. It creates no branch or PR. Use
`--target codefoundry-io/triad-codex-dispatch` or
`--target codefoundry-io/triad-dispatch` for a single host. With no published
release yet, this live-data preview is unavailable; offline tests exercise the
same rendering and API state transitions without creating test releases/PRs:

```sh
uv run --locked pytest -q tests/test_release_artifacts.py \
  tests/test_publish_release.py tests/test_release_prs.py
```

For an advanced manual delivery retry without rebuilding source artifacts, the
operator must supply an approved two-host App installation token in `GH_TOKEN`
plus a source-read token in `SOURCE_GH_TOKEN`; see
[GitHub's installation-token generation procedure](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app).
This CLI does not mint credentials or read/copy a private key. Prefer the
original workflow's failed-job re-run for routine delivery recovery. With those
authorized environment credentials supplied, run:

```sh
python3 tools/release_prs.py --tag "$TAG"
```

## Generated proposal and host responsibility

A proposal uses branch `automation/triad-lib/v0.1.0.dev4` and title
`Library update request: v0.1.0.dev4`. It adds exactly:

- `docs/library-updates/v0.1.0.dev4/release.json`: release and archive identity.
- `docs/library-updates/v0.1.0.dev4/README.md`: release notes, hashes, prior recorded
  library version (or unrecorded), library acquisition/verification guidance and
  pending consumer adoption. The notice supplies no host verification evidence.

Existing open, closed or merged PRs prevent duplicate creation. A matching
branch-only interrupted attempt can resume, including after the default branch
advances; conflicting branches and maintainer edits are preserved. No force
push, reopen, automatic merge or installation occurs.

Consumers verify the library pin/hash and compatibility using the
[library guide](installing.md); integration, deployment and plugin lifecycle
instructions belong to their own projects. The owner's scope correction
supersedes the earlier vendor installation/update guidance requirement. Keep
library publication, notice delivery and consumer adoption as separate evidence
in the final operator report.

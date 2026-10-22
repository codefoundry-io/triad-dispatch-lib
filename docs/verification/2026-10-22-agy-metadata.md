# AGY metadata compatibility candidate

The owner approved preserving AGY `toolAction`/`toolSummary` and separating these
undeclared top-level fields before actual verdict validation. The shared rule is
[R-AGY-METADATA](../../spec/reference/review-rules.md#R-AGY-METADATA), with the
[decision and bounded plan](../../spec/decisions/2026-10-22-agy-result-metadata.md).

## Implementation and verification

Implementation source `184e9bf6b43197bf4b93b2fd1f0466bdb5cbf24f` adds the shared
helper and applies it only to AGY admission. Generic verdict validation and
other carriers remain strict. Raw extraction, declared/nested fields, canonical
schemas, all six bindings, negative verdicts and terminal failures are preserved.

- Local macOS 26.6.2 arm64 / Python 3.12.13: focused RED 37 failures, then
  GREEN 130 tests; final affected tests 190 passed. Full suite: 1397 passed.
- Assets, authoring and structural API compatibility checks passed.
- Built dev5 sdist and rebuilt its wheel; isolated wheel verification passed
  seven public-consumer tests, twelve raw JSON cases and all four bundles.
  Candidate wheel SHA-256:
  `738ad14d7976ec83d85f1f3799cddb25e217e234c5db02f23a1f849caa662e4c`.
- [Native package CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/39772302033)
  passed on macOS 15 and Ubuntu 24.04 with Python 3.12 and 3.14, covering source,
  unpacked sdist, installed wheel and synthetic drivers at that implementation
  commit. [API CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/39772302537)
  also passed. These results do not certify consumer-host installation.

## First formal round

Round `20261022-lib-agy-metadata-r1-b7d3a8`, content digest
`2b9599d017cd709e1799fb70e607059248151abd3721da8a65e9ddbd20e4474d`, used the
project's Opus 5.5/xhigh, Sol 6.1/xhigh and AGY Argon/high roster. All three
returned `SAFE TO MERGE`; collection was `AGREED` and final verification returned
`ROUND_INTEGRITY_OK`. The separate Astra/high comparison reported the C80 status
issue and no runtime defect. Requested settings are not hidden runtime attestation.
All producers terminated; the managed packet was exported and its exact temporary
root and isolated launcher handles were removed.

The original AGY 1.4.5 terminal `SUCCESS` response included both `toolAction` and
`toolSummary`. The candidate Codex wrapper retained the complete raw run log,
separated those fields and admitted the remaining twelve-field bound verdict.
This is actual provider evidence for that invocation, not a claim that every
provider output or host release is verified. The earlier ordinary diagnostic
also succeeded, but its truncated audit alone cannot prove metadata presence.

Accepted bounded documentation findings: stale C80 library status; stale case
and rule totals; dev4 versions in active smoke examples; and missing guidance for
host-owned recovered AGY output submitted through strict `native-final`.
These are corrected before a fresh full-scope review of the changed candidate.
No runtime defect was reported. An encoder recursion scenario was explicitly
unobserved and classified as a nonblocking hardening suggestion; no new failure
handler or validation redesign is introduced without a demonstrated trigger.

## Second formal round

Round `20261022-lib-agy-metadata-r2-d38e96` reviewed candidate
`7d26f400c97bdd5fb2942a97da2bf815e16135cc`, content digest
`b87f8cf1aa74368cf2f57deb7f05188d87de2fafc0590e902ba888eeaee451c3`, after
the four R1 documentation corrections. All three required reviewers returned
`SAFE TO MERGE`; collection returned `AGREED` and verification returned
`ROUND_INTEGRITY_OK`. The separate non-voting Astra/high comparison found no
concrete defect. All producers completed, the packet was exported and the exact
managed temporary root was removed.

Three accepted Minor findings are corrected in the combined candidate: README
adoption wording now matches the dated host records; the mapping contract links
the C80 metadata exception; and consumer-test/API documentation distinguishes
the dev4 floor from additive dev5 coverage. The unobserved encoder-recursion
scenario remains the nonblocking hardening limit recorded above.

Retained exact-head CI evidence for `7d26f40` records successful
[package CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/39775040999)
on macOS 15 and Ubuntu 24.04 with Python 3.12 and 3.14, including unpacked-sdist
rebuild and installed-wheel checks, and successful
[API CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/39775041050).
R2 and those runs apply to that basis only. The later combined PR #24 includes
the PR #20/#22 documentation and these corrections and requires a fresh complete
review; this record does not claim independent formal approval of their original
PR heads or approval of the changed combined candidate.

## Host and deployment sequence

[Codex PR47](https://github.com/codefoundry-io/triad-codex-dispatch/pull/47) integrates
the verified candidate helper while preserving native stream recovery. Its tests,
formal host review, native CI and publication are separate from this library gate.
Claude and AGY own their integrations through the existing
[Claude proposal](https://github.com/codefoundry-io/triad-dispatch/pull/1) and
[AGY proposal](https://github.com/codefoundry-io/agy-triad-dispatch/pull/2).

1. Complete the corrected library review and exact-head CI for PR24.
2. After owner approval of integration/publication, merge and publish dev5 using
   the existing release procedure and its exact artifact manifest.
3. Each host reviews the common rule and independently adopts the published
   artifact. Refresh any candidate wheel/source provenance to the actual released
   identity and verify package bytes before host release.
4. Each host runs its own regression, native-platform and provider checks, then
   follows its separately authorized merge, publication and installation process.

No merge, public release, local installation or global provider-setting change is
claimed here. Published library dev4 and historical failed reviews remain unchanged.

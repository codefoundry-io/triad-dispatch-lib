# Policy provenance and request synchronization

This record describes the bounded documentation/policy-comment plan preceding
the [approved adoption APIs](../design/2026-10-15-adoption-apis.md). It does not
approve later changed bytes, package publication or consumer adoption.

Candidate `3fb1699dcd71647f6ace4355a703f7d47fc19864` corrected the two canonical
A policy headers and adjacent current digests while retaining imported ancestry.
It synchronized requester comments and library/host integration boundaries.
Parsed TOML and bytes after the headers were equal to base
`ee8b4b4ab3c1440788733931874047a1821ee08e`; runtime/package/schema assets were
unchanged. Local source verification passed 952 tests and authoring/assets checks.

R1 `20261015-lib-provenance-r1-f3a168` completed `BLOCKED`: Opus required
correcting the consolidation PR attribution, also noting stale host-policy byte
claims/header pointers and the lost fixed rule guard. Sol, Argon and nonvoting
Astra independently found the attribution error. All producers terminated and
the round was exported/cleaned before corrections.

Correction `743e52a8b5fce448684b24aae38fcdeca200d834` separates original
consolidation PR #1/9489543 from later adoption-observability PR #2/ee8b4b4; scopes
host byte equality to imported policy revisions; and adds a fixed parsed
tool/decision/priority rule assertion alongside the current digest check.
Copied-fixture controls rejected a priority change and accepted a comment change.
Canonical policy bytes were not changed by this correction.

Local macOS/Python 3.12.13 results: 24 focused tests, 953 full source tests,
authoring 1 valid/0 invalid, generated-assets and diff checks passed. Fresh scoped
Sol/medium review found all three corrections addressed and no new breakage.

[Native CI 38697006277](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38697006277)
verified actual checkout 743e52a against EXPECTED_SHA in each job:

| Actual runner | Python | Source | Unpacked sdist |
| --- | --- | --- | --- |
| macOS 15.7.9 ARM64 | 3.12.10 | 953 passed | 953 passed |
| macOS 15.7.9 ARM64 | 3.14.7 | 953 passed | 953 passed |
| Ubuntu 24.04.5 | 3.12.15 | 953 passed | 953 passed |
| Ubuntu 24.04.5 | 3.14.8 | 953 passed | 953 passed |

Each job passed source/archive authoring and asset checks, built the sdist and
wheel, and passed all four installed synthetic drivers without skipped stages.
Actual job logs and driver reports were inspected; the configured matrix alone
was not used as platform proof. This snapshot predates the new API assertions.

R2 `20261015-lib-provenance-r2-b5ed9d` completed `AGREED` on 743e52a: required
Opus 5.5/xhigh, Sol 6.1/xhigh and Argon/high all returned SAFE; separate Astra/high
found no actionable defect. Each entry had 2400 seconds and official web research
authorization. All producers terminated, final integrity passed and the round
was exported/cleaned. Native runtime model/effort identity remained UNEXPOSED;
native containment was prompt-controlled. The host trace hid the native message,
so it supplied no independent dispatch-message byte-equality proof.

Opus retained three nonblocking followups, explicitly assigned to the
[next plan](../superpowers/plans/2026-10-15-adoption-apis.md): strengthen the rule
guard to include optional qualifiers, scope the migration unchanged-bytes claim
to its original move, and supersede pending diagnostic decisions with the owner's
approved `.missing`/declined `.member` boundary. Their later changes require
fresh combined verification and review; this record does not mark them fixed.

The tests/CI are synthetic library and package evidence. No Gemini enforcement,
host re-vendoring, provider success, new host adoption or release was measured.
The package remains unpublished 0.1.0.dev4 and final merge is a separate action.

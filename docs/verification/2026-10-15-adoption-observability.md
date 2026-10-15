# Additive dev4 observability verification

The owner-approved [design](../design/2026-10-15-adoption-observability.md) adds
bounded L2 diagnostics and L7 manifests. Runtime commit `fed36fb`, test-version
correction `2ca6536`, and integration snapshot `cc01cdc` contain the measured code.
Later concurrent-branch reconciliation changes documentation only. Native CI and
formal review assess their own committed snapshots; results are retained with
PR #2 after source freeze and are not implied by this local record.

## Regression and compatibility evidence

- Admission tests: 23 RED failures on missing attributes, then 23 GREEN.
- Manifest tests: 65 RED failures on the unsupported keyword, then 65 GREEN.
- Combined new and existing admission/prompt/output/agreement suite: 308 passed.
- All 54 supported default renderer profiles matched `0f215114` byte-for-byte.
- Independent task review passed spec and quality checks. The initial complete
  suite found one version-hardcoded identity test (951 passed / 1 failed on both
  Python versions); it now uses installed metadata to reach the intended
  site-packages refusal. The distinct version-mismatch test remains. Its scoped
  review passed, and 140 affected tests passed before the complete rerun.

## Complete local rerun

Native macOS 26.6.2 ARM64, uv 0.11.8, locked pytest 9.1.1:

| Check | Python 3.12.13 | Python 3.14.6 |
| --- | --- | --- |
| Source pytest | 952 passed | 952 passed |
| Unpacked-sdist pytest | 952 passed | 952 passed |
| Source/archive authoring and generated assets | PASS | PASS |
| Rebuilt wheel, verified bundle replay | PASS | PASS |
| Codex prompt/admission driver | 54 cases | 54 cases |
| Four-route driver | 51 profiles, 4 investigations | 51 profiles, 4 investigations |
| Native callback synthetic self-test | PASS | PASS |
| Isolated installed L2/L7 probe | PASS | PASS |

Each version used separate source/archive environments and a neutral unpacked
sdist directory. All 17 recorded stages per interpreter exited zero. The extra
installed probe used an isolated `-I` child and verified site-packages/dev4 origin,
binding field and schema path, fixed messages, default-text equivalence, selected
web dependency and fresh manifest ownership. All dependency installations used
binary distributions; no provider or native reviewer was invoked by these tests.

The file inventory was identical before and after measurement despite the
leader committing those frozen bytes. Its fingerprint was
`680b37129117f79db388550b8503922b546546ed6e8c03a37eaf382e5540caf2`.
Measured artifacts, before documentation-only reconciliation:

| Python | Artifact | SHA256 |
| --- | --- | --- |
| 3.12 | sdist | `ac9f637f512a69548ce30a45db9e0e0dc6b9e2a19a580444a5b471fdcb16cc2e` |
| 3.12 | rebuilt wheel | `2b37e26762d915944197390e76b2752f471a212b917f5860ec6fee3ef6ff1181` |
| 3.14 | sdist | `0fd6c71b7e3d4ff5fd60969785ed0f0ddc182004f446f8719c5971b78e676d5e` |
| 3.14 | rebuilt wheel | `d572ad576063000c6d38173ac0b37fcb7a9636db3ac16f7114f069a2c65fccad` |

The two wheels have identical contained filenames/payload hashes, not identical
container hashes. Runtime/schema/prompt payload files did not change during
documentation reconciliation. This local record establishes no Ubuntu result,
real-provider behavior, dev4 consumer adoption, publication or merge. Read the
exact-head PR CI and complete project review for those separately measured gates.

## R1 documentation corrections

Before these corrections, exact-head CI
[38673591607](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38673591607)
passed 952 source and 952 archive tests plus all four installed-wheel drivers
in each Ubuntu/macOS and Python 3.12/3.14 job at `2eff9d0`. The complete review
`20261015-lib-observability-r1-fcb113` then returned `BLOCKED`: Opus requested
five documentation corrections; Sol approved without findings and Argon approved
with the same README finding. Separate Astra found no required fix.
All results and source/custody integrity were validated before export and cleanup.

The verified corrections update stale README/migration adoption and merge status,
repair the historical B sentence and adjacent released-source wording, and state
the exact L2 diagnostic limits. `absolute_schema_path` describes validator
evaluation and need not resolve as a JSON Pointer through source `$ref`/`if`
nodes. The existing nested-reference regression already demonstrates this path.
The value-free guarantee covers fixed message/`.args` and `.field`/`.path`;
Python exception internals retain existing references, including `__context__`.
The previous wording promised more than the additive API implemented. Runtime,
tests, canonical schemas, prompt payloads and dependency versions are unchanged.

Independent scoped checks confirmed the findings and current release evidence.
These are documentation corrections, so existing spec/authoring/assets checks
verify their integration; no runtime behavior or new implementation-mirroring
test is introduced. Changed documentation and the README package description
require new exact-head source/package CI and a fresh complete review. Their
outcomes remain with PR #2 after this source record is frozen.

Before the next source freeze, concurrent amendments `e8ea66d`/`b18da1b`
published Claude scratch scripts, captured outputs and input identities and
reduced its planned first slice to two library functions. Those artifacts are
preserved without executing them; matching unpublished host inputs still prevent
independent reproduction. Current request/adoption/status wording is reconciled
to this new evidence. No host implementation or runtime API changes are included.

## R2 documentation corrections and incomplete review

Exact-head CI [38676236147](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38676236147)
passed all four Ubuntu/macOS and Python 3.12/3.14 jobs at
`bc817cabb993e6fb8fd4764b901985ce74a3bcd7`: each ran 952 source tests, 952
unpacked-sdist tests and all four installed-wheel drivers without skipped checks.
Round `20261015-lib-observability-r2-b1a9fc` then ended `INCOMPLETE`. Opus and
Sol returned `SAFE TO MERGE`; Argon returned no valid verdict after an individual
quota exhaustion error. The provider reported a reset interval, but recovery has
not been observed. All producers, including the separate Astra comparison,
terminated before the round was exported and cleaned. No approval transfers to
changed bytes or compensates for the missing required reviewer.

Opus identified three documentation Minors: current-tense Codex candidate wording
in the setup section, missing two-function supersession in the design, and the
spike README's inaccurate "hashes above" pointer. Sol and separate Astra identified
one additional Minor: the source archive includes the spike Markdown but omits
its scripts and captured outputs. A fresh sdist of `bc817ca` reproduced the latter:
both Markdown files were included byte-for-byte, while all three scripts and four
output files were absent. That archive's SHA256 is
`d080d8bc2853ee68e4b2c7c475ec3792e9b21283bf2cb4a27c129de39079ec41`.
No scratch script was executed and the frozen checkout remained unchanged.

These four corrections date the setup observation, name the superseding functions,
link the actual hash record and explicitly identify repository-only evidence with
a commit-pinned source link. Packaging rules, runtime, tests, assets and dependencies
remain unchanged. Opus's optional overload suggestion concerns future publication
of typing metadata; no `py.typed` marker or new typing guarantee is introduced here.
Affected documentation/package checks and fresh exact-head CI verify the correction;
a new complete project review remains required after provider recovery. Final
post-freeze outcomes are retained with PR #2 rather than implied by this record.

After R2 closed, concurrent amendments `e763df8` and `d5d7f65` narrowed the
remaining L2 request to `.member` and published S1's probe, full selected-test
failure log and wheel inventory/hashes. Current request/adoption/design records
reflect those reports; earlier R1/R2 findings above retain their measured source
boundaries. The S1 evidence files are preserved without execution, and the
repository-only evidence link now points to the snapshot containing those files.

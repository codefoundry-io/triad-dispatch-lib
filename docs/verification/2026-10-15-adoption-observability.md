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

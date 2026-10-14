# Specification/library consolidation verification

Date: 2026-10-13. Task 2 builds on approved Task 1 commit `3115cf3`.
The build under test is the Task 2 working tree, before this evidence record was
completed. Release/build commit provenance belongs here, outside runtime manifests.

## Source and TDD

The new packaging probe tests first failed: 12 failures because the all-bundle
verification entry point was absent. They cover manifest metadata and refusal of
corruption in each of eight payloads and all three manifest IDs. After adding
verification through the strict runtime loader, `tests/test_replay.py` passed
25 tests. The first combined run exposed one existing dev2 version literal in
`test_profile_and_identity` (632 passed, 1 failed); updating the driver tests to
dev3 restored the intended import-origin assertion.

`uv sync --locked` succeeds without dependency changes; root
`uv run --locked pytest -q` passes **633 tests** (447 library + 186 specification).
`uv run --locked python spec/tools/check_authoring.py` reports 1/1 valid map.
`uv run --locked python tools/sync_spec_assets.py --check` and `git diff --check`
pass. Importlib pytest mode remains enabled. All development commands used
`/bin/zsh -lic` with `sandbox_permissions="require_escalated"` from the workspace
host cwd, then entered this repository.

## Distribution

The dev3 sdist is unpacked outside the checkout without `.git`, its canonical
specification inputs are compared byte-for-byte with the source tree, and its
locked environment runs both suites, the authoring checker and generator check.
Its wheel is rebuilt there and used by all four isolated installed-wheel drivers.
Bounded spec source-directory inclusions avoid `_runs`, caches, temporary output
trees and VCS metadata without warning-producing unmatched exclusion patterns.
Archive inspection also verifies that the wheel does not ship source test/docs/tool
trees. Exact artifact paths, hashes and final driver results are recorded below.

## Bundle identities and preserved history

| Bundle | `contract_id` |
| --- | --- |
| verdict | `455dfd8a7d586d04eedb60ee492cf421e076a77bafcccbba12de37cc12bf0340` |
| roster | `a99fb58dbd920dfed0d88d8c8b9117bd07633b76b5d2565e05f50a5b5c423ed8` |
| prompts | `c332d95688b9db3dac187a0bebac6ddc0eddfdbdc5401a649697d0601455e843` |

The installed probe checks every manifest shape/ID and payload digest, reporting
all three complete manifests instead of the removed `source_commit`. It retains
isolated `site-packages` import checks and strict failure behavior. Canonical
bytes, schema IDs, import ancestry and historical decisions/changelog/cases are
unchanged. Active authoring guidance is intentionally updated, so original
import hashes are not assertions about the edited guidance.

The inherited trailing space at `spec/decisions/owner-register.md:728` is preserved
as a historical byte. Task 2's diff check passes; this is not a claim that the
whole imported historical diff is whitespace-clean.

## Limits

Actual platform is macOS 26.6.2 ARM64, Python 3.12.13, uv 0.11.8. CI configuration
retains pinned actions/dependencies and Ubuntu 24.04/macOS 15 runners, adding
combined source and unpacked-sdist checks and all four dev3 drivers. The original
local snapshot did not establish remote CI or Ubuntu execution; the committed-head
results below now supply that separate evidence. No new real provider success is claimed.
Earlier dev2 CI/native evidence remains historical. Neither host or old-spec
repository is modified; no global install, package publication, final merge,
spec tag, host release or adoption is performed.

## Independent review and committed-head CI

Task 1 and Task 2 received independent Sol/high reviews; both were compliant and
approved with no open findings. A fresh Astra/high reviewer inspected the whole
branch `c6dd981..3bcb0da` and reported no Critical, Important or Minor findings.
Requested model/effort settings are recorded, while effective settings remain
UNEXPOSED. Review containment was prompt-controlled, with unchanged HEAD and clean
tracked trees before and after the reviews.

The final reviewer independently checked the 131 original import hashes, exactly
seven intentionally edited active guidance files, and all eight runtime payloads
against upstream, current canonical source and pre-consolidation package bytes.
Historical prose was reviewed for migration fidelity, not a new semantic audit.
Real host installation/provider adoption and noncooperative callback isolation
remain outside this slice's evidence and retain their documented boundaries.

[CI run 38287530518](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38287530518)
succeeded for reviewed head `3bcb0da7eb54780aebb1bcc91fd10ba2f2a4acae`:

| Native runner | Interpreter | Source | Unpacked sdist | Installed drivers |
| --- | --- | --- | --- | --- |
| Ubuntu 24.04 x86-64 | Python 3.12.15 | 633 passed | 633 passed | all four passed |
| macOS 15 ARM64 | Python 3.12.10 | 633 passed | 633 passed | all four passed |

Both jobs also passed the source/archive authoring and generator checks, rebuilt
the wheel from the unpacked source, and verified a clean tracked tree. The watch
command exited zero; job metadata and full logs are retained locally under
`_runs/spec-consolidation/ci-38287530518.*`. These are native platform and synthetic
library results, not authenticated provider or consumer-adoption proof.

The following documentation checkpoint records this completed verification; it
does not change the reviewed implementation or runtime asset bytes. The existing
draft PR is updated, with final merge, publication and host ports still separate.

## Tested archive snapshot

These hashes describe the tested working-tree build before finalizing this
report, not an archive that contains its own final hash. Final committed-head
native CI remains separate controller verification.

- Sdist: `/Users/chaniri/codex_workspace/workspace/triad-dispatch-lib/dist/triad_dispatch_lib-0.1.0.dev3.tar.gz`
- Sdist SHA-256: `4d683d8d3135bf77f12cc9a50d22fa77db42fedcaf24acaaa6db2261b0e87c1a`
- Unpacked source: `/private/tmp/triad-task2-archive-lm4fy3b8/triad_dispatch_lib-0.1.0.dev3`
- Rebuilt wheel: `/private/tmp/triad-task2-archive-lm4fy3b8/triad_dispatch_lib-0.1.0.dev3/dist/triad_dispatch_lib-0.1.0.dev3-py3-none-any.whl`
- Wheel SHA-256: `411159a18ed0ee212fa4c0d4e1c473613d3e54bccba19abeadd8d8aa02c133de`
- Logs: `/private/tmp/triad-task2-archive-lm4fy3b8` (`sync.log`, `pytest.log`, `authoring.log`, `generator.log`,
  `wheel-build.log`, `installed-probe.log`, `codex-driver.log`,
  `four-route-driver.log`, `native-driver.log`). Temporary logs are local
  diagnostics; the durable outcome is retained here.

Archive inspection compared all **132 specification inputs**
byte-for-byte and found no `_runs`, VCS, cache or temporary output trees in the
sdist/wheel. The unpacked source had no `.git`. Its locked sync, **633 combined
tests**, authoring checker, generator check and wheel build all exited zero.
The final source-distribution build log has no unmatched-pattern warnings.

All four drivers ran from the unpacked source using its rebuilt wheel:

```sh
uv run --locked python tools/verify_wheel.py <rebuilt-wheel>
uv run --locked python tools/codex_smoke.py --wheel <rebuilt-wheel> --expected-version 0.1.0.dev3 self-test
uv run --locked python tools/four_route_smoke.py --wheel <rebuilt-wheel> --expected-version 0.1.0.dev3
uv run --locked python tools/native_codex_smoke.py --wheel <rebuilt-wheel> --expected-version 0.1.0.dev3 --self-test
```

The installed probe passed **10 raw replay vectors**, verified all three bundle
identities/eight payloads and loaded from isolated `site-packages`. Binary-only
dependencies included jsonschema 4.26.0, referencing
0.37.0, rpds-py 2026.9.1
and attrs 26.1.0. The Codex driver passed **54 synthetic
cases** across three phases. The four-route driver passed **51 prompt profiles**
and **4 investigation profiles** with its synthetic carrier/agreement matrix.
The supervised native callback self-test completed three formal entries with
peak concurrency **2**, retained dissent and blocked agreement; its separate
ordinary investigation completed with integrity true. All results are synthetic.

## Self-review

Reviewed the owned diff against the Task 2 brief: no runtime source, canonical
payload, legacy schema ID, historical case/decision/changelog or import-origin
change. The four driver interfaces and public arguments are preserved. Package
and lock versions agree at dev3; dependency pins are unchanged. The three spec
agent maps remain identical and updated links resolve within the consolidated
tree. Active guidance distinguishes pending cutover, import ancestry, per-bundle
IDs and independent host releases. No open implementation concern remains;
independent task/branch review and committed-head CI were pending at this earlier
self-review checkpoint. Their subsequent completion is recorded above under
Independent review and committed-head CI.

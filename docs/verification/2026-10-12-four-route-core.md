# Four-route core verification

Date: 2026-10-12. Unpublished development package: `0.1.0.dev2`.

## Scope and results

Local native macOS 26.6.2 ARM64, Python 3.12.13 and uv 0.11.8 verification:

- Locked sync succeeded; source and unpacked-sdist suites each pass 364 tests.
- Built the exact `dist/triad_dispatch_lib-0.1.0.dev2.tar.gz` sdist, then rebuilt
  `dist/triad_dispatch_lib-0.1.0.dev2-py3-none-any.whl` from that sdist.
- Isolated installed-wheel raw replay passes all 10 cases. The Codex adapter
  passes all 54 cases across the three formal phases.
- The new synthetic four-route driver passes nine scenarios: unanimous approval,
  informational dissent, Google sibling binding swap, invoke failure, false and
  exceptional integrity, refused preflight, bounded callbacks and independent
  investigations. Peer outcomes survive failures and integrity refusal.
- Installed prompt coverage includes 48 route/host/phase/web combinations and
  three AGY/A hook variants. Four investigations return ordinary data independently
  of formal agreement. Exported runtime function/class paths are checked against
  isolated site-packages; neither repository source imports nor source-only tests
  are accepted as installed proof.
- Both archives contain no bytecode/cache entries. Removing redundant MANIFEST
  global exclusions eliminates absent-file notices; explicit inclusion patterns
  continue to carry tools, tests, documentation and packaged canonical assets.
- Local documentation links and `git diff --check` pass.

## Reproduction and output identity

Run the [README commands](../../README.md#work-locally) using exact dev2 paths;
old dev1 artifacts can coexist in `dist/`. The workflow also unpacks the exact
sdist into a temporary directory and runs the complete locked suite there.

All three installed drivers create fresh temporary environments and execute with
Python `-I` from a neutral working directory. Reports include wheel SHA-256,
package version, actual import path and platform. The four-route report also
includes paths for every exported runtime API and SHA-256 for all 51 rendered
prompt profiles. Its callbacks and carrier data are explicitly synthetic; only
the package runtime under verification comes from the wheel.

Local exact output reports and archive digests are retained in the task's ignored
`_runs/four-route-implementation/task4-*` evidence. They are verification artifacts,
not package runtime dependencies. The final local verification of implementation
commit `2f8c81354dac8485e8dc55bfb428f446fd739035` produced:

- sdist SHA-256: `6adf41e919bf852e9917ffd67205d0beb55481b62f0e9bbfa9aa3487b600fec8`
- wheel SHA-256: `f287786bbe04d1a37bd97c7e192e80ccf6d133af21847c03a3e9a97ad9b5c76d`

## Platform and execution limits

[Native CI run 38217590730](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38217590730)
passed on implementation commit `2f8c81354dac8485e8dc55bfb428f446fd739035`:

| Native platform | Python | Source suite | Unpacked-sdist suite | Installed-wheel checks |
| --- | --- | --- | --- | --- |
| Ubuntu 24.04 x86-64 | 3.12.15 | 364 passed | 364 passed | All three drivers passed |
| macOS 15.7.9 ARM64 | 3.12.10 | 364 passed | 364 passed | All three drivers passed |

Each platform passed the same 10 raw replay cases, 54 Codex adapter cases, nine
four-route scenarios, 51 prompt profiles and 27 exported runtime path checks
described above. The final independent whole-branch review and scoped re-review
left no open findings. Earlier 157-test CI belongs to the
[historical slice](2026-10-12-lib-only-codex-integration.md).

No real provider calls, existing host imports/tests/edits, SDK/MCP execution,
global installation, merge, release or package-index publication occurred for
this slice. Neither consumer has adopted the package. Cancellation is cooperative:
callbacks own process termination/reaping and must finish cleanup. See the
[public callback and carrier contract](../../README.md#async-host-callbacks).

# Roster instance location source verification — 2026-10-23

This record covers the unpublished `0.1.0.dev7` implementation candidate based
on `3c74a187eaadb8d24e6b5f631356be43d757deb6`. Current exact-commit package,
native CI, independent implementation review, admission and publication evidence
belongs to [PR #23](https://github.com/codefoundry-io/triad-dispatch-lib/pull/23).
This source record does not establish those later results.

## Implementation and scope

`RosterError` initializes the typed `instance_path` attribute to `None`;
roster validation copies `tuple(validation_error.absolute_path)` from the same
first selected error used for existing diagnostics. Production delta: +2/-0,
net +2 lines across two files. No schema, acceptance, ordering, constructor,
fixed-message, args, serialization mechanism or dependency version changes.
Local and remote dev7 tag checks returned no matches before the metadata bump.
Historical published dev4-dev6 artifacts and host pins remain separate.

The tests cover defaults/override/standalone/selection indices 0 and 3, root
versus unavailable location, both Google route-block winners, preserved default
slots and appended merged entries, input nonmutation, captured tuple stability,
unknown-property parent locations and a package-root consumer at index 1.
Inspection of the current canonical roster schema confirmed fixed properties,
closed object definitions and no dynamic-key vocabulary; concrete privacy tests
retain unknown-key and value sentinels outside public diagnostics. Exception
contexts and tracebacks remain outside that public guarantee.

## Local source results

All development commands ran through literal `/bin/zsh -lic` with
`sandbox_permissions="require_escalated"`, outer cwd
`/Users/chaniri/codex_workspace`, then entered this repository. Host Python was
`/opt/homebrew/opt/python@3.12/libexec/bin/python3`, Python 3.12.13; uv was 0.11.8.
Logs are retained untruncated under
`/Users/chaniri/codex_workspace/_runs/20261023-roster-instance-location/`.

| Command | Exit | Result | Log |
| --- | --- | --- | --- |
| `uv run --locked pytest -q tests/test_roster_diagnostics.py tests/test_public_api_consumers.py` before production | 1 | 38 failed, 8 passed in 0.63s; absent `instance_path` | `task1-focused-red.log` |
| Same focused command after two-line implementation | 0 | 46 passed in 0.50s | `task1-focused-green.log` |
| `uv sync --locked` | 0 | 16 packages resolved; editable candidate dev7 prepared | `task1-uv-sync.log` |
| `uv run --locked pytest -q` | 0 | 1541 passed in 58.49s; no exclusions | `task1-full-source-pytest.log` |
| `uv run --locked python tools/sync_spec_assets.py --check` | 0 | No asset drift; silent success | `task1-assets.log` |
| `uv run --locked python spec/tools/check_authoring.py` | 0 | 2 total, 2 valid, 0 invalid | `task1-authoring.log` |
| `uv run --locked python tools/check_api_compatibility.py` | 0 | Declared public API baseline is structurally compatible | `task1-api-compatibility.log` |
| `git diff --check` | 0 | Silent success | `task1-diff-check.log` |

After adding the evidence records, authoring and diff checks were repeated with
exit 0 (`task1-authoring-final.log`, `task1-diff-check-final.log`). No production
or test changes followed the complete source run.

The RED failures included `AttributeError: 'RosterError' object has no attribute
'instance_path'` after existing schema/code/text/args checks. No production code
was added before this observed failure. The same test assertions passed GREEN.

## Remaining verification and authority

The root leader owns exact sdist normalization/extraction, archive tests and
wheel rebuild/verification, synthetic driver checks, exact-head Ubuntu/macOS
Python 3.12/3.14 package CI, API CI, formal implementation review and separate
Astra comparison, PR/issue updates and the publication packet. These are pending
external verification for this implementer report; no success or failure is
claimed here. No provider invocation, push, merge, release, host formatting,
host adoption or workstation installation is established by the local results.

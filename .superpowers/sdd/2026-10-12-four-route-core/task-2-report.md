# Task 2 implementation report

Status: DONE

Base: `53356fb755205b0247d56cc3ba977aa050e82226`

Implementation head: `44305e0db486f2d571ee25293ea9e4466d350637`

This report is committed separately after that implementation head; the report
commit changes only this file. No push was performed.

## Changes

- Added frozen `ProviderOutput`, explicit metadata/terminal guards, four formal
  carrier extractors and `admit_output`. Native final stays raw and host marker
  removal remains host-owned. CLI carriers must match family and Google route.
- Claude/AGY require native structured-output objects. Gemini requires a string.
  Full envelopes/records pass the existing strict parser before original JSON
  member-span extraction. Escaped member names work; byte inputs are sliced
  from their original byte carrier, without verdict serialization.
- AGY requires exactly one successful terminal and valid object JSONL records.
  Only LF separates records, preserving literal Unicode separators in JSON
  strings and refusing non-JSON record separators and malformed tails.
- Added frozen `AgreementResult` and unanimous `evaluate_agreement`: every named
  selected binding is checked, both Google routes and repeated families count,
  all six response bindings are rechecked, missing/failing/negative results
  prevent agreement, and false host integrity blocks unanimous safe responses.
- Invalid caller maps have fixed `AgreementError.code` refusals. Per-leg output
  refusals retain AdmissionError/OutputError codes. ContractError propagates.
- Edited only Task 2's seven allowed implementation/test paths and this report.

## Execution and evidence

All execution below used tool cwd `/Users/chaniri/codex_workspace`, explicit
`/bin/zsh -lic`, `sandbox_permissions="require_escalated"`, then
`cd /Users/chaniri/codex_workspace/workspace/triad-dispatch-lib` before project
commands. Every running exec session was consumed to terminal exit code.

Environment preflight (exit 0):

```sh
command -v python3
python3 --version
command -v uv
uv --version
cd /Users/chaniri/codex_workspace/workspace/triad-dispatch-lib
uv sync --locked
```

Resolved Python `/opt/homebrew/opt/python@3.12/libexec/bin/python3`, Python
3.12.13, `/opt/homebrew/bin/uv`, uv 0.11.8. Locked sync checked 12 packages.

TDD initial command:

```sh
uv run --locked pytest -q tests/test_output.py tests/test_agreement.py
```

- First attempt had two fixture-import collection errors (exit 2); corrected
  import paths before accepting RED evidence.
- Observed RED: exit 1, 83 failures from missing output/agreement APIs.
- First focused GREEN: exit 0, 83 passed in 0.41s.
- First full suite: `uv run --locked pytest -q`, exit 0, 305 passed in 3.17s.
- Self-review added boundary cases. Observed second RED: exit 1, 2 failed and
  92 passed in 0.63s. Both failures exposed AGY `splitlines()` mishandling a
  literal U+2028 inside a string and accepting a U+001E record separator.
- Corrected LF-only JSONL handling. Focused GREEN: exit 0, 94 passed in 0.60s;
  full GREEN: exit 0, 316 passed in 3.35s.
- Refactored byte extraction to slice the original raw bytes. Final focused
  GREEN: exit 0, 94 passed in 0.61s. Final full GREEN: exit 0, 316 passed in
  3.43s. No failed or skipped tests were reported.

Final combined verification used `&&` between each command, terminal exit 0:

```sh
uv run --locked pytest -q tests/test_output.py tests/test_agreement.py
uv run --locked pytest -q
git diff --check
uv build --sdist > /tmp/triad-task2-sdist.log 2>&1
uv build dist/triad_dispatch_lib-0.1.0.dev1.tar.gz --wheel > /tmp/triad-task2-wheel.log 2>&1
uv run --locked python tools/verify_wheel.py dist/triad_dispatch_lib-0.1.0.dev1-py3-none-any.whl > /tmp/triad-task2-verify-wheel.log 2>&1
tail -n 4 /tmp/triad-task2-verify-wheel.log
```

The rebuilt wheel verified all 10 existing raw replay cases from an isolated
installed site-packages location. Package pin remained
`fcd96a15d18f3131c1f0111bdb10c3faceae34f8`, schema SHA-256 remained
`d755905ac60348542fc1dbbeb37b92bc3fab0a2dc34b7a1b454c935d0be04184`.
Final wheel SHA-256:
`82edba86ecdbcd3d5bf1a8b8bed7abe3789db53641b4e6e4b3d5bbab99a1db44`.

Exact-path staging and implementation commit (exit 0):

```sh
git add src/triad_dispatch_lib/output.py src/triad_dispatch_lib/agreement.py src/triad_dispatch_lib/json_input.py src/triad_dispatch_lib/errors.py src/triad_dispatch_lib/__init__.py tests/test_output.py tests/test_agreement.py
git commit -m "Add strict provider output admission and unanimous agreement"
git rev-parse HEAD
git status --short
```

Implementation commit contained exactly seven owned files; working tree was
clean immediately afterward.

## Self-review and limitations

- Terminal completion/timeout/transport/exit checks precede envelope extraction.
  Failure plus a valid payload cannot become approval. Bool exit codes and
  non-bool status flags are refused; only native final permits null exit code.
- Duplicate and escaped duplicate members, nonfinite numbers, invalid UTF-8,
  truncation and outer-envelope strictness retain existing AdmissionError codes.
- Ordinary finding text mentioning quota/auth remains ordinary data. No stderr
  phrase matching, AGY error taxonomy, retries, SDK/MCP or provider invocation
  was added. No provider or host tests/imports/edits occurred.
- Native Claude host-stripped output is supported; native marker/fence removal
  is deliberately not performed in this library. Pre-parsed verdict dictionaries
  cannot enter agreement as ballots.
- All selected entries count equally; acceptance classifications are not an
  agreement API input, so informational dissent cannot be excluded.
- Validation/build results are synthetic local macOS ARM64 Python 3.12 evidence,
  not real-provider execution or fresh Ubuntu compatibility proof. The wheel
  verifier's 10 cases cover the existing admission API; the 94 new source cases
  cover output/agreement behavior. Parent integration owns expanded installed
  four-route replay and host adoption.
- Existing `docs/status.md` is outside this task's allowed edit scope; the parent
  owns consolidated project status. No unresolved implementation concerns found.

# Library-owned Codex integration verification

Date: 2026-10-12. Runtime package remains `0.1.0.dev1`.

## Owner boundary

The owner selected isolated integration tests and then explicitly clarified that
all work and tests belong in `triad-dispatch-lib`. Existing Codex and Claude hosts
are read-only references: no source changes, host test execution, bootstrap,
default dependency changes or installation occurred. The Codex adapter here is
repository test support, not either host's runtime or formal custody engine.

Read-only comparison found matching verdict schema bytes and compatible six-field
invocation inputs. Existing host integrity preflight and error mapping would need
preservation during a later adoption. Those observations do not prove adoption;
this slice deliberately does not implement or exercise that host connection.

Current shared-spec main was rechecked at
`396a04dac310d5ff91dbe0a36982f7679aa00428`. Its changes since the pinned
`fcd96a15d18f3131c1f0111bdb10c3faceae34f8` concern packet accessibility (C79),
without changing the schemas or clauses used by this library.

## Deterministic evidence

TDD: the initial focused run failed the missing matrix and missing-wheel
pre-install refusal tests (2 failed, 15 passed). After implementation the full
suite passed 155 tests. Two further fault-injection cases showed that incorrectly
rendering a phase or its purpose could escape the matrix's own checks; both
failed before adding explicit phase/purpose assertions. The final suite passes
157 tests. A deliberately duplicate-erasing validator is also detected by the
self-test, so case labels alone cannot manufacture a successful run.

Local environment: Python 3.12.13, macOS 26.6.2 ARM64, uv 0.11.8.
The sdist-built wheel passes 10 raw replay fixtures and 54 synthetic integration
cases using the existing isolated install and actual site-packages validator.
The previous missing-wheel CLI minor is fixed: it exits 2 before creating an
environment or starting pip. Runtime library code, package version, dependencies
and canonical assets were not changed.

| Cases per phase | Expected result |
| --- | --- |
| SAFE, must-fix negative, uncertainty-only negative, Minor-only negative | 4 admitted unchanged, including the negative verdicts |
| Changed review ID, family, content digest, leg name, attempt | 5 binding refusals |
| Codex route changed from null to agy | Schema refusal |
| Duplicate, nested duplicate, invalid UTF-8, Markdown fence, trailing prose, overflow | 6 original-input refusals |
| Changed saved prompt or packet | 2 adapter refusals before admission |

The same 18 cases run under formal-plan, implementation-review and pre-merge.
Google route-swap semantics remain covered by library unit tests; the Codex
integration matrix does not pretend a non-null Codex route is schema-valid.

## Fresh native response evidence

Four new independent native Codex children were requested with
`gpt-6.1-sol`, medium, `fork_turns=none`. Each was given only a rendered prompt
path and its bounded library-owned synthetic packet, using neutral case labels.
Expected verdicts were recorded before dispatch and withheld from all children.
Read-only inspection was allowed; code/test execution, providers, web, prior
conversations, sibling packets and further agents were prohibited.

| Case | Phase / fixture | Observed final verdict | Installed admission |
| --- | --- | --- | --- |
| A | formal-plan, correct formula and endpoint tests | SAFE TO MERGE | Passed |
| B | formal-plan, incorrect discount-amount formula | MERGE WITH FIXES, plan.md:4 must-fix | Passed |
| C | implementation-review, correct pure function | SAFE TO MERGE | Passed |
| D | implementation-review, incorrect pure function | MERGE WITH FIXES, example.py:3 must-fix | Passed |

Both plan reviewers listed only `brief.md` and `plan.md` as inspected, not the
future `price.py` or `test_price.py`. Defect cases ignored instruction-like data
asking for SAFE and identified the wrong remaining-price calculation. Controls
did not invent blocking findings. These are four bounded observations, not a
general model-reliability or prompt-injection-resistance guarantee.

All four ended with observed `FINAL_ANSWER` notifications. Their exact final text
was saved as UTF-8 without an added newline or JSON reserialization and passed
through installed-wheel admission without repair or invisible retry. Capture
method is `parent-transcribed-final-text`; runtime model, effort and agent IDs
were `UNEXPOSED`. Observable task names are `/root/lib_codex_probe_a` through
`/root/lib_codex_probe_d`. No machine-attested provider bytes are claimed.

The runtime wheel built at `347599a1f04a378a30b0fa33ad6dbf585e43efec` has SHA-256
`b69bcc886965f5b42614d10ba02e7f0149563a12b77ec51d47d69a1120e55603`.
Original artifacts and receipts remain under ignored
`_runs/lib-codex-matrix-20261012-r1/`. Later test-driver phase assertions do not
change rendered native prompts or the installed runtime validator.
Earlier pre-merge control/defect observations remain in the
[prior evidence record](2026-10-12-codex-prompt-smoke.md); they were not rerun or
relabeled as new observations.

## Independent review and native CI

Native [CI run 38205026277](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38205026277)
passed at `03d0ecd4b7a6ec01c1c6e35957fd2ef18bd4910f`. Both jobs passed 157 source
tests, 157 unpacked-sdist tests, 10 installed raw replay cases and 54 installed
Codex matrix cases. Each reported the actual package/validator site-packages path.

| Platform | Observed Python / architecture | Wheel SHA-256 |
| --- | --- | --- |
| Ubuntu 24.04 | 3.12.15 / x86_64 | `93dfebf9aa77cf235d2b31acdae87afb6368b3e88ae4b2050862bed46c44a5be` |
| macOS 15 | 3.12.10 / arm64 | `4e3180321756dfc134175b5dd3ff62854c8920e808179d325235f46a93fecc86` |

The local reviewed-commit wheel also passed 10 replay and 54 matrix cases; its
SHA-256 is `d0a70dfc3cedfb4399cf2341f8fb405c2bb5efff6dce075b3661d0e3de3a1441`.
The local unpacked source distribution passed all 157 tests. Archive hashes are
observed identities; cross-platform byte reproducibility is not asserted.

Fresh whole-branch reviewer: requested `gpt-6-astra`, high, `fork_turns=none`,
range `c6dd981..03d0ecd`. No Critical, Important or Minor findings. The reviewer
passed 156 tests and excluded only the environment-creation test under its
no-install brief; parent and CI full runs include that test. It independently
checked four saved native artifacts and revalidated their complete verdicts.
Tracked fingerprints, index, HEAD and branch stayed unchanged. Read-only
containment was prompt-controlled; hidden runtime settings were UNEXPOSED.
Technical readiness does not authorize final merge.

Review scope rulings retained:

- Actual host adoption/execution/error mapping is excluded by the owner's
  library-only boundary. Host integration remains unproven and needs its own tests.
- Other renderer families and classification/aggregation are outside the current
  public API. Broader adoption needs those additional implementations.
- Formal custody, concurrent-change prevention and authentication against malicious
  package/manifest replacement are not provided. Consistency checks must not be
  treated as a security or custody boundary.
- Input-size limits remain the documented caller responsibility. Unbounded caller
  inputs can exhaust resources if that responsibility is ignored.
- General model reliability, injection resistance and hidden runtime identity
  cannot be inferred from four bounded parent-transcribed observations. Other
  scenarios may behave differently.
- The read-only reviewer did not repeat platform/installation checks. The parent
  verified the native CI evidence above; other Python/OS/architecture combinations
  remain unverified and need their own native runs.

## Native artifact identities

| Case | Prompt SHA-256 | Saved raw final text SHA-256 |
| --- | --- | --- |
| A | `a23928a4d0c8b9c32491ad2f687febb2c54924bbc9cbb6520ed422eab6950be6` | `987ab7800ae133d829911de40728a853f785bb77af9c3c8fe5922daf0a97343d` |
| B | `d6607f1a9df469be38d3f47aa78889af8d61302abf46819b2867610d3d5a7928` | `6ac1af6893d724a13e49d2a332f182afb9a47af97d37e398a330b9cdc125f1e2` |
| C | `41ad4a24b8b7067c182372b96b0c4bb15fded79ae447e16f8a121f8e9de813af` | `f9030242e71805e38d1f19238b285f2c1f60601f5faa33851f4a1b6204ce828f` |
| D | `f98c5b34440b52336515e1e20a9846e0649e2e7141f20bbaa0ec34348c9286e6` | `54fc0b30964024fc1cd7bcdb3306d4c9d29c026ab696ca8756ba1a26f7e14d59` |

# Minimal adoption follow-ups: implementation verification

The owner approved the [reviewed design](../superpowers/specs/2026-10-16-minimal-adoption-followups-design.md),
both Minor regressions/documentation, the same formal review and issue/PR updates.
The [plan](../superpowers/plans/2026-10-16-minimal-adoption-followups.md) keeps host
changes as guidance and excludes issue #5 and release-update-PR automation.

## Implemented boundary

Runtime commit `e7fdd4f` adds safe roster `.path/.missing/.document`,
`validate_transport_receipt` and `ReceiptError`, and packages the unchanged
canonical receipt schema in a fourth verified bundle. First-error choice, fixed
messages/codes, copies and validation order remain compatible. The new function
validates the parsed transport object only; host authenticity/currentness,
execution, installation, classifiers and model selection remain separate.

Documentation/test commit `050edb01a6b1cddddc6269b4d3356b4cc04471c8`
records the two Minor cases and [contribution dispositions](../requests/2026-10-16-adoption-followups-disposition.md).
The neither-block Google case retains `anyOf` and `.missing=None`; adding
`gemini={}` selects the route-required `agy` name. The record regression detects
both unsupported measured-row claims and stale absence claims. It deliberately
recognizes the existing/proposed measurement forms, without model/version pins
or a runtime classifier. Canonical R-GOOGLE text and vendor rows are unchanged.

Issue #9 is partial: no unknown-key spelling or input pointer is added. PR #8
retains attribution and S5/injected-asset limits; PR #11 leaves locking and race
verification to hosts; PR #12's three proposed rows/global-model claims remain
held for original evidence. No incoming PR is merged or issue closed here.

## Focused RED/GREEN and task review

- New runtime tests: 66 expected RED failures for missing interfaces, then
  66 passes. Existing affected roster/contracts/assets/driver suite: 320 passes.
- Installed-driver controls: nine expected RED failures before extending the
  probe/inventory; five wrong-behavior controls now detect skipped validation,
  wrong refusal code and wrong roster metadata.
- Record controls: six expected RED failures with a no-op checker, then 31
  focused record tests pass, including the combined proposed AGY/Codex wording.
  One test-only regex typo was corrected before the final GREEN run.
- Fresh independent Sol 6.1/high task reviews approved both tasks, with no
  Critical, Important or Minor findings. They inspected code/evidence without
  rerunning suites. These task checks do not replace the project formal review.

The first Task 2 preflight/RED used an escalated login shell without spelling
the required literal wrapper. It was repeated through `/bin/zsh -lic` before
implementation; later tests/mutations used that wrapper. No permission failure
was misclassified as a code defect.

## Local source, archive and wheel verification

Native local platform: macOS 26.6.2 ARM64. Runtime/test source is `050edb0`;
the checkout also contains the preserved release work and parent status draft.
These measurements precede the test-only CI correction below; runtime/package
implementation is unchanged by that correction. Each interpreter used
an independent environment, a neutral unpacked sdist and a wheel rebuilt there.

| Interpreter | Source | Unpacked sdist | Installed drivers |
| --- | --- | --- | --- |
| Python 3.12.13 | 1,143 passed; 6 deselected | 1,143 passed; 6 deselected | 4 passed |
| Python 3.14.6 | 1,143 passed; 6 deselected | 1,143 passed; 6 deselected | 4 passed |

The only local exclusion is
`test_cli_refuses_output_collision_and_preserves_artifacts`: six already-held
release-helper regressions. They were neither repaired nor deleted. These results
do not claim a green full checkout including that independent work.

Both runs passed locked environment setup, asset generation check, authoring
check, sdist build, archive tests/checks, wheel build and the existing four isolated
drivers (`verify_wheel`, `codex_smoke self-test`, `four_route_smoke`, and
`native_codex_smoke --self-test`). Installed verification confirms 31 exports,
four manifests/nine payloads, actual new API calls and both receipt error paths;
the recursion probe uses an explicitly synthetic local schema fault. Canonical
and packaged receipt bytes match. Dependencies/version floors remain unchanged.

| Python | sdist SHA-256 | Rebuilt wheel SHA-256 |
| --- | --- | --- |
| 3.12 | `80d616fefde6137a21e1433c4ddd7813ddf78414d79019348ffe4f539462a11c` | `7b9b26fd14377f5b2fe283ea5f79ae54bfa4180ff920c2a56b41a8573d2605d5` |
| 3.14 | `8d69b5f28977d7b99131cc82eec2885fd75306d3d16f7bf5a6cded9ddd9fe805` | `7b37ae42f9cf95d8fe58158d3558fe508e7936b8f65d5f4a1c626f200d56c57b` |

These are local candidate artifacts, not published release assets. Installed
synthetic tests do not establish real-provider execution or either host's adoption.

## CI-discovered test observation correction

Initial [CI run 38854284902](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38854284902)
at publication `68b6a26972858cf6333b68d553fc566664626388` passed all four
source suites and three complete jobs. The macOS/Python 3.12 unpacked-sdist
suite failed `test_matching_terminal_ack_does_not_wait_for_repaired_response[hash-True]`
with 1,101 other passes. This failed run is not counted as a green gate.

Independent diagnosis traced a fixed 80 ms observation in the unchanged test,
not evidence of a production acknowledgment defect. The driver acknowledges
matching terminal custody before response admission and returns from cleanup
after an acknowledged admission failure. A controlled 150 ms poll delay reproduced
the same test failure with that correct driver. The actual CI scheduling timeline
was not observed.

Commit `20278ce` replaces only the test's observation/drain block: use the existing
three-second bounded `wait_request`, retain whether progress occurred before
repair, and always repair/drain in `finally` before asserting. All six hash/UTF-8/
missing × ordinary/cleanup cases and their `failed` versus `timed_out` assertions
remain. Runtime code, provider deadlines and custody contracts do not change.

The delayed correct driver passes the conditional observation; the ordinary case
still completes as `failed` before its one-second deadline. A deliberately broken
driver that acknowledges only after response admission still fails the pre-repair
assertion after the bounded wait, then drains both callbacks. These controlled
observations establish that the correction retains the regression's distinction.
The six existing focused cases pass on Python 3.12.13 (4.64 s) and 3.14.6
(3.81 s), with 112 unrelated cases deselected in each run. A new complete native
matrix and the planned full formal review assess the corrected publication head.

## Publication and formal review boundary

The scoped publication branch uses main `dac1af62297402a0078a616e8e194c7a69cafe18`
ancestry plus this slice's exact selected blobs. An alternate index preserves the
active checkout, index and held edits. It excludes the release delivery plan/design,
`tools/release_artifacts.py` and `tests/test_release_artifacts.py` entirely.
Its native Ubuntu 24.04/macOS 15 × Python 3.12/3.14 CI therefore runs complete
source/archive suites without the local test exclusion. Exact publication SHA,
asserted checkout identity and per-job results are recorded with the Draft PR.

After the candidate freeze, the project public v2 review uses Opus 5.5/xhigh,
Sol 6.1/xhigh and Argon/high, with a separate nonvoting Astra/high comparison.
Each has 2,400 seconds and authorized current official web research. The managed
packet includes the full publication diff, exact source blobs, local and CI
evidence and frozen contribution inputs. Terminal observations, integrity,
findings/dispositions and export/cleanup outcomes are retained with the PR after
collection; this pre-review record does not claim formal approval or native CI
success before those operations finish. Native hidden model/effort and read
containment remain explicitly unexposed/prompt-controlled where applicable.

Runtime/package support changes remain bounded: 122 additions/7 deletions across
runtime/package tools/config, including the 47-line installed probe; generated
assets add 104 lines. Tests add 338 lines and remove twelve, covering the refusal
matrix and fault controls. Task 2 documentation adds 234/removes 14 lines; the
growth over the initial estimate records complete API contracts and three
contributions' distinct evidence limits, without new infrastructure.

Main merge, library release and host update/install remain separate decisions.
Package version is still unpublished `0.1.0.dev4`.

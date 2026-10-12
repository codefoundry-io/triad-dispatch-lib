# Supervised native Codex callback verification

Date: 2026-10-12. Package: unpublished `0.1.0.dev2`.
Driver implementation: `9d6f8a0db65261d765d05c492f33aa5462bb49ce`.

## Scope

The owner approved fresh Codex response verification and bounded parallel review
with separate perspective investigations. All work stays in this library
repository. The new [driver](../../tools/native_codex_smoke.py) supervises a file
exchange around the existing installed `run_review` / `run_investigations` APIs.
The parent task creates native children using `collaboration.spawn_agent`; the
library and driver do not spawn agents or provider processes.

No runtime source, canonical assets, package metadata, dependencies, consumer
repositories or shared specification changed in this slice. The four-route core
remains described by the [previous verification](2026-10-12-four-route-core.md).

## Actual native observations

All six fresh independent children requested `gpt-6.1-sol` with `medium` reasoning
and no inherited conversation. Each received its published prompt and the same
two complete bound files for its round, without expected outcomes or sibling
results. The parent retained original final strings without rewriting verdicts,
stripping markers or retrying toward a desired answer.

| Round | Entries | Actual result | Library result |
| --- | --- | --- | --- |
| Correct arithmetic | `codex-a`, `codex-b`, `codex-c` | Three `SAFE TO MERGE` responses | All admitted; integrity true; agreement true |
| Defective arithmetic | `codex-d` | `MERGE WITH FIXES`, one must-fix at `example.py:2` | Admitted negative result; integrity true; agreement false |
| Separate investigations | `perspective-boundaries`, `perspective-tests` | Two ordinary text responses | Both completed; integrity true; no agreement field |

The correct fixture computes `cents * (100 - percent) // 100`; the defect computes
`cents * percent // 100`. Both briefs specify nonnegative integer cents, integer
percent in 0..100 and floor rounding. The defect reviewer identified 1000/20
returning 200 instead of 800 and the reversed endpoints. Boundary analysis also
identified why subtracting a floored discount gives incorrect remaining-price
rounding. Test-design analysis supplied discriminating cases and explained why
the 50-percent example alone misses the defect.

The correct round shares review ID
`native-dev2-63b168cf90b9464e9cf78a2719fa9ac6` and content digest
`68ef5f4a362ff76a0f6da55a100ea6d75758147190bdfb58ea5ca81a75befd01`.
The defect round uses a fresh review ID
`native-dev2-4a3430a43357409383f38a6ef420ceee` and digest
`468acf7dc744e9eba9193a3e5e6132c410017562d2315e660ad59b3ddfb252ee`.
All formal responses pass the original schema and six binding checks.

For the correct round, the ordered callback trace is start A, start B, finish A,
finish B, start C, finish C. Peak active callbacks are two, and outcomes retain
input order. A single native tool snapshot observed A/B running together while
the third request was absent. C was spawned only after its request appeared when
the first receipts released slots. The investigation round also has peak two
callbacks and one native snapshot showing both children running. These observations
establish callback limits and supervisor-visible overlap, not backend scheduling.

All six children delivered terminal final responses and all three driver commands
returned exit zero. Formal report hashes measured before and after investigations
are identical. Report creation itself is not approval: the defect driver exits
zero while recording agreement false.

## Installed artifacts and custody

The three actual rounds used isolated wheel installations, Python `-I`, neutral
child working directories and verified paths for all 27 exported runtime APIs
under their respective temporary `site-packages/triad_dispatch_lib` prefixes.
Local native environment: macOS 26.6.2 ARM64, Python 3.12.13, uv 0.11.8.

- sdist SHA-256: `addcfa258c85c223aea741d7022d0eecb215b8b9ab685e5743562ec76d5db416`
- wheel SHA-256: `b89d07594f7173393949eca07c5525cfa1709a36857c543c8259934b82c548eb`

The parent writes the exact tool-returned final string as UTF-8 `response.txt`,
then atomically publishes a bound terminal receipt. Fresh integrity checks bind
config, wheel, packet, prompt, request, response and receipt hashes and unique
supervisor-visible child identities. Review `ProviderOutput` carries
`carrier="native-final"`, `exit_code=None`, `completed=True`.

| Entry / child suffix | Response bytes | Original response SHA-256 |
| --- | ---: | --- |
| `codex-a` / `native_live_a` | 968 | `992e88d8a931ef48c7d6aa61d6ba27e31737ab2598e967d343ec4df14332b699` |
| `codex-b` / `native_live_b` | 995 | `9c6cb40b1194328c570ff4c9798ee43af643a407cc8c11969f2d63496af7dfce` |
| `codex-c` / `native_live_c` | 1002 | `0f4cd61a564d3f764493796e46167fdff334b8a63fc4e2f14fe17518c9e6e38f` |
| `codex-d` / `native_live_d` | 1313 | `cd9e8825cc05f64aa9d3dfcc058d383f145e35b04cbffc72d585ce595d567e1a` |
| `perspective-boundaries` / `native_live_e` | 878 | `bba44f95e99cfb31891dff3c38c62f1f20b8cdb51b9ca37dc375988ff1358950` |
| `perspective-tests` / `native_live_f` | 1033 | `3ab5d60175829d90bc589cffc62ab98b94a1b1dfb8091ec41964b554ce8ae7e2` |

Local evidence is retained under ignored
`_runs/native-codex-callbacks/live-20261012T074819Z-901ce291/`: three configs,
bounded packets, pre-dispatch expectations, manifests, prompts, requests,
original responses, receipts, reports, driver logs and native observations.
`artifact-hashes.json` indexes these files; its SHA-256 is
`04a266e8abef7011fa66eb59a332adadb6dca13550b21f5a8076930b08317b9e`.
`evidence-summary.json` SHA-256 is
`3abd2a2c0180f9937158b399cd4b48e33ce71faca284ce159b0b2e0b90a470cd`.
These local artifacts are evidence, not shipped dependencies or public replay
fixtures. Reproduction uses new run directories and fresh native children through
the [README protocol](../../README.md#supervised-native-callback-experiment).

## Regression verification and review

The focused driver tests progressed from missing-driver RED to 35 passing tests.
They exercise real async callbacks and file exchange, including queued third
entries, invalid/stale/duplicate receipts, changed inputs and captured bytes,
all-preflight-before-publication, dissent, cancellation acknowledgements and
ordinary investigations. Deliberate always-approve and hash-bypass mutations
were both detected in temporary copies.

Task review found that cleanup retries could replace the original identity owner
and erase duplicate evidence. The fix retains first ownership and latches the
violation. A regression verifies repeated invalid acknowledgements keep cleanup
waiting, a later unique terminal acknowledgement settles it, and integrity stays
false. Independent scoped re-review found no remaining issues.

Final local source and unpacked-sdist suites each pass **399 tests**. The rebuilt
installed native synthetic exchange passes. The prior wheel at the initial driver
commit also passed the existing 10 raw replay cases, 54 Codex adapter cases and
four-route matrix (nine scenarios, 51 prompt profiles); the subsequent fix changes
only the new driver and its tests.

[Native CI run 38222619438](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38222619438)
passed on reviewed head `99e8e7f44a8ee6d75516f2905185871f643d3e94`:

| Native runner | Python | Source suite | Unpacked-sdist suite | Installed wheel |
| --- | --- | --- | --- | --- |
| Ubuntu 24.04 x86-64 | 3.12 | 399 passed | 399 passed | All four drivers passed |
| macOS 15 ARM64 | 3.12 | 399 passed | 399 passed | All four drivers passed |

Each runner verifies 10 raw replays, 54 Codex adapter cases, nine four-route
scenarios, 51 prompt profiles and the new synthetic supervised exchange with
three review entries, dissent and an ordinary investigation. These CI exchanges
use synthetic responses, separately from the six actual macOS observations above.

Final independent whole-branch review (`c6dd981..99e8e7f`, requested
`gpt-6-astra`/`high`) found no Critical, Important or Minor issues. It independently
checked all 44 indexed evidence-file hashes, response/report correspondence and
the installed API paths. Review was prompt-controlled and read-only; pre/post
HEAD and tree fingerprints matched and the checkout stayed clean. The reviewer
did not inspect external CI; the root separately verified the successful run and
retained its complete logs. Subsequent edits record these results only.

## Limits

Capture is a parent copy of the tool-returned final string, not independently
attested provider wire bytes. Child identity means `/root/<task_name>` exposed by
the supervisor; opaque backend IDs and effective model/reasoning settings remain
`UNEXPOSED`. Timestamps are parent observations, including shared pre-dispatch
batch timestamps, not backend start/end measurements. Read-only child scope is
prompt-controlled, not a newly enforced provider sandbox.

Actual native cancellation/timeout was not exercised: all six children completed.
Synthetic tests verify cancellation propagation and cleanup waiting, but the
parent must interrupt and await its owned native child in a real cancellation.
The cooperative driver can wait indefinitely if its supervisor fails to supply a
valid terminal acknowledgement. Native Codex responses were observed on macOS
only; Ubuntu CI runs synthetic exchanges, not native agents.

No existing host execution/adoption, host migration guide, SDK/MCP/provider CLI
experiment, global install, final merge, release or package-index publication is
part of this slice. `openai-codex` remains deferred and the Gemini workaround is
unchanged. This is ordinary Codex verification, not formal multi-family admission.

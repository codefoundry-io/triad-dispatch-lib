# Gemini packet availability (C79)

## Evidence and cause

- Shared main inspected: `fcd96a15d18f3131c1f0111bdb10c3faceae34f8`.
- [B issue 42](https://github.com/codefoundry-io/triad-codex-dispatch/issues/42)
  reports Gemini CLI 0.63.0, B 0.2.559 / `6cc7271f`, guarded-worktree:
  native `read_file` rejects external `shared/TASK.md` and `shared/REVIEW.diff`
  with `Path not in workspace`. Vendor/wrapper exit 0 and schema-valid
  DO NOT MERGE describe missing coverage, not a transport failure.
- B `bin/review_round_v2.py` selects product cwd and renders packet paths from
  the separate prepared directory. `bin/gemini_wrapper.py` only forwards raw
  `--add-dir` to native `--include-directories`, while refusing raw extra roots
  for formal review. Provider-free version/policy preflight cannot prove reads.
- A `1de943af4436b3eca2aea903d05c223c8d56f92d`:
  `.claude/skills/triad-cross-family-review/lib/review_scratch.py` creates its
  worktree inside the packet directory (3208-3213) and writes brief/patch/history
  inside that worktree (3619-3633). `lib/roster_v2.py` launches from it (845-850,
  905-920). A's Gemini wrapper has no include-directories fix to copy.
- Official [Gemini CLI configuration](https://geminicli.com/docs/reference/configuration/)
  documents `--include-directories`; exact task-local 0.63.0 `--help` exposes it.
  The owner's global 0.60.0 installation is unchanged. Native read verification
  and the generated formal call are recorded separately below when run.

## Bounded implementation and preserved behavior

R-PREPARE already requires available packet inputs. Clarify its observable
meaning and add C79 before changing host code. Keep B's existing external packet
lifecycle; moving custody or embedding the entire diff would change more scope.

1. Add a failing actual-wrapper/producer regression for the external packet.
2. Propagate the exact `prepared_dir` only to guarded Gemini launch controls,
   using a dedicated internal wrapper option. Bind the value through the existing
   preflight digest, adapter and allocation; reject invalid or changed controls.
3. Verify packet reads, related product discovery, rejected broad/sibling grants,
   unchanged negative-result collection, and existing raw/prepared-directory paths.
4. Verify the provider-free 0.63 file-tool behavior and review the bounded change.
   The owner will test authenticated Gemini inside the company after release;
   that live test is not a prerequisite for this release and remains NOT RUN here.

Actual production scope: four Python modules, 39 additions and 5 deletions (net
34), plus focused regressions and short user/reference documentation. No prompt clause,
verdict schema, authentication, model/effort, user setting or native-host change.
The packaged read-only policy and exact executed-command custody remain intact.
Changing these launch controls requires a fresh review basis; no hand-edited
same-basis argv or relabelled old verdict is admitted.

On A: retain co-location and exercise C79 at its next conformance run; no host
rewrite is requested. On B: fix the confirmed missing propagation. Other-host
review is requested on the same specification commit; the owner has authorized
B to continue independently under settled contracts.

## Verification status

The task-local official Gemini 0.63.0 package's actual `Config`, `WorkspaceContext`
and `ReadFileTool` reproduce `path_not_in_workspace` without the packet root, read
the marker with only `shared` added, and still deny an unrelated sibling. The
probe uses the installed entry point's core chunk `chunk-RWBXO4OP.js`; network is
disabled. It applies the native pending-directory registration loop without full
Config initialization and replaces only the storage temp getter with an isolated
fixture path. It therefore proves native file-tool behavior, not CLI parsing,
authentication, a model call, or effective enterprise policy.

B implementation: [PR43](https://github.com/codefoundry-io/triad-codex-dispatch/pull/43),
commit `d0f32ad89be037884d39a48bfcec123358e8f4c3`. The dedicated intended RED
reproduced the original missing packet access. GREEN: 148 focused tests passed,
4 route skips; 2,462 full tests passed, 4 skips; four skill validators passed on
macOS arm64, Python 3.12.13. The generated formal producer, preflight, wrapper,
subprocess transport and collector run with a deterministic file-reading vendor
boundary. These regressions prove propagation and result accounting; native
behavior and authenticated company execution remain distinct evidence.

The immutable archive of that same B commit also passed 2,462 tests with 4 skips;
335 tracked files and the 52 packaged hash targets match the committed bytes.
Original untracked documents were preserved. This does not claim a clean original
checkout, Ubuntu verification, installation or fresh-session exposure.

At the owner's request, final reviewers may use web research and version-pinned
[Gemini CLI source](https://github.com/google-gemini/gemini-cli/tree/v0.63.0).
The option parser and CLI configuration are in `packages/cli/src/config/config.ts`;
`packages/core/src/config/config.ts`, `utils/workspaceContext.ts` and
`tools/read-file.ts` provide the native registration and read-path checks.
This source evidence remains distinct from authenticated service behavior.

Final source review `triad-gemini-packet-20261012-r2`: owner-selected Sol/xhigh,
Astra/high and AGY Google Pro/high all SAFE with `ROUND_INTEGRITY_OK` and shared
digest `dc0a0f569fac7075abb05e85e0ff411282702286c335fbbbbd277fbd848ec438`.
Web and official source lookup were explicitly authorized. Google's Minor
comment suggestion concerned hypothetical future native changes; no current
defect was reproduced, so it was declined without changing source. This result
uses the existing owner composition after confirmed Claude quota exhaustion;
it does not claim a fixed four-leg ledger admission or successful Claude call.

A current read-only source inspected; runtime C79 NOT RUN. The owner requested
implementation and release with actual Gemini validation afterward in their
company environment. No live Gemini success or change to A, user settings,
installation or tagged spec adoption is claimed.

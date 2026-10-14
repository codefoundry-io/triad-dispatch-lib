# Superseded terminal contract — historical evidence only

Replaced on 2026-10-11 by the owner-approved vendor invocation contract.
This is not current implementation guidance. Original source: bc95f31.

<a id="R-TERMINAL"></a>
Transport success requires: process exit collected, all reader threads joined without error, the owned process group
reaped, stdin delivery confirmed. A settings-guard release failure after a completed transcript is still a failure; the
transcript is preserved. A display-mirror failure is distinct from a failure to capture the result.
A dispatch lasts from the moment the wrapper starts it until the engine's last signal check (the end of its last vendor
run), every attempt and the gaps between them included (server-capacity backoff, schema-repair turns), whether or not a vendor child is running. A
wrapper signalled (SIGTERM or SIGHUP) anywhere inside a dispatch reaps any owned group and ends as a terminal failure:
token `unknown`, exit 1 (`EXIT_CLI_FAIL`), the answer withheld, and an extraction error naming the signal (`wrapper
interrupted (<SIG>)`), recorded like any failed dispatch. A signal outside a dispatch — before the wrapper starts it
(argument checks; on B also its preflight probes) or after its terminal record — leaves no record; on A a pre-dispatch
vendor probe runs in the record-only mode a dispatch uses (below). On B: `_run_once` records the
signal and `_mark_signal_failure` sets that shape (`bin/_common.py:1400-1452` @ `7f75863`); the record-only handler is
installed inside `_run_once` only (`:1425-1441`), so a signal between attempts exits 143 with no record (DL-70). On A:
every window of a dispatch ends in that shape with its summary, audit row and run-log — after the spawn, in the wait,
inside the timeout arm's group kill (the SIGKILL escalation kept) and between attempts (`_terminal_signal_to_exit`,
`3rd-Agent/wrappers/_common.py:3441-3448`; `_run_once`, `:3559-3585`, `:3924-3949` @ triad `bf38f60`). A signal after
the engine's last check is not consumed, and the hosts differ: on A the handler only records once a dispatch began, so the
completed answer is published and recorded `ok` (`_terminal_signal_to_exit` @ triad `e40001d`); on B the default handlers
are restored when the run returns, so a later signal ends the process at 128+signum with no record (`bin/_common.py:1418-1441`
@ `7f75863`). On A a signal during ANY pre-dispatch vendor probe (agy `--version`, gemini's review preflight) ends in the interrupted-run record (summary, audit row, run-log written) once the bounded probe returns, never a bare 128+signum exit (@ triad `3fde8d6`, `7e9e1fb`); at triad `e0b15f1` A also runs an agy model-catalog call before a pinned review dispatch, which reaps its own group on a cut-short or a normal exit (`3rd-Agent/wrappers/antigravity_wrapper.py` `_model_catalog_refusal`) — code that goes under R-MODEL (DL-116); the gemini preflight and
`agy --version` are plain `subprocess.run` calls with no group of their own, so a helper they might fork is not reaped (a
recorded limit — no run has shown one; `3rd-Agent/wrappers/gemini_wrapper.py` `_probe`, `antigravity_wrapper.py` `_probe_agy_version`).
A failed stderr write drops that one line, never the answer or the exit, and a dropped line is never written later; a
stderr closed at start drops every line. A full non-blocking stderr drops the line at once, and a blocking stderr whose
reader stops draining blocks the wrapper — both are recorded limits, not bounded (no run has shown either; On A `log` @
triad `e40001d`; B writes with a plain `print`, `bin/_common.py:322-324` @ `7f75863`). A caller missing a summary or
read-audit custody line refuses to collect — fail closed. A failed
host record write (audit row, run-log, debug log) never changes the provider result or loses the answer, on both hosts (A
one stderr line, and A's record seam catches any exception, not only an OSError — `_dispatch_record` @ triad `e40001d`;
B `audit()` returns False, `bin/_common.py:2139-2153` @ `7f75863`); on A a review attempt whose run-log
was lost carries no receipt, so it is INVALID at collection and retried, never agreed. Verdict
precedence, both hosts: a timeout verdict stands over a signal (an interrupted run is `unknown` / 1 and never retried);
frozen R-AUTH has no carve-out for a signalled attempt, so on A a signalled codex or gemini run's captured output
goes through the auth-carrier rung first and a carrier STOP ends `oauth-env` / 65 (`_common.py` `_run_once` @ triad
`fdd7029`; gemini's exit code 41 is read inside that rung, @ triad `8909103`; B: DL-95); a recorded limit on A: a
signalled agy run's carriers are not read (no measured agy carrier capture) — `unknown` / 1, never retried. A probe
that recorded a signal keeps the record-only mode until its refusal record is written, so a second SIGTERM / SIGHUP in
that window is recorded too (frozen C1; `gemini_wrapper.py` preflight, `antigravity_wrapper.py` `--version` probe, and
its catalog call until that goes, DL-116, @ triad `0115727`); a signal replaces a stdin-delivery or reader failure; a
stdin-delivery or reader failure replaces a vendor exit code of 0 (A `:3924-3949`; B `bin/_common.py:1433-1437`,
`:1663-1679` @ `7f75863`). A run whose output readers did not all finish without error fails closed at a vendor exit 0
on both hosts, with different tokens (a fact): On A `truncated-answer` / 65, the captured prefix kept for the run-log and
never returned (`3rd-Agent/wrappers/_common.py:3886-3889`, `:3916-3920` @ triad e0b15f1), and A's agy driver applies the
same at any vendor exit (`antigravity_wrapper.py:1424-1455`); On B `unknown` / 1 with the transport failure recorded and
classification skipped (`bin/_common.py:1641-1674`, `:1680-1684` @ `7f75863`), applied also to a transport setup failure
at any exit. At a nonzero vendor exit, A's codex / gemini runs and B's runs keep the vendor's own diagnosis. A signal between attempts (a server-capacity backoff, a schema-repair turn) spawns nothing:
the previous attempt's record, with its captured evidence, carries the signal failure, and the agy driver adds no
attempt to the read audit for it (On A: `_common.py:3561-3585`, `3rd-Agent/wrappers/antigravity_wrapper.py:1061-1072`;
B has no handler there, DL-70). A helper outside the owned process group that still holds the child's stdout keeps
that pipe open; cleanup closes only the pipes no live reader still blocks on, so it stays bounded (A `_common.py:3749-3758`;
B `bin/_common.py:1623-1630`).

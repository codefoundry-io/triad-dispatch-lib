# Single external CLI invocation — replacement guidance

Owner approved the recommended next-unit proposal by "진행" on2026-10-11,
after the briefing described removing capacity restarts and schema-correction
calls, the earlier transient recovery loss, and preserved explicit retry.
This is a replacement contract for both hosts, not a request to copy B internals.

## Evidence and current behavior

B25372be `bin/_common.py::run_cli_with_retry` repeats capacity failures up to
two additional calls, sleeping15/45seconds, and can call again after failed
local schema validation. Ordinary/raw Claude and Gemini use it. Claude's native
structured-output path and formal Google already avoid these outer restarts.
Read-only A1de943af `3rd-Agent/wrappers/_common.py::run_cli_with_retry` at2862
has the same common loops; its native Claude spawning remains A-owned.
Shared main was fetched at3afc4d7; draft3061281; PR13 had no newer comment after
6101997909. A's code is evidence of current behavior, not design authority.

## Selected outcome and tradeoff

R-TERMINAL/C78 now return the first capacity/schema failure using existing
64/66 outcomes. Vendor-internal request retries remain the vendor's concern.
No claim is made that every vendor retries every failure. A transient error
previously recovered by another automatic CLI invocation can now surface sooner;
the user/leader diagnoses it and explicitly retries if warranted. Valid output,
auth STOP, known failure classification, exact input and review bindings remain.
Do not add a retry switch, scheduler, error taxonomy, timer or replacement agent.

Preflight probes are not inference calls. Manual failed-entry retry under
R-RETRY remains; a completed review finding is not a provider failure. Native
host legs, model/effort, user settings, AGY profiles and cleanup are outside this
bounded implementation. B preserves its helper signature and zero-valued record
fields for existing consumers while removing the loops; no schema migration.

## Verification and adoption

Before implementation, use real local subprocess fixtures to count launches
and capture exact prompts for capacity, schema-invalid and success controls.
Include auth, transport and formal-path regressions; independently review the
complete change. Local fixtures establish wrapper behavior, not current vendor
conformance. Both hosts record their own implementation/test status in C78.
No host completion, adopted revision, merge, installation or release is claimed.

## B verification and adoption status

B implementationf4d6331 is on its existing development branch. The common
driver removes automatic capacity/schema replay; production delta+91/-184,
net93lines removed. Its historical helper signature and zero-valued counters
remain compatible. Initial prompts, parsing, classification and local validation
remain; no new scheduler, provider setting or native-host change.

Fresh dedicated RED5failed/4passed measured3capacity invocations and2schema
invocations. A previous RED had two incorrect success-control assertions; those
were corrected to the documented dictionary result before the valid RED and
before production edits. Fresh dedicated GREEN397focused/2369full passed,
4skipped; four validators and diff check passed. Tracked/nonignored source and
HEAD/status matched; exact temporary allocations were removed. Two exit-code
comments were then aligned with executable AST equality. Native macOS26.6.2
arm64/Python3.12.13; no Ubuntu, universal vendor or installed-release claim.

R1 could not complete because Claude's original terminal JSON reported an actual
monthly spend limit (is_error=true, api_error_status429). B preserved unknown/
exit1 and the original result; this is an observed diagnostic classification
limit, not evidence of an A native-leg defect. No billing/settings/classifier
mutation was made. The owner had authorized excluding Claude on actual quota
exhaustion. All started siblings finished, final integrity matched and exact
stages were cleaned. No R1 approval was reused.

Fresh R2 used the owner-selected Sol/xhigh+Astra/high+Google Pro/high roster on
one new basis. All three SAFE; ROUND_INTEGRITY_OK; every terminal handle consumed,
custody exported and exact stages removed. This task selection does not change
the common default roster or imply a fixed workspace-ledger admission.

Two verified nonblocking Minors remain disclosed: duplicate deterministic Claude
answer extraction already existed in25372be; three authentication troubleshooting
paragraphs still say capacity retry, while explicit one-call policy and executable
behavior are correct. Neither is a functional blocker or an automatic new backlog;
the owner's substantial-defect-only wording limit ends iteration here.

Evidence: B workspace `_runs/infra/20261011-single-cli-call/` and
`_runs/reviews/triad-single-cli-20261011-r2/`. A remains read-only1de943af with
the common loops; its implementation and tests stay A-owned/pending. Shared main
was re-fetched at3afc4d7; PR13 had no newer reply after6104736069 before review.
This publishes B evidence in the shared draft, not a new adopted revision,
installation, main merge, release or proof that A is complete.

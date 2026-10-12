# Host profile and investigation evidence amendment

> **Historical record; its REVIEW no-web statements are superseded on 2026-10-03.** REVIEW web now follows the owner's
> standing authorization in current [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](owner-register.md#D-REVIEW-LEGS-20261003)); the no-web posture applies only to a false
> condition. Investigation web is allowed for every investigation and dispatch leg
> ([R-INVEST](../reference/review-rules.md#R-INVEST)), not only on an explicit authorization.

Implementation candidate, not a tag, installed adoption or live conformance.
Latest remote main checked before authoring: `2eb883fee59e66556ee7c7f87189b38231136622`.
Authority: the verbatim D-B1/D-B2 answers in
[the owner follow-up](2026-09-20-owner-follow-up.md). No new owner choice is inferred.

## Evidence and current behavior

A `92c8afd`, `3rd-Agent/wrappers/policies/gemini-readonly.toml`, consumes the
existing 100/200 payload. B `8fd5245`, `bin/policies/gemini-formal-readonly.toml:6-37`,
uses a 999 allow/deny set and 998 catch-all, including explicit Plan Mode transition
denies and canonical search. Its allow set still includes two web tools. Replacing
B with A's profile would discard existing B protections. The owner chose separate
profiles when usage differs.

Gemini CLI v0.60.0 primary sources:
[policy loading](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/policy/config.ts),
[policy engine](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/policy/policy-engine.ts).
These establish source behavior, not effective runtime enforcement or admin-policy
attribution. Existing V1–V5 stay NOT RUN.

The investigation prompt's order prose currently requires permanent AS SENT
prompt storage; C29 also assumes every invocation has a persistent read audit.
The owner rejected a new permanent evidence store. B's current masking and
failure-only evidence remain intentional. A's already existing audit/hook remains
its host capability; B does not activate a dormant hook for symmetry.

## Proposed aligned behavior and host effects

- Keep A's `gemini-readonly.toml` bytes and verification manifest unchanged.
  Add `gemini-readonly-b.toml` for B. Each host vendors its selected complete
  payload byte-for-byte with an adjacent digest. B moves only the two web tool
  names from its allow set into its explicit deny set; existing reads, Plan Mode
  transition denies and catch-all remain. No overlay loader or merged policy engine.
- Keep the actual `web-evidence` clause bytes unchanged. Append it last only on an
  explicitly authorized Google web INVESTIGATION, with route-specific tool names.
  Ordinary audit/redaction/retention rules apply; no separate permanent prompt or
  fetch log is required. A URL in prose still does not prove a fetch. Unobserved,
  incomplete or unverifiable web evidence remains UNSURE. Test prompt assembly and
  use bounded, task-authorized live evidence to verify actual fetch interpretation.
- C28 records resolved prompt-file and child-cwd identity in existing success
  summary/audit surfaces using the host's existing redaction mode. Refusals identify
  the candidate through that same masking policy. No second logging subsystem.

Preserve both authentication boundaries, REVIEW no-web, raw custom prompt/schema,
authorized read roots, wrapper entry-cwd resolution, existing validation, normal
failure evidence and all cleanup ownership/retention rules.

## Verification and sharing

Authoring tests validate B payload invariants and its exact digest, and assert A's
existing payload remains unchanged. B's separate manifest retains live checks as
NOT RUN. B implementation must add offline policy/preflight/argv tests and complete
its ordinary source behavior, platform and review gates. No stub proves service
behavior, and no successful exit proves complete fetched page content.

Claude leader: review this entire commit, including C15/C28/C29, R-CONTAIN/R-INVEST,
the investigation order prose and units. Keep A unchanged during B-first work;
report any actual conflicting retained requirement before adopting this candidate.
B's implementation/verification and source-line handoff follow separately. The
specification owns policy payloads and shared clause text; host instructions point
to them without copying normative explanations.

Budget: host production +0/-0; approximately 160 contract/manifest/test lines and
120 documentation lines. This materializes settled answers; it adds no runtime
service, scheduler, configuration layer or logging store.

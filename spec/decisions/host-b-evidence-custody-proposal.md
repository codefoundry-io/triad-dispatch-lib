# D-B2: bounded evidence custody proposal

> **Historical record; its REVIEW no-web statements are superseded on 2026-10-03.** REVIEW web now follows the owner's
> standing authorization in current [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](owner-register.md#D-REVIEW-LEGS-20261003)); the no-web posture applies only to a false
> condition.

Status: the private-store proposal below was superseded by the
[owner's no-new-permanent-store decision](2026-09-20-owner-follow-up.md#d-b2-no-new-permanent-web-investigation-evidence-store).
Do not implement the historical recommendation. Common wording alignment remains
a separate cross-host task. Original proposal remote main inspected at
`2eb883fee59e66556ee7c7f87189b38231136622`; B at `ba6344b` plus P1; A at
`92c8afd500499d8736afcc28b39a87a4f87fed50`. No A files change.

## Confirmed conflict

C28 requires resolved paths in success summary/audit. C29 requires the exact
sent investigation prompt and fetched-page evidence. B's existing hardened
audit masks prompt/path text, and ordinary `prompt_head` is truncated to 200
characters. Failure-only temporary run logs cannot satisfy successful custody.

Source evidence: B `bin/_common.py::load_prompt_text`, `validate_wrapper_cwd`,
`_audit_redact_enabled`, `_redact_prompt_args`, `audit`; the existing invariant
in `tests/test_effective_cwd_receipt.py:52-60`. A has the same relative-path
refusal at `3rd-Agent/wrappers/_common.py:1148-1190` and audit masking at
`2628-2659`. A's C29 append path at `antigravity_wrapper.py:1381-1393` and
`tests/unit/wrappers/t49-agy-web-evidence-c29.sh:93-101` prove the ordinary
unredacted path only. These facts do not authorize bypassing hardened mode.

## Recommended narrow contract clarification

1. Preserve current hardened ordinary-log masking. C28 records exact resolved
   paths when redaction is off; when it is on, record the existing redacted
   representation and explicitly identify the limit. Relative-path acceptance
   never requires the caller to disable hardening or add an evidence directory.
2. For an explicitly web-authorized INVESTIGATION, require a caller-designated
   evidence destination before claiming complete C29 evidence. Preserve exact
   sent prompt bytes, clause digest and bounded fetched-page records there with
   exclusive private-file writes. This is an explicit local custody destination,
   not a global settings change or new shared schema/framework.
3. Ordinary audit references the evidence identifier/digest and custody state;
   its existing redaction still applies to paths and prompt text. No full prompt
   is added to the general durable audit. Without the authorized destination,
   do not claim that hashes alone satisfy exact-prompt evidence or that an
   unobserved URL fetch occurred. Preserve ordinary raw INVESTIGATION behavior.

The alternative is to explicitly weaken C29's exact-byte requirement to a
digest/redacted-state record. That is smaller but does not retain the agreed
reproduction evidence, so it is not recommended. Silently writing full text into
ordinary hardened logs is not an acceptable implementation shortcut.

## Impact, preserved functionality and verification

Both hosts need the same custody meaning; each keeps its own adapters. A's current
append behavior stays and later gains the same hardened-mode evidence treatment.
B adds only process-cwd path normalization and explicit web-investigation
custody under their separate functional plans. REVIEW still cannot use web;
raw prompts, optional arbitrary schemas, current redaction, auth boundaries,
exit behavior and no-provider-before-argument-validation remain intact.

Verify relative process cwd versus child cwd, missing/nonregular/invalid-UTF8/
empty/outside-root inputs, success audit in both redaction modes, exclusive
evidence creation, exact sent prompt with the clause last, evidence failure
without false conformance, and fetch-record coverage. Use synthetic providers
first. Live vendor checks remain separately described and cannot retroactively
mark V1-V5 or either host conformant.

After the owner resolves this contract choice, record the same amendment commit
and Claude handoff alongside the source/behavior/tests before dependent changes.

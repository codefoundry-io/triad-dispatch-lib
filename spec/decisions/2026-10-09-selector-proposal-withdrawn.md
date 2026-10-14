# Model/effort environment proposal — withdrawn

Status: WITHDRAWN by the owner on 2026-10-09. This is a cancellation record,
not an implementation backlog or a new runtime contract.

Owner (verbatim):

> 이 스펙은 없애자 어차피 사용자 환경 설정은 건드리는거 아니고 기존에 effort는 잘 동작했으니 스펙에서도 폐기해

Disposition: discard the newly proposed model/effort environment inspection,
possible-override warning, additional selector scrubbing/normalization and
effective-effort attestation work. The earlier preserve-and-warn proposal is
withdrawn too. Do not make per-dispatch hooks, model-support matrices or further
precedence experiments prerequisites for continuing existing dispatch work.
Preserve user settings and the existing model/effort forwarding behavior.

This supersedes the selector investigation/request in
`2026-10-09-child-env-name-filter.md` and PR13 comments6078615855,6078758142,
6078840760,6078884713 as implementation requests. Keep their observations and
corrections as historical evidence only; they authorize no new feature or gate.
No model/effort environment warning was implemented by B.

Scope: the additional selector proposal only. Existing credential/endpoint and
loader hygiene, C75's independent name-before-value question, native host
ownership and existing CLI option forwarding are not removed by this record.
The broader unadmitted U2c candidate must not be reported as completed or shipped.
Neither host should implement the withdrawn extension from an older comment or
checkpoint. No changes to user-global settings, release or adoption are made.

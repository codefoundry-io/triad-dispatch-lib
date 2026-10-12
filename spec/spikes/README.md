# spikes/ — measured evidence behind a rule or case change

A spike record is written when a host measures a defect or an ambiguity and fixes it on its own side: the observation
with `path:line` anchors, the cause chain (vendor facts, host lines), the fix and its test, the live before/after run,
and the lines the OTHER host should touch (`reference/spec-authoring.md § 4`). It is evidence, not a rule — the rule it
produced lives in `reference/` with an anchor, the case in `cases/cases.json`; both point here. One file per spike,
named `<UTC-date>-<slug>.md`; a record is never rewritten after the other leader has read it (append a dated section).

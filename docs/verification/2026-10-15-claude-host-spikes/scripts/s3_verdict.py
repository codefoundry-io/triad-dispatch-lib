import json
import triad_dispatch_lib as lib
import verdict_v2 as A
BIND = ("review_id", "family", "content_digest", "leg_name", "attempt", "route")
BASE = {"schema_version": 2, "review_id": "review-1", "family": "codex", "content_digest": "a" * 64,
        "leg_name": "codex-leg", "attempt": 1, "route": None, "verdict": "SAFE TO MERGE",
        "criteria_checked": ["correctness"], "findings": [], "affected_surfaces_inspected": ["src/main.py"],
        "open_questions": []}
F = {"path": "src/main.py", "line": 1, "severity": "Minor", "summary": "S", "trigger": "T", "evidence": "E", "context_known": True}
B = dict(F, severity="must-fix")
J = json.dumps
EXP = {k: BASE[k] for k in BIND}
cases = []
def add(name, obj=None, text=None, expected=None):
    cases.append((name, J(obj) if text is None else text, expected or EXP))
for fam, route in [("codex", None), ("claude", None), ("google", "agy"), ("google", "gemini")]:
    o = dict(BASE, family=fam, route=route); e = {k: o[k] for k in BIND}
    add(f"valid SAFE {fam}/{route}", o, expected=e)
    add(f"valid negative {fam}/{route}", dict(o, verdict="DO NOT MERGE", findings=[B]), expected=e)
add("MERGE WITH FIXES + Minor", dict(BASE, verdict="MERGE WITH FIXES", findings=[F]))
add("SAFE + must-fix", dict(BASE, findings=[B]))
add("SAFE + open question", dict(BASE, open_questions=["q"]))
add("negative, no content", dict(BASE, verdict="DO NOT MERGE"))
add("uncertainty-only negative", dict(BASE, verdict="DO NOT MERGE", open_questions=["fact"]))
add("duplicate member", text=J(BASE).replace('"attempt": 1', '"attempt": 1, "attempt": 1'))
add("escaped duplicate", text=J(BASE).replace('"attempt": 1', '"attempt": 2, "\\u0061ttempt": 1'))
add("NaN attempt", text=J(BASE).replace('"attempt": 1', '"attempt": NaN'))
add("1e999 line", text=J(dict(BASE, verdict="DO NOT MERGE", findings=[dict(B, line=7)])).replace('"line": 7', '"line": 1e999'))
add("BOM prefix", text="﻿" + J(BASE))
add("fenced", text="```json\n" + J(BASE) + "\n```")
add("two documents", text=J(BASE) + " " + J(BASE))
add("array root", text=J([BASE]))
add("null root", text="null")
add("truncated", text=J(BASE)[:-5])
add("schema_version 1", dict(BASE, schema_version=1))
add("extra field", dict(BASE, extra=True))
add("attempt 0", dict(BASE, attempt=0))
add("attempt true", dict(BASE, attempt=True))
add("attempt 1.0", dict(BASE, attempt=1.0))
add("codex + route agy", dict(BASE, route="agy"))
add("google + null route", dict(BASE, family="google"))
add("absolute surface", dict(BASE, affected_surfaces_inspected=["/abs"]))
add("parent surface", dict(BASE, affected_surfaces_inspected=["../x"]))
add("empty criteria", dict(BASE, criteria_checked=[]))
add("dup criteria", dict(BASE, criteria_checked=["a", "a"]))
add("finding unknown key", dict(BASE, verdict="DO NOT MERGE", findings=[dict(B, unknown=1)]))
add("severity lowercase", dict(BASE, verdict="DO NOT MERGE", findings=[dict(B, severity="critical")]))
add("line null", dict(BASE, verdict="DO NOT MERGE", findings=[dict(B, line=None)]))
add("optional correction", dict(BASE, verdict="DO NOT MERGE", findings=[dict(B, correction="fix")]))
add("review_id newline", dict(BASE, review_id="a\nb"))
add("digest uppercase", dict(BASE, content_digest="A" * 64))
add("leg_name blank", dict(BASE, leg_name=" "))
for f, v in [("review_id", "other"), ("family", "claude"), ("content_digest", "b" * 64), ("leg_name", "other"), ("attempt", 2), ("route", "gemini")]:
    o = dict(BASE)
    if f == "route":
        o.update(family="google", route="agy")
    e = {k: o[k] for k in BIND}; e[f] = v
    add(f"binding mismatch {f}", o, expected=e)
def a_admit(text, exp):
    ok, obj, reason, kind = A._parse_strict(text, "reply")
    if not ok:
        return "reject", "parse:" + (kind or "?")
    adm = A._admit_obj(obj, exp, "reply")
    if adm.ok:
        return "accept", ""
    cls = "binding" if "the reply was not produced for this dispatch" in (adm.reason or "") else "schema"
    return "reject", f"{cls}:exit{adm.exit_code}"
def l_admit(text, exp):
    try:
        lib.validate_verdict(text, expected=exp); return "accept", ""
    except lib.AdmissionError as e:
        return "reject", e.code
match = 0; cls_notes = []
print(f"{'case':34} {'A':7} {'A class':16} {'lib':7} {'lib code':18} same")
for name, text, exp in cases:
    a, ac = a_admit(text, exp); l, lc = l_admit(text, exp)
    eq = a == l; match += eq
    print(f"{name:34} {a:7} {ac:16} {l:7} {lc:18} {'yes' if eq else 'NO'}")
    if eq and a == "reject" and ac.split(':')[0] != {"invalid_json": "parse", "duplicate_member": "parse", "nonfinite_number": "parse", "schema_violation": "schema", "binding_mismatch": "binding"}.get(lc, "?"):
        cls_notes.append((name, ac, lc))
print(f"\ncases={len(cases)} same_decision={match} different={len(cases) - match}")
print("same decision, different reason class:", cls_notes or "none")

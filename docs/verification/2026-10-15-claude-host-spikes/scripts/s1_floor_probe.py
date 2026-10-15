"""S1 floor probe: call five public functions of triad_dispatch_lib under the apt-equivalent
environment (jsonschema 4.10.3, referencing 0.31.0) and print which raise.
Run: PYTHONPATH=src <venv-apt>/bin/python docs/verification/2026-10-15-claude-host-spikes/scripts/s1_floor_probe.py
"""
import importlib.metadata as m
import triad_dispatch_lib as lib

print("env:", "jsonschema", m.version("jsonschema"), "referencing", m.version("referencing"))
exp = {"review_id": "r", "family": "codex", "content_digest": "a" * 64, "leg_name": "l", "attempt": 1, "route": None}
cases = [
    ("parse_json", lambda: lib.parse_json('{"a": 1}')),
    ("validate_binding", lambda: lib.validate_binding(exp)),
    ("load_roster_contract", lambda: lib.load_roster_contract()),
    ("resolve_roster", lambda: lib.resolve_roster({"schema": "triad-review-legs.v2", "legs": []})),
    ("render_review_clauses", lambda: lib.render_review_clauses(
        family="codex", host="A", review_date="2026-10-15", review_web_authorized=False,
        replacements={"worktree": "w", "brief-file": "b", "packet-files": "p", "review-id": "r",
                      "content-digest": "a" * 64, "leg-name": "l", "attempt": "1"})),
]
for name, fn in cases:
    try:
        fn(); print(f"{name}: OK")
    except Exception as e:  # noqa: BLE001 - a probe reports every exception class
        print(f"{name}: {type(e).__name__}: {str(e)[:110]}")

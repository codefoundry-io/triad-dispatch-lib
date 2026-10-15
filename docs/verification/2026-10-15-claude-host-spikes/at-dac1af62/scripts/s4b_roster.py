import json
from pathlib import Path
import triad_dispatch_lib as lib
import roster_v2 as A
WT = Path("/Users/chaniri/triad/_runs/worktrees/impl-claude-host")
defaults = json.loads(A.DEFAULTS_PATH.read_bytes())
override_path = A.project_override_path(WT)
override_bytes = override_path.read_bytes()
lib_res = lib.resolve_roster(defaults, override_bytes)
a_defaults = A.load_defaults()
legs = [dict(l) for l in a_defaults["legs"]]
over = A._read_json(override_path, "project override")
by_name = {l["name"]: i for i, l in enumerate(legs)}
for leg in over["legs"]:
    if leg["name"] in by_name:
        legs[by_name[leg["name"]]] = A._merge_leg(legs[by_name[leg["name"]]], leg)
    else:
        legs.append(dict(leg))
print("lib legs:", [(l["name"], l["enabled"]) for l in lib_res["legs"]])
print("A   legs:", [(l["name"], l["enabled"]) for l in legs])
print("merged legs byte-identical (json, sorted keys):", json.dumps(lib_res["legs"], sort_keys=True) == json.dumps(legs, sort_keys=True))
for x, y in zip(lib_res["legs"], legs):
    if x != y:
        print("  DIFF", x["name"], {k: (x.get(k), y.get(k)) for k in set(x) | set(y) if x.get(k) != y.get(k)})
print("lib _comment taken from override:", lib_res.get("_comment") == over.get("_comment"))
print("lib select_entries:", [l["name"] for l in lib.select_entries(lib_res)])
print("lib google route values (unresolved, as data):", {l["name"]: l.get("google", {}).get("route") for l in lib_res["legs"] if l["vendor"] == "google"})
try:
    full = A.resolve_roster(WT)
    print("A resolve_roster OK — legs:", [e.name for e in full.legs], "| startable:", [e.name for e in full.startable],
          "| families:", sorted(full.families), "| routes:", {e.name: e.route for e in full.legs if e.vendor == "google"},
          "| warnings:", full.warnings)
except A.RosterError as e:
    print("A resolve_roster refused:", e)
d = {"schema": "triad-review-legs.v2", "legs": [{"name": "g", "vendor": "google", "enabled": True, "acceptance": "required",
     "timeout_s": 30, "google": {"route": "agy"}, "agy": {"model": "m", "effort": "high"}}]}
o = {"schema": "triad-review-legs.v2", "legs": [{"name": "g", "agy": {"model": None}}]}
print("null override keeps sibling — lib:", lib.resolve_roster(d, json.dumps(o))["legs"][0]["agy"], "| A:", A._merge_leg(d["legs"][0], o["legs"][0])["agy"])
# A-only rules the lib does not apply: claude.model / claude.effort pin, unknown preset
bad = {"schema": "triad-review-legs.v2", "legs": [{"name": "claude", "claude": {"model": "claude-opus-5-5", "effort": "xhigh"}}]}
try:
    r = lib.resolve_roster(defaults, json.dumps(bad)); print("lib accepts claude.model/effort override:", r["legs"][0]["claude"])
except lib.RosterError as e:
    print("lib refuses claude.model/effort override:", e.code)
try:
    A._check_capabilities(lib.resolve_roster(defaults, json.dumps(bad))["legs"][0]); print("A _check_capabilities accepts it")
except A.RosterError as e:
    print("A _check_capabilities refuses it:", str(e)[:120])

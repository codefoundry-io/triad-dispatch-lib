"""S5: `merge_roster(defaults, override_text)` versus the claude host's `_merge_leg` fold over the same inputs, then
`validate_resolved`. argv[1] = the host skill root, argv[2] = the project override file. PYTHONPATH = <lib>/src:<host skill>/lib."""
import copy, json, sys
import triad_dispatch_lib as lib, roster_v2
A, override_path = sys.argv[1], sys.argv[2]
defaults = json.load(open(f"{A}/spec/review-legs.default.json"))
override_text = open(override_path, encoding="utf-8").read()
merged = lib.merge_roster(copy.deepcopy(defaults), override_text)
print("merge_roster: legs=", len(merged["legs"]), "| keys=", sorted(merged.keys()))
lib.validate_resolved(merged); print("validate_resolved(merged): OK (None)")
over = json.loads(override_text); legs = [dict(l) for l in defaults["legs"]]; idx = {l["name"]: i for i, l in enumerate(legs)}
for leg in over["legs"]:
    if leg["name"] in idx: legs[idx[leg["name"]]] = roster_v2._merge_leg(legs[idx[leg["name"]]], leg)
    else: legs.append(dict(leg))
key = lambda ls: json.dumps(sorted(ls, key=lambda l: l["name"]), sort_keys=True)
print("S5 merge_roster legs == host _merge_leg legs (sorted JSON):", key(merged["legs"]) == key(legs))

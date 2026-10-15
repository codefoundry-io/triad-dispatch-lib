"""S2'': dev4 `render_review_clauses(with_manifest=True)` versus the claude host's `prompts_v2.render_with_manifest`
over the 24 host-A profiles (text AND the ordered manifest). PYTHONPATH = <lib-A2>/src:<host skill>/lib."""
import itertools
import triad_dispatch_lib as lib, prompts_v2
DATE = "2026-10-15"; WT = "/tmp/wt"
BASE = {"worktree": WT, "brief-file": WT + "/brief.md", "packet-files": "brief.md, diff.prod.patch", "review-id": "r",
        "content-digest": "a" * 64, "leg-name": "l", "attempt": "1"}
same = diff = 0
for family, kind, web in itertools.product(["claude", "codex", "google"], ["formal-plan", "pre-merge", "implementation-review"], [False, True]):
    for route in ([None] if family != "google" else ["agy", "gemini"]):
        hook = (family == "google" and route == "agy"); res = None
        for extra in ({"gated-patch-file": WT + "/diff.prod.patch"}, {}):
            try:
                res = lib.render_review_clauses(family=family, host="A", review_date=DATE, review_web_authorized=web,
                                                replacements=BASE | extra, review_kind=kind, route=route,
                                                agy_hook_active=hook, with_manifest=True); break
            except Exception:
                pass
        text, man = res
        ctx = prompts_v2.RenderCtx(worktree=WT, review_id="r", content_digest="a" * 64, leg_name="l", attempt=1,
                                   google_route=route, brief_file=WT + "/brief.md", gated_patch_file=WT + "/diff.prod.patch",
                                   packet_files=("brief.md", "diff.prod.patch"), review_kind=kind,
                                   review_web_authorized=web, review_date=DATE)
        htext, hman = prompts_v2.render_with_manifest(family, ctx)
        ok = (text == htext) and ([(n, s) for n, s in hman] == [(d["name"], d["sha256"]) for d in man])
        same += ok; diff += (not ok)
print(f"S2'' profiles={same + diff} text+manifest identical={same} different={diff}")

import itertools, difflib
import triad_dispatch_lib as lib
import prompts_v2 as A
WT, RID, DIG, LEG, DATE = "/tmp/review-wt", "review-1", "a" * 64, "x-leg", "2026-10-15"
PACKET = ("brief.md", "diff.prod.patch", "diff.tests.patch", "history.txt")
BRIEF, PATCH = "/tmp/review-wt/brief.md", "/tmp/review-wt/diff.prod.patch"   # impl passes absolute, worktree-rooted paths
rows = []
for family, route in [("codex", None), ("claude", None), ("google", "agy"), ("google", "gemini")]:
    for kind in ["formal-plan", "implementation-review", "pre-merge"]:
        for web in (False, True):
            ctx = A.RenderCtx(worktree=WT, review_id=RID, content_digest=DIG, leg_name=LEG, attempt=1,
                              google_route=route, brief_file=BRIEF, gated_patch_file=PATCH, packet_files=PACKET,
                              review_kind=kind, review_web_authorized=web, review_date=DATE)
            a_text = A.render(family, ctx)
            repl = {"worktree": WT, "brief-file": BRIEF, "packet-files": ", ".join(PACKET),
                    "review-id": RID, "content-digest": DIG, "leg-name": LEG, "attempt": "1"}
            if family == "google":
                repl["gated-patch-file"] = PATCH
            hooks = (False, True) if (family == "google" and route == "agy") else (False,)
            best = None
            for hook in hooks:
                l_text = lib.render_review_clauses(family=family, host="A", review_date=DATE, review_web_authorized=web,
                                                   replacements=repl, review_kind=kind, route=route, agy_hook_active=hook)
                if a_text == l_text:
                    best = hook; break
            rows.append((family, route, kind, web, best, a_text, l_text))
same = sum(r[4] is not None for r in rows)
print(f"profiles={len(rows)} identical={same} different={len(rows) - same}")
print("agy profiles match with agy_hook_active =", sorted({r[4] for r in rows if r[1] == 'agy' and r[4] is not None}))
shown = 0
for family, route, kind, web, best, a_text, l_text in rows:
    if best is not None or shown >= 3: continue
    shown += 1
    print(f"\n--- DIFF family={family} route={route} kind={kind} web={web} (A -> lib) ---")
    for line in itertools.islice(difflib.unified_diff(a_text.splitlines(), l_text.splitlines(), "A", "lib", lineterm="", n=0), 30):
        print(line[:200])
for route in ("agy", "gemini"):
    a = A.render_investigation_clause(route)
    l = lib.render_investigation_prompt("P", family="google", route=route, web_authorized=True)
    print(f"investigation suffix {route}: identical={l == 'P' + chr(10) * 2 + a}")

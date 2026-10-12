"""Record integrity of the case corpus and the shared development log (one id, one row)."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cases():
    return {case["id"]: case for case in json.loads((ROOT / "cases/cases.json").read_text())["cases"]}


def test_dev_log_ids_are_unique_and_increasing():
    # Ids held by other unpublished spec branches leave gaps (authoring/shared-dev-log.md).
    ids = [int(n) for n in re.findall(r"^\| DL-(\d+) \|", (ROOT / "authoring/shared-dev-log.md").read_text(), re.M)]
    assert ids == sorted(set(ids))


def test_dev_log_rows_name_existing_cases():
    known = cases()
    for row in re.findall(r"^\| DL-\d+ \| ([^|]+)\|", (ROOT / "authoring/shared-dev-log.md").read_text(), re.M):
        for case_id in re.findall(r"C\d+", row):
            assert case_id in known, (case_id, row)


def test_c66_sealed_attempt_case_is_owned_by_review_lifecycle():
    case = cases()["C66"]
    assert case["surface"] == "review-lifecycle"
    assert "R-BIND" in case["rule"]
    assert case["tests"].get("A", "").strip() and case["tests"].get("B", "").strip()


def test_c68_threat_model_case_cites_its_rule():
    case = cases()["C68"]
    assert "R-THREAT" in case["rule"]


def _footer_ids(label):
    text = (ROOT / "authoring/shared-dev-log.md").read_text()
    line = next(l for l in text.splitlines() if l.startswith(label))
    return set(re.findall(r"DL-\d+", line))


def _status_ids(pattern):
    ids = set()
    for line in (ROOT / "authoring/shared-dev-log.md").read_text().splitlines():
        m = re.match(r"^\| (DL-\d+) \|", line)
        if m and re.search(pattern, line.rstrip().rstrip("|").rsplit(" | ", 1)[1]):
            ids.add(m[1])
    return ids


def test_dev_log_footer_matches_the_status_cells():
    assert _footer_ids("Rows with B work open:") == _status_ids(r"OPEN \(B")
    assert _footer_ids("Rows with A work open:") == _status_ids(r"OPEN \(A")
    assert _footer_ids("Checks suggested for B:") == _status_ids(r"CHECK-B")
    assert _footer_ids("Rows awaiting the owner:") == _status_ids(r"(?:^|; )OWNER")


def _vendor_lines():
    return json.loads((ROOT / "contracts/vendor-failure-lines.json").read_text())["lines"]


def test_vendor_failure_rows_match_their_own_sentence_with_a_known_token():
    # R-CLASSIFY: each row's lowercase match part is part of its sentence, and its token is a contract token.
    tokens = {t["token"] for t in json.loads((ROOT / "contracts/exit-tokens.json").read_text())["tokens"]}
    for row in _vendor_lines():
        assert set(row) >= {"cli", "line", "match", "carrier", "token", "observed"}, row
        assert row["match"] == row["match"].lower() and row["match"] in row["line"].lower(), row
        assert row["token"] in tokens, row


def test_agy_print_timeout_row_is_a_timeout_on_agy():
    # Observed 2026-10-03 on host A: agy returned a partial answer at vendor exit 0 (authoring/shared-dev-log.md DL-62).
    rows = [r for r in _vendor_lines() if "print timeout" in r["line"]]
    assert [(r["cli"], r["token"]) for r in rows] == [("agy", "timeout")]
    assert "[agy] " in rows[0]["carrier"] and "any vendor exit" in rows[0]["carrier"]


def test_codex_incorrect_api_key_row_is_oauth_env():
    # R-AUTH / C37: the measured codex 401 line (host A gate-1 r18, 2026-09-25); no credential text in the row.
    rows = [r for r in _vendor_lines() if "incorrect api key" in r["match"]]
    assert [(r["cli"], r["token"]) for r in rows] == [("codex", "oauth-env")]
    assert "sk-" not in rows[0]["line"]
    # R-CLASSIFY: the measured vendor wording, never the bare phrase the spec and instructions quote.
    assert rows[0]["match"] == "unexpected status 401 unauthorized: incorrect api key"


def test_agy_ai_credits_row_is_a_subscription_cap_from_the_vendor_source():
    # R-CLASSIFY: agy changelog 1.2.15 quotes the sentence for an exhausted plan quota with no AI credits.
    rows = [r for r in _vendor_lines() if r["match"] == "your ai credits balance is too low to continue"]
    assert [(r["cli"], r["token"], r["line"]) for r in rows] == [
        ("agy", "cli-subscription-cap", "Your AI credits balance is too low to continue.")]
    assert "changelog 1.2.15" in rows[0]["observed"] and "not captured" in rows[0]["carrier"]


def test_c31_names_no_claude_cli_route_on_host_a():
    # owner 2026-10-08 (D-OWNER-ANSWERS-20261008 item 2): the claude family runs natively on host A
    assert cases()["C31"]["tests"]["A"].startswith(
        "n/a — host A runs the claude family natively and has no claude CLI route (D-OWNER-ANSWERS-20261008)")


def _rule(anchor):
    text = (ROOT / "reference/review-rules.md").read_text()
    start = text.index(f'<a id="{anchor}"></a>')
    end = text.find('<a id="R-', start + 1)
    return text[start:end]


def test_r_threat_splits_per_folder_from_machine_level_concurrency():
    # owner fact 2026-10-08 (D-CONCURRENCY-FACT-20261008): one folder runs one operation at a time; folders and hosts do not
    rule = _rule("R-THREAT")
    assert "D-CONCURRENCY-FACT-20261008" in rule
    assert "There is no concurrent operation" not in rule
    assert "machine-level" in rule
    assert "D-CONCURRENCY-FACT-20261008" in cases()["C68"]["expected"]


def test_agy_finish_resubmission_is_a_shared_admission_rule():
    # owner 2026-10-08 (D-OWNER-ANSWERS-20261008B item 7): kept on both hosts, written beside the agy admission
    rule = _rule("R-CONTAIN")
    assert "D-OWNER-ANSWERS-20261008B" in rule and "a LATER `finish`" in rule


def _row(dl_id):
    for line in (ROOT / "authoring/shared-dev-log.md").read_text().splitlines():
        if line.startswith(f"| {dl_id} |"):
            return [c.strip() for c in line.strip().strip("|").split(" | ")]
    raise AssertionError(dl_id)


def test_c18_passes_the_google_pin_as_written_with_no_catalog_gate():
    # R-MODEL (owner 2026-09-27, D-RULINGS-20260927B Q10-1): no model-list probe; a refused model is one terminal record
    case = cases()["C18"]
    assert "R-MODEL" in case["rule"]
    assert "catalog" not in case["expected"]
    assert "as written" in case["expected"] and "one terminal" in case["expected"]


def test_no_spec_text_gates_a_model_on_a_catalog():
    # R-MODEL wins over every sentence written before the merge (PR #6)
    rules = (ROOT / "reference/review-rules.md").read_text()
    for stale in ("is validated against the route's catalog", "The catalog call is an authenticated CLI call",
                  "like the catalog call", "A cut-short agy catalog call"):
        assert stale not in rules, stale
    example = (ROOT / "contracts/review-legs.example.json").read_text()
    assert "route catalog" not in example and "recorded catalog" not in example
    assert "adapter catalog resolution" not in (ROOT / "contracts/README.md").read_text()
    models_row = next(r for r in _vendor_lines() if r["match"] == "please sign in to view available models")
    assert "a host reads before a review dispatch" not in models_row["carrier"]
    assert "R-MODEL" in _rule("R-NOCOST")


def test_catalog_gates_on_both_hosts_have_a_row():
    row = _row("DL-116")
    assert "R-MODEL" in row[4] and "_model_catalog_refusal" in row[4] and "_probe_agy_models" in row[4]
    assert "FIXED-A" in row[6] and "FIXED-B" in row[6]
    assert "DL-116" in _row("DL-21")[6]


def test_unmatched_vendor_failure_rows_have_a_row():
    row = _row("DL-117")
    assert row[1] == "C43" and row[2] == "REQ-CUSTODY"
    evidence_and_action = " ".join(row[4:6]).lower()
    assert "you've hit your usage limit" in evidence_and_action
    assert "your ai credits balance is too low to continue" in evidence_and_action
    assert "FIXED-A" in row[6] and "FIXED-B" in row[6] and "CHECK-B" in row[6]
    assert "unmeasured" in row[6].lower()


def test_merged_rows_use_the_current_status_grammar():
    assert "CONFORMS-A" in _row("DL-20")[6] and "pending" not in _row("DL-20")[6]
    assert "D-DELETION-BY-CODE-20261004" in _row("DL-22")[6] and "CHECK-B" in _row("DL-22")[6]
    assert "pending" not in _row("DL-21")[6] and "to decide" not in _row("DL-21")[6]


def test_c12_and_c34_select_claude_by_alias():
    # owner 2026-10-08 (D-OWNER-ANSWERS-20261008 item 17): alias over exact model ID wherever a CLI accepts one
    c12, c34 = cases()["C12"], cases()["C34"]
    assert "claude-opus-5-5" not in c12["expected"] and "`opus` alias" in c12["expected"]
    assert "only where a route takes a full model name" in c12["expected"]
    assert "claude-opus-5-5" not in c34["summary"] + c34["expected"]
    assert "alias" in c34["expected"] and "R-MODEL" in c34["rule"]
    assert "test_C34_opus_55_pin_rejects_provider_selection_of_opus_5" in c34["tests"]["B"]
    assert _row("DL-100")[6].startswith("FIXED-SPEC") and not re.search(r"(?:^|; )OWNER", _row("DL-100")[6])
    assert "C34 test" in _row("DL-114")[5]


def test_host_a_keeps_a_read_only_agy_web_prerequisite_check():
    # owner 2026-10-08 ("읽기 확인만 남김 (권장)"): host A reads the agy settings file only to check the read_url(*) allow
    register = (ROOT / "decisions/owner-register.md").read_text()
    entry = register[register.index('<a id="D-AGY-SETTINGS-UNTOUCHED-20261008">'):]
    entry = entry[:entry.index("<a id=", 10)]
    assert "읽기 확인만 남김 (권장)" in entry and "reads and writes none of" not in entry
    rule = _rule("R-REVIEW-WEB")
    assert "_v2_agy_web_refusal" in rule and "Host A does not check it before a round" not in rule
    assert "reads and writes none of" not in rule and "A recorded limit on A: on a machine without that allow" not in rule
    assert "WITHDRAWN (A" not in _row("DL-58")[6]
    assert "per-round preflight" not in _row("DL-112")[5].split("B:")[0].split("keep")[0]
    assert "no `_agy_settings` import" in _row("DL-112")[5]
    assert "FIXED-B" in _row("DL-107")[6]


def test_shipped_api_key_advice_removal_has_a_host_scoped_record():
    row = _row("DL-118")
    assert "C37" in row[1] and "CLAUDE.recommended.md" in row[4]
    assert "FIXED-A" in row[6] and "CHECK-B" in row[6]


def test_no_host_learns_an_authentication_classification():
    assert "refuses every proposal whose class is `oauth-env`" in " ".join(_rule("R-CLASSIFY").split())
    row = _row("DL-119")
    assert "VENDOR_EXIT_PROPOSAL_CLASSES" in row[4] and "bin/_common.py" in row[4]
    assert "FIXED-A" in row[6] and "IMPLEMENTED-B-CANDIDATE" in row[6]
    assert "full C76 remains partial" in row[6]


def test_a_classifier_proposal_is_verified_on_the_stored_record():
    rule = " ".join(_rule("R-CLASSIFY").split())
    assert "without calling the vendor again" in rule
    assert "classifies the failed run's stored record a second time" in rule
    row = _row("DL-104")
    assert "FIXED-A" in row[6] and "IMPLEMENTED-B-CANDIDATE" in row[6]
    assert "full C76 runtime remains partial" in row[6]


def test_task_blocked_has_one_producer_the_codex_host_claude_wrapper():
    notes = json.loads((ROOT / "contracts/exit-tokens.json").read_text())["notes"]
    note = next(n for n in notes if "`task-blocked` (65) stays" in n)
    assert "promote_claude_extraction" not in note and "DL-110" in note
    assert "the three extractors" not in " ".join(_rule("R-CLASSIFY").split())
    assert "FIXED-A" in _row("DL-110")[6]

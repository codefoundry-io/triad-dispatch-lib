"""Prompt payload format (prompts/README.md § Clause-file format); host rendering is verified separately."""

import re
from pathlib import Path

import pytest

PROMPTS = Path(__file__).resolve().parents[1] / "prompts"
LEG_FILES = ("leg-claude.md", "leg-codex.md", "leg-google.md")
LIBRARIES = ("common-clauses.md", "investigation.md")
HEADER = re.compile(r"^## (\S+)(?: \((.*)\))?$")
ORDER_ITEM = re.compile(r"^\d+\. (\S+)(?: \(.*\))?$")


def sections(name):
    """[(clause name, header note, body lines)] after the file preamble."""
    result, current = [], None
    for line in (PROMPTS / name).read_text().split("\n"):
        match = HEADER.match(line)
        if match:
            current = (match[1], match[2] or "", [])
            result.append(current)
        elif current is not None:
            current[2].append(line)
    return result


def fenced(lines):
    """(text blocks, non-blank lines outside every block)."""
    blocks, outside, block = [], [], None
    for line in lines:
        if block is None and line == "```text":
            block = []
        elif block is not None and line == "```":
            blocks.append("\n".join(block))
            block = None
        elif block is not None:
            block.append(line)
        elif line.strip():
            outside.append(line)
    assert block is None, "unterminated fenced block"
    return blocks, outside


def clauses(name):
    return {clause: fenced(lines)[0][0] for clause, _, lines in sections(name) if clause != "order"}


@pytest.mark.parametrize("name", LEG_FILES + LIBRARIES)
def test_every_clause_section_holds_exactly_one_text_block(name):
    for clause, _, lines in sections(name):
        blocks, _ = fenced(lines)
        assert len(blocks) == (0 if clause == "order" else 1), (name, clause)


@pytest.mark.parametrize("name", LEG_FILES)
def test_leg_files_carry_no_prose_outside_fences_and_only_items_in_order(name):
    for clause, _, lines in sections(name):
        _, outside = fenced(lines)
        if clause == "order":
            assert all(ORDER_ITEM.match(line) for line in outside), (name, outside)
        else:
            assert outside == [], (name, clause, outside)


def test_review_no_web_is_a_fenced_clause():
    assert clauses("common-clauses.md")["review-no-web"] == (
        "Do not use web search, URL fetching, or other network research in REVIEW.")


def test_current_date_clause_is_two_sentences_with_the_round_date():
    text = clauses("common-clauses.md")["current-date"]
    assert "<review-date>" in text
    assert text.endswith(".") and len(re.split(r"(?<=\.)\s+", text)) == 2, text


@pytest.mark.parametrize("name", LEG_FILES)
def test_every_leg_renders_current_date_after_current_basis(name):
    order = [ORDER_ITEM.match(line)[1]
             for clause, _, lines in sections(name) if clause == "order"
             for line in fenced(lines)[1]]
    assert order[order.index("common:current-basis") + 1] == "common:current-date", order


def test_host_specific_clauses_carry_the_a_only_marker():
    marked = {clause for name in LEG_FILES + LIBRARIES
              for clause, note, _ in sections(name) if clause != "order" and "A-only" in note}
    assert marked == {"claude-output-shape-notice", "claude-output-integrity", "google-a-hook-audit"}


def test_review_web_permission_carries_the_privacy_rule():
    text = clauses("common-clauses.md")["review-web-permission"]
    assert "never send the reviewed material, a local path or a person's name" in text


# The owner approved this wording verbatim (decisions/owner-register.md#D-OWNER-ANSWERS-20261008B, item 19);
# it replaces the earlier "short, at most three sentences" shape of this test.
DEPLOYMENT_CONTEXT_20261008 = (
    "When the reviewed code is a TRIAD dispatch host's own code (its review and dispatch toolkit), its deployment "
    "context, evidence R-THREAT / D-THREAT-MODEL-20261003 / D-CONCURRENCY-FACT-20261008, is one operator and no "
    "malicious actor. Inside one working folder no second operation runs while one runs (concurrency inside one "
    "operation, such as two legs of one round, is real); operations started from different folders, and the "
    "claude-host and codex-host toolkits, do run at the same time on one machine and meet at machine-level state "
    "(the CLIs' own settings and configuration, a classifier extension file, the logs of one installed toolkit). "
    "For any other reviewed target, the deployment context is the one the brief states. Under the host context, a "
    "finding whose trigger needs deliberate tampering with the host's own files, or a second operation inside one "
    "working folder, is ruled out: label it HARDENING-SUGGESTION, which does not block on its own. Ordinary "
    "failures (a full disk, a stop at any point such as a crash or a session that hits its token or usage limit, a "
    "wrong argument or another ordinary operator action, an operation from another folder or the other host "
    "meeting the same machine-level state, a vendor answer a run has shown — a capture, a "
    "contracts/vendor-failure-lines.json row or the vendor's own source —, an odd layout of files the leader "
    "creates by hand, a reviewer's or leader's mistake) stay in scope at their full severity. A vendor shape no run "
    "has shown is a recorded limit, not a defect: label it HARDENING-SUGGESTION and say in its trigger that no run "
    "shows it.")


def test_deployment_context_clause_is_the_owner_approved_text():
    text = clauses("common-clauses.md")["deployment-context"]
    assert text == DEPLOYMENT_CONTEXT_20261008
    assert "R-THREAT" in text and "TRIAD dispatch host's own code" in text  # evidence pointer and scope


def test_severity_instruction_scopes_vendor_output_to_shapes_a_run_has_shown():
    # owner 2026-10-08 (D-OWNER-ANSWERS-20261008B, item 19): only this sentence of the clause changed
    text = clauses("common-clauses.md")["severity-instruction"]
    assert ("review packets), so a missing validation on those IS in scope; for vendor output, that means a shape "
            "a run has shown, and a shape no run has shown is a recorded limit (HARDENING-SUGGESTION).") in text
    assert text.startswith("Report every finding — coverage first")
    assert text.endswith("a bare SAFE with no criteria enumeration and no findings is a failed review.")


@pytest.mark.parametrize("name", LEG_FILES)
def test_every_leg_renders_deployment_context_before_severity(name):
    order = [ORDER_ITEM.match(line)[1]
             for clause, _, lines in sections(name) if clause == "order"
             for line in fenced(lines)[1]]
    assert order[order.index("common:severity-instruction") - 1] == "common:deployment-context", order


def test_deployment_context_keeps_stops_and_hand_made_layouts_in_scope():
    # owner 2026-10-03 / 2026-10-08: only deliberate tampering and a second operation inside one working folder
    # are out of scope; an operation from another folder or the other host stays in scope
    assert "operation from another folder or the other host" in clauses("common-clauses.md")["deployment-context"]
    text = clauses("common-clauses.md")["deployment-context"]
    assert "exact instant" not in text and "unusual layout" not in text
    assert "token" in text and "by hand" in text

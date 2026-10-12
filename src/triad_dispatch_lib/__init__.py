"""Shared deterministic TRIAD admission."""

from .errors import AdmissionError, ContractError, PromptError, RosterError
from .json_input import parse_json
from .verdict import validate_binding, validate_verdict
from .prompts import render_data, render_review_clauses, render_investigation_prompt
from .contracts import load_roster_contract
from .roster import resolve_roster, select_entries

__all__ = ["RosterError", "resolve_roster", "select_entries", "load_roster_contract",
           "render_investigation_prompt", "AdmissionError", "ContractError", "PromptError", "parse_json",
           "validate_binding", "validate_verdict", "render_data", "render_review_clauses"]

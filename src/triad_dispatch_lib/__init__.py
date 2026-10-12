"""Shared deterministic TRIAD admission."""

from .errors import AdmissionError, ContractError, PromptError
from .json_input import parse_json
from .verdict import validate_binding, validate_verdict
from .prompts import render_data, render_review_clauses

__all__ = ["AdmissionError", "ContractError", "PromptError", "parse_json",
           "validate_binding", "validate_verdict", "render_data", "render_review_clauses"]

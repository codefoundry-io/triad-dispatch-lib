"""Shared deterministic TRIAD admission."""

from .errors import AdmissionError, ContractError
from .json_input import parse_json
from .verdict import validate_verdict

__all__ = ["AdmissionError", "ContractError", "parse_json", "validate_verdict"]

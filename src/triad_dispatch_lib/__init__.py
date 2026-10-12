"""Shared deterministic TRIAD admission."""

from .errors import AdmissionError, ContractError
from .json_input import parse_json

__all__ = ["AdmissionError", "ContractError", "parse_json"]

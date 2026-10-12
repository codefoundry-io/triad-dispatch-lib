"""Errors that never interpolate untrusted verdict contents."""

_MESSAGES = {
    "invalid_json": "Invalid original JSON.",
    "invalid_utf8": "JSON bytes must be UTF-8.",
    "duplicate_member": "Duplicate JSON object member.",
    "nonfinite_number": "Nonfinite JSON number.",
    "invalid_input_type": "Original JSON must be str or bytes.",
    "nesting_limit": "JSON nesting exceeds the decoder limit.",
    "schema_violation": "Verdict violates the canonical schema.",
    "invalid_expected": "Invalid expected invocation binding.",
    "binding_mismatch": "Verdict does not match the expected invocation.",
}


class AdmissionError(ValueError):
    """Rejected input; ``code`` is stable, human-readable wording is not."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(_MESSAGES[code])


class ContractError(RuntimeError):
    """The packaged validation contract is unavailable or inconsistent."""


class PromptError(ValueError):
    """Invalid rendering arguments, separate from verdict admission."""


class RosterError(ValueError):
    """Caller roster refusal with fixed text and a stable reason code."""

    def __init__(self, code: str):
        self.code = code
        super().__init__({
            "invalid_json": "Invalid roster override JSON.",
            "schema_violation": "Roster violates the canonical schema.",
            "duplicate_name": "Duplicate roster entry name.",
            "empty_selection": "Roster has no enabled entries.",
            "nesting_limit": "Roster nesting exceeds the validation limit.",
        }[code])

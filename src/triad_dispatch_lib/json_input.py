"""Parse original JSON without losing duplicate-member evidence."""

import json
import math

from .errors import AdmissionError


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AdmissionError("duplicate_member")
        result[key] = value
    return result


def _constant(_value):
    raise AdmissionError("nonfinite_number")


def _float(value):
    result = float(value)
    if not math.isfinite(result):
        raise AdmissionError("nonfinite_number")
    return result


def parse_json(raw: str | bytes) -> object:
    """Decode UTF-8 JSON once; reject duplicate members and nonfinite numbers.

    No fence stripping, repair, coercion, or extraction is performed. Callers
    must bound input sizes according to their execution environment.
    """
    if not isinstance(raw, (str, bytes)):
        raise AdmissionError("invalid_input_type")
    try:
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8")
        return json.loads(raw, object_pairs_hook=_object,
                          parse_constant=_constant, parse_float=_float)
    except AdmissionError:
        raise
    except UnicodeDecodeError:
        raise AdmissionError("invalid_utf8") from None
    except RecursionError:
        raise AdmissionError("nesting_limit") from None
    except ValueError:
        raise AdmissionError("invalid_json") from None

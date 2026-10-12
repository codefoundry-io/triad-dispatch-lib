"""Read a verified, pinned specification payload from package resources."""

import hashlib
from importlib.resources import files

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from .errors import ContractError
from .json_input import parse_json

SOURCE_REPOSITORY = "https://github.com/codefoundry-io/triad-dispatch-spec"
SOURCE_COMMIT = "fcd96a15d18f3131c1f0111bdb10c3faceae34f8"
SCHEMA_NAME = "leg-verdict.schema.json"


def load_contract() -> dict:
    """Return fresh schema data; hashes establish consistency, not authenticity."""
    try:
        root = files("triad_dispatch_lib").joinpath("data")
        manifest = parse_json(root.joinpath("source-manifest.json").read_bytes())
        if (
            not isinstance(manifest, dict)
            or set(manifest) != {"source_repository", "source_commit", "status", "sha256"}
            or manifest["source_repository"] != SOURCE_REPOSITORY
            or manifest["source_commit"] != SOURCE_COMMIT
            or manifest["status"] != "candidate"
            or not isinstance(manifest["sha256"], dict)
            or set(manifest["sha256"]) != {SCHEMA_NAME}
        ):
            raise ContractError("Invalid packaged contract provenance.")
        raw = root.joinpath(SCHEMA_NAME).read_bytes()
        if hashlib.sha256(raw).hexdigest() != manifest["sha256"][SCHEMA_NAME]:
            raise ContractError("Packaged contract digest mismatch.")
        schema = parse_json(raw)
        if not isinstance(schema, dict) or schema.get("$schema") != Draft202012Validator.META_SCHEMA["$id"]:
            raise ContractError("Unsupported packaged contract dialect.")
        Draft202012Validator.check_schema(schema)
        return schema
    except (OSError, ValueError, SchemaError, RecursionError):
        raise ContractError("Unreadable or invalid packaged contract.") from None

"""Review-stage schema boundary; host dispatch behavior is verified separately."""

import hashlib
import json
import tomllib
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator


SCHEMA = json.loads(
    (Path(__file__).resolve().parents[1] / "contracts/review-kind.schema.json").read_text()
)


@pytest.fixture(scope="module")
def validator():
    Draft202012Validator.check_schema(SCHEMA)
    return Draft202012Validator(SCHEMA)


@pytest.mark.parametrize("stage", ["formal-plan", "pre-merge", "implementation-review"])
def test_allowed_stage(validator, stage):
    validator.validate(stage)


def test_omission_default_is_an_annotation(validator):
    assert SCHEMA["default"] == "pre-merge"
    assert validator.is_valid(SCHEMA["default"])


@pytest.mark.parametrize("stage", [None, "unknown", "", 1])
def test_invalid_stage_is_refused(validator, stage):
    assert not validator.is_valid(stage)


def test_verification_manifest_binds_current_schema_bytes():
    root = Path(__file__).resolve().parents[1]
    manifest = tomllib.loads(
        (root / "contracts/review-strategy.verify.toml").read_text()
    )
    assert manifest["contract_sha256"] == hashlib.sha256(
        (root / manifest["contract"]).read_bytes()
    ).hexdigest()

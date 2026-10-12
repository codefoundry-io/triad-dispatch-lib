"""Render pinned fenced clauses; leave host I/O and native execution outside."""

from datetime import date
from importlib.resources import files
import json
import re

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from referencing import Registry
from referencing.exceptions import Unresolvable

from .contracts import load_verified_bundle
from .errors import ContractError, PromptError
from .json_input import parse_json

PAYLOADS = ("prompts/common-clauses.md", "prompts/leg-codex.md", "contracts/review-kind.schema.json")
REPLACEMENTS = {"worktree", "brief-file", "packet-files", "review-id", "content-digest", "leg-name", "attempt"}


def _bundle():
    root = files("triad_dispatch_lib").joinpath("data", "prompt-bundle")
    try:
        return {name: raw.decode("utf-8") for name, raw in load_verified_bundle(root, PAYLOADS).items()}
    except UnicodeError:
        raise ContractError("Invalid prompt bundle encoding.") from None


def parse_clauses(text: str, *, host: str | None) -> dict[str, str]:
    """Parse the fixed canonical fenced-clause format, not general Markdown."""
    clauses, seen = {}, set()
    for section in re.split(r"^## ", text, flags=re.MULTILINE)[1:]:
        heading = section.split("\n", 1)[0]
        name = heading.split()[0]
        if name in seen:
            raise ContractError("Duplicate prompt clause.")
        seen.add(name)
        blocks = re.findall(r"^```text\n(.*?)^```$", section, re.MULTILINE | re.DOTALL)
        if name == "order" and not blocks:
            continue
        if len(blocks) != 1:
            raise ContractError("Invalid prompt clause format.")
        if host is not None and re.search(r"\b" + ("A" if host == "B" else "B") + r"-only\b", heading):
            continue
        clauses[name] = blocks[0].rstrip("\n")
    return clauses


def render_review_clauses(*, family: str, host: str, review_date: str,
                          review_web_authorized: bool, replacements: dict,
                          review_kind: str = "pre-merge") -> str:
    """Render the supported Codex/B profile with one-pass caller substitution.

    Caller-owned replacement values are already encoded single-line strings.
    This function performs no path inspection and grants no execution authority.
    """
    if family != "codex" or host != "B":
        raise PromptError("Unsupported prompt profile.")
    if type(review_web_authorized) is not bool:
        raise PromptError("Web permission must be a boolean.")
    try:
        if not isinstance(review_date, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", review_date):
            raise ValueError
        date.fromisoformat(review_date)
    except ValueError:
        raise PromptError("Review date must be an explicit ISO calendar date.") from None
    if (not isinstance(replacements, dict) or set(replacements) != REPLACEMENTS
            or any(not isinstance(value, str) or "\n" in value or "\r" in value for value in replacements.values())):
        raise PromptError("Invalid caller replacements.")
    bundle = _bundle()
    try:
        phase_schema = parse_json(bundle[PAYLOADS[2]])
        if not isinstance(phase_schema, dict) or phase_schema.get("$schema") != Draft202012Validator.META_SCHEMA["$id"]:
            raise ValueError
        Draft202012Validator.check_schema(phase_schema)
    except (ValueError, SchemaError):
        raise ContractError("Invalid prompt phase contract.") from None
    try:
        if not Draft202012Validator(phase_schema, registry=Registry()).is_valid(review_kind):
            raise PromptError("Invalid review kind.")
    except Unresolvable:
        raise ContractError("Invalid prompt phase contract.") from None
    common = parse_clauses(bundle[PAYLOADS[0]], host=host)
    leg_text = bundle[PAYLOADS[1]].replace("common:<review-purpose>",
        "common:" + ("plan-purpose" if review_kind == "formal-plan" else "code-purpose"))
    leg = parse_clauses(leg_text, host=host)
    all_common = parse_clauses(bundle[PAYLOADS[0]], host=None)
    all_leg = parse_clauses(leg_text, host=None)
    order = re.findall(r"^\d+\. ([\w:-]+)", leg_text, re.MULTILINE)
    if not order or len(order) != len(set(order)):
        raise ContractError("Invalid prompt clause order.")
    try:
        pieces = []
        for name in order:
            selected, complete, key = (common, all_common, name[7:]) if name.startswith("common:") else (leg, all_leg, name)
            if key not in complete:
                raise KeyError
            if key in selected:
                pieces.append(selected[key])
        values = replacements | {"review-kind": review_kind, "review-date": review_date,
            "review-web-policy": common["review-web-permission" if review_web_authorized else "review-no-web"]}
    except KeyError:
        raise ContractError("Missing ordered prompt clause.") from None
    text = "\n\n".join(pieces)
    if not set(re.findall(r"<([a-z][a-z-]+)>", text)).issubset(values):
        raise ContractError("Unexpected prompt placeholders.")
    return re.sub(r"<([a-z][a-z-]+)>", lambda match: values[match[1]], text)


def render_data(value: str) -> str:
    """Transport caller-authored residual text without interpreting its contents."""
    if not isinstance(value, str):
        raise PromptError("Residual data must be text.")
    common = parse_clauses(_bundle()[PAYLOADS[0]], host="B")
    fence = "`" * (max([2, *(len(run) for run in re.findall(r"`+", value))]) + 1)
    return common["data-fence-caveat"] + "\n" + fence + "text\n" + json.dumps(value, ensure_ascii=True) + "\n" + fence

"""First selected schema diagnostics remain value-free and document-specific."""
import copy
import importlib
import json

import pytest
import triad_dispatch_lib as lib


def entry(**changes):
    return dict(name='c', vendor='codex', enabled=True, acceptance='required',
                timeout_s=30, codex={}, **changes)


def roster(*legs):
    return {'schema': 'triad-review-legs.v2', 'legs': list(legs)}


def diagnostic(operation, document, path, missing):
    with pytest.raises(lib.RosterError) as caught:
        operation()
    error = caught.value
    assert error.code == 'schema_violation'
    assert str(error) == 'Roster violates the canonical schema.'
    assert (error.document, error.path, error.missing) == (document, path, missing)


@pytest.mark.parametrize('code', ['invalid_json', 'schema_violation', 'duplicate_name',
                                 'empty_selection', 'nesting_limit'])
def test_direct_error_diagnostic_defaults(code):
    error = lib.RosterError(code)
    assert (error.path, error.missing, error.document) == (None, None, None)


@pytest.mark.parametrize('operation', [lib.merge_roster, lib.resolve_roster])
def test_defaults_schema_precedes_override_parse(operation):
    diagnostic(lambda: operation({}, '{'), 'defaults', ('required',), 'schema')


def test_override_root_and_nested_required_paths():
    base = roster(entry())
    diagnostic(lambda: lib.resolve_roster(base, '{}'), 'override', ('required',), 'schema')
    diagnostic(lambda: lib.resolve_roster(base, json.dumps(roster({}))), 'override',
               ('properties', 'legs', 'items', 'required'), 'name')


@pytest.mark.parametrize('operation', [lib.validate_resolved, lib.select_entries])
def test_standalone_and_selection_revalidate_resolved(operation):
    diagnostic(lambda: operation(roster({'name': 'new', 'vendor': 'codex'})), 'resolved',
               ('properties', 'legs', 'items', 'allOf', 1, 'required'), 'enabled')


def test_final_validation_attribution_and_copy():
    base = roster(entry())
    saved = copy.deepcopy(base)
    diagnostic(lambda: lib.resolve_roster(base, json.dumps(roster({'name': 'new'}))),
               'resolved', ('properties', 'legs', 'items', 'allOf', 1, 'required'), 'vendor')
    assert base == saved


@pytest.mark.parametrize('sibling,tail,missing', [
    (False, ('anyOf',), None),
    (True, ('allOf', 0, 'then', 'required'), 'agy'),
])
def test_google_first_error_does_not_walk_anyof_children(sibling, tail, missing):
    leg = dict(name='g', vendor='google', enabled=True, acceptance='required',
               timeout_s=30, google={'route': 'agy'})
    if sibling:
        leg['gemini'] = {}
    diagnostic(lambda: lib.validate_resolved(roster(leg)), 'resolved',
               ('properties', 'legs', 'items', 'allOf', 1, 'allOf', 2, 'then') + tail, missing)


def test_nonrequired_winner_precedes_missing_and_duplicate_errors():
    value = roster({'name': 'c', 'private-key': 'private-value'}, {'name': 'c'})
    diagnostic(lambda: lib.merge_roster(value, '{'), 'defaults',
               ('properties', 'legs', 'items', 'allOf', 0, 'additionalProperties'), None)


@pytest.mark.parametrize('operation,code', [
    (lambda: lib.merge_roster(roster(entry()), '{'), 'invalid_json'),
    (lambda: lib.merge_roster(roster(entry(), entry())), 'duplicate_name'),
    (lambda: lib.select_entries(roster({**entry(), 'enabled': False})), 'empty_selection'),
])
def test_non_schema_refusal_attributes_are_none(operation, code):
    with pytest.raises(lib.RosterError) as caught:
        operation()
    assert caught.value.code == code
    assert (caught.value.path, caught.value.missing, caught.value.document) == (None, None, None)


def test_validation_recursion_has_no_schema_metadata(monkeypatch):
    module = importlib.import_module('triad_dispatch_lib.roster')
    schema = lib.load_roster_contract()
    schema['$defs']['resolvedRoster'] = {'$ref': '#/$defs/resolvedRoster'}
    monkeypatch.setattr(module, 'load_roster_contract', lambda: schema)
    with pytest.raises(lib.RosterError) as caught:
        lib.validate_resolved({})
    assert caught.value.code == 'nesting_limit'
    assert (caught.value.path, caught.value.missing, caught.value.document) == (None, None, None)

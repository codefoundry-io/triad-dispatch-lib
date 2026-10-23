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


def diagnostic(operation, document, path, missing, instance_path):
    with pytest.raises(lib.RosterError) as caught:
        operation()
    error = caught.value
    assert error.code == 'schema_violation'
    assert str(error) == 'Roster violates the canonical schema.'
    assert error.args == ('Roster violates the canonical schema.',)
    assert (error.document, error.path, error.missing) == (document, path, missing)
    assert error.instance_path == instance_path
    assert isinstance(error.instance_path, tuple)
    return error


@pytest.mark.parametrize('code', ['invalid_json', 'schema_violation', 'duplicate_name',
                                 'empty_selection', 'nesting_limit'])
def test_direct_error_diagnostic_defaults(code):
    error = lib.RosterError(code)
    assert (error.path, error.missing, error.document) == (None, None, None)
    assert error.instance_path is None


@pytest.mark.parametrize('operation', [lib.merge_roster, lib.resolve_roster])
def test_defaults_schema_precedes_override_parse(operation):
    diagnostic(lambda: operation({}, '{'), 'defaults', ('required',), 'schema', ())


def test_override_root_and_nested_required_paths():
    base = roster(entry())
    diagnostic(lambda: lib.resolve_roster(base, '{}'), 'override', ('required',), 'schema', ())
    diagnostic(lambda: lib.resolve_roster(base, json.dumps(roster({}))), 'override',
               ('properties', 'legs', 'items', 'required'), 'name', ('legs', 0))


@pytest.mark.parametrize('operation', [lib.validate_resolved, lib.select_entries])
def test_standalone_and_selection_revalidate_resolved(operation):
    diagnostic(lambda: operation(roster({'name': 'new', 'vendor': 'codex'})), 'resolved',
               ('properties', 'legs', 'items', 'allOf', 1, 'required'), 'enabled', ('legs', 0))


def test_final_validation_attribution_and_copy():
    base = roster(entry())
    saved = copy.deepcopy(base)
    diagnostic(lambda: lib.resolve_roster(base, json.dumps(roster({'name': 'new'}))),
               'resolved', ('properties', 'legs', 'items', 'allOf', 1, 'required'), 'vendor', ('legs', 1))
    assert base == saved


@pytest.mark.parametrize('sibling,tail,missing', [
    (False, ('anyOf',), None),
    (True, ('allOf', 0, 'then', 'required'), 'agy'),
])
@pytest.mark.parametrize('index', [0, 3])
def test_google_first_error_does_not_walk_anyof_children(sibling, tail, missing, index):
    leg = dict(name='g', vendor='google', enabled=True, acceptance='required',
               timeout_s=30, google={'route': 'agy'})
    if sibling:
        leg['gemini'] = {}
    value = roster(*[{**entry(), 'name': f'c{i}'} for i in range(index)], leg)
    saved = copy.deepcopy(value)
    diagnostic(lambda: lib.validate_resolved(value), 'resolved',
               ('properties', 'legs', 'items', 'allOf', 1, 'allOf', 2, 'then') + tail,
               missing, ('legs', index))
    assert value == saved


def test_nonrequired_winner_precedes_missing_and_duplicate_errors():
    value = roster({'name': 'c', 'private-key': 'private-value'}, {'name': 'c'})
    diagnostic(lambda: lib.merge_roster(value, '{'), 'defaults',
               ('properties', 'legs', 'items', 'allOf', 0, 'additionalProperties'), None, ('legs', 0))


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
    assert caught.value.instance_path is None


def test_validation_recursion_has_no_schema_metadata(monkeypatch):
    module = importlib.import_module('triad_dispatch_lib.roster')
    schema = lib.load_roster_contract()
    schema['$defs']['resolvedRoster'] = {'$ref': '#/$defs/resolvedRoster'}
    monkeypatch.setattr(module, 'load_roster_contract', lambda: schema)
    with pytest.raises(lib.RosterError) as caught:
        lib.validate_resolved({})
    assert caught.value.code == 'nesting_limit'
    assert (caught.value.path, caught.value.missing, caught.value.document) == (None, None, None)
    assert caught.value.instance_path is None


@pytest.mark.parametrize('index', [0, 3])
@pytest.mark.parametrize('operation,document', [
    ('defaults', 'defaults'), ('override', 'override'),
    ('validate', 'resolved'), ('select', 'resolved'),
])
def test_timeout_location_is_relative_to_validated_document(operation, document, index):
    value = roster(*[{**entry(), 'name': f'c{i}'} for i in range(index + 1)])
    value['legs'][index]['timeout_s'] = 'private-timeout-value'
    saved = copy.deepcopy(value)
    raw = json.dumps(value)
    operations = {
        'defaults': lambda: lib.resolve_roster(value),
        'override': lambda: lib.resolve_roster(roster(entry()), raw),
        'validate': lambda: lib.validate_resolved(value),
        'select': lambda: lib.select_entries(value),
    }
    prefix = ('properties', 'legs', 'items')
    if document != 'override':
        prefix += ('allOf', 0)
    error = diagnostic(operations[operation], document,
                       prefix + ('properties', 'timeout_s', 'type'), None,
                       ('legs', index, 'timeout_s'))
    assert value == saved
    assert 'private-timeout-value' not in repr(vars(error)) + str(error) + repr(error.args)
    value['legs'].clear()
    assert error.instance_path == ('legs', index, 'timeout_s')


@pytest.mark.parametrize('value,path,missing', [
    ({}, ('required',), 'schema'),
    ([], ('type',), None),
    ({**roster(entry()), 'private-key': 'private-value'}, ('additionalProperties',), None),
])
def test_root_location_distinguishes_root_from_unavailable(value, path, missing):
    saved = copy.deepcopy(value)
    error = diagnostic(lambda: lib.validate_resolved(value), 'resolved', path, missing, ())
    assert value == saved
    public = repr(vars(error)) + str(error) + repr(error.args)
    assert 'private-key' not in public
    assert 'private-value' not in public


@pytest.mark.parametrize('index', [0, 3])
@pytest.mark.parametrize('adapter', [False, True])
def test_unknown_property_diagnostic_exposes_only_parent(index, adapter):
    value = roster(*[{**entry(), 'name': f'c{i}'} for i in range(index + 1)])
    parent = value['legs'][index]['codex'] if adapter else value['legs'][index]
    parent['private-key'] = 'private-value'
    saved = copy.deepcopy(value)
    path = ('properties', 'legs', 'items', 'allOf', 0)
    location = ('legs', index)
    if adapter:
        path += ('properties', 'codex')
        location += ('codex',)
    error = diagnostic(lambda: lib.validate_resolved(value), 'resolved',
                       path + ('additionalProperties',), None, location)
    assert value == saved
    public = repr(vars(error)) + str(error) + repr(error.args)
    assert 'private-key' not in public
    assert 'private-value' not in public


@pytest.mark.parametrize('append,index', [(False, 2), (True, 3)])
def test_final_location_uses_merged_order_and_survives_caller_mutation(append, index):
    base = roster(*[{**entry(), 'name': f'c{i}'} for i in range(3)])
    # A valid vendor override needs an adapter after merging; a new name appends.
    changed = {'name': 'new'} if append else {'name': 'c2', 'vendor': 'google'}
    override = roster(changed)
    saved = copy.deepcopy(base)
    raw = json.dumps(override)
    tail = ('required',) if append else ('allOf', 2, 'then', 'anyOf')
    error = diagnostic(lambda: lib.resolve_roster(base, raw), 'resolved',
                       ('properties', 'legs', 'items', 'allOf', 1) + tail,
                       'vendor' if append else None, ('legs', index))
    assert base == saved
    assert json.loads(raw) == override
    base['legs'].reverse()
    override['legs'].clear()
    assert error.instance_path == ('legs', index)

import copy
import json

import pytest
import triad_dispatch_lib as lib


def entry(name='c', vendor='codex', **changes):
    return {'name': name, 'vendor': vendor, 'enabled': True,
            'acceptance': 'required', 'timeout_s': 30,
            vendor: {}, **changes}


def roster(*legs):
    return {'schema': 'triad-review-legs.v2', 'legs': list(legs)}


@pytest.fixture(params=['combined', 'split'])
def resolve(request):
    def run(defaults, overrides=None):
        if request.param == 'combined':
            return lib.resolve_roster(defaults, overrides)
        merged = lib.merge_roster(defaults, overrides)
        lib.validate_resolved(merged)
        return merged
    return run


def test_recursive_partial_null_merge_and_copy(resolve):
    defaults = roster(entry(codex={'model': 'chosen', 'reasoning': 'high'}))
    saved = copy.deepcopy(defaults)
    result = resolve(defaults, json.dumps(roster({'name': 'c', 'codex': {'model': None}})))
    assert result['legs'][0]['codex'] == {'model': None, 'reasoning': 'high'}
    result['legs'][0]['codex']['reasoning'] = 'low'
    assert defaults == saved
    assert resolve(defaults)['legs'][0]['codex'] == saved['legs'][0]['codex']


def test_four_routes_same_family_order_and_selection_copy(resolve):
    defaults = roster(entry(), entry('claude', 'claude'),
                      entry('gemini', 'google', google={'route': 'gemini'}, gemini={}))
    new = entry('agy', 'google', google={'route': 'agy'}, agy={})
    result = resolve(defaults, json.dumps(roster({'name': 'c', 'enabled': False}, new)).encode())
    selected = lib.select_entries(result)
    assert [leg['name'] for leg in selected] == ['claude', 'gemini', 'agy']
    selected[0]['claude']['model'] = 'changed'
    assert result['legs'][1]['claude'] == {}


@pytest.mark.parametrize('raw', ['{', '{"schema":"triad-review-legs.v2","legs":[],"legs":[]}',
                                 '{"schema":"triad-review-legs.v2","legs":[],"x":NaN}',
                                 b'\xff', 42])
def test_strict_json_refusal_is_fixed_roster_error(raw, resolve):
    assert hasattr(lib, 'RosterError'), 'roster error missing'
    with pytest.raises(lib.RosterError) as caught:
        resolve(roster(entry()), raw)
    assert caught.value.code == 'invalid_json'
    assert str(raw) not in str(caught.value)


@pytest.mark.parametrize('defaults,override', [
    (roster(entry(), entry()), None),
    (roster(entry()), roster({'name': 'c'}, {'name': 'c'})),
    (roster(entry(enabled=False, codex={'model': ''})), None),
    (roster(entry(claude={})), None),
    (roster(entry()), roster({'name': 'c', 'claude': {}})),
    (roster(entry()), roster({'name': 'c', 'codex': {'unknown': 'x'}})),
    (roster(entry()), roster({'name': 'new', 'vendor': 'codex'})),
])
def test_invalid_even_disabled_entries_refused(defaults, override, resolve):
    assert hasattr(lib, 'RosterError'), 'roster error missing'
    with pytest.raises(lib.RosterError):
        resolve(defaults, None if override is None else json.dumps(override))


def test_empty_selection_and_select_validation(resolve):
    result = resolve(roster(entry(enabled=False)))
    with pytest.raises(lib.RosterError):
        lib.select_entries(result)
    with pytest.raises(lib.RosterError):
        lib.select_entries(roster(entry(enabled=False, claude={})))


def test_preserves_opaque_settings_and_null_route_without_defaults(resolve):
    result = resolve(roster(entry('g', 'google', google={'route': 'gemini'},
                                 agy={'model': 'opaque'}, gemini={'effort': 'host-value'})),
                     json.dumps(roster({'name': 'g', 'google': {'route': None}})))
    assert result['legs'][0]['google'] == {'route': None}
    assert result['legs'][0]['gemini'] == {'effort': 'host-value'}
    assert result['legs'][0]['agy'] == {'model': 'opaque'}


def test_multiple_codex_entries_retained_separately(resolve):
    result = resolve(roster(entry('one'), entry('two')))
    assert [leg['name'] for leg in lib.select_entries(result)] == ['one', 'two']


def test_schema_reference_cannot_retrieve_remote(monkeypatch, resolve):
    import importlib
    import socket
    module = importlib.import_module('triad_dispatch_lib.roster')
    schema = lib.load_roster_contract()
    schema['$defs']['resolvedRoster'] = {'$ref': 'https://example.invalid/remote.json'}
    monkeypatch.setattr(module, 'load_roster_contract', lambda: schema)
    monkeypatch.setattr(socket.socket, 'connect', lambda *args: pytest.fail('network retrieval'))
    with pytest.raises(lib.ContractError):
        resolve(roster(entry()))
    for operation in (lib.merge_roster, lib.validate_resolved):
        with pytest.raises(lib.ContractError):
            operation(roster(entry()))


def test_roster_split_public_exports():
    import importlib
    module = importlib.import_module('triad_dispatch_lib.roster')
    for name in ('merge_roster', 'validate_resolved'):
        assert callable(getattr(lib, name, None)), f'{name} API missing'
        assert getattr(lib, name) is getattr(module, name)
        assert lib.__all__.count(name) == 1


def test_merge_roster_preserves_inherited_block_until_validation():
    defaults = roster(entry('claude', 'claude'))
    saved = copy.deepcopy(defaults)
    raw = json.dumps(roster({'name': 'claude', 'vendor': 'codex'}))
    merged = lib.merge_roster(defaults, raw)
    assert merged['legs'][0]['vendor'] == 'codex'
    assert merged['legs'][0]['claude'] == {}
    assert 'codex' not in merged['legs'][0]
    assert defaults == saved
    for operation in (lambda: lib.validate_resolved(merged),
                      lambda: lib.resolve_roster(defaults, raw),
                      lambda: lib.select_entries(merged)):
        with pytest.raises(lib.RosterError) as caught:
            operation()
        assert caught.value.code == 'schema_violation'
        assert str(caught.value) == 'Roster violates the canonical schema.'


def test_merge_roster_returns_incomplete_append():
    defaults = roster(entry())
    appended = {'name': 'new', 'vendor': 'codex'}
    raw = json.dumps(roster(appended))
    merged = lib.merge_roster(defaults, raw)
    assert [leg['name'] for leg in merged['legs']] == ['c', 'new']
    assert merged['legs'][1] == appended
    for operation in (lambda: lib.validate_resolved(merged),
                      lambda: lib.resolve_roster(defaults, raw)):
        with pytest.raises(lib.RosterError) as caught:
            operation()
        assert caught.value.code == 'schema_violation'


@pytest.mark.parametrize('defaults,override,code', [
    (roster(entry(unknown=True)), '{', 'schema_violation'),
    (roster(entry(), entry()), '{', 'duplicate_name'),
    (roster(entry(unknown=True), entry()), None, 'schema_violation'),
    (roster(entry()), roster({'name': 'c'}, {'name': 'c'}), 'duplicate_name'),
    (roster(entry()), roster({'name': 'c', 'unknown': True}, {'name': 'c'}), 'schema_violation'),
    (roster(entry()), 'null', 'schema_violation'),
])
def test_merge_roster_input_refusal_codes_and_precedence(defaults, override, code):
    raw = json.dumps(override) if isinstance(override, dict) else override
    with pytest.raises(lib.RosterError) as caught:
        lib.merge_roster(defaults, raw)
    assert caught.value.code == code


def test_validate_resolved_returns_none_without_mutation():
    value = roster(entry(codex={'model': 'chosen', 'reasoning': 'high'}))
    saved = copy.deepcopy(value)
    assert lib.validate_resolved(value) is None
    assert value == saved


@pytest.mark.parametrize('value,code', [
    (roster(entry(), entry()), 'duplicate_name'),
    (roster(entry(unknown=True), entry()), 'schema_violation'),
    (roster(entry(enabled=False, claude={})), 'schema_violation'),
])
def test_validate_resolved_refuses_invalid_rosters(value, code):
    with pytest.raises(lib.RosterError) as caught:
        lib.validate_resolved(value)
    assert caught.value.code == code


def test_merge_roster_no_override_is_independent():
    defaults = roster(entry(codex={'model': 'chosen'}))
    saved = copy.deepcopy(defaults)
    merged = lib.merge_roster(defaults)
    merged['legs'][0]['codex']['model'] = 'changed'
    merged['legs'].append(entry('new'))
    assert defaults == saved


@pytest.mark.parametrize('defaults,names', [
    (roster(), []), (roster(entry(enabled=False)), []),
    (roster(entry('c'), entry('C')), ['c', 'C']),
])
def test_split_resolution_retains_empty_disabled_and_case_sensitive_names(defaults, names):
    merged = lib.merge_roster(defaults)
    assert merged == defaults
    assert lib.validate_resolved(merged) is None
    assert lib.resolve_roster(defaults) == merged
    if names:
        assert [leg['name'] for leg in lib.select_entries(merged)] == names
    else:
        with pytest.raises(lib.RosterError) as caught:
            lib.select_entries(merged)
        assert caught.value.code == 'empty_selection'


def test_resolve_roster_uses_one_schema_snapshot(monkeypatch):
    import importlib
    module = importlib.import_module('triad_dispatch_lib.roster')
    schema = lib.load_roster_contract()
    loads, events = [], []
    def load():
        loads.append(True)
        assert len(loads) == 1, 'resolver loaded a second schema snapshot'
        return schema
    validate = module._validate
    def observed(value, received, *, resolved):
        events.append((received, resolved))
        return validate(value, received, resolved=resolved)
    monkeypatch.setattr(module, 'load_roster_contract', load)
    monkeypatch.setattr(module, '_validate', observed)
    result = lib.resolve_roster(roster(entry(codex={'model': 'chosen', 'reasoning': 'high'})),
                               json.dumps(roster({'name': 'c', 'codex': {'model': None}})))
    assert result['legs'][0]['codex'] == {'model': None, 'reasoning': 'high'}
    assert len(loads) == 1
    assert [flag for _, flag in events] == [True, False, True]
    assert all(received is schema for received, _ in events)


@pytest.mark.parametrize('raw', ['{', '{"schema":"triad-review-legs.v2","legs":[],"legs":[]}',
                                 '{"schema":"triad-review-legs.v2","legs":[],"x":NaN}',
                                 bytes([255]), 42])
def test_merge_roster_strict_json_refusal(raw):
    with pytest.raises(lib.RosterError) as caught:
        lib.merge_roster(roster(entry()), raw)
    assert caught.value.code == 'invalid_json'
    assert str(raw) not in str(caught.value)

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


def resolve(defaults, overrides=None):
    assert callable(getattr(lib, 'resolve_roster', None)), 'roster resolver missing'
    return lib.resolve_roster(defaults, overrides)


def test_recursive_partial_null_merge_and_copy():
    defaults = roster(entry(codex={'model': 'chosen', 'reasoning': 'high'}))
    saved = copy.deepcopy(defaults)
    result = resolve(defaults, json.dumps(roster({'name': 'c', 'codex': {'model': None}})))
    assert result['legs'][0]['codex'] == {'model': None, 'reasoning': 'high'}
    result['legs'][0]['codex']['reasoning'] = 'low'
    assert defaults == saved
    assert resolve(defaults)['legs'][0]['codex'] == saved['legs'][0]['codex']


def test_four_routes_same_family_order_and_selection_copy():
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
def test_strict_json_refusal_is_fixed_roster_error(raw):
    assert hasattr(lib, 'RosterError'), 'roster error missing'
    with pytest.raises(lib.RosterError) as caught:
        resolve(roster(entry()), raw)
    assert caught.value.code
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
def test_invalid_even_disabled_entries_refused(defaults, override):
    assert hasattr(lib, 'RosterError'), 'roster error missing'
    with pytest.raises(lib.RosterError):
        resolve(defaults, None if override is None else json.dumps(override))


def test_empty_selection_and_select_validation():
    result = resolve(roster(entry(enabled=False)))
    with pytest.raises(lib.RosterError):
        lib.select_entries(result)
    with pytest.raises(lib.RosterError):
        lib.select_entries(roster(entry(enabled=False, claude={})))


def test_preserves_opaque_settings_and_null_route_without_defaults():
    result = resolve(roster(entry('g', 'google', google={'route': 'gemini'},
                                 agy={'model': 'opaque'}, gemini={'effort': 'host-value'})),
                     json.dumps(roster({'name': 'g', 'google': {'route': None}})))
    assert result['legs'][0]['google'] == {'route': None}
    assert result['legs'][0]['gemini'] == {'effort': 'host-value'}
    assert result['legs'][0]['agy'] == {'model': 'opaque'}


def test_multiple_codex_entries_retained_separately():
    result = resolve(roster(entry('one'), entry('two')))
    assert [leg['name'] for leg in lib.select_entries(result)] == ['one', 'two']


def test_schema_reference_cannot_retrieve_remote(monkeypatch):
    import importlib
    import socket
    module = importlib.import_module('triad_dispatch_lib.roster')
    schema = lib.load_roster_contract()
    schema['$defs']['resolvedRoster'] = {'$ref': 'https://example.invalid/remote.json'}
    monkeypatch.setattr(module, 'load_roster_contract', lambda: schema)
    monkeypatch.setattr(socket.socket, 'connect', lambda *args: pytest.fail('network retrieval'))
    with pytest.raises(lib.ContractError):
        resolve(roster(entry()))

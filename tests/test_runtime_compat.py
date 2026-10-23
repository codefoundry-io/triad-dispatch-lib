"""Pure runtime decisions: exact bindings, complete validation and safe retention."""
from dataclasses import FrozenInstanceError, replace
from collections import UserList
import copy
import hashlib
import json
import pickle

import pytest
import triad_dispatch_lib as lib


@pytest.mark.parametrize('code', [
    'invalid_descriptor', 'invalid_binding', 'unsupported_schema', 'invalid_selector',
    'missing_context', 'unknown_binding', 'ambiguous_binding', 'unsupported_binding',
    'command_mismatch', 'capability_mismatch', 'invalid_inventory', 'incomplete_inventory',
])
@pytest.mark.parametrize('operation', [copy.copy, copy.deepcopy,
                                      lambda value: pickle.loads(pickle.dumps(value))],
                         ids=['copy', 'deepcopy', 'pickle'])
def test_runtime_errors_preserve_code_and_state_across_copy_and_pickle(code, operation):
    error = lib.RuntimeCompatibilityError(code)
    error.context = {'operation': ['decision']}
    restored = operation(error)
    assert restored is not error
    assert type(restored) is lib.RuntimeCompatibilityError
    assert restored.code == code
    assert restored.args == error.args
    assert restored.__dict__ == error.__dict__


def document(**changes):
    return dict(schema='triad-consumer-binding.v1', consumer='host-a',
                baseline_digest='a' * 64, library_digest='b' * 64,
                adapter='native-v2', capabilities=['native', 'json'],
                commands=['triad-review', 'triad-investigate'],
                context_digest='c' * 64) | changes


def binding(**changes):
    return lib.validate_consumer_binding(document(**changes))


def runtime(*bindings, **changes):
    return lib.validate_runtime_descriptor(dict(
        schema='triad-runtime-compat.v1', artifact_digest='d' * 64,
        commands=['triad-review', 'triad-investigate'], capabilities=['native', 'json'],
        supported_bindings=[b.binding_id for b in bindings]) | changes)


def refuses(code, operation, *args, **kwargs):
    with pytest.raises(lib.RuntimeCompatibilityError) as caught:
        operation(*args, **kwargs)
    assert caught.value.code == code
    assert 'private-secret' not in str(caught.value)


def test_canonical_binding_identity_and_immutable_normalization():
    # Omitting any context field or failing to sort changes the independently encoded identity.
    doc = document()
    original = json.loads(json.dumps(doc))
    result = lib.validate_consumer_binding(doc)
    canonical = ('{"adapter":"native-v2","baseline_digest":"' + 'a' * 64 +
                 '","capabilities":["json","native"],"commands":["triad-investigate","triad-review"],'
                 '"consumer":"host-a","context_digest":"' + 'c' * 64 +
                 '","library_digest":"' + 'b' * 64 + '","schema":"triad-consumer-binding.v1"}')
    assert result.binding_id == hashlib.sha256(canonical.encode()).hexdigest()
    assert result.commands == ('triad-investigate', 'triad-review')
    assert result.capabilities == ('json', 'native')
    assert doc == original
    assert binding(context_digest='e' * 64).binding_id != result.binding_id
    with pytest.raises(FrozenInstanceError):
        result.consumer = 'other'


@pytest.mark.parametrize('change', [
    {'consumer': True}, {'consumer': ''}, {'consumer': 'a' * 129},
    {'adapter': '../private-secret'}, {'commands': []}, {'commands': ['../x']},
    {'commands': ['a/b']}, {'commands': ['a\x00']}, {'commands': ['a', 'a']},
    {'commands': 'triad-review'}, {'commands': [True]}, {'capabilities': ['x', 'x']},
    {'capabilities': [False]}, {'baseline_digest': 'A' * 64}, {'library_digest': 'b' * 63},
    {'context_digest': None}, {'private-secret': 'private-secret'}, {'binding_id': 'a' * 64},
])
def test_binding_refuses_invalid_shape_and_values(change):
    refuses('invalid_binding', lib.validate_consumer_binding, document(**change))


@pytest.mark.parametrize('field', list(document()))
def test_binding_requires_every_field(field):
    doc = document()
    del doc[field]
    refuses('invalid_binding', lib.validate_consumer_binding, doc)


@pytest.mark.parametrize('value', [None, [], 'private-secret', True])
def test_binding_refuses_non_documents(value):
    refuses('invalid_binding', lib.validate_consumer_binding, value)


def test_schema_refusal_and_empty_optional_capabilities():
    refuses('unsupported_schema', lib.validate_consumer_binding, document(schema='future'))
    b = binding(capabilities=[])
    r = runtime(b, capabilities=[])
    assert lib.check_consumer_compatibility(r, b) is None
    assert r.supported_bindings == (b.binding_id,)


@pytest.mark.parametrize('change', [
    {'artifact_digest': True}, {'artifact_digest': 'A' * 64}, {'supported_bindings': []},
    {'supported_bindings': ['x']}, {'supported_bindings': ['a' * 64, 'a' * 64]},
    {'commands': []}, {'commands': ['a', 'a']}, {'capabilities': ['x', 'x']},
    {'private-secret': 'private-secret'}, {'commands': {'a'}},
])
def test_runtime_refuses_invalid_metadata(change):
    b = binding()
    refuses('invalid_descriptor', runtime, b, **change)


def test_runtime_schema_is_checked():
    refuses('unsupported_schema', runtime, binding(), schema='future')


@pytest.mark.parametrize('value', [None, [], True, 'private-secret', {},
                                 {'schema': 'triad-runtime-compat.v1'}])
def test_runtime_requires_a_complete_document(value):
    refuses('invalid_descriptor', lib.validate_runtime_descriptor, value)


@pytest.mark.parametrize('field', ['commands', 'capabilities'])
def test_binding_documents_require_json_lists(field):
    doc = document()
    doc[field] = tuple(doc[field])
    refuses('invalid_binding', lib.validate_consumer_binding, doc)


@pytest.mark.parametrize('field', ['commands', 'capabilities', 'supported_bindings'])
def test_runtime_documents_require_json_lists(field):
    b = binding()
    doc = dict(schema='triad-runtime-compat.v1', artifact_digest='d' * 64,
               commands=['triad-review'], capabilities=[], supported_bindings=[b.binding_id])
    doc[field] = tuple(doc[field])
    refuses('invalid_descriptor', lib.validate_runtime_descriptor, doc)


@pytest.mark.parametrize('field', ['commands', 'capabilities'])
def test_operations_refuse_mutable_binding_record_fields(field):
    b = binding()
    mutable = replace(b, **{field: list(getattr(b, field))})
    refuses('invalid_binding', lib.check_consumer_compatibility, runtime(b), mutable)
    refuses('invalid_binding', lib.select_consumer_binding, runtime(b), [b, mutable],
            explicit_binding=b.binding_id, legacy_binding=None)


@pytest.mark.parametrize('field', ['commands', 'capabilities', 'supported_bindings'])
def test_operations_refuse_mutable_runtime_record_fields(field):
    b = binding()
    r = runtime(b)
    mutable = replace(r, **{field: list(getattr(r, field))})
    refuses('invalid_descriptor', lib.check_consumer_compatibility, mutable, b)
    refuses('invalid_descriptor', lib.select_consumer_binding, mutable, [b],
            explicit_binding=b.binding_id, legacy_binding=None)


def test_compatibility_requires_exact_membership_commands_and_capabilities():
    b = binding()
    refuses('unsupported_binding', lib.check_consumer_compatibility,
            runtime(b), binding(context_digest='e' * 64))
    refuses('command_mismatch', lib.check_consumer_compatibility,
            runtime(b, commands=['triad-review']), b)
    refuses('capability_mismatch', lib.check_consumer_compatibility,
            runtime(b, capabilities=[]), b)


@pytest.mark.parametrize('change', [{'binding_id': 'e' * 64}, {'consumer': True},
                                    {'commands': ('x', 'x')}, {'schema': 'future'}])
def test_operations_revalidate_directly_constructed_bindings(change):
    b = binding()
    bad = replace(b, **change)
    code = 'unsupported_schema' if change.get('schema') else 'invalid_binding'
    refuses(code, lib.check_consumer_compatibility, runtime(b), bad)
    refuses(code, lib.select_consumer_binding, runtime(b), [b, bad],
            explicit_binding=b.binding_id, legacy_binding=None)


def test_operations_revalidate_directly_constructed_runtime():
    b = binding()
    refuses('invalid_descriptor', lib.check_consumer_compatibility,
            replace(runtime(b), supported_bindings=()), b)


def test_explicit_and_established_legacy_selection_are_order_independent():
    a, b = binding(), binding(consumer='host-b')
    r = runtime(a, b)
    for inventory in ([a, b], [b, a]):
        assert lib.select_consumer_binding(r, inventory, explicit_binding=b.binding_id,
                                           legacy_binding=a.binding_id) == b
        assert lib.select_consumer_binding(r, inventory, explicit_binding=None,
                                           legacy_binding=a.binding_id) == a


@pytest.mark.parametrize('explicit,legacy,code', [
    (None, None, 'missing_context'), ('', None, 'invalid_selector'),
    (True, None, 'invalid_selector'), ('private-secret', None, 'invalid_selector'),
    ('e' * 64, None, 'unknown_binding'), (None, 'e' * 64, 'unknown_binding'),
    (None, '', 'invalid_selector'),
])
def test_selection_never_guesses_or_falls_back(explicit, legacy, code):
    b = binding()
    refuses(code, lib.select_consumer_binding, runtime(b), [b],
            explicit_binding=explicit, legacy_binding=legacy)


def test_complete_inventory_refuses_duplicate_and_unselected_invalid_members():
    b = binding()
    refuses('ambiguous_binding', lib.select_consumer_binding, runtime(b), [b, b],
            explicit_binding=b.binding_id, legacy_binding=None)
    refuses('invalid_binding', lib.select_consumer_binding, runtime(b), [b, object()],
            explicit_binding=b.binding_id, legacy_binding=None)


def test_selection_checks_runtime_support_and_inventory_type():
    b = binding()
    other = binding(consumer='host-b')
    refuses('unsupported_binding', lib.select_consumer_binding, runtime(other), [b],
            explicit_binding=b.binding_id, legacy_binding=None)
    refuses('invalid_inventory', lib.select_consumer_binding, runtime(b), 'private-secret',
            explicit_binding=b.binding_id, legacy_binding=None)
    refuses('invalid_descriptor', lib.select_consumer_binding, object(), [b],
            explicit_binding=b.binding_id, legacy_binding=None)


def test_retention_preserves_active_and_consumer_references_and_unknown_use():
    a, b, c = 'a' * 64, 'b' * 64, 'c' * 64
    result = lib.plan_runtime_retention([c, b, a], consumer_references=[b, b],
                                       active_references=[a], dependencies_known=True)
    assert (result.retain, result.remove, result.diagnostic) == ((a, b), (c,), 'references_preserved')
    unknown = lib.plan_runtime_retention([b, a], consumer_references=[],
                                        active_references=[], dependencies_known=False)
    assert (unknown.retain, unknown.remove, unknown.diagnostic) == ((a, b), (), 'dependencies_unknown')
    empty = lib.plan_runtime_retention([], consumer_references=[], active_references=[],
                                      dependencies_known=True)
    assert (empty.retain, empty.remove) == ((), ())


@pytest.mark.parametrize('artifacts,consumers,active,known,code', [
    (['a' * 64] * 2, [], [], True, 'invalid_inventory'),
    (['A' * 64], [], [], True, 'invalid_inventory'),
    (['a' * 64], ['b' * 64], [], True, 'incomplete_inventory'),
    (['a' * 64], [], ['b' * 64], False, 'incomplete_inventory'),
    (['a' * 64], [], [], 1, 'invalid_inventory'),
    ('a' * 64, [], [], True, 'invalid_inventory'),
    ([], [True], [], True, 'invalid_inventory'),
])
def test_retention_refuses_incomplete_or_malformed_inventories(artifacts, consumers, active, known, code):
    refuses(code, lib.plan_runtime_retention, artifacts, consumer_references=consumers,
            active_references=active, dependencies_known=known)


@pytest.mark.parametrize('field', ['artifacts', 'consumer_references', 'active_references'])
def test_retention_refuses_sequence_containers_outside_list_tuple(field):
    args = dict(artifacts=['a' * 64], consumer_references=[], active_references=[],
                dependencies_known=True)
    args[field] = UserList(args[field])
    refuses('invalid_inventory', lib.plan_runtime_retention, **args)


def test_retention_accepts_tuple_inventories_without_mutation():
    artifact = 'a' * 64
    result = lib.plan_runtime_retention((artifact,), consumer_references=(artifact,),
                                       active_references=(), dependencies_known=True)
    assert (result.retain, result.remove) == ((artifact,), ())

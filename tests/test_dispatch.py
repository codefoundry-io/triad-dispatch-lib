import asyncio
import copy
import json

import pytest
import triad_dispatch_lib as lib
from tests.test_roster import entry
from tests.test_verdict import BASE, BINDINGS
from tests.test_output import wrap


def run_scenario(coro):
    # A broken coordinator must fail these barrier tests instead of hanging CI.
    async def bounded():
        async with asyncio.timeout(10):
            return await coro
    return asyncio.run(bounded())


def requests():
    assert hasattr(lib, 'ReviewRequest'), 'async coordinator API missing'
    return [lib.ReviewRequest(
        entry(name, family, **({'google': {'route': route}, route: {}} if route else {})),
        {k: (dict(BASE, leg_name=name, family=family, route=route))[k] for k in BINDINGS},
        'Complete review scope')
        for name, family, route in [('c', 'codex', None), ('a', 'claude', None),
                                    ('g', 'google', 'gemini'), ('y', 'google', 'agy')]]


async def preflight(request):
    return None


async def integrity():
    return True


def output(request):
    carrier = {'codex': 'native-final', 'claude': 'claude-json',
               'gemini': 'gemini-json', 'agy': 'agy-stream-json'}[
                   request.expected['route'] or request.expected['family']]
    return lib.ProviderOutput(carrier, wrap(json.dumps(BASE | request.expected), carrier), 0, True)


def test_four_routes_overlap_preserve_order_and_admit_carriers():
    async def scenario():
        selected = requests()
        started, release = asyncio.Event(), asyncio.Event()
        seen = []
        async def invoke(request):
            seen.append(request.entry['name'])
            if len(seen) == 4:
                started.set()
            await release.wait()
            return output(request)
        task = asyncio.create_task(lib.run_review(selected, invoke, preflight=preflight,
                                                  integrity_check=integrity, max_concurrency=4))
        await started.wait()
        release.set()
        result = await task
        assert [o.name for o in result.outcomes] == ['c', 'a', 'g', 'y']
        assert [o.status for o in result.outcomes] == ['completed'] * 4
        assert result.agreement.agreed
    run_scenario(scenario())


def test_ceiling_and_reverse_completion_and_same_family_siblings():
    async def scenario():
        selected = [requests()[0], lib.ReviewRequest(entry('second'),
                    requests()[0].expected | {'leg_name': 'second'}, 'another perspective'),
                    requests()[1]]
        gates = {r.entry['name']: asyncio.Event() for r in selected}
        pair, third = asyncio.Event(), asyncio.Event()
        active, peak, seen = 0, 0, []
        async def invoke(request):
            nonlocal active, peak
            name = request.entry['name']
            seen.append(name)
            active += 1
            peak = max(peak, active)
            if len(seen) == 2:
                pair.set()
            if len(seen) == 3:
                third.set()
            await gates[name].wait()
            active -= 1
            return output(request)
        task = asyncio.create_task(lib.run_review(selected, invoke, preflight=preflight,
                                                  integrity_check=integrity, max_concurrency=2))
        await pair.wait()
        assert seen == ['c', 'second']
        gates['second'].set()
        await third.wait()
        gates['a'].set()
        gates['c'].set()
        result = await task
        assert peak == 2
        assert [o.name for o in result.outcomes] == ['c', 'second', 'a']
        assert result.agreement.agreed
    run_scenario(scenario())


@pytest.mark.parametrize('mutation', ['empty', 'duplicate', 'disabled', 'invalid', 'basis',
                                    'name', 'family', 'route', 'unresolved'])
def test_invalid_selection_refused_before_any_callback(mutation):
    selected = requests()
    if mutation == 'empty': selected = []
    elif mutation == 'duplicate': selected.append(selected[0])
    elif mutation == 'disabled': selected[0].entry['enabled'] = False
    elif mutation == 'invalid': selected[0].entry['codex']['unknown'] = 'secret'
    elif mutation == 'basis': selected[1].expected['review_id'] = 'different'
    elif mutation == 'unresolved': selected[2].entry['google']['route'] = None
    else: selected[2].expected[{'name': 'leg_name', 'family': 'family', 'route': 'route'}[mutation]] = {
        'name': 'other', 'family': 'codex', 'route': 'agy'}[mutation]
    async def forbidden(*args):
        pytest.fail('callback ran for invalid selection')
    with pytest.raises(lib.DispatchError):
        asyncio.run(lib.run_review(selected, forbidden, preflight=forbidden,
                                   integrity_check=forbidden, max_concurrency=2))


@pytest.mark.parametrize('limit', [0, -1, True, 1.5, None])
def test_concurrency_is_positive_exact_integer(limit):
    selected = requests()
    with pytest.raises(lib.DispatchError):
        asyncio.run(lib.run_review(selected, preflight, preflight=preflight,
                                   integrity_check=integrity, max_concurrency=limit))


@pytest.mark.parametrize('behavior', ['raise', 'return', 'cancel'])
def test_all_preflights_finish_before_invoke_and_failure_aborts(behavior):
    async def check(request):
        if request.entry['name'] == 'y':
            if behavior == 'raise': raise RuntimeError('private error')
            if behavior == 'cancel': raise asyncio.CancelledError
            return True
    async def forbidden(request):
        pytest.fail('invoke ran before all preflights succeeded')
    selected = requests()
    with pytest.raises(lib.DispatchError) as caught:
        asyncio.run(lib.run_review(selected, forbidden, preflight=check,
                                   integrity_check=integrity, max_concurrency=2))
    assert 'private error' not in str(caught.value)


def test_callback_mutation_cannot_change_saved_binding_or_other_callbacks():
    selected = requests()
    async def check(request):
        request.expected['review_id'] = 'mutated'
        request.entry['enabled'] = False
    async def invoke(request):
        result = output(request)
        request.expected['content_digest'] = 'b' * 64
        selected[-1].expected['review_id'] = 'outside mutation'
        return result
    result = asyncio.run(lib.run_review(selected, invoke, preflight=check,
                                       integrity_check=integrity, max_concurrency=1))
    assert result.agreement.agreed


def test_real_deadline_late_success_exception_and_self_cancel_preserve_peers():
    async def scenario():
        selected = requests()
        selected[0].entry['timeout_s'] = 1
        cleaned = asyncio.Event()
        calls = []
        async def invoke(request):
            name = request.entry['name']
            calls.append(name)
            if name == 'c':
                try:
                    await asyncio.Event().wait()
                except asyncio.CancelledError:
                    cleaned.set()
                    return output(request)
            if name == 'a': raise RuntimeError('private provider text')
            if name == 'g': raise asyncio.CancelledError
            return output(request)
        result = await lib.run_review(selected, invoke, preflight=preflight,
                                      integrity_check=integrity, max_concurrency=4)
        assert cleaned.is_set()
        assert [o.status for o in result.outcomes] == ['timed_out', 'failed', 'failed', 'completed']
        assert [o.error_code for o in result.outcomes] == ['timed_out', 'callback_failed', 'callback_failed', None]
        assert result.outcomes[0].value is None
        assert sorted(calls) == ['a', 'c', 'g', 'y']
        assert not result.agreement.agreed
    run_scenario(scenario())


@pytest.mark.parametrize('stage', ['preflight', 'invoke', 'integrity'])
def test_parent_cancel_awaits_child_cleanup_and_propagates(stage):
    async def scenario():
        entered, cleaning, release = asyncio.Event(), asyncio.Event(), asyncio.Event()
        async def blocked(*args):
            entered.set()
            try:
                await asyncio.Event().wait()
            finally:
                cleaning.set()
                await release.wait()
        async def invoke(request): return output(request)
        task = asyncio.create_task(lib.run_review(requests(), blocked if stage == 'invoke' else invoke,
                    preflight=blocked if stage == 'preflight' else preflight,
                    integrity_check=blocked if stage == 'integrity' else integrity, max_concurrency=4))
        await entered.wait()
        task.cancel()
        await cleaning.wait()
        assert not task.done()
        release.set()
        with pytest.raises(asyncio.CancelledError): await task
    run_scenario(scenario())


@pytest.mark.parametrize('value', [False, 1, None, 'raise', 'cancel'])
def test_integrity_failure_keeps_completed_outcomes_and_blocks(value):
    async def check():
        if value == 'raise': raise RuntimeError('private')
        if value == 'cancel': raise asyncio.CancelledError
        return value
    async def invoke(request): return output(request)
    result = asyncio.run(lib.run_review(requests(), invoke, preflight=preflight,
                                       integrity_check=check, max_concurrency=4))
    assert all(o.status == 'completed' for o in result.outcomes)
    assert len(result.agreement.verdicts) == 4
    assert not result.agreement.agreed and not result.agreement.integrity_ok


def test_investigations_keep_prompts_settings_and_are_ordinary_data():
    async def scenario():
        selected = [lib.InvestigationRequest(r.entry, 'custom question', True) for r in requests()]
        selected[2].entry['gemini'] = {'model': 'opaque', 'effort': 'host-effort'}
        observed = []
        async def invoke(request):
            observed.append(copy.deepcopy(request))
            return {'verdict': 'SAFE TO MERGE', 'ordinary': True}
        result = await lib.run_investigations(selected, invoke, preflight=preflight, max_concurrency=2)
        assert isinstance(result, tuple) and len(result) == 4
        assert all(o.value == {'verdict': 'SAFE TO MERGE', 'ordinary': True} for o in result)
        assert observed[0].prompt == 'custom question'
        assert observed[2].prompt.startswith('custom question\n\n')
        assert 'google_web_search' in observed[2].prompt
        assert observed[2].entry['gemini'] == {'model': 'opaque', 'effort': 'host-effort'}
        assert 'search_web' in observed[3].prompt
        assert not hasattr(result, 'agreement')
    run_scenario(scenario())


def test_invalid_callback_value_is_per_leg_failure_and_terminal_failure_is_admitted_separately():
    async def invoke(request):
        if request.entry['name'] == 'c': return {'private': 'invalid provider output'}
        result = output(request)
        if request.entry['name'] == 'a':
            return lib.ProviderOutput(result.carrier, result.stdout, 1, True)
        return result
    result = asyncio.run(lib.run_review(requests(), invoke, preflight=preflight,
                                       integrity_check=integrity, max_concurrency=4))
    assert [o.status for o in result.outcomes] == ['failed', 'completed', 'completed', 'completed']
    assert result.outcomes[0].error_code == 'callback_failed'
    assert result.agreement.reasons == {'c': 'missing_output', 'a': 'nonzero_exit'}


def test_preflight_real_deadline_prevents_invocation_and_awaits_cleanup():
    async def scenario():
        selected = requests()
        selected[0].entry['timeout_s'] = 1
        cleaned = asyncio.Event()
        async def check(request):
            if request.entry['name'] == 'c':
                try: await asyncio.Event().wait()
                finally: cleaned.set()
        async def forbidden(request): pytest.fail('invoke after timed-out preflight')
        with pytest.raises(lib.DispatchError) as caught:
            await lib.run_review(selected, forbidden, preflight=check,
                                 integrity_check=integrity, max_concurrency=4)
        assert caught.value.code == 'preflight_failed'
        assert cleaned.is_set()
    run_scenario(scenario())


def test_queued_invoke_has_its_full_deadline_after_slot_acquisition():
    async def scenario():
        selected = requests()[:2]
        for request in selected: request.entry['timeout_s'] = 1
        async def invoke(request):
            if request.entry['name'] == 'c': await asyncio.Event().wait()
            return output(request)
        result = await lib.run_review(selected, invoke, preflight=preflight,
                                      integrity_check=integrity, max_concurrency=1)
        assert [o.status for o in result.outcomes] == ['timed_out', 'completed']
        assert result.outcomes[1].value is not None
    run_scenario(scenario())


@pytest.mark.parametrize('site', ['roster', 'prompt', 'admission'])
def test_library_contract_errors_propagate(site, monkeypatch):
    import triad_dispatch_lib.dispatch as dispatch
    import triad_dispatch_lib.verdict as verdict
    selected = requests()
    def broken(*args, **kwargs): raise lib.ContractError('broken packaged contract')
    async def invoke(request): return output(request)
    if site == 'admission':
        # Preparation calls validate_binding too: fail only once invocation ran.
        async def invoke(request):
            monkeypatch.setattr(verdict, 'load_contract', broken)
            return output(request)
    elif site == 'roster': monkeypatch.setattr(dispatch, 'resolve_roster', broken)
    else: monkeypatch.setattr(dispatch, 'render_investigation_prompt', broken)
    with pytest.raises(lib.ContractError):
        if site == 'prompt':
            asyncio.run(lib.run_investigations([lib.InvestigationRequest(selected[0].entry, 'q')],
                        invoke, preflight=preflight, max_concurrency=1))
        else:
            asyncio.run(lib.run_review(selected, invoke, preflight=preflight,
                        integrity_check=integrity, max_concurrency=4))


@pytest.mark.parametrize('selected', [None, 42, [object()]])
def test_malformed_request_collection_is_fixed_refusal(selected):
    with pytest.raises(lib.DispatchError):
        asyncio.run(lib.run_review(selected, preflight, preflight=preflight,
                                   integrity_check=integrity, max_concurrency=1))


@pytest.mark.parametrize('repeated', [False, True])
def test_parent_cancellation_during_deadline_cleanup_waits_without_recancelling(repeated):
    async def scenario():
        selected = requests()[:1]
        selected[0].entry['timeout_s'] = 1
        cleaning, release, finished = asyncio.Event(), asyncio.Event(), asyncio.Event()
        async def invoke(request):
            try:
                await asyncio.Event().wait()
            finally:
                cleaning.set()
                await release.wait()
                finished.set()
        task = asyncio.create_task(lib.run_review(selected, invoke, preflight=preflight,
                    integrity_check=integrity, max_concurrency=1))
        await cleaning.wait()  # A real deadline has already cancelled the child once.
        task.cancel()
        for _ in range(3): await asyncio.sleep(0)
        if repeated:
            task.cancel()
            for _ in range(3): await asyncio.sleep(0)
        release.set()
        with pytest.raises(asyncio.CancelledError): await task
        assert finished.is_set(), 'parent cancellation interrupted child deadline cleanup'
    run_scenario(scenario())


@pytest.mark.parametrize('stage', ['preflight', 'invoke', 'integrity'])
def test_callback_contract_error_is_distinct_and_owned_peers_settle(stage):
    async def scenario():
        selected = requests()[:2]
        selected[1].entry['timeout_s'] = 1
        all_started, release = asyncio.Event(), asyncio.Event()
        peer_cleaning, peer_finished = asyncio.Event(), asyncio.Event()
        error = lib.ContractError('packaged contract is unavailable')
        started = 0
        async def callback(request):
            nonlocal started
            started += 1
            if started == 2: all_started.set()
            await all_started.wait()
            if request.entry['name'] == 'c': raise error
            try:
                await release.wait()
            finally:
                peer_cleaning.set()
                await release.wait()
                peer_finished.set()
            return None if stage == 'preflight' else output(request)
        async def invoke(request): return output(request)
        async def bad_integrity(): raise error
        task = asyncio.create_task(lib.run_review(selected,
                    callback if stage == 'invoke' else invoke,
                    preflight=callback if stage == 'preflight' else preflight,
                    integrity_check=bad_integrity if stage == 'integrity' else integrity,
                    max_concurrency=2))
        if stage != 'integrity':
            await all_started.wait()
            await peer_cleaning.wait()
            assert not task.done(), 'contract failure escaped before peer cleanup'
            release.set()
        with pytest.raises(lib.ContractError) as caught: await task
        assert caught.value is error
        if stage != 'integrity': assert peer_finished.is_set()
    run_scenario(scenario())


@pytest.mark.parametrize('stage', ['preflight', 'invoke'])
def test_callback_contract_error_during_deadline_cleanup_is_preserved(stage):
    selected = requests()[:1]
    selected[0].entry['timeout_s'] = 1
    async def broken(request):
        try:
            await asyncio.Event().wait()
        finally:
            raise lib.ContractError('contract unavailable during cleanup')
    async def invoke(request): return output(request)
    with pytest.raises(lib.ContractError):
        asyncio.run(lib.run_review(selected, broken if stage == 'invoke' else invoke,
                    preflight=broken if stage == 'preflight' else preflight,
                    integrity_check=integrity, max_concurrency=1))

"""Bounded async coordination; execution and native process custody stay in hosts.

Callbacks must cooperate with cancellation and reap their own native processes.
Preflight checks actual model/effort/options/capabilities and must return None.
Completed calls describe callback delivery, not verdict admission: terminal
metadata and original verdict bytes are independently checked for agreement.
"""

import asyncio
from copy import deepcopy
from dataclasses import dataclass

from .agreement import AgreementResult, evaluate_agreement
from .errors import AdmissionError, DispatchError, RosterError
from .output import ProviderOutput
from .prompts import render_investigation_prompt
from .roster import resolve_roster
from .verdict import validate_binding


@dataclass(frozen=True)
class ReviewRequest:
    entry: dict
    expected: dict
    prompt: str


@dataclass(frozen=True)
class InvestigationRequest:
    entry: dict
    prompt: str
    web_authorized: bool = False


@dataclass(frozen=True)
class CallOutcome:
    name: str
    status: str
    value: object | None
    error_code: str | None


@dataclass(frozen=True)
class ReviewRun:
    outcomes: tuple[CallOutcome, ...]
    agreement: AgreementResult


def _prepare(requests, kind, max_concurrency, callbacks):
    if type(max_concurrency) is not int or max_concurrency < 1:
        raise DispatchError('invalid_concurrency')
    if any(not callable(callback) for callback in callbacks):
        raise DispatchError('invalid_callback')
    try:
        prepared = deepcopy(tuple(requests))
    except (TypeError, ValueError, RecursionError):
        raise DispatchError('invalid_requests') from None
    if not prepared:
        raise DispatchError('empty_selection')
    if any(not isinstance(request, kind) or not isinstance(request.prompt, str)
           or not isinstance(request.entry, dict) for request in prepared):
        raise DispatchError('invalid_requests')
    try:
        resolve_roster({'schema': 'triad-review-legs.v2',
                        'legs': [request.entry for request in prepared]})
    except RosterError:
        raise DispatchError('invalid_entries') from None
    basis = None
    for request in prepared:
        entry = request.entry
        if not entry['enabled']:
            raise DispatchError('disabled_entry')
        route = entry.get('google', {}).get('route') if entry['vendor'] == 'google' else None
        if entry['vendor'] == 'google' and route not in ('gemini', 'agy'):
            raise DispatchError('unresolved_route')
        if kind is ReviewRequest:
            try:
                validate_binding(request.expected)
            except AdmissionError:
                raise DispatchError('invalid_binding') from None
            if (request.expected['leg_name'], request.expected['family'], request.expected['route']) != (
                    entry['name'], entry['vendor'], route):
                raise DispatchError('binding_mismatch')
            current = (request.expected['review_id'], request.expected['content_digest'])
            if basis is not None and basis != current:
                raise DispatchError('mixed_basis')
            basis = current
        elif type(request.web_authorized) is not bool:
            raise DispatchError('invalid_requests')
    if kind is InvestigationRequest:
        prepared = tuple(InvestigationRequest(request.entry,
            render_investigation_prompt(request.prompt, family=request.entry['vendor'],
                route=request.entry.get('google', {}).get('route'),
                web_authorized=request.web_authorized), request.web_authorized)
            for request in prepared)
    return prepared


async def _call(callback, args, timeout=None):
    """Isolate child self-cancel and retain deadline status after late returns."""
    async def invoke():
        return await callback(*args)
    child = asyncio.create_task(invoke())
    try:
        done, _ = await asyncio.wait({child}, timeout=timeout)
        if not done:
            child.cancel()
            await asyncio.gather(child, return_exceptions=True)
            return 'timed_out', None
        try:
            return 'completed', child.result()
        except (Exception, asyncio.CancelledError):
            return 'failed', None
    except asyncio.CancelledError:
        child.cancel()
        await asyncio.gather(child, return_exceptions=True)
        raise


async def _bounded(requests, callback, max_concurrency, *, preflight=False, review=False):
    slots = asyncio.Semaphore(max_concurrency)
    async def one(request):
        async with slots:
            status, value = await _call(callback, (deepcopy(request),), request.entry['timeout_s'])
            if status == 'completed' and ((preflight and value is not None)
                    or (review and not isinstance(value, ProviderOutput))):
                status, value = 'failed', None
            return CallOutcome(request.entry['name'], status, value,
                               None if status == 'completed' else (
                                   'timed_out' if status == 'timed_out' else 'callback_failed'))
    children = [asyncio.create_task(one(request)) for request in requests]
    try:
        return tuple(await asyncio.gather(*children))
    except asyncio.CancelledError:
        for child in children:
            child.cancel()
        await asyncio.gather(*children, return_exceptions=True)
        raise


async def _preflight(requests, callback, max_concurrency):
    outcomes = await _bounded(requests, callback, max_concurrency, preflight=True)
    if any(outcome.status != 'completed' for outcome in outcomes):
        raise DispatchError('preflight_failed')


async def run_review(requests, invoke, *, preflight, integrity_check,
                     max_concurrency: int) -> ReviewRun:
    """Preflight all, invoke once per leg, then obtain fresh host integrity.

    Inputs and callback arguments are independent snapshots. Host integrity
    exceptions, self-cancellation and non-bool values block agreement while
    preserving outcomes. Cancellation of this coordinator propagates only after
    its owned callback tasks have settled.
    """
    prepared = _prepare(requests, ReviewRequest, max_concurrency,
                        (invoke, preflight, integrity_check))
    await _preflight(prepared, preflight, max_concurrency)
    outcomes = await _bounded(prepared, invoke, max_concurrency, review=True)
    status, integrity = await _call(integrity_check, ())
    agreement = evaluate_agreement(
        {request.entry['name']: request.expected for request in prepared},
        {outcome.name: outcome.value for outcome in outcomes if outcome.status == 'completed'},
        integrity_ok=status == 'completed' and integrity is True)
    return ReviewRun(outcomes, agreement)


async def run_investigations(requests, invoke, *, preflight,
                             max_concurrency: int) -> tuple[CallOutcome, ...]:
    """Return ordinary perspective evidence, with no formal admission or vote."""
    prepared = _prepare(requests, InvestigationRequest, max_concurrency, (invoke, preflight))
    await _preflight(prepared, preflight, max_concurrency)
    return await _bounded(prepared, invoke, max_concurrency)

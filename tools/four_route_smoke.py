"""Synthetic four-route proof using runtime functions from an isolated wheel."""
import argparse
import asyncio
import hashlib
from importlib.metadata import version
import inspect
import json
from pathlib import Path
import platform
import runpy
import subprocess


def helpers():
    return runpy.run_path(str(Path(__file__).with_name('verify_wheel.py')))


def identity(prefix, expected_version):
    import triad_dispatch_lib as lib
    if version('triad-dispatch-lib') != expected_version:
        raise ValueError('Installed version mismatch')
    paths = {}
    for name in lib.__all__:
        value = getattr(lib, name)
        path = Path(inspect.getfile(value))
        helpers()['verify_import'](path, prefix)
        paths[name] = str(path)
    helpers()['verify_import'](Path(lib.__file__), prefix)
    return dict(version=version('triad-dispatch-lib'), package_path=lib.__file__,
                runtime_paths=paths, python=platform.python_version(),
                platform=platform.platform(), machine=platform.machine())


def synthetic_smoke():
    import triad_dispatch_lib as lib
    routes = [('c', 'codex', None), ('a', 'claude', None),
              ('g', 'google', 'gemini'), ('y', 'google', 'agy')]
    defaults = {'schema': 'triad-review-legs.v2', 'legs': [
        dict(name=name, vendor=family, enabled=True, acceptance='required', timeout_s=30,
             **({family: {}} if route is None else {'google': {'route': route}, route: {}}))
        for name, family, route in routes]}
    selected = lib.select_entries(lib.resolve_roster(defaults, json.dumps({
        'schema': 'triad-review-legs.v2', 'legs': [{'name': 'y', 'acceptance': 'informational'}]})))
    assert [entry['name'] for entry in selected] == ['c', 'a', 'g', 'y']
    requests, profiles = [], []
    for entry, (name, family, route) in zip(selected, routes, strict=True):
        expected = dict(review_id='synthetic-four-route', family=family, route=route,
                        content_digest='a' * 64, leg_name=name, attempt=1)
        values = {'worktree': '"/synthetic"', 'brief-file': '"/synthetic/brief.md"',
                  'packet-files': '["/synthetic/brief.md"]', 'review-id': expected['review_id'],
                  'content-digest': expected['content_digest'], 'leg-name': name, 'attempt': '1'}
        if family == 'google':
            values['gated-patch-file'] = '"/synthetic/patch"'
        for host in ('A', 'B'):
            for phase in ('formal-plan', 'implementation-review', 'pre-merge'):
                for web in (False, True):
                    prompt = lib.render_review_clauses(family=family, host=host, route=route,
                        review_kind=phase, review_date='2026-10-12',
                        review_web_authorized=web, replacements=values)
                    assert f'independent {phase} review' in prompt
                    assert f'leg_name={name}' in prompt
                    if route:
                        assert f'route={route}' in prompt
                    profiles.append(dict(family=family, route=route, host=host, phase=phase,
                                         web=web, sha256=hashlib.sha256(prompt.encode()).hexdigest()))
                if route == 'agy' and host == 'A':
                    hooked = lib.render_review_clauses(family=family, host=host, route=route,
                        review_kind=phase, review_date='2026-10-12', review_web_authorized=False,
                        replacements=values, agy_hook_active=True)
                    assert 'PreToolUse hook' in hooked
                    profiles.append(dict(family=family, route=route, host=host, phase=phase,
                                         hook=True, sha256=hashlib.sha256(hooked.encode()).hexdigest()))
        requests.append(lib.ReviewRequest(entry, expected, prompt + '\nComplete synthetic scope'))

    def output(request, *, dissent=False, swap=False):
        expected = dict(request.expected)
        if swap and expected['route']:
            expected['route'] = 'agy' if expected['route'] == 'gemini' else 'gemini'
            expected['leg_name'] = 'y' if expected['leg_name'] == 'g' else 'g'
        verdict = dict(schema_version=2, **expected, verdict='SAFE TO MERGE',
                       criteria_checked=['correctness'], findings=[],
                       affected_surfaces_inspected=['synthetic.py'], open_questions=[])
        if dissent:
            verdict.update(verdict='DO NOT MERGE', open_questions=['Synthetic unresolved fact'])
        raw = json.dumps(verdict)
        carrier = {'c': 'native-final', 'a': 'claude-json',
                   'g': 'gemini-json', 'y': 'agy-stream-json'}[request.entry['name']]
        if carrier == 'claude-json':
            raw = '{"subtype":"success","structured_output":' + raw + '}'
        elif carrier == 'gemini-json':
            raw = json.dumps({'response': raw})
        elif carrier == 'agy-stream-json':
            raw = '{"event":"result","result":{"status":"SUCCESS","structured_output":' + raw + '}}'
        result = lib.ProviderOutput(carrier, raw.encode(), 0, True)
        if not swap:
            assert lib.admit_output(result, expected=request.expected) == verdict
        return result

    async def scenario():
        cases = {}
        async def preflight(request):
            return None
        async def integrity():
            return True
        for name in ('unanimous', 'informational-dissent', 'google-sibling-swap',
                     'invoke-failure', 'integrity-false', 'integrity-exception'):
            async def invoke(request):
                if name == 'invoke-failure' and request.entry['name'] == 'g':
                    raise RuntimeError('synthetic failure')
                return output(request, dissent=name == 'informational-dissent' and request.entry['name'] == 'y',
                              swap=name == 'google-sibling-swap')
            async def check():
                if name == 'integrity-exception':
                    raise RuntimeError('synthetic integrity failure')
                return name != 'integrity-false'
            run = await lib.run_review(requests, invoke, preflight=preflight,
                                       integrity_check=check, max_concurrency=2)
            assert run.agreement.agreed is (name == 'unanimous'), name
            assert len(run.outcomes) == 4
            if name == 'informational-dissent':
                assert run.agreement.reasons == {'y': 'negative_verdict'}
            if name == 'google-sibling-swap':
                assert run.agreement.reasons == {'g': 'binding_mismatch', 'y': 'binding_mismatch'}
            if name == 'invoke-failure':
                assert [o.status for o in run.outcomes] == ['completed', 'completed', 'failed', 'completed']
                assert len(run.agreement.verdicts) == 3
            if name.startswith('integrity-'):
                assert len(run.agreement.verdicts) == 4 and not run.agreement.integrity_ok
            cases[name] = run.agreement.agreed
        async def refused(request):
            return True
        async def forbidden(request):
            raise AssertionError('Invoked after refused preflight')
        try:
            await lib.run_review(requests, forbidden, preflight=refused,
                                 integrity_check=integrity, max_concurrency=2)
        except lib.DispatchError:
            cases['preflight-refused'] = True
        else:
            raise AssertionError('Malformed preflight accepted')
        active = peak = 0
        reached, release = asyncio.Event(), asyncio.Event()
        async def bounded(request):
            nonlocal active, peak
            active += 1
            peak = max(active, peak)
            if active == 2:
                reached.set()
            await release.wait()
            active -= 1
            return output(request)
        task = asyncio.create_task(lib.run_review(requests, bounded, preflight=preflight,
                                   integrity_check=integrity, max_concurrency=2))
        await reached.wait()
        assert peak == 2
        release.set()
        run = await task
        assert peak == 2 and run.agreement.agreed
        assert [o.name for o in run.outcomes] == ['c', 'a', 'g', 'y']
        cases['bounded-callbacks'] = True
        investigations = [lib.InvestigationRequest(r.entry, 'Perspective ' + r.entry['name'], True)
                          for r in requests]
        async def investigate(request):
            assert request.prompt.startswith('Perspective ' + request.entry['name'])
            if request.entry['vendor'] == 'google':
                assert 'WEB EVIDENCE PROCEDURE' in request.prompt
            else:
                assert 'WEB EVIDENCE PROCEDURE' not in request.prompt
            return {'ordinary_data': request.entry['name']}
        outcomes = await lib.run_investigations(investigations, investigate,
                                               preflight=preflight, max_concurrency=2)
        assert [o.value for o in outcomes] == [{'ordinary_data': name} for name in ('c', 'a', 'g', 'y')]
        assert run.agreement.agreed
        cases['independent-investigations'] = True
        return cases, len(outcomes)

    async def watchdog():
        async with asyncio.timeout(15):
            return await scenario()
    cases, count = asyncio.run(watchdog())
    return dict(capture_method='synthetic', cases=cases, prompt_profiles=profiles,
                investigation_count=count)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheel', type=Path, required=True)
    parser.add_argument('--expected-version', required=True)
    parser.add_argument('--installed-prefix', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        wheel = args.wheel.resolve()
    except RuntimeError:  # Python 3.12 reports symlink loops during resolution.
        parser.error('wheel must be an existing regular file')
    if not wheel.is_file():
        parser.error('wheel must be an existing regular file')
    if args.installed_prefix is None:
        with helpers()['installed_wheel'](wheel) as (python, prefix, neutral):
            return subprocess.run([str(python), '-I', str(Path(__file__).resolve()),
                '--wheel', str(wheel), '--expected-version', args.expected_version,
                '--installed-prefix', str(prefix)], cwd=neutral).returncode
    report = identity(args.installed_prefix, args.expected_version)
    report.update(synthetic_smoke())
    report['wheel_sha256'] = hashlib.sha256(wheel.read_bytes()).hexdigest()
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

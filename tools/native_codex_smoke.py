"""Repository-only cooperative parent-supervised Codex file exchange driver."""
import argparse
import asyncio
from dataclasses import fields, is_dataclass
import errno
import hashlib
import json
import math
import os
from pathlib import Path
import re
import runpy
import stat
import subprocess
import tempfile
import time


CAPTURE = 'parent-tool-final-string'
SAFE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_-]{0,127}\Z', re.ASCII)
HOST = dict(supervisor='codex-parent', native_tool='collaboration.spawn_agent',
            capture_method=CAPTURE, cleanup='interrupt-and-await-terminal',
            effective_settings='UNEXPOSED')


def helper(name):
    return runpy.run_path(str(Path(__file__).with_name(name + '.py')))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def regular(path):
    path = Path(path)
    try:
        if (not path.is_absolute() or stat.S_ISLNK(path.lstat().st_mode)
                or path.resolve(strict=True) != path or not path.is_file()):
            raise ValueError('Expected canonical absolute regular file')
    except RuntimeError:  # Python 3.12 resolve() reports ancestor symlink loops this way.
        raise ValueError('Expected canonical absolute regular file') from None
    except OSError as error:
        if error.errno != errno.ELOOP:
            raise
        raise ValueError('Expected canonical absolute regular file') from None
    return path.read_bytes()


def strict(raw):
    import triad_dispatch_lib as lib
    try:
        return lib.parse_json(raw)
    except lib.AdmissionError as error:
        raise ValueError('Invalid original JSON: ' + error.code) from None


def exact(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError('Unexpected object fields')


def safe(value):
    if not isinstance(value, str) or not SAFE.fullmatch(value):
        raise ValueError('Unsafe identifier')


def atomic(path, value):
    """Readiness is published last, by atomic rename in its own directory."""
    raw = json.dumps(value, sort_keys=True, indent=2, allow_nan=False).encode() + b'\n'
    temporary = path.with_name(path.name + '.tmp')
    try:
        path.lstat()
    except FileNotFoundError:
        pass
    else:
        raise ValueError('Refusing artifact reuse')
    with temporary.open('xb') as stream:
        stream.write(raw)
    os.replace(temporary, path)
    return raw


def serial(value):
    if isinstance(value, bytes):
        return dict(sha256=sha(value), length=len(value))
    if is_dataclass(value):
        return {field.name: serial(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, dict):
        return {key: serial(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(item) for item in value]
    return value


def prepare(config):
    import triad_dispatch_lib as lib
    codex = helper('codex_smoke')
    exact(config, ('mode', 'run_id', 'max_concurrency', 'host', 'requests'))
    safe(config['run_id'])
    if config['mode'] not in ('review', 'investigation'):
        raise ValueError('Invalid mode')
    if type(config['max_concurrency']) is not int or config['max_concurrency'] < 1:
        raise ValueError('Invalid concurrency')
    host = config['host']
    exact(host, (*HOST, 'supported_settings'))
    if any(host[key] != value for key, value in HOST.items()):
        raise ValueError('Unsupported parent protocol')
    settings = host['supported_settings']
    if not isinstance(settings, list) or not settings:
        raise ValueError('Missing declared capabilities')
    for setting in settings:
        exact(setting, ('model', 'reasoning'))
        if any(not isinstance(v, str) or not v.strip() for v in setting.values()):
            raise ValueError('Invalid capability')
    items = config['requests']
    if not isinstance(items, list) or not items:
        raise ValueError('Empty requests')
    prepared, common = [], None
    for item in items:
        exact(item, ('entry', 'context', 'perspective') if config['mode'] == 'investigation'
              else ('entry', 'context'))
        entry = item['entry']
        if not isinstance(entry, dict):
            raise ValueError('Invalid entry')
        safe(entry.get('name'))
        timeout = entry.get('timeout_s')
        if (entry.get('vendor') != 'codex' or entry.get('enabled') is not True
                or type(timeout) not in (int, float) or not 0 < timeout <= 3600
                or not math.isfinite(timeout)):
            raise ValueError('Invalid Codex entry or bounded timeout')
        requested = entry.get('codex')
        exact(requested, ('model', 'reasoning'))
        if requested not in settings:
            raise ValueError('Requested settings unavailable')
        context = item['context']
        packet = codex['prepare_context'](context)
        if context['expected']['leg_name'] != entry['name']:
            raise ValueError('Entry binding mismatch')
        # Render even investigation context to exercise the same scope validation.
        review_prompt = codex['render_prompt'](context)
        if config['mode'] == 'review':
            scope = dict(context)
            scope['expected'] = {k:v for k,v in context['expected'].items() if k != 'leg_name'}
            if common is not None and common != scope:
                raise ValueError('Formal reviewers must share full basis and scope')
            common = scope
            prompt = review_prompt
        else:
            perspective = item['perspective']
            if not isinstance(perspective, str) or not perspective.strip():
                raise ValueError('Empty investigation perspective')
            prompt = lib.render_investigation_prompt(
                'Investigate the bound evidence. Return ordinary text, not an approval ballot.\n'
                + 'Perspective:\n' + lib.render_data(perspective)
                + '\nBound packet and scope:\n' + json.dumps(context, sort_keys=True), family='codex')
        prepared.append(dict(entry=entry, context=context, packet_hashes=packet['packet_hashes'],
                             prompt=prompt.encode(), requested_settings=requested))
    try:
        lib.resolve_roster(dict(schema='triad-review-legs.v2', legs=[p['entry'] for p in prepared]))
    except lib.RosterError as error:
        raise ValueError('Invalid roster: ' + error.code) from None
    return prepared


async def run(config_path, wheel_path, run_dir, *, runtime_identity=None, capture_label=CAPTURE):
    """Run real library callbacks; a separate async parent services request files."""
    import triad_dispatch_lib as lib
    config_path, wheel_path, run_dir = map(Path, (config_path, wheel_path, run_dir))
    config_raw, wheel_raw = regular(config_path), regular(wheel_path)
    config = strict(config_raw)
    prepared = prepare(config)  # No directory/publication before complete validation.
    prepare_context = helper('codex_smoke')['prepare_context']
    try:
        if (not run_dir.is_absolute() or not run_dir.parent.is_dir()
                or run_dir.parent.resolve(strict=True) != run_dir.parent):
            raise ValueError('Run parent must be canonical')
    except RuntimeError:
        raise ValueError('Run parent must be canonical') from None
    if run_dir.exists() or run_dir.is_symlink():
        raise ValueError('Run directory already exists')
    run_dir.mkdir()
    snapshots = {config_path:sha(config_raw), wheel_path:sha(wheel_raw)}
    observations, agents, trace = {}, {}, []
    active = peak = 0
    bound = {}
    acknowledged, cancel_requested = set(), set()
    for item in prepared:
        name = item['entry']['name']
        folder = run_dir / name
        folder.mkdir()
        prompt_path = folder / 'prompt.txt'
        with prompt_path.open('xb') as stream:
            stream.write(item['prompt'])
        snapshots[prompt_path] = sha(item['prompt'])
        for record in item['packet_hashes']:
            snapshots[Path(item['context']['worktree']) / record['path']] = record['sha256']
        bound[name] = item
    manifest = dict(mode=config['mode'], run_id=config['run_id'], config_path=str(config_path),
                    config_sha256=sha(config_raw), wheel_path=str(wheel_path), wheel_sha256=sha(wheel_raw),
                    runtime=runtime_identity or {}, entries=[dict(name=p['entry']['name'],
                    expected=p['context']['expected'], packet_hashes=p['packet_hashes'],
                    prompt_sha256=sha(p['prompt']), requested_settings=p['requested_settings']) for p in prepared])
    snapshots[run_dir/'manifest.json'] = sha(atomic(run_dir/'manifest.json', manifest))

    def event(kind, name):
        trace.append(dict(sequence=len(trace), event=kind, leg_name=name,
                          monotonic_s=time.monotonic(), active=active))

    def consume(name, request_raw, *, cleanup=False):
        item = bound[name]
        folder = run_dir/name
        path = folder/'receipt.json'
        raw = regular(path)
        observation = observations.setdefault(name, {})
        observation.update(receipt_sha256=sha(raw), receipt_length=len(raw),
                           cleanup_only=cleanup)
        snapshots[path] = sha(raw)
        receipt = strict(raw)
        exact(receipt, ('run_id','leg_name','request_sha256','prompt_sha256','response_sha256',
                        'agent_id','status','capture_method','requested_settings','effective_settings',
                        'parent_spawned_at','parent_terminal_at'))
        expected = dict(run_id=config['run_id'], leg_name=name, request_sha256=sha(request_raw),
                        prompt_sha256=sha(item['prompt']), capture_method=CAPTURE,
                        requested_settings=item['requested_settings'], effective_settings='UNEXPOSED')
        if any(receipt[k] != v for k,v in expected.items()):
            raise ValueError('Receipt binding mismatch')
        if receipt['status'] not in ('completed','failed','cancelled'):
            raise ValueError('Nonterminal receipt')
        if not isinstance(receipt['agent_id'], str) or not receipt['agent_id'].strip():
            raise ValueError('Missing supervisor-visible identity')
        for key in ('parent_spawned_at','parent_terminal_at'):
            try:
                if type(receipt[key]) not in (int,float) or not math.isfinite(receipt[key]):
                    raise ValueError('Invalid observation timestamp')
            except OverflowError:
                raise ValueError('Invalid observation timestamp') from None
        if receipt['parent_terminal_at'] < receipt['parent_spawned_at']:
            raise ValueError('Reversed observation timestamps')
        if not isinstance(receipt['response_sha256'], str) or not re.fullmatch('[0-9a-f]{64}', receipt['response_sha256']):
            raise ValueError('Invalid response hash')
        duplicate = receipt['agent_id'] in agents and agents[receipt['agent_id']] != name
        # First ownership and detected custody violations survive cleanup retries.
        agents.setdefault(receipt['agent_id'], name)
        observation.update(receipt=receipt,
                           duplicate_agent=duplicate or observation.get('duplicate_agent', False))
        if duplicate:
            raise ValueError('Reused agent identity')
        acknowledged.add(name)  # Response admission cannot undo observed child termination.
        response = None
        if receipt['status'] == 'completed':
            response = regular(folder/'response.txt')
            observations[name]['response_sha256'] = sha(response)
            observations[name]['response_length'] = len(response)
            snapshots[folder/'response.txt'] = sha(response)
            response.decode('utf-8', errors='strict')
            if sha(response) != receipt['response_sha256']:
                raise ValueError('Response hash mismatch')
        return receipt, response

    def request_cancel(name, raw):
        if name in cancel_requested:
            return
        cancel_requested.add(name)
        try:
            atomic(run_dir/name/'cancel-request.json', dict(run_id=config['run_id'], leg_name=name,
                   request_sha256=sha(raw), prompt_sha256=sha(bound[name]['prompt'])))
        except (ValueError, OSError) as error:
            try:
                observation = observations.setdefault(name, {})
                observation['cancel_publication_error'] = type(error).__name__
                observation['cancel_publication_error'] = str(error)
            except Exception:
                pass  # A diagnostic failure must not replace cancellation.

    async def terminal(name, raw, *, cleanup=False):
        first_error = None
        while True:
            try:
                try:
                    (run_dir/name/'receipt.json').lstat()
                except FileNotFoundError:
                    ready = False
                else:
                    ready = True
                if ready:
                    result = consume(name, raw, cleanup=cleanup)
            except (ValueError, OSError) as error:
                observation = observations.setdefault(name, {})
                observation['validation_error'] = str(error)
                if name in acknowledged:
                    if cleanup:
                        return observation['receipt'], None
                    raise
                observation.setdefault('first_refusal', dict(
                    validation_error=str(error), receipt_sha256=observation.get('receipt_sha256'),
                    receipt_length=observation.get('receipt_length')))
                if first_error is None:
                    first_error = error
                request_cancel(name, raw)
                # Stay inside invoke's cancellation boundary until a matching ack.
            else:
                if ready:
                    if first_error is not None and not cleanup:
                        raise first_error  # A replacement acknowledges cleanup, never success.
                    return result
            await asyncio.sleep(.01)

    async def preflight(request):
        # Library performs every preflight before invoke; recheck prepared evidence.
        item = bound[request.entry['name']]
        prepare_context(item['context'])
        if regular(run_dir/request.entry['name']/'prompt.txt') != item['prompt']:
            raise ValueError('Prompt changed before invoke')

    async def invoke(request):
        nonlocal active, peak
        name = request.entry['name']
        item = bound[name]
        active += 1
        peak = max(peak, active)
        event('start', name)
        raw = None
        try:
            receipt_path = run_dir/name/'receipt.json'
            try:
                receipt_path.lstat()
            except FileNotFoundError:
                pass
            else:
                raise ValueError('Refusing preexisting receipt')
            value = dict(run_id=config['run_id'], leg_name=name, mode=config['mode'],
                         entry=item['entry'], expected=item['context']['expected'],
                         requested_settings=item['requested_settings'],
                         prompt_path=str(run_dir/name/'prompt.txt'), prompt_sha256=sha(item['prompt']),
                         capture_method=CAPTURE, effective_settings='UNEXPOSED')
            raw = atomic(run_dir/name/'request.json', value)
            snapshots[run_dir/name/'request.json'] = sha(raw)
            receipt, response = await terminal(name, raw)
            if receipt['status'] != 'completed':
                raise ValueError('Parent observed unsuccessful terminal')
            return (lib.ProviderOutput('native-final', response, None, True)
                    if config['mode'] == 'review' else response)
        except asyncio.CancelledError:
            if raw is not None:
                try:
                    request_cancel(name, raw)
                finally:
                    # Published native work remains owned even if cancellation publication fails.
                    await terminal(name, raw, cleanup=True)
            raise
        finally:
            active -= 1
            event('finish', name)

    async def integrity():
        try:
            return (all(sha(regular(path)) == hashed for path,hashed in snapshots.items())
                    and not any(o.get('duplicate_agent', False) for o in observations.values()))
        except (ValueError, OSError):
            return False

    if config['mode'] == 'review':
        requests = [lib.ReviewRequest(p['entry'], p['context']['expected'], p['prompt'].decode()) for p in prepared]
        result = await lib.run_review(requests, invoke, preflight=preflight, integrity_check=integrity,
                                      max_concurrency=config['max_concurrency'])
        report = dict(outcomes=serial(result.outcomes), agreement=serial(result.agreement))
    else:
        requests = [lib.InvestigationRequest(p['entry'], p['prompt'].decode()) for p in prepared]
        outcomes = await lib.run_investigations(requests, invoke, preflight=preflight,
                                               max_concurrency=config['max_concurrency'])
        report = dict(outcomes=serial(outcomes), integrity_ok=await integrity())
    report.update(runtime=runtime_identity or {}, wheel_sha256=sha(wheel_raw), mode=config['mode'],
                  run_id=config['run_id'], capture_label=capture_label, capture_method=CAPTURE,
                  trace=trace, peak_active=peak, observations=observations)
    atomic(run_dir/'report.json', report)
    return report


def self_test(wheel, runtime):
    """Synthetic supervisor over the same published callback file protocol."""
    with tempfile.TemporaryDirectory(prefix='triad-native-synthetic-') as temporary:
        root = Path(temporary).resolve()
        packet = root/'brief.md'
        packet.write_text('Synthetic arithmetic review evidence.\n')
        codex = helper('codex_smoke')
        digest = codex['packet_digest'](codex['packet_records'](root,[packet]))
        host = HOST | dict(supported_settings=[dict(model='synthetic',reasoning='high')])
        async def scenario(mode):
            names = ['first','second','third'] if mode == 'review' else ['ordinary']
            items = []
            for name in names:
                expected = dict(review_id='synthetic-round', family='codex', content_digest=digest,
                                leg_name=name, attempt=1, route=None)
                context = dict(expected=expected, worktree=str(root), brief_file=str(packet),
                               packet_files=[str(packet)], review_date='2026-10-12', objective='Synthetic review',
                               criteria=['correctness'], approved_boundary=['brief.md'])
                item = dict(entry=dict(name=name,vendor='codex',enabled=True,acceptance='required',
                            timeout_s=10,codex=dict(model='synthetic',reasoning='high')),context=context)
                if mode == 'investigation': item['perspective'] = 'Boundary cases'
                items.append(item)
            config_path = root/(mode+'.json')
            atomic(config_path, dict(mode=mode,run_id='synthetic-'+mode,max_concurrency=2,host=host,requests=items))
            directory = root/mode
            task = asyncio.create_task(run(config_path,wheel,directory,runtime_identity=runtime,capture_label='synthetic'))
            for name in names:
                path = directory/name/'request.json'
                while not path.exists():
                    if task.done(): return await task
                    await asyncio.sleep(.002)
                request_raw = regular(path)
                request = strict(request_raw)
                if mode == 'review':
                    raw = json.dumps(dict(schema_version=2,**request['expected'],
                        verdict='DO NOT MERGE' if name == 'third' else 'SAFE TO MERGE',
                        criteria_checked=['correctness'],findings=[],affected_surfaces_inspected=['brief.md'],
                        open_questions=['Synthetic dissent'] if name == 'third' else [])).encode()
                else: raw = b'Ordinary synthetic investigation evidence.\n'
                (directory/name/'response.txt').write_bytes(raw)
                atomic(directory/name/'receipt.json', dict(run_id=request['run_id'],leg_name=name,
                    request_sha256=sha(request_raw),prompt_sha256=request['prompt_sha256'],response_sha256=sha(raw),
                    agent_id='synthetic-'+name,status='completed',capture_method=CAPTURE,
                    requested_settings=request['requested_settings'],effective_settings='UNEXPOSED',
                    parent_spawned_at=100.0,parent_terminal_at=101.0))
            report = await task
            if mode == 'review':
                assert report['peak_active'] == 2
                assert report['agreement']['integrity_ok'] is True
                assert report['agreement']['agreed'] is False
                assert report['agreement']['verdicts']['third']['verdict'] == 'DO NOT MERGE'
            else:
                assert 'agreement' not in report and report['integrity_ok'] is True
                assert report['outcomes'][0]['value']['sha256'] == sha(raw)
            return report
        return dict(capture_label='synthetic', review=asyncio.run(scenario('review')),
                    investigation=asyncio.run(scenario('investigation')))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheel',type=Path,required=True)
    parser.add_argument('--expected-version',required=True)
    parser.add_argument('--config',type=Path)
    parser.add_argument('--run-dir',type=Path)
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--installed-prefix',type=Path,help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        wheel = args.wheel.absolute()
        regular(wheel)
        if args.self_test:
            if args.config or args.run_dir: raise ValueError('Self-test is alternative to config/run-dir')
        else:
            if not args.config or not args.run_dir: raise ValueError('Config and new run directory required')
            args.config, args.run_dir = args.config.absolute(), args.run_dir.absolute()
            regular(args.config)
            if args.run_dir.exists() or args.run_dir.is_symlink(): raise ValueError('Run directory exists')
        if not args.installed_prefix:
            with helper('verify_wheel')['installed_wheel'](wheel) as (python,prefix,neutral):
                forwarded = ['--wheel',str(wheel),'--expected-version',args.expected_version,
                             '--installed-prefix',str(prefix)]
                forwarded += ['--self-test'] if args.self_test else ['--config',str(args.config),'--run-dir',str(args.run_dir)]
                return subprocess.run([str(python),'-I',str(Path(__file__).resolve()),*forwarded],cwd=neutral).returncode
        runtime = helper('four_route_smoke')['identity'](args.installed_prefix,args.expected_version)
        report = (self_test(wheel,runtime) if args.self_test else
                  asyncio.run(run(args.config,wheel,args.run_dir,runtime_identity=runtime)))
        print(json.dumps(report,sort_keys=True))
        return 0
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    raise SystemExit(main())

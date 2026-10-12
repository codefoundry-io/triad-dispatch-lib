"""Exercise actual supervised file exchange; no provider/native execution."""
import asyncio
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


@pytest.fixture
def driver():
    path = Path(__file__).resolve().parents[1] / 'tools/native_codex_smoke.py'
    assert path.is_file(), 'supervised native callback driver is absent'
    spec = importlib.util.spec_from_file_location('native_driver', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


@pytest.fixture
def setup_run(tmp_path):
    packet = tmp_path / 'packet'
    packet.mkdir()
    brief = packet / 'brief.md'
    brief.write_text('Review integer arithmetic.\n')
    records = [{'path': 'brief.md', 'sha256': digest(brief.read_bytes())}]
    content = digest(json.dumps(records, sort_keys=True, separators=(',', ':')).encode())
    requests = []
    for name in ('first', 'second', 'third'):
        entry = dict(name=name, vendor='codex', enabled=True, acceptance='required',
                     timeout_s=2, codex=dict(model='test-model', reasoning='high'))
        expected = dict(review_id='round-1', family='codex', content_digest=content,
                        leg_name=name, attempt=1, route=None)
        context = dict(expected=expected, worktree=str(packet), brief_file=str(brief),
                       packet_files=[str(brief)], review_date='2026-10-12',
                       objective='Review arithmetic', criteria=['correctness'],
                       approved_boundary=['brief.md'])
        requests.append(dict(entry=entry, context=context))
    host = dict(supervisor='codex-parent', native_tool='collaboration.spawn_agent',
                supported_settings=[dict(model='test-model', reasoning='high')],
                capture_method='parent-tool-final-string', cleanup='interrupt-and-await-terminal',
                effective_settings='UNEXPOSED')
    config = tmp_path / 'config.json'
    config.write_text(json.dumps(dict(mode='review', run_id='run-1', max_concurrency=2,
                                     host=host, requests=requests)))
    wheel = tmp_path / 'test.whl'
    wheel.write_bytes(b'wheel identity fixture')
    return config, wheel, tmp_path / 'run'


def receipt_for(request, raw, *, agent=None, status='completed'):
    return dict(run_id=request['run_id'], leg_name=request['leg_name'],
                request_sha256=request['_hash'], prompt_sha256=request['prompt_sha256'],
                response_sha256=digest(raw), agent_id=agent or 'agent-' + request['leg_name'],
                status=status, capture_method='parent-tool-final-string',
                requested_settings=request['requested_settings'], effective_settings='UNEXPOSED',
                parent_spawned_at=100.0, parent_terminal_at=101.0)


async def wait_request(run, name):
    path = run / name / 'request.json'
    async with asyncio.timeout(3):
        while not path.exists():
            await asyncio.sleep(.002)
    raw = path.read_bytes()
    value = json.loads(raw)
    value['_hash'] = digest(raw)
    return value


def verdict(request, *, dissent=False):
    return json.dumps(dict(schema_version=2, **request['expected'],
                          verdict='DO NOT MERGE' if dissent else 'SAFE TO MERGE',
                          criteria_checked=['correctness'], findings=[],
                          affected_surfaces_inspected=['brief.md'],
                          open_questions=['Synthetic unresolved fact'] if dissent else [])).encode()


def post(run, request, raw, receipt=None):
    folder = run / request['leg_name']
    (folder / 'response.txt').write_bytes(raw)
    temporary = folder / 'receipt.tmp'
    temporary.write_text(json.dumps(receipt or receipt_for(request, raw)))
    temporary.rename(folder / 'receipt.json')


async def exchange(driver, setup_run, edit=None, mutate=None):
    config, wheel, run = setup_run
    task = asyncio.create_task(driver.run(config, wheel, run))
    for name in ('first', 'second', 'third'):
        request = await wait_request(run, name)
        raw = verdict(request, dissent=name == 'third')
        receipt = receipt_for(request, raw)
        if edit:
            edit(receipt, request)
        post(run, request, raw, receipt)
    if mutate:
        mutate(config, wheel, run)
    return await task


def test_review_dissent_order_and_two_slots(driver, setup_run):
    async def scenario():
        config, wheel, run = setup_run
        task = asyncio.create_task(driver.run(config, wheel, run))
        first, second = await asyncio.gather(wait_request(run, 'first'), wait_request(run, 'second'))
        assert not (run / 'third/request.json').exists()
        post(run, second, verdict(second))
        third = await wait_request(run, 'third')
        post(run, third, verdict(third, dissent=True))
        post(run, first, verdict(first))
        report = await task
        assert report['peak_active'] == 2
        assert [o['name'] for o in report['outcomes']] == ['first', 'second', 'third']
        assert report['agreement']['agreed'] is False
        assert report['agreement']['verdicts']['third']['verdict'] == 'DO NOT MERGE'
        assert report['agreement']['integrity_ok'] is True
        assert all(o['value']['exit_code'] is None for o in report['outcomes'])
        assert report == json.loads((run / 'report.json').read_text())
    asyncio.run(scenario())


@pytest.mark.parametrize('field,value', [('run_id','old'), ('prompt_sha256','0'*64),
    ('request_sha256','0'*64), ('response_sha256','0'*64), ('status','failed'),
    ('effective_settings','high'), ('parent_terminal_at',True),
    ('requested_settings',dict(model='wrong',reasoning='high'))])
def test_receipt_refusals(driver, setup_run, field, value):
    report = asyncio.run(exchange(driver, setup_run, lambda r,q: r.update({field:value})))
    assert all(o['status'] == 'failed' for o in report['outcomes'])
    assert not report['agreement']['agreed']


def test_duplicate_agent_is_refused(driver, setup_run):
    report = asyncio.run(exchange(driver, setup_run, lambda r,q: r.update(agent_id='same')))
    assert not report['agreement']['integrity_ok']
    assert not report['agreement']['agreed']


@pytest.mark.parametrize('target', ['config', 'wheel', 'packet', 'prompt', 'request', 'response', 'receipt'])
def test_fresh_integrity_detects_mutation(driver, setup_run, target):
    def mutate(config, wheel, run):
        path = {'config':config, 'wheel':wheel, 'packet':config.parent/'packet/brief.md',
                **{name:run/'first'/filename for name,filename in
                   [('prompt','prompt.txt'),('request','request.json'),('response','response.txt'),('receipt','receipt.json')]}}[target]
        path.write_bytes(path.read_bytes() + b' ')
    report = asyncio.run(exchange(driver, setup_run, mutate=mutate))
    assert not report['agreement']['integrity_ok']
    assert len(report['outcomes']) == 3


@pytest.mark.parametrize('bad', ['name','setting','scope','symlink','duplicate-json','timeout','concurrency'])
def test_all_preflight_before_publish(driver, setup_run, bad):
    config, wheel, run = setup_run
    value = json.loads(config.read_text())
    last = value['requests'][-1]
    if bad == 'name': last['entry']['name'] = '../escape'
    if bad == 'setting': last['entry']['codex']['model'] = 'unsupported'
    if bad == 'scope': last['context']['objective'] = 'Different scope'
    if bad == 'timeout': last['entry']['timeout_s'] = 999999
    if bad == 'concurrency': value['max_concurrency'] = True
    if bad == 'symlink':
        path = config.parent/'link.md'
        path.symlink_to(config.parent/'packet/brief.md')
        last['context']['packet_files'] = [str(path)]
    config.write_text(json.dumps(value))
    if bad == 'duplicate-json': config.write_text(config.read_text().replace('"run_id": "run-1"', '"run_id": "run-1", "run_id": "run-1"'))
    with pytest.raises(ValueError): asyncio.run(driver.run(config, wheel, run))
    assert not list(run.glob('*/request.json'))


def test_duplicate_receipt_members_and_altered_response(driver, setup_run):
    async def scenario():
        config,wheel,run = setup_run
        value = json.loads(config.read_text()); value['requests'] = value['requests'][:1]
        config.write_text(json.dumps(value))
        task = asyncio.create_task(driver.run(config,wheel,run))
        request = await wait_request(run,'first')
        raw = verdict(request)
        post(run,request,raw)
        path = run/'first/receipt.json'
        path.write_text(path.read_text().replace('"status": "completed"','"status": "completed", "status": "completed"'))
        report = await task
        assert report['outcomes'][0]['status'] == 'failed'
    asyncio.run(scenario())


def test_timeout_waits_for_parent_and_late_completion_is_cleanup_only(driver, setup_run):
    async def scenario():
        config,wheel,run = setup_run
        value = json.loads(config.read_text()); value['requests'] = value['requests'][:1]
        value['requests'][0]['entry']['timeout_s'] = 1
        config.write_text(json.dumps(value))
        task = asyncio.create_task(driver.run(config,wheel,run))
        request = await wait_request(run,'first')
        async with asyncio.timeout(2):
            while not (run/'first/cancel-request.json').exists(): await asyncio.sleep(.002)
        await asyncio.sleep(.03)
        assert not task.done()
        post(run,request,verdict(request))
        report = await task
        assert report['outcomes'][0]['status'] == 'timed_out'
        assert not report['agreement']['agreed']
        assert report['observations']['first']['cleanup_only'] is True
    asyncio.run(scenario())


def test_investigation_preserves_plain_bytes_without_agreement(driver, setup_run):
    async def scenario():
        config,wheel,run = setup_run
        value = json.loads(config.read_text()); value['mode'] = 'investigation'
        value['requests'] = value['requests'][:1]; value['requests'][0]['perspective'] = 'Boundary cases'
        config.write_text(json.dumps(value))
        task = asyncio.create_task(driver.run(config,wheel,run))
        request = await wait_request(run,'first')
        raw = b'Ordinary evidence.\n```not a ballot```\n'
        post(run,request,raw)
        report = await task
        assert 'agreement' not in report
        assert report['integrity_ok'] is True
        assert report['outcomes'][0]['value'] == {'sha256':digest(raw),'length':len(raw)}
        assert (run/'first/response.txt').read_bytes() == raw
    asyncio.run(scenario())


def test_existing_run_refused(driver, setup_run):
    config,wheel,run = setup_run
    run.mkdir(); (run/'receipt.json').write_text('preserve')
    with pytest.raises(ValueError): asyncio.run(driver.run(config,wheel,run))
    assert (run/'receipt.json').read_text() == 'preserve'


@pytest.mark.parametrize('kind', ['altered-bytes','fenced-json','cancelled','extra-field'])
def test_original_response_and_terminal_guards(driver, setup_run, kind):
    async def scenario():
        config,wheel,run = setup_run
        value = json.loads(config.read_text()); value['requests'] = value['requests'][:1]
        config.write_text(json.dumps(value))
        task = asyncio.create_task(driver.run(config,wheel,run))
        request = await wait_request(run,'first')
        raw = verdict(request)
        receipt = receipt_for(request,raw)
        if kind == 'altered-bytes': raw += b' changed'
        if kind == 'fenced-json':
            raw = b'```json\n'+raw+b'\n```'; receipt = receipt_for(request,raw)
        if kind == 'cancelled': receipt['status'] = 'cancelled'
        if kind == 'extra-field': receipt['extra'] = True
        post(run,request,raw,receipt)
        report = await task
        assert not report['agreement']['agreed']
        if kind != 'fenced-json': assert report['outcomes'][0]['status'] == 'failed'
        else: assert report['agreement']['reasons']['first'] == 'invalid_json'
    asyncio.run(scenario())


def test_preexisting_receipt_for_queued_leg_never_publishes_request(driver, setup_run):
    async def scenario():
        config,wheel,run = setup_run
        task = asyncio.create_task(driver.run(config,wheel,run))
        first,second = await asyncio.gather(wait_request(run,'first'),wait_request(run,'second'))
        (run/'third/receipt.json').write_text('{}')
        post(run,first,verdict(first)); post(run,second,verdict(second))
        report = await task
        assert not (run/'third/request.json').exists()
        assert report['outcomes'][2]['status'] == 'failed'
    asyncio.run(scenario())


def test_failed_receipt_retains_original_evidence_hash(driver, setup_run):
    report = asyncio.run(exchange(driver, setup_run, lambda r,q: r.update(run_id='stale')))
    observation = report['observations']['first']
    assert observation['receipt_sha256'] == digest((setup_run[2]/'first/receipt.json').read_bytes())
    assert observation['validation_error'] == 'Receipt binding mismatch'

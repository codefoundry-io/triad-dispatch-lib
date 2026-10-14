"""Exercise actual supervised file exchange; no provider/native execution."""
import asyncio
import errno
import hashlib
import importlib.util
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import venv

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
        if edit:
            await asyncio.sleep(.04)
            if (run/name/'cancel-request.json').exists():
                post(run, request, raw)
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


@pytest.fixture(scope='module')
def cli_runtime(tmp_path_factory):
    """Copy real package/dependencies into one isolated runtime; no wheel build."""
    import jsonschema
    import triad_dispatch_lib as lib

    root = tmp_path_factory.mktemp('native-cli-runtime').resolve()
    prefix = root/'venv'
    venv.EnvBuilder(with_pip=False, symlinks=True).create(prefix)
    site = prefix/'lib'/('python%d.%d' % sys.version_info[:2])/'site-packages'
    shutil.copytree(Path(lib.__file__).parent, site/'triad_dispatch_lib')
    distribution = importlib.metadata.distribution('triad-dispatch-lib')
    metadata = site/('triad_dispatch_lib-' + distribution.version + '.dist-info')
    metadata.mkdir()
    (metadata/'METADATA').write_text(distribution.read_text('METADATA'))
    (site/'test-dependencies.pth').write_text(str(Path(jsonschema.__file__).parent.parent) + '\n')
    try:
        yield prefix/'bin/python', prefix, distribution.version
    finally:
        shutil.rmtree(root)


@pytest.mark.parametrize('mode,repeated,expected', [
    ('normal', False, 0), ('invalid', False, 2),
    ('wrapper', False, 130), ('wrapper', True, 130),
    ('group', False, 130), ('group', True, 130),
])
def test_outer_cli_retains_child_and_environment_until_terminal_ack(
        driver, setup_run, cli_runtime, mode, repeated, expected):
    config, wheel, run = setup_run
    python, prefix, version = cli_runtime
    root = config.parent
    value = json.loads(config.read_text())
    value['requests'] = value['requests'][:1]
    value['requests'][0]['entry']['timeout_s'] = 30
    if mode == 'invalid':
        value['requests'][0]['context']['criteria'] = []
    config.write_text(json.dumps(value))
    bootstrap = root/'outer.py'
    bootstrap.write_text('''import importlib.util, json, subprocess, sys, tempfile
from contextlib import contextmanager
from pathlib import Path
source, python, prefix, root = map(Path, sys.argv[1:5])
sys.argv = [str(source), *sys.argv[5:]]
spec = importlib.util.spec_from_file_location('native_outer', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
real_popen = subprocess.Popen
children = []
class ObservedPopen(real_popen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        children.append(self)
        (root/'child.pid').write_text(str(self.pid))
subprocess.Popen = ObservedPopen
@contextmanager
def installed(wheel):
    with tempfile.TemporaryDirectory(prefix='install-scope-', dir=root) as temporary:
        (root/'scope.json').write_text(json.dumps({'neutral': temporary}))
        try:
            yield python, prefix, Path(temporary)
        finally:
            (root/'cleanup.json').write_text(json.dumps({'child_returncode': children[-1].poll()}))
original_helper = module.helper
def helper(name):
    return {'installed_wheel': installed} if name == 'verify_wheel' else original_helper(name)
module.helper = helper
raise SystemExit(module.main())
''')
    with (root/'outer.stdout').open('w') as out, (root/'outer.stderr').open('w') as err:
        process = subprocess.Popen([sys.executable, str(bootstrap), str(Path(driver.__file__)),
            str(python), str(prefix), str(root), '--wheel', str(wheel), '--expected-version', version,
            '--config', str(config), '--run-dir', str(run)], stdout=out, stderr=err, start_new_session=True)
        request = None
        try:
            if mode != 'invalid':
                deadline = time.monotonic() + 10
                while not (run/'first/request.json').exists():
                    if process.poll() is not None or time.monotonic() >= deadline:
                        pytest.fail('outer/inner CLI failed before request: ' + (root/'outer.stderr').read_text())
                    time.sleep(.01)
                request = asyncio.run(wait_request(run, 'first'))
                child = int((root/'child.pid').read_text())
                neutral = Path(json.loads((root/'scope.json').read_text())['neutral'])
                if mode in ('wrapper', 'group'):
                    interrupt = (lambda: process.send_signal(signal.SIGINT)) if mode == 'wrapper' else (
                        lambda: os.killpg(process.pid, signal.SIGINT))
                    interrupt()
                    if repeated:
                        time.sleep(.05)
                        if process.poll() is None:
                            interrupt()
                    time.sleep(.8)  # Deliberately beyond subprocess.run's 0.25s SIGINT grace.
                    held_until_ack = process.poll() is None and neutral.is_dir() and prefix.is_dir()
                    child_status = subprocess.run(['ps', '-p', str(child), '-o', 'stat='],
                                                  capture_output=True, text=True)
                    child_live = child_status.returncode == 0 and not child_status.stdout.strip().startswith('Z')
                    cancellation_requested = (run/'first/cancel-request.json').exists()
                post(run, request, verdict(request))
            status = process.wait(timeout=10)
        finally:
            if process.poll() is None:
                if request is not None:
                    post(run, request, verdict(request))
                process.send_signal(signal.SIGINT)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGTERM)
                    process.wait(timeout=5)
            # The inner has its own session; failing-test cleanup must drain it too.
            if (root/'child.pid').exists():
                owned_child = int((root/'child.pid').read_text())

                def child_alive():
                    result = subprocess.run(['ps', '-p', str(owned_child), '-o', 'stat='],
                                            capture_output=True, text=True)
                    return result.returncode == 0 and not result.stdout.strip().startswith('Z')

                if child_alive():
                    try:
                        os.kill(owned_child, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                    deadline = time.monotonic() + 5
                    while child_alive() and time.monotonic() < deadline:
                        time.sleep(.01)
                    if child_alive():
                        try:
                            os.kill(owned_child, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        deadline = time.monotonic() + 3
                        while child_alive() and time.monotonic() < deadline:
                            time.sleep(.01)
                    assert not child_alive(), 'owned inner CLI survived failing-test cleanup'
        if mode in ('wrapper', 'group'):
            assert held_until_ack and child_live, 'CLI released child/environment before delayed terminal ack'
            assert cancellation_requested
            assert not (run/'report.json').exists()
        elif mode == 'normal':
            assert json.loads((run/'report.json').read_text())['agreement']['agreed']
        else:
            assert not run.exists()
        assert status == expected
        assert not Path(json.loads((root/'scope.json').read_text())['neutral']).exists()
        assert json.loads((root/'cleanup.json').read_text())['child_returncode'] is not None


def test_driver_refuses_casefold_name_collision_before_artifacts(driver, setup_run):
    import triad_dispatch_lib as lib

    config, wheel, run = setup_run
    value = json.loads(config.read_text())
    value['requests'] = value['requests'][:2]
    for item, name in zip(value['requests'], ('codex', 'Codex')):
        item['entry']['name'] = name
        item['context']['expected']['leg_name'] = name
    roster = lib.resolve_roster(dict(schema='triad-review-legs.v2',
                                    legs=[item['entry'] for item in value['requests']]))
    assert [entry['name'] for entry in lib.select_entries(roster)] == ['codex', 'Codex']
    with pytest.raises(ValueError, match='[Cc]ase'):
        driver.prepare(value)
    assert not run.exists()


@pytest.mark.parametrize('mode,scope', [
    (None, None), ('review', 'wrapper'), ('review', 'group'),
    ('investigation', 'wrapper'), ('investigation', 'group'),
])
def test_self_test_interrupt_drains_synthetic_supervisor_and_cleans_environment(
        driver, setup_run, cli_runtime, mode, scope):
    _, wheel, _ = setup_run
    python, prefix, version = cli_runtime
    root = wheel.parent
    inner = root/'synthetic-inner.py'
    inner.write_text('''import asyncio, importlib.util, json, sys, tempfile
from pathlib import Path
source, root = map(Path, sys.argv[1:3])
target = sys.argv[3]
sys.argv = [str(source), *sys.argv[4:]]
spec = importlib.util.spec_from_file_location('native_inner', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
real_temporary = tempfile.TemporaryDirectory
def temporary(*args, **kwargs):
    if kwargs.get('prefix') == 'triad-native-synthetic-':
        kwargs['dir'] = root
    return real_temporary(*args, **kwargs)
tempfile.TemporaryDirectory = temporary
real_sleep = asyncio.sleep
async def sleep(delay, *args, **kwargs):
    if delay == .002:
        frame = asyncio.current_task().get_coro().cr_frame
        if frame.f_locals.get('mode') == target and not (root/'poll.json').exists():
            directory = frame.f_locals['directory']
            (root/'poll.json').write_text(json.dumps({'directory': str(directory)}))
            while not (root/'release').exists():
                await real_sleep(.01)
    return await real_sleep(delay, *args, **kwargs)
asyncio.sleep = sleep
raise SystemExit(module.main())
''')
    outer = root/'synthetic-outer.py'
    outer.write_text('''import importlib.util, json, subprocess, sys, tempfile
from contextlib import contextmanager
from pathlib import Path
source, inner, python, prefix, root = map(Path, sys.argv[1:6])
target = sys.argv[6]
sys.argv = [str(source), *sys.argv[7:]]
spec = importlib.util.spec_from_file_location('native_outer', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
real_popen = subprocess.Popen
class Observed(real_popen):
    def __init__(self, args, **kwargs):
        args = [args[0], '-I', str(inner), str(source), str(root), target, *args[3:]]
        super().__init__(args, **kwargs)
        (root/'child.pid').write_text(str(self.pid))
subprocess.Popen = Observed
@contextmanager
def installed(wheel):
    with tempfile.TemporaryDirectory(prefix='synthetic-install-', dir=root) as neutral:
        (root/'neutral').write_text(neutral)
        try:
            yield python, prefix, Path(neutral)
        finally:
            (root/'environment-cleaned').touch()
original = module.helper
module.helper = lambda name: {'installed_wheel': installed} if name == 'verify_wheel' else original(name)
raise SystemExit(module.main())
''')
    with (root/'synthetic.stdout').open('w') as out, (root/'synthetic.stderr').open('w') as err:
        process = subprocess.Popen([sys.executable, str(outer), str(Path(driver.__file__)),
            str(inner), str(python), str(prefix), str(root), mode or 'none', '--wheel', str(wheel),
            '--expected-version', version, '--self-test'], stdout=out, stderr=err, start_new_session=True)
        try:
            if mode is not None:
                deadline = time.monotonic()+10
                while not (root/'poll.json').exists():
                    if process.poll() is not None or time.monotonic() >= deadline:
                        pytest.fail('No synthetic poll: ' + (root/'synthetic.stderr').read_text())
                    time.sleep(.01)
                directory = Path(json.loads((root/'poll.json').read_text())['directory'])
                deadline = time.monotonic()+3
                while not list(directory.glob('*/request.json')) and time.monotonic() < deadline:
                    time.sleep(.01)
                assert list(directory.glob('*/request.json'))
                child = int((root/'child.pid').read_text())
                descendants = subprocess.run(['pgrep', '-P', str(child)], capture_output=True, text=True)
                assert not descendants.stdout.strip(), 'Synthetic driver launched a child process'
                interrupt = (lambda: process.send_signal(signal.SIGINT)) if scope == 'wrapper' else (
                    lambda: os.killpg(process.pid, signal.SIGINT))
                interrupt()
                time.sleep(.05)
                if process.poll() is None:
                    interrupt()
                time.sleep(.1)
                held = process.poll() is None and directory.parent.exists()
                (root/'release').touch()
            try:
                status = process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pytest.fail('Synthetic supervisor did not drain after its polling window was released')
            if mode is not None:
                assert held, 'Synthetic supervisor was cancelled before it could deliver receipts'
                assert status == 130
            else:
                assert status == 0, (root/'synthetic.stderr').read_text()
                assert json.loads((root/'synthetic.stdout').read_text())['capture_label'] == 'synthetic'
            assert not list(root.glob('triad-native-synthetic-*'))
            assert (root/'environment-cleaned').exists()
            assert not Path((root/'neutral').read_text()).exists()
            child_status = subprocess.run(['ps', '-p', (root/'child.pid').read_text(), '-o', 'stat='],
                                          capture_output=True, text=True)
            assert child_status.returncode != 0, 'Inner self-test was not reaped'
        finally:
            (root/'release').touch()
            if (root/'child.pid').exists():
                owned_child = int((root/'child.pid').read_text())
                child_status = subprocess.run(['ps', '-p', str(owned_child), '-o', 'stat='],
                                              capture_output=True, text=True)
                if child_status.returncode == 0 and not child_status.stdout.strip().startswith('Z'):
                    try:
                        os.kill(owned_child, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
            if process.poll() is None:
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
            for temporary in root.glob('triad-native-synthetic-*'):
                shutil.rmtree(temporary)


def test_outer_cli_preserves_pending_interrupt_and_forwards_once_on_reentry(
        driver, setup_run, monkeypatch):
    from contextlib import contextmanager

    _, wheel, _ = setup_run
    original_handler = signal.getsignal(signal.SIGINT)
    forwarded = []
    active = []

    @contextmanager
    def installed(_):
        active.append(True)
        try:
            yield Path(sys.executable), wheel.parent, wheel.parent
        finally:
            active.pop()

    class Child:
        def __init__(self, *args, **kwargs):
            # Interrupt while Popen has not yet returned the child binding.
            handler = signal.getsignal(signal.SIGINT)
            handler(signal.SIGINT, None)
            handler(signal.SIGINT, None)

        def send_signal(self, number):
            # A repeat at the forward boundary must neither abort nor duplicate it.
            signal.getsignal(signal.SIGINT)(signal.SIGINT, None)
            forwarded.append(number)

        def wait(self):
            assert active and forwarded == [signal.SIGINT]
            return -signal.SIGINT

    monkeypatch.setattr(driver, 'helper', lambda _: {'installed_wheel': installed})
    monkeypatch.setattr(driver.subprocess, 'Popen', Child)
    monkeypatch.setattr(sys, 'argv', ['native', '--wheel', str(wheel),
                                    '--expected-version', 'test', '--self-test'])
    try:
        try:
            assert driver.main() == 130
        except KeyboardInterrupt:
            pytest.fail('SIGINT escaped before child binding or during forwarding')
        assert forwarded == [signal.SIGINT]
        assert signal.getsignal(signal.SIGINT) is original_handler
        assert not active
    finally:
        signal.signal(signal.SIGINT, original_handler)


@pytest.mark.parametrize('error_number', [None, errno.EIO, errno.EACCES])
@pytest.mark.parametrize('dangling', [False, True])
def test_atomic_refuses_existing_destination_without_overwriting(
        driver, tmp_path, monkeypatch, error_number, dangling):
    destination = tmp_path/'request.json'
    sentinel = b'Existing artifact must remain unchanged.\n'
    if dangling:
        destination.symlink_to('missing-target.json')
    else:
        destination.write_bytes(sentinel)
    original_stat, original_lstat = os.stat, os.lstat
    armed = error_number is not None

    def stat(path, *args, **kwargs):
        if armed and path == destination:
            raise OSError(error_number, 'synthetic destination probe failure', str(path))
        return original_stat(path, *args, **kwargs)

    def lstat(path, *args, **kwargs):
        if armed and path == destination:
            raise OSError(error_number, 'synthetic destination probe failure', str(path))
        return original_lstat(path, *args, **kwargs)

    monkeypatch.setattr(os, 'stat', stat)
    monkeypatch.setattr(os, 'lstat', lstat)
    failure = None
    try:
        driver.atomic(destination, {'new': 'artifact'})
    except (ValueError, OSError) as error:
        failure = error
    finally:
        armed = False
    if dangling:
        assert destination.is_symlink(), 'artifact reuse replaced a dangling destination link'
        assert destination.readlink() == Path('missing-target.json')
    else:
        assert destination.read_bytes() == sentinel, 'artifact reuse overwrote its destination'
    assert not destination.with_name('request.json.tmp').exists()
    if error_number is None:
        assert isinstance(failure, ValueError)
        assert str(failure) == 'Refusing artifact reuse'
    else:
        assert isinstance(failure, OSError)
        assert failure.errno == error_number


def test_atomic_publishes_missing_destination(driver, tmp_path):
    destination = tmp_path/'request.json'
    raw = driver.atomic(destination, {'new': 'artifact'})
    assert destination.read_bytes() == raw
    assert json.loads(raw) == {'new': 'artifact'}
    assert not destination.with_name('request.json.tmp').exists()


def test_preflight_helper_loads_are_bounded_per_run(driver, setup_run, monkeypatch):
    original_helper = driver.helper
    loads = []

    def helper(name):
        value = original_helper(name)
        if name == 'codex_smoke':
            loads.append(value)
        return value

    monkeypatch.setattr(driver, 'helper', helper)

    async def scenario():
        config, wheel, first_run = setup_run
        counts = []
        for run in (first_run, first_run.with_name('second-run')):
            task = asyncio.create_task(driver.run(config, wheel, run))
            for name in ('first', 'second', 'third'):
                request = await wait_request(run, name)
                post(run, request, verdict(request))
            report = await task
            assert report['agreement']['agreed']
            counts.append(len(loads))
        assert counts == [2, 4], 'preflight reloaded the real helper for every request'
    asyncio.run(scenario())


def test_reused_preflight_helper_revalidates_changed_packet(driver, setup_run, monkeypatch):
    from triad_dispatch_lib import DispatchError

    config, wheel, run = setup_run
    brief = config.parent/'packet/brief.md'
    original_prepare = driver.prepare

    def prepare(value):
        prepared = original_prepare(value)
        brief.write_text('Packet changed after preparation.\n')
        return prepared

    monkeypatch.setattr(driver, 'prepare', prepare)
    with pytest.raises(DispatchError) as caught:
        asyncio.run(driver.run(config, wheel, run))
    assert caught.value.code == 'preflight_failed'
    assert not list(run.glob('*/request.json'))
    assert brief.read_text() == 'Packet changed after preparation.\n'


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


@pytest.mark.parametrize('bad,diagnostic', [
    ('huge-timeout', 'Invalid Codex entry or bounded timeout'),
    ('cyclic-run-parent', 'Run parent must be canonical'),
    ('missing-run-parent', 'Run parent must be canonical'),
    ('file-run-parent', 'Run parent must be canonical'),
])
def test_cli_invalid_timeout_and_run_parent_exit_before_publication(
        driver, setup_run, monkeypatch, capsys, bad, diagnostic):
    config, wheel, run = setup_run
    original_run = run
    if bad == 'huge-timeout':
        value = json.loads(config.read_text())
        value['requests'][-1]['entry']['timeout_s'] = 10**400
        config.write_text(json.dumps(value))
    elif bad == 'cyclic-run-parent':
        loop = config.parent/'loop'
        loop.symlink_to('loop')
        run = loop/'run'
    else:
        parent = config.parent/'invalid-parent'
        if bad == 'file-run-parent':
            parent.write_text('This is a file, not a directory.\n')
        run = parent/'run'
    original_helper = driver.helper

    def helper(name):
        if name == 'four_route_smoke':
            # Exercise CLI validation without installing or asserting a fake wheel identity.
            return {'identity': lambda *args: {}}
        return original_helper(name)

    monkeypatch.setattr(driver, 'helper', helper)
    monkeypatch.setattr(sys, 'argv', [
        'native_codex_smoke.py', '--wheel', str(wheel), '--expected-version', 'test',
        '--config', str(config), '--run-dir', str(run), '--installed-prefix', str(config.parent),
    ])
    with pytest.raises(SystemExit) as caught:
        driver.main()
    assert caught.value.code == 2
    captured = capsys.readouterr()
    assert diagnostic in captured.err
    assert 'Traceback' not in captured.err
    assert not captured.out
    assert not run.exists()
    assert not original_run.exists()


@pytest.mark.parametrize('error_number', [None, errno.EIO, errno.EACCES])
def test_run_parent_status_error_preserves_errno_before_artifacts(driver, setup_run, monkeypatch, error_number):
    config, wheel, run = setup_run
    parent = run.parent
    original_stat = os.stat

    def stat(path, *args, **kwargs):
        if error_number and Path(path) == parent and kwargs.get('follow_symlinks', True):
            raise OSError(error_number, 'synthetic following parent status failure', str(parent))
        return original_stat(path, *args, **kwargs)

    monkeypatch.setattr(os, 'stat', stat)
    if error_number is None:
        report = asyncio.run(exchange(driver, setup_run))
        assert all(outcome['status'] == 'completed' for outcome in report['outcomes'])
    else:
        failure = None
        try:
            asyncio.run(driver.run(config, wheel, run))
        except (ValueError, OSError) as error:
            failure = error
        assert not run.exists()
        assert isinstance(failure, OSError), 'run-parent status error lost its original errno'
        assert failure.errno == error_number


@pytest.mark.parametrize('error_number', [None, errno.EIO, errno.EACCES])
def test_run_parent_alias_refused_before_creating_artifacts(driver, setup_run, monkeypatch, error_number):
    from triad_dispatch_lib import DispatchError

    config, wheel, _ = setup_run
    actual = config.parent/'actual-parent'
    actual.mkdir()
    alias = config.parent/'parent-alias'
    alias.symlink_to(actual, target_is_directory=True)
    original_stat, original_lstat = os.stat, os.lstat

    def stat(path, *args, **kwargs):
        if error_number and Path(path) == alias and not kwargs.get('follow_symlinks', True):
            raise OSError(error_number, 'synthetic run-parent metadata failure', str(alias))
        return original_stat(path, *args, **kwargs)

    def lstat(path, *args, **kwargs):
        if error_number and Path(path) == alias:
            raise OSError(error_number, 'synthetic run-parent metadata failure', str(alias))
        return original_lstat(path, *args, **kwargs)

    monkeypatch.setattr(os, 'stat', stat)
    monkeypatch.setattr(os, 'lstat', lstat)
    failure = None
    try:
        asyncio.run(driver.run(config, wheel, alias/'run'))
    except (ValueError, OSError, DispatchError) as error:
        failure = error
    assert not (actual/'run').exists(), 'noncanonical parent allowed run artifact creation'
    assert not list(actual.iterdir())
    if error_number:
        assert isinstance(failure, OSError)
        assert failure.errno == error_number
    else:
        assert isinstance(failure, ValueError)
        assert str(failure) == 'Run parent must be canonical'


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
        await asyncio.sleep(.04)
        if (run/'first/cancel-request.json').exists():
            post(run, request, raw)
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


@pytest.mark.parametrize('cancellation,broken_diagnostic', [
    ('timeout', False), ('timeout', True), ('parent', False),
])
def test_cancel_publication_failure_retains_custody_until_terminal_ack(
        driver, setup_run, monkeypatch, cancellation, broken_diagnostic):
    """An I/O error must not release a native slot before its terminal receipt."""
    class BrokenDiagnostic(OSError):
        def __str__(self):
            raise RuntimeError('diagnostic formatting failed')

    async def scenario():
        config, wheel, run = setup_run
        value = json.loads(config.read_text())
        value['requests'] = value['requests'][:2]
        value['max_concurrency'] = 1
        value['requests'][0]['entry']['timeout_s'] = 1
        config.write_text(json.dumps(value))
        publication_failed = asyncio.Event()
        original_atomic = driver.atomic

        def atomic(path, payload):
            if path.name == 'cancel-request.json':
                publication_failed.set()
                if broken_diagnostic:
                    raise BrokenDiagnostic()
                raise OSError('synthetic cancellation publication failure')
            return original_atomic(path, payload)

        monkeypatch.setattr(driver, 'atomic', atomic)
        task = asyncio.create_task(driver.run(config, wheel, run))
        request = await wait_request(run, 'first')
        if cancellation == 'parent':
            task.cancel()
        async with asyncio.timeout(3):
            await publication_failed.wait()
        await asyncio.sleep(.04)
        if cancellation == 'parent':
            task.cancel()  # Repeated cancellation must also retain custody.
            await asyncio.sleep(.04)
        held_until_ack = not task.done() and not (run/'second/request.json').exists()
        # Always provide terminal cleanup, including on RED, so no task is leaked.
        post(run, request, verdict(request))
        if cancellation == 'parent':
            with pytest.raises(asyncio.CancelledError):
                await task
            assert not (run/'second/request.json').exists()
        else:
            second = await wait_request(run, 'second')
            post(run, second, verdict(second))
            report = await task
            assert held_until_ack, 'cancellation publication failure released native custody before ack'
            assert [o['status'] for o in report['outcomes']] == ['timed_out', 'completed']
            assert report['observations']['first']['cleanup_only'] is True
            diagnostic = report['observations']['first']['cancel_publication_error']
            assert diagnostic
            if broken_diagnostic:
                assert diagnostic == 'BrokenDiagnostic'
            else:
                assert 'synthetic cancellation publication failure' in diagnostic
            assert not report['agreement']['agreed']
        assert held_until_ack, 'cancellation publication failure released native custody before ack'
    asyncio.run(scenario())


@pytest.mark.parametrize('field,bad,interruption', [
    ('run_id', 'stale', None), ('status', 'running', None),
    ('parent_spawned_at', 10**400, None), ('parent_terminal_at', 10**400, None),
    ('parent_spawned_at', 10**400, 'after-deadline'),
    ('parent_terminal_at', 10**400, 'after-deadline'),
    ('run_id', 'stale', 'deadline'), ('run_id', 'stale', 'parent'),
])
def test_invalid_receipt_retains_slot_until_matching_ack(driver, setup_run, field, bad, interruption):
    async def scenario():
        config, wheel, run = setup_run
        value = json.loads(config.read_text())
        value['requests'] = value['requests'][:2]
        value['max_concurrency'] = 1
        value['requests'][0]['entry']['timeout_s'] = 1
        value['requests'][1]['entry']['timeout_s'] = 10
        config.write_text(json.dumps(value))
        task = asyncio.create_task(driver.run(config, wheel, run))
        request = await wait_request(run, 'first')
        if interruption == 'after-deadline':
            async with asyncio.timeout(3):
                while not (run/'first/cancel-request.json').exists():
                    await asyncio.sleep(.002)
        raw = verdict(request)
        malformed = receipt_for(request, raw)
        malformed[field] = bad
        post(run, request, raw, malformed)
        rejected_hash = digest((run/'first/receipt.json').read_bytes())
        await asyncio.sleep(.04)
        retained = not task.done() and not (run/'second/request.json').exists()
        cancel_requested = (run/'first/cancel-request.json').exists()
        if interruption == 'deadline':
            await asyncio.sleep(1.05)
        elif interruption == 'parent':
            task.cancel()
            await asyncio.sleep(.02)
            task.cancel()
            await asyncio.sleep(.02)
        retained_after_interrupt = not task.done() and not (run/'second/request.json').exists()
        # Always repair and drain on RED, including an incorrectly dispatched second leg.
        post(run, request, raw)
        if interruption == 'parent':
            if (run/'second/request.json').exists():
                second = await wait_request(run, 'second')
                post(run, second, verdict(second))
            with pytest.raises(asyncio.CancelledError):
                await task
        else:
            second = await wait_request(run, 'second')
            post(run, second, verdict(second))
            report = await task
            assert retained, 'invalid receipt released native custody before matching ack'
            assert report['outcomes'][0]['status'] == ('timed_out' if interruption else 'failed')
            assert report['observations']['first']['first_refusal']['receipt_sha256'] == rejected_hash
            assert report['observations']['first']['receipt']['run_id'] == 'run-1'
            assert 'cancel_publication_error' not in report['observations']['first']
            assert not report['agreement']['agreed']
        assert retained, 'invalid receipt released native custody before matching ack'
        assert cancel_requested, 'receipt refusal did not request cancellation'
        assert retained_after_interrupt, 'interruption released custody during receipt cleanup'
    asyncio.run(scenario())


@pytest.mark.parametrize('cleanup', [False, True])
@pytest.mark.parametrize('bad_response', ['hash', 'utf8', 'missing'])
def test_matching_terminal_ack_does_not_wait_for_repaired_response(driver, setup_run, cleanup, bad_response):
    async def scenario():
        config, wheel, run = setup_run
        value = json.loads(config.read_text())
        value['requests'] = value['requests'][:2]
        value['max_concurrency'] = 1
        value['requests'][0]['entry']['timeout_s'] = 1
        config.write_text(json.dumps(value))
        task = asyncio.create_task(driver.run(config, wheel, run))
        request = await wait_request(run, 'first')
        if cleanup:
            async with asyncio.timeout(3):
                while not (run/'first/cancel-request.json').exists():
                    await asyncio.sleep(.002)
        raw = b'\xff' if bad_response == 'utf8' else verdict(request)
        receipt = receipt_for(request, raw)
        if bad_response == 'hash':
            receipt['response_sha256'] = '0'*64
        post(run, request, raw, receipt)
        if bad_response == 'missing':
            (run/'first/response.txt').unlink()
        await asyncio.sleep(.08)
        advanced_before_repair = (run/'second/request.json').exists()
        # Repair only to drain an incorrectly blocked RED run before asserting.
        post(run, request, verdict(request))
        second = await wait_request(run, 'second')
        post(run, second, verdict(second))
        report = await task
        assert advanced_before_repair, 'valid terminal acknowledgment waited for response repair'
        assert report['outcomes'][0]['status'] == ('timed_out' if cleanup else 'failed')
        assert not report['agreement']['agreed']
    asyncio.run(scenario())


@pytest.mark.parametrize('cleanup', [False, True])
def test_cyclic_receipt_symlink_retains_custody_until_regular_ack(driver, setup_run, cleanup):
    async def scenario():
        config, wheel, run = setup_run
        value = json.loads(config.read_text())
        value['requests'] = value['requests'][:2]
        value['max_concurrency'] = 1
        value['requests'][0]['entry']['timeout_s'] = 1
        value['requests'][1]['entry']['timeout_s'] = 10
        config.write_text(json.dumps(value))
        task = asyncio.create_task(driver.run(config, wheel, run))
        request = await wait_request(run, 'first')
        receipt_path = run/'first/receipt.json'
        try:
            if cleanup:
                async with asyncio.timeout(3):
                    while not (run/'first/cancel-request.json').exists():
                        await asyncio.sleep(.002)
            receipt_path.symlink_to('receipt.json')
            await asyncio.sleep(.04)
            retained = not task.done() and not (run/'second/request.json').exists()
        finally:
            # Replace and drain even on RED so a refusal cannot leak callbacks.
            receipt_path.unlink(missing_ok=True)
            post(run, request, verdict(request))
            second = await wait_request(run, 'second')
            post(run, second, verdict(second))
            report = await task
        assert retained, 'cyclic receipt symlink released custody before regular ack'
        assert report['outcomes'][0]['status'] == ('timed_out' if cleanup else 'failed')
        assert report['observations']['first']['first_refusal']['validation_error'] == (
            'Expected canonical absolute regular file')
        assert report['observations']['first']['receipt']['run_id'] == 'run-1'
        assert not report['agreement']['agreed']
    asyncio.run(scenario())


def test_regular_refuses_ancestor_symlink_loop(driver, tmp_path):
    ancestor = tmp_path/'loop'
    ancestor.symlink_to('loop')
    with pytest.raises(ValueError, match='Expected canonical absolute regular file'):
        driver.regular(ancestor/'receipt.json')


@pytest.mark.parametrize('error_number', [None, errno.EIO, errno.EACCES])
@pytest.mark.parametrize('ancestor', [False, True])
def test_regular_never_reads_symlink_when_link_metadata_fails(
        driver, tmp_path, monkeypatch, error_number, ancestor):
    directory = tmp_path/'actual' if ancestor else tmp_path
    directory.mkdir(exist_ok=True)
    target = directory/'target.txt'
    target.write_bytes(b'Actual target bytes.\n')
    link = tmp_path/'link.txt'
    link.symlink_to('actual' if ancestor else 'target.txt', target_is_directory=ancestor)
    path = link/'target.txt' if ancestor else link
    assert driver.regular(target) == b'Actual target bytes.\n'
    original_stat, original_lstat = os.stat, os.lstat

    def stat(path, *args, **kwargs):
        if error_number and path == link and not kwargs.get('follow_symlinks', True):
            raise OSError(error_number, 'synthetic link metadata failure', str(link))
        return original_stat(path, *args, **kwargs)

    def lstat(path, *args, **kwargs):
        if error_number and Path(path) == link:
            raise OSError(error_number, 'synthetic link metadata failure', str(link))
        return original_lstat(path, *args, **kwargs)

    monkeypatch.setattr(os, 'stat', stat)
    monkeypatch.setattr(os, 'lstat', lstat)
    if ancestor:
        # Ancestor faults leave the regular leaf's own metadata available.
        assert path.lstat().st_size == len(b'Actual target bytes.\n')
    with pytest.raises(OSError if error_number else ValueError) as caught:
        driver.regular(path)
    if error_number:
        assert caught.value.errno == error_number
    else:
        assert str(caught.value) == 'Expected canonical absolute regular file'
    assert target.read_bytes() == b'Actual target bytes.\n'


@pytest.mark.parametrize('error_number', [None, errno.EIO, errno.EACCES])
def test_regular_following_status_failure_preserves_errno(driver, tmp_path, monkeypatch, error_number):
    path = tmp_path/'canonical.txt'
    path.write_bytes(b'Canonical file bytes.\n')
    original_stat = os.stat

    def stat(value, *args, **kwargs):
        if error_number and Path(value) == path and kwargs.get('follow_symlinks', True):
            raise OSError(error_number, 'synthetic regular type-status failure', str(path))
        return original_stat(value, *args, **kwargs)

    monkeypatch.setattr(os, 'stat', stat)
    if error_number is None:
        assert driver.regular(path) == b'Canonical file bytes.\n'
    else:
        failure = None
        try:
            driver.regular(path)
        except (ValueError, OSError) as error:
            failure = error
        assert isinstance(failure, OSError), 'regular type-status failure lost its original errno'
        assert failure.errno == error_number


@pytest.mark.parametrize('phase,error_number', [
    (phase, number)
    for phase in ('normal', 'cleanup')
    for number in (errno.EACCES, errno.EIO)
] + [('deadline', errno.EACCES), ('parent', errno.EIO)])
def test_receipt_readiness_error_retains_custody(
        driver, setup_run, monkeypatch, phase, error_number):
    async def scenario():
        config, wheel, run = setup_run
        value = json.loads(config.read_text())
        value['requests'] = value['requests'][:2]
        value['max_concurrency'] = 1
        value['requests'][0]['entry']['timeout_s'] = 1
        value['requests'][1]['entry']['timeout_s'] = 10
        config.write_text(json.dumps(value))
        receipt_path = run/'first/receipt.json'
        original_stat, original_lstat = os.stat, os.lstat
        armed = False

        def stat(path, *args, **kwargs):
            if armed and path == receipt_path and not kwargs.get('follow_symlinks', True):
                raise OSError(error_number, 'synthetic readiness probe failure', str(path))
            return original_stat(path, *args, **kwargs)

        def lstat(path, *args, **kwargs):
            if armed and path == receipt_path:
                raise OSError(error_number, 'synthetic readiness probe failure', str(path))
            return original_lstat(path, *args, **kwargs)

        monkeypatch.setattr(os, 'stat', stat)
        monkeypatch.setattr(os, 'lstat', lstat)
        task = asyncio.create_task(driver.run(config, wheel, run))
        request = await wait_request(run, 'first')
        cancelled = False
        try:
            if phase == 'cleanup':
                async with asyncio.timeout(3):
                    while not (run/'first/cancel-request.json').exists():
                        await asyncio.sleep(.002)
            armed = True
            await asyncio.sleep(.04)
            retained = not task.done() and not (run/'second/request.json').exists()
            cancellation_requested = (run/'first/cancel-request.json').exists()
            if phase == 'deadline':
                await asyncio.sleep(1.05)
            elif phase == 'parent':
                task.cancel()
                await asyncio.sleep(.02)
                task.cancel()
                await asyncio.sleep(.02)
            retained_after_interrupt = not task.done() and not (run/'second/request.json').exists()
        finally:
            # Disarm and acknowledge even on RED; drain any wrongly dispatched second leg.
            armed = False
            post(run, request, verdict(request))
            if phase != 'parent' or (run/'second/request.json').exists():
                second = await wait_request(run, 'second')
                post(run, second, verdict(second))
            try:
                report = await task
            except asyncio.CancelledError:
                cancelled = True
        assert retained, 'receipt readiness error released custody before matching ack'
        assert cancellation_requested, 'receipt readiness refusal did not request cancellation'
        assert retained_after_interrupt, 'interruption released readiness-failure custody'
        if phase == 'parent':
            assert cancelled
            assert not (run/'second/request.json').exists()
        else:
            assert not cancelled
            assert report['outcomes'][0]['status'] == (
                'timed_out' if phase in ('cleanup', 'deadline') else 'failed')
            observation = report['observations']['first']
            assert 'synthetic readiness probe failure' in observation['first_refusal']['validation_error']
            assert observation['first_refusal']['receipt_sha256'] is None
            assert observation['first_refusal']['receipt_length'] is None
            assert observation['receipt']['run_id'] == 'run-1'
            assert 'cancel_publication_error' not in observation
            assert not report['agreement']['agreed']
    asyncio.run(scenario())


@pytest.mark.parametrize('dangling', [False, True])
def test_receipt_readiness_distinguishes_absence_from_dangling_link(driver, setup_run, dangling):
    async def scenario():
        config, wheel, run = setup_run
        value = json.loads(config.read_text())
        value['requests'] = value['requests'][:2]
        value['max_concurrency'] = 1
        config.write_text(json.dumps(value))
        task = asyncio.create_task(driver.run(config, wheel, run))
        request = await wait_request(run, 'first')
        receipt_path = run/'first/receipt.json'
        try:
            if dangling:
                receipt_path.symlink_to('missing-receipt.json')
            await asyncio.sleep(.04)
            held = not task.done() and not (run/'second/request.json').exists()
            cancel_requested = (run/'first/cancel-request.json').exists()
        finally:
            receipt_path.unlink(missing_ok=True)
            post(run, request, verdict(request))
            second = await wait_request(run, 'second')
            post(run, second, verdict(second))
            report = await task
        assert held
        assert cancel_requested is dangling
        observation = report['observations']['first']
        if dangling:
            assert report['outcomes'][0]['status'] == 'failed'
            assert observation['first_refusal']['validation_error'] == (
                'Expected canonical absolute regular file')
            assert not report['agreement']['agreed']
        else:
            assert report['outcomes'][0]['status'] == 'completed'
            assert 'first_refusal' not in observation
            assert report['agreement']['agreed']
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
        if kind == 'extra-field':
            await asyncio.sleep(.04)
            if (run/'first/cancel-request.json').exists():
                post(run, request, raw)
        report = await task
        assert not report['agreement']['agreed']
        if kind != 'fenced-json': assert report['outcomes'][0]['status'] == 'failed'
        else: assert report['agreement']['reasons']['first'] == 'invalid_json'
    asyncio.run(scenario())


@pytest.mark.parametrize('error_number', [None, errno.EIO, errno.EACCES])
def test_preexisting_receipt_for_queued_leg_never_publishes_request(
        driver, setup_run, monkeypatch, error_number):
    async def scenario():
        config,wheel,run = setup_run
        receipt_path = run/'third/receipt.json'
        original_stat, original_lstat = os.stat, os.lstat
        armed = False
        probe_failed = asyncio.Event()

        def stat(path, *args, **kwargs):
            if armed and path == receipt_path:
                probe_failed.set()
                raise OSError(error_number, 'synthetic pre-publication receipt failure', str(path))
            return original_stat(path, *args, **kwargs)

        def lstat(path, *args, **kwargs):
            if armed and path == receipt_path:
                probe_failed.set()
                raise OSError(error_number, 'synthetic pre-publication receipt failure', str(path))
            return original_lstat(path, *args, **kwargs)

        monkeypatch.setattr(os, 'stat', stat)
        monkeypatch.setattr(os, 'lstat', lstat)
        task = asyncio.create_task(driver.run(config,wheel,run))
        first,second = await asyncio.gather(wait_request(run,'first'),wait_request(run,'second'))
        try:
            receipt_path.write_text('{}')
            armed = error_number is not None
            post(run,first,verdict(first)); post(run,second,verdict(second))
            if error_number is None:
                await task
            else:
                async with asyncio.timeout(3):
                    await probe_failed.wait()
            published_before_refusal = (run/'third/request.json').exists()
        finally:
            # Disarm and acknowledge a wrongly published RED request before asserting.
            armed = False
            if (run/'third/request.json').exists():
                third = await wait_request(run, 'third')
                post(run, third, verdict(third))
            report = await task
        assert not published_before_refusal, 'receipt probe error allowed queued request publication'
        assert not (run/'third/request.json').exists()
        assert not (run/'third/cancel-request.json').exists()
        assert receipt_path.read_text() == '{}'
        assert report['outcomes'][2]['status'] == 'failed'
        assert not report['agreement']['agreed']
    asyncio.run(scenario())


def test_failed_receipt_retains_original_evidence_hash(driver, setup_run):
    report = asyncio.run(exchange(driver, setup_run, lambda r,q: r.update(run_id='stale')))
    observation = report['observations']['first']
    request = json.loads((setup_run[2]/'first/request.json').read_text())
    request['_hash'] = digest((setup_run[2]/'first/request.json').read_bytes())
    rejected = receipt_for(request, verdict(request))
    rejected['run_id'] = 'stale'
    assert observation['first_refusal']['receipt_sha256'] == digest(json.dumps(rejected).encode())
    assert observation['first_refusal']['validation_error'] == 'Receipt binding mismatch'
    assert observation['receipt_sha256'] == digest((setup_run[2]/'first/receipt.json').read_bytes())


def test_investigation_cleanup_retries_preserve_duplicate_identity_evidence(driver, setup_run):
    """A reused identity must never become valid by re-reading the same ack."""
    async def scenario():
        config, wheel, run = setup_run
        value = json.loads(config.read_text())
        value['mode'] = 'investigation'
        value['requests'] = value['requests'][:2]
        for item in value['requests']:
            item['perspective'] = 'Boundary evidence'
        value['requests'][1]['entry']['timeout_s'] = 1
        config.write_text(json.dumps(value))
        task = asyncio.create_task(driver.run(config, wheel, run))
        first, second = await asyncio.gather(wait_request(run, 'first'), wait_request(run, 'second'))
        first_raw, second_raw = b'First ordinary evidence.\n', b'Second ordinary evidence.\n'
        post(run, first, first_raw, receipt_for(first, first_raw, agent='owned-first'))
        async with asyncio.timeout(3):
            while not (run/'second/cancel-request.json').exists():
                await asyncio.sleep(.002)
        post(run, second, second_raw, receipt_for(second, second_raw, agent='owned-first'))
        # Several actual cleanup polls must reject this identical duplicate ack.
        await asyncio.sleep(.08)
        waited_for_unique_ack = not task.done()
        # Supply valid unique terminal cleanup even on RED, so no task is leaked.
        replacement = run/'second/receipt.replacement'
        replacement.write_text(json.dumps(receipt_for(second, second_raw, agent='owned-second')))
        replacement.replace(run/'second/receipt.json')
        report = await task
        assert waited_for_unique_ack, 'duplicate cleanup receipt released custody on retry'
        assert [o['status'] for o in report['outcomes']] == ['completed', 'timed_out']
        assert report['observations']['second']['receipt']['agent_id'] == 'owned-second'
        assert report['observations']['second']['duplicate_agent'] is True
        assert report['observations']['second']['validation_error'] == 'Reused agent identity'
        assert report['integrity_ok'] is False
        assert 'agreement' not in report
    asyncio.run(scenario())

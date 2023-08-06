import pytest
import inspect
import functools
import asyncio
import qasync

'''
QtWebEngineWidgets wants to be inited BEFORE the QApplication is created.
We create application here, because we want to run the QEventLoop
'''
if qasync.QtModuleName == 'PyQt5':
    try:
        from PyQt5 import QtWebEngineWidgets
    except:
        pass
elif qasync.QtModuleName == 'PySide2':
    try:
        from PySide2 import QtWebEngineWidgets
    except:
        pass
elif qasync.QtModuleName == 'PySide6':
    try:
        from PySide6 import QtWebEngineWidgets
    except:
        pass
else:
    raise NotImplementedError(qasync.QtModuleName)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "qasync: mark async function as a test to be ran using qasync event loop",
    )


@pytest.mark.tryfirst
def pytest_pycollect_makeitem(collector, name, obj):
    if collector.funcnamefilter(name) and inspect.iscoroutinefunction(obj):
        item = pytest.Function.from_parent(collector, name=name)
        if "qasync" in item.keywords:
            return list(collector._genfunctions(name, obj))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_pyfunc_call(pyfuncitem):
    if "qasync" in pyfuncitem.keywords:
        pyfuncitem.obj = wrap_in_sync(
            pyfuncitem.obj, _loop=pyfuncitem.funcargs["event_loop"]
        )
    yield


def pytest_runtest_setup(item):
    if "qasync" in item.keywords:
        # inject an event loop fixture for all async tests
        if "event_loop" in item.fixturenames:
            item.fixturenames.remove("event_loop")
        item.fixturenames.insert(0, "event_loop")


def wrap_in_sync(func, _loop):
    @functools.wraps(func)
    def inner(**kwargs):
        coro = func(**kwargs)
        if coro is not None:
            task = asyncio.ensure_future(coro, loop=_loop)
            try:
                _loop.run_until_complete(task)
            except BaseException:
                # run_until_complete doesn't get the result from exceptions
                # that are not subclasses of `Exception`. Consume all
                # exceptions to prevent asyncio's warning from logging.
                if task.done() and not task.cancelled():
                    task.exception()
                raise

    return inner


@pytest.hookimpl(trylast=True)
def pytest_fixture_post_finalizer(fixturedef, request):
    if fixturedef.argname == "event_loop":
        # Set empty loop policy, so that subsequent get_event_loop() provides a new loop
        asyncio.set_event_loop_policy(None)


class FixtureStripper:
    REQUEST = "request"
    EVENT_LOOP = "event_loop"

    def __init__(self, fixturedef):
        self.fixturedef = fixturedef
        self.to_strip = set()

    def add(self, name):
        if name in self.fixturedef.argnames:
            return
        self.fixturedef.argnames += (name,)
        self.to_strip.add(name)

    def get_and_strip_from(self, name, data_dict):
        result = data_dict[name]
        if name in self.to_strip:
            del data_dict[name]
        return result


@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef):
    if fixturedef.argname == "event_loop":
        outcome = yield
        loop = outcome.get_result()
        policy = asyncio.get_event_loop_policy()
        try:
            old_loop = policy.get_event_loop()
            if old_loop is not loop:
                old_loop.close()
        except RuntimeError:
            # Swallow this, since it's probably bad event loop hygiene.
            pass
        policy.set_event_loop(loop)
        return

    if inspect.iscoroutinefunction(fixturedef.func):
        coro = fixturedef.func

        fixture_stripper = FixtureStripper(fixturedef)
        fixture_stripper.add(FixtureStripper.EVENT_LOOP)

        def wrapper(*args, **kwargs):
            loop = fixture_stripper.get_and_strip_from(
                FixtureStripper.EVENT_LOOP, kwargs
            )

            return loop.run_until_complete(coro(*args, **kwargs))

        fixturedef.func = wrapper

    yield


_app = qasync.QApplication([])  # this has to be global, or I get intermittent Qt warnings/crashes at shutdown

@pytest.fixture
def event_loop():
    loop = qasync.QEventLoop(_app)
    try:
        yield loop
    finally:
        loop.close()

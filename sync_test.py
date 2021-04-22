import pytest

from sync import SyncCommand


@pytest.fixture(name='sync')
def fixture_twitter(request):
    sync = SyncCommand(idc=1, command='hdw_ngpio')
    yield sync


def test_sync(sync):
    assert sync.prefix == 'hdw'

import pytest

from sync import SyncCommand


@pytest.fixture(name='sync')
def fixture_twitter(request):
    sync = SyncCommand(idc=1, command='hdw_ngpio')
    yield sync


def test_sync(sync):
    assert sync.prefix == 'hdw'


@pytest.mark.parametrize('com, expected', (
        ('hdw_ngpio', 'hdw'),
        ('itf_ngpio', 'itf'),
        ('itf-ngpio', ''),
        ('', ''),
        (1, ''),
        (True, ''),
))
def test_sync_set_prefix(sync, com, expected):
    sync.command = com
    sync.set_prefix()
    assert sync.prefix == expected


@pytest.mark.parametrize('com, prx, expected', (
        ('hdw_ngpio', 'hdw', True),
        ('itf_ngpio', 'itf', True),
        ('itf-ngpio', 'itf', False),
        ('', '', True),
        ('', False, True),
        ('', None, True),
))
def test_sync_check_prefix(sync, com, prx, expected):
    sync.command = com
    sync.set_prefix()
    assert sync.check_prefix(prx) == expected


@pytest.mark.parametrize('idx, ep, expected', (
        (1, 'sync/', 'sync/1/'),
        (1, '/sync', 'sync/1/'),
        (2, '/', '2/'),
        (0, '/', ''),
        (0, '/sync', ''),
        ("0", '/sync', ''),
        (1, '', ''),
))
def test_sync_parse_endpoint(sync, idx, ep, expected):
    sync.idc = idx
    sync.parse_endpoint(ep)
    assert sync.endpoint == expected


@pytest.mark.parametrize('val, expected', (
        (33, 'True'),
        (True, 'True'),
        ('true', 'True'),
        ('T', 'True'),
        ('', 'False'),
        ('Dupa', 'False'),
        (0, 'False'),
        (False, 'False'),
(None, 'False'),
))
def test_sync_set_value(sync, val, expected):
    sync.set_value(val)
    assert sync.value == expected

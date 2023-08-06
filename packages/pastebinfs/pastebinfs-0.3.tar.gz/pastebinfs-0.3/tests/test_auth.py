import requests_mock
import pastebinfs.sync
import pytest

def test_valid_auth(requests_mock: requests_mock.Mocker):
    requests_mock.post('https://pastebin.com/api/api_login.php', text='837AD232A4F231AFF')
    user_key = pastebinfs.sync.pastebin_auth("api_key", "username", "password")
    assert user_key == "837AD232A4F231AFF", "incorrect user key"


def test_invalid_api_key(requests_mock: requests_mock.Mocker):
    requests_mock.post('https://pastebin.com/api/api_login.php', status_code=401, text="Bad API request, invalid api_dev_key")
    with pytest.raises(ValueError, match='Bad API request, invalid api_dev_key'):
        pastebinfs.sync.pastebin_auth("api_key", "username", "password")


def test_invalid_credentials(requests_mock: requests_mock.Mocker):
    requests_mock.post('https://pastebin.com/api/api_login.php', status_code=401, text="Bad API request, invalid api_dev_key")
    with pytest.raises(ValueError, match='Bad API request, invalid api_dev_key'):
        pastebinfs.sync.pastebin_auth("api_key", "username", "password")

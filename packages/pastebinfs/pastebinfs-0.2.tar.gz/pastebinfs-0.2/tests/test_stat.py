from tests.pastebin_api_mock import setup_fake_pastebin_api
import requests_mock
import pastebinfs.os
import requests

def test_os_stat(requests_mock: requests_mock.Mocker):
    setup_fake_pastebin_api(requests_mock)
    res = pastebinfs.os.stat("test.txt", "api_key", "837AD232A4F231AFF")
    assert res.st_birthtime == 1297953260, "wrong creation/update time"
    assert res.st_key == '0b42rwhf', "wrong paste_key time"
    assert res.st_mode == 0, "wrong visibility mode time"
    assert res.st_size == 15, "wrong size time"
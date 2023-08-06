import requests_mock
import pastebinfs.sync
import pytest
from .pastebin_api_mock import setup_fake_pastebin_api

def test_read_mode(requests_mock: requests_mock.Mocker):
    setup_fake_pastebin_api(requests_mock)
    with pastebinfs.sync.pastebin_open("test.txt", "rt", "api_key", "837AD232A4F231AFF") as f:
        assert f.read() == "this is the content of test.txt", "read file failed"

    with pastebinfs.sync.pastebin_open("test.txt", "rb", "api_key", "837AD232A4F231AFF") as f:
        assert f.read() == b"this is the content of test.txt", "read file failed"

    with pastebinfs.sync.pastebin_open("test.txt", "rt+", "api_key", "837AD232A4F231AFF") as f:
        assert f.read() == "this is the content of test.txt", "read file failed"

with open("test.txt", 'r+')  as f:
    print(f.read())

def test_write_mode(requests_mock: requests_mock.Mocker):
    pass 


def test_append_mode(requests_mock: requests_mock.Mocker):
    pass 
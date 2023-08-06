import requests_mock
import pastebinfs.sync
import pytest

def test_open_without_openmode(requests_mock: requests_mock.Mocker):
    with pytest.raises(ValueError, match='must have exactly one of create/read/write/append mode'):
        pastebinfs.sync.pastebin_open("a.txt", "", "api_key", "username", "password")

def test_open_with_incompatible_openmode(requests_mock: requests_mock.Mocker):
    with pytest.raises(ValueError, match='must have exactly one of create/read/write/append mode'):
        pastebinfs.sync.pastebin_open("a.txt", "rw", "api_key", "username", "password")
    
    with pytest.raises(ValueError, match='must have exactly one of create/read/write/append mode'):
        pastebinfs.sync.pastebin_open("a.txt", "ra", "api_key", "username", "password")

    with pytest.raises(ValueError, match='must have exactly one of create/read/write/append mode'):
        pastebinfs.sync.pastebin_open("a.txt", "wa", "api_key", "username", "password")

    with pytest.raises(ValueError, match='must have exactly one of create/read/write/append mode'):
        pastebinfs.sync.pastebin_open("a.txt", "rwa", "api_key", "username", "password")

    with pytest.raises(ValueError, match='must have exactly one of create/read/write/append mode'):
        pastebinfs.sync.pastebin_open("a.txt", "rwa+", "api_key", "username", "password")

    with pytest.raises(ValueError, match=r'open mode must be either \(t\)ext or \(b\)inary'):
        pastebinfs.sync.pastebin_open("a.txt", "rtb", "api_key", "username", "password")
    

def test_open_existing_file(requests_mock: requests_mock.Mocker):
    pass# if flag is x or r then the file must exist

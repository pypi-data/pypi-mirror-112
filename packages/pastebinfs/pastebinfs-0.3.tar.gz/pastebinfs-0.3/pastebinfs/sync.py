from pastebinfs.parse_path import parse_path
from pastebinfs.pastebin import bufferedbyte, pastebinapi
from pastebinfs.pastebin import bufferedtext
from pastebinfs.pastebin import MAX_PATH_LENGTH

from typing import Union

def pastebin_auth(api_key: str, username: str, password: str) -> str:
    """Login the user and retruns his ``user_key``

    This key can be cached since, it is only invalidated by the next (api) login.

    Arguments:
        api_key {str} -- the api_key of the application.

        username {str} -- the username of the user that wants to login.

        password {str} -- the password of the user that wants to login.

    Returns:
        user_key {str} -- The ``user_key`` of the user that logged in.

    Raises:
        ValueError: Bad API request, use POST request, not GET
        ValueError: Bad API request, invalid api_dev_key
        ValueError: Bad API request, invalid login
        ValueError: Bad API request, account not active
        ValueError: Bad API request, invalid POST parameters
    """
    return pastebinapi.get_user_key(api_key, username, password)


def pastebin_open(path: str, open_mode: str = "rt", api_key: str = None, user_key: str = None, buffering: bool = True) -> Union[bufferedtext.BufferedTextPastebinFile, bufferedbyte.BufferedBinaryPastebinFile]:
    """Returns a ``File-Like`` object

    get_your ``user_key`` with: ``pastebinfs.sync.pastebin_auth(api_key, username, password)``

    open_mode:
        * 'r' open for reading (default)
        * 'w' open for writing, truncating the file first
        * 'x' open for exclusive creation, failing if the file already exists
        * 'a' open for writing, appending to the end of the file if it exists
        * 'b' binary mode
        * 't' text mode (default)
        * '+' open for updating (reading and writing)

    Arguments:
        path {str} -- a path where the file should be stored (max. 100 chars).

        open_mode {str} -- see above.
        
        api_key {str} -- the api_key of the application.

        user_key {str} -- the user_key of the user you want the create the file for.

        buffering {bool} -- if buffering is enabled the file is only updated on close or flush else the file will be updated on write

    Returns:
        a File-Like object {multiple} -- The ``user_key`` of the user that logged in.

    Raises:
        PermissionError: If user_key or api_key is not set
        OverflowError: If the path exceeds the max length of 100 characters
        FileExistsError: If the file is opened with flag 'x' and exits this error is thrown
        ValueError: If the file is open in multiple modes (r and w)

    """
    path = parse_path(path)
    open_mode = open_mode.lower()
    
    if not api_key or not user_key:
        raise PermissionError("you need to supply a api_key as well as user_key")

    if len(path) > MAX_PATH_LENGTH:
        raise OverflowError("path too long, max length is 100 characters")

    open_mode_ctr = 0

    if 'w' in open_mode:
       open_mode_ctr += 1
    
    if 'r' in open_mode:
       open_mode_ctr += 1
    
    if 'a' in open_mode:
       open_mode_ctr += 1
    
    if 'x' in open_mode:
       open_mode_ctr += 1
    
    if open_mode_ctr != 1:
        raise ValueError('must have exactly one of create/read/write/append mode')

    if 't' in open_mode and 'b' in open_mode:
        raise ValueError('open mode must be either (t)ext or (b)inary')

    file_ids_at_path = pastebinapi.get_all_pastes_ids_with_path(path, api_key, user_key)

    if 'x' in open_mode and file_ids_at_path:
        raise FileExistsError("the file already exists")
    
    if 'r' in open_mode and not file_ids_at_path:
        raise FileNotFoundError("the requested file was not found")

    if not buffering: 
        raise NotImplementedError("not buffered binary file not supported")

    if 'b' in open_mode:
        return bufferedbyte.BufferedBinaryPastebinFile(path, api_key, user_key, open_mode)

    return bufferedtext.BufferedTextPastebinFile(path, api_key, user_key, open_mode)

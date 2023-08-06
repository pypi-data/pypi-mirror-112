import re
import xml.etree.ElementTree as ET
from typing import List
import requests

def get_user_key(api_key: str, username: str, password: str) -> str:
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
    r = requests.post("https://pastebin.com/api/api_login.php",
                      data={
                          "api_dev_key": api_key,
                          "api_user_name": username,
                          "api_user_password": password
                      })

    try:
        r.raise_for_status()
    except:
        raise ValueError(r.text)

    return r.text


def get_all_pastes_by_user(api_key: str, user_key: str) -> List[dict]:
    """Returns all pastes with a dict of metadata
    
    Possible keys:
    ```
        paste_key
        paste_date
        paste_title
        paste_size
        paste_expire_date
        paste_private
        paste_format_long
        paste_format_short
        paste_url
        paste_hits
    ```

    Arguments:
        api_key {str} -- the api_key of the application.

        user_key {str} -- the user_key of the user you want the pastes for.

    Returns:
        list of pastes infos {list} -- paste info is a dict with the keys mentioned above.

    Raises:
        ValueError: Bad API request, invalid api_dev_key
        ValueError: Bad API request, invalid api_user_key
    """
    r = requests.post("https://pastebin.com/api/api_post.php", data={
        "api_dev_key": api_key,
        "api_option": "list",
        "api_results_limit": 1000,
        "api_user_key": user_key
    })

    try:
        r.raise_for_status()
    except:
        raise ValueError(r.text)

    if r.text == "No pastes found.":
        return list()

    out = list()

    root = ET.fromstring(f'<?xml version="1.0"?><data>{r.text}</data>')
    for element in root:
        element_dict = dict()
        for node in element:
            element_dict[node.tag] = node.text

        out.append(element_dict)

    return out


def get_meta_data_for_path(path: str, api_key: str, user_key: str) -> List[dict]:
    """returns all metadata for a given path

    Arguments:
        path {str} -- the path(name) of the pastes.

        api_key {str} -- the api_key of the application.

        user_key {str} -- the user_key of the user you want the pastes for.

    Returns:
        List of paste metadata {List[dict]} -- all metadata pastes with the ``pastename == path``.
    """
    pastes = get_all_pastes_by_user(api_key, user_key)
    return list(filter(lambda paste: paste['paste_title'] == path, pastes))


def get_all_pastes_ids_with_path(path: str, api_key: str, user_key: str) -> List[str]:
    """returns all paste id with the name ``path``

    Arguments:
        path {str} -- the path(name) of the pastes.

        api_key {str} -- the api_key of the application.

        user_key {str} -- the user_key of the user you want the pastes for.

    Returns:
        List of pastes {List[str]} -- Returns all pastes with the ``pastename == path``.
    """
    pastes_data = get_meta_data_for_path(path, api_key, user_key)
    return list(map(lambda x: x['paste_key'], pastes_data))


def get_paste(id: str, api_key: str, user_key: str) -> str:
    """returns the content of a paste

    Arguments:
        id {str} -- the id of the paste.

        api_key {str} -- the api_key of the application.

        user_key {str} -- the user_key of the user you want the paste for.

    Returns:
        paste content {str} -- Returns the content of the paste.

    Raises:
        ValueError: Invalid paste id
        ValueError: Bad API request, invalid api_dev_key
        ValueError: Bad API request, invalid api_user_key
        ValueError: Bad API request, invalid permission to view this paste or invalid api_paste_key
    """
    r = requests.post("https://pastebin.com/api/api_raw.php",
                      data={
                          "api_dev_key": api_key,
                          "api_paste_key": id,
                          "api_option": "show_paste",
                          "api_user_key": user_key
                      })

    try:
        r.raise_for_status()
    except:
        raise ValueError(r.text)

    return r.text

def get_paste_for_path(path: str, api_key: str, user_key: str) -> str:
    """returns the content of a paste

    Arguments:
        path {str} -- the path(name) of the paste.

        api_key {str} -- the api_key of the application.

        user_key {str} -- the user_key of the user you want the paste for.

    Returns:
        paste content {str} -- Returns the content of the paste.

    Raises:
        ValueError: Paste does not exist
    """
    list_of_paste_ids = get_all_pastes_ids_with_path(path, api_key, user_key)
    if not list_of_paste_ids:
        raise ValueError("no paste at path found")
    
    return get_paste(list_of_paste_ids[0], api_key, user_key)


def delete_paste(id: str, api_key: str, user_key: str) -> None:
    """delete a paste with the given ``id``

    Arguments:
        id {str} -- the id of the paste.

        api_key {str} -- the api_key of the application.

        user_key {str} -- the user_key of the user.

    Returns: None

    Raises:
        ValueError: Bad API request, invalid api_dev_key
        ValueError: Bad API request, invalid api_user_key
        ValueError: Bad API request, invalid permission to remove paste
    """
    r = requests.post("https://pastebin.com/api/api_post.php",
                      data={
                          "api_dev_key": api_key,
                          "api_paste_key": id,
                          "api_option": "delete",
                          "api_user_key": user_key
                      })
    
    try:
        r.raise_for_status()
    except:
        raise ValueError(r.text)

    if r.text != "Paste Removed":
        raise Exception("paste could not be removed")


def create_paste(path: str, data: bytes, api_key: str, user_key: str, visibility: int = 1) -> str:
    """Create a paste with the name=``path`` and content=``data``

    Arguments:
        path {str} -- the path(name) of the paste.

        data {bytes} -- the content of the new paste.

        api_key {str} -- the api_key of the application.

        user_key {str} -- the user_key of the user.

        visibility {int} -- the visibility of the new paste: ``public = 0, unlisted = 1(Default), private = 2``.

    Returns: 
        paste_key {str} -- the paste_key of the new generated paste

    Raises:
        ValueError: Bad API request, invalid api_dev_key
        ValueError: Bad API request, maximum number of 25 unlisted pastes for your free account
        ValueError: Bad API request, maximum number of 10 private pastes for your free account
        ValueError: Bad API request, api_paste_code was empty
        ValueError: Bad API request, maximum paste file size exceeded
        ValueError: Bad API request, invalid api_paste_private
        ValueError: Bad API request, invalid api_paste_format
        ValueError: Bad API request, invalid api_user_key
        ValueError: Bad API request, invalid or expired api_user_key
        ValueError: Bad API request, you can't add paste to folder as guest
    """
    r = requests.post("https://pastebin.com/api/api_post.php",
                      data={
                          "api_dev_key": api_key,
                          "api_paste_code": data,
                          "api_paste_name": path,
                          "api_option": "paste",
                          "api_paste_private": visibility, # public = 0, unlisted = 1, private = 2
                          "api_user_key": user_key
                      })

    try:
        r.raise_for_status()
    except:
        raise ValueError(r.text)

    new_paste_id = re.match("https://pastebin.com/(.*?)$", r.text)
    return new_paste_id and new_paste_id.group(1)


def create_or_update_paste(path: str, data: bytes, api_key: str, user_key: str, visibility: int = 1) -> str:
    """Create a paste(if not exists) or delete a old paste and create a new one with same name("update")

    Arguments:
        path {str} -- the path(name) of the paste.

        data {bytes} -- the content of the new paste.

        api_key {str} -- the api_key of the application.

        user_key {str} -- the user_key of the user.

        visibility {int} -- the visibility of the new paste: ``public = 0, unlisted = 1(Default), private = 2``.

    Returns:
        paste_key {str} -- the paste_key of the new generated paste    
    """
    pastes = get_all_pastes_ids_with_path(path, api_key, user_key)
    new_id = create_paste(path, data, api_key, user_key)
    for paste in pastes:
        delete_paste(paste, api_key, user_key)
    return new_id

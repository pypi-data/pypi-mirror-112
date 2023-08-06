from pastebinfs.parse_path import parse_path
from pastebinfs.pastebin import pastebinapi
from dataclasses import dataclass

@dataclass(init=False)
class patebin_stat_result:
    st_size: int  # size of file, in bytes please remind: Binary files are base64 encoded so this might be off
    st_updatetime: int  # time of file creation(or last update)
    st_mode: int  # protection modes, public = 0, unlisted = 1, private = 2
    st_key: str  # the paste key

def stat(path: str, api_key: str, user_key: str) -> patebin_stat_result:    
    path = parse_path(path)
    pastes_metadata = pastebinapi.get_meta_data_for_path(path, api_key, user_key)    
    if not pastes_metadata:
        raise FileNotFoundError("cant find file")

    first_paste = pastes_metadata[0]

    stat_result = patebin_stat_result()
    stat_result.st_size = int(first_paste['paste_size'])
    stat_result.st_updatetime = int(first_paste['paste_date'])
    stat_result.st_mode = int(first_paste['paste_private'])
    stat_result.st_key = first_paste['paste_key']
    return stat_result

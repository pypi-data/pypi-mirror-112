"""
Pastebin Buffered text File implementation
"""

import io
from typing import List, Optional, final

from pastebinfs.pastebin import pastebinapi
from pastebinfs.pastebin import MAX_FILE_SIZE

# TextIOBase
# https://docs.python.org/3/library/io.html#io.TextIOBase
# https://github.com/python/cpython/blob/bb3e0c240bc60fe08d332ff5955d54197f79751c/Lib/_pyio.py#L1843

@final
class BufferedTextPastebinFile(io.TextIOBase):
    def __init__(self, path: str, api_key: str, user_key: str, open_mode: str) -> None:
        super().__init__()
        self._path = path
        self._api_key = api_key
        self._user_key = user_key
        self._open_mode = open_mode
        self._closed = False
        self._buffer = io.StringIO()
        self._loaded = False

    def readable(self) -> bool:
        if self.closed:
            raise ValueError("I/O operation on closed file.")
        return 'r' in self._open_mode or '+' in self._open_mode

    def writable(self) -> bool: 
        if self.closed:
            raise ValueError("I/O operation on closed file.")
    
        return 'a' in self._open_mode or 'w' in self._open_mode or '+' in self._open_mode
    
    def seekable(self) -> bool:
        return True

    def close(self) -> None:
        self.flush()
        try:
            self._buffer.close()
        finally:
            self._buffer.close()
            self._closed = True
        
    @property
    def closed(self) -> bool:
        return self._closed
    
    def __load_data(self):
        if not self._loaded:
            if 'r' in self._open_mode or 'a' in self._open_mode:
                paste_content_encoded = pastebinapi.get_paste_for_path(self._path, self._api_key, self._user_key)

                old_seek_pos = self._buffer.tell()
                self._buffer.seek(0, io.SEEK_SET)
                self._buffer.write(paste_content_encoded)
                self._buffer.seek(old_seek_pos, io.SEEK_SET)

                if 'a' in self._open_mode:
                    self._buffer.seek(0, io.SEEK_END)
        
        self._loaded = True

    def read(self, __size: Optional[int] = None) -> str:
        if self.closed:
            raise ValueError("I/O operation on closed file.")

        if not self.readable():
            raise ValueError("not readable")

        self.__load_data()
        return self._buffer.read(__size)

    def readline(self, __size: int) -> str:
        if self.closed:
            raise ValueError("I/O operation on closed file.")

        if not self.readable():
            raise ValueError("not readable")

        self.__load_data()
        return self._buffer.readline(__size)
        
    def readlines(self, __hint: int) -> List[str]:
        if self.closed:
            raise ValueError("I/O operation on closed file.")

        if not self.readable():
            raise ValueError("not readable")

        self.__load_data()
        return self._buffer.readlines(__hint)

    def write(self, __s: str) -> int:
        if self.closed:
            raise ValueError("I/O operation on closed file.")

        if not self.writable():
            raise ValueError("not writable")
        
        self.__load_data()
        
        return self._buffer.write(__s)

    def flush(self) -> None:
        if self.closed:
            raise ValueError("I/O operation on closed file.")

        if self.writable():
            old_seek_pos = self._buffer.tell()
            self._buffer.seek(0, io.SEEK_SET)
            data = self._buffer.read()
           
            if len(data) > MAX_FILE_SIZE:
                raise BufferError("cannot upload file - too large")

            pastebinapi.create_or_update_paste(self._path, data, self._api_key, self._user_key)

            self._buffer.seek(old_seek_pos, io.SEEK_SET)

    def truncate(self, __size: Optional[int]) -> int:
        return super().truncate(__size=__size)
    
    def seek(self, __offset: int, __whence: int = 0) -> int:
        return self._buffer.seek(__offset, __whence)

    def tell(self) -> int:
        if self.closed:
            raise ValueError("tell from closed file")

        return self._buffer.tell()
from abc import abstractmethod
import os
from datetime import datetime


class LocalFileCache:
    def __init__(self, root_path, ttl=None) -> None:
        self.root_path = root_path
        self.ttl = ttl

    def _is_valid_(self, local_file_path, ttl=None) -> bool:
        ttl = ttl or self.ttl
        if not os.path.isfile(local_file_path):
            return False

        if ttl is None:
            return True

        mod_time = datetime.fromtimestamp(os.stat(local_file_path).st_mtime)
        if (datetime.now() - mod_time).seconds < self.ttl:
            return True

        return False

    def require(self, key, ttl=None, *args, **kargs):
        local_file_path = self.key_to_local_relative_path(key, *args, **kargs)
        local_file_path = os.path.join(self.root_path, local_file_path)
        if self._is_valid_(local_file_path, ttl=ttl):
            return local_file_path

        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        self.retrieve(key, local_file_path, *args, **kargs)
        return local_file_path

    @abstractmethod
    def key_to_local_relative_path(self, key, *args, **kargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, key, local_file_path, *args, **kargs) -> None:
        raise NotImplementedError

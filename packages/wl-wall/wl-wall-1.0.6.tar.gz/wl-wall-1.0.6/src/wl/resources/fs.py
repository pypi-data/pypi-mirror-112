from os import scandir
from pathlib import Path, PosixPath
from typing import Dict, List, Callable


class Fs:
    def __init__(self, path: Path=None):
        self.path = path

    def set_path(self, path: Path):
        self.path = path

    def get_path_content(self) -> Dict[str, PosixPath]:
        result = {}
        for dirent in scandir(self.path):
            result[dirent.name] = dirent

        return result

    def get_path_content_keys(self) -> List[str]:
        content = self.get_path_content()
        content = list(content.keys())
        content.sort()

        return content

    def get_path_content_values(self) -> List[PosixPath]:
        content = self.get_path_content()
        content = list(content.values())

        return content


fs = Fs()

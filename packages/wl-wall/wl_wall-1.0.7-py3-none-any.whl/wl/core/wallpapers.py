from pathlib import Path
from ..resources.fs import fs
from ..resources.config import config
from ..cli.log import warn


class Wallpapers:
    def __init__(self):
        self.config = config.parse()

    def get_wallpapers(self):
        if not "wallpapers_folder" in self.config:
            warn(
                "The wallpapers folder is not configured, please setup it key in the config | error at get wallpapers for parser"
            )

            return []
        files = []
        fs.set_path(Path(self.config['wallpapers_folder']))
        for dirent in fs.get_path_content_values():
            if dirent.is_file():
                files.append(dirent.name)
        files.sort()

        return files


wallpapers = Wallpapers()

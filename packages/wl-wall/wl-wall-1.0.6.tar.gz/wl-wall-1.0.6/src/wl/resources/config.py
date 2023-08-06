import json
from typing import Dict, TypeVar
from ..paths import config_dir_path, config_path
from ..cli.log import warn

V = TypeVar("V")


class Config:
    def __init__(self):
        self.options = [
            'wallpapers_folder'
        ]

    def check(self, create: bool=False):
        if not config_dir_path.is_dir():
            warn(f'Config dir path: {config_dir_path} not found')
            if create:
                config_dir_path.mkdir()
        if not config_path.is_file():
            warn(f'Config file path: {config_path} not found')
            if create:
                config_path.touch()
                self.dump({})

    def parse(self) -> Dict[str, V]:
        with open(config_path, 'r') as config:
            return json.load(config)

    def dump(self, new_dict: Dict[str, V]) -> Dict[str, V]:
        with open(config_path, 'w') as config:
            json.dump(new_dict, config)

        return self.parse()


config = Config()

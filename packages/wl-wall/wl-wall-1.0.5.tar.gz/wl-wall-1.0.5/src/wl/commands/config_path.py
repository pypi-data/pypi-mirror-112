from .command import Command
from ..paths import config_path


class ConfigPath(Command):
    def run(self):
        print('The config path is:', str(config_path.absolute()))

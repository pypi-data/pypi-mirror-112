from .command import Command
from ..resources.config import config
from ..cli.log import error, success

class Config(Command):
    def meta(self):
        self.config_options = config.options
        self.config = config.parse()

    def run(self):
        self.config[self._argv.key] = self._argv.value
        config.dump(self.config)
        success(f'Updated config successfully.\n{self._argv.key} = {self._argv.value}')

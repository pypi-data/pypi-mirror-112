from .command import Command
from ..resources.config import config
from ..cli.datatypes.str import title
from ..cli.datatypes.dict import display


class ConfigGet(Command):
    def meta(self):
        self.config = config.parse()

    def run(self):
        title('Config data')
        if not self._argv.raw:
            display(self.config)
            return

        print(self.config)

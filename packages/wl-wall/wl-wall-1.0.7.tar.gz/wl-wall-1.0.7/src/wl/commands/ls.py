from .command import Command
from ..core.wallpapers import wallpapers
from ..cli.datatypes.str import title
from ..cli.datatypes.list import display


class Ls(Command):
    def meta(self):
        self.wallpapers = wallpapers.get_wallpapers()

    def run(self):
        if not self._argv.it:
            title('Available wallpapers')
            display(self.wallpapers)
        else:
            print(' '.join(self.wallpapers))

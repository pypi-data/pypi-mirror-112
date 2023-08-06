import subprocess
from pathlib import Path
from .command import Command
from ..resources.config import config
from ..cli.log import error, success


class Restore(Command):
    def meta(self):
        self.config = config.parse()
        if not 'wallpaper' in self.config:
            error('Before execute this, please set a wallpaper with the set command')
        self.wallpaper_path = Path(self.config['wallpaper'])
        self.command = f"feh --bg-scale {self.wallpaper_path.absolute()}"

    def run(self):
        subprocess.run([self.command], shell=True)
        success(f"Updated wallpaper successfully\nSet wallpaper -> {self.wallpaper_path}")

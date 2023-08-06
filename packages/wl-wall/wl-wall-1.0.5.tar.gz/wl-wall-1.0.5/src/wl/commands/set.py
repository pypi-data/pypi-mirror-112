import subprocess
from pathlib import Path
from .command import Command
from ..core.wallpapers import wallpapers
from ..cli.log import success, error, info
from ..resources.config import config


class Set(Command):
    def meta(self):
        self.wallpapers = wallpapers.get_wallpapers()
        self.config = config.parse()
        if not 'wallpapers_folder' in self.config:
            error('Invalid wallpapers folder, please setup it with the config command')
        self.wallpaper_path = Path(self.config['wallpapers_folder']) / self._argv.wallpaper
        self.command = f"feh --bg-scale {self.wallpaper_path.absolute()}"

    def run(self):
        subprocess.run([self.command], shell=True)
        success(f"Updated wallpaper successfully\nSet wallpaper -> {self._argv.wallpaper}")
        info('Reconfiguring the config (to save the actual wallpaper)')
        self.config['wallpaper'] = str(self.wallpaper_path)
        config.dump(self.config)
        success('Configuration update successfully!')

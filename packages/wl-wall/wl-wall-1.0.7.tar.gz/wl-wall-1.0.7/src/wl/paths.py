from pathlib import Path
from os.path import expanduser

config_dir_path = Path(expanduser('~')) / '.config/wl'
config_path = config_dir_path / 'wl.conf.json'

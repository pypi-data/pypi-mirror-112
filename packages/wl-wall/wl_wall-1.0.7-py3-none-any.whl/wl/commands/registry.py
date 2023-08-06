from .config import Config
from .config_get import ConfigGet
from .set import Set
from .ls import Ls
from .config_path import ConfigPath
from .restore import Restore

registry = {
    'config': Config,
    'config_get': ConfigGet,
    'set': Set,
    'ls': Ls,
    'config_path': ConfigPath,
    'restore': Restore
}

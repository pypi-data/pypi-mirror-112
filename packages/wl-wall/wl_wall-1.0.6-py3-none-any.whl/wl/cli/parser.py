import argparse
from .. import __version__
from ..resources.config import config
from ..core.wallpapers import wallpapers

config_options = config.options
parser = argparse.ArgumentParser(prog="wl", description="A simply cli wallpaper manager.")
parser.add_argument("-v", "--version", action="version", version=__version__)
subparsers = parser.add_subparsers(title="subparsers")
config_parser = subparsers.add_parser("config", help="Modify the config")
config_parser.set_defaults(subparser="config")
config_parser.add_argument(
    "-k",
    "--key",
    help="Choose a config key",
    choices=config_options,
)
config_parser.add_argument(
    "-v",
    "--value",
    help="A value for the choosen config key",
)
config_parser_subparsers = config_parser.add_subparsers(title="subparsers")
config_parser_get = config_parser_subparsers.add_parser(
    "get", help="A config parser displayer"
)
config_parser_get.set_defaults(subparser="config_get")
config_parser_get.add_argument(
    '-r', '--raw',
    action='store_true',
    help='Represent the data as JSON (if it task is posible)'
)
config_parser_path = config_parser_subparsers.add_parser(
    'path', help='Display the config path'
)
config_parser_path.set_defaults(subparser='config_path')
set_parser = subparsers.add_parser("set", help="The core, set a wallpaper")
set_parser.set_defaults(subparser="set")
set_parser.add_argument(
    "wallpaper",
    help="The wallpaper to choose, availables: " + ", ".join(wallpapers.get_wallpapers()),
)
ls_parser = subparsers.add_parser('ls', help='Show the available wallpapers in the configured wallpapers folder')
ls_parser.set_defaults(subparser='ls')
ls_parser.add_argument(
    '-it',
    action='store_true',
    help='Show as bash iterable'
)
restore_parser = subparsers.add_parser('restore', help='Restore a selected wallpaper')
restore_parser.set_defaults(subparser='restore')

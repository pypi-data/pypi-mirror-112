from .resources.config import config
config.check(create=True)
from .cli.parser import parser
from .cli.log import error
from .commands.registry import registry


def main():
    args = parser.parse_args()
    if not 'subparser' in args:
        error('Nothing to do, use -h/--help to get help')
    registry[args.subparser](args)


if __name__ == '__main__':
    main()

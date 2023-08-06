from sys import stderr


def warn(message: str):
    print(f'Warn: {message}', file=stderr)


def error(message: str):
    print(f'Error: {message}', file=stderr)
    exit(1)


def success(message: str):
    print(f'Success: {message}')


def info(message: str):
    print(f'Info: {message}')

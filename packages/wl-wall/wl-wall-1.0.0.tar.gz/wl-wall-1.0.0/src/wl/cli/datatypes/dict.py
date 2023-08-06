from typing import Dict, TypeVar

V = TypeVar("V")


def display(data: Dict[str, V]):
    for key, val in data.items():
        print(' ', key, '->', val)
        print('-' * (len(f'{key} -> {val}') + 4))

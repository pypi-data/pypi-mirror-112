import argparse


def arguments(**kwargs) -> argparse.Namespace:
    return argparse.Namespace(**kwargs)

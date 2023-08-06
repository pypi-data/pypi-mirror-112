import argparse


class Command:
    def __init__(self, args: argparse.Namespace):
        self._argv = args
        self.meta()
        self.run()

    def meta(self):
        pass

    def run(self):
        pass

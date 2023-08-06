import argparse

class FloadModule:
    def init(self, ops):
        pass

    def add_arguments(self, parser:argparse.ArgumentParser):
        pass 


class Pipeline(FloadModule):
    def process(self, item):
        pass


class Source(FloadModule):
    def start(self):
        pass

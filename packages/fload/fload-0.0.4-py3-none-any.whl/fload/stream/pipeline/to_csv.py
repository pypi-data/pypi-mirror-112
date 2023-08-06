import argparse
import csv

from fload.base import Pipeline


class ToCSVProcessor(Pipeline):
    header_setted = False # whether header has been setted.
    writer = None
    f = None

    def init(self, ops):
        filepath = ops.file
        encoding = ops.encoding
        self.f = open(filepath, 'w', encoding=encoding, newline='')

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument("file")
        parser.add_argument('--encoding', default='UTF8')

    def process(self, item):
        if not self.header_setted:
            self.writer = csv.DictWriter(self.f, fieldnames=item.keys())
            self.writer.writeheader()
            self.header_setted = True

        self.writer.writerow(item)

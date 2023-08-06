from fload.stream import Source
import csv

class CSVSource(Source):
    csv_file = None

    def add_arguments(self, parser):
        parser.add_argument('csvfile')
        parser.add_argument('--encoding')

    def init(self, ops):
        self.csv_file = ops.csvfile
        self.encoding = ops.encoding or 'UTF8'

    def start(self):
        input_file = csv.DictReader(open(self.csv_file, encoding=self.encoding),)
        for row in input_file:
            yield row

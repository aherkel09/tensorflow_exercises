import csv, os
from fetch_data import DataFetcher

class ParWriter:
    def __init__(self):
        self.fetcher = DataFetcher()

    def write_all(self):
        for f in self.fetcher.files:
            self.write_file(self.read_file(f), f)

    def read_file(self, file):
        file_data = []

        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter=self.fetcher.delimiters[self.fetcher.ext])
            print(next(reader))

    def write_file(self, data, file):
        return
        
        
if __name__ == '__main__':
    par = ParWriter()
    par.write_all()

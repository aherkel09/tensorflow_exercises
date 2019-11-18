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
            next(reader) # skip headers
            for row in reader:
                file_data += self.read_row(row)

    def read_row(self, row):
        cols = self.fetcher.col_data
        fil = self.fetcher.filter
        
        if fil and row[fil['field']] not in fil['values']:
            return ''
        else:
            return [
                row[cols['Cumulative_Onset']],
                self.get_condition(row[cols['Data']]),
                row[cols['Duration']],
                1
                ]

    def get_condition(self, data):
        condition_file = self.fetcher.conditions['filepath']
        extension = '.' + condition_file.split('.')[1]
        with open(condition_file, 'r') as f:
            reader = csv.reader(f, delimiter=self.fetcher.delimiters[extension])
            next(reader)
            for row in reader:
                if row[0] == data:
                    print(data, row[1])
                    return row[1]

    def write_file(self, data, file):
        return
        
        
if __name__ == '__main__':
    par = ParWriter()
    par.write_all()

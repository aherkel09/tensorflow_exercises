import csv, os
from fetch_data import DataFetcher

class ParWriter:
    def __init__(self):
        self.fetcher = DataFetcher()

    def write_all(self):
        index = 1
        
        if not os.path.isdir('par_files'):
            os.mkdir('par_files')
            
        for f in self.fetcher.files:
            data = self.read_file(f)
            out_path = os.path.join('par_files', self.fetcher.output_file + str(index))
            self.write_file(data, out_path)
            index += 1

    def read_file(self, fname):
        file_data = []
        with open(fname, 'r') as f:
            reader = csv.reader(f, delimiter=self.fetcher.delimiters[self.fetcher.ext])
            next(reader) # skip headers
            for row in reader:
                trial_filter = self.fetcher.filter
                
                if len(row):
                    # only add data if trial type matches filter, or if there is no filter
                    if (trial_filter and row[trial_filter['field']] in trial_filter['values']) or not trial_filter:
                        file_data += [self.read_row(row)]

        return file_data

    def read_row(self, row):
            cols = self.fetcher.col_data
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
                    return row[1]

    def write_file(self, data, output):
        with open(output + '.par', 'w', newline='') as o:
            writer = csv.writer(o)
            writer.writerow(['Cumulative_Onset', 'Condition_Number_Code', 'Duration', 'Weight'])
            writer.writerows(data)
        
        
if __name__ == '__main__':
    par = ParWriter()
    par.write_all()

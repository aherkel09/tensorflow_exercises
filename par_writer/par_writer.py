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
            file_num = self.get_zeros(index)
            out_path = os.path.join('par_files', self.fetcher.output_file + file_num)
            self.write_file(data, out_path)
            index += 1
    
    def get_zeros(self, num):
        zeros = ''
        
        if num < 10:
            zeros = '00'
        elif num < 100:
            zeros = '0'
        
        return zeros + str(num)

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
        columns = self.fetcher.conditions['columns']
        
        extension = '.' + condition_file.split('.')[1]
        
        with open(condition_file, 'r') as f:
            reader = csv.reader(f, delimiter=self.fetcher.delimiters[extension])
            next(reader)
            
            for row in reader:
                if row[columns[0]] == data:
                    return row[columns[1]]
                

    def write_file(self, data, output):
        with open(output + '.par', 'w', newline='') as o:
            writer = csv.writer(o, delimiter='\t')
            writer.writerow(['Cumulative_Onset', 'Condition_Number_Code', 'Duration', 'Weight'])
            writer.writerows(data)
        
        
if __name__ == '__main__':
    par = ParWriter()
    par.write_all()

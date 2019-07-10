import codecs, csv, os

class ParWriter:
    def __init__(self):
        self.data = self.get_tsv_data()
        self.files = self.get_output_files()
    
    def get_tsv_data(self):
        data = {}
        
        run = 1
        while run <= 20:
            data[run] = self.get_run_data(run)
            run += 1
            
        return data

    def get_run_data(self, run):
        root_directory = os.getcwd() + '\\tsv_out'
        category_file = os.path.join(root_directory, 'living_nonliving-' + str(run) + '.tsv')

        unique_rows = 3 # number of unique rows of data in living_nonliving files
        run_data = {
            'Cululative_Onset': [[(36 + 24*n) for n in range(0,25)]]*unique_rows, # onsets per tsv data
            'Condition_Number_Code': self.get_codes(category_file),
            'Duration': [[15 for d in range(0,25)]]*unique_rows, # durations per tsv data
            'Weight': [[1 for w in range(0, 25)]]*unique_rows, # set all weights to 1
        }
        
        return run_data

    def get_codes(self, file):
        # get living_nonliving codes from file
        codes = []
        with open(file, 'rb') as tsv:
            reader = csv.reader(codecs.iterdecode(tsv, 'utf-8'), delimiter='\t')
            for row in reader:
                codes.append(row)
                        
        return codes

    def get_output_files(self):
        files = {}
        
        for run in self.data:
            files[run] = self.get_run_files(run)

        return files

    def get_run_files(self, run):
        files = []
        
        # format run for file output
        if run < 10:
            run = '00' + str(run)
        else:
            run = '0' + str(run)
        
        for row in self.rows_to_subjects():
            for subject in self.rows_to_subjects(row):
                filename = 'tsv_out\\FS_0' + subject + '\\bold\\' + run + '\\horikawa.par'
                filepath = os.path.join(os.getcwd(), filename)
                files.append((subject, filepath))
                
        return files

    def rows_to_subjects(self, row=None):
        # map data rows to subjects (based on tsv_in data)
        rows_to_subjects = {
            1: ['1', '2', '3'],
            2: ['4'],
            3: ['5']
        }

        if row:
            return rows_to_subjects[row]

        return rows_to_subjects

    def write_by_run(self):
        for run in self.data:
            for file in self.files[run]:
                with open(file[1], 'w', newline='') as par:
                    print('Writing data for subject ' + file[0] + ', run ' + str(run))
                    subject_data = self.get_subject_data(file[0], self.data[run])
                    row_data = self.get_row_data(subject_data)
                    
                    writer = csv.writer(par, delimiter='\t')
                    writer.writerow(self.data[run].keys()) # headers
                    writer.writerows(row_data)
                    
    def get_subject_data(self, subject, run_data):
        subject_data = []
        
        for row in self.rows_to_subjects():
            if subject in self.rows_to_subjects(row):
                for d in run_data:
                    subject_data.append(run_data[d][row-1])

        return subject_data

    def get_row_data(self, subject_data):
        same_length = [False for s in subject_data if len(s) != len(subject_data[0])]
        row_data = []

        if False not in same_length: # verify all rows have same length
            for i in range(len(subject_data[0])):
                line_data = []
                
                for s in subject_data:
                    line_data.append(s[i])
                    
                row_data.append(line_data)
                
        return row_data

if __name__ == '__main__':
    writer = ParWriter()
    writer.write_by_run()

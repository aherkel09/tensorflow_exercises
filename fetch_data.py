import csv, os

class DataFetcher:
    def __init__(self):
        self.files = []
        self.headers = []
        self.col_data = {}
        self.filter = {}
        self.conditions = {}
        self.output_file = None
        self.delimiters = {'.csv': ',', '.tsv': '\t'}
        self.dir = self.ask_dir()
        self.ext = self.ask_ext()

        self.get_files()
        self.get_data()

    def ask_dir(self):
        location = input('enter the directory containing your data files' +
        '(all files & subdirectories will be searched): ')

        if os.path.isdir(location):
            return location
        else:
            print('error: please enter a valid directory')
            return self.ask_dir()

    def ask_ext(self):
        ext = input('enter the extension of your data files (.csv, .tsv): ')
        if ext in ['.csv', '.tsv']:
            return ext
        else:
            print('error: please enter a supported file extension')
            return self.ask_ext()

    def get_files(self):
        for path, subdirs, files in os.walk(self.dir):
            for name in files:
                if name.endswith(self.ext):
                    self.add_to_files(os.path.join(path, name))

    def add_to_files(self, path):
        with open(path, 'r') as f:
            reader = csv.reader(f, delimiter=self.delimiters[self.ext])
            if self.match_headers(next(reader)):
                self.files += [path]
            else:
                raise ValueError(
                    'found nonmatching headers in file', path)

    def match_headers(self, headers):
        if not len(self.headers):
            self.headers = headers
            return True
        elif headers == self.headers:
            return True
        return False

    def get_data(self):
        print('found', len(self.files), 'files')
        print('columns:', self.headers)
        
        self.col_data['Cumulative_Onset'] = self.ask_col_name('onset')
        self.col_data['Duration'] = self.ask_col_name('duration')
        self.filter = self.ask_filter()
        self.conditions = self.ask_conditions()
        self.output_file = self.ask_output_file()

    def ask_col_name(self, col):
        name = input('enter the name of the ' + col + ' column: ')
        if name in self.headers:
            return name
        else:
            print('error: enter a valid column name')
            return self.ask_col_name(col)

    def ask_filter(self):
        action = input(
            'do you wish to (1) keep all trials or (2) filter by trial type? (1/2): ')
        if action == '2':
            return self.ask_trial_info()
        elif action == '1':
            return None # proceed
        else:
            print('error: please enter a valid choice')
            return self.ask_filter()

    def ask_trial_info(self):
        trial_col = input('enter the column containing the trial type info: ')
        if trial_col in self.headers:
            keep = input('enter the list of values you wish to keep: ')
            return {'field': trial_col, 'values': keep.split(', ')}
        else:
            print('error: enter a valid column name')
            return self.ask_trial_info()

    def ask_conditions(self):
        num_conditions = input('enter the number of conditions: ')
        num_conditions = int(num_conditions)
        return self.assign_conditions(num_conditions)
        
    def assign_conditions(self, num_conditions):
        if num_conditions == 1:
            return num_conditions
        else:
            return self.get_condition_file()

    def get_condition_file(self):
        path = input('enter the path to your condition file: ')
        if os.path.isfile(path):
            return {
                'filepath': path,
                'headers': self.read_condition_headers(path)
                }
        else:
            print('error: please enter a valid file path')
            return self.get_condition_file()
        
    def read_condition_headers(self, path):
        extension = path.split('.')[1]
        with open(path, 'r') as f:
            reader = csv.reader(f, delimiter=self.delimiters['.' + extension])
            return next(reader)

    def ask_output_file(self):
        return input('enter a base file name for your .par files (w/o extension): ')

if __name__ == '__main__':
    df = DataFetcher()
    df.get_data()
    
    print(df.col_data)
    print(df.output_file)
    

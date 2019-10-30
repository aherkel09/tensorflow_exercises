import glob, os, csv

from csv_by_subject import SearchSubjects
from writer import Writer

class SubjectCondenser():
    def __init__(self, data_dir, subjects_file, header_rows):
        self.data_dir = data_dir
        self.subjects_file = subjects_file
        self.header_rows = header_rows
        self.headers = {}
        self.data = {}

    def get_all_files(self):
        files = glob.glob(self.data_dir + '/*.csv')
        if self.subjects_file in files:
            files.remove(self.subjects_file)
            
        return files

    def get_subjects(self):
        subjects = []
        with open(self.subjects_file, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            subject_col = self.get_subject_col(headers)
            self.skip_headers(reader)

            for row in reader:
                index = headers.index(subject_col)
                subjects += [row[index]]

            return (subject_col, subjects)

    def get_subject_col(self, headers):
        print('Headers:', headers)
        col = input('Enter the name of the subject column: ')

        if col in headers:
            return col

        raise

    def skip_headers(self, reader):
        headers = []
        remaining = self.header_rows - 1 # already read the 1st row
        while remaining > 0:
            headers += next(reader)
            remaining -= 1

        return [headers]

    def search_file(self, filename, info):
        print('Searching', filename, '...')
        headers = []
        data = []
        with open(filename, 'r') as csv_in:
            reader = csv.reader(csv_in)
            headers += [next(reader)]
            col_num = headers[0].index(info[0])
            headers += self.skip_headers(reader)

            for row in reader:
                subject = row[col_num]
                if subject in info[1]:
                    data += [row]

            return (headers, data)

    def condense_all(self):
        files = self.get_all_files()
        subject_info = self.get_subjects()
        
        for f in files:
            search = self.search_file(f, subject_info)
            self.headers[f] = search[0]
            self.data[f] = search[1]

        self.writeout()

    def writeout(self):
        writer = Writer()
        path = self.data_dir + '/condensed/'
        os.mkdir(path)
        for d in self.data:
            filename = d.split('\\')[1].split('.')[0]
            print('Writing to', filename, '...')
            writer.write_to_file(path + filename + '_condensed.csv',
                                 self.headers[d],
                                 self.data[d]
                                 )
            
        print(
            '\nFinished. Check the condensed folder in the root' +
            'directory for data revisions.\n'
            )



def ask_data_dir():
    data_dir = input('Enter path to root directory: ')
    subjects_file = input('Enter path to subjects file: ')
    headers = input('How many header rows are in your data files?: ')
    
    if os.path.isdir(data_dir) and os.path.isfile(subjects_file):
        condenser = SubjectCondenser(data_dir, subjects_file, int(headers))
        condenser.condense_all()
    else:
        print('Please enter a valid directory path & subjects file.')
        ask_data_dir()
        
if __name__ == '__main__':
    print(
        'Please ensure all .csv files you wish to analyze are ' +
        'placed in the same directory.\nNote that all files in the ' +
        'directory will be analyzed.'
    )

    ask_data_dir()
    
        

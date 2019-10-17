import glob, os

from csv_by_subject import SearchSubjects
from writer import Writer

class SubjectCondenser():
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.files = self.get_all_files()
        self.subjects = []
        self.headers = {}
        self.data = {}
        
    def get_all_files(self):
        files = glob.glob(self.data_dir + '/*.csv')
        return files

    def search_file(self, index):
        file = self.files[index]
        print('Searching', file, '...')
        search = SearchSubjects(file)
        search.get_subject_column('subjectkey')
        search.get_all_subjects(headers=2)

        if index == 0:
            # set list of subjects from first file for matching
            self.subjects = list(search.subject_data.keys())
            print(
                '\nFound',
                str(len(self.subjects)),
                'subjects.\n'
                )

        return search

    def match_subjects(self, data):
        matched = {}
        unmatched = []
        for subject in self.subjects:
            if subject in data:
                matched[subject] = data[subject]
            else:
                unmatched += [subject]

        self.remove_unmatched_subjects(unmatched)      
        return matched

    def remove_unmatched_subjects(self, unmatched):
        for subj in unmatched:
            self.subjects.remove(subj)

    def condense_all(self):
        for i in range(len(self.files)):
            search = self.search_file(i)
            matched = search.subject_data
            matched = self.match_subjects(matched)

            self.headers[self.files[i]] = search.headers
            self.data[self.files[i]] = matched

        print(
            '\nCondensed to',
            str(len(list(matched.keys()))),
            'subjects.\n'
            )

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
    data_dir = str(input('Enter root directory: '))
    
    if os.path.isdir(data_dir):
        condenser = SubjectCondenser(data_dir)
        condenser.condense_all()
    else:
        print('Please enter a valid directory path.')
        ask_data_dir()
        
if __name__ == '__main__':
    print(
        'Please ensure all .csv files you wish to analyze are ' +
        'placed in the same directory.\nNote that all files in the ' +
        'directory will be analyzed.'
    )

    ask_data_dir()
    
        

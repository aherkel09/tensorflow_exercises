import csv, os

class SearchSubjects():
    def __init__(self, filename, header_rows, col_name):
        self.filename = filename
        self.header_rows = header_rows
        self.col_name = col_name
        self.col_num = None
        self.headers = []
        self.subjects= []

    def search(self):
        self.get_subject_column()
        self.get_all_subjects()

    def get_subject_column(self):
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)

            for i in range(len(headers)):
                if headers[i] == self.col_name:
                    self.col_num = i
                    return

            raise ValueError('"' + self.col_name + '" not found in headers.')

    def get_all_subjects(self):
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            rows = self.header_rows
            
            while rows > 0:
                self.headers += [next(reader)]
                rows -= 1

            for row in reader:
                subject = row[self.col_num]
                if subject not in self.subjects:
                    self.subjects += [subject]

def ask_subjects():
    filepath = input('Enter the path of the file you wish to search: ')
    header_rows = input('Enter the number of header rows in your file: ')
    subject_col = input('Enter the name of the subject ID column: ')
    
    if os.path.isfile(filepath):
        search = SearchSubjects(filepath, int(header_rows), subject_col)
        search.search()
        
if __name__ == '__main__':
    ask_subjects()
        
            

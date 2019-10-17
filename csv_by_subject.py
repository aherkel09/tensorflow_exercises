import csv

class SearchSubjects():
    def __init__(self, filename):
        self.filename = filename
        self.headers = []
        self.col_num = None
        self.subject_data = {}

    def get_subject_column(self, col_name):
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)

            for i in range(len(headers)):
                if headers[i] == col_name:
                    self.col_num = i
                    return

            raise ValueError('"' + col_name + '" not found in headers.')

    def get_all_subjects(self, headers=1):
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)

            while headers > 0:
                self.headers += [next(reader)]
                headers -= 1

            for row in reader:
                self.subject_data[row[self.col_num]] = row
            

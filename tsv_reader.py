import csv, os

class TSVReader:
    def __init__(self):
        self.root_directory = os.getcwd()
        self.tsv_files = self.get_tsv_files()

    def get_tsv_files(self):
        file_tree = {}
        for subdir, dirs, files in os.walk(self.root_directory): # check all files in all subdirectories
            for filename in files:
                if filename.endswith('.tsv') and subdir in file_tree.keys():
                    file_tree[subdir].append(os.path.join(subdir, filename))
                elif filename.endswith('.tsv'):
                    file_tree[subdir] = [os.path.join(subdir, filename)]

        return file_tree

    # create a single file for each column in tsv_files
    def create_column_files(self):
        for file_list in self.tsv_files.values():
            for file in file_list:
                self.write_column_data(file)

    def write_column_data(self, file):
        with open(file, 'r') as tsv:
            reader = csv.reader(tsv, delimiter='\t')
            columns = next(reader) # get column headers from first line

            for c in range(len(columns)):

                with open(columns[c] + '.tsv', 'a') as col_file:
                    data = []
                    writer = csv.writer(col_file)

                    for row in reader:
                        data.append(row[c])

                    writer.writerow(data)

if __name__ == '__main__':
    reader = TSVReader()
    reader.create_column_files()

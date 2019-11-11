import csv, os

class TSVReader:
    # create reader instance for files matching file_extension
    def __init__(self, root_dir):
        self.root_directory = root_dir
        self.tsv_files = {}

    #create file_tree object with format {subdir1: [file1, file2, ...], ...}
    def get_files(self):
        file_tree = {}

        # check all files in all subdirectories
        for subdir, dirs, files in os.walk(self.root_directory):
            for filename in files:
                if filename.endswith('.tsv') and subdir in file_tree.keys():
                    file_tree[subdir].append(os.path.join(subdir, filename))
                elif filename.endswith('.tsv'):
                    file_tree[subdir] = [os.path.join(subdir, filename)]

        self.tsv_files = file_tree
        
        return file_tree

    def get_column_headers(self, file):
        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            
            return next(reader)

    def get_column_number(self, columns, match):
        number = [c for c in range(len(columns)) if columns[c] == match]
        if len(number) == 1:
            return number[0]
        else:
            # if column not found or column header not unique
            print(match, 'matched', number)
            raise ValueError('Column was matched ' + len(number) + ' times.')

    def read_column_data(self, file, col_num):
        with open(file, 'r') as f:
            data = []
            reader = csv.reader(f, delimiter='\t')
            next(reader) # skip  header row

            for row in reader:
                # create list of column data
                data.append(row[col_num])

            return data

if __name__ == '__main__':
    reader = TSVReader('perceptionTest')
    reader.get_files()
    first_file = next(iter(reader.tsv_files.values()))[0]

    cols = reader.get_column_headers(first_file)
    stim_id = reader.get_column_number(cols, 'stim_id')
    data = reader.read_column_data(first_file, stim_id)

    print(data)

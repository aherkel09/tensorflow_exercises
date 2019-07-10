import csv, os

class TSVWriter:
    def __init__(self, out_file):
        self.out_file = 'tsv_out\\' + out_file
        self.root_directory = os.getcwd()
        self.filepath = os.path.join(self.root_directory, self.out_file)

    def request_overwrite(self):
        overwrite = input('Data exist at \n' + self.filepath + '\nOverwrite? (y/n): ')

        if overwrite == 'y':
            os.remove(self.filepath)
        else:
            raise Exception('Please move existing data files before proceeding.')

        return True

    def write_column_data(self, col_data):
        with open(self.out_file, 'a') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(col_data)

if __name__ == '__main__':
    writer = TSVWriter('writer_test.tsv')
    print('Initialized writer at', writer.out_file)

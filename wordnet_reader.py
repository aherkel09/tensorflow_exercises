import csv, os
from nltk.corpus import wordnet as wn

class WordnetReader:
    def __init__(self):
        self.root_directory = os.getcwd()
        self.offset_list = []
        self.tsv_files = self.get_tsv_files()

    def get_tsv_files(self):
        file_list = []
        for subdir, dirs, files in os.walk(self.root_directory): # check all files in all subdirectories
            for filename in files:
                if filename.endswith('.tsv'):
                    file_list.append(os.path.join(subdir, filename))

        return file_list

    def get_all_offsets(self):
        for file in self.tsv_files:
            file_offsets = self.get_file_offsets(file)
            for offset in file_offsets:
                if offset not in self.offset_list:
                    self.offset_list.append(offset)

        return self.offset_list

    def get_file_offsets(self, file):
        offsets = []
        with open(file, 'r') as tsv:
            tsv = csv.reader(tsv, delimiter='\t')
            offset_column = self.get_column_number(next(tsv)) # get offset column number from header row
            for row in tsv:
                if row[offset_column].isdigit() and row[offset_column] not in offsets:
                    offsets.append(int(row[offset_column]))

        return offsets

    def get_column_number(self, first_line):
        for col in range(len(first_line)):
            if first_line[col] == 'category_id':
                return col

        raise ValueError('"category_id" not found in', first_line)

if __name__ == '__main__':
    reader = WordnetReader()
    offset_list = reader.get_all_offsets()

    for offset in offset_list:
        synset = wn.synset_from_pos_and_offset('n', offset)
        print(synset.lemmas()[0].name())

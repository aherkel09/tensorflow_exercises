import csv, os
from nltk.corpus import wordnet as wn

class WordnetReader:
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

    def get_all_offsets(self):
        offsets = {}
        for subdir, file_list in self.tsv_files.items():
            subdir_offsets = []
            for file in file_list:
                file_offsets = self.get_file_offsets(file)
                subdir_offsets += [f for f in file_offsets if f not in subdir_offsets]
            offsets[subdir] = subdir_offsets

        offsets = self.compare_values(offsets) # make sure all subdirs have same offset values
        return offsets

    def get_file_offsets(self, file):
        offset_list = []
        with open(file, 'r') as tsv:
            tsv = csv.reader(tsv, delimiter='\t')
            offset_column = self.get_column_number(next(tsv)) # get offset column number from header row
            for row in tsv:
                if row[offset_column].isdigit() and int(row[offset_column]) not in offset_list:
                    offset_list.append(int(row[offset_column]))

        return offset_list

    def compare_values(self, offsets):
        compare_dir = None
        compare_offsets = []
        for o in offsets:
            if len(compare_offsets) == 0:
                compare_dir = o
                compare_offsets = offsets[o]
            elif offsets[o] != compare_offsets:
                print('\nError: Wordnet offsets in\n', compare_dir, '\ndo not match offsets in\n', o, '\n')
                raise ValueError('Wordnet Offsets Do Not Match')

        return compare

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

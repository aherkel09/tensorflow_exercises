import csv, os
from nltk.corpus import wordnet as wn

class WordnetReader:
    def __init__(self, root_dir, wordnet_col):
        self.root_directory = root_dir
        self.wordnet_col = wordnet_col
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
        offsets = []
        for subdir, file_list in self.tsv_files.items():
            subdir_offsets = []
            for file in file_list:
                file_offsets = self.get_file_offsets(file)
                
                for f in file_offsets:
                    if f not in subdir_offsets:
                        subdir_offsets += [f]
                
            for s in subdir_offsets:
                if s not in offsets:
                    offsets += [s]

        return offsets

    def get_file_offsets(self, file):
        offset_list = []
        with open(file, 'r') as tsv:
            tsv = csv.reader(tsv, delimiter='\t')
            offset_column = self.get_column_number(next(tsv)) # get offset column number from header row
            for row in tsv:
                offset = row[offset_column].split('.')[0]
                if offset.isdigit() and offset not in offset_list:
                    offset_list.append(int(offset))

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

        return compare_offsets

    def get_column_number(self, first_line):
        for col in range(len(first_line)):
            if first_line[col] == self.wordnet_col:
                return col

        raise ValueError(self.wordnet_col, 'not found in', first_line)

if __name__ == '__main__':
    reader = WordnetReader('imageryTest', 'category_id')
    offsets = reader.get_all_offsets()
    print(len(offsets))

    with open('imagery_offsets.csv', 'w', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(['wordnet_offset', 'wordnet_lemma_name', 'wordnet_definition'])
        
        for offset in offsets:
            synset = wn.synset_from_pos_and_offset('n', int(offset))
            writer.writerow([offset, synset.lemmas()[0].name(), synset.definition()])

import codecs, csv, os
from nltk.corpus import wordnet as wn

class WordnetRowReader:
    def __init__(self):
        self.root_directory = os.getcwd()
        self.tsv_files = self.get_run_files()

    def get_run_files(self):
        file_tree = {}
        for subdir, dirs, files in os.walk(self.root_directory + '\\tsv_out'): # check all files in all subdirectories
            for filename in files:
                if filename.startswith('category_id'):
                    run = filename.split('-')[1].replace('.tsv', '')
                    file_tree[run] = os.path.join(subdir, filename)

        return file_tree

    def get_all_offsets(self):
        offsets = {}
        for run, run_file in self.tsv_files.items():
            file_offsets = self.get_file_offsets(run_file)
            offsets[run] = file_offsets

        return offsets

    def get_file_offsets(self, file):
        offset_list = []
        with open(file, 'rb') as tsv:
            tsv = csv.reader(codecs.iterdecode(tsv, 'utf-8'), delimiter='\t')
            for row in tsv:
                row_list = []
                for offset in row:
                    if offset.isdigit() and int(offset) not in row_list:
                        row_list.append(int(offset))
                offset_list.append(row_list)

        return offset_list

    def find_duplicates(self, offsets):
        duplicates = {}
        for run in offsets:
            check = None
            row_count = 1
            for row in offsets[run]:
                if check and row == check:
                    if run in duplicates.keys():
                        duplicates[run].append(row_count)
                    else:
                        duplicates[run] = [row_count]
                elif not check:
                    check = row
                row_count += 1

        return duplicates

if __name__ == '__main__':
    reader = WordnetRowReader()
    run_offsets = reader.get_all_offsets()
    print(reader.find_duplicates(run_offsets))
'''
    for run in run_offsets:
        for row in run_offsets[run]:
            print('\nRow', row)
            for offset in range(len(row)):
                print('Offset', offset)
                #synset = wn.synset_from_pos_and_offset('n', offset)
                #print(synset.lemmas()[0].name())
'''

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

    def drop_duplicate_runs(self, offsets):
        duplicates = []
        check = 1

        while check < 20:
            for run in offsets:
                if offsets[run] == offsets[str(check)] and run != str(check):
                    duplicates.append(run)
            check += 1

        for d in duplicates:
            offsets.pop(d)

        return offsets

    def drop_duplicate_rows(self, offsets):
        for run in offsets:
            check = None
            row_count = 0
            for row in offsets[run]:
                if check and row == check:
                    before = [offsets[run][r] for r in range(len(offsets[run])) if r < row_count]
                    after = [offsets[run][r] for r in range(len(offsets[run])) if r >= row_count and offsets[run][r] != check]
                    offsets[run] = before + after
                elif not check:
                    check = row
                row_count += 1

        return offsets

if __name__ == '__main__':
    reader = WordnetRowReader()
    offsets = reader.get_all_offsets()
    offsets = reader.drop_duplicate_runs(offsets)
    offsets = reader.drop_duplicate_rows(offsets)

    for run in offsets:
        for row in range(len(offsets[run])):
            print('\nRun:', run, 'Row:', row)
            lemmas = []
            for offset in offsets[run][row]:
                synset = wn.synset_from_pos_and_offset('n', offset)
                lemmas.append(synset.lemmas()[0].name())
            print(lemmas)

            for x in range(len(lemmas)):
                for l in range(len(lemmas)):
                    if x != l and lemmas[l] == lemmas[x]:
                        print('duplicate!')

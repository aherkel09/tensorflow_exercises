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
            run_list = []
            
            for row in offsets[run]:
                if row not in run_list:
                    run_list.append(row)

            offsets[run] = run_list
            
        return offsets

    def get_lemmas(self, offsets):
        lemmas = {}
        for run in offsets:
            row_list = []
            for row in offsets[run]:
                lemma_list = []
                for offset in row:
                    synset = wn.synset_from_pos_and_offset('n', offset)
                    lemma_list.append(synset.lemmas()[0].name())
                row_list.append(lemma_list)
            lemmas[run] = row_list

        return lemmas

    def write_lemmas(self, lemmas):
        for l in lemmas:
            with open('tsv_out\\lemmas-' + l + '.tsv', 'a') as tsv:
                writer = csv.writer(tsv, delimiter='\t')
                writer.writerows(lemmas[l])
    

if __name__ == '__main__':
    reader = WordnetRowReader()
    offsets = reader.get_all_offsets()
    offsets = reader.drop_duplicate_runs(offsets)
    offsets = reader.drop_duplicate_rows(offsets)
    
    lemmas = reader.get_lemmas(offsets)
    reader.write_lemmas(lemmas)
    

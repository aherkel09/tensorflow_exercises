import csv, os
from nltk.corpus import wordnet as wn

class WordnetReader:
    def __init__(self):
        self.root_directory = os.getcwd()
        self.offset_list = []
        self.tsv_files = self.get_tsv_files()

    def get_tsv_files(self):
        file_list = []
        for subdir, dirs, files in os.walk(self.root_directory):
            for filename in files:
                if filename.endswith('.tsv'):
                    file_list.append(os.path.join(subdir, filename))

        return file_list

    def get_all_offsets(self):
        for file in self.tsv_files:
            file_offsets = self.get_wordnet_offsets(file)
            for offset in file_offsets:
                if offset not in self.offset_list:
                    self.offset_list.append(offset)

        return self.offset_list

    def get_wordnet_offsets(self, file):
        offsets = []
        with open(file, 'r') as tsv:
            tsv = csv.reader(tsv, delimiter='\t')
            next(tsv) # skip header row
            for row in tsv:
                if row[4].isdigit() and row[4] not in offsets:
                    offsets.append(int(row[4]))

        return offsets

if __name__ == '__main__':    
    reader = WordnetReader()
    offset_list = reader.get_all_offsets()

    for offset in offset_list:
        synset = wn.synset_from_pos_and_offset('n', offset)
        print(synset.lemmas()[0].name())

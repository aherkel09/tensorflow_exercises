import csv, os
from nltk.corpus import wordnet as wn

class WordnetReader:
    def __init__(self, root_dir, wordnet_col):
        self.root_directory = root_dir
        self.wordnet_col = wordnet_col
        self.offsets = self.get_all_offsets()

    def get_all_offsets(self):
        offsets = {}
        for subdir, dirs, files in os.walk(self.root_directory): # check all files in all subdirectories
            for file in [f for f in files if f.endswith('.tsv')]: # search .tsv files only
                filepath = os.path.join(subdir, file)
                file_offsets = self.get_file_offsets(filepath)
                
                for offset in [f for f in file_offsets if f not in offsets.keys()]:
                    offsets[offset] = self.get_wordnet_info(offset)
        
        return offsets

    def get_file_offsets(self, file):
        offset_list = []
        with open(file, 'r') as tsv:
            tsv = csv.reader(tsv, delimiter='\t')
            wordnet_column = self.get_column_number(next(tsv))
            
            if wordnet_column:
                for row in tsv:
                    offset = row[wordnet_column].split('.')[0]
                    if offset != 'n/a':
                        offset_list.append(offset)

                return offset_list
            
        return None

    def get_column_number(self, headers):
        for col in range(len(headers)):
            if headers[col] == self.wordnet_col:
                return col

        raise ValueError(self.wordnet_col, 'not found in', headers)
    
    def get_wordnet_info(self, offset):                    
        synset = wn.synset_from_pos_and_offset('n', int(offset))
        lemma = (synset.lemmas()[0].name())
        definition = (synset.definition())
            
        return [offset, lemma, definition]
    
    def write_out(self):
        with open('offsets\\perceptionTraining_offsets.csv', 'w', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow(['wordnet_offset', 'wordnet_lemma', 'wordnet_definition', 'living_nonliving'])
            
            for o in self.offsets:
                writer.writerow(self.offsets[o])
            
    
    def search_offset(self, search):
        search_results = {}
        for file in self.offsets:
            search_results[file] = []
            for o in range(len(self.offsets[file])):
                if self.offsets[file][o] == search:
                    search_results[file] += [o]
        
        return search_results
    
if __name__ == '__main__':
    reader = WordnetReader('C:/Users/aherk/ccn_scripts/horikawa/perceptionTraining', 'stim_id')
    reader.write_out()
    

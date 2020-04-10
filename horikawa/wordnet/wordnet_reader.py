import csv, os
from nltk.corpus import wordnet as wn

class WordnetReader:
    def __init__(self, root_dir, wordnet_col):
        self.root_directory = root_dir
        self.wordnet_col = wordnet_col
        self.offsets = self.get_all_offsets()
        # [print(self.offsets[o]) for o in self.offsets]

    def get_all_offsets(self):
        file_tree = {}
        for subdir, dirs, files in os.walk(self.root_directory): # check all files in all subdirectories
            for file in [f for f in files if f.endswith('.tsv')]: # search .tsv files only
                filepath = os.path.join(subdir, file)
                file_offsets = self.get_file_offsets(filepath)
                
                if file_offsets:
                    file_tree[filepath] = file_offsets
        
        return file_tree

    def get_file_offsets(self, file):
        offset_list = []
        with open(file, 'r') as tsv:
            tsv = csv.reader(tsv, delimiter='\t')
            wordnet_column = self.get_column_number(next(tsv))
            
            if wordnet_column:
                for row in tsv:
                    offset = row[wordnet_column].split('.')[0]
                    offset_list.append(offset)

                return offset_list
            
        return None

    def get_column_number(self, headers):
        for col in range(len(headers)):
            if headers[col] == self.wordnet_col:
                return col

        raise ValueError(self.wordnet_col, 'not found in', headers)
    
    def search_offset(self, search):
        search_results = {}
        for file in self.offsets:
            search_results[file] = []
            for o in range(len(self.offsets[file])):
                if self.offsets[file][o] == search:
                    search_results[file] += [o]
        
        return search_results
    
if __name__ == '__main__':
    reader = WordnetReader('C:/Users/aherk/ccn_scripts/horikawa/perceptionTest', 'stim_id')
    results = reader.search_offset('2824058')
    [print(r, results[r]) for r in results]
    

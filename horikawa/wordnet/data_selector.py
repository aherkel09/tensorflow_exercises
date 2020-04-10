import csv, os, sqlite3, random
from wordnet_reader import WordnetReader

class DataSelector:
    def __init__(self):
        self.conn = sqlite3.connect('offsets/offsets.db')
        self.cursor = self.conn.cursor()
        self.living, self.nonliving = self.get_data('1'), self.get_data('2')
        self.least_items = min(len(self.living), len(self.nonliving)) # used to make equal-length lists
    
    def get_data(self, value):
        return self.cursor.execute('''
                SELECT wordnet_offset, wordnet_lemma_name 
                FROM perception_offsets WHERE living_nonliving=?;
            ''', (value)).fetchall()
        
    def random_item(self, data_list):
        random.shuffle(data_list) # randomize list before slicing
        return data_list[:self.least_items][
            random.randint(0, self.least_items - 1) # access random index
        ]
                    
    def random_pair(self):
        return (
            self.random_item(self.living),
            self.random_item(self.nonliving)
        )
    
    def unique_pair(self, check, existing):
        
        first_unique = check[0][0] not in [e[0][0] for e in existing]
        second_unique = check[1][0] not in [e[1][0] for e in existing]
        
        return first_unique and second_unique
    
    def get_x_pairs(self, x):
        pairs = []
        
        while len(pairs) < x:
            new_pair = self.random_pair()
            if self.unique_pair(new_pair, pairs):
                pairs += [new_pair]
        
        return pairs
    
    def find_in_data(self, offset):
        reader = WordnetReader(
            'C:/users/aherk/ccn_scripts/horikawa/perceptionTest',
            'stim_id'
        )
        
        return reader.search_offset(str(offset))
    
    def map_to_series(self, pairs):
        series_map = {}
        
        for p in pairs:
            series_map[p] = [
                self.find_in_data(p[0][0]),
                self.find_in_data(p[1][0])
                ]
        
        return series_map
        
if __name__ == '__main__':
    selector = DataSelector()
    five_pairs = selector.get_x_pairs(5)    
    map = selector.map_to_series(five_pairs)
    
    with open('selected.txt', 'w') as f:
        for pair in map:
            counter = 0
            for i in map[pair]:
                f.write(str(pair[counter]) + ':\n')
                counter += 1
                for file in i:
                    f.write('\t' + file[50:] + ': ' + str(i[file]) + '\n')
                
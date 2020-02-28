import sqlite3, random

class DataSelector:
    def __init__(self):
        self.conn = sqlite3.connect('offsets/offsets.db')
        self.cursor = self.conn.cursor()
        self.living, self.nonliving = self.get_data('1'), self.get_data('2')
        self.least_items = min(len(self.living), len(self.nonliving)) - 1 # used to make equal-length lists
    
    def get_data(self, value):
        query = str('''
                    SELECT wordnet_offset, wordnet_lemma_name 
                    FROM perception_offsets 
                    WHERE living_nonliving="value";
                ''').replace('value', value)
        
        return self.cursor.execute(query).fetchall()
            
    def random_pair(self):
        shuffled_living = random.shuffle(self.living)[:self.least_items]
        random_living = shuffled_living[random.randint(0, self.least_items)]
        
        shuffled_nonliving = random.shuffle(self.nonliving)[:self.least_items]
        random_nonliving = shuffled_nonliving[random.randint(0, self.least_items)]
        
        return (random_living, random_nonliving)
    
    def get_x_pairs(x):
        pairs = []
        
        for i in range(x):
            pairs += [self.random_pair]
        
        return pairs
        

if __name__ == '__main__':
    selector = DataSelector()
    
    # test random_pair()
    print(selector.random_pair())
        
    # test get_x_pairs()
    print(selector.get_x_pairs(5))

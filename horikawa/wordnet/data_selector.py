import sqlite3, random

class DataSelector:
    def __init__(self):
        self.conn = sqlite3.connect('offsets/offsets.db')
        self.cursor = self.conn.cursor()
        self.living, self.nonliving = self.get_data()
    
    def get_data(self):
        living = self.cursor.execute('''
            SELECT wordnet_offset, wordnet_lemma_name 
            FROM perception_offsets WHERE living_nonliving="1";
        ''').fetchall()
        
        nonliving = self.cursor.execute('''
            SELECT wordnet_offset, wordnet_lemma_name 
            FROM perception_offsets WHERE living_nonliving="2";
        ''').fetchall()
        
        return living, nonliving
    
    def random_pair(self):
        return

if __name__ == '__main__':
    selector = DataSelector()
    print(selector.living)
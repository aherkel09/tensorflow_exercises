import sqlite3, json
from queries import Queries

class MegaQuery:
    def __init__(self, db_file):
        self.megaquery = ''
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.queries = {}
        self.temptables = []
        self.mastertable = ['mrin', 'mrinback02_temp']
    
    def start(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        print('Connected to database', self.db_file)
        
    def create_tables(self):
        print('Creating temporary tables from queries...')
        self.queries = Queries()
        for q in self.queries.all:
            tempname = q + '_temp'
            self.cursor.execute('CREATE TEMPORARY TABLE ' + 
                                tempname + ' AS ' + self.queries.all[q][1])
            
            if tempname != self.mastertable[1]:
                self.temptables += [tempname]
    
    def build_the_big_one(self):
        print('Building MegaQuery...')
        megaquery = ('SELECT mrin.subjectkey FROM ' + 
                     self.mastertable[1] + ' ' + self.mastertable[0])
        for t in self.temptables:
            tablename = t.split('_')[0]
            megaquery += self.add_join(t, self.queries.all[tablename][0])
        self.megaquery = megaquery
        
    def add_join(self, tablename, varname):
        # join temptable to mrinback02
        join = (' JOIN ' + tablename + ' ' + varname + 
                ' ON ' + varname + '.subjectkey=mrin.subjectkey')
        return join
    
    def execute(self):
        try:
            print('\nAttempting to execute MegaQuery:', self.megaquery, sep='\n')
            self.cursor.execute(self.megaquery)
            self.output_result()
        except Exception as e:
            print(e)
            raise ValueError('Could not execute MegaQuery.')
        
    def output_result(self):
        result = self.cursor.fetchall()
        print('\nResult:', len(result), 'Subjects')
        

if __name__ == '__main__':
    megaquery = MegaQuery('abcd.db')
    megaquery.start()
    megaquery.create_tables()
    megaquery.build_the_big_one()
    megaquery.execute()
    
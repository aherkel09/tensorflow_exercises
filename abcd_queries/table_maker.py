import sqlite3
from megaquery import MegaQuery

class TableMaker:
    def __init__(self, subject_file, db):
        self.subject_file = subject_file
        self.db = db
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
    
    def get_tables(self):
        tables = []
        tablenames = self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table";').fetchall()
        for t in tablenames:
            tables += [t[0]]
        
        return tables
    
    def megaquery(self):
        megaquery = MegaQuery(self.db)
        query_result = megaquery.run_all()
        return query_result
    
    def make_tables(self):
        data = self.megaquery()
        tables = self.get_tables()
        
        for t in tables:
            t += '_condensed' # tablenames for output
        
        

if __name__ == '__main__':
    tablemaker = TableMaker('subjects.csv', 'abcd.db')
    tablemaker.make_tables()
        
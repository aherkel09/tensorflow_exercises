import sqlite3, csv, os
from queries import Queries

class MegaQuery:
    def __init__(self, db_file):
        self.megaquery = ''
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.results = None
        self.queries = {}
        self.master_table = 'verified_t1_t2'
        self.temp_tables = []
        
    
    def start(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.results = open('megaquery_results.txt', 'w')
        self.results.write('Connected to database ' + self.db_file + '\n')
        
        
    def create_tables(self):
        self.results.write('\nCreating temporary tables from queries...')
        self.queries = Queries()
        
        for q in self.queries.all:
            self.results.write('\n' + self.queries.all[q][1] + '\n')
            self.cursor.execute('CREATE TEMPORARY TABLE ' + 
                                q + '_temp AS ' + self.queries.all[q][1])
            
            if q != self.master_table:
                self.temp_tables += [q]
                
    
    def build_the_big_one(self):
        self.results.write('\nBuilding MegaQuery...\n')
        megaquery = ('''
                        CREATE TEMPORARY TABLE subjects AS
                        SELECT veri.subjectkey FROM verified_t1_t2 veri
                    ''')
        
        for t in self.temp_tables:
            megaquery += self.add_join(t, self.queries.all[t][0], 'veri')
            
        self.megaquery = megaquery
        
        
    def add_join(self, tablename, varname, join_to):
        # join temp_table to master_table
        join = (' JOIN ' + tablename + '_temp ' + varname + 
                ' ON ' + varname + '.subjectkey=' + join_to + '.subjectkey')
        
        return join
    
    
    def execute(self):
        try:
            self.results.write('\nAttempting to execute MegaQuery:\n\n' + self.megaquery + '\n')
            self.cursor.execute(self.megaquery)
            self.cursor.execute('SELECT * FROM subjects')
            self.results.write('\nSuccess. Found ' +
                               str(len(self.cursor.fetchall())) +
                               ' subjects.\n')
            self.output_results()
        except Exception as e:
            print(e)
            raise ValueError('Could not execute MegaQuery.')
                

    def create_new_table(self, table):
        new_table = table + '_filtered'
        subjects = 'SELECT subjectkey FROM subjects'
        query = 'SELECT * FROM ' + table + ' WHERE subjectkey IN (' + subjects + ');'
        create_table = 'CREATE TEMPORARY TABLE ' + new_table + ' AS ' + query
        self.results.write('\n' + create_table + '\n')
        self.cursor.execute(create_table)
        self.write_results(new_table)
        

    def write_results(self, table):
        self.cursor.execute('SELECT * FROM ' + table)
        columns = [d[0] for d in self.cursor.description]
        data = self.cursor.fetchall()
        with open('abcd_data/filtered/' + table + '.csv', 'w', newline='\n') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(columns)
            writer.writerows(data)


    def output_results(self):
        self.results.write('\nFiltering data by subject...\n')
        tables = [t[0] for t in self.cursor.execute('''
                        SELECT name FROM sqlite_master
                        WHERE type="table";
                        ''').fetchall()]

        for t in tables:
            if t != 'abcd' and '_temp' not in t:
                self.create_new_table(t)

        self.results.write('\nMegaQuery complete!')
        self.results.close()
        

if __name__ == '__main__':
    megaquery = MegaQuery('abcd.db')
    megaquery.start()
    megaquery.create_tables()
    megaquery.build_the_big_one()
    megaquery.execute()
    

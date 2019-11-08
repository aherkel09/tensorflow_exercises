import sqlite3, json, csv
from queries import Queries

class MegaQuery:
    def __init__(self, db_file):
        self.megaquery = ''
        self.db_file = db_file
        self.conn = None
        self.cursor = None
        self.results = None
        self.queries = {}
        self.temptables = []
        
    
    def start(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.results = open('megaquery_results.txt', 'w')
        self.results.write('Connected to database ' + self.db_file)
        
        
    def create_tables(self):
        self.results.write('\nCreating temporary tables from queries...')
        self.queries = Queries()
        
        for q in self.queries.all:
            self.results.write(self.queries.all[q][1])
            self.cursor.execute('CREATE TEMPORARY TABLE ' + 
                                q + '_temp AS ' + self.queries.all[q][1])
            
            if q != 'mrinback02':
                self.temptables += [q]
                
    
    def build_the_big_one(self):
        self.results.write('\nBuilding MegaQuery...')
        megaquery = ('''
                        CREATE TEMPORARY TABLE subjects AS
                        SELECT mrin.subjectkey FROM mrinback02_temp mrin
                    ''')
        
        for t in self.temptables:
            megaquery += self.add_join(t, self.queries.all[t][0], 'mrin')
            
        self.megaquery = megaquery
        
        
    def add_join(self, tablename, varname, join_to):
        # join temptable to mrinback02
        join = (' JOIN ' + tablename + '_temp ' + varname + 
                ' ON ' + varname + '.subjectkey=' + join_to + '.subjectkey')
        
        return join
    
    
    def execute(self):
        try:
            self.results.write('\nAttempting to execute MegaQuery:\n' + self.megaquery)
            self.cursor.execute(self.megaquery)
            self.cursor.execute('SELECT * FROM subjects')
            self.results.write('\nSuccess. Found ' +
                               str(len(self.cursor.fetchall())) +
                               ' subjects.')
            self.output_results()
        except Exception as e:
            print(e)
            raise ValueError('Could not execute MegaQuery.')
                

    def create_new_table(self, table):
        new_table = table + '_filtered'
        subjects = 'SELECT subjectkey FROM subjects'
        query = 'SELECT * FROM ' + table + ' WHERE subjectkey IN (' + subjects + ');'
        create_table = 'CREATE TEMPORARY TABLE ' + new_table + ' AS ' + query
        self.results.write(create_table)
        self.cursor.execute(create_table)
        self.write_results(new_table)
        

    def write_results(self, table):
        self.cursor.execute('SELECT * FROM ' + table)
        columns = [d[0] for d in self.cursor.description]
        data = self.cursor.fetchall()
        
        with open('/ccn_scripts/abcd_data/' + table + '.csv', 'w', newline='\n') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(columns)
            writer.writerows(data)


    def output_results(self):
        self.results.write('\nFiltering data by subject...')
        tables = [t[0] for t in self.cursor.execute('''
                        SELECT name FROM sqlite_master
                        WHERE type="table";
                        ''').fetchall()]

        for t in tables:
            if t not in ['abcd', 'subjects'] and '_temp' not in t:
                self.create_new_table(t)

        self.results.write('\nMegaQuery complete!')
        self.results.close()
        

if __name__ == '__main__':
    megaquery = MegaQuery('abcd.db')
    megaquery.start()
    megaquery.create_tables()
    megaquery.build_the_big_one()
    megaquery.execute()
    

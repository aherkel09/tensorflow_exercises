import csv, os, pandas, sqlite3

class CSVToSQLite:
    def __init__(self, data_dir, db_file):
        self.data_dir = data_dir
        self.db_file = db_file
        self.conn = None
        self.cur = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cur = self.conn.cursor()

    def read_by_file(self):
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.csv'):
                print('Exporting data from', filename, '...')
                self.write_to_database(filename)
        print('Finished.')         
            
    def write_to_database(self, filename):
        tablename = filename.split('.')[0]
        data = pandas.read_csv(os.path.join(self.data_dir, filename), low_memory=False)
        data.to_sql(tablename, self.conn, if_exists='replace')

def ask_data_info():
    data_dir = str(input(
        'Enter .csv data directory (all files will be searched): '
    ))
    db_file = str(input('Enter .db file path: '))
    
    if os.path.isdir(data_dir) and os.path.isfile(db_file):
        return (data_dir, db_file)
    else:
        print('Something went wrong. Please verify file locations.')
        ask_data_dir()

if __name__ == '__main__':
    info = ask_data_info()
    csvsql = CSVToSQLite(info[0], info[1])
    csvsql.connect()
    csvsql.read_by_file()
    csvsql.conn.close()

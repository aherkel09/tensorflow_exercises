import sqlite3, csv

def query():
    conn = sqlite3.connect('abcd.db')
    c = conn.cursor()

    tables = get_tables(c)
    print(str(tables) + '\n\n')

    for table in [t for t in tables if "_filtered" in t]:
        c.execute('DROP TABLE ' + table)

    c.execute('DROP TABLE subjects')  
    print(get_tables(c))

def get_tables(c):
    return [t[0] for t in c.execute('''
        SELECT name FROM sqlite_master
        WHERE type="table";
    ''')]

def match_files():
    r_one = []
    r_two = []
    
    with open('ehis01_filtered.csv', 'r') as f_one:
        r_one = [r[1:] for r in csv.reader(f_one)]

    with open('/ccn_scripts/abcd_data/ehis01.csv', 'r') as f_two:
        r_two = [r for r in csv.reader(f_two)]

    print(len(r_one) == len(r_two))

if __name__ == '__main__':
    print('starting...')
    query()

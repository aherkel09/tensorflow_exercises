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
    
    with open('/ccn_scripts/abcd_data/ehis01_filtered.csv', 'r') as f_one:
        r_one = [r[1:] for r in csv.reader(f_one)]

    with open('/ccn_scripts/abcd_data/fastqc01_filtered.csv', 'r') as f_two:
        r_two = [r[1:] for r in csv.reader(f_two)]

    return (r_one, r_two)

def num_unique():
    data = match_files()
    first_subjects = []
    second_subjects = []
    
    for d in data[0]:
        if d[3] not in first_subjects:
            first_subjects += [d[3]]

    for d in data[1]:
        if d[3] not in second_subjects:
            second_subjects += [d[3]]

    print(len(first_subjects))
    print(len(second_subjects))
    print(first_subjects == second_subjects)

if __name__ == '__main__':
    print('starting...')
    num_unique()

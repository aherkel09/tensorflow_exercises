import sqlite3

conn = sqlite3.connect('abcd.db')
cursor = conn.cursor()

query = '''
            SELECT subjectkey FROM fastqc01 
            WHERE ftq_series_id LIKE '%nBack%' 
            AND ftq_complete=1 AND ftq_quality=1 
            AND ftq_recalled=0 AND ftq_usable=1 
            AND (ftq_notes LIKE '' OR ftq_notes IS NULL)
            ORDER BY subjectkey;
        '''

cursor.execute(query)
results = cursor.fetchall()

print('found', len(results), 'potential subjects.')

usable_runs = {}

for id in results:
    if id not in usable_runs:
        usable_runs[id] = 1
    else:
        usable_runs[id] += 1
        
verified = [(u) for u in usable_runs if usable_runs[u] == 4]

print('verified', len(verified), 'subjects.')

get_tables = '''
                SELECT name FROM sqlite_master
                WHERE type='table'
            '''

cursor.execute(get_tables)
tables = [c[0] for c in cursor.fetchall()]

if 'verified_t1_t2' not in tables:
    cursor.execute('CREATE TABLE verified_t1_t2(subjectkey)')
    conn.commit()

def insert_subjects(ids):
    insert = '''
                INSERT INTO verified_t1_t2(subjectkey) 
                VALUES(?)
            '''
    
    cursor.executemany(insert, ids)
    print(cursor.rowcount, 'records created.')
    conn.commit()

insert_subjects(verified)
cursor.close()
    
    
    
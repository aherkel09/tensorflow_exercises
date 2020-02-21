import sqlite3

conn = sqlite3.connect('abcd.db')
c = conn.cursor()

all_ids = '''
            SELECT * FROM verified_t1_t2
        '''

c.execute(all_ids)
id_list = [id[0] for id in c.fetchall()]

def check_unique(ids):
    found = []
    for i in ids:
        if i not in found:
            found += [i]
        else:
            return False
    
    return True

print(check_unique(id_list))
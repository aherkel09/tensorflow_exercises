import sqlite3

def compare():
    conn = sqlite3.connect('offsets.db')
    c = conn.cursor()

    imagery = c.execute('''
                            SELECT wordnet_offset
                            FROM imagery_offsets
                        ''').fetchall()
    
    imagery = sorted([i[0] for i in imagery])
    

    perception = c.execute('''
                            SELECT wordnet_offset
                            FROM perception_offsets
                            ''').fetchall()
    
    perception = sorted([p[0] for p in perception])

    return imagery == perception

if __name__ == '__main__':
    print('imagery offsets match perception offsets?', compare())

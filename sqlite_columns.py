import sqlite3

class SQLiteColumns:
    def __init__(self, tablename):
        self.test = False
        self.conn = sqlite3.connect('abcd.db')
        self.cursor = self.conn.cursor()
        self.tablename = tablename

    def reset_cursor(self):
        self.cursor = self.conn.cursor()

    def get_columns(self):
        self.cursor.execute('SELECT * FROM ' + self.tablename)
        return self.cursor.description

    def list_columns(self):
        for c in self.get_columns():
            print(c[0])

    def match_columns(self, match):
        num_results = 0
        for c in self.get_columns():
            if (match in c[0]):
                print(c[0])
                num_results += 1
            elif self.test:
                print(match, 'not in', c[0])
                
        print(str(num_results) + ' results found.')
        
def ask_table():
    table = str(input('Enter the table you wish to search: '))
    try:
        sqlc = SQLiteColumns(table)
        select_action(sqlc, ask_next_step())
    except Exception as e:
        print(e)
        print("Error: Please enter a valid table name")
        ask_table()

def ask_next_step():
    print('What would you like to do?', '1: See all columns',
          '2: Look for a specific column', sep='\n')
    next_step = input('Enter option number: ')
    return int(next_step)

def select_action(sqlc, action):
    if action == 1:
        sqlc.list_columns()
    elif action == 2:
        search = get_search().lower()
        sqlc.match_columns(search)

def get_search():
    return str(input('Enter all or part of the column name: '))

if __name__ == '__main__':
    ask_table()

import sqlite3

conn = sqlite3.connect('abcd.db')
c = conn.cursor()

res = c.execute("SELECT name FROM sqlite_master WHERE type='table';")

for name in res:
    print(name[0])

c.execute("SELECT * FROM ehis01")
while True:
    batch = c.fetchmany(5)
    print(batch)
    if not batch:
        break

conn.close()

import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

c.execute("""SELECT * FROM users""")
print('\nusers:',c.fetchall())

c.execute("""SELECT * FROM habits""")
print('\nhabits:',c.fetchall())

c.execute("""SELECT * FROM checkins""")
print('\ncheckins:',c.fetchall())

conn.commit()
conn.close()
import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

c.execute("""DROP TABLE users""")

c.execute("""DROP TABLE habits""")

c.execute("""DROP TABLE checkins""")

conn.commit()

conn.close()


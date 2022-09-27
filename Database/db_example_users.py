import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

#user examples
c.execute("""INSERT INTO users VALUES (
    'userid_1',
    'salt24662',
    'Jim' ,
    'pass1',
    '2022-06-27 06:59:59',
    '2022-09-28 14:29:00',
    'jim@test.com'
)""")

c.execute("""INSERT INTO users VALUES (
    'userid_2',
    'salt24662',
    'Rick' ,
    'pass2',
    '2022-03-27 10:10:34',
    '2022-10-4 15:32:03',
    'rick@test.com'
)""")

c.execute("""INSERT INTO users VALUES (
    'userid_3',
    'salt24662',
    'Tom' ,
    'pass3',
    '2022-02-11 05:12:43',
    '2022-05-15 19:54:15',
    'tom@test.com'
)""")


c.execute("""SELECT * FROM users""")
print(c.fetchall())

conn.commit()
conn.close()
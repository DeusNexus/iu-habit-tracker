import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

#habit examples
c.execute("""INSERT INTO checkins VALUES (
    'user_id1',
    'habit_id1',
    'checkin_id1',
    '2022-05-11 05:12:43',
    '2022-05-12 05:12:43',
    'True',
    'Great work',
    5,
    0,
    'False',
    0
)""")

c.execute("""INSERT INTO checkins VALUES (
    'user_id1',
    'habit_id1',
    'checkin_id2',
    '2022-05-12 05:12:43',
    '2022-05-13 05:12:43',
    'True',
    'Wow',
    5,
    0,
    'False',
    0
)""")

c.execute("""INSERT INTO checkins VALUES (
    'user_id1',
    'habit_id1',
    'checkin_id3',
    '2022-05-13 05:12:43',
    '2022-05-14 05:12:43',
    'True',
    'Amazing',
    5,
    0,
    'False',
    0
)""")

c.execute("""SELECT * FROM checkins""")
print(c.fetchall())

conn.commit()
conn.close()
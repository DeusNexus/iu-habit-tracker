
import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

#habit examples
c.execute("""INSERT INTO habits VALUES (
            'userid_1',
            'habit_id1',
            'title_reading',
            'description_good for my mind',
            '1D',
            'True',
            'None',
            5,
            'Eduction',
            'The more you learn the better',
            5,
            'False',
            1,
            30,
            'False',
            0,
            0,
            '2022-05-11 05:12:43',
            '2022-05-11 05:12:43',
            '2022-05-12 05:12:43',
            0,
            0,
            0,
            0,
            0
)""")

c.execute("""INSERT INTO habits VALUES (
            'userid_1',
            'habit_id2',
            'title_leisure',
            'description_good to relax',
            '2D',
            'True',
            'None',
            2,
            'Enjoyment',
            'Life a good life',
            2,
            'False',
            1,
            4,
            'False',
            0,
            0,
            '2022-05-11 05:12:43',
            '2022-05-11 05:12:43',
            '2022-05-14 05:12:43',
            0,
            0,
            0,
            0,
            0
)""")

c.execute("""INSERT INTO habits VALUES (
            'userid_1',
            'habit_id3',
            'title_gym',
            'description_do cardio',
            '3D',
            'True',
            'None',
            4,
            'Sport',
            'Stay healthy both in mind and body',
            2,
            'False',
            1,
            5,
            'False',
            0,
            0,
            '2022-05-11 05:12:43',
            '2022-05-11 05:12:43',
            '2022-05-14 05:12:43',
            0,
            0,
            0,
            0,
            0
)""")

c.execute("""SELECT * FROM habits""")
print(c.fetchall())

conn.commit()
conn.close()
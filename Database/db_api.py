import sqlite3

users = [
    {
        'userid':'userid_1',
        'salt':'salt24662',
        'name':'Jim',
        'password':'pass1',
        'created':'2022-06-27 06:59:59',
        'last_login':'2022-09-28 14:29:00',
    },
    {
        'userid':'userid_2',
        'salt':'salt2435',
        'name':'Rick',
        'password':'pass2',
        'created':'2022-03-27 10:10:34',
        'last_login':'2022-10-4 15:32:03',
    },
    {
        'userid':'userid_3',
        'salt':'salt5435',
        'name':'Tom',
        'password':'pass3',
        'created':'2022-02-11 05:12:43',
        'last_login':'2022-05-15 19:54:15',
    },
]

habits = [
    {
        'user_id':'userid_1',
        'habit_id':'habit_id1',
        'title':'title_reading',
        'description':'description_good for my mind',
        'interval':'1D',
        'active':'True',
        'start_from':'None',
        'difficulity':5,
        'category':'Eduction',
        'moto':'The more you learn the better',
        'importance':5,
        'style':1,
        'milestone_streak':30,
        'is_dynamic':'False',
        'checkin_num_before_deadline':0,
        'dynamic_count':0,
        'created_on':'2022-05-11 05:12:43',
        'prev_deadline':'2022-05-11 05:12:43',
        'next_deadline':'2022-05-12 05:12:43',
        'streak':0,
        'success':0,
        'fail':0,
        'cost':0,
        'cost_accum':0
    },
    {
        'user_id':'userid_1',
        'habit_id':'habit_id2',
        'title':'title_laughing',
        'description':'Why not?',
        'interval':'1D',
        'active':'True',
        'start_from':'None',
        'difficulity':1,
        'category':'Mental Health',
        'moto':'More joy is better',
        'importance':5,
        'style':1,
        'milestone_streak':365,
        'is_dynamic':'False',
        'checkin_num_before_deadline':0,
        'dynamic_count':0,
        'created_on':'2022-05-13 05:12:43',
        'prev_deadline':'2022-05-14 05:12:43',
        'next_deadline':'2022-05-15 05:12:43',
        'streak':1,
        'success':1,
        'fail':0,
        'cost':0,
        'cost_accum':0
    },
    {
        'user_id':'userid_1',
        'habit_id':'habit_id3',
        'title':'title_cinema',
        'description':'Movie night',
        'interval':'1W',
        'active':'True',
        'start_from':'None',
        'difficulity':1,
        'category':'Entertainment',
        'moto':'To get inspired',
        'importance':2,
        'style':1,
        'milestone_streak':4,
        'is_dynamic':'False',
        'checkin_num_before_deadline':0,
        'dynamic_count':0,
        'created_on':'2022-06-13 05:12:43',
        'prev_deadline':'2022-06-13 05:12:43',
        'next_deadline':'2022-06-20 05:12:43',
        'streak':0,
        'success':1,
        'fail':0,
        'cost':4.95,
        'cost_accum':0
    },
]

checkins = [
    {
        'user_id':'user_id1',
        'habit_id':'habit_id1',
        'checkin_id':'checkin_id1',
        'checkin_datetime':'2022-05-11 05:12:43',
        'deadline':'2022-05-12 05:12:43',
        'success':'True',
        'note':'Great work',
        'rating':4,
        'cost_accum':0,
        'dynamic':'False',
        'dynamic_count':0
    },
    {
        'user_id':'user_id1',
        'habit_id':'habit_id1',
        'checkin_id':'checkin_id2',
        'checkin_datetime':'2022-05-11 05:12:43',
        'deadline':'2022-05-13 05:12:43',
        'success':'True',
        'note':'Wow',
        'rating':5,
        'cost_accum':0,
        'dynamic':'False',
        'dynamic_count':0
    },
    {
        'user_id':'user_id1',
        'habit_id':'habit_id1',
        'checkin_id':'checkin_id3',
        'checkin_datetime':'2022-05-13 05:12:43',
        'deadline':'2022-05-14 05:12:43',
        'success':'True',
        'note':'Amazing',
        'rating':4,
        'cost_accum':0,
        'dynamic':'False',
        'dynamic_count':0
    },
]

#Initializes the database tables: users, habits and checkins
def db_init():
    """Initializes the habit tracker database with the tables users, habits and checkins. If the tables already exist it will return an error."""

    try:
        conn = sqlite3.connect('app.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE users (
                    user_id text,
                    salt text,
                    name text,
                    password text,
                    created text,
                    last_login text
        )""")

        c.execute("""CREATE TABLE habits (
                    user_id text,
                    habit_id text,
                    title text,
                    description text,
                    interval text,
                    active text,
                    start_from text,
                    difficulity integer,
                    category text,
                    moto text,
                    importance integer,
                    style integer,
                    milestone integer,
                    is_dynamic text,
                    checkin_num_before_deadline integer,
                    dynamic_count integer,
                    created_on text,
                    prev_deadline text,
                    next_deadline text,
                    streak integer,
                    success integer,
                    fail integer,
                    cost real,
                    cost_accum real
        )""")

        c.execute("""CREATE TABLE checkins (
                    user_id text,
                    habit_id text,
                    checkin_id text,
                    checkin_datetime text,
                    deadline text,
                    success text,
                    note text,
                    rating integer,
                    cost_accum real,
                    dynamic text,
                    dynamic_count integer
        )""")

        conn.commit()
        conn.close()
    except Exception as e:
        print('[Unable to insert table]',e)

#Drop all database tables
def db_drop():
    try:
        """Drops all tables of the habit tracker database."""
        conn = sqlite3.connect('app.db')
        c = conn.cursor()

        c.execute("""DROP TABLE users""")
        c.execute("""DROP TABLE habits""")
        c.execute("""DROP TABLE checkins""")

        conn.commit()
        conn.close()
        print('Dropped all tables in database!')

    except Exception as e:
        print('[Unable to drop tables]',e)

#Insert example users
def db_users_example(users):
    """Inserts example users into the users-table by passing an list with user dict objects."""
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    def insert_user(user):
        c.execute("""INSERT INTO users VALUES (:userid,:salt,:name ,:password,:created,:last_login)""", user)

    #user examples
    for u in users:
        insert_user(u)

    c.execute("""SELECT * FROM users""")
    print(c.fetchall())

    conn.commit()
    conn.close()

#Insert habits for example users
def db_habits_example(habits):
    """"Inserts example habits for the provided example users by providing an list with habit dict objects"""
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    #habit examples
    def insert_habit(habit):
        c.execute("""INSERT INTO habits VALUES (:user_id,:habit_id,:title,
        :description,:interval,:active,:start_from,:difficulity,:category,:moto,:importance,
        :style,:milestone_streak,:is_dynamic,:checkin_num_before_deadline,:dynamic_count,:created_on,:prev_deadline,
        :next_deadline,:streak,:success,:fail,:cost,:cost_accum)""", habit)

    for h in habits:
        insert_habit(h)

    c.execute("""SELECT * FROM habits""")
    print(c.fetchall())

    conn.commit()
    conn.close()

#Insert Checkins for example habits
def db_checkins_example(checkins):
    """Inserts example checkins into the checkin-table by providing a list with dict checkins."""
    conn = sqlite3.connect('app.db')
    c = conn.cursor()

    #habit examples
    def insert_checkin(checkin):
        c.execute("""INSERT INTO checkins VALUES (:user_id,:habit_id,:checkin_id,:checkin_datetime,:deadline,:success,:note,:rating,:cost_accum,:dynamic,:dynamic_count)""",checkin)

    for checkin in checkins:
        insert_checkin(checkin)

    c.execute("""SELECT * FROM checkins""")
    print(c.fetchall())

    conn.commit()
    conn.close()

#Display all tables
def db_view():
    """Displays all entries in the habit tracker database tables by printing to the terminal."""
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

db_drop()
db_init()
db_users_example(users)
db_habits_example(habits)
db_checkins_example(checkins)
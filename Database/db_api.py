import sqlite3
from urllib.request import pathname2url

from time import sleep
import Load

DB_FILE = 'Database/app.db'

users = [
    {
        'user_id':'4z6cr',
        'salt':"b'$2b$14$bjwObtQ6eROB8au4gaquLu'",
        'name':'<Example> Jim - pw:pass1',
        'password':"b'$2b$14$bjwObtQ6eROB8au4gaquLuhBljuja6D649YEtMfIfw8HAlrMGGdH2'",
        'created':'2022-06-27 06:59:59.1',
        'last_login':'2022-09-28 14:29:00.1',
    },
    {
        'user_id':'qpiqk',
        'salt':"b'$2b$14$Xt4xMz37x9NqP7d9sIUFlO'",
        'name':'<Example> Rick - pw:pass2',
        'password':"b'$2b$14$Xt4xMz37x9NqP7d9sIUFlOSFVMVDKU.GtTUW/gGbSbVAP/7vmqqlK'",
        'created':'2022-03-27 10:10:34.1',
        'last_login':'2022-10-4 15:32:03.1',
    },
    {
        'user_id':'bw8tg',
        'salt':"b'$2b$14$8uNhMbB6dmvvMg5JKzF.3u'",
        'name':'<Example> Tom - pw:pass3',
        'password':"b'$2b$14$8uNhMbB6dmvvMg5JKzF.3uWOCIJvW7XWv4JaQTgM4G1m9n7iGNgrO'",
        'created':'2022-02-11 05:12:43.1',
        'last_login':'2022-05-15 19:54:15.1',
    },
]

habits = [
    {
        'user_id':'4z6cr',
        'habit_id':'6tryr',
        'title':'title_reading',
        'description':'description_good for my mind',
        'interval':'1D',
        'active':'True',
        'start_from':'',
        'difficulity':5,
        'category':'Eduction',
        'moto':'The more you learn the better',
        'importance':5,
        'style':1,
        'milestone_streak':30,
        'is_dynamic':'False',
        'checkin_num_before_deadline':0,
        'dynamic_count':0,
        'created_on':'2022-05-11 05:12:43.1',
        'prev_deadline':'2022-05-11 05:12:43.1',
        'next_deadline':'2022-05-12 05:12:43.1',
        'streak':0,
        'success':0,
        'fail':0,
        'cost':0,
        'cost_accum':0
    },
    {
        'user_id':'4z6cr',
        'habit_id':'bxmqk',
        'title':'title_laughing',
        'description':'Why not?',
        'interval':'1D',
        'active':'True',
        'start_from':'',
        'difficulity':1,
        'category':'Mental Health',
        'moto':'More joy is better',
        'importance':5,
        'style':1,
        'milestone_streak':365,
        'is_dynamic':'False',
        'checkin_num_before_deadline':0,
        'dynamic_count':0,
        'created_on':'2022-05-13 05:12:43.1',
        'prev_deadline':'2022-05-14 05:12:43.1',
        'next_deadline':'2022-05-15 05:12:43.1',
        'streak':1,
        'success':1,
        'fail':0,
        'cost':0,
        'cost_accum':0
    },
    {
        'user_id':'4z6cr',
        'habit_id':'fy2um',
        'title':'title_cinema',
        'description':'Movie night',
        'interval':'1W',
        'active':'True',
        'start_from':'',
        'difficulity':1,
        'category':'Entertainment',
        'moto':'To get inspired',
        'importance':2,
        'style':1,
        'milestone_streak':4,
        'is_dynamic':'False',
        'checkin_num_before_deadline':0,
        'dynamic_count':0,
        'created_on':'2022-06-13 05:12:43.1',
        'prev_deadline':'2022-06-13 05:12:43.1',
        'next_deadline':'2022-06-20 05:12:43.1',
        'streak':0,
        'success':1,
        'fail':0,
        'cost':4.95,
        'cost_accum':0
    },
]

checkins = [
    {
        'user_id':'4z6cr',
        'habit_id':'6tryr',
        'checkin_id':'hed69',
        'checkin_datetime':'2022-05-11 05:12:43.1',
        'deadline':'2022-05-12 05:12:43.1',
        'success':'True',
        'note':'Great work',
        'rating':4,
        'cost':0,
        'cost_accum':0,
        'dynamic':'False',
        'dynamic_count':0
    },
    {
        'user_id':'4z6cr',
        'habit_id':'6tryr',
        'checkin_id':'9luhm',
        'checkin_datetime':'2022-05-11 05:12:43.1',
        'deadline':'2022-05-13 05:12:43.1',
        'success':'True',
        'note':'Wow',
        'rating':5,
        'cost':0,
        'cost_accum':0,
        'dynamic':'False',
        'dynamic_count':0
    },
    {
        'user_id':'4z6cr',
        'habit_id':'6tryr',
        'checkin_id':'cg3yacl',
        'checkin_datetime':'2022-05-13 05:12:43.1',
        'deadline':'2022-05-14 05:12:43.1',
        'success':'True',
        'note':'Amazing',
        'rating':4,
        'cost':0,
        'cost_accum':0,
        'dynamic':'False',
        'dynamic_count':0
    },
]

#Initializes the database tables: users, habits and checkins
def db_init() -> None:
    """Initializes the habit tracker database with the tables users, habits and checkins. If the tables already exist it will return an error."""

    try:
        conn = sqlite3.connect(DB_FILE)
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
                    milestone_streak integer,
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
                    cost real,
                    cost_accum real,
                    dynamic text,
                    dynamic_count integer
        )""")

        conn.commit()
        conn.close()
    except Exception as e:
        print('[Unable to insert table]',e)

#Drop all database tables
def db_drop() -> None:
    try:
        """Drops all tables of the habit tracker database."""
        conn = sqlite3.connect(DB_FILE)
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
def db_users_insert(users) -> None:
    """Inserts users into the users-table by passing an list with user dict objects."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    def insert_user(user):
        c.execute("""INSERT INTO users VALUES (:user_id,:salt,:name ,:password,:created,:last_login)""", user)

    #user examples
    for u in users:
        insert_user(u)

    # c.execute("""SELECT * FROM users""")
    # print(c.fetchall())

    conn.commit()
    conn.close()

#Insert habits for users
def db_habits_insert(habits) -> None:
    """"Inserts (example) habits for the provided (example) users by providing an list with habit dict objects"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #habit examples
    def insert_habit(habit):
        c.execute("""INSERT INTO habits VALUES (:user_id,:habit_id,:title,
        :description,:interval,:active,:start_from,:difficulity,:category,:moto,:importance,
        :style,:milestone_streak,:is_dynamic,:checkin_num_before_deadline,:dynamic_count,:created_on,:prev_deadline,
        :next_deadline,:streak,:success,:fail,:cost,:cost_accum)""", habit)

    for h in habits:
        insert_habit(h)

    # c.execute("""SELECT * FROM habits""")
    # print(c.fetchall())

    conn.commit()
    conn.close()

#Delete habits for users
def db_habits_delete(habit_id) -> None:
    """"Deletes (example) habits for the provided (example) users by providing an habit_id"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #habit examples
    def delete_habit(habit_id):
        c.execute("""DELETE FROM habits WHERE habit_id IS :habit_id""",{"habit_id":habit_id})

    delete_habit(habit_id)

    # c.execute("""SELECT * FROM habits""")
    # print(c.fetchall())

    conn.commit()
    conn.close()

#Insert Checkins for example habits
def db_checkins_insert(checkins) -> None:
    """Inserts (example) checkins into the checkin-table by providing a list with dict checkins."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #habit examples
    def insert_checkin(checkin):
        c.execute("""INSERT INTO checkins VALUES (:user_id,:habit_id,:checkin_id,:checkin_datetime,:deadline,:success,:note,:rating,:cost,:cost_accum,:dynamic,:dynamic_count)""",checkin)

    for checkin in checkins:
        insert_checkin(checkin)

    # c.execute("""SELECT * FROM checkins""")
    # print(c.fetchall())

    conn.commit()
    conn.close()

#Delete checkins for habit_id
def db_checkins_delete(habit_id) -> None:
    """"Deletes checkins for the provided habit_id"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #habit examples
    def delete_checkin(habit_id):
        c.execute("""DELETE FROM checkins WHERE habit_id IS :habit_id""",{"habit_id":habit_id})

    delete_checkin(habit_id)

    # c.execute("""SELECT * FROM checkins""")
    # print(c.fetchall())

    conn.commit()
    conn.close()

def db_update_habit_checkin(habit) -> None:
    """Update habit when a checkin happens by providing the changed habit as an object."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #habit examples
    def update_habit(habit):
        # user_id text,
        # habit_id text,
        # title text,
        # description text,
        # interval text,
        # active text,
        # start_from text,
        # difficulity integer,
        # category text,
        # moto text,
        # importance integer,
        # style integer,
        ## milestone_streak integer,
        # is_dynamic text,
        ## checkin_num_before_deadline integer,
        ## dynamic_count integer,
        # created_on text,
        ## prev_deadline text,
        ## next_deadline text,
        ## streak integer,
        ## success integer,
        ## fail integer,
        ## cost real,
        ## cost_accum real

        #Update all attributes involved with checkin
        c.execute(f"""UPDATE habits SET milestone_streak = :val WHERE habit_id IS :habit_id""", {"habit_id":habit.habit_id,"val":habit.milestone_streak})
        c.execute(f"""UPDATE habits SET checkin_num_before_deadline = :val WHERE habit_id IS :habit_id""", {"habit_id":habit.habit_id,"val":habit.checkin_num_before_deadline})
        c.execute(f"""UPDATE habits SET dynamic_count = :val WHERE habit_id IS :habit_id""", {"habit_id":habit.habit_id,"val":habit.dynamic_count})
        c.execute(f"""UPDATE habits SET prev_deadline = :val WHERE habit_id IS :habit_id""", {"habit_id":habit.habit_id,"val":habit.prev_deadline})
        c.execute(f"""UPDATE habits SET next_deadline = :val WHERE habit_id IS :habit_id""", {"habit_id":habit.habit_id,"val":habit.next_deadline})
        c.execute(f"""UPDATE habits SET streak = :val WHERE habit_id IS :habit_id""", {"habit_id":habit.habit_id,"val":habit.streak})
        c.execute(f"""UPDATE habits SET success = :val WHERE habit_id IS :habit_id""", {"habit_id":habit.habit_id,"val":habit.success})
        c.execute(f"""UPDATE habits SET fail = :val WHERE habit_id IS :habit_id""", {"habit_id":habit.habit_id,"val":habit.fail})
        c.execute(f"""UPDATE habits SET cost = :val WHERE habit_id IS :habit_id""", {"habit_id":habit.habit_id,"val":habit.cost})
        c.execute(f"""UPDATE habits SET cost_accum = :val WHERE habit_id IS :habit_id""", {"habit_id":habit.habit_id,"val":habit.cost_accum})

    update_habit(habit)

    # c.execute("""SELECT * FROM habits""")
    # print(c.fetchall())

    conn.commit()
    conn.close()

def db_update_habit(habit_id, attr, val) -> None:
    """Update habit attribute by providing the habit_id, the attribute name to change and the new value."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    #habit examples
    def update_habit(habit_id,attr,val):
        c.execute(f"""UPDATE habits SET {attr} = :val WHERE habit_id IS :habit_id""", {"habit_id":habit_id,"attr":attr,"val":val})

    update_habit(habit_id, attr, val)

    # c.execute("""SELECT * FROM habits""")
    # print(c.fetchall())

    conn.commit()
    conn.close()

#Display all tables
def db_view():
    """Displays all entries in the habit tracker database tables by printing to the terminal."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""SELECT * FROM users""")
    # print('\nusers:',c.fetchall())

    c.execute("""SELECT * FROM habits""")
    # print('\nhabits:',c.fetchall())

    c.execute("""SELECT * FROM checkins""")
    # print('\ncheckins:',c.fetchall())

    conn.commit()
    conn.close()

def db_get_users() -> list:
    """Returns all users from the database table users."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""SELECT * FROM users""")
    users = c.fetchall()
    conn.commit()
    conn.close()
    return users

def db_get_habits(user_id:str) -> list:
    """Returns all habits for a user_id from the database table habits"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""SELECT * FROM habits WHERE user_id IS :user_id""",{"user_id":user_id})
    habits = c.fetchall()
    conn.commit()
    conn.close()
    return habits

def db_get_checkins(user_id:str) -> list:
    """Returns all checkins for a user_id from the database table habits"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""SELECT * FROM checkins WHERE user_id IS :user_id""",{"user_id":user_id})
    checkins = c.fetchall()
    conn.commit()
    conn.close()
    return checkins

def db_exists():
    """Run each time when the habit tracker starts to see if db already exist or we need to init a new one."""
    try:
        dburi = 'file:{}?mode=rw'.format(pathname2url(DB_FILE))
        conn = sqlite3.connect(dburi, uri=True)
        print('[✔️] Found existing database! Proceeding to load application.')
    except sqlite3.OperationalError as e:
        # handle missing database case
        print('[⚠️] No existing database found, creating a new one with example data...')
        db_init()
        db_users_insert(users)
        db_habits_insert(habits)
        db_checkins_insert(checkins)
        print('[💽] A persistent database has been created and will be used in the future to store your user data!')
        # print(e)

def db_export(user_id: str) -> dict:
    '''Export user for the given user_id. Used in the Import/Export screen for the active user.
    Generates a dict object containing user, habits and checkins which is returned to write out as json file.
    '''
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""SELECT * FROM users WHERE user_id IS :user_id""",{"user_id":user_id})
    user = c.fetchall()

    c.execute("""SELECT * FROM habits WHERE user_id IS :user_id""",{"user_id":user_id})
    habits = c.fetchall()

    c.execute("""SELECT * FROM checkins WHERE user_id IS :user_id""",{"user_id":user_id})
    checkins = c.fetchall()

    conn.commit()
    conn.close()

    return {
        "user":user,
        "habits":habits,
        "checkins":checkins
    }

def db_import(user_obj) -> bool:
    '''Imports user for the given user_obj. Used in the Import/Export screen for importing user  from json file.
    If user_id already exist it will throw an error.
    Iterates over user, habits and checkins to add them to the database.
    '''
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # print(user_obj)

    user = user_obj['user']
    # print('user: ',user)
    user_id = user[0][0]
    # print('user_id: ',user_id)
    habits = user_obj['habits']
    # print('habits: ',habits)
    checkins = user_obj['checkins']
    # print('checkins: ',checkins)

    #Find if user_id exists in db
    c.execute("""SELECT * FROM users WHERE user_id IS :user_id""",{"user_id":user_id})
    fetched_user = c.fetchall()

    # print('Fetched User: ',fetched_user)
    try:
        if(not fetched_user):
            print('No user_id yet exists, proceeding to insert data to db.')
            #User does not yet exist, proceed to import.
            print('Inserting user...')
            db_users_insert(user)
            print('Inserting habits for user...')
            db_habits_insert(habits)
            print('Inserting checkins for habits of user...')
            db_checkins_insert(checkins)
            print('Committing all inserts...')
            conn.commit()
            print('Closing connection to database...')
            conn.close()
            sleep(2)
            return "success"

        elif(user):
            #User already exists
            print('user_id already exists in db, cancelling operation.')
            conn.commit()
            conn.close()
            sleep(2)
            return "exists"

    except Exception as e:
        #Error
        conn.commit()
        conn.close()
        print('db_import error:',e)
        sleep(2)
        return "error"

def db_reset_user_full(user_id:str) -> None:
    '''Reset the user completely to a blank minimum state, user table is unaffected, both habits and checkins for user are removed for the given user_id.'''
    
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        print(('Removing all checkins for user...'))
        c.execute("""DELETE FROM checkins WHERE user_id IS :user_id""",{"user_id":user_id})
        print('Removing all habits for user...')
        c.execute("""DELETE FROM habits WHERE user_id IS :user_id""",{"user_id":user_id})
        conn.commit()
        conn.close()
        print('[*] User account successfully completed a full reset')
        
    except Exception as e:
        print('db_reset_user_full error:',e)
        conn.commit()
        conn.close()
        sleep(2)

def db_reset_user_example_data(user_id:str) -> None:
    '''Reset the user and insert example data (habits and checkins).'''
    
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        print(('Removing all checkins for user...'))
        c.execute("""DELETE FROM checkins WHERE user_id IS :user_id""",{"user_id":user_id})
        print('Removing all habits for user...')
        c.execute("""DELETE FROM habits WHERE user_id IS :user_id""",{"user_id":user_id})

        conn.commit()
        conn.close()

        habits, checkins = Load.default_example_data(user_id)
        print('Inserting example habits for user...')
        db_habits_insert(habits)
        print('Inserting corresponding example checkins for user...')
        db_checkins_insert(checkins)
        print('[*] User account successfully completed a full reset')
        
    except Exception as e:
        print('db_reset_user_full error:',e)
        conn.commit()
        conn.close()
        sleep(2)
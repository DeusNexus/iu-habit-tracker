import sqlite3
from urllib.request import pathname2url

from time import sleep
import Load

#Example users, habits and checkins
from Database import Examples
users, habits, checkins = Examples.data()

DB_FILE = 'Database/app.db'

def open_connection() -> 'c, conn':
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    return c, conn

def close_connection(conn) -> None:
    conn.commit()
    conn.close()

#Initializes the database tables: users, habits and checkins
def db_init() -> None:
    """Initializes the habit tracker database with the tables users, habits and checkins. If the tables already exist it will return an error."""

    try:
        c, conn = open_connection()

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

        close_connection(conn)
    except Exception as e:
        print('[Unable to insert table]',e)

#Drop all database tables
def db_drop() -> None:
    try:
        """Drops all tables of the habit tracker database."""
        c, conn = open_connection()

        c.execute("""DROP TABLE users""")
        c.execute("""DROP TABLE habits""")
        c.execute("""DROP TABLE checkins""")

        close_connection(conn)
        print('Dropped all tables in database!')

    except Exception as e:
        print('[Unable to drop tables]',e)

#Insert example users
def db_users_insert(users) -> None:
    """Inserts users into the users-table by passing an list with user dict objects."""
    c, conn = open_connection()

    def insert_user(user):
        c.execute("""INSERT INTO users VALUES (:user_id,:salt,:name ,:password,:created,:last_login)""", user)

    #user examples
    for u in users:
        insert_user(u)

    # c.execute("""SELECT * FROM users""")
    # print(c.fetchall())

    close_connection(conn)

#Insert habits for users
def db_habits_insert(habits) -> None:
    """"Inserts (example) habits for the provided (example) users by providing an list with habit dict objects"""
    c, conn = open_connection()

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

    close_connection(conn)

#Delete habits for users
def db_habits_delete(habit_id) -> None:
    """"Deletes (example) habits for the provided (example) users by providing an habit_id"""
    c, conn = open_connection()

    #habit examples
    def delete_habit(habit_id):
        c.execute("""DELETE FROM habits WHERE habit_id IS :habit_id""",{"habit_id":habit_id})

    delete_habit(habit_id)

    # c.execute("""SELECT * FROM habits""")
    # print(c.fetchall())

    close_connection(conn)

#Insert Checkins for example habits
def db_checkins_insert(checkins) -> None:
    """Inserts (example) checkins into the checkin-table by providing a list with dict checkins."""
    c, conn = open_connection()

    #habit examples
    def insert_checkin(checkin):
        c.execute("""INSERT INTO checkins VALUES (:user_id,:habit_id,:checkin_id,:checkin_datetime,:deadline,:success,:note,:rating,:cost,:cost_accum,:dynamic,:dynamic_count)""",checkin)

    for checkin in checkins:
        insert_checkin(checkin)

    # c.execute("""SELECT * FROM checkins""")
    # print(c.fetchall())

    close_connection(conn)

#Delete checkins for habit_id
def db_checkins_delete(habit_id) -> None:
    """"Deletes checkins for the provided habit_id"""
    c, conn = open_connection()

    #habit examples
    def delete_checkin(habit_id):
        c.execute("""DELETE FROM checkins WHERE habit_id IS :habit_id""",{"habit_id":habit_id})

    delete_checkin(habit_id)

    # c.execute("""SELECT * FROM checkins""")
    # print(c.fetchall())

    close_connection(conn)

def db_update_habit_checkin(habit) -> None:
    """Update habit when a checkin happens by providing the changed habit as an object."""
    c, conn = open_connection()

    #habit examples
    def update_habit(habit):
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

    close_connection(conn)

def db_update_habit(habit_id, attr, val) -> None:
    """Update habit attribute by providing the habit_id, the attribute name to change and the new value."""
    c, conn = open_connection()

    #habit examples
    def update_habit(habit_id,attr,val):
        c.execute(f"""UPDATE habits SET {attr} = :val WHERE habit_id IS :habit_id""", {"habit_id":habit_id,"attr":attr,"val":val})

    update_habit(habit_id, attr, val)

    # c.execute("""SELECT * FROM habits""")
    # print(c.fetchall())

    close_connection(conn)

#Display all tables
def db_view():
    """Displays all entries in the habit tracker database tables by printing to the terminal."""
    c, conn = open_connection()

    c.execute("""SELECT * FROM users""")
    # print('\nusers:',c.fetchall())

    c.execute("""SELECT * FROM habits""")
    # print('\nhabits:',c.fetchall())

    c.execute("""SELECT * FROM checkins""")
    # print('\ncheckins:',c.fetchall())

    close_connection(conn)

def db_get_users() -> list:
    """Returns all users from the database table users."""
    c, conn = open_connection()
    c.execute("""SELECT * FROM users""")
    users = c.fetchall()
    close_connection(conn)
    return users

def db_get_habits(user_id:str) -> list:
    """Returns all habits for a user_id from the database table habits"""
    c, conn = open_connection()
    c.execute("""SELECT * FROM habits WHERE user_id IS :user_id""",{"user_id":user_id})
    habits = c.fetchall()
    close_connection(conn)
    return habits

def db_get_habits_by_attr(user_id:str, attr:str, value:str) -> list:
    """Returns all habits for a user_id and attribute with given value from the database table habits"""
    c, conn = open_connection()
    c.execute(f"""SELECT * FROM habits WHERE user_id IS :user_id AND {attr} IS :value""",{"user_id":user_id, "value":value})
    habits = c.fetchall()
    close_connection(conn)
    return habits

def db_get_habits_by_attr_operator(user_id:str, attr:str, value:str, operator:str) -> list:
    """Returns all habits for a user_id and attribute with given value using a comparison operator from the database table habits"""
    c, conn = open_connection()
    c.execute(f"""SELECT * FROM habits WHERE user_id IS :user_id AND {attr} {operator} :value""",{"user_id":user_id, "value":value})
    habits = c.fetchall()
    close_connection(conn)
    return habits

def db_get_checkins(user_id:str) -> list:
    """Returns all checkins for a user_id from the database table habits"""
    c, conn = open_connection()
    c.execute("""SELECT * FROM checkins WHERE user_id IS :user_id""",{"user_id":user_id})
    checkins = c.fetchall()
    close_connection(conn)
    return checkins

def db_exists():
    """Run each time when the habit tracker starts to see if db already exist or we need to init a new one."""
    try:
        dburi = 'file:{}?mode=rw'.format(pathname2url(DB_FILE))
        c = sqlite3.connect(dburi, uri=True)
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
    c, conn = open_connection()

    c.execute("""SELECT * FROM users WHERE user_id IS :user_id""",{"user_id":user_id})
    user = c.fetchall()

    c.execute("""SELECT * FROM habits WHERE user_id IS :user_id""",{"user_id":user_id})
    habits = c.fetchall()

    c.execute("""SELECT * FROM checkins WHERE user_id IS :user_id""",{"user_id":user_id})
    checkins = c.fetchall()

    close_connection(conn)

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
    c, conn = open_connection()

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
            print('Closing connection to database...')
            close_connection(conn)
            sleep(2)
            return "success"

        elif(user):
            #User already exists
            print('user_id already exists in db, cancelling operation.')
            close_connection(conn)
            sleep(2)
            return "exists"

    except Exception as e:
        #Error
        close_connection(conn)
        print('db_import error:',e)
        sleep(2)
        return "error"

def db_reset_user_full(user_id:str) -> None:
    '''Reset the user completely to a blank minimum state, user table is unaffected, both habits and checkins for user are removed for the given user_id.'''
    
    try:
        c, conn = open_connection()
        print(('Removing all checkins for user...'))
        c.execute("""DELETE FROM checkins WHERE user_id IS :user_id""",{"user_id":user_id})
        print('Removing all habits for user...')
        c.execute("""DELETE FROM habits WHERE user_id IS :user_id""",{"user_id":user_id})
        close_connection(conn)
        print('[*] User account successfully completed a full reset')
        
    except Exception as e:
        print('db_reset_user_full error:',e)
        close_connection(conn)
        sleep(2)

def db_reset_user_example_data(user_id:str) -> None:
    '''Reset the user and insert example data (habits and checkins).'''
    
    try:
        c, conn = open_connection()

        print(('Removing all checkins for user...'))
        c.execute("""DELETE FROM checkins WHERE user_id IS :user_id""",{"user_id":user_id})
        print('Removing all habits for user...')
        c.execute("""DELETE FROM habits WHERE user_id IS :user_id""",{"user_id":user_id})

        close_connection(conn)

        habits, checkins = Load.default_example_data(user_id)
        print('Inserting example habits for user...')
        db_habits_insert(habits)
        print('Inserting corresponding example checkins for user...')
        db_checkins_insert(checkins)
        print('[*] User account successfully completed a full reset')
        
    except Exception as e:
        print('db_reset_user_full error:',e)
        close_connection(conn)
        sleep(2)
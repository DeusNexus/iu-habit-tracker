from datetime import datetime
from Database import db_api as api
from Classes.CheckIn import CheckIn
import traceback
from time import sleep
from shortuuid import ShortUUID
from Utils import style

SLEEP_SPEED=0

def User_Model(res):
    user = {
        'user_id':res[0],
        'salt':res[1],
        'name':str(res[2]),
        'password':res[3],
        'created':datetime.strptime(res[4], "%Y-%m-%d %H:%M:%S.%f"),
        'last_login':datetime.strptime(res[5], "%Y-%m-%d %H:%M:%S.%f"),
    }
    return user

def Habit_Model(res):
    habit = {
        'user_id':str(res[0]),
        'habit_id':str(res[1]),
        'title':str(res[2]),
        'description':str(res[3]),
        'interval':str(res[4]),
        'active': True if res[5] == 'True' else False,
        'start_from':datetime.strptime(res[6], "%Y-%m-%d %H:%M:%S.%f") if res[6] != '' else None,
        'difficulity':int(res[7]) if res[7] else 0,
        'category':str(res[8]),
        'moto':str(res[9]),
        'importance':int(res[10]) if res[10] else 0,
        'style':int(res[11]) if res[11] else 0,
        'milestone_streak': int(res[12]) if(res[12]) else 0,
        'is_dynamic': True if res[13] == 'True' else False,
        'checkin_num_before_deadline': int(res[14]) if res[14] else 0,
        'dynamic_count': int(res[15]) if res[15] else 0,
        'created_on':datetime.strptime(res[16], "%Y-%m-%d %H:%M:%S.%f"),
        'prev_deadline':datetime.strptime(res[17], "%Y-%m-%d %H:%M:%S.%f"),
        'next_deadline':datetime.strptime(res[18], "%Y-%m-%d %H:%M:%S.%f"),
        'streak':int(res[19]),
        'success':int(res[20]),
        'fail':int(res[21]),
        'cost':res[22],
        'cost_accum':res[23],
    }
    return habit

def Checkin_Model(res):
    checkin = {
        'user_id':str(res[0]),
        'habit_id':str(res[1]),
        'checkin_id':str(res[2]),
        'checkin_datetime':datetime.strptime(res[3],"%Y-%m-%d %H:%M:%S.%f"),
        'deadline':datetime.strptime(res[4], "%Y-%m-%d %H:%M:%S.%f"),
        'success': True if res[5] == 'True' else False,
        'note':str(res[6]),
        'rating':int(res[7]),
        'cost':float(res[8]),
        'cost_accum':float(res[9]),
        'dynamic': True if res[10] == 'True' else False,
        'dynamic_count':int(res[11]) if res[11] else 0
    }
    return checkin

def load_users(users):
    '''Creates Example Users, Habits and Check-ins in memory from database.'''
    api.db_view()
    db_users = api.db_get_users()
    print(style(f'[🔍] Loaded {len(db_users)} available users from sqlite3 database...','GREEN'))
    #[('userid_1', 'salt24662', 'Jim', 'pass1', '2022-06-27 06:59:59', '2022-09-28 14:29:00'),...]    
    # print(db_users)
    #For each user in the database, create a user class in memory and then overwrite with database values.

    index=0
    for u in db_users:
        print(f'[⏳] Initializing {index+1} of {len(db_users)}...')
        um = User_Model(u)
        users.create(um['name'],um['password'])
        users.users[index].overwrite(um['user_id'],um['salt'],um['name'],um['password'],um['created'],um['last_login'])
        index += 1
    print(style(f'[✔️] Habit Tracker fully initialized!','GREEN'))
    

def default_example_data(user_id) -> tuple:
    '''Generates example data for a user_id so that it is unique and returns the habits and checkins as a tuple.!'''
    habits = [
                {
                    'user_id':user_id,
                    'habit_id':ShortUUID().random(length=5).lower(),
                    'title':'Example Habit 1',
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
                    'user_id':user_id,
                    'habit_id':ShortUUID().random(length=5).lower(),
                    'title':'Example Habit 2',
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
                    'user_id':user_id,
                    'habit_id':ShortUUID().random(length=5).lower(),
                    'title':'Example Habit 3',
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
            'user_id':user_id,
            'habit_id':habits[0]['habit_id'],
            'checkin_id':ShortUUID().random(length=5).lower(),
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
            'user_id':user_id,
            'habit_id':habits[0]['habit_id'],
            'checkin_id':ShortUUID().random(length=5).lower(),
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
            'user_id':user_id,
            'habit_id':habits[0]['habit_id'],
            'checkin_id':ShortUUID().random(length=5).lower(),
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

    return (habits, checkins)

def load_user_data(users,user_id):
    '''The load_user_data function receives the loggedin user and then fetches the latest local database to insert users habits and checkins. Its main purpose is to load data from storage to memory while the program operates.'''
    
     #For each example user class now, create example habits and overwrite with database values.
    
    #Get the habits of the active user_id
    habits = api.db_get_habits(user_id)
    #Get the checkins of the active user_id
    checkins = api.db_get_checkins(user_id)

    #Now we need to got the the correct index in users.users where our active user is located.    
    try:
        for u in users.users:
            #Find the user that is logging in
            if(user_id == u.user_id):

                #Go over all habits that got send from the database for this user
                for hidx, h in enumerate(habits):
                    #The database sends them in a list, for convenience the list is parsed into a dict model for easier access to the different attributes
                    hm = Habit_Model(h)
                    #Create new habit but then use overwrite to fill out all database values, basically a temporary place holder.
                    u.create_habit(hm['title'],hm['description'],hm['interval'],hm['active'],hm['start_from'],hm['difficulity'],hm['category'],hm['moto'],hm['importance'],hm['milestone_streak'],hm['style'],hm['is_dynamic'],hm['checkin_num_before_deadline'],hm['habit_id'],hm['user_id'],hm['cost'])
                    #Overwrite the habit instance with current db values
                    u.habits[hidx].overwrite(
                        user_id=hm['user_id'],
                        habit_id=hm['habit_id'],
                        title=hm['title'],
                        description=hm['description'],
                        interval=hm['interval'],
                        active=hm['active'],
                        start_from=hm['start_from'],
                        difficulity=hm['difficulity'],
                        category=hm['category'],
                        moto=hm['moto'],
                        importance=hm['importance'],
                        milestone_streak=hm['milestone_streak'],
                        style=hm['style'],
                        is_dynamic=hm['is_dynamic'],
                        checkin_num_before_deadline=hm['checkin_num_before_deadline'],
                        dynamic_count=hm['dynamic_count'],
                        created_on=hm['created_on'],
                        prev_deadline=hm['prev_deadline'],
                        next_deadline=hm['next_deadline'],
                        streak=hm['streak'],
                        success=hm['success'],
                        fail=hm['fail'],
                        cost=hm['cost'],
                        cost_accum=hm['cost_accum'])

                # CheckIn(user_id,'habit_id1','checkin_id1','2020-06-06 12:15:20',True,'Good',5,0,0,False,0)
                #While still on current habit, lets load all the available checkins from the database and add them to the habits checkins list.
                for cidx, c in enumerate(checkins):
                    for hidx, h in enumerate(u.habits):
                        #Convert the database tuple into a dict using the model
                        cm = Checkin_Model(c)
                        if h.habit_id == cm['habit_id']:                        
                            #Create placeholder checkin
                            h.checkins.append(CheckIn(cm['user_id'],cm['habit_id'],cm['checkin_id'],cm['deadline'],cm['success'],cm['note'],cm['rating'],cm['cost'],cm['cost_accum'],cm['dynamic'],cm['dynamic_count']))
                            h.checkins[-1].overwrite(cm['user_id'],cm['habit_id'],cm['checkin_id'],cm['checkin_datetime'],cm['deadline'],cm['success'],cm['note'],cm['rating'],cm['cost'],cm['cost_accum'],cm['dynamic'],cm['dynamic_count'])

    except Exception as e:
        print("[❌] Fail in load_user_data: ",e)
        traceback.print_exc()
        sleep(30)

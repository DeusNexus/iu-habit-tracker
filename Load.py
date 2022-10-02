from datetime import datetime
from Database import db_api as api
from Classes.CheckIn import CheckIn
import traceback
from time import sleep

def User_Model(res):
    user = {
        'user_id':res[0],
        'salt':res[1],
        'name':res[2],
        'password':res[3],
        'created':res[4],
        'last_login':res[5],
    }
    return user

def Habit_Model(res):
    habit = {
        'user_id':res[0],
        'habit_id':res[1],
        'title':res[2],
        'description':res[3],
        'interval':res[4],
        'active':res[5],
        'start_from':res[6],
        'difficulity':res[7],
        'category':res[8],
        'moto':res[9],
        'importance':res[10],
        'style':res[11],
        'milestone_streak':res[12],
        'is_dynamic':res[13],
        'checkin_num_before_deadline':res[14],
        'dynamic_count':res[15],
        'created_on':res[16],
        'prev_deadline':res[17],
        'next_deadline':res[18],
        'streak':res[19],
        'success':res[20],
        'fail':res[21],
        'cost':res[22],
        'cost_accum':res[23]
    }
    return habit

def Checkin_Model(res):
    checkin = {
        'user_id':res[0],
        'habit_id':res[1],
        'checkin_id':res[2],
        'checkin_datetime':res[3],
        'deadline':res[4],
        'success':res[5],
        'note':res[6],
        'rating':res[7],
        'cost':res[8],
        'cost_accum':res[9],
        'dynamic':res[10],
        'dynamic_count':res[11]
    }
    return checkin

def load_users(users):
    '''Creates Example Users, Habits and Check-ins in memory from database.'''
    api.db_view()
    db_users = api.db_get_users()
    print(f'[🔍] Loaded {len(db_users)} available users from sqlite3 database...')
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
    print(f'[✔️] Habit Tracker fully initialized!')
    sleep(2)
    

def default_example_data():
    '''Return example data to a provided user when resetting!'''
    return [
        [
           'Cardio Workout', 'Cardio Activities','3D',True,None,1,'Sport','To become lean and more stamina',5,5,0,False,0
        ],[
           'Weight Lifting', 'Muscle workout','2D',True,None,4,'Sport','For power in body',5,5,0,False,0
        ]
    ]

def load_user_data(users,user_id):
    '''The load_user_data function receives the loggedin user and then fetches the latest local database to insert users habits and checkins. Its main purpose is to load data from storage to memory while the program operates.'''
     #For each example user class now, create example habits and overwrite with database values.
    habits = api.db_get_habits(user_id)
    checkins = api.db_get_checkins(user_id)

    h_index = 0
    c_index = 0
    try:
        for u in users.users:
            #Find the user that is logging in
            if(user_id == u.user_id):

                #Go over all habits that got send from the database for this user
                for h in habits:
                    #The database sends them in a list, for convenience the list is parsed into a dict model for easier access to the different attributes
                    hm = Habit_Model(h)
                    #Create new habit but then use overwrite to fill out all database values, basically a temporary place holder.
                    u.create_habit(hm['title'],hm['description'],hm['interval'],hm['active'],hm['start_from'],hm['difficulity'],hm['category'],hm['moto'],hm['importance'],hm['milestone_streak'],hm['style'],hm['is_dynamic'],hm['checkin_num_before_deadline'])
                    #Overwrite the habit instance with current db values
                    u.habits[h_index].overwrite(
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
                    for c in checkins:
                        #Convert the database tuple into a dict using the model
                        cm = Checkin_Model(c)
                        if cm['habit_id'] == u.habits[h_index].habit_id:
                            #Create placeholder checkin
                            u.habits[h_index].checkins.append(CheckIn(cm['user_id'],cm['habit_id'],cm['checkin_id'],cm['deadline'],cm['success'],cm['note'],cm['rating'],cm['cost'],cm['cost_accum'],cm['dynamic'],cm['dynamic_count']))
                            u.habits[h_index].checkins[c_index].overwrite(cm['user_id'],cm['habit_id'],cm['checkin_id'],cm['checkin_datetime'],cm['deadline'],cm['success'],cm['note'],cm['rating'],cm['cost_accum'],cm['dynamic'],cm['dynamic_count'])
                        c_index += 1

                    #Increas h_index and move to next habit for user
                    h_index += 1

    except Exception as e:
        print("[❌] Fail in load_user_data: ",e)
        traceback.print_exc()

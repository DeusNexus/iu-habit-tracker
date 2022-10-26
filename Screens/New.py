import os
import questionary as quest
from time import sleep
from datetime import datetime
from Database import db_api as api
from Utils import interval_to_seconds

#Function to Clear Terminal
clear = lambda : os.system('tput reset')

def new(state):
    '''The new screen is used for creating new habits, which can be normal or dynamic. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print('[New Screen]')
    questions = ['Regular Habit - Fixed Deadlines','Dynamic Habit - Specify how often to check in before deadline'] + ['Go Back to User Screen']
    ans = quest.select('Choose what kind of Habit you want to create:', questions).ask()

    def questionary(is_dynamic:bool):
        #user input
        title_ask = interval_ask = milestone_ask = checkin_num_before_deadline_ask = True

        while(title_ask):
            title = quest.text('What will be the title of the new habit? E.g. Gym Workout').ask()
            if len(title) > 2: 
                title_ask = False
            else:
                print('Please use 3 or more characters for a title!')

        description = quest.text('Provide a description? E.g. Leg day').ask()

        while(interval_ask):
            interval = quest.text('Define an interval for the habit. You can use any whole number followed by m/H/D/W/M/Y; e.g. 3D or 1W or 30m').ask()
            try :
                interval_to_seconds(interval)
                interval_ask = False
            except ValueError:
                print('Please input a valid interval format. E.g: <int><char> like 15m, 2H, 5D, 1W, 6M, 2Y')

        if(is_dynamic):
            while(checkin_num_before_deadline_ask):
                checkin_num_before_deadline = quest.text('How often do you want to perform the habit before a deadline? Type an integer numer; e.g. 1, 3, 5').ask()
                if(type(int(checkin_num_before_deadline)) == int):
                    checkin_num_before_deadline_ask = False
                else:
                    print('Please use an integer value for how many times you need to checkin before the deadline. E.g. 1, 3, 10')
        else:
            checkin_num_before_deadline = 1

        optional = quest.confirm("Fill out optional fields? E.g. active, difficulity, category, moto, importance, milestone target.").ask()

        #No optional questions -> Fill default values
        if(not optional):
            active = True
            start_from = datetime.now()
            difficulity = None
            category = None
            moto = None
            importance = None
            milestone = None
            style = 0

        #If optional is True, fill out more details
        else:
            active = quest.confirm("Do you directly want to set the habit to active?").ask()

            if(active):
                start_from = datetime.now()
            else:
                start_from = quest.text('Provide a start date when you want it to become active? Please follow the format YYYY/MM/DD HH:mm, e.g. 2050/03/28 15:35.').ask()

            difficulity = quest.select("How difficult do you find it to perform?",['1','2','3','4','5']).ask()

            category = quest.text('Do you want to assign this habit to a common category? Similar habits will be grouped together. E.g.: Eduction, Sport, Hobby').ask()

            moto = quest.text('What is your moto you would like to remind yourself of to keep doing the habit?').ask()

            importance = quest.select("How important do you find it to perform?",['1','2','3','4','5']).ask()

            while(milestone_ask):
                milestone = quest.text("Set milestone target for multiple successes. E.g. 5 for 5 consequent succesfull checkins!").ask()
                if(type(int(milestone)) == int):
                    milestone_ask = False
                else:
                    print("Use an integer to specify the milestone target.")
            
            style = 0

        #Create habit with user input
        try:
            habit_index = len(state["active_user"].habits)
            #When habit_id = None is passed it automatically generates one.
            state["active_user"].create_habit(title, description, interval, active, start_from, difficulity, category, moto, importance, milestone, style, is_dynamic, checkin_num_before_deadline,None)
            api.db_habits_insert([
                {
                    'user_id':state["active_user"].user_id,
                    'habit_id':state["active_user"].habits[habit_index].habit_id,
                    'title':title,
                    'description':description,
                    'interval':interval,
                    'active':'True' if active else 'False',
                    'start_from':start_from,
                    'difficulity':difficulity,
                    'category':category,
                    'moto':moto,
                    'importance':importance,
                    'style':style,
                    'milestone_streak':milestone,
                    'is_dynamic':'True' if is_dynamic else 'False',
                    'checkin_num_before_deadline':checkin_num_before_deadline,
                    'dynamic_count':state["active_user"].habits[habit_index].dynamic_count,
                    'created_on':state["active_user"].habits[habit_index].created_on,
                    'prev_deadline':state["active_user"].habits[habit_index].prev_deadline,
                    'next_deadline':state["active_user"].habits[habit_index].next_deadline,
                    'streak':state["active_user"].habits[habit_index].streak,
                    'success':state["active_user"].habits[habit_index].success,
                    'fail':state["active_user"].habits[habit_index].fail,
                    'cost':state["active_user"].habits[habit_index].cost,
                    'cost_accum':state["active_user"].habits[habit_index].cost_accum
                }
            ])
            print('[*] Added your habit!')
        except Exception as e:
            print('[!] Failed to add habit, an error occured!')
            print(e)

    
    #Regular habit
    if(ans == questions[0]):
        sleep(1*state["SLEEP_SPEED"])
        questionary(is_dynamic=False)

        #Show habit before submit? Then return to user screen
        sleep(1*state["SLEEP_SPEED"])
        print('[!] Returning back to User Screen...')
        sleep(1*state["SLEEP_SPEED"])
        state["user_screen"](state)

    #Dynamic Habit
    elif(ans == questions[1]):
        sleep(1*state["SLEEP_SPEED"])
        questionary(is_dynamic=True)

        #Show habit before submit? Then return to user screen
        sleep(1*state["SLEEP_SPEED"])
        print('[!] Returning back to User Screen...')
        sleep(1*state["SLEEP_SPEED"])
        state["user_screen"](state)

    elif(ans == 'Go Back to User Screen'):
        clear()
        sleep(1*state["SLEEP_SPEED"])
        print('[!] Returning back to User Screen...')
        sleep(1*state["SLEEP_SPEED"])
        state["user_screen"](state)
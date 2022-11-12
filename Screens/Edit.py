import os
import questionary as quest
from time import sleep
from datetime import datetime
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

from Database.db_api import db_update_habit
from Utils import interval_to_seconds

#User to return to the user screen
def return_user_screen(state):
    sleep(1*state["SLEEP_SPEED"])
    print('[!] Returning back to User Screen...')
    sleep(1*state["SLEEP_SPEED"])
    clear()
    state["user_screen"](state)

#Print the edit information and options, go through questionary style input and check input values for validity.
def edit(state):
        '''The edit screen is used for editing habits. Habits can be set to active or inactive, and have their unique details changed. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
        clear()
        print('[Edit Screen]')

        #User has no habits, so return back to user screen.
        if( len(state["active_user"].habits) == 0 ): 
            print('You currently do not have any habits to edit!')
            return_user_screen(state)

        #User has habits, show list of habits to edit.
        else:
            ans = quest.select('Which habit would you like to edit?', [habit.title for habit in state["active_user"].habits] + ['Go Back to User Screen'],style=state['qstyle']).ask()
            
            if(ans == 'Go Back to User Screen'):
                return_user_screen(state)

            #Make variable for current habit for easy access
            curr_habit = None
            for habit in state["active_user"].habits:
                if habit.title == ans:
                    curr_habit = habit

            #Edit options to choose from
            habit_attr = [
                "title",
                "description",
                "interval",
                "active",
                "start_from",
                "difficulity",
                "category",
                "moto",
                "importance",
                "milestone_streak",
                "cost"
            ]

            #unique attribute for dynamic habit
            dynamic_attr = [
                "checkin_num_before_deadline"
            ]
            
            #Stay in the edit loop until edit is set to False
            editing = True
            while(editing and curr_habit):
                clear()
                print(f"[Overview of {'Dynamic' if curr_habit.is_dynamic else 'Regular'} Habit Attributes]")
                if(habit.is_dynamic):
                    for attr in habit_attr:
                        print(f"   {attr}: {getattr(curr_habit,attr)}")
                else:
                    for attr in (habit_attr + dynamic_attr):
                        #For regular habit don't print out the dynamic counter, also hidden from edit options
                        if(not attr=='checkin_num_before_deadline'):
                            print(f"   {attr}: {getattr(curr_habit,attr)}")
                
                anw_attr = quest.select('\nWhich habit attribute would you like to edit?', habit_attr+['[Return]'],style=state['qstyle']).ask()

                if(anw_attr == '[Return]'):
                    editing = False
                    clear()
                    #Go back to edit
                    edit(state)

                ## Attributes to edit and update in database / in-memory
                if(anw_attr == 'title'):
                    ans_title = quest.text('What new title would you want to give to this habit?',style=state['qstyle']).ask()
                    curr_habit.title = ans_title
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_title)

                elif(anw_attr == 'description'):
                    ans_description = quest.text('What new description would you want to give to this habit?',style=state['qstyle']).ask()
                    curr_habit.description = ans_description
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_description)

                elif(anw_attr == 'interval'):
                    interval_ask = True
                    while(interval_ask):
                        try:
                            ans_interval = quest.text('What new interval would you want to give to this habit?',style=state['qstyle']).ask()
                            #Test for valid interval
                            interval_to_seconds(ans_interval)
                            
                            curr_habit.interval = ans_interval
                            db_update_habit(curr_habit.habit_id,anw_attr,ans_interval)
                            interval_ask = False
                        except ValueError as e:
                            print('Please input a valid interval format. E.g: <int><char> like 15m, 2H, 5D, 1W, 6M, 2Y')

                elif(anw_attr == 'active'):
                    ans_active = quest.confirm('To what would you like to set active to?',style=state['qstyle']).ask()
                    curr_habit.active = ans_active
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_active)

                elif(anw_attr == 'start_from'):
                    start_from_ask=True
                    while(start_from_ask):
                        try:
                            start_from_res = quest.text('Provide a start date when you want it to become active? Please follow the format YYYY-MM-DD HH:mm, e.g. 2050-03-28 15:35.',style=state['qstyle']).ask()
                            ans_start_from = datetime.strptime(start_from_res+'.000001', "%Y-%m-%d %H:%M:%S.%f")
                            curr_habit.start_from = ans_start_from
                            db_update_habit(curr_habit.habit_id,anw_attr,ans_start_from)
                            start_from_ask = False
                        except ValueError as e:
                            print('Please provide a valid date in the format YYYY-MM-DD HH:MM:SS, e.g. 2030-01-28 12:13:14')

                elif(anw_attr == 'difficulity'):
                    ans_difficulity = quest.select('What new difficulity would you want to give to this habit?',['1','2','3','4','5'],style=state['qstyle']).ask()
                    curr_habit.difficulity = ans_difficulity
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_difficulity)

                elif(anw_attr == 'category'):
                    ans_category = quest.text('What new category would you want to give to this habit?',style=state['qstyle']).ask()
                    curr_habit.category = ans_category
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_category)

                elif(anw_attr == 'moto'):
                    ans_moto = quest.text('What new moto would you want to give to this habit?',style=state['qstyle']).ask()
                    curr_habit.moto = ans_moto
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_moto)

                elif(anw_attr == 'importance'):
                    ans_importance = quest.select('What new importance would you want to give to this habit?',['1','2','3','4','5'],style=state['qstyle']).ask()
                    curr_habit.importance = ans_importance
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_importance)

                elif(anw_attr == 'milestone_streak'):
                    milestone_streak_ask=True
                    while(milestone_streak_ask):
                        try:
                            ans_milestone_streak = int(quest.text('What new milestone streak would you want to give to this habit? \nFor example you want to checkin daily, if you reach 30 milestone you have checked in successfully every day for 30 days.',style=state['qstyle']).ask())
                            if(ans_milestone_streak < 1):
                                print('You need to specify a milestone of atleast 1 or higher.')
                            else:
                                curr_habit.milestone_streak = ans_milestone_streak
                                db_update_habit(curr_habit.habit_id,anw_attr,ans_milestone_streak)
                                milestone_streak_ask = False
                        except ValueError as e:
                            print("Use an integer to specify the milestone target.")

                elif(anw_attr == 'cost'):
                    cost_ask=True
                    while(cost_ask):
                        try:
                            ans_cost = float(quest.text('What will be the new cost for your habit? Accumulated value does not change but new cost value will be added.',style=state['qstyle']).ask())
                            if(not ans_cost > 0):
                                print('Please specify a positive number for the cost.')
                            else:
                                curr_habit.cost = ans_cost
                                db_update_habit(curr_habit.habit_id,anw_attr,ans_cost)
                                cost_ask = False
                        except ValueError as e:
                            print("Use a correct float number to define your habit cost! E.g.: 1, 2.50, 9.99")

                elif(anw_attr == 'checkin_num_before_deadline' and habit.is_dynamic):
                    checkin_num_before_deadline_ask=True
                    while(checkin_num_before_deadline_ask):
                        try:
                            ans_checkin_num_before_deadline = int(quest.text('What dynamic checking target would you like to set for this habit?',style=state['qstyle']).ask())
                            if(not ans_checkin_num_before_deadline > 0):
                                print('Provide a integer that is larger than 0!')
                            else:
                                curr_habit.checkin_num_before_deadline = ans_checkin_num_before_deadline
                                db_update_habit(curr_habit.habit_id,anw_attr,ans_checkin_num_before_deadline)
                                checkin_num_before_deadline_ask=False
                        except ValueError as e:
                            print('Provide a valid integer for checkin number before deadline!')
                
                
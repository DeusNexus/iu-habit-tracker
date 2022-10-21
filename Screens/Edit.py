import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')
from Database.db_api import db_update_habit

from Constants import SLEEP_SPEED

def edit(active_user,user_screen,app):
        '''The edit screen is used for editing habits. Habits can be set to active or inactive, and have their unique details changed. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
        clear()
        print('[Edit Screen]')

        #User has no habits, so return back to user screen.
        if( len(active_user.habits) == 0 ): 
            print('You currently do not have any habits to edit!')
            sleep(1*SLEEP_SPEED)
            print('[!] Returning to User Screen...')
            sleep(2*SLEEP_SPEED)
            clear()
            user_screen(active_user,app)

        #User has habits, show list of habits to edit.
        else:
            ans = quest.select('Which habit would you like to edit?', [habit.title for habit in active_user.habits] + ['Go Back to User Screen']).ask()
            
            if(ans == 'Go Back to User Screen'):
                print('[!] Returning to User Screen...')
                sleep(2*SLEEP_SPEED)
                clear()
                user_screen(active_user,app)

            #Make variable for current habit for easy access
            curr_habit = None
            for habit in active_user.habits:
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
                "style",
            ]

            dynamic_attr = [
                "checkin_num_before_deadline"
            ]

            editing = True
            while(editing):
                clear()
                print(f"[Overview of {'Dynamic' if curr_habit.is_dynamic else ''} Habit Attributes]")
                if(habit.is_dynamic):
                    for attr in habit_attr:
                        print(f"   {attr}: {getattr(curr_habit,attr)}")
                else:
                    for attr in (habit_attr + dynamic_attr):
                        print(f"   {attr}: {getattr(curr_habit,attr)}")
                
                anw_attr = quest.select('\nWhich habit attribute would you like to edit?', habit_attr+['[Return]']).ask()

                if(anw_attr == '[Return]'):
                    editing = False
                    print('[!] Returning to User Screen...')
                    sleep(2*SLEEP_SPEED)
                    clear()
                    user_screen(active_user,app)

                ## Attributes to edit and update in database / in-memory
                if(anw_attr == 'title'):
                    ans_title = quest.text('What new title would you want to give to this habit?').ask()
                    curr_habit.title = ans_title
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_title)

                elif(anw_attr == 'description'):
                    ans_description = quest.text('What new description would you want to give to this habit?').ask()
                    curr_habit.description = ans_description
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_description)

                elif(anw_attr == 'interval'):
                    ans_interval = quest.text('What new interval would you want to give to this habit?').ask()
                    curr_habit.interval = ans_interval
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_interval)

                elif(anw_attr == 'active'):
                    ans_active = quest.confirm('To what would you like to set active to?').ask()
                    curr_habit.active = ans_active
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_active)

                elif(anw_attr == 'start_from'):
                    ans_start_from = quest.text('Provide a new starting date in the format, MM-DD-YYYY HH:MM:SS. E.g.: 03-27-2025 12:30:45?').ask()
                    curr_habit.start_from = ans_start_from
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_start_from)

                elif(anw_attr == 'difficulity'):
                    ans_difficulity = quest.select('What new difficulity would you want to give to this habit?',['1','2','3','4','5']).ask()
                    curr_habit.difficulity = ans_difficulity
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_difficulity)

                elif(anw_attr == 'category'):
                    ans_category = quest.text('What new category would you want to give to this habit?').ask()
                    curr_habit.category = ans_category
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_category)

                elif(anw_attr == 'moto'):
                    ans_moto = quest.text('What new moto would you want to give to this habit?').ask()
                    curr_habit.moto = ans_moto
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_moto)

                elif(anw_attr == 'importance'):
                    ans_importance = quest.select('What new importance would you want to give to this habit?',['1','2','3','4','5']).ask()
                    curr_habit.importance = ans_importance
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_importance)

                elif(anw_attr == 'milestone_streak'):
                    ans_milestone_streak = quest.text('What new milestone streak would you want to give to this habit? \nFor example you want to checkin daily, if you reach 30 milestone you have checked in successfully every day for 30 days.').ask()
                    curr_habit.milestone_streak = ans_milestone_streak
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_milestone_streak)

                elif(anw_attr == 'style'):
                    ans_style = quest.select('What new style would you want to give to this habit?',['0','1']).ask()
                    curr_habit.style = ans_style
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_style)

                elif(anw_attr == 'checkin_num_before_deadline' and habit.is_dynamic):
                    ans_checkin_num_before_deadline = quest.text('What dynamic checking target would you like to set for this habit?').ask()
                    curr_habit.checkin_num_before_deadline = ans_checkin_num_before_deadline
                    db_update_habit(curr_habit.habit_id,anw_attr,ans_checkin_num_before_deadline)
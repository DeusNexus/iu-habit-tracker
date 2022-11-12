import os
import questionary as quest
from time import sleep
from datetime import datetime
#Function to Clear Terminal
clear = lambda : os.system('tput reset')
import traceback

#Screens
from Screens.View import view
from Screens.Habit_Checkin import habit_checkin
from Screens.New import new
from Screens.Edit import edit
from Screens.Delete import delete
from Screens.ExportImport import export_import
from Screens.Reset import reset
from Screens.Credits import credits
from Screens.Logout import logout

from Classes.Analytics import earliest

#Text Styling
from Utils import style

#Update new active habits
from Database.db_api import db_update_habit

#The user screen acts as the main menu after a user logs-in to his personal account.
def user_screen(state):
    '''The user screen acts as the main menu for the user. The user_screen function receives the User-object of the logged-in user and passes it further to the individual menu views. The individual views can then access user data and execute user functions.'''
    try:
        #Clear the cli text
        clear()
        sleep(1*state["SLEEP_SPEED"])
        
        #Print welcome statement
        print(style('[USER SCREEN]','UNDERLINE'))
        print(style(f'\nWelcome back {state["active_user"].name}, {("your last login was on " + state["active_user"].last_login.strftime("%A %d-%m-%Y, %H:%M")) if type(state["active_user"].last_login) == datetime else "this is the first time you login! This is a great way to keep building your habits, good luck."}.','YELLOW'))
        print(
            '\nYou currently have '+
            style(f'{len([habit for habit in state["active_user"].habits if habit.active])} active','GREEN') + 
            ' and '+
            style(f'{len([habit for habit in state["active_user"].habits if not habit.active])} inactive','CYAN')+
            ' habits.')

        #Habits that turned active
        new_active = False
        new_active_habits = []
        for habit in state['active_user'].habits:
            if not habit.active and datetime.now() > habit.start_from:
                habit.update_deadline_now_active()
                habit.active = True
                db_update_habit(habit.habit_id, 'active', 'True')
                db_update_habit(habit.habit_id, 'prev_deadline', habit.prev_deadline)
                db_update_habit(habit.habit_id, 'next_deadline', habit.next_deadline)
                new_active_habits.append(habit)
                new_active = True
        if new_active:
            print(style('\nThe following habit(s) just turned their status to active:','YELLOW'))
            for r in new_active_habits:
                print(style(f'[{r.title}] active from {r.start_from.strftime("%A %d-%m-%Y, %H:%M")} and', 'BOLD') + style(f' deadline on {r.next_deadline.strftime("%A %d-%m-%Y, %H:%M")}', 'YELLOW'))
            print('')


        #Find earliest habit for user to meet deadline for.
        if state["active_user"].habits:
            earliest_deadline = earliest(state["active_user"].habits)
            print(
                f'Next earliest '+
                style('deadline','RED')+
                ' for '+
                style(f'"{earliest_deadline.title}"','RED')+
                ' is on '+
                style(f'{earliest_deadline.next_deadline.strftime("%A %d-%m-%Y, %H:%M")}','YELLOW')+
                ', please check-in if you have completed it or your streak will reset!')
        
        #Show menu options
        print(f'\nPlease select one of the menu options to interact with the habit tracker.\n')
        option = quest.select('[User Screen Options]', ['View','Checkin','New','Edit','Delete','Export/Import','Reset','See Credits','Logout'],style=state['qstyle']).ask()

        if(option == 'View'):
            view(state)
        elif(option == 'Checkin'):
            habit_checkin(state)
        elif(option == 'New'):
            new(state)
        elif(option == 'Edit'):
            edit(state)
        elif(option == 'Delete'):
            delete(state)
        elif(option == 'Export/Import'):
            export_import(state)
        elif(option == 'Reset'):
            reset(state)
        elif(option == 'See Credits'):
            credits(state)
        elif(option == 'Logout'):
            logout(state)
            
    except Exception as e:
        print(e)
        traceback.print_exc()
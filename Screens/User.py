import os
import questionary as quest
from time import sleep
import datetime as datetime
#Function to Clear Terminal
clear = lambda : os.system('tput reset')
import traceback

#Screens
from Screens.View import view
from Screens.New import new
from Screens.Edit import edit
from Screens.Delete import delete
from Screens.ExportImport import export_import
from Screens.Reset import reset
from Screens.Credits import credits
from Screens.Logout import logout

from Classes.Analytics import earliest

#The user screen acts as the main menu after a user logs-in to his personal account.
def user_screen(state):
    '''The user screen acts as the main menu for the user. The user_screen function receives the User-object of the logged-in user and passes it further to the individual menu views. The individual views can then access user data and execute user functions.'''
    try:
        clear()
        sleep(1*state["SLEEP_SPEED"])
        
        print(f'\nWelcome back {state["active_user"].name}, {("your last login was on " + state["active_user"].last_login.strftime("%A %d-%m-%Y, %H:%M")) if type(state["active_user"].last_login) == datetime.datetime else "this is the first time you login! This is a great way to keep building your habits, good luck."}.')
        print(f'\nYou currently have {len([habit for habit in state["active_user"].habits if habit.active])} active and {len([habit for habit in state["active_user"].habits if not habit.active])} inactive habits.')


        if state["active_user"].habits:
            earliest_deadline = earliest(state["active_user"].habits)
            print(f'Next earliest deadline for "{earliest_deadline.title}" is on {earliest_deadline.next_deadline.strftime("%A %d-%m-%Y, %H:%M")}, please check-in if you have completed it or your streak will reset!')

        print(f'\nPlease select one of the menu options to interact with the habit tracker.\n')
        
        #Screens
        option = quest.select('[User Screen Options]', ['View','New','Edit','Delete','Export/Import','Reset','See Credits','Logout']).ask()

        if(option == 'View'):
            view(state)
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
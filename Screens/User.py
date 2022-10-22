import os
import questionary as quest
from time import sleep
import datetime as datetime
#Function to Clear Terminal
clear = lambda : os.system('tput reset')
import traceback

from Constants import SLEEP_SPEED

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
def user_screen(active_user,app):
    '''The user screen acts as the main menu for the user. The user_screen function receives the User-object of the logged-in user and passes it further to the individual menu views. The individual views can then access user data and execute user functions.'''
    try:
        clear()
        sleep(1*SLEEP_SPEED)
        
        print(f'\nWelcome back {active_user.name}, {("your last login was on " + active_user.last_login.strftime("%A %d-%m-%Y, %H:%M")) if type(active_user.last_login) == datetime.datetime else "this is the first time you login! This is a great way to keep building your habits, good luck."}.')
        print(f'\nYou currently have {len([habit for habit in active_user.habits if habit.active])} active and {len([habit for habit in active_user.habits if not habit.active])} inactive habits.')


        if active_user.habits:
            earliest_deadline = earliest(active_user.habits)
            print(f'Next earliest deadline for "{earliest_deadline.title}" is on {earliest_deadline.next_deadline.strftime("%A %d-%m-%Y, %H:%M")}, please check-in if you have completed it or your streak will reset!')

        print(f'\nPlease select one of the menu options to interact with the habit tracker.\n')
        
        #Screens
        option = quest.select('[User Screen Options]', ['View','New','Edit','Delete','Export/Import','Reset','See Credits','Logout']).ask()

        if(option == 'View'):
            view(active_user,user_screen,app)
        elif(option == 'New'):
            new(active_user,user_screen,app)
        elif(option == 'Edit'):
            edit(active_user,user_screen,app)
        elif(option == 'Delete'):
            delete(active_user,user_screen,app)
        elif(option == 'Export/Import'):
            export_import(active_user,user_screen,app)
        elif(option == 'Reset'):
            reset(active_user,user_screen,app)
        elif(option == 'See Credits'):
            credits(active_user,user_screen,app)
        elif(option == 'Logout'):
            logout(active_user,app)
            
    except Exception as e:
        print(e)
        traceback.print_exc()
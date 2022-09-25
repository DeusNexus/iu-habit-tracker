import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

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
def user_screen(active_user):
    '''The user screen acts as the main menu for the user. The user_screen function receives the User-object of the logged-in user and passes it further to the individual menu views. The individual views can then access user data and execute user functions.'''
    try:
        clear()
        sleep(1)


        print(f'\nWelcome back {active_user.name}, your last login was on {active_user.last_login.strftime("%A %d-%m-%Y, %H:%M")}.')
        print(f'\nYou currently have {len([habit for habit in active_user.habits if habit.active])} active and {len([habit for habit in active_user.habits if not habit.active])} inactive habits.')


        if active_user.habits:
            earliest_deadline = earliest(active_user.habits)
            print(f'Next earliest deadline for "{earliest_deadline.title}" is on {earliest_deadline.next_deadline.strftime("%A %d-%m-%Y, %H:%M")}, please check-in if you have completed it or your streak will reset!')

        print(f'\nPlease select one of the menu options to interact with the habit tracker.\n')
        
        #Screens
        option = quest.select('[User Screen Options]', ['View','New','Edit','Delete','Export/Import','Reset','See Credits','Logout & Exit']).ask()

        if(option == 'View'):
            view(active_user,user_screen)
        elif(option == 'New'):
            new(active_user,user_screen)
        elif(option == 'Edit'):
            edit(active_user,user_screen)
        elif(option == 'Delete'):
            delete(active_user,user_screen)
        elif(option == 'Export/Import'):
            export_import(active_user,user_screen)
        elif(option == 'Reset'):
            reset(active_user,user_screen)
        elif(option == 'See Credits'):
            credits(active_user,user_screen)
        elif(option == 'Logout & Exit'):
            logout(active_user)
            
    except Exception as e:
        print(e)
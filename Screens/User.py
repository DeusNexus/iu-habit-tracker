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

def user_screen(active_user):
    clear()
    sleep(1)
    
    print(f'\nWelcome back {active_user.name}, your last login was on {active_user.last_login}.')
    print(f'You currently have {len(active_user.habits)} habits of which ...\n')
    print(f'Please select one of the menu options to interact with the habit tracker.\n')
    
    #Screens
    option = quest.select('[User Screen Options]', ['View','New','Edit','Delete','Export/Import','Reset','See Credits','Logout & Exit']).ask()

    try:
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
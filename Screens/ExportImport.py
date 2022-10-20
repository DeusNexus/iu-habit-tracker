import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

SLEEP_SPEED=0

def export_import(active_user,user_screen):
    '''The export/import screen is used for importing or exporting a user account using json files. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print('[Export/Import Screen]\n')
    print('You have options to either export your user file as a json file or import it by giving the file path.')
    print('If you choose export, the file will be saved in the same directory as the habit tracker.')
    print('If you wish to import a file, it is recommened to drop it into the habit tracker directory so it can be easily found.')
    print('Once in the directory you can select the filename of the supported files.\n\n')
    questions = ['Export My Account', 'Import Account', 'Go Back to User Screen']
    ans = quest.select('What do you want to do?', questions).ask()
    if(ans==questions[0]):
        sleep(1*SLEEP_SPEED)
        pass
    elif(ans==questions[1]):
        sleep(1*SLEEP_SPEED)
        pass
    elif(ans==questions[2]):
        sleep(1*SLEEP_SPEED)
        print('[!] Returning to User Screen...')
        sleep(2*SLEEP_SPEED)
        clear()
        user_screen(active_user)
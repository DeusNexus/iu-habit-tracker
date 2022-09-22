import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

def edit(active_user,user_screen):
        clear()
        print('[Edit Screen]')
        if( len(active_user.habits) == 0 ): 
            print('You currently do not have any habits to edit!')
            sleep(1)
            print('[!] Returning to User Screen...')
            sleep(2)
            clear()
            user_screen(active_user)
        else:
            ans = quest.select('Which habit would you like to edit?', active_user.habits).ask()
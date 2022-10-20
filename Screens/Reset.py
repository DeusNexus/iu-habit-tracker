import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

SLEEP_SPEED=0

def reset(active_user,user_screen):
    '''The reset screen is used for resetting the user to various default states. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print('[Reset Screen]')
    print('In case that you would like to completely reset your account then you can make use of this menu.\n')
    sleep(1*SLEEP_SPEED)
    print('You have two options, either delete all your creation date, login time, habits and then have example habit data loaded again \n')
    sleep(1*SLEEP_SPEED)
    print('or everything gets reset like stated above and no example data is added so you can start with your own personal journey.')
    sleep(1*SLEEP_SPEED)
    questions = ['Full Reset with Example Data', 'Full Reset without Example Data', 'Go Back to User Screen']
    ans = quest.select('What would you like to do?',questions).ask()
    if(ans==questions[0]):
        sleep(1*SLEEP_SPEED)
        pass
    elif(ans==questions[1]):
        sleep(1*SLEEP_SPEED)
        pass
    elif(ans==questions[2]):
        clear()
        sleep(1*SLEEP_SPEED)
        print('Returning back to User Screen...')
        sleep(1*SLEEP_SPEED)
        user_screen(active_user)
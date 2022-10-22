import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

from Database import db_api as api

def reset(state):
    '''The reset screen is used for resetting the user to various default states. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print('[Reset Screen]')
    print('In case that you would like to completely reset your account then you can make use of this menu.\n')
    sleep(1*state["SLEEP_SPEED"])
    print('You have two options, either delete all your creation date, login time, habits and then have example habit data loaded again \n')
    sleep(1*state["SLEEP_SPEED"])
    print('or everything gets reset like stated above and no example data is added so you can start with your own personal journey.')
    sleep(1*state["SLEEP_SPEED"])
    questions = ['Full Reset with Example Data', 'Full Reset without Example Data', 'Go Back to User Screen']
    ans = quest.select('What would you like to do?',questions).ask()
    
    #Full Reset with Example Data
    if(ans==questions[0]):
        sleep(1*state["SLEEP_SPEED"])
        pass

    #Full Reset withou Example Data
    elif(ans==questions[1]):
        sleep(1*state["SLEEP_SPEED"])
        api.db_reset_user_full(state["active_user"].user_id)
        sleep(1)
        print('Reloading application, please login again to your fully resetted account.')
        sleep(3)
        clear()

        #Clear out the in-memory objects, user will get their data loaded when they successfully login.
        state["active_user"] = None
        for u in state["users"].users:
            u.habits = []
        
        #Return to login-screen to load resetted user from database so in-memory is consistent with db.
        state["app"](skip=True)
        pass

    #Go back to user screen
    elif(ans==questions[2]):
        clear()
        sleep(1*state["SLEEP_SPEED"])
        print('[!] Returning back to User Screen...')
        sleep(1*state["SLEEP_SPEED"])
        state["user_screen"](state)
        pass
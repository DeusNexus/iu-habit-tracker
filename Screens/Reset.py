import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

from Database import db_api as api

#Text Styling
from Utils import style

#Returns to user screen
def return_user_screen(state):
    sleep(1*state["SLEEP_SPEED"])
    print('[!] Returning back to User Screen...')
    sleep(1*state["SLEEP_SPEED"])
    clear()
    state["user_screen"](state)

#Returns to main app (to reload the app from database and login again)
def return_app(state):
    state["active_user"].reset()
    sleep(1)
    print('Reloading application, please login again to your resetted account.')
    sleep(3)
    clear()
    
    #Return to login-screen to load resetted user from database so in-memory is consistent with db.
    state["app"](skip=True)

#Do reset print and show options
def reset(state):
    '''The reset screen is used for resetting the user to various default states. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print(style('[Reset Screen]','UNDERLINE'))
    print(style('In case that you would like to completely reset your account then you can make use of this menu.','RED'))
    sleep(1*state["SLEEP_SPEED"])
    print(style('You have two options, either delete all your habits and checkins and then have example habit data loaded again','RED'))
    sleep(1*state["SLEEP_SPEED"])
    print(style('or everything gets reset like stated above and no example data is added so you can start with your own personal journey.\n','RED'))
    sleep(1*state["SLEEP_SPEED"])
    questions = ['Full Reset with Example Data', 'Full Reset without Example Data', 'Go Back to User Screen']
    ans = quest.select('What would you like to do?',questions,style=state['qstyle']).ask()
    
    #Full Reset with Example Data
    if(ans==questions[0]):
        api.db_reset_user_example_data(state["active_user"].user_id)
        state["active_user"].reset()
        return_app(state)

    #Full Reset withou Example Data
    elif(ans==questions[1]):
        api.db_reset_user_full(state["active_user"].user_id)
        state["active_user"].reset()
        return_app(state)

    #Go back to user screen
    elif(ans==questions[2]):
        return_user_screen(state)
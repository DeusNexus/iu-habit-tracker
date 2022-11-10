import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

#Logout the user and return to the login screen (while skipping to ask if you are new user skip=True)
def logout(state):
        '''The logout screen exits the User screen and greets with a goodbye message and finally calls the app(skip=True) function that renders the login screen and skips asking to create a new user. It receives the User-object, active_user, and app to access the user data and start the application from the login screen.'''
        clear()
        print(f'Dear {state["active_user"].name} it was good to see you. Your account will be logged out and return to the login screen. Hope to see you back soon!')
        sleep(2*state["SLEEP_SPEED"])
        print('Logging out ...')
        for i in range(3):
            print(f'.... in {3-i} ....')
            sleep(1*state["SLEEP_SPEED"])
        clear()
        state["app"](skip=True)
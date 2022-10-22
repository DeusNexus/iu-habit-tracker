import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

from Constants import SLEEP_SPEED

def logout(active_user,app):
        '''The logout screen exits the User screen and greets with a goodbye message and finally calls the app(skip=True) function that renders the login screen and skips asking to create a new user. It receives the User-object, active_user, and app to access the user data and start the application from the login screen.'''
        clear()
        print(f'Dear {active_user.name} it was good to see you. Your account will be logged out and return to the login screen. Hope to see you back soon!')
        sleep(2*SLEEP_SPEED)
        print('Logging out ...')
        for i in range(3):
            sleep(1*SLEEP_SPEED)
            print(f'.... in {3-i} ....')
        clear()
        app(skip=True)
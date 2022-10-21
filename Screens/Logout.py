import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

from Constants import SLEEP_SPEED

def logout(active_user,app):
        '''The logout screen exits the User screen and greets a goodbye message and finally terminates the habit tracker application. It receives the User-object, active_user, to access the user data.'''
        clear()
        print(f'Dear {active_user.name} it was good to see you. Your account will be logged out and the application will terminate. Hope to see you back soon!')
        sleep(2*SLEEP_SPEED)
        print('Logging out ...')
        for i in range(3):
            sleep(1*SLEEP_SPEED)
            print(f'.... in {3-i} ....')
        app(skip=True)
        # print('Habit Tracker exited successfully.')
        # exit()
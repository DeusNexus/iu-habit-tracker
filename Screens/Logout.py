import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

def logout(active_user):
        clear()
        print(f'Dear {active_user.name} it was good to see you. Your account will be logged out and the application will terminate. Hope to see you back soon!')
        sleep(2)
        print('Logging out and Exiting application in ...')
        for i in range(3):
            sleep(1)
            print(f'.... in {3-i} ....')
        print('Habit Tracker exited successfully.')
        exit()
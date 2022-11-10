import os
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

# Get the size
# of the terminal
columns,lines = os.get_terminal_size()

#Return to the user screen
def return_user_screen(state):
    sleep(1*state["SLEEP_SPEED"])
    print('[!] Returning back to User Screen...')
    sleep(1*state["SLEEP_SPEED"])
    clear()
    state["user_screen"](state)

#Display credits
def credits(state):
    '''The credits screen is used for showing credits of the creator, course and the university name and returns afterwards back to user screen. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print('[Credit Screen]')
    plines = []
    for i in range(lines):
        if(i < lines//2):
            plines.append((i * (columns//lines) * '.' + ' Created by Fabian Menne - 2022'))
        else:
            plines.append(((lines-i) * (columns//lines) * '.' + ' Created by Fabian Menne - 2022'))
    for line in plines:
        print(line)
        sleep(0.1*state["SLEEP_SPEED"])
    print('\nThank you for checking out the Habit Tracker! :D\n')
    sleep(2*state["SLEEP_SPEED"])
    print('Returning to User Menu...')
    for i in range(3):
        sleep(0.5*state["SLEEP_SPEED"])
        print(f'.... in {3-i} ....')
    return_user_screen(state)
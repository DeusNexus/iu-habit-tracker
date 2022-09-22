import os
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

# Get the size
# of the terminal
columns,lines = os.get_terminal_size()

def credits(active_user,user_screen):
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
        sleep(0.1)
    print('\nThank you for checking out the Habit Tracker! :D\n')
    sleep(2)
    print('Returning to User Menu...')
    for i in range(3):
        sleep(0.5)
        print(f'.... in {3-i} ....')
    print('[*] Loading User Screen!')
    sleep(1)
    clear()
    user_screen(active_user)
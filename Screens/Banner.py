from datetime import datetime
import os
from Utils import style

# Get the size
# of the terminal
columns,lines = os.get_terminal_size()

#Create a banner by printing a line n multiple times and adjusting for the cli screen size.
def banner(users) -> list[str]:
    '''Creates a dynamic welcome banner depending on the command-line column and lines of the open window.'''
    lines = []
    u = users.users
    b = {
        'l1': style('*.' * (columns//2),'YELLOW'),
        'l2': style('/\\' * (columns//6)+ ' ' * (( columns//3 - len('Welcome to Habit Tracker') ) // 2) + 'Welcome to Habit Tracker' + ' ' * (( columns//3 - len('Welcome to Habit Tracker') ) // 2) + '/\\' * (columns//6),'GREEN'),
        'l3': style('.*' * (columns//6)+ ' ' * (( columns//3 - len(f'Today is {datetime.now().strftime("%A %d-%m-%Y, %H:%M:%S")}') ) // 2) + f'Today is {datetime.now().strftime("%A %d-%m-%Y, %H:%M:%S")}' + ' ' * (( columns//3 - len(f'Today is {datetime.now().strftime("%A %d-%m-%Y, %H:%M:%S")}') ) // 2) + '.*' * (columns//6),'BOLD'),
        'l4': style('\\/' * (columns//6)+ ' ' * (( columns//3 - len(f'Total Users Registered: {len(u)}') ) // 2) + f'Total Users Registered: {len(u)}' + ' ' * (( columns//3 - len(f'Total Users Registered: {len(u)}') ) // 2) + '\\/' * (columns//6),'CYAN'),
        'l5': style('*' * (columns//3)+ ' ' * (columns//3)  + '*'*(columns//3),'BLUE'),
        'l6': style('*~~*' * (columns//4),'RED'),
    }
    
    def add_line(text,times):
        for i in range(times):
            lines.append(text)
    
    add_line(b['l6'], 2)
    add_line(b['l1'], 6)
    add_line(b['l6'], 2)
    add_line(b['l2'], 1)
    add_line(b['l5'], 1)
    add_line(b['l3'], 1)
    add_line(b['l5'], 1)
    add_line(b['l4'], 1)
    add_line(b['l6'], 2)
    add_line(b['l1'], 6)
    add_line(b['l6'], 2)

    return lines
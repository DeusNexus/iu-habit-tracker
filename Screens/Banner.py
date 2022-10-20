from datetime import datetime
import os

# Get the size
# of the terminal
columns,lines = os.get_terminal_size()

def banner(users) -> list[str]:
    '''Creates a dynamic welcome banner depending on the command-line column and lines of the open window.'''
    lines = []
    u = users.users
    b = {
        'l1': '*.' * (columns//2),
        'l2': '/\\' * (columns//6)+ ' ' * (( columns//3 - len('Welcome to Habit Tracker') ) // 2) + 'Welcome to Habit Tracker' + ' ' * (( columns//3 - len('Welcome to Habit Tracker') ) // 2) + '/\\' * (columns//6),
        'l3': '.*' * (columns//6)+ ' ' * (( columns//3 - len(f'Today is {datetime.now().strftime("%A %d-%m-%Y, %H:%M:%S")}') ) // 2) + f'Today is {datetime.now().strftime("%A %d-%m-%Y, %H:%M:%S")}' + ' ' * (( columns//3 - len(f'Today is {datetime.now().strftime("%A %d-%m-%Y, %H:%M:%S")}') ) // 2) + '.*' * (columns//6),
        'l4': '\\/' * (columns//6)+ ' ' * (( columns//3 - len(f'Total Users Registered: {len(u)}') ) // 2) + f'Total Users Registered: {len(u)}' + ' ' * (( columns//3 - len(f'Total Users Registered: {len(u)}') ) // 2) + '\\/' * (columns//6),
        'l5': '*' * (columns//3)+ ' ' * (columns//3)  + '*'*(columns//3),
        'l6': '*~~*' * (columns//4),
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
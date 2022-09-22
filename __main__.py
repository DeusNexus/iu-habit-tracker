from random import randint
import questionary as quest
from datetime import datetime
from time import sleep
import os

#Import of Classes and Functions
from Classes.Habit import Habit
from Classes.User import User
from Classes.Users import Users

#Import for Mock data
from Load import load_example_data, load_user_data

#Function to Clear Terminal
clear = lambda : os.system('tput reset')

# Get the size
# of the terminal
columns,lines = os.get_terminal_size()

#Define Users
users = Users()

#active user will contain unique User
active_user = None
login = False

#Create Example Data from Classes
load_example_data(users)
#If user data is available in DB load it into memory
load_user_data(users)

#Import screens
from Screens.User import user_screen
from Screens.View import view
from Screens.New import new
from Screens.Edit import edit
from Screens.Delete import delete
from Screens.ExportImport import export_import
from Screens.Reset import reset
from Screens.Credits import credits
from Screens.Logout import logout

def banner() -> list[str]:
    lines = []
    b = {
        'l1': '*' * columns,
        'l2': '.' * (columns//3)+ ' ' * (( columns//3 - len('Welcome to Habit Tracker') ) // 2) + 'Welcome to Habit Tracker' + ' ' * (( columns//3 - len('Welcome to Habit Tracker') ) // 2) + '.' * (columns//3),
        'l3': '.' * (columns//3)+ ' ' * (( columns//3 - len(f'Today is {datetime.now()}') ) // 2) + f'Today is {datetime.now()}' + ' ' * (( columns//3 - len(f'Today is {datetime.now()}') ) // 2) + '.' * (columns//3),
        'l4': '.' * (columns//3)+ ' ' * (( columns//3 - len(f'Total Users Registered: {len(users.users)}') ) // 2) + f'Total Users Registered: {len(users.users)}' + ' ' * (( columns//3 - len(f'Total Users Registered: {len(users.users)}') ) // 2) + '.' * (columns//3),
        'l5': '*' * (columns//3)+ ' ' * (columns//3)  + '*'*(columns//3),
    }
    
    def add_line(text,times):
        for i in range(times):
            lines.append(text)
    
    add_line(b['l1'], 5)
    add_line(b['l2'], 1)
    add_line(b['l5'], 1)
    add_line(b['l3'], 1)
    add_line(b['l5'], 1)
    add_line(b['l4'], 1)
    add_line(b['l1'], 5)

    return lines

def app(skip:bool=False) -> None:
    global login
    global active_user

    if(not skip):
        print('[START SCREEN]')
        start = quest.confirm("Are you a new user?").ask()
    else:
        start = False
    
    #registration process
    if(start):
        register = quest.select("Want to create a new account or exit the application?", choices=["Create New Account", "Exit Application"]).ask()
        if(register=='Create New Account'):
            #create new account and show registration options
            uname = quest.text("What will be your username?").ask()
            password = quest.password("Provide a secure password").ask()
            print(f'\n[!] Check your user details below!\nUsername:{uname}     Password: {password}\n')
            corr_info = quest.confirm("Is your information correct?").ask()
            if(corr_info):
                clear()
                users.create(uname, password)
                sleep(1)
                print('[*] Successfully registered! Lets get started.')
                sleep(1)
                print('[*] Reloading application... Please login to the Habit Tracker with your new account!\n')
                sleep(1)
                app(skip=True)
            else:
                print('[!] Try to register again until you get your login details right!')
        elif(register=='Exit Application'):
            #terminate application
            print('\nGoodbye! Hope to see return soon.')
            quit()

    #login to user screen
    else:
        #show registered users
        selected_username = quest.select('The following users are registered to the application, please choose your username.', [u.name for u in users.users] ).ask()
        
        while(not login):
            #input user password
            provided_password = bytes(quest.password('Enter your password:').ask(), 'utf8')
            
            #set active user
            for u in users.users:
                if u.name == selected_username:
                    active_user = u
                else:
                    pass
            
            #check if password is valid else retry
            if(active_user.auth(provided_password)):
                login = True
                user_screen(active_user)
            else:
                login = False
                ans = quest.select('The password you entered seems to be incorrect. Would you like to try again or go back to the start screen?',['Try again','Return to Start Screen']).ask()
                if(ans == 'Return to Start Screen'):
                    sleep(1)
                    clear()
                    print('\n[*] Going back to Start Screen...\n')
                    sleep(1)
                    app()
                else:
                    pass
        
#Mock demo that created habits and shows them seperately.
def demo() -> None:
    listofhabits = [
        Habit('Gym','Go to the gym once every day.','1M',True,None,3,'Health','Good looking figure and healthy body',5,'f@e.nl',7,0),
        Habit('Sport at Home','Do 10 situps in the evening','3D',True,None,2,'Health','Good looking figure and healthy body',3,'f@e.nl',5,0),
        Habit('Study for at least 30min','Progress your study by being actively engaged','1Y',True,None,2,'Education','Become smarter by doing small step everyday',5,'f@e.nl',30,0),
        Habit('Check emails','Reply to any new emails','4H',True,None,1,'Be responsive',4,'f@e.nl',7,0)
    ]

    for habit in listofhabits:
        habit.info()
        habit.checkin('Good day', randint(1, 6))
        habit.display_checkins()

#Start habit tracker application
if __name__ == "__main__":
    for line in banner():
        print(line)
        sleep(0.01)
    print('\n')
    
    try:
        app()
    except KeyboardInterrupt as e:
        print('\n\nYou have terminated the application with Ctrl+C!')
    except ValueError as e:
        print('\nWrong value was given!',e)
    except TypeError as e:
        #print(e)
        pass
    # demo()
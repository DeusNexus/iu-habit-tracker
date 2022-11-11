import questionary as quest
from time import sleep
import os
import traceback

#Sqlite3 Database Operational API
from Database import db_api as api

#Import of Classes and Functions
from Classes.Habit import Habit
from Classes.User import User
from Classes.Users import Users

#Import for Mock data
from Load import load_users, load_user_data

#Function to Clear Terminal
clear = lambda : os.system('tput reset')

#Import screens
from Screens.Banner import banner
from Screens.User import user_screen
from Screens.View import view
from Screens.New import new
from Screens.Edit import edit
from Screens.Delete import delete
from Screens.ExportImport import export_import
from Screens.Reset import reset
from Screens.Credits import credits
from Screens.Logout import logout

#Text Styling
from Utils import style

#Main program entry
def app(skip:bool=False) -> None:
    try:
        '''The main application, receives whether to skip as boolean the question whether to create a new user if user just created an account and directly goes to the user list to login.'''
        
        #Application State
        state = {
            'users': Users(),
            'active_user': None,
            'user_index':0,
            'login': False,
            'SLEEP_SPEED':1,
            'app':app,
            'user_screen': user_screen
        }

        #Pass the state created above into load_users function that will insert database users into the state.
        load_users(state['users'])

        #When app(skip=False) ask if they are new user else continue below.
        if(not skip):
            print(style('\n[START SCREEN]','UNDERLINE'))
            start = quest.confirm("Are you a new user?").ask()
        else:
            start = False
        
        #Ask if already registeered -> registration process
        if(start):
            register = quest.select("Want to create a new account or exit the application?", choices=["Create New Account", "Exit Application"]).ask()
            if(register=='Create New Account'):
                #create new account and show registration options
                uname = quest.text("What will be your username?").ask()
                password = quest.password("Provide a secure password").ask()
                print(f'\n[⚠️] Check your user details below!\nUsername:{uname}     Password: {password}\n')
                corr_info = quest.confirm("Is your information correct?").ask()
                if(corr_info):
                    clear()
                    users_len = len(state['users'].users)
                    #Create User instance in memory
                    state['users'].create(uname, password)
                    #Insert the new user into the database for persistency
                    uu = state['users'].users[users_len]
                    api.db_users_insert([{
                        'user_id':uu.user_id,
                        'salt':f"{uu.salt}",
                        'name':uu.name,
                        'password':f"{uu.password}",
                        'created':uu.created,
                        'last_login':uu.last_login,
                    }])
                    sleep(1*state['SLEEP_SPEED'])
                    print('[💾] Successfully registered! Lets get started.')
                    sleep(1*state['SLEEP_SPEED'])
                    print('[🔃] Reloading application... Please login to the Habit Tracker with your new account!\n')
                    sleep(1*state['SLEEP_SPEED'])
                    state['app'](skip=True)
                else:
                    print('[⚠️] Try to register again until you get your login details right!')
            elif(register=='Exit Application'):
                #terminate application
                print('\nGoodbye! Hope to see return soon.')
                quit()

        #Already registered -> login to user screen
        else:
            #show registered users
            login_options = [u.name for u in state['users'].users] + ['[Exit]']
            selected_username = quest.select('The following users are registered to the application, please choose your username.', login_options ).ask()

            if(not selected_username):
                print('No username was selected, assuming that user tried to cancel action with cntrl + c, terminating application...')
                exit()

            if(selected_username) == '[Exit]': 
                print("Goodbye! Terminating application...")
                sleep(2)
                exit()
            
            while(not state['login']):
                #input user password
                provided_password = quest.password('Enter your password:').ask()

                #set user_index to 0
                state["user_index"] = 0

                #set active user
                for u in state['users'].users:
                    if u.name == selected_username:
                        state['active_user'] = u
                    else:
                        #If user to login is not the one in the list then increment the index which is used for easy reference to state["users"].users[index]
                        state['user_index'] += 1
                
                #check if password is valid else retry
                if(state['active_user'].auth(provided_password)):
                    #If user data is available in DB load it into memory
                    try:
                        #Load all user data from db into the memory as classes.
                        load_user_data(state['users'],state['active_user'].user_id)
                        
                        #Set login true and show the user screen.
                        state['login'] = True
                        state['user_screen'](state)
                        state['active_user'].set_last_login()
                    except Exception as e:
                        print('[❌] Error in app() authentication user:',e)
                else:
                    state['login'] = False
                    ans = quest.select('The password you entered seems to be incorrect. Would you like to try again or go back to the start screen?',['Try again','Return to Start Screen']).ask()
                    if(ans == 'Return to Start Screen'):
                        sleep(1*state['SLEEP_SPEED'])
                        clear()
                        print('\n[↩️] Going back to Start Screen...\n')
                        sleep(1*state['SLEEP_SPEED'])
                        app()
                    else:
                        pass
    
    except Exception as e:
        print('Error occured: ',e)
        traceback.print_exc()
        sleep(10)
    except KeyboardInterrupt as e:
        print('\n\nYou have terminated the application with Ctrl+C!')
        exit()


#Start habit tracker application
try:
    print(style("[🔎] Starting Habit Tracker and checking if database already exists...",'BLUE'))
    #Check if the database alreadt exist or init a new one
    api.db_exists()

    #Ask whether one wants to create a new account or not (skip=False) and then start the main program.
    app(skip=False)

#Error Catching
except KeyboardInterrupt as e:
    print('\n\nYou have terminated the application with Ctrl+C!')
    exit()

except ValueError as e:
    print('\n[❌] Wrong value was given!',e)
    traceback.print_exc()

except TypeError as e:
    print('[❌] TypeError:',e)
    traceback.print_exc()
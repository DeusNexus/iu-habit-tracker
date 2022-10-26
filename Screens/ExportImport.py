import os
import questionary as quest
from time import sleep
import json 

#Function to Clear Terminal
clear = lambda : os.system('tput reset')

#Database for Export or Importing
from Database import db_api as api

def export_import(state):
    '''The export/import screen is used for importing or exporting a user account using json files. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print('[Export/Import Screen]\n')
    print('You have options to either export your user file as a json file or import it by giving the file path.')
    print('If you choose export, the file will be saved in the same directory as the habit tracker.')
    print('If you wish to import a file, it is recommened to drop it into the habit tracker directory so it can be easily found.')
    print('Once in the directory you can select the filename of the supported files.\n\n')
    questions = ['Export My Account', 'Import Account', 'Go Back to User Screen']
    ans = quest.select('What do you want to do?', questions).ask()

    #Export
    if(ans==questions[0]):
        
        sleep(1*state["SLEEP_SPEED"])

        print('Attempting to creat JSON file for export..')

        try:
            #Retrieve all database tables for the user_id
            user_obj = api.db_export(state["active_user"].user_id)
            # print('User_obj from database: ',user_obj,'\n')

            #Write the file out with formatting and json extension
            with open(f'./EXPORT/habit_tracker-{state["active_user"].name}-{state["active_user"].user_id}.json',mode='w') as file:
                json_formatted = json.dumps(user_obj)
                # print('JSON Formatted: ',json_formatted)
                file.write(json_formatted)

        except Exception as e:
            print('[!] Something went wrong while exporting the user: ',e)

        sleep(1*state["SLEEP_SPEED"])
        print('[!] Returning to User Screen...')
        sleep(2*state["SLEEP_SPEED"])
        clear()
        state["user_screen"](state)

    #Import
    elif(ans==questions[1]):
        sleep(1*state["SLEEP_SPEED"])

        #Look at files in current dir
        files = list(filter(lambda name: str.__contains__(name,".json"), os.listdir('./IMPORT')))

        if(files):
            file_name = quest.select('Select a valid user json file to import from available files:', files).ask()
            
            with open(f'./IMPORT/{file_name}',mode='r') as file:
                user_obj = json.loads(file.read()) #user_obj is a dict
                #print(type(user_obj),user_obj)
                resp = api.db_import(user_obj)
                if(resp == 'success'):
                    print('[*] User successfully inserted into database! Please logout and reload the application to login to the new user.')
                elif(resp == 'exists'):
                    print('[!] The user already exists in the database with the user_id, import is aborted.')
                elif(resp == 'error'):
                    print('[!] Failure, check if file is not wrong or corrupt.')
                file.close()
        else:
            print('No .json files found in IMPORT_EXPORT folder.')

        sleep(1*state["SLEEP_SPEED"])
        print('[!] Returning to User Screen...')
        sleep(2*state["SLEEP_SPEED"])
        clear()
        state["user_screen"](state)

    #Return
    elif(ans==questions[2]):
        sleep(1*state["SLEEP_SPEED"])
        print('[!] Returning to User Screen...')
        sleep(2*state["SLEEP_SPEED"])
        clear()
        state["user_screen"](state)
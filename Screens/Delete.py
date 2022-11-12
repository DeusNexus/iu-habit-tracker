import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')
from Database import db_api as api

#Text Styling
from Utils import style

#Return to user screen
def return_user_screen(state):
    sleep(1*state["SLEEP_SPEED"])
    print('[!] Returning back to User Screen...')
    sleep(1*state["SLEEP_SPEED"])
    clear()
    state["user_screen"](state)

def delete(state):
        '''The delete screen is used for deleting habits. Habits list is printed and user can select which one to permanently remove. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
        clear()
        print(style('[Delete Screen]','UNDERLINE'))
        print(style('\nBe careful, deleting a habit will PERMANENTLY remove it. There is no way to recover it later on!','RED'))

        #In case no habits are available, show message and return to user_screen
        if( len(state["active_user"].habits) == 0 ): 
            print('You currently do not have any habits to delete!')
            return_user_screen(state)

        #If user has habits, show the list of titles so one can be selected for deletion.
        else:
            habits:list = state["active_user"].habits
            print(style(f'Total Available Habits: {len(habits)}\n','CYAN'))
            habit_strings:list =  [habit.title for habit in habits] + ['Go Back to User Screen']
            ans = quest.select('Be careful, which habit would you like to permanently delete?', habit_strings,style=state['qstyle']).ask()
            
            #Option Return
            if(ans == 'Go Back to User Screen'):
                return_user_screen(state)
            
            #If a habit title is selected, continue to delete habit.
            else:
                print('Showing each habit: ...')
                #Habit to Delete
                h2d = None
                #Go over the habits until we find the user specified title (take note that habits with same title would always delete the first one!)
                
                for index, habit in enumerate(state["active_user"].habits):
                    if ans == habit.title:
                        h2d = habit
                        print('Habit at Index: ', index)

                        sleep(1*state["SLEEP_SPEED"])
                        print(f'Deleting "{h2d.title}" habit with id: {h2d.habit_id}...')

                        #Remove habit from memory, since habit instance also includes the checkins list we don't have to remove these specifically from memory.
                        state["active_user"].habits.pop(index)

                        #Habit to remove from db
                        print('Deleting habits from database..')
                        api.db_habits_delete(h2d.habit_id)

                        #Remove all checkins for the habit_id
                        print('Deleting checkins for habit from database...')
                        api.db_checkins_delete(h2d.habit_id)

                #state["active_user"].delete_habit(habit_id)
                return_user_screen(state)


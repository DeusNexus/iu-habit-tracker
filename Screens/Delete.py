import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')
from Database import db_api as api

def delete(state):
        '''The delete screen is used for deleting habits. Habits list is printed and user can select which one to permanently remove. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
        clear()
        print('[Delete Screen]')
        if( len(state["active_user"].habits) == 0 ): 
            print('You currently do not have any habits to delete!')
            sleep(1*state["SLEEP_SPEED"])
            print('[!] Returning to User Screen...')
            sleep(2*state["SLEEP_SPEED"])
            clear()
            state["user_screen"](state)
        else:
            habits:list = state["active_user"].habits
            print('Total Available Habits: ',len(habits))
            habit_strings:list =  [habit.title for habit in habits] + ['Go Back to User Screen']
            ans = quest.select('Be careful, which habit would you like to permanently delete?', habit_strings).ask()
            
            if(ans == 'Go Back to User Screen'):
                sleep(1*state["SLEEP_SPEED"])
                print('[!] Returning to User Screen...')
                sleep(2*state["SLEEP_SPEED"])
                clear()
                state["user_screen"](state)
            else:
                print('Showing each habit: ...')
                h2d = None
                index = 0
                for habit in state["active_user"].habits:
                    if ans == habit.title:
                        h2d = habit
                    else:
                        index += 1
                sleep(1*state["SLEEP_SPEED"])
                print(f'Deleting "{h2d.title}" habit with id: {h2d.habit_id}...')
                state["active_user"].habits.pop(index)
                api.db_habits_delete(h2d.habit_id)

                #state["active_user"].delete_habit(habit_id)
                sleep(1*state["SLEEP_SPEED"])
                print('[!] Returning to User Screen...')
                sleep(2*state["SLEEP_SPEED"])
                clear()
                state["user_screen"](state)


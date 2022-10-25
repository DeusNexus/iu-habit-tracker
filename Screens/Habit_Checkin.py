import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')
from Database import db_api as api

def habit_checkin(state):
        '''Generates screen for all available habit checkins. Lists habits available to checkin, whether deadline is due or still on-time and updates the database and in-memory objects accordingly.'''
        clear()
        print('[Checkin Screen]')

        #In case no habits are available, show message and return to user_screen
        if( len(state["active_user"].habits) == 0 ): 
            print('You currently do not have any habits to checkin to!')
            sleep(1*state["SLEEP_SPEED"])
            print('[!] Returning to User Screen...')
            sleep(2*state["SLEEP_SPEED"])
            clear()
            state["user_screen"](state)

        #If user has habits, show the list of titles so one can be selected for deletion.
        else:
            #List all active habits ready to checkin to.
            habits:list = [habit for habit in state["active_user"].habits if habit.active]

            print('Total Available Habits for Checkin: ',len(habits))
            habit_strings:list =  [habit.title for habit in habits] + ['Go Back to User Screen']
            ans = quest.select('Which habit would you like to checkin for?', habit_strings).ask()

            h2c = None
            
            for habit in habits:
                #Set variable to reference the habit in question to checkin to.
                if habit.title == ans:
                    h2c = habit
                else:
                    pass
            
            #Option Return
            if(ans == 'Go Back to User Screen'):
                sleep(1*state["SLEEP_SPEED"])
                print('[!] Returning to User Screen...')
                sleep(2*state["SLEEP_SPEED"])
                clear()
                state['user_screen'](state)
            
            #If a habit title is selected, continue to delete habit.
            else:
                print('Checkin in to habit...')
                sleep(1*state["SLEEP_SPEED"])

                note = quest.text('Write a short note on how it went. Did everything go as you planned for? Any issues or things that were positive?').ask()
                rating = quest.select('How well did it go? 1 = Worst and 5 = Best!',['1','2','3','4','5']).ask()

                #If dynamic habit, use the dynamic_checkin method of the habit instance
                if(h2c.is_dynamic):
                    sleep(1*state["SLEEP_SPEED"])
                    print('Checking in for Dynamic Habit...')
                    h2c.dynamic_checkin(note,rating)
                    sleep(10*state["SLEEP_SPEED"])
                    print('[DYNAMIC CHECKIN DID WE MEET DEADLINE GOAL YET, DID WE FAIL OR STILL TARGET NOT MET AND DEADLINE NOT DUE. ]')
                    sleep(1*state["SLEEP_SPEED"])
                    print('Checkin registered and new deadline generated based on your interval.')

                #If regular habit, use normal checkin method
                else:
                    print('Checking in for Regular Habit...')
                    sleep(1*state["SLEEP_SPEED"])
                    h2c.checkin(note,rating)
                    sleep(10*state["SLEEP_SPEED"])
                    print('Checkin registered and new deadline generated based on your interval.')

                #Return to checkin list
                habit_checkin(state)
                pass


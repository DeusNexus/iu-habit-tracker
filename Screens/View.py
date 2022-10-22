import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

import Classes.Analytics as Analytics

def view(state):
    '''The view screen is used to display habits of the user and give various options to see all, an individual or filtered habits. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print('[View Screen]')
    
    if( len(state["active_user"].habits) == 0 ): 
        print('You currently do not have any habits to view!')
        sleep(1*state["SLEEP_SPEED"])
        print('[!] Returning to User Screen...')
        sleep(2*state["SLEEP_SPEED"])
        clear()
        state["user_screen"](state)
        pass

    else:
        options = ['All Habits','Individual Habit', 'Filter Criteria','Go Back to User Screen']
        ans = quest.select('Menu Options:', options).ask()
        if(ans == options[0]):
            for habit in state["active_user"].habits:
                habit.info_habit()
                print('Streak:',habit.streak)
                print('Highest Streak for Habit: ', Analytics.habit_longest_streak(habit.checkins))
                print('\n')

            print('[All Habit Statistics]')
            print('longest_streak: ', Analytics.total_longest_streak(state["active_user"].habits))
            print('most_punctual_sec: ', Analytics.most_punctual(state["active_user"].habits))
            print('most_late_sec: ', Analytics.most_late(state["active_user"].habits))
            sleep(8*state["SLEEP_SPEED"])
            print('[!] Returning to User Screen...')
            sleep(1*state["SLEEP_SPEED"])
            clear()
            state["user_screen"](state)
            pass

        elif(ans == options[1]):
            print('Not Yet Implemented')
            sleep(8*state["SLEEP_SPEED"])
            print('[!] Returning to User Screen...')
            sleep(1*state["SLEEP_SPEED"])
            clear()
            state["user_screen"](state)
            pass

        elif(ans == options[2]):
            print('Not Yet Implemented')
            sleep(2*state["SLEEP_SPEED"])
            print('[!] Returning to User Screen...')
            sleep(1*state["SLEEP_SPEED"])
            clear()
            state["user_screen"](state)
            pass

        elif(ans == options[3]):
            clear()
            sleep(1*state["SLEEP_SPEED"])
            print('[!] Returning back to User Screen...')
            sleep(1*state["SLEEP_SPEED"])
            state["user_screen"](state)
            pass
        
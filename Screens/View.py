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

        #All Habits
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
            
            ao2 = ['Page 2','[Return]']
            interact = quest.select('See more?',ao2).ask()

            if(interact == ao2[0]):
                print('PAGE 2')
                print('NOT IMPLEMENTED')
            elif(interact == ao2[1]):
                clear()
                view(state)

            sleep(1*state["SLEEP_SPEED"])
            clear()
            view(state)
            pass
        
        #Individual Habit
        elif(ans == options[1]):
            choices = [habit.title for habit in state["active_user"].habits] + ['[Return]']
            selected_habit = quest.select('Which habit would you like to individually inspect?', choices).ask()

            for habit in state["active_user"].habits:
                if habit.title == selected_habit:
                    #Now give detailed overview of the habits. Add more individual view options? View Checkins in paginated form?
                    print(f'Viewing habit: {selected_habit}')
                    print(f'Total Successful Checkins: {habit.success}')
                    print(f'Total Failed Checkins: {habit.fail}')
                    print(f'Active Streak: {habit.streak}')
                    print(f'Difficulity: {habit.difficulity}')
                    print(f'Category: {habit.category}')
                    print(f'Importance: {habit.importance}')
                else: 
                    pass
            
            io2 =  ['Page 2','[Return]']
            interact = quest.select('See more?',io2).ask()
            
            if(interact == io2[0]):
                print('PAGE 2')
                print('NOT IMPLEMENTED')
            elif(interact == io2[1]):
                clear()
                view(state)

            sleep(1*state["SLEEP_SPEED"])
            clear()
            view(state)
            pass
        
        #Filter Criteria
        elif(ans == options[2]):
            criteria = ['interval','difficulity','category','importance','streak','success','fail','cost','cost_accum']
            ans = quest.select('Which filter criteria would you like to use?',criteria).ask()

            sleep(2*state["SLEEP_SPEED"])
            print('[!] Returning to User Screen...')
            sleep(1*state["SLEEP_SPEED"])
            clear()
            view(state)
            pass
        
        #Return to user screen
        elif(ans == options[3]):
            clear()
            sleep(1*state["SLEEP_SPEED"])
            print('[!] Returning back to User Screen...')
            sleep(1*state["SLEEP_SPEED"])
            state["user_screen"](state)
            pass
        
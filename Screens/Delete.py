import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

def delete(active_user,user_screen):
        clear()
        print('[Delete Screen]')
        if( len(active_user.habits) == 0 ): 
            print('You currently do not have any habits to delete!')
            sleep(1)
            print('[!] Returning to User Screen...')
            sleep(2)
            clear()
            user_screen(active_user)
        else:
            habits:list = active_user.habits
            print('Total Available Habits: ',len(habits))
            habit_strings:list =  [habit.title for habit in habits]
            ans = quest.select('Be careful, which habit would you like to permanently delete?', habit_strings).ask()
            print('Showing each habit: ...')
            h2d = None
            index = 0
            for habit in active_user.habits:
                if ans == habit.title:
                    h2d = habit
                else:
                    index += 1
            sleep(1)
            print(f'Deleting "{h2d.title}" habit with id: {h2d.habit_id}...')
            active_user.habits.pop(index)

            #active_user.delete_habit(habit_id)
            sleep(1)
            print('[!] Returning to User Screen...')
            sleep(2)
            clear()
            user_screen(active_user)


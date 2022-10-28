import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')
from Database import db_api as api
from datetime import datetime

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
            habit_strings:list =  [
                f'{idx+1} [{"Dynamic" if habit.is_dynamic else "Regular"}]'+ 
                f'[{"DEADLINE DUE" if datetime.now() > habit.next_deadline else "IN TIME"}] {habit.title} - '+ 
                f'Streak: {habit.streak} - '+
                f'Deadline: {habit.next_deadline.strftime("%Y-%m-%d %H:%M")}\n'
                for idx,habit in enumerate(habits)] + ['Go Back to User Screen']
            ans = quest.select('Which habit would you like to checkin for?', habit_strings).ask()

            #First check if we don't want to return (last element in list) since that one doesn't have an index (this could have been done in a better way, but for simplicity of program should be fine.)            
            if(ans != habit_strings[-1]):
                #Indexes are not starting from 0 so we substract 1
                h2c = habits[int(ans[0])-1]
            
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
                    
                    #Checkin to the habit, creates new checkin instance for the habit in habit.checkins[]
                    h2c.dynamic_checkin(note,rating)
                    
                    try:
                        #Insert the checkin to the db
                        latest_checkin = h2c.checkins[-1]
                        
                        print('lastest checkin: ',latest_checkin)

                        api.db_checkins_insert([
                            {
                                'user_id':h2c.user_id,
                                'habit_id':latest_checkin.habit_id,
                                'checkin_id':latest_checkin.checkin_id,
                                'checkin_datetime':latest_checkin.checkin_datetime,
                                'deadline':latest_checkin.deadline,
                                'success':'True' if latest_checkin.success else 'False',
                                'note':latest_checkin.note,
                                'rating':latest_checkin.rating,
                                'cost':h2c.cost,
                                'cost_accum':h2c.cost_accum,
                                'dynamic':'True' if latest_checkin.dynamic else 'False',
                                'dynamic_count':latest_checkin.dynamic_count
                            }
                        ])
                        
                    except Exception as e:
                        print('Failed to insert dynamic checkin: ',e)

                    sleep(10*state["SLEEP_SPEED"])
                    print('[DYNAMIC CHECKIN DID WE MEET DEADLINE GOAL YET, DID WE FAIL OR STILL TARGET NOT MET AND DEADLINE NOT DUE. ]')
                    sleep(1*state["SLEEP_SPEED"])
                    print('Checkin registered and new deadline generated based on your interval.')

                #If regular habit, use normal checkin method
                else:
                    print('Checking in for Regular Habit...')
                    sleep(1*state["SLEEP_SPEED"])
                    
                    #Checkin to habit, creates new checkin instance for the habit in habit.checkins[]
                    h2c.checkin(note,rating)

                    try:
                        #Insert the checkin to the db
                        latest_checkin = h2c.checkins[-1]

                        print('lastest checkin: ',latest_checkin)

                        api.db_checkins_insert([
                            {
                                'user_id':h2c.user_id,
                                'habit_id':latest_checkin.habit_id,
                                'checkin_id':latest_checkin.checkin_id,
                                'checkin_datetime':latest_checkin.checkin_datetime,
                                'deadline':latest_checkin.deadline,
                                'success':'True' if latest_checkin.success else 'False',
                                'note':latest_checkin.note,
                                'rating':latest_checkin.rating,
                                'cost':h2c.cost,
                                'cost_accum':h2c.cost_accum,
                                'dynamic':'True' if latest_checkin.dynamic else 'False',
                                'dynamic_count':latest_checkin.dynamic_count
                            }
                        ])

                    except Exception as e:
                        print('Failed to insert regular checkin: ',e)

                    sleep(10*state["SLEEP_SPEED"])
                    print('Checkin registered and new deadline generated based on your interval.')

                #Return to checkin list
                habit_checkin(state)
                pass


import os
import questionary as quest
from time import sleep
from datetime import datetime
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

import Classes.Analytics as Analytics
from Database import db_api as api
from Load import Habit_Model
from Utils import style, seconds_to_timestring

#Used to return to user screen
def return_user_screen(state):
    sleep(1*state["SLEEP_SPEED"])
    print('[!] Returning back to User Screen...')
    sleep(1*state["SLEEP_SPEED"])
    clear()
    state["user_screen"](state)

#Used to return to view screen
def return_view_screen(state):
    sleep(1*state["SLEEP_SPEED"])
    print('[!] Returning to View Screen...')
    sleep(1*state["SLEEP_SPEED"])
    clear()
    view(state)

def view(state):
    '''The view screen is used to display habits of the user and give various options to see all, an individual or filtered habits. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print('[View Screen]')
    
    #In case the user has no habits or no active habits show message and return.
    if( len(state["active_user"].habits) == 0 or len([habit for habit in state["active_user"].habits if habit.active == True]) < 1): 
        print('You currently do not have any habits to view!')
        return_user_screen(state)

    #If the user has habits, which are not all inactive.
    else:
        options = ['All Habits','Individual Habit', 'Filter Criteria','Go Back to User Screen']
        ans = quest.select('Menu Options:', options,style=state['qstyle']).ask()

        def view_all(ans):
            #All Habits
            if(ans == options[0]):
                print(style('[All Active Habits]','UNDERLINE'))
                for habit in state["active_user"].habits:
                    #Only show active habits
                    if habit.active:
                        habit.info_habit()
                        print(style(f'Streak: {habit.streak}','BOLD'))
                        print(style(f'Highest Streak for Habit: {Analytics.habit_longest_streak(habit.checkins)}','BOLD')+'\n')
                    #Do nothing for inactive habits
                    else:
                        pass
                
                #options to choose from
                ao2 = ['Global Statistics','[Return]']
                interact = quest.select('See more?',ao2,style=state['qstyle']).ask()

                #When first option is choosen
                if(interact == ao2[0]):
                    clear()
                    habits = [habit for habit in state["active_user"].habits if habit.active]
                    print(style('[Global Statistics for all habits]','UNDERLINE'))
                    print('\n')
                    print(style(f'Most Accumulated Cost ($) for a habit: {Analytics.most_expensive(habits)}','CYAN'))
                    print(style(f'Most Fails for a habit: {Analytics.most_fail(habits)}','RED'))
                    print(style(f'Most Success for a habit: {Analytics.most_success(habits)}','GREEN'))
                    print(style(f'Total Fail: {Analytics.total_fail(habits)}','RED'))
                    print(style(f'Total Success: {Analytics.total_success(habits)}','GREEN')+ '\n')
                    print(style(f'Best performing interval: {Analytics.best_performing_interval(habits)}','BOLD'))
                    print(style(f'Best performing category: {Analytics.best_performing_category(habits)}','BOLD')+ '\n')
                    print(style(f'Max Current Streak: {Analytics.total_longest_current_streak(habits)}','YELLOW'))
                    print(style(f'Max Running Streak: {Analytics.total_longest_running_streak(habits)}','YELLOW') + '\n')
                    print(style(f'Most Punctual Habit On Average Title:  {Analytics.most_punctual(habits)[1]}','BOLD'))
                    print(style(f'Most Punctual Habit On Average Time:  {seconds_to_timestring(round(Analytics.most_punctual(habits)[0],2))}','BOLD')+ '\n')
                    print(style(f'Most Late Habit On Average Title: {Analytics.most_late(habits)[1]}','RED'))
                    print(style(f'Most Late Habit On Average Time: {seconds_to_timestring(round(Analytics.most_late(habits)[0],2))}','RED')+ '\n')
                    print(style(f'Average Total Streak: {round(Analytics.avg_total_streak(habits),2)}','CYAN'))
                    print(style(f'Average Break Streak: {round(Analytics.avg_break_streak(habits),2)}','RED')+ '\n')
                    print(style(f'Average Time Left Till Deadline: {seconds_to_timestring(round(Analytics.avg_time_left(habits),2))}','BLUE')+ '\n')
                    print(style(f'Earliest Habit Deadline: {Analytics.earliest(habits).title}','YELLOW'))
                    print('\n')

                    api.db_view()

                    #Options to choose from in global stat
                    ao3 = ['Back to All Habits','[Return]']
                    interact2 = quest.select('See more?',ao3,style=state['qstyle']).ask()
                    
                    #Option 1 in global statistics
                    if(interact2==ao3[0]):
                        clear()
                        #Return to all habits, view_all receives the answer that returns to the right view
                        view_all(options[0])
                    #Option 2 in global statistics
                    elif(interact2==ao3[1]):
                        clear()
                        #Return to view screen
                        return_view_screen(state)

                #When second option is choosen [Return]
                elif(interact == ao2[1]):
                    clear()
                    return_view_screen(state)
            
            #Individual Habit
            elif(ans == options[1]):
                #Get all habit titles and add return option to the list, then present as question
                choices = [habit.title for habit in state["active_user"].habits if habit.active] + ['[Return]']
                selected_habit = quest.select('Which habit would you like to individually inspect?', choices,style=state['qstyle']).ask()

                #Store the habit index of question answer to user later on in same menu (retain info).
                habit_index = None

                #Go over all habits and set the choosen habit plus print all the details
                for indx, habit in enumerate(state["active_user"].habits):
                    if habit.title == selected_habit and habit.active:
                        habit_index = indx
                        #Now give detailed overview of the habits. Add more individual view options? View Checkins in paginated form?
                        print(style(f'\n[Viewing Individual Habit]\n','UNDERLINE'))
                        print(style(f"[{'DYNAMIC' if habit.is_dynamic == True else 'REGULAR'}][{habit.interval}] - {habit.title}",'YELLOW'))
                        print(f"\nDescription: {habit.description}")
                        print(f"Moto: {habit.moto}")
                        print(f"Category: {habit.category}")
                        print((f"\nDifficulity: {habit.difficulity} " if habit.difficulity else '\nDifficulity not set, see Edit menu.'))
                        print((f"Importance: {habit.importance}" if habit.importance else '\nImportance not set, see Edit Menu.'))
                        print((f"\nMilestone Streak: {habit.milestone_streak}" if habit.milestone_streak else '\nMilestone streak not set, see Edit menu..'))
                        print((f"{'Required # of Checkins before Deadline:' + str(habit.checkin_num_before_deadline)} | {'Current # of Checkins before Deadline:' + str(habit.dynamic_count)}" if habit.is_dynamic==True else ''))
                        print(f"Streak: {habit.streak}  Success:{habit.success} Fail: {habit.fail} ")
                        print((f"\nCost: {habit.cost}  |  Accumulated Cost: {habit.cost_accum}" if habit.cost or habit.cost_accum  else '\n'))
                        print(f"Deadline Due: {habit.next_deadline.strftime('%Y-%m-%d %H:%M')}  Created: {habit.created_on.strftime('%Y-%m-%d %H:%M')}\n")
                        print(
                            style(f"Deadline FAILED by {seconds_to_timestring(habit.next_deadline.timestamp() -  datetime.now().timestamp())}",'RED')
                            if (habit.next_deadline.timestamp() - datetime.now().timestamp()) < 0 
                            else 
                            style(f"Deadline IN-TIME by {seconds_to_timestring(habit.next_deadline.timestamp() -  datetime.now().timestamp())}",'GREEN')
                        )
                        print('\n')
                
                #Options after the print, to see more or return
                io2 =  ['Detailed Summary Statistics','[Return]']
                interact = quest.select('See more?',io2,style=state['qstyle']).ask()
                
                #Answer of question, see more details
                if(interact == io2[0]):
                    clear()
                    h = state["active_user"].habits[habit_index]
                    print(
                        style(f"[Detailed Summary Statistics for {h.title}]\n",'UNDERLINE')+
                        f"\nHighest Unbroken Streak: {Analytics.indiv_max_streak(h)}"+
                        f"\nAverage Reported Rating Checkins: {round(Analytics.indiv_avg_rating(h),2)}"+
                        f"\nAverage Streak: {Analytics.indiv_avg_streak(h)}"+
                        f"\nNumber of Checkins: {len(h.checkins)}"
                    )
                    print('\n')
                    print(f'CHECK-INS: \n{"" if (len(h.checkins) > 0) else "NONE"}')
                    for checkin in h.checkins:
                        print(
                                (style("[SUCCESS]",'GREEN') if checkin.success else style("[FAIL]",'RED')) +
                                style(f"{f'[Dynamic Count: {checkin.dynamic_count}]' if checkin.dynamic else ''}",'BOLD')+
                                " Checkin on "+
                                style(f"{checkin.checkin_datetime.strftime('%Y-%m-%d %H:%M')},",'YELLOW')+
                                f" (rated {checkin.rating}/5): {checkin.note}"
                            )
                    print('\n')
                    quest.select('Press Enter to return.', ['Enter'],style=state['qstyle']).ask()
                    clear()
                    view_all(ans)

                #Return option to view screen
                elif(interact == io2[1]):
                    return_view_screen(state)

                return_view_screen(state)
            
            #Filter Criteria
            elif(ans == options[2]):
                #All valid attributes to choose from
                criteria = ['interval','difficulity','category','importance','streak','success','fail','cost','cost_accum']
                ans = quest.select('Which filter criteria would you like to use?',criteria,style=state['qstyle']).ask()

                #Formatted data to print for habit
                def print_overview(hm):
                    print(
                            style(f"[{'DYNAMIC' if hm['is_dynamic']==True else 'REGULAR'}][{hm['interval']}] - {hm['title']}",'YELLOW')+ 
                            style(f"\nDescription: {hm['description']}'",'BOLD')+
                            style(f"\nMoto: {hm['moto']}",'BOLD')+
                            f"\nCategory: {hm['category']}"+
                            (f"\n\nDifficulity: {hm['difficulity']} " if hm['difficulity'] else '\n\nDifficulity not set, see Edit menu.')+
                            (f"\nImportance: {hm['importance']}" if hm['importance'] else '\nImportance not set, see Edit Menu.')+
                            (f"\n\nMilestone Streak: {hm['milestone_streak']}" if hm['milestone_streak'] else '\nMilestone streak not set, see Edit menu..')+
                            (f"\n{'Required # of Checkins before Deadline:' + str(hm['checkin_num_before_deadline'])} | {'Current # of Checkins before Deadline:' + str(hm['dynamic_count'])}" if hm['is_dynamic']==True else '') +
                            f"\nStreak: {hm['streak']}  Success:{hm['success']} Fail: {hm['fail']} "+
                            (f"\n\nCost: {hm['cost']}  |  Accumulated Cost: {hm['cost_accum']}" if hm['cost'] or hm['cost_accum']  else '\n')+
                            f"\nDeadline Due: {hm['next_deadline'].strftime('%Y-%m-%d %H:%M')}  Created: {hm['created_on'].strftime('%Y-%m-%d %H:%M')}"+
                            (   style(f"\nDeadline FAILED by {seconds_to_timestring(hm['next_deadline'].timestamp() -  datetime.now().timestamp())}\n",'RED') 
                                if (hm['next_deadline'].timestamp() - datetime.now().timestamp()) < 0 
                                else style(f"\nDeadline IN-TIME by {seconds_to_timestring(hm['next_deadline'].timestamp() -  datetime.now().timestamp())}\n",'GREEN'))
                        )

                #Filter option
                if(ans == 'interval'):
                    interval = quest.text('Write the interval which you would like to use a filter for you habits? E.g. 1D, 4H',style=state['qstyle']).ask()
                    
                    if(interval):
                        try:
                            interval_habits = api.db_get_habits_by_attr(state["active_user"].user_id, 'interval', interval)
                            
                            if(len(interval_habits) < 1):
                                print('No habits found for your specified filter criteria.')
                                print('Returning to View screen...')
                                sleep(2)
                                return_view_screen(state)
                            
                            print('\n')
                            for habit in interval_habits:
                                #Converts a unnamed array given by SQLITE of habits to a dict with easy to access attributes
                                hm = Habit_Model(habit)
                                print_overview(hm)

                            print('\n')
                            quest.select('Press Enter to Continue',['Okay'],style=state['qstyle']).ask()
                        except Exception as e:
                            print("Failed to get interval: ",e)
                            traceback.print_exc()
                            sleep(10)
                
                #Filter option
                elif(ans == 'difficulity'):
                        difficulity = quest.select('Select the difficulity that you want to use to filter your habits?', ['1','2','3','4','5'],style=state['qstyle']).ask()
                        
                        try:
                            if(difficulity):
                                difficulity_habits = api.db_get_habits_by_attr(state["active_user"].user_id, 'difficulity', difficulity)

                                if(len(difficulity_habits) < 1):
                                    print('No habits found for your specified filter criteria.')
                                    print('Returning to View screen...')
                                    sleep(2)
                                    return_view_screen(state)

                                print('\n')
                                for habit in difficulity_habits:
                                        #Converts a unnamed array given by SQLITE of habits to a dict with easy to access attributes
                                        hm = Habit_Model(habit)
                                        print_overview(hm)

                            print('\n')
                            quest.select('Press Enter to Continue',['Okay'],style=state['qstyle']).ask()
                        except Exception as e:
                            print("Failed to get difficulity: ",e)
                            traceback.print_exc()
                            sleep(10)
                
                #Filter option
                elif(ans =='category'):
                        category = quest.text('Provide the category you want to use as a filter, note it is case-sensitive how you defined it! E.g. Sport, Food, Education..?',style=state['qstyle']).ask()
                        
                        try:
                            if(category):
                                category_habits = api.db_get_habits_by_attr(state["active_user"].user_id, 'category', category)

                                if(len(category_habits) < 1):
                                    print('No habits found for your specified filter criteria.')
                                    print('Returning to View screen...')
                                    sleep(2)
                                    return_view_screen(state)

                                print('\n')
                                for habit in category_habits:
                                        #Converts a unnamed array given by SQLITE of habits to a dict with easy to access attributes
                                        hm = Habit_Model(habit)
                                        print_overview(hm)

                            print('\n')
                            quest.select('Press Enter to Continue',['Okay'],style=state['qstyle']).ask()
                        except Exception as e:
                            print("Failed to get difficulity: ",e)
                            traceback.print_exc()
                            sleep(10)
                
                #Filter option 
                elif(ans =='importance'):
                        importance = quest.select('Select the importance that you want to use to filter your habits?', ['1','2','3','4','5'],style=state['qstyle']).ask()
                        
                        try:
                            if(importance):
                                importance_habits = api.db_get_habits_by_attr(state["active_user"].user_id, 'importance', importance)

                                if(len(importance_habits) < 1):
                                    print('No habits found for your specified filter criteria.')
                                    print('Returning to View screen...')
                                    sleep(2)
                                    return_view_screen(state)

                                print('\n')
                                for habit in importance_habits:
                                        #Converts a unnamed array given by SQLITE of habits to a dict with easy to access attributes
                                        hm = Habit_Model(habit)
                                        print_overview(hm)

                            print('\n')
                            quest.select('Press Enter to Continue',['Okay'],style=state['qstyle']).ask()
                        except Exception as e:
                            print("Failed to get difficulity: ",e)
                            traceback.print_exc()
                            sleep(10)
                
                #Filter option
                elif(ans =='streak'):
                        operator = quest.select('Select one of the operators to use for comparison. Next you will provide a value to compare for. E.g.: streak <= 5, streak > 7', ['>','>=','=','<','<='],style=state['qstyle']).ask()
                        comparison_val = quest.text('Provide a valid number (float or int) that will be used to compare?',style=state['qstyle']).ask()
                        try:
                            if(operator and comparison_val):
                                streak_habits = api.db_get_habits_by_attr_operator(state["active_user"].user_id, 'streak', comparison_val, operator)

                                if(len(streak_habits) < 1):
                                    print('No habits found for your specified filter criteria.')
                                    print('Returning to View screen...')
                                    sleep(2)
                                    return_view_screen(state)

                                print('\n')
                                for habit in streak_habits:
                                        #Converts a unnamed array given by SQLITE of habits to a dict with easy to access attributes
                                        hm = Habit_Model(habit)
                                        print_overview(hm)

                            print('\n')
                            quest.select('Press Enter to Continue',['Okay'],style=state['qstyle']).ask()
                        except Exception as e:
                            print("Failed to get difficulity: ",e)
                            traceback.print_exc()
                            sleep(10)
                
                #Filter option
                elif(ans =='success'):
                        operator = quest.select('Select one of the operators to use for comparison. Next you will provide a value to compare for. E.g.: success <= 5, success > 7', ['>','>=','=','<','<='],style=state['qstyle']).ask()
                        comparison_val = quest.text('Provide a valid number (float or int) that will be used to compare?',style=state['qstyle']).ask()
                        try:
                            if(operator and comparison_val):
                                success_habits = api.db_get_habits_by_attr_operator(state["active_user"].user_id, 'success', comparison_val, operator)

                                if(len(success_habits) < 1):
                                    print('No habits found for your specified filter criteria.')
                                    print('Returning to View screen...')
                                    sleep(2)
                                    return_view_screen(state)

                                print('\n')
                                for habit in success_habits:
                                        #Converts a unnamed array given by SQLITE of habits to a dict with easy to access attributes
                                        hm = Habit_Model(habit)
                                        print_overview(hm)

                            print('\n')
                            quest.select('Press Enter to Continue',['Okay'],style=state['qstyle']).ask()
                        except Exception as e:
                            print("Failed to get difficulity: ",e)
                            traceback.print_exc()
                            sleep(10)
                
                #Filter option
                elif(ans =='fail'):
                        operator = quest.select('Select one of the operators to use for comparison. Next you will provide a value to compare for. E.g.: fail <= 5, fail > 7', ['>','>=','=','<','<='],style=state['qstyle']).ask()
                        comparison_val = quest.text('Provide a valid number (float or int) that will be used to compare?',style=state['qstyle']).ask()
                        try:
                            if(operator and comparison_val):
                                fail_habits = api.db_get_habits_by_attr_operator(state["active_user"].user_id, 'fail', comparison_val, operator)

                                if(len(fail_habits) < 1):
                                    print('No habits found for your specified filter criteria.')
                                    print('Returning to View screen...')
                                    sleep(2)
                                    return_view_screen(state)

                                print('\n')
                                for habit in fail_habits:
                                        #Converts a unnamed array given by SQLITE of habits to a dict with easy to access attributes
                                        hm = Habit_Model(habit)
                                        print_overview(hm)

                            print('\n')
                            quest.select('Press Enter to Continue',['Okay'],style=state['qstyle']).ask()
                        except Exception as e:
                            print("Failed to get difficulity: ",e)
                            traceback.print_exc()
                            sleep(10)
                
                #Filter option
                elif(ans =='cost'):
                        operator = quest.select('Select one of the operators to use for comparison. Next you will provide a value to compare for. E.g.: fail <= 5, fail > 7', ['>','>=','=','<','<='],style=state['qstyle']).ask()
                        comparison_val = quest.text('Provide a valid number (float or int) that will be used to compare?',style=state['qstyle']).ask()
                        try:
                            if(operator and comparison_val):
                                cost_habits = api.db_get_habits_by_attr_operator(state["active_user"].user_id, 'cost', comparison_val, operator)

                                if(len(cost_habits) < 1):
                                    print('No habits found for your specified filter criteria.')
                                    print('Returning to View screen...')
                                    sleep(2)
                                    return_view_screen(state)

                                print('\n')
                                for habit in cost_habits:
                                        #Converts a unnamed array given by SQLITE of habits to a dict with easy to access attributes
                                        hm = Habit_Model(habit)
                                        print_overview(hm)

                            print('\n')
                            quest.select('Press Enter to Continue',['Okay'],style=state['qstyle']).ask()
                        except Exception as e:
                            print("Failed to get difficulity: ",e)
                            traceback.print_exc()
                            sleep(10)
                
                #Filter option  
                elif(ans =='cost_accum'):
                        operator = quest.select('Select one of the operators to use for comparison. Next you will provide a value to compare for. E.g.: cost_accum <= 5, cost_accum > 7', ['>','>=','=','<','<='],style=state['qstyle']).ask()
                        comparison_val = quest.text('Provide a valid number (float or int) that will be used to compare?',style=state['qstyle']).ask()
                        try:
                            if(operator and comparison_val):
                                cost_accum_habits = api.db_get_habits_by_attr_operator(state["active_user"].user_id, 'cost_accum', comparison_val, operator)

                                if(len(cost_accum_habits) < 1):
                                    print('No habits found for your specified filter criteria.')
                                    print('Returning to View screen...')
                                    sleep(2)
                                    return_view_screen(state)

                                print('\n')
                                for habit in cost_accum_habits:
                                        #Converts a unnamed array given by SQLITE of habits to a dict with easy to access attributes
                                        hm = Habit_Model(habit)
                                        print_overview(hm)

                            print('\n')
                            quest.select('Press Enter to Continue',['Okay'],style=state['qstyle']).ask()
                        except Exception as e:
                            print("Failed to get difficulity: ",e)
                            traceback.print_exc()
                            sleep(10)

                return_view_screen(state)
            
            #Return to user screen options in the view menu
            elif(ans == options[3]):
                return_user_screen(state)

        #Return to view all habits window if ans was set
        view_all(ans)
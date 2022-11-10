#habits:list[habit]
from functools import reduce
from Classes.Habit import Habit

def active_habits(habits:list) -> list:
    '''Receives habits list and returns only the active habits as a list.'''
    total_active = 0

    #For each habit increment if it is active
    for habit in habits:
        if(habit.active):
            total_active += 1
    
    return total_active

def same_period(habits:list, interval:str) -> list:
    '''Receives habits list and returns all habits with the given interval in a list,e.g. 1W.'''
    same_interval = []

    #For each habit increment if it has same interval
    for habit in habits:
        if(habit.interval == interval):
            same_interval.append(habit)
    
    return same_interval

def habit_longest_streak(checkins:list) -> int:
    '''Receives checkins list and counts what the longest uninterrupted streak is of the habit and returns the streak as integer.'''
    #count the amount of consequent successes that are True (when checkins has success = False then a streak has ended!)
    try:
        longest_streak_habit = 0
        current_count = 0

        for checkin in checkins:
            if checkin.success:
                current_count += 1
                if current_count > longest_streak_habit:
                    longest_streak_habit = current_count
            elif not checkin.success:
                current_count = 0

        return longest_streak_habit
    except Exception as e:
        print('habit_longest_streak error:',e)

def most_success(habits:list) -> int:
    '''Receives habits list and finds the max value of success and then returns this highest success as integer.'''
    try:
        return max(habit.success for habit in habits)
    except Exception as e:
        print('most_success error:',e)

def most_fail(habits:list) -> int:
    '''Receives habits list and then finds the max value of fail and then returns this highest fail as integer.'''
    try:
        return max(habit.fail for habit in habits)
    except Exception as e:
        print('most_fail error:',e)

def most_punctual(habits:list) -> [int, str]:
    '''Receives habits list and for each habit in habits looks which has most time remaining on average per checkin until the deadline when the habit was checked in.'''

    #Go through all available checkins and put the time remaining until deadline in a list, then calculate avg of list for habit
    #Store habit and avg time remaining in dict and find max avg (most time remains) and return the habit with its details
    #Make sure it's a pure function!
    try:
        most_time_remain_sec = 0
        most_punctual_habit = None

        #!!!! Make sure that avg time left until deadline for each habit is calculated and based on that see which is most punctual!
        for habit in habits:
            # print(habit.title)
            sum_of_time_left_till_deadline = 0
            total_checkins_habit = len(habit.checkins) if habit.checkins else 1 #Prevent ZeroDivision if 0 habits
            
            #Add time left for each checkin to total sum of time remaining for habit.
            for checkin in habit.checkins:
                sum_of_time_left_till_deadline += checkin.deadline.timestamp() - checkin.checkin_datetime.timestamp()
            
            #Now calc average time left for habit
            avg_time_left = sum_of_time_left_till_deadline / total_checkins_habit
            
            #If we indeed find avg that has more time remaining then update the most_time_remain to the value and set the most_punctual_habit to be the habit object.
            if avg_time_left > most_time_remain_sec:
                most_time_remain_sec = avg_time_left
                most_punctual_habit = habit.title

       

        if(not most_punctual_habit):
            most_punctual_habit = 'Not enough data'
            most_time_remain_sec = 0

        # print('\nMost Punctual Habit: ',most_punctual_habit)
        # print('Time Remaining on AVG: ',most_time_remain_sec)

        #Return the value of most punctual habit
        return [most_time_remain_sec, most_punctual_habit]
        
    except Exception as e:
        print('most_punctual error:',e)

def most_late(habits:list) -> [int, str]:
    '''Receives habits list and for each habit in habits looks which has least time remaining on average per checkin until the deadline when the habit was checked in.'''

    #Go through all available checkins and put the time remaining until deadline in a list, then calculate avg of list for habit
    #Store habit and avg time remaining in dict and find min avg (least time remains) and return the habit with its details
    #Make sure it's a pure function!
    try:
        least_time_remain_sec = 10000000000000000000000000   #Start big so no value is higher than this.
        most_late_habit = None

        #!!!! Make sure that avg time left until deadline for each habit is calculated and based on that see which is most late!
        for habit in habits:
            # print(habit.title)
            sum_of_time_left_till_deadline = 0
            total_checkins_habit = len(habit.checkins) if habit.checkins else 1 #Prevent ZeroDivision if 0 habits
            
            #Add time left for each checkin to total sum of time remaining for habit.
            for checkin in habit.checkins:
                sum_of_time_left_till_deadline += checkin.deadline.timestamp() - checkin.checkin_datetime.timestamp()
            
            #Now calc average time left for habit
            avg_time_left = sum_of_time_left_till_deadline / total_checkins_habit
            
            #If we indeed find avg that has more time remaining then update the most_time_remain to the value and set the most_punctual_habit to be the habit object.
            if avg_time_left < least_time_remain_sec:
                least_time_remain_sec = avg_time_left
                most_late_habit = habit.title


        if(not most_late_habit):
            most_late_habit = 'Not enough data'
            least_time_remain_sec = 0

        # print('\nMost Late Habit: ',most_late_habit)
        # print('Time Remaining on AVG: ',least_time_remain_sec)

        #Return the value of most punctual habit
        return [least_time_remain_sec, most_late_habit]

    except Exception as e:
        print('most_late error:',e)


def most_expensive(habits:list) -> float:
    '''Receives list of habits and returns the highest accumulated cost for a habit'''
    highest_cost = 0

    for habit in habits:
        if habit.cost_accum > highest_cost:
            highest_cost = habit.cost_accum
    
    return highest_cost

def total_longest_current_streak(habits:list):
    '''Receives habits list and returns the highest active streak.'''
    #check for highest streak among habits
    try:
        return max(habit.streak for habit in habits)
    except Exception as e:
        print('total_longest_streak error:',e)

def total_longest_running_streak(habits:list):
    '''Receives habits list and returns the highest running streak.'''
    #check for highest streak among habits
    try:
        highest_running_streak = 0
        current_streak = 0

        for habit in habits:
            for checkin in habit.checkins:
                if checkin.success:
                    current_streak += 1
                    if current_streak > highest_running_streak:
                        highest_running_streak = current_streak
                else:
                    current_streak = 0

        return highest_running_streak
    except Exception as e:
        print('total_longest_streak error:',e)

def total_success(habits:list) -> int:
    '''Receives habits list and counts the total success sum across all habits.'''
    try:
        return sum(habit.success for habit in habits)
    except Exception as e:
        print('total_success error:',e)
    pass

def total_fail(habits:list) -> int:
    '''Receives habits list and counts the total fail sum across all habits.'''
    try:
        return sum(habit.fail for habit in habits)
    except Exception as e:
        print('total_fail error:',e)
    pass

def best_performing_category(habits:list) -> str:
    '''Receives habits list and checks, when category is provided, which has the best success/fail ratio and returns the category label as string.'''
    #Get all unique categories
    categories = {}

    for habit in habits:
        #If category not yet found in categories dict then create a new one with a nesteded dict containing the current habit success and fail
        if(habit.category and habit.category.lower() not in categories.keys()):
            categories[habit.category.lower()] = {'success':habit.success, 'fail':habit.fail, 'ratio':0}
        #If category already exists then add the success and fails to the category from the current habit
        elif(habit.category):
            categories[habit.category.lower()]['success'] += habit.success
            categories[habit.category.lower()]['fail'] += habit.fail
        #If no category then skip the habit
        else:
            pass
    
     #Init counter variable and best_category
    best_ratio = 0
    best_category = ''

    #For each category key, add the success and fail to the dict and calulcate the ratio
    for category in categories.keys():
        success = categories[category]['success']
        fail = categories[category]['fail']
        categories[category]['ratio'] = success/fail if fail else success
        
        #If we can find a newer better success ratio for habit category then update the best
        if(categories[category]['ratio'] > best_ratio):
            best_ratio = categories[category]['ratio']
            best_category = category
        else:
            pass
    
    return best_category    

def best_performing_interval(habits:list) -> str:
    '''Receives habits list and checks which interval has the best success/fail ratio and returns the interval label as string.'''
    #Get all unique intervals
    intervals = {}

    for habit in habits:
        #If interval not yet found in intervals dict then create a new one with a nesteded dict containing the current habit success and fail
        if(habit.interval not in intervals.keys()):
            intervals[habit.interval] = {'success':habit.success, 'fail':habit.fail, 'ratio':0}
        #If interval already exists then add the success and fails to the interval from the current habit
        elif(habit.interval not in intervals.keys()):
            intervals[habit.interval]['success'] += habit.success
            intervals[habit.interval]['fail'] += habit.fail
        #If no interval then skip the habit (should never be the case)
        else:
            pass
    
    #Init counter variable and best_interval
    best_ratio = 0
    best_interval = ''

    #For each interval key, add the success and fail to the dict and calulcate the ratio
    for interval in intervals.keys():
        success = intervals[interval]['success']
        fail = intervals[interval]['fail']
        intervals[interval]['ratio'] = success/fail if fail else success
        
        #Now look for best ratio
        #If we can find a newer better success ratio for habit category then update the best
        if(intervals[interval]['ratio'] > best_ratio):
            best_ratio = intervals[interval]['ratio']
            best_interval = interval
        else:
            pass
    
    #Return the best interval
    return best_interval   

def avg_total_streak(habits:list) -> int:
    '''Receives habits list and calculates the avg streak across all habits.'''
    total_habits = len(habits)
    total_streak = 0

    #For each habit add the streak to total_streak
    for habit in habits:
        total_streak += habit.streak
    
    #Return avg total streak, prevent ZeroDivision
    return total_streak / total_habits if total_habits else total_streak

def avg_break_streak(habits:list) -> int:
    '''Receives habits list and calculates how long on average the user keeps a failing streak in a row'''
    #check for highest streak among habits
    try:
        highest_running_break_streak = 0
        current_break_streak = 0

        for habit in habits:
            for checkin in habit.checkins:
                if not checkin.success:
                    current_break_streak += 1
                    if current_break_streak > highest_running_break_streak:
                        highest_running_break_streak = current_break_streak
                else:
                    current_break_streak = 0

        return highest_running_break_streak
    except Exception as e:
        print('avg_break_streak error:',e)

def avg_time_left(habits:list) -> int:
    '''Receives habits list and calculates the avg time left until deadlines are due, only checks for in-time deadlines, and returns this value as seconds in int.'''

    #Counters
    total_checkins = 0
    total_time_left = 0

    for habit in habits:
        #Add to total amount of checkins
        total_checkins += len(habit.checkins)

        #For each checkin calculate the time difference between deadline and checkin time
        for checkin in habit.checkins:
            if (checkin.deadline.timestamp() > checkin.checkin_datetime.timestamp()):
                time_left_before_deadline = checkin.deadline.timestamp() - checkin.checkin_datetime.timestamp()
                total_time_left += time_left_before_deadline
    
    #Return the average time left, prevent ZeroDivision
    return total_time_left / total_checkins if total_checkins else total_time_left

def earliest(habits:list) -> Habit:
    '''Receives habits and checks which habit has the most early deadline to be met and the habit is returned.'''
    return reduce(lambda x,y: x if x.next_deadline < y.next_deadline else y, habits)

def indiv_max_streak(habit) -> int:
    '''Receives a habit and returns the highest streak ever achieved for habit as int.'''
    highest_streak = 0
    current_streak = 0

    for checkin in habit.checkins:
        if checkin.success:
            current_streak += 1
            if current_streak > highest_streak:
                highest_streak = current_streak
        else:
            current_streak = 0
    
    return highest_streak

def indiv_avg_streak(habit) -> int:
    '''Receives a habit and returns the avg streak for habit as float.'''
    number_of_streaks = 0
    streak_sum = 0
    on_streak = False

    for checkin in habit.checkins:
        if checkin.success and not on_streak:
            on_streak = True
            streak_sum += 1
            number_of_streaks += 1
            # print('Streak Sum: ',streak_sum)
        elif checkin.success and on_streak:
            streak_sum += 1
            # print('Streak Sum (on streak): ',streak_sum)
        else:
            on_streak = False
    
    #Prevent ZeroDivision
    return float((streak_sum) / (number_of_streaks if number_of_streaks > 0 else 1))
    

def indiv_avg_rating(habit) -> float:
    '''Receives a habit and calculates the average reported checkin rating for the user and returns it as a float.'''
    tot_sum = 0
    #Prevent ZeroDivision
    tot_checkins = len(habit.checkins) if habit.checkins else 1
    
    for checkin in habit.checkins:
        tot_sum += int(checkin.rating)
    
    return float(tot_sum / tot_checkins)


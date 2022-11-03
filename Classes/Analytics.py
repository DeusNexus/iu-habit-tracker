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

def most_punctual(habits:list) -> int:
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
            for checkin in habit.checkins:

                current_remain = 0
                current_remain = checkin.deadline.timestamp() - checkin.checkin_datetime.timestamp()
                print('Most Punctual Current remaining: ',current_remain)

                #Compare current remaining against most_time_remain for previous habits, it it has high time remaining it is more punctual.
                if current_remain > most_time_remain_sec:
                    most_time_remain_sec = current_remain
                    most_punctual_habit = habit

        #Return the value of most punctual habit
        print('Most punctual habit: ',habit.title)
        return most_time_remain_sec
        
    except Exception as e:
        print('most_punctual error:',e)

def most_late(habits:list) -> int:
    '''Receives habits list and for each habit in habits looks which has least time remaining on average per checkin until the deadline when the habit was checked in.'''

    #Go through all available checkins and put the time remaining until deadline in a list, then calculate avg of list for habit
    #Store habit and avg time remaining in dict and find min avg (least time remains) and return the habit with its details
    #Make sure it's a pure function!
    try:
        least_time_remain_sec = 100000000000000000000000000
        most_late_habit = None

        #!!!! Make sure that avg time left until deadline for each habit is calculated and based on that see which is most late!
        for habit in habits:
            for checkin in habit.checkins:
                current_remain = 0
                current_remain = checkin.deadline.timestamp() - checkin.checkin_datetime.timestamp()
                print('Most Late Current remaining: ',current_remain)
                
                #Compare the current least_time_remain from all previous habits with current_remain of habit, if it is less then update this to be a more late habit (less time left until deadline)
                if current_remain < least_time_remain_sec and current_remain > 0:
                    least_time_remain_sec = current_remain
                    most_late_habit = habit
                    print('Found habit with less time remaining (updated least_time_remain & most_late_habit): ',least_time_remain_sec)

        #After all habits return the value of most_late habit
        print('Most late habit: ',habit.title)
        return least_time_remain_sec

    except Exception as e:
        print('most_late error:',e)

def total_longest_streak(habits:list):
    '''Receives habits list and returns the habit with the highest streak.'''
    #check for highest streak among habits
    try:
        return max(habit.streak for habit in habits)
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
        categories[category]['ratio'] = success/fail
        
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
        intervals[interval]['ratio'] = success/fail
        
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
    
    #Return avg total streak
    return total_streak / total_habits

def avg_break_streak(habits:list) -> int:
    '''Receives habits list and calculates ....?'''
    pass

def avg_time_left(habits:list) -> int:
    '''Receives habits list and calculates the avg time left until deadlines are due and returns this value as seconds in int.'''

    #Counters
    total_checkins = 0
    total_time_left = 0

    for habit in habits:
        #Add to total amount of checkins
        total_checkins += len(habit.checkins)

        #For each checkin calculate the time difference between deadline and checkin time
        for checkin in habit.checkins:
            time_left_before_deadline = checkin.deadline - checkin.checkin_datetime
            total_time_left += time_left_before_deadline
    
    #Return the average time left
    return total_time_left / total_checkins

def earliest(habits:list) -> Habit:
    '''Receives habits and checks which habit has the most early deadline to be met and the habit is returned.'''
    return reduce(lambda x,y: x if x.next_deadline < y.next_deadline else y, habits)
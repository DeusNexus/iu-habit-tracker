#habits:list[habit]
from functools import reduce
from Classes.Habit import Habit

def active_habits(habits:list) -> list:
    '''Receives habits list and returns only the active habits as a list.'''
    pass

def same_period(habits:list, interval:str) -> list:
    '''Receives habits list and returns all habits with the given interval,e.g. 1W.'''
    pass

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
        print(e)

def most_success(habits:list) -> int:
    '''Receives habits list and finds the max value of success and then returns this highest success as integer.'''
    try:
        return max(habit.success for habit in habits)
    except Exception as e:
        print(e)

def most_fail(habits:list) -> int:
    '''Receives habits list and then finds the max value of fail and then returns this highest fail as integer.'''
    try:
        return max(habit.fail for habit in habits)
    except Exception as e:
        print(e)

def most_punctual(habits:list) -> int:
    '''Receives habits list and for each habit in habits looks which has most time remaining on average per checkin until the deadline when the habit was checked in.'''

    #Go through all available checkins and put the time remaining until deadline in a list, then calculate avg of list for habit
    #Store habit and avg time remaining in dict and find max avg (most time remains) and return the habit with its details
    #Make sure it's a pure function!
    try:
        most_time_remain_sec = 0
        most_punctual_habit = None
        current_remain = 0

        #!!!! Make sure that avg time left until deadline for each habit is calculated and based on that see which is most punctual!
        for habit in habits:
            for checkin in habit.checkins:
                current_remain = checkin.deadline.timestamp() - checkin.checkin_datetime.timestamp()
                if current_remain > most_time_remain_sec:
                    most_time_remain_sec = current_remain
                    most_punctual_habit = habit

        print('Most punctual habit: ',habit.title)
        return most_time_remain_sec
    except Exception as e:
        print(e)

def most_late(habits:list) -> int:
    '''Receives habits list and for each habit in habits looks which has least time remaining on average per checkin until the deadline when the habit was checked in.'''

    #Go through all available checkins and put the time remaining until deadline in a list, then calculate avg of list for habit
    #Store habit and avg time remaining in dict and find min avg (least time remains) and return the habit with its details
    #Make sure it's a pure function!
    try:
        least_time_remain_sec = 100000000000000000000000000
        most_late_habit = None
        current_remain = 0

        #!!!! Make sure that avg time left until deadline for each habit is calculated and based on that see which is most late!
        for habit in habits:
            for checkin in habit.checkins:
                print('Current remaining: ',current_remain)
                current_remain = checkin.deadline.timestamp() - checkin.checkin_datetime.timestamp()
                print('Current remaining: ',current_remain)
                if current_remain < least_time_remain_sec and least_time_remain_sec != 0:
                    least_time_remain_sec = current_remain
                    most_late_habit = habit
        print('Most late habit: ',habit.title)
        return least_time_remain_sec
    except Exception as e:
        print(e)

def total_longest_streak(habits:list):
    '''Receives habits list and returns the habit with the highest streak.'''
    #check for highest streak among habits
    try:
        return max(habit.streak for habit in habits)
    except Exception as e:
        print(e)

def total_success(habits:list) -> int:
    '''Receives habits list and counts the total success sum across all habits.'''
    try:
        return sum(habit.success for habit in habits)
    except Exception as e:
        print(e)
    pass

def total_fail(habits:list) -> int:
    '''Receives habits list and counts the total fail sum across all habits.'''
    try:
        return sum(habit.fail for habit in habits)
    except Exception as e:
        print(e)
    pass

def best_performing_category(habits:list) -> str:
    '''Receives habits list and checks, when category is provided, which has the best success/fail ratio and returns the category label as string.'''
    pass

def best_performing_interval(habits:list) -> str:
    '''Receives habits list and checks which interval has the best success/fail ratio and returns the interval label as string.'''
    pass

def avg_total_streak(habits:list) -> int:
    '''Receives habits list and calculates the avg streak across all habits.'''
    pass

def avg_break_streak(habits:list) -> int:
    '''Receives habits list and calculates ....?'''
    pass

def avg_time_left(habits:list) -> int:
    '''Receives habits list and calculates the avg time left until deadlines are due and returns this value as seconds in int.'''
    pass

def earliest(habits:list) -> Habit:
    '''Receives habits and checks which habit has the most early deadline to be met and the habit is returned.'''
    return reduce(lambda x,y: x if x.next_deadline < y.next_deadline else y, habits)
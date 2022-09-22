#habits:list[habit]
from functools import reduce

def active_habits(habits:list) -> list:
    pass

def same_period(habits:list, interval:str) -> list:
    pass

def habit_longest_streak(checkins:list) -> int:
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
    try:
        return max(habit.success for habit in habits)
    except Exception as e:
        print(e)

def most_fail(habits:list) -> int:
    try:
        return max(habit.fail for habit in habits)
    except Exception as e:
        print(e)

def most_punctual(habits:list) -> int:
    #Go through all available checkins and put the time remaining until deadline in a list, then calculate avg of list for habit
    #Store habit and avg time remaining in dict and find max avg (most time remains) and return the habit with its details
    #Make sure it's a pure function!
    try:
        most_time_remain_sec = 0
        most_punctual_habit = None
        current_remain = 0

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
    #Go through all available checkins and put the time remaining until deadline in a list, then calculate avg of list for habit
    #Store habit and avg time remaining in dict and find min avg (least time remains) and return the habit with its details
    #Make sure it's a pure function!
    try:
        least_time_remain_sec = 1000000000000000000000
        most_late_habit = None
        current_remain = 0

        for habit in habits:
            for checkin in habit.checkins:
                current_remain = checkin.deadline.timestamp() - checkin.checkin_datetime.timestamp()
                if current_remain < least_time_remain_sec and least_time_remain_sec != 0:
                    least_time_remain_sec = current_remain
                    most_late_habit = habit
        print('Most late habit: ',habit.title)
        return least_time_remain_sec
    except Exception as e:
        print(e)

def total_longest_streak(habits:list):
    #check for highest streak among habits
    try:
        return max(habit.streak for habit in habits)
    except Exception as e:
        print(e)

def total_success(habits:list) -> int:
    try:
        return sum(habit.success for habit in habits)
    except Exception as e:
        print(e)
    pass

def total_fail(habits:list) -> int:
    try:
        return sum(habit.fail for habit in habits)
    except Exception as e:
        print(e)
    pass

def best_performing_category(habits:list) -> str:
    pass

def best_performing_interval(habits:list) -> str:
    pass

def avg_total_streak(habits:list) -> int:
    pass

def avg_break_streak(habits:list) -> int:
    pass

def avg_time_left(habits:list) -> int:
    pass
from datetime import datetime

def interval_to_seconds(intrv: str) -> int:
    '''Interval is given as a string with whole integer followed by m/H/D/W/M/Y, e.g. 1m,5H,10D,2W,1Y and then returned as total seconds duration.'''
    time = {
        'm':60,
        'H':60*60,
        'D':60*60*24,
        'W':60*60*24*7,
        'M':60*60*24*7*4,
        'Y':60*60*24*365
    }

    try:
        #multiply the found value of char in time by numbers - e.g. 2D = 2 * time['D'] 
        char:str = intrv[-1]
        num:int = int(intrv[:-1])

        if num == 0 or num < 1 or intrv[0] == '0':
            raise ValueError('Invalid Numerical Prefix')
            
        return num * time[char]

    except ValueError as e:
        print(e)

def add_streak_to_deadline(deadline: datetime, seconds: int) -> datetime:
    '''Receives a deadline date and adds the number of seconds to the date to provide us with the new next deadline which is returned as datetime.'''
    return datetime.fromtimestamp((seconds + deadline.timestamp()))

def stylize(src: str, style:str = 'bold') -> str:
    '''Receives text as string, a pre-defined style and then decorates the string with the style codes and returns the styled string as string.'''
    
    styles = {
        'bold': '\033[1m',
        'end': '\033[0m'
    }

    return styles[style]+src+styles['end']
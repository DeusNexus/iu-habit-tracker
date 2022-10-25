from datetime import datetime
from shortuuid import ShortUUID

#Child Class
from Classes.CheckIn import CheckIn

#Functions
from Utils import interval_to_seconds, add_streak_to_deadline, interval_to_seconds

class Habit:
    def __init__(
            self,
            title:str,
            description:str,
            interval:str,
            active:bool=True,
            start_from:datetime=None,
            difficulity:int=None,
            category:str=None,
            moto:str=None,
            importance:int=None,
            milestone:int=None,
            style:int=0,
            is_dynamic:bool=False,
            checkin_num_before_deadline:int=1,
            habit_id:str=None,
            ) -> None:

        '''Initializes a new Habit instance with the supplied arguments, can be normal or dynamic which indicate how the streak habit is interpreted and deadline met.'''
        #user-defined
        self.title:str = title
        self.description:str = description
        self.interval:str = interval
        self.active:bool = active
        self.start_from:datetime = start_from
        self.difficulity:int = difficulity
        self.category:str = category
        self.moto:str = moto
        self.importance:int = importance
        self.style:int = style
        self.milestone_streak:int = milestone
        self.is_dynamic:bool = is_dynamic
        self.checkin_num_before_deadline:int = checkin_num_before_deadline

        #dynamic checkin counter
        self.dynamic_count:int = 0
 
        #Datetime now for all initial variables
        date = datetime.now()

        self.habit_id:str = habit_id if habit_id else ShortUUID().random(length=5).lower()
        self.created_on:datetime = date
        self.prev_deadline: datetime = date
        self.next_deadline: datetime = add_streak_to_deadline(self.prev_deadline, interval_to_seconds(self.interval))

        #initialize counters
        self.streak:int = 0
        self.success:int = 0
        self.fail:int = 0
        self.cost:float = 0
        self.cost_accum:float = 0

        #checkin list - childeren of habit
        self.checkins:list[CheckIn] = []

    def overwrite(self,
            user_id:str,
            habit_id:str,
            title:str,
            description:str,
            interval:str,
            active:str,
            start_from:str,
            difficulity:int,
            category:str,
            moto:str,
            importance:int,
            milestone_streak:int,
            style:int,
            is_dynamic:str,
            checkin_num_before_deadline:int,
            dynamic_count:int,
            created_on:str,
            prev_deadline:str,
            next_deadline:str,
            streak:int,
            success:int,
            fail:int,
            cost:float,
            cost_accum:float):

        """The function is used in combination with user_id to overwrite values of internal user class when a user already exists in DB"""
        self.user_id:str = user_id
        self.title:str = title
        self.description:str = description
        self.interval:str = interval
        self.active:bool = bool(active)
        self.start_from:datetime = datetime.strptime(start_from, "%Y-%m-%d %H:%M:%S.%f") if not start_from == '' else None
        self.difficulity:int = difficulity
        self.category:str = category
        self.moto:str = moto
        self.importance:int = importance
        self.milestone_streak:int = milestone_streak
        self.style:int = style
        self.is_dynamic:bool = bool(is_dynamic)
        self.checkin_num_before_deadline:int = checkin_num_before_deadline
        self.habit_id:str = habit_id if habit_id else ShortUUID().random(length=5).lower()
        self.dynamic_count:int = dynamic_count
        self.created_on:datetime = datetime.strptime(created_on, "%Y-%m-%d %H:%M:%S.%f")
        self.prev_deadline: datetime = datetime.strptime(prev_deadline, "%Y-%m-%d %H:%M:%S.%f")
        self.next_deadline: datetime = datetime.strptime(next_deadline,  "%Y-%m-%d %H:%M:%S.%f")
        self.streak:int = streak
        self.success:int = success
        self.fail:int = fail
        self.cost:float = cost
        self.cost_accum:float = cost_accum
        self.checkins:list[CheckIn] = []
        

    def update_deadlines(self) -> None:
        '''Updates the previous_deadline to the current and sets the next_deadline to current deadline plus habit interval length.'''
        old_deadline = self.prev_deadline
        self.prev_deadline: datetime = self.next_deadline
        self.next_deadline: datetime = add_streak_to_deadline(self.prev_deadline, interval_to_seconds(self.interval))

    def incr_streak(self) -> None:
        '''Increases the habit streak by 1'''
        self.streak += 1
    def reset_streak(self) -> None:
        '''Resets the habit streak to 0'''
        self.streak = 0
    def incr_success(self) -> None:
        '''Increases the total successfully met deadlines by 1'''
        self.success += 1
    def incr_fail(self) -> None:
        '''Increases the total failed deadlines by 1'''
        self.fail += 1
    def dynamic_incr(self) -> None:
        '''Increases dynamic checkin count by 1. Once the checkin count reaches the dynamic checkin goal value before the deadline the habit is considered successfull and next streak begins. '''
        self.dynamic_count += 1
    def dynamic_reset(self) -> None:
        '''Resets the dynamic checkin count to 0. If the deadline of a dynamic habit is not reached with the required checkin goal count the dynamic streak resets back to 0. The user can then attempt to reach the dynamic goal before the new the next_deadline.'''
        self.dynamic_count = 0

    def checkin(self,note:str,rating:int) -> None:
        '''Used to checkin a habit and user can optionally provide a note to himself and a rating how well it went. 
        For regular habit if the deadline is met the streak is increased and deadline updated. All checkins are appended to the Habit checkins list.'''
        if self.is_dynamic:
            raise ValueError('Tried to checkin with regular checkin method for a dynamic habit!')
        #Check if deadline is success or failed
        now = datetime.now() #.strftime('%Y-%m-%d %H:%M:%S.%f')
        print('\n[CHECKIN] Next Deadline: ',self.next_deadline,' Now:' ,now)
        if(now <= self.next_deadline):
            #Insert successful checkin to checkins list
            self.checkins.append(CheckIn(self.next_deadline,True,note,rating,self.cost,self.cost_accum))
            #success checkin before deadline
            self.incr_streak()
            self.update_deadlines()
            
        else:
            #failed checkin
            #Insert failed checkin to checkins list
            self.checkins.append(CheckIn(self.next_deadline,False,note,rating,self.cost,self.cost_accum))

            self.reset_streak()
            self.update_deadlines()
            

    def dynamic_checkin(self,note:str,rating:int):
        '''Used to checkin a dynamic habit and user can optionally provide a note to himself and a rating how well it went. 
        For dynamic habit it checks if the goal count is reached or the deadline is due and updates the dynamic streak and deadlines accordingly. All checkins are appended to the Habit checkins list.'''
        if not self.is_dynamic:
            raise ValueError('Tried to checkin with dynamic checkin method for a regular habit!')
        #Compare if we haven't exceeded deadline yet with less than required checkins
        now = datetime.now() #.strftime('%Y-%m-%d %H:%M:%S.%f')
        print('\n[CHECKIN] Next Deadline: ',self.next_deadline,' Now:' ,now, ' Checkin Target:', self.checkin_num_before_deadline)
        if(now <= self.next_deadline and self.dynamic_count < self.checkin_num_before_deadline):
            #success dynamic checkin before deadline
            self.dynamic_incr()
            #Insert successful checkin to checkins list
            self.checkins.append(CheckIn(self.next_deadline,True,note,rating,self.cost,self.cost_accum,True,self.dynamic_count))

        #Still before deadline but this checkin target is met and therefor the dynamic habit has completed its goal for current deadline!    
        elif(now <= self.next_deadline and self.dynamic_count >= self.checkin_num_before_deadline):
            #Insert final checkin to checkins list before resetting the habit counters
            self.checkins.append(CheckIn(self.next_deadline,True,note,rating,self.cost,self.cost_accum,True,self.dynamic_count))
            #Reset counter for next deadline
            self.dynamic_reset()
            #Update deadline to next interval
            self.update_deadlines()
        
        #Failed checkins, deadline is met but dynamic checkin count hasn't meet target
        elif(now > self.next_deadline and self.dynamic_count < self.checkin_num_before_deadline):
            #Insert failed checkin to checkins list
            self.checkins.append(CheckIn(self.next_deadline,False,note,rating,self.cost,self.cost_accum,True,self.dynamic_count))
             #failed checkin
            self.reset_streak()
            self.update_deadlines()
            self.dynamic_reset()            


    def info_habit(self) -> None:
        '''Used for debugging to print Habit information to the terminal.'''
        habit_type = '[]'
        if self.is_dynamic:
            habit_type = '[ Dynamic ]'
        else:
            habit_type = '[ Regular ]'
        return print(f'[{self.title}: {self.description}] {habit_type}\nCreated on: {self.created_on} \nDeadline: {self.next_deadline}')

    def info_checkins(self) -> None:
        '''Used for debugging, iterates over the checkins of a habit and prints information out for each checkin.'''
        for checkin in self.checkins:
            checkin.info_checkin()

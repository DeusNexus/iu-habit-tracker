from datetime import datetime
from shortuuid import ShortUUID

#Child Class
from Classes.CheckIn import CheckIn

#Functions
from Utils import interval_to_seconds, add_streak_to_deadline, interval_to_seconds, style

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
            is_dynamic:bool=False,
            checkin_num_before_deadline:int=1,
            habit_id:str=None,
            user_id: str=None,
            cost:float=0
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
        self.milestone_streak:int = milestone
        self.is_dynamic:bool = is_dynamic
        self.checkin_num_before_deadline:int = checkin_num_before_deadline

        #dynamic checkin counter
        self.dynamic_count:int = 0
 
        #Datetime now for all initial variables
        date = datetime.now()
        
        self.user_id:str = user_id
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
        self.habit_id:str = habit_id if habit_id else ShortUUID().random(length=5).lower()
        self.title:str = title
        self.description:str = description
        self.interval:str = interval
        self.active:bool = active
        self.start_from = datetime.now() if start_from == '' else start_from
        self.difficulity:int = difficulity
        self.category:str = category
        self.moto:str = moto
        self.importance:int = importance
        self.milestone_streak:int = milestone_streak
        self.is_dynamic:bool = is_dynamic
        self.checkin_num_before_deadline:int = checkin_num_before_deadline
        self.dynamic_count:int = dynamic_count
        self.created_on:datetime = created_on
        self.prev_deadline: datetime = prev_deadline
        self.next_deadline: datetime = next_deadline
        self.streak:int = streak
        self.success:int = success
        self.fail:int = fail
        self.cost:float = cost
        self.cost_accum:float = cost_accum
        self.checkins:list[CheckIn] = []
        
    def update_deadlines(self) -> None:
        '''Updates the previous_deadline to the current and sets the next_deadline to current deadline plus habit interval length.'''
        self.prev_deadline: datetime = self.next_deadline
        self.next_deadline: datetime = add_streak_to_deadline(self.prev_deadline, interval_to_seconds(self.interval))

        print(style(f'Updating your deadline to new one based on your given habit interval!','GREEN'))
        print(
            style(f'\n{self.title}','UNDERLINE')+
            '\nOld Deadline: '+
            style(f'{self.prev_deadline.strftime("%Y-%m-%d %H:%M")}', 'CYAN') +   
            '\nNew Deadline: ' + 
            style(f'{self.next_deadline.strftime("%Y-%m-%d %H:%M")}','YELLOW') +
            '\nInterval: ' +
            style(f'{self.interval}','BLUE')+
            '\nNew Streak: '+
            style(f'{self.streak}','BOLD'))
        
        if(self.milestone_streak):
            if(self.milestone_streak > 0):
                if(self.streak % self.milestone_streak == 0):
                    print(f'You completed a milestone streak with {self.milestone_streak} uninterrupted successful checkins!')

    def update_deadlines_failed(self) -> None:
        '''Updates the previous_deadline to the current and sets the next_deadline to current deadline based on date in the future plus the interval.'''
        self.prev_deadline: datetime = self.next_deadline
        #Add interval to now instead of old deadline (can be far in the past and give a new deadline in the past).
        self.next_deadline: dattime = add_streak_to_deadline(datetime.now(), interval_to_seconds(self.interval))
        print(style(f'You failed to meet your habit checkin deadline! This means that your current streak is reset back to 0. \nSince your deadline is in the past the new deadline will be based on current date plus your specified interval.','RED'))
        print(
            style(f'\n{self.title}','UNDERLINE')+
            '\nOld Deadline: '+
            style(f'{self.prev_deadline.strftime("%Y-%m-%d %H:%M")}', 'CYAN') +   
            '\nNew Deadline: ' + 
            style(f'{self.next_deadline.strftime("%Y-%m-%d %H:%M")}','YELLOW') +
            '\nInterval: ' +
            style(f'{self.interval}','BLUE')+
            style(f'\nNew Streak: {self.streak}','BOLD'))

    def update_deadline_now_active(self):
        '''Updates the deadline when start_from triggers the habit to become active in a future date. It adds the specified interval to the start_from date.'''
        self.prev_deadline: datetime = self.next_deadline
        self.next_deadline: datetime = add_streak_to_deadline(self.start_from, interval_to_seconds(self.interval))

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
    def incr_cost(self) -> None:
        '''Increase the accum_cost when a habit is performed.'''
        self.cost_accum = self.cost + self.cost_accum

    def checkin(self,note:str,rating:int) -> None:
        '''Used to checkin a habit and user can optionally provide a note to himself and a rating how well it went. 
        For regular habit if the deadline is met the streak is increased and deadline updated. All checkins are appended to the Habit checkins list.'''
        if self.is_dynamic:
            raise ValueError('Tried to checkin with regular checkin method for a dynamic habit!')
        #Check if deadline is success or failed
        now = datetime.now()

        if(now <= self.next_deadline):
            #Insert successful checkin to checkins list
            self.checkins.append(
                CheckIn(
                    user_id=self.user_id,
                    habit_id=self.habit_id,
                    checkin_id='', #Generated instead
                    deadline=self.next_deadline,
                    success=True,   #Deadline was met
                    note=note,
                    rating=rating,
                    cost=self.cost,
                    cost_accum=self.cost_accum,
                    dynamic=False,
                    dynamic_count=0))
            self.incr_cost()
            #success checkin before deadline
            self.incr_streak()
            self.incr_success()
            self.update_deadlines()
            
        else:
            #failed checkin
            #Insert failed checkin to checkins list
            self.checkins.append(
                CheckIn(
                    user_id=self.user_id,
                    habit_id=self.habit_id,
                    checkin_id='', #Generated instead
                    deadline=self.next_deadline,
                    success=False,   #Deadline was met
                    note=note,
                    rating=rating,
                    cost=self.cost,
                    cost_accum=self.cost_accum,
                    dynamic=False,
                    dynamic_count=0)
                    )
            self.incr_cost()
            self.reset_streak()
            self.incr_fail()
            self.update_deadlines_failed()
            

    def dynamic_checkin(self,note:str,rating:int):
        '''Used to checkin a dynamic habit and user can optionally provide a note to himself and a rating how well it went. 
        For dynamic habit it checks if the goal count is reached or the deadline is due and updates the dynamic streak and deadlines accordingly. All checkins are appended to the Habit checkins list.'''
        if not self.is_dynamic:
            raise ValueError('Tried to checkin with dynamic checkin method for a regular habit!')
        #Compare if we haven't exceeded deadline yet with less than required checkins
        now = datetime.now()
        
        #Target of 3
        #Current is 2
        if(now <= self.next_deadline and self.dynamic_count < (int(self.checkin_num_before_deadline) - 1)):
            #success dynamic checkin before deadline
            self.dynamic_incr()
            self.incr_cost()
            #Insert successful checkin to checkins list
            self.checkins.append(
                CheckIn(
                    user_id=self.user_id,
                    habit_id=self.habit_id,
                    checkin_id='',
                    deadline=self.next_deadline,
                    success=True,   #Dynamic (partial) deadline was met
                    note=note,
                    rating=rating,
                    cost=self.cost,
                    cost_accum=self.cost_accum,
                    dynamic=True,
                    dynamic_count=self.dynamic_count)
            )
            print(
                '\nYou '+
                style('successfully','GREEN')+
                ' checked in before the deadline of your dynamic habit. '+
                '\nYou current checkin target is now '+
                style(f'{self.dynamic_count}','CYAN')+
                ' of '+
                style(f'{self.checkin_num_before_deadline}','PURPLE')+
                ', your streak is '+
                style(f'{self.streak}','BOLD')+
                ' and next (current) deadline still on '+
                style(f'{self.next_deadline.strftime("%Y-%m-%d %H:%M")}.','YELLOW'))

        #Still before deadline but this checkin target is met and therefor the dynamic habit has completed its goal for current deadline!    
        elif(now <= self.next_deadline and self.dynamic_count >= self.checkin_num_before_deadline - 1):
            #Insert final checkin to checkins list before resetting the habit counters
            self.checkins.append(
                CheckIn(
                    user_id=self.user_id,
                    habit_id=self.habit_id,
                    checkin_id='',
                    deadline=self.next_deadline,
                    success=True,   #Deadline was met
                    note=note,
                    rating=rating,
                    cost=self.cost,
                    cost_accum=self.cost_accum,
                    dynamic=True,
                    dynamic_count=self.dynamic_count)
            )
            #Reset counter for next deadline
            self.incr_cost()
            self.dynamic_reset()
            self.incr_streak()
            self.incr_success()
            #Update deadline to next interval
            self.update_deadlines()
            print(
                '\nYou '+
                style('successfully','GREEN')+
                ' checked in before the deadline of your dynamic habit and you have reached your checkin goal! '+
                'This means you increment your habit streak by one and have a new deadline to meet. '+
                '\nYou current checkin target is now '+
                style(f'{self.dynamic_count}','CYAN')+
                ' of '+
                style(f'{self.checkin_num_before_deadline}','PURPLE')+
                ', your streak is '+
                style(f'{self.streak}','BOLD')+
                ' and new deadline is on '+
                style(f'{self.next_deadline.strftime("%Y-%m-%d %H:%M")}.','YELLOW'))
        
        #Failed checkins, deadline is met but dynamic checkin count hasn't meet target
        elif(now > self.next_deadline and self.dynamic_count < self.checkin_num_before_deadline):
            #Insert failed checkin to checkins list
            self.checkins.append(
                CheckIn(
                    user_id=self.user_id,
                    habit_id=self.habit_id,
                    checkin_id='',
                    deadline=self.next_deadline,
                    success=False,   #Deadline failed
                    note=note,
                    rating=rating,
                    cost=self.cost,
                    cost_accum=self.cost_accum,
                    dynamic=True,
                    dynamic_count=self.dynamic_count)
            )
            self.incr_cost()
            #failed checkin
            self.reset_streak()
            self.incr_fail()
            self.dynamic_reset()
            #Update failed deadline to by in future
            self.update_deadlines_failed()
            print(
                '\nYou '+
                style('failed','RED')+
                ' to checked in before the deadline of your dynamic habit therefor lose your streak! A new deadline is created and you need to start over with your checkin target for the provided interval. '+
                '\nYou current checkin target is now '+
                style(f'{self.dynamic_count}','CYAN')+
                ' of '+
                style(f'{self.checkin_num_before_deadline}','PURPLE')+
                ', your streak is '+
                style(f'{self.streak}','BOLD')+
                ' and new deadline is on '+
                style(f'{self.next_deadline.strftime("%Y-%m-%d %H:%M")}.','YELLOW'))

    def info_habit(self) -> None:
        '''Used for debugging to print Habit information to the terminal.'''
        habit_type = '[]'
        if self.is_dynamic:
            habit_type = '[Dynamic]'
        else:
            habit_type = '[Regular]'
        return print(
            f'{habit_type} '+
            style(f'[{self.title}: {self.description}] ','BLUE')+
            '\nCreated on: '+
            style(f'{self.created_on.strftime("%Y-%m-%d %H:%M")}','CYAN')+
            ' \nCurrent Deadline: '+
            style(f'{self.next_deadline.strftime("%Y-%m-%d %H:%M")}','YELLOW'))

    def info_checkins(self) -> None:
        '''Used for debugging, iterates over the checkins of a habit and prints information out for each checkin.'''
        for checkin in self.checkins:
            checkin.info_checkin()

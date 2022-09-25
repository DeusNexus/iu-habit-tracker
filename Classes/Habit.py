from datetime import datetime
from shortuuid import ShortUUID

#Child Class
from Classes.CheckIn import CheckIn

#Functions
from Utils import interval_to_seconds, add_streak_to_deadline, interval_to_seconds

class Habit:
    def __init__(
            self,
            title:str='My Habit',
            description:str='Habit Description',
            interval:str='1H',
            active:bool=True,
            start_from:datetime=None,
            difficulity:int=None,
            category:str=None,
            moto:str=None,
            importance:int=None,
            push_notif:bool=False,
            milestone:int=None,
            style:int=0,
            is_dynamic:bool=False,
            checkin_num_before_deadline:int=1
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
        self.push_notif:bool = push_notif
        self.style:int = style
        self.milestone_streak:int = milestone
        self.is_dynamic:bool = is_dynamic
        self.checkin_num_before_deadline:int = checkin_num_before_deadline

        #dynamic checkin counter
        self.dynamic_count:int = 0
 
        #Datetime now for all initial variables
        date = datetime.now()

        self.habit_id:str = ShortUUID().random(length=5).lower()
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
        self.dynamic_checkin += 1
    def dynamic_reset(self) -> None:
        '''Resets the dynamic checkin count to 0. If the deadline of a dynamic habit is not reached with the required checkin goal count the dynamic streak resets back to 0. The user can then attempt to reach the dynamic goal before the new the next_deadline.'''
        self.dynamic_checkin = 0

    def checkin(self,note:str,rating:int) -> None:
        '''Used to checkin a habit and user can optionally provide a note to himself and a rating how well it went. 
        For regular habit if the deadline is met the streak is increased and deadline updated. All checkins are appended to the Habit checkins list.'''
        #Check if deadline is success or failed
        now = datetime.now()
        #print('\n[CHECKIN] Next Deadline: ',self.next_deadline,' Now:' ,now)
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
        #Compare if we haven't exceeded deadline yet with less than required checkins
        now = datetime.now()
        print('\n[CHECKIN] Next Deadline: ',self.next_deadline,' Now:' ,now, ' Checkin Target:', checkin_num_before_deadline)
        if(now <= self.next_deadline and dynamic_count < checkin_num_before_deadline):
            #success dynamic checkin before deadline
            self.dynamic_incr()
            #Insert successful checkin to checkins list
            self.checkins.append(CheckIn(self.next_deadline,True,note,rating,self.cost,self.cost_accum,True,self.dynamic_count))

        #Still before deadline but this checkin target is met and therefor the dynamic habit has completed its goal for current deadline!    
        elif(now <= self.next_deadline and dynamic_count >= checkin_num_before_deadline):
            #Insert final checkin to checkins list before resetting the habit counters
            self.checkins.append(CheckIn(self.next_deadline,True,note,rating,self.cost,self.cost_accum,True,self.dynamic_count))
            #Reset counter for next deadline
            self.dynamic_reset()()
            #Update deadline to next interval
            self.update_deadlines()
        
        #Failed checkins, deadline is met but dynamic checkin count hasn't meet target
        elif(now > self.next_deadline and dynamic_count < checkin_num_before_deadline):
            #Insert failed checkin to checkins list
            self.checkins.append(CheckIn(self.next_deadline,False,note,rating,self.cost,self.cost_accum,True,self.dynamic_count))
             #failed checkin
            self.reset_streak()
            self.update_deadlines()
            self.dynamic_reset()            


    def info_habit(self) -> None:
        '''Used for debugging to print Habit information to the terminal.'''
        return print(f'{self.title}: {self.description} \nCreated on: {self.created_on} \nDeadline: {self.next_deadline}\n')

    def checkins(self) -> None:
        '''Used for debugging, iterates over the checkins of a habit and prints information out for each checkin.'''
        for checkin in self.checkins:
            checkin.info_checkin()

# #Test data
# sport = Habit('Sport','1D')
# print('[HABIT] Created: ',sport.created_on, 'Prev_deadline:',sport.prev_deadline, 'Next_deadline:',sport.next_deadline, sep='\n')
# sport.checkin('Good Job!',3)
# for checkin in sport.checkins:
#     print('Checkin Date',checkin.checkin_datetime, 'Checkin Note:',checkin.note, 'Checkin Success:',checkin.success,sep='\n')
# print('Streak:',sport.streak)
# sport.checkin('Getting beter!',5)
# for checkin in sport.checkins:
#     print('Checkin Date',checkin.checkin_datetime, 'Checkin Note:',checkin.note, 'Checkin Success:',checkin.success,sep='\n')
# print('Streak:',sport.streak)

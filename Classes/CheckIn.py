from datetime import datetime
from shortuuid import ShortUUID

class CheckIn:
    def __init__(self, deadline:datetime, success:bool,note:str=None,rating:int=None,cost:float=0, cost_accum:float=0, dynamic:bool=False, dynamic_count:int=0) -> None:
        '''Initializes a checkin for a regular or dynamic habit habit. The current deadline, whether the checkin deadline was successfull, optional note and rating can be provided by the user. Cost, cost_accum, dynamic and dynamic_count are provided by the habit itself.'''
        self.checkin_id:str = ShortUUID().random(length=5).lower()
        self.checkin_datetime:datetime = datetime.now()
        self.deadline:datetime = deadline
        self.success:bool = success
        self.note:str = note
        self.rating:int = rating
        self.cost_accum:float = cost_accum + cost
        self.dynamic:bool = dynamic
        self.dynamic_count:int = dynamic_count
    
    def info_checkin(self) -> None:
        '''Used for debugging, prints out the information of the checkin.'''
        print(f'Check-in id:{self.checkin_id}, Check-in Date: {self.checkin_datetime}, Success: {self.success}, Personal Note: {self.note}, Rating: {self.rating}\n\n\n')
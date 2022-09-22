import bcrypt
from datetime import datetime
from shortuuid import ShortUUID

from Classes.Habit import Habit

class User:
    def __init__(self,name:str,password:str,email:str=None) -> None:
        self.user_id:str = ShortUUID().random(length=5).lower()
        self.salt:bytes = bcrypt.gensalt(14)
        self.name:str = name
        self.password:bytes = bcrypt.hashpw(bytes(password,'utf8'),self.salt)
        self.created:datetime = datetime.now()
        self.last_login:datetime = datetime.now()
        self.email:str = email
        self.habits:list = []

    def set_last_login(self) -> None:
        self.last_login = datetime.now()
    
    def reset(self,type:int=0) -> None:
        #reset to default OR clean without example data
        self.created = datetime.now()
        self.last_login = datetime.now()
        self.email = email

        #default reset with example data
        if(type==0):
            self.habits = [] #insert example habits!!
        #clean all habits and don't add example data
        elif(type==1):
            self.habits = [] #insert example habits!!

    def info(self) -> None:
        print(f'id:{self.user_id} \nsalt:{self.salt} \nname:{self.name} \npassword:{self.password} \ncreated:{self.created} \nlast_login:{self.last_login}')
    
    def auth(self,password:bytes) -> bool:
        #validate given password against hashed password
        return bcrypt.checkpw(password, self.password)
    
    def create_habit(
        self,
        title:str,
        description:str,
        interval:str,
        active:bool,
        start_from:datetime,
        difficulity:int,
        category:str,
        moto:str,
        importance:int,
        push_notif:bool,
        milestone:int,
        style:int,
        is_dynamic:bool,
        checkin_num_before_deadline:int
        ) -> None:
        
        #Instantiate a habit and put it in the user habits list
        self.habits.append(Habit(title, description, interval, active, start_from, difficulity, category, moto, importance, push_notif, milestone, style, is_dynamic, checkin_num_before_deadline))
    
    def delete_habit(self,habit_id:str) -> None:
        index=0
        for habit in self.habits:
            if habit.habit_id == habit_id:
                self.habits.pop(index)
            index += 1
        
        #if the habit id has not been found, then give feedback.
        if(index==len(self.habits)):
            print(f'Could not find habit with habit_id: {habit_id}!')


# u = Users()
# u.create('Fabian','Cow123')
# for user in u.users: user.info()
# print(u.users[0].user_id)
# u.delete(u.users[0].user_id)
# #for user in u.users: user.info()


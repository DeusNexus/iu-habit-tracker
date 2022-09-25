import bcrypt
from datetime import datetime
from shortuuid import ShortUUID

from Classes.Habit import Habit

class User:
    def __init__(self,name:str,password:str,email:str=None) -> None:
        '''On init is used when setting up a User and receives a name, password and email (optional). Using a salt the password is hashed and stored in encrypted manner. It creates a habit list for the user where the Habit objects are stored in. '''
        self.user_id:str = ShortUUID().random(length=5).lower()
        self.salt:bytes = bcrypt.gensalt(14)
        self.name:str = name
        self.password:bytes = bcrypt.hashpw(bytes(password,'utf8'),self.salt)
        self.created:datetime = datetime.now()
        self.last_login:datetime = datetime.now()
        self.email:str = email
        self.habits:list = []

    def set_last_login(self) -> None:
        '''Calling the function will update the last_login to the current datetime.'''
        self.last_login = datetime.now()
    
    def reset(self,type:int=0) -> None:
        '''Used to reset the user to initial state and depending on the provided type it will load example habits or leave the habits list empty.'''
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
        '''Used for debugging and prints User data to the terminal.'''
        print(f'id:{self.user_id} \nsalt:{self.salt} \nname:{self.name} \npassword:{self.password} \ncreated:{self.created} \nlast_login:{self.last_login}')
    
    def auth(self,password:bytes) -> bool:
        '''Checks if the provided password in bytes is valid against the hashed stored password in the User.'''
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
        '''Creates a new Habit for the user and appends it to the users's habits list.'''
        #Instantiate a habit and put it in the user habits list
        self.habits.append(Habit(title, description, interval, active, start_from, difficulity, category, moto, importance, push_notif, milestone, style, is_dynamic, checkin_num_before_deadline))
    
    def delete_habit(self,habit_id:str) -> None:
        '''Delete a habit from the user's habits list by providing the habit_id of the habit to be removed.'''
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


import bcrypt
from datetime import datetime
from shortuuid import ShortUUID

from Classes.Habit import Habit
from Load import default_example_data

class User:
    def __init__(self,name:str,password:str,user_id:str=None) -> None:
        '''On init is used when setting up a User and receives a name and password. Using a salt the password is hashed and stored in encrypted manner. It creates a habit list for the user where the Habit objects are stored in. '''
        self.user_id:str = ShortUUID().random(length=5).lower()
        self.salt:bytes = bcrypt.gensalt(14) #Each new user gets a random salt
        self.name:str = name
        self.password:bytes = bcrypt.hashpw(bytes(password,encoding='utf8'),self.salt) if type(password) == str else password #Bcrypt uses bytes for password and hashedpassword arguments
        self.created:datetime = datetime.now()
        self.last_login:datetime = datetime.now()
        self.habits:list = []

    def overwrite(self,
        user_id:str,
        salt:str,
        name:str,
        password:str,
        created:str,
        last_login:str):
        """The function is used in combination with user_id to overwrite values of internal user class when a user already exists in DB."""

        # print("Overwrite password: ",password," Overwrite salt: ",salt)
        self.user_id:str = str(user_id)
        self.salt:bytes = bcrypt.gensalt(14) if type(salt) == str else salt #If salt is empty then generate a new one, else take the salt and store as bytes
        # print("Overwrite password: ",password," Overwrite salt: ",self.salt)
        self.name:str = str(name)
        self.password:bytes = eval(password) if type(password) == str else password #Only hash password if it's not already in bytes format == already hashed!
        # print("Overwrite password: ",password," Overwrite salt: ",self.salt)
        self.created:datetime = created 
        self.last_login:datetime = last_login

    def set_last_login(self) -> None:
        '''Calling the function will update the last_login to the current datetime.'''
        self.last_login = datetime.now()
    
    def reset(self) -> None:
        '''Used to reset the user to initial state and depending on the provided type it will load example habits or leave the habits list empty.'''
        #reset to default OR clean without example data

        self.habits = []

        # #default reset with example data
        # if(type==0):
        #     self.habits = [] #insert example habits!!
        #     (habits, checkins) = default_example_data(self.user_id)
        #     for indx, habit in enumerate(habits):
        #         self.create_habit(
        #             title='',
        #             description='',
        #             interval='1D',
        #             active=True,
        #             start_from='',
        #             difficulity=5,
        #             category='',
        #             moto='',
        #             importance=5,
        #             milestone=31,
        #             style=0,
        #             is_dynamic=False,
        #             checkin_num_before_deadline=1,
        #             habit_id='',
        #             user_id='',
        #             cost=0)
                
        #         print('*habit.values(): ',*habit.values())
        #         self.habits[indx].overwrite(*habit.values())
                
        #         for indx2, checkin in enumerate(checkins):
        #             print('*checkin.values(): ',*checkin.values())
        #             self.habits[indx].checkin('test_note',5)
        #             self.habits[indx].checkins[indx2].overwrite(*checkin.values())
            
        # #clean all habits and don't add example data
        # elif(type==1):
        #     self.habits = []

    def info(self) -> None:
        '''Used for debugging and prints User data to the terminal.'''
        print(f'id:{self.user_id} \nsalt:{self.salt} \nname:{self.name} \npassword:{self.password} \ncreated:{self.created} \nlast_login:{self.last_login}')
    
    def auth(self,password:str) -> bool:
        '''Checks if the provided password in bytes is valid against the hashed stored password in the User.'''
        #validate given password against hashed password
        # print("User/Auth: ",type(password),password,type(self.password),self.password)
        psw = password if type(password) == bytes else bytes(password,encoding='utf8')
        return bcrypt.checkpw(psw, self.password)
    
    def create_habit(
        self,
        title:str,
        description:str,
        interval:str,
        active:bool,
        start_from:str,
        difficulity:int,
        category:str,
        moto:str,
        importance:int,
        milestone:int,
        style:int,
        is_dynamic:bool,
        checkin_num_before_deadline:int,
        habit_id: str,
        user_id: str,
        cost: float
        ) -> None:
        '''Creates a new Habit for the user and appends it to the users's habits list.'''
        #Instantiate a habit and put it in the user habits list
        self.habits.append(Habit(title, description, interval, active, start_from, difficulity, category, moto, importance, milestone, style, is_dynamic, checkin_num_before_deadline, habit_id, user_id, cost))
    
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



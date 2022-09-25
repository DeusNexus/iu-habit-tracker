from Classes.User import User

class Users:
    def __init__(self) -> None:
        '''On init created a empty users list that will contain User objects when the application starts.'''
        self.users:list[User] = []
    
    def create(self,name:str, password:str) -> None:
        '''Create a new user by providing a name and password. It is added to the users list in Users object.'''
        self.users.append(User(name,password))
    
    def reset(self) -> None:
        '''Reset is used to set the users list to an empty list again.'''
        self.users = []
        print('\nDeleting all users!')

    def delete(self,user_id:str) -> None:
        '''Delete is used to remove an individual User from the users list in Users. A user_id is passed to it for which user has to be deleted if it matches.'''
        i = 0
        for user in self.users:
            if user.user_id == user_id:
                self.users.pop(i)
                print('User deleted!')
            i += 1


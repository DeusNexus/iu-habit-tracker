from Classes.User import User

class Users:
    def __init__(self) -> None:
        self.users:list[User] = []
    
    def create(self,name:str, password:str) -> None:
        self.users.append(User(name,password))
    
    def reset(self) -> None:
        self.users = []
        print('\nDeleting all users!')

    def delete(self,user_id:str) -> None:
        i = 0
        for user in self.users:
            if user.user_id == user_id:
                self.users.pop(i)
                print('User deleted!')
            i += 1


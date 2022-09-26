import pytest
import Load
from Classes.Users import Users

def test_load_example_data():
    users = Users()
    assert users.users == [], 'Users was not created with empty list'
    Load.load_example_data(users)
    assert len(users.users ) > 0, 'No example data was inserted into users!'

def test_default_example_data():
    for example_habit in Load.default_example_data():
        #Create Habit takes 14 arguments
        assert len(example_habit) == 14, 'The function did not provide the correct amount of arguments to create habits.'


########### NOT DONE
def test_load_user_data():
    db_users = ''
    Load.load_user_data(db_users)
    assert True
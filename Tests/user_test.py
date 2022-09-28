import pytest
import bcrypt
from Classes.User import User
from Load import default_example_data

#============Fixtures===========
@pytest.fixture
def tCred(): 
    return {
        'name':'TestUser',
        'password':'testpass'
    }

@pytest.fixture
def tUser():
    return User('TestUser','testpass')

@pytest.fixture
def tUserHabits(tUser):
    tUser.create_habit(title='TestHabit', description='TestDescription', interval='1W', active=True, start_from=None, difficulity=5, category='TestCat', moto='TestMoto', importance=5, milestone=10, style=None, is_dynamic=False, checkin_num_before_deadline=0)
    tUser.create_habit(title='TestHabit2', description='TestDescription2', interval='1W', active=True, start_from=None, difficulity=5, category='TestCat2', moto='TestMoto2', importance=5, milestone=10, style=None, is_dynamic=False, checkin_num_before_deadline=0)
    tUser.create_habit(title='TestHabit3', description='TestDescription3', interval='1W', active=True, start_from=None, difficulity=5, category='TestCat3', moto='TestMoto3', importance=5, milestone=10, style=None, is_dynamic=False, checkin_num_before_deadline=0)
    tUser.create_habit(title='TestHabitD1', description='TestDescriptionD1', interval='1W', active=True, start_from=None, difficulity=5, category='TestCatD1', moto='TestMotoD1', importance=5, milestone=10, style=None, is_dynamic=True, checkin_num_before_deadline=3)
    tUser.create_habit(title='TestHabitD2', description='TestDescriptionD2', interval='1W', active=True, start_from=None, difficulity=5, category='TestCatD2', moto='TestMotoD2', importance=5, milestone=10, style=None, is_dynamic=True, checkin_num_before_deadline=3)

@pytest.fixture
def tUserHabitsCheckins(tUser):
    for habit in tUser.habits:
        if not habit.is_dynamic:
            habit.checkin(note='notetest',rating=3)
    for habit in tUser.habits:
        if habit.is_dynamic:
            habit.dynamic_checkin(note='notetest',rating=3)


#=============Tests============
def test_create_user_empty() -> None:
    with pytest.raises(TypeError):
        user = User()

@pytest.fixture
def test_create_user_default(tCred) -> None:
    user = User(tCred.name,tCred.password)
    assert type(user) == User, "Failed to create user of type User!"

def test_set_last_login_updates(tUser):
    last_login  = tUser.last_login
    tUser.set_last_login()
    assert last_login != tUser.last_login, "last_login did not update!"

def test_reset_default(tUser,tUserHabits,tUserHabitsCheckins):
    assert tUser.habits[0].checkins, "There are no checkins to test!"
    assert tUser.habits, "There are no habits to test!"
    created = tUser.created
    last_login = tUser.last_login
    tUser.reset(0)
    #Default should contain the example habits!
    assert len(tUser.habits) == len(default_example_data()) and len(tUser.habits) != 0, "No example habits got inserted after reset!"
    assert tUser.created != created, "Created was not reset to a new datetime"
    assert tUser.last_login != last_login, "Last_login was not reset to a new datetime"

def test_reset_full(tUser,tUserHabits,tUserHabitsCheckins):
    assert tUser.habits[0].checkins, "There are no checkins to test!"
    assert tUser.habits, "There are no habits to test!"
    created = tUser.created
    last_login = tUser.last_login
    tUser.reset(1)
    #Full reset should have no habits
    assert len(tUser.habits) == 0, "Habits did not get assigned an empty list!"
    assert tUser.created != created, "Created was not reset to a new datetime"
    assert tUser.last_login != last_login, "Last_login was not reset to a new datetime"

def test_auth(tUser):
    assert tUser.auth(bytes('testpass',encoding='utf8')), 'Correct password fails to login in auth'
    assert not tUser.auth(bytes('wrongpass',encoding='utf8')), 'Wrong password success to login in auth'

def test_create_habit(tUser):
    #Create 5 regular habits
    for x in range(5):
            tUser.create_habit(title=f'TestHabit{x}', description=f'TestDescription{x}', interval='1W', active=True, start_from=None, difficulity=5, category=f'TestCat{x}', moto=f'TestMoto{x}', importance=5, milestone=10, style=None, is_dynamic=False, checkin_num_before_deadline=0)

    #Check that atleast one habit exists
    assert tUser.habits[0], 'No habits were created!'
    assert len(tUser.habits) == 5, 'Not the same amount of habits were created as create function was called!'
    i = 0
    for habit in tUser.habits:
        assert habit.title == f'TestHabit{i}'
        assert habit.description == f'TestDescription{i}'
        assert habit.category == f'TestCat{i}'
        assert habit.moto == f'TestMoto{i}'
        i += 1

def test_delete_habit(tUser,tUserHabits):
    habit_count_after_create_habit =  len(tUser.habits)
    assert habit_count_after_create_habit != 0, "There are no habits for user created!"
    #Delete first habit in list using the habit_id
    tUser.delete_habit(tUser.habits[0].habit_id)
    assert habit_count_after_create_habit != len(tUser.habits), "No habit got deleted!"
    assert habit_count_after_create_habit - 1 == len(tUser.habits), "More then one habit got deleted!"

def test_info(tUser):
    assert tUser.info() == None, "Nothing should be returned from this debug function, it only prints to the console."
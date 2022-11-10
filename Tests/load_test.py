import pytest
import Load
from Database import db_api as api
from Classes.Users import Users

#Check that we start with empty list and that the database is able to insert users into the state object (here users.users)
def test_load_users():
    users = Users()
    print('test_load_users users.users: ',users.users)
    assert users.users == [], 'Users was not created with empty list'

    #Retrieve persistent data from database IF it exists!
    db_users = api.db_get_users()

    Load.load_users(users)

    print('test_load_users users.users: ',users.users)

    assert len(users.users) > 0, 'No users were loaded!'

    for u in users.users:
        assert(u.user_id,u.salt,u.name,u.password,u.created,u.last_login), 'User does not have the correct required data for a regular init.'

#Check that user that logins has been populated with his/her habits and checkins, e.g. start with empty lists for habit and checkins and afterwards they should be non-empty!
def test_load_user_data():
    users = Users()
    print('test_load_users users.users: ',users.users)
    assert users.users == [], 'Users was not created with empty list'

    #Retrieve persistent data from database IF it exists!
    db_users = api.db_get_users()

    Load.load_users(users)

    print('test_load_users users.users: ',users.users)

    assert len(users.users) > 0, 'No users were loaded!'

    #Data Load test starts here
    for user in users.users:
        Load.load_user_data(users, user.user_id)
    
    print("users.users[0]",users.users[0])
    assert users.users[0].habits
    #Make sure that first user has actual habit to check for!!
    print("users.users[0].habits[0]",users.users[0].habits)
    assert users.users[0].habits[0], 'No habit was found for the user habits, make sure first user in db does have a habit!'
    #Make sure that first user has actual checkins for first habit!!
    print("users.users[0].habits[0].checkins[0]",users.users[0].habits[0].checkins)
    assert users.users[0].habits[0].checkins[0], 'No checkins were found for habit[0], make sure first user in db does have a habit with checkin to check for!'

#Check if the example data is generated correctly with the correct amount of attributes for both habits and checkins (important for database > model > correct python types)
def test_default_example_data():
    (habits, checkins) = Load.default_example_data('test_id_tests')

    for habit in habits:
        #Overwriting habit takes 23 default arguments that will overwrite a initialized habit with the example values.
        print(habit)
        assert len(habit.keys()) == 23, 'The function did not provide the correct amount of arguments to create habits.'

    for checkin in checkins:
        #Overwriting checkin takes 12 default arguments that will overwrite a initialized checkin with the example values.
        print(checkin)
        assert len(checkin.keys()) == 12

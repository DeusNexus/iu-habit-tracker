import pytest
from Classes.Users import Users

@pytest.fixture
def ulist():
    users = Users()
    assert type(users) == Users, 'Could not init Users'
    return users

def test_init(ulist):
    assert len(ulist.users) == 0, 'No empty list found when initializing Users'

def test_create(ulist):
    amnt = 6
    i = 1
    for _ in range(amnt):
        ulist.create(f'test{i}', 'testpass')
        i += 1
    assert len(ulist.users) == amnt
    assert ulist.users[amnt-1].name == f'test{amnt}','The last user in the list does not created the correct corresponding name when calling multiple times.'

def test_reset(ulist):
    amnt = 6
    i = 1
    for _ in range(amnt):
        ulist.create(f'test{i}', 'testpass')
        i += 1
    assert len(ulist.users) == amnt, 'When creating users in Users the amount of users did not correspond to the length of the users list.'
    ulist.reset()
    assert len(ulist.users) == 0, 'Users list was not reset/empty.'

def test_delete(ulist):
    ulist.create('test', 'testpass')
    assert len(ulist.users) == 1, 'No user was created'
    user_id = ulist.users[0].user_id
    assert user_id, 'There is no user_id for the first user'
    ulist.delete(user_id)
    assert len(ulist.users) == 0, 'The user with user_id did not get removed out of the users list!'
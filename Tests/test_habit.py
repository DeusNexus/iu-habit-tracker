import pytest
from Classes.Habit import Habit

@pytest.fixture
def habit():
    habit = Habit('titletest','descriptiontest','1D')
    assert type(habit) == Habit, 'Could not init habit with minimum args!'
    assert habit.is_dynamic == False, 'is_dynamic is not set to False!'
    return habit

@pytest.fixture
def dynamic():
    dynamic = Habit(title='titletest',description='descriptiontest',interval='1D',is_dynamic=True)
    assert type(dynamic) == Habit, 'Could not init habit with minimum args!'
    assert dynamic.is_dynamic, 'is_dynamic is not set to True!'
    return dynamic

def test_init_no_args():
    with pytest.raises(TypeError):
        Habit()

def test_init_correct_args_all():
    habit = Habit('testtitle','testdescription','1D',True,None,5,'testcategory','testmoto',5,False,10,0,False)
    assert type(habit) == Habit, 'No habit was init with correct values'

def test_init_incorrect_args():
    with pytest.raises(ValueError):
        #Test 0D
        Habit('testtitle','testdescription','0D',True,None,5,'testcategory','testmoto',5,False,10,0,False)

def test_update_deadlines(habit):
    prev_deadline = habit.prev_deadline
    next_deadline = habit.next_deadline
    habit.update_deadlines()
    assert prev_deadline != habit.prev_deadline, 'The prev_deadline did not get updated when calling update_deadlines'
    assert next_deadline != habit.next_deadline, 'The next_deadline did not get updated when calling update_deadlines'

def test_incr_streak(habit):
    streak = habit.streak
    habit.incr_streak()
    assert streak + 1 == habit.streak, 'The habit streak did not correctly get incremented by 1'

def test_reset_streak(habit):
    habit.incr_streak()
    assert habit.streak > 0, 'Habit streak did not get incremented in test.'
    habit.reset_streak()
    assert habit.streak == 0, 'The streak did not reset back to 0!'

def test_incr_success(habit):
    success = habit.success
    habit.incr_success()
    assert success + 1 == habit.success, 'The habit success did not correctly get incremented by 1'

def test_incr_fail(habit):
    fail = habit.fail
    habit.incr_fail()
    assert fail + 1 == habit.fail, 'The habit fail did not correctly get incremented by 1'

def test_dynamic_incr(habit):
    dynamic_count = habit.dynamic_count
    habit.dynamic_incr()
    assert dynamic_count + 1 == habit.dynamic_count, 'The habit dynamic_count did not correctly get incremented by 1'

def test_dynamic_reset(habit):
    habit.dynamic_incr()
    assert habit.dynamic_count > 0, 'Habit dynamic_count did not get incremented in test.'
    habit.dynamic_reset()
    assert habit.dynamic_count == 0, 'The dynamic_count did not reset back to 0!'

def test_checkin(habit):
    assert len(habit.checkins) == 0, 'Checkins already present which should not be the case!'
    habit.checkin('note', 5)
    assert len(habit.checkins) == 1, 'Was not able to create a checkin in checkins'
    for _ in range(4):
        habit.checkin('note', 1)
    assert len(habit.checkins) == 5, 'Total amount of habit checkins does not correspond with the amount in the checkins list!'

def test_checkin_invalid_regular(habit):
    with pytest.raises(ValueError):
        habit.dynamic_checkin('note', 5)

def test_checkin_invalid_dynamic(dynamic):
    with pytest.raises(ValueError):
        dynamic.checkin('note', 5)

def test_dynamic_checkin(dynamic):
    assert len(dynamic.checkins) == 0, 'Checkins already present which should not be the case!'
    dynamic.dynamic_checkin('note', 5)
    assert len(dynamic.checkins) == 1, 'Was not able to create a dynamic_checkin in checkins'
    for _ in range(4):
        dynamic.dynamic_checkin('note', 1)
    assert len(dynamic.checkins) == 5, 'Total amount of dynammic_habit checkins does not correspond with the amount in the checkins list!'

def test_info_habit(habit):
    assert not habit.info_habit(), "Info habit should not return anything and is solely used for debugging."

def test_info_checkins(habit):
    for _ in range(5):
        habit.checkin('test',5)
    assert len(habit.checkins) > 0, "No checkins found for habit!"
    assert not habit.info_checkins(), "Checkins should not return anything and is solely used for debugging."
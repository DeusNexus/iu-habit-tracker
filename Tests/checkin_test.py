import pytest
from datetime import datetime
from Classes.CheckIn import CheckIn

def test_checkin_init_with_empty_values():
    checkin = CheckIn(
        user_id='testuserid',
        habit_id='testhabitid',
        checkin_id='testcheckinid',
        deadline=datetime.now(), 
        success=True)
    

    #Print debug info about the newly created checkin in case assert error
    checkin.info_checkin()
    # print('checkin obj: ',checkin, checkin.keys())
    assert type(checkin) == CheckIn, 'Leaving default arguments empty resulted in an error when creating a checkin.'

def test_checkin_init_with_all_values():
    checkin = CheckIn(
        user_id='testuserid',
        habit_id='testhabitid',
        checkin_id='testcheckinid',
        deadline=datetime.now(), 
        success=True, 
        note='Test',
        rating=5,
        cost=13.5, 
        cost_accum=150, 
        dynamic=False, 
        dynamic_count=0)
    assert type(checkin) == CheckIn, 'This is not a valid checkin with all given arguments to init a checkin.'

def test_info_checkin():
    checkin = CheckIn(
        user_id='testuserid',
        habit_id='testhabitid',
        checkin_id='testcheckinid',
        deadline=datetime.now(), 
        success=True)
    assert not checkin.info_checkin(), 'Info_checkin should not return anything, but only print to console for debugging.'
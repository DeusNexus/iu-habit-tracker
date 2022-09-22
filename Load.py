def load_example_data(users):
    #hardcoded example data, could be stored in database aswell
    users.create('John', 'pass')
    users.create('Rick', 'pass1')
    users.create('Tom', 'pass2')
    users.users[0].create_habit(title='Cardio Workout', description='Cardio Activities', interval='3D', active=True, start_from=None, difficulity=1, category='Sport', moto='To become lean and more stamina', importance=5, push_notif=True, milestone=5, style=0, is_dynamic=False, checkin_num_before_deadline=0)
    users.users[0].create_habit(title='Weight Lifting', description='Muscle workout', interval='2D', active=True, start_from=None, difficulity=4, category='Sport', moto='For power in body', importance=5, push_notif=True, milestone=5, style=0, is_dynamic=False, checkin_num_before_deadline=0)
    users.users[0].create_habit(title='Cycling', description='Outdoor Cycling', interval='1W', active=True, start_from=None, difficulity=2, category='Sport', moto='Outdoor sporting for mindfulness', importance=2, push_notif=True, milestone=2, style=0, is_dynamic=True, checkin_num_before_deadline=1)
    users.users[0].create_habit(title='Bow and Arrow', description='Shooting', interval='1D', active=True, start_from=None, difficulity=2, category='Sport', moto='Precision', importance=2, push_notif=True, milestone=2, style=0, is_dynamic=True, checkin_num_before_deadline=1)
    users.users[1].create_habit(title='Movie Night', description='Go out and have fun with family', interval='2W', active=True, start_from=None, difficulity=1, category='Leisure', moto='Everyone relaxes', importance=4, push_notif=True, milestone=4, style=0, is_dynamic=False, checkin_num_before_deadline=0)
    users.users[1].create_habit(title='Hiking', description='Walk in nature', interval='1W', active=True, start_from=None, difficulity=3, category='Sport', moto='Great for health', importance=5, push_notif=True, milestone=2, style=0, is_dynamic=False, checkin_num_before_deadline=0)

    users.users[0].habits[0].checkin('Good first attempt!', 5)
    users.users[0].habits[0].checkin('Good first attempt!', 5)
    users.users[0].habits[0].checkin('Good first attempt!', 5)
    users.users[0].habits[0].checkin('Good first attempt!', 5)
    users.users[0].habits[1].checkin('Good first attempt!', 5)
    users.users[0].habits[1].checkin('Good first attempt!', 5)
    

def load_user_data(users):
    pass
    #users:list = DB
    #for user in users, create a user in active_users
    #for user in active_users insert the corresponding user habits/data
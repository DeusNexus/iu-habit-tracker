import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

# self.checkin_id:str = ShortUUID().random(length=5).lower()
# self.checkin_datetime:datetime = datetime.now()
# self.deadline:datetime = deadline
# self.success:bool = success
# self.note:str = note
# self.rating:int = rating
# self.cost_accum:float = cost_accum + cost
# self.dynamic:bool = dynamic
# self.dynamic_count:int = dynamic_count

checkins = [
    {
        'user_id':'user_id1',
        'habit_id':'habit_id1',
        'checkin_id':'checkin_id1',
        'checkin_datetime':'2022-05-11 05:12:43',
        'deadline':'2022-05-12 05:12:43',
        'success':'True',
        'note':'Great work',
        'rating':4,
        'cost_accum':0,
        'dynamic':'False',
        'dynamic_count':0
    },
    {
        'user_id':'user_id1',
        'habit_id':'habit_id1',
        'checkin_id':'checkin_id2',
        'checkin_datetime':'2022-05-11 05:12:43',
        'deadline':'2022-05-13 05:12:43',
        'success':'True',
        'note':'Wow',
        'rating':5,
        'cost_accum':0,
        'dynamic':'False',
        'dynamic_count':0
    },
    {
        'user_id':'user_id1',
        'habit_id':'habit_id1',
        'checkin_id':'checkin_id3',
        'checkin_datetime':'2022-05-13 05:12:43',
        'deadline':'2022-05-14 05:12:43',
        'success':'True',
        'note':'Amazing',
        'rating':4,
        'cost_accum':0,
        'dynamic':'False',
        'dynamic_count':0
    },
]

#habit examples
def insert_checkin(checkin):
    c.execute("""INSERT INTO checkins VALUES (:user_id,:habit_id,:checkin_id,:checkin_datetime,:deadline,:success,:note,:rating,:cost_accum,:dynamic,:dynamic_count)""",checkin)

for checkin in checkins:
    insert_checkin(checkin)

c.execute("""SELECT * FROM checkins""")
print(c.fetchall())

conn.commit()
conn.close()

import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

# self.title:str = title
# self.description:str = description
# self.interval:str = interval
# self.active:bool = active
# self.start_from:datetime = start_from
# self.difficulity:int = difficulity
# self.category:str = category
# self.moto:str = moto
# self.importance:int = importance
# self.push_notif:bool = push_notif
# self.style:int = style
# self.milestone_streak:int = milestone
# self.is_dynamic:bool = is_dynamic
# self.checkin_num_before_deadline:int = checkin_num_before_deadline
# self.dynamic_count:int = 0
# self.habit_id:str = ShortUUID().random(length=5).lower()
# self.created_on:datetime = date
# self.prev_deadline: datetime = date
# self.next_deadline: datetime = add_streak_to_deadline(self.prev_deadline, interval_to_seconds(self.interval))
# self.streak:int = 0
# self.success:int = 0
# self.fail:int = 0
# self.cost:float = 0
# self.cost_accum:float = 0
# self.checkins:list[CheckIn] = []

habits = [
    {
        'user_id':'userid_1',
        'habit_id':'habit_id1',
        'title':'title_reading',
        'description':'description_good for my mind',
        'interval':'1D',
        'active':'True',
        'start_from':'None',
        'difficulity':5,
        'category':'Eduction',
        'moto':'The more you learn the better',
        'importance':5,
        'push_notif':'False',
        'style':1,
        'milestone_streak':30,
        'is_dynamic':'False',
        'checkin_num_before_deadline':0,
        'dynamic_count':0,
        'created_on':'2022-05-11 05:12:43',
        'prev_deadline':'2022-05-11 05:12:43',
        'next_deadline':'2022-05-12 05:12:43',
        'streak':0,
        'success':0,
        'fail':0,
        'cost':0,
        'cost_accum':0
    },
    {
        'user_id':'userid_1',
        'habit_id':'habit_id2',
        'title':'title_laughing',
        'description':'Why not?',
        'interval':'1D',
        'active':'True',
        'start_from':'None',
        'difficulity':1,
        'category':'Mental Health',
        'moto':'More joy is better',
        'importance':5,
        'push_notif':'False',
        'style':1,
        'milestone_streak':365,
        'is_dynamic':'False',
        'checkin_num_before_deadline':0,
        'dynamic_count':0,
        'created_on':'2022-05-13 05:12:43',
        'prev_deadline':'2022-05-14 05:12:43',
        'next_deadline':'2022-05-15 05:12:43',
        'streak':1,
        'success':1,
        'fail':0,
        'cost':0,
        'cost_accum':0
    },
    {
        'user_id':'userid_1',
        'habit_id':'habit_id3',
        'title':'title_cinema',
        'description':'Movie night',
        'interval':'1W',
        'active':'True',
        'start_from':'None',
        'difficulity':1,
        'category':'Entertainment',
        'moto':'To get inspired',
        'importance':2,
        'push_notif':'False',
        'style':1,
        'milestone_streak':4,
        'is_dynamic':'False',
        'checkin_num_before_deadline':0,
        'dynamic_count':0,
        'created_on':'2022-06-13 05:12:43',
        'prev_deadline':'2022-06-13 05:12:43',
        'next_deadline':'2022-06-20 05:12:43',
        'streak':0,
        'success':1,
        'fail':0,
        'cost':4.95,
        'cost_accum':0
    },

]

#habit examples
def insert_habit(habit):
    c.execute("""INSERT INTO habits VALUES (:user_id,:habit_id,:title,
    :description,:interval,:active,:start_from,:difficulity,:category,:moto,:importance,:push_notif,
    :style,:milestone_streak,:is_dynamic,:checkin_num_before_deadline,:dynamic_count,:created_on,:prev_deadline,
    :next_deadline,:streak,:success,:fail,:cost,:cost_accum)""", habit)

for h in habits:
    insert_habit(h)

c.execute("""SELECT * FROM habits""")
print(c.fetchall())

conn.commit()
conn.close()
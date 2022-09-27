import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

c.execute("""CREATE TABLE users (
            user_id text,
            salt text,
            name text,
            password text,
            created text,
            last_login text,
            email text
)""")

c.execute("""CREATE TABLE habits (
            user_id text,
            habit_id text,
            title text,
            description text,
            interval text,
            active text,
            start_from text,
            difficulity integer,
            category text,
            moto text,
            importance integer,
            push_notif text,
            style integer,
            milestone integer,
            is_dynamic text,
            checkin_num_before_deadline integer,
            dynamic_count integer,
            created_on text,
            prev_deadline text,
            next_deadline text,
            streak integer,
            success integer,
            fail integer,
            cost real,
            cost_accum real
)""")

c.execute("""CREATE TABLE checkins (
            user_id text,
            habit_id text,
            checkin_id text,
            checkin_datetime text,
            deadline text,
            success text,
            note text,
            rating integer,
            cost_accum real,
            dynamic text,
            dynamic_count integer
)""")

conn.commit()

conn.close()

# self.checkin_id:str = ShortUUID().random(length=5).lower()
# self.checkin_datetime:datetime = datetime.now()
# self.deadline:datetime = deadline
# self.success:bool = success
# self.note:str = note
# self.rating:int = rating
# self.cost_accum:float = cost_accum + cost
# self.dynamic:bool = dynamic
# self.dynamic_count:int = dynamic_count

# #user-defined
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
# #dynamic checkin counter
# self.dynamic_count:int = 0
# #Datetime now for all initial variables
# date = datetime.now()
# self.habit_id:str = ShortUUID().random(length=5).lower()
# self.created_on:datetime = date
# self.prev_deadline: datetime = date
# self.next_deadline: datetime = add_streak_to_deadline(self.prev_deadline, interval_to_seconds(self.interval))
# #initialize counters
# self.streak:int = 0
# self.success:int = 0
# self.fail:int = 0
# self.cost:float = 0
# self.cost_accum:float = 0
# #checkin list - childeren of habit
# self.checkins:list[CheckIn] = []

# self.user_id:str = ShortUUID().random(length=5).lower()
# self.salt:bytes = bcrypt.gensalt(14)
# self.name:str = name
# self.password:bytes = bcrypt.hashpw(bytes(password,'utf8'),self.salt)
# self.created:datetime = datetime.now()
# self.last_login:datetime = datetime.now()
# self.email:str = email
# self.habits:list = []
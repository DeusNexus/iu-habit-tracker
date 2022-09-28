import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

# self.user_id:str = ShortUUID().random(length=5).lower()
# self.salt:bytes = bcrypt.gensalt(14)
# self.name:str = name
# self.password:bytes = bcrypt.hashpw(bytes(password,'utf8'),self.salt)
# self.created:datetime = datetime.now()
# self.last_login:datetime = datetime.now()
# self.email:str = email
# self.habits:list = [] -- NOT A users table attribute

users = [{
            'userid':'userid_1',
            'salt':'salt24662',
            'name':'Jim',
            'password':'pass1',
            'created':'2022-06-27 06:59:59',
            'last_login':'2022-09-28 14:29:00',
            'email':'jim@test.com'
        },
        {
            'userid':'userid_2',
            'salt':'salt2435',
            'name':'Rick',
            'password':'pass2',
            'created':'2022-03-27 10:10:34',
            'last_login':'2022-10-4 15:32:03',
            'email':'rick@test.com'
        },
        {
            'userid':'userid_3',
            'salt':'salt5435',
            'name':'Tom',
            'password':'pass3',
            'created':'2022-02-11 05:12:43',
            'last_login':'2022-05-15 19:54:15',
            'email':'tom@test.com'
        },
        ]

def insert_user(user):
    c.execute("""INSERT INTO users VALUES (:userid,:salt,:name ,:password,:created,:last_login,:email)""", user)

#user examples
for u in users:
    insert_user(u)

c.execute("""SELECT * FROM users""")
print(c.fetchall())

conn.commit()
conn.close()
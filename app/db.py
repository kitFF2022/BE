import pymysql
from app.models.user import User


class DB(object):

    conn = None
    cur = None
    sql = ""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
            print("\033[32m" + "DB  " + "\033[0m", end=':     ')
            print("DB singleton object created.")
        else:
            print("\033[33m" + "DB  " + "\033[0m", end=':     ')
            print("DB singleton object Recycle\n")
        return cls._instance

    def __init__(self):
        DB.conn = pymysql.connect(host='localhost', user='FarmFactory',
                                  password='Nekarakube!1', db='FFDB', charset='utf8mb4')
        DB.cur = DB.conn.cursor()
        DB.sql = "CREATE TABLE IF NOT EXISTS User(id int NOT NULL AUTO_INCREMENT, Name char(30), Team char(30), Nickname char(30), Emailaddr char(30), Password char(30), ProfilePic char(125), PRIMARY KEY (id), UNIQUE(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        DB.sql = "CREATE TABLE IF NOT EXISTS Team(id int NOT NULL AUTO_INCREMENT, Name char(30), Owner int, ProfilePic char(255), PRIMARY KEY (id), UNIQUE(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        DB.sql = "CREATE TABLE IF NOT EXISTS Project(id int NOT NULL AUTO_INCREMENT, Name char(30), Owner int, Data char(255), ProfilePic char(255), PRIMARY KEY (id), UNIQUE(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        DB.sql = "CREATE TABLE IF NOT EXISTS Object(id int NOT NULL AUTO_INCREMENT, Name char(30), Owner int, Data char(255), ProfilePic char(255), PRIMARY KEY (id), UNIQUE(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        print("\033[32m" + "DB  " + "\033[0m", end=':     ')
        print("DB Table initiation complete.")

    def __del__(self):
        DB.conn.close()

    def WarnTestDelAllTableData(self):
        DB.sql = "DROP TABLE User"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        DB.sql = "DROP TABLE Team"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        DB.sql = "DROP TABLE Project"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        DB.sql = "DROP TABLE Object"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        DB.sql = "CREATE TABLE IF NOT EXISTS User(id int NOT NULL AUTO_INCREMENT, Name char(30), Team char(30), Nickname char(30), Emailaddr char(30), Password char(30), ProfilePic char(125), PRIMARY KEY (id), UNIQUE(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        DB.sql = "CREATE TABLE IF NOT EXISTS Team(id int NOT NULL AUTO_INCREMENT, Name char(30), Owner int, ProfilePic char(255), PRIMARY KEY (id), UNIQUE(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        DB.sql = "CREATE TABLE IF NOT EXISTS Project(id int NOT NULL AUTO_INCREMENT, Name char(30), Owner int, Data char(255), ProfilePic char(255), PRIMARY KEY (id), UNIQUE(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        DB.sql = "CREATE TABLE IF NOT EXISTS Object(id int NOT NULL AUTO_INCREMENT, Name char(30), Owner int, Data char(255), ProfilePic char(255), PRIMARY KEY (id), UNIQUE(id))"
        DB.cur.execute(DB.sql)
        DB.conn.commit()
        print("\033[33m" + "DB  " + "\033[0m", end=':     ')
        print("All tables DROPED and CREATED")


"""
    def addUser(self, user: User):
        DB.sql = "INSERT INTO User(Name, Nickname, Emailaddr, Password) VALUES("

"""

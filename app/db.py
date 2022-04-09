from types import NoneType
import pymysql
from app.models.user import User


class DB(object):

    _conn = None
    _cur = None
    _sql = ""
    _err = False

    def DBOK(self):
        return DB.err

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
        print("\033[32m" + "DB  " + "\033[0m", end=':     ')
        print("DB initiation started")
        DB._connectDB(self)
        if not DB._err:
            DB._createTable(self)
            print("\033[32m" + "DB  " + "\033[0m", end=':     ')
            print("DB connection confirmed")

    def __del__(self):
        if DB._conn != None:
            DB._conn.close()

    def _createTable(self):
        if not DB._err:
            DB._sql = "CREATE TABLE IF NOT EXISTS User(id int NOT NULL AUTO_INCREMENT, Name char(30), Team char(30), Nickname char(30), Emailaddr char(30), Password char(30), ProfilePic char(125), PRIMARY KEY (id), UNIQUE(id))"
            DB._cur.execute(DB._sql)
            DB._conn.commit()
            DB._sql = "CREATE TABLE IF NOT EXISTS Team(id int NOT NULL AUTO_INCREMENT, Name char(30), Owner int, ProfilePic char(255), PRIMARY KEY (id), UNIQUE(id))"
            DB._cur.execute(DB._sql)
            DB._conn.commit()
            DB._sql = "CREATE TABLE IF NOT EXISTS Project(id int NOT NULL AUTO_INCREMENT, Name char(30), Owner int, Data char(255), ProfilePic char(255), PRIMARY KEY (id), UNIQUE(id))"
            DB._cur.execute(DB._sql)
            DB._conn.commit()
            DB._sql = "CREATE TABLE IF NOT EXISTS Object(id int NOT NULL AUTO_INCREMENT, Name char(30), Owner int, Data char(255), ProfilePic char(255), PRIMARY KEY (id), UNIQUE(id))"
            DB._cur.execute(DB._sql)
            DB._conn.commit()
            DB._conn.close()

    def _dropTable(self):
        if not DB._err:
            DB._sql = "DROP TABLE User"
            DB._cur.execute(DB._sql)
            DB._conn.commit()
            DB._sql = "DROP TABLE Team"
            DB._cur.execute(DB._sql)
            DB._conn.commit()
            DB._sql = "DROP TABLE Project"
            DB._cur.execute(DB._sql)
            DB._conn.commit()
            DB._sql = "DROP TABLE Object"
            DB._cur.execute(DB._sql)
            DB._conn.commit()
            DB._conn.close()

    def _connectDB(self):
        try:
            DB._conn = pymysql.connect(
                host='localhost', user='FarmFactory', password='Nekarakube!1', db='FFDB', charset='utf8mb4')
        except pymysql.err.OperationalError:
            DB.err = True
            print("\033[31m" + "DB  " + "\033[0m", end=':     ')
            print("DB CONNECTION FAILED !!!")
        else:
            DB.err = False
            DB._cur = DB._conn.cursor()

    def WarnTestDelAllTableData(self):
        DB._connectDB(self)
        DB._dropTable(self)
        DB._connectDB(self)
        DB._createTable(self)
        print("\033[33m" + "DB  " + "\033[0m", end=':     ')
        print("All tables DROPED and CREATED")

    def addUser(self, user: User):
        if not DB.err:
            DB._sql = "INSERT INTO User(Name, Nickname, Emailaddr, Password) VALUES('" + user.Name + \
                "', " + user.Nickname + "', " + user.Emailaddr + "', " + user.Password + "')"
            DB._cur.execute(DB._sql)
            DB._conn.commit()
            return True
        else:
            return False

    def getUser(self, user: User):
        if not DB.err:
            DB._sql = "SELECT * FROM userTable WHERE Emailaddr='" + user.Emailaddr + "'"
            DB._cur.execute(DB._sql)
            row = DB._cur.fetchone()
            return True, row
        else:
            return False, None

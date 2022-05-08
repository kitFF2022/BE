import pymysql
from app.models.user import User, UserSignIn, UserUpdate


class DB:
    _conn = None
    _cur = None
    _sql = ""

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
        if DB._connectDB(self):
            DB._createTable(self)
            print("\033[32m" + "DB  " + "\033[0m", end=':     ')
            print("DB connection confirmed")

    def __del__(self):
        if DB._conn.open:
            DB._conn.close()

    def _createTable(self):
        DB._sql = "CREATE TABLE IF NOT EXISTS User(id int NOT NULL AUTO_INCREMENT UNIQUE, Name char(30), Team char(30), Nickname char(30), Emailaddr char(30) UNIQUE, Password char(30), ProfilePic char(125), PRIMARY KEY (id))"
        DB._cur.execute(DB._sql)
        DB._conn.commit()
        DB._sql = "CREATE TABLE IF NOT EXISTS Team(id int NOT NULL AUTO_INCREMENT UNIQUE, Name char(30), Owner int, ProfilePic char(255), PRIMARY KEY (id))"
        DB._cur.execute(DB._sql)
        DB._conn.commit()
        DB._sql = "CREATE TABLE IF NOT EXISTS Project(id int NOT NULL AUTO_INCREMENT UNIQUE, Name char(30), Owner int, Data char(255), ProfilePic char(255), PRIMARY KEY (id))"
        DB._cur.execute(DB._sql)
        DB._conn.commit()
        DB._sql = "CREATE TABLE IF NOT EXISTS Object(id int NOT NULL AUTO_INCREMENT UNIQUE, Name char(30), Owner int, Data char(255), ProfilePic char(255), PRIMARY KEY (id))"
        DB._cur.execute(DB._sql)
        DB._conn.commit()
        DB._conn.close()
        print("\033[33m" + "DB  " + "\033[0m", end=':     ')
        print("All tables CREATED")

    def _dropTable(self):
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
        print("\033[33m" + "DB  " + "\033[0m", end=':     ')
        print("All tables DROPED")

    def _connectDB(self):
        try:
            DB._conn = pymysql.connect(
                host='172.17.0.4', user='FarmFactory', password='Yuzuha2090!', db='FFDB', charset='utf8mb4')
        except pymysql.err.OperationalError:
            print("\033[31m" + "DB  " + "\033[0m", end=':     ')
            print("DB CONNECTION FAILED !!!")
            return False
        else:
            print("\033[33m" + "DB  " + "\033[0m", end=':     ')
            print("DB CONNECTED !!!")
            DB._cur = DB._conn.cursor()
            return True

    def WarnTestDelAllTableData(self):
        i = 0
        if DB._connectDB(self):
            i = i + 1
            DB._dropTable(self)
        if DB._connectDB(self):
            i = i + 1
            DB._createTable(self)
        if i == 2:
            return True
        else:
            return False

    def _addUser(self, user: User):
        if DB._conn.open:
            try:
                DB._sql = "INSERT INTO User(Name, Nickname, Emailaddr, Password) VALUES('" + user.Name + \
                    "', '" + user.Nickname + "', '" + user.Emailaddr + "', '" + user.Password + "')"
                DB._cur.execute(DB._sql)
                DB._conn.commit()
                DB._conn.close()
            except pymysql.err.IntegrityError:
                return False
            else:
                return True
        else:
            return False

    def _updateUser(self, user: UserUpdate, Emailaddr: str):
        if DB._conn.open:
            try:
                sqlstr = "UPDATE User SET"
                if user.Name is not None:
                    sqlstr = sqlstr + " Name = '"  + user.Name + "',"
                if user.Team is not None:
                    sqlstr = sqlstr + " Team = '"  + user.Team + "',"
                if user.Nickname is not None:
                    sqlstr = sqlstr + " Nickname = '"  + user.Nickname + "',"
                if user.Password is not None:
                    sqlstr = sqlstr + " Password = '"  + user.Password + "',"
                if sqlstr[-1] == ',':
                    sqlstr = sqlstr[:-1]
                sqlstr = sqlstr + " WHERE Emailaddr = '" + Emailaddr + "'"
                DB._sql = sqlstr
                DB._cur.execute(DB._sql)
                DB._conn.commit()
                DB._conn.close()
            except pymysql.err.IntegrityError:
                return False
            else:
                return True
        else:
            return False

    def _updateUserProfilePic(self, filename: str, Emailaddr: str):
        if DB._conn.open:
            try:
                DB._sql = "UPDATE User SET ProfilePic = '" + filename + "' WHERE Emailaddr = '" + Emailaddr + "'"
                DB._cur.execute(DB._sql)
                DB._conn.commit()
                DB._conn.close()
            except pymysql.err.IntegrityError:
                return False
            else:
                return True
        else:
            return False
    def _getUser(self, user: UserSignIn):
        if DB._conn.open:
            DB._sql = "SELECT * FROM User WHERE Emailaddr='" + user.Emailaddr + "'"
            DB._cur.execute(DB._sql)
            row = DB._cur.fetchone()
            DB._conn.close()
            return True, row
        else:
            return False, None

    def _getUserByEmail(self, user: str):
        if DB._conn.open:
            DB._sql = "SELECT * FROM User WHERE Emailaddr='" + user + "'"
            DB._cur.execute(DB._sql)
            row = DB._cur.fetchone()
            DB._conn.close()
            return True, row
        else:
            return False, None

    def getUserData(self, user: str):
        if DB._connectDB(self):
            dbUser = DB._getUserByEmail(self, user)
            if dbUser[0]:
                if dbUser[1] == None:
                    return None
                else:
                    ProfilePic = True
                    if dbUser[1][6] == None:
                        ProfilePic = False
                    dbUser = {
                        "Name": dbUser[1][1],
                        "Team": dbUser[1][2],
                        "Nickname": dbUser[1][3],
                        "Emailaddr": dbUser[1][4],
                        "ProfilePic": str(ProfilePic),
                    }
                    return dbUser

    def getDBUserData(self, user: str):
        if DB._connectDB(self):
            dbUser = DB._getUserByEmail(self, user)
            if dbUser[0]:
                if dbUser[1] == None:
                    return None
                else:
                    dbUser = {
                        "Name": dbUser[1][1],
                        "Team": dbUser[1][2],
                        "Nickname": dbUser[1][3],
                        "Emailaddr": dbUser[1][4],
                        "ProfilePic": dbUser[1][6],
                    }
                    return dbUser

    def signinUser(self, user: UserSignIn):
        if DB._connectDB(self):
            dbUser = DB._getUser(self, user)
            if dbUser[0]:
                if dbUser[1] == None:
                    return 2
                else:
                    if dbUser[1][5] == user.Password:
                        return 1
                    else:
                        return 2
            else:
                return 3
        else:
            return 4

    def signupUser(self, user: User):
        if DB._connectDB(self):
            if self._addUser(user):
                return 1
            else:
                return 2
        else:
            return 3

    def updateUser(self, user: UserUpdate, Emailaddr: str):
        if DB._connectDB(self):
            if self._updateUser(user, Emailaddr):
                return 1
            else:
                return 2
        else:
            return 3

    def updateUserProfilePic(self, Filename: str, Emailaddr: str ):
        if DB._connectDB(self):
            if self._updateUserProfilePic(Filename, Emailaddr):
                return 1
            else:
                return 2
        else:
            return 3

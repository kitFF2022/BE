from pydantic import EmailStr
import pymysql
from app.models.user import User, UserSignIn, UserUpdate
from app.models.team import Team


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
        if self._connectDB():
            self._createTable()
            print("\033[32m" + "DB  " + "\033[0m", end=':     ')
            print("DB connection confirmed")

    def __del__(self):
        if self._conn.open:
            self._conn.close()

    def _createTable(self):
        self._sql = "CREATE TABLE IF NOT EXISTS User(id int NOT NULL AUTO_INCREMENT UNIQUE, Name char(30), Team char(30), Nickname char(30), Emailaddr char(30) UNIQUE, Password char(30), ProfilePic char(125), PRIMARY KEY (id))"
        self._cur.execute(self._sql)
        self._conn.commit()
        self._sql = "CREATE TABLE IF NOT EXISTS Team(id int NOT NULL AUTO_INCREMENT UNIQUE, Name char(30), Owner int, ProfilePic char(255), PRIMARY KEY (id), FOREIGN KEY (Owner) REFERENCES User(id))"
        self._cur.execute(self._sql)
        self._conn.commit()
        self._sql = "CREATE TABLE IF NOT EXISTS Project(id int NOT NULL AUTO_INCREMENT UNIQUE, Name char(30), Owner int, Data char(255), ProfilePic char(255), PRIMARY KEY (id))"
        self._cur.execute(self._sql)
        self._conn.commit()
        self._sql = "CREATE TABLE IF NOT EXISTS Object(id int NOT NULL AUTO_INCREMENT UNIQUE, Name char(30), Owner int, Data char(255), ProfilePic char(255), PRIMARY KEY (id))"
        self._cur.execute(self._sql)
        self._conn.commit()
        self._conn.close()
        print("\033[33m" + "DB  " + "\033[0m", end=':     ')
        print("All tables CREATED")

    def _dropTable(self):
        self._sql = "DROP TABLE Object"
        self._cur.execute(self._sql)
        self._conn.commit()
        self._sql = "DROP TABLE Project"
        self._cur.execute(self._sql)
        self._conn.commit()
        self._sql = "DROP TABLE Team"
        self._cur.execute(self._sql)
        self._conn.commit()
        self._sql = "DROP TABLE User"
        self._cur.execute(self._sql)
        self._conn.commit()
        self._conn.close()
        print("\033[33m" + "DB  " + "\033[0m", end=':     ')
        print("All tables DROPED")

    def _connectDB(self):
        try:
            self._conn = pymysql.connect(
                host='172.17.0.3', user='FarmFactory', password='Yuzuha2090!', db='FFDB', charset='utf8mb4')
        except pymysql.err.OperationalError:
            print("\033[31m" + "DB  " + "\033[0m", end=':     ')
            print("DB CONNECTION FAILED !!!")
            return False
        else:
            print("\033[33m" + "DB  " + "\033[0m", end=':     ')
            print("DB CONNECTED !!!")
            self._cur = self._conn.cursor()
            return True

    def WarnTestDelAllTableData(self):
        i = 0
        if self._connectDB():
            i = i + 1
            self._dropTable()
        if self._connectDB():
            i = i + 1
            self._createTable()
        if i == 2:
            return True
        else:
            return False

    def _addUser(self, user: User):
        if self._conn.open:
            try:
                self._sql = "INSERT INTO User(Name, Nickname, Emailaddr, Password) VALUES('" + user.Name + \
                    "', '" + user.Nickname + "', '" + user.Emailaddr + "', '" + user.Password + "')"
                self._cur.execute(self._sql)
                self._conn.commit()
                self._conn.close()
            except pymysql.err.IntegrityError:
                return False
            else:
                return True
        else:
            return False

    def _updateUser(self, user: UserUpdate, Emailaddr: str):
        if self._conn.open:
            try:
                sqlstr = "UPDATE User SET"
                if user.Name is not None:
                    sqlstr = sqlstr + " Name = '" + user.Name + "',"
                if user.Team is not None:
                    sqlstr = sqlstr + " Team = '" + user.Team + "',"
                if user.Nickname is not None:
                    sqlstr = sqlstr + " Nickname = '" + user.Nickname + "',"
                if user.Password is not None:
                    sqlstr = sqlstr + " Password = '" + user.Password + "',"
                if sqlstr[-1] == ',':
                    sqlstr = sqlstr[:-1]
                sqlstr = sqlstr + " WHERE Emailaddr = '" + Emailaddr + "'"
                self._sql = sqlstr
                self._cur.execute(self._sql)
                self._conn.commit()
                self._conn.close()
            except pymysql.err.IntegrityError:
                return False
            else:
                return True
        else:
            return False

    def _updateUserProfilePic(self, filename: str, Emailaddr: str):
        if self._conn.open:
            try:
                self._sql = "UPDATE User SET ProfilePic = '" + \
                    filename + "' WHERE Emailaddr = '" + Emailaddr + "'"
                self._cur.execute(self._sql)
                self._conn.commit()
                self._conn.close()
            except pymysql.err.IntegrityError:
                return False
            else:
                return True
        else:
            return False

    def _removeUserProfilePic(self, Emailaddr: str):
        if self._conn.open:
            try:
                self._sql = "UPDATE User SET ProfilePic = NULL WHERE Emailaddr = '" + Emailaddr + "'"
                self._cur.execute(self._sql)
                self._conn.commit()
                self._conn.close()
            except pymysql.err.IntegrityError:
                return False
            else:
                return True
        else:
            return False

    def _getUser(self, user: UserSignIn):
        if self._conn.open:
            self._sql = "SELECT * FROM User WHERE Emailaddr='" + user.Emailaddr + "'"
            self._cur.execute(self._sql)
            row = self._cur.fetchone()
            self._conn.close()
            return True, row
        else:
            return False, None

    def _getUserByEmail(self, user: str):
        if self._conn.open:
            self._sql = "SELECT * FROM User WHERE Emailaddr='" + user + "'"
            self._cur.execute(self._sql)
            row = self._cur.fetchone()
            self._conn.close()
            return True, row
        else:
            return False, None

    def _getUserById(self, userId: int):
        if self._conn.open:
            self._sql = "SELECT * FROM User WHERE id=" + str(userId)
            self._cur.execute(self._sql)
            row = self._cur.fetchone()
            self._conn.close()
            return True, row
        else:
            return False, None

    def _createTeam(self, team: Team):
        if self._conn.open:
            self._sql = "INSERT INTO Team(Name, Owner) VALUES('" + \
                team.Name + "', " + str(team.Owner) + ")"
            self._cur.execute(self._sql)
            self._conn.commit()
            self._conn.close()
            return True
        else:
            return False

    def _getTeambyId(self, teamId: int):
        if self._conn.open:
            self._sql = "SELECT * FROM Team WHERE id='" + str(teamId) + "'"
            self._cur.execute(self._sql)
            row = self._cur.fetchone()
            self._conn.close()
            return row
        else:
            return None

    def _getTeambyOwnerId(self, ownerId: int):
        if self._conn.open:
            self._sql = "SELECT * FROM Team WHERE Owner='" + str(ownerId) + "'"
            self._cur.execute(self._sql)
            row = self._cur.fetchone()
            self._conn.close()
            return row
        else:
            return None

    def _updateUserTeam(self, userId: int, teamId: int):
        if self._conn.open:
            self._sql = "UPDATE User SET Team = " + \
                str(teamId) + " WHERE id = " + str(userId)
            self._cur.execute(self._sql)
            self._conn.commit()
            self._conn.close()
            return True
        else:
            return False

    def _updateUserTeamNone(self, userId: int):
        if self._conn.open:
            self._sql = "UPDATE User SET Team = NULL WHERE id = " + str(userId)
            self._cur.execute(self._sql)
            self._conn.commit()
            self._conn.close()
            return True
        else:
            return False

    def _deleteUser(self, user: EmailStr):
        if self._conn.open:
            self._sql = "DELETE FROM User WHERE Emailaddr = '" + user + "'"
            self._cur.execute(self._sql)
            self._conn.commit()
            self._conn.close()
            return True
        else:
            return False

    def _updateTeam(self, team: Team, teamId: int):
        if self._conn.open:
            self._sql = "UPDATE Team SET Name = '" + \
                team.Name + "' WHERE id = " + str(teamId)
            self._cur.execute(self._sql)
            self._conn.commit()
            self._conn.close()
            return True
        else:
            return False

    def _deleteTeam(self, teamId: int):
        if self._conn.open:
            self._sql = "DELETE FROM Team WHERE id = " + str(teamId)
            self._cur.execute(self._sql)
            self._conn.commit()
            self._conn.close()
            return True
        else:
            return False

    def _updateTeamProfilePic(self, filename: str, teamId: int):
        if self._conn.open:
            if filename is None:
                self._sql = "UPDATE Team SET ProfilePic = NULL WHERE id = " + \
                    str(teamId)
                self._cur.execute(self._sql)
                self._conn.commit()
                self._conn.close()
                return True
            else:
                self._sql = "UPDATE Team SET ProfilePic = '" + \
                    filename + "' WHERE id = " + str(teamId)
                self._cur.execute(self._sql)
                self._conn.commit()
                self._conn.close()
                return True
        else:
            return False

    def getUserData(self, user: str):
        if self._connectDB():
            dbUser = self._getUserByEmail(user)
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
        if self._connectDB():
            dbUser = self._getUserByEmail(user)
            if dbUser[0]:
                if dbUser[1] == None:
                    return None
                else:
                    dbUser = {
                        "id": dbUser[1][0],
                        "Name": dbUser[1][1],
                        "Team": dbUser[1][2],
                        "Nickname": dbUser[1][3],
                        "Emailaddr": dbUser[1][4],
                        "ProfilePic": dbUser[1][6],
                    }
                    return dbUser

    def getDBUserDatabyId(self, user: int):
        if self._connectDB():
            dbUser = self._getUserById(user)
            if dbUser[0]:
                if dbUser[1] == None:
                    return None
                else:
                    dbUser = {
                        "id": dbUser[1][0],
                        "Name": dbUser[1][1],
                        "Team": dbUser[1][2],
                        "Nickname": dbUser[1][3],
                        "Emailaddr": dbUser[1][4],
                        "ProfilePic": dbUser[1][6],
                    }
                    return dbUser

    def signinUser(self, user: UserSignIn):
        if self._connectDB():
            dbUser = self._getUser(user)
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

    def deleteUser(self, user: EmailStr):
        if self. _connectDB():
            return self._deleteUser(user)

    def signupUser(self, user: User):
        if self._connectDB():
            if self._addUser(user):
                return 1
            else:
                return 2
        else:
            return 3

    def updateUser(self, user: UserUpdate, Emailaddr: str):
        if self._connectDB():
            if self._updateUser(user, Emailaddr):
                return 1
            else:
                return 2
        else:
            return 3

    def updateUserProfilePic(self, Filename: str, Emailaddr: str):
        if self._connectDB():
            if Filename == "NULL":
                if self._removeUserProfilePic(Emailaddr):
                    return 1
                else:
                    return 2
            else:
                if self._updateUserProfilePic(Filename, Emailaddr):
                    return 1
                else:
                    return 2
        else:
            return 3

    def createTeam(self, team: Team):
        if self._connectDB():
            return self._createTeam(team)
        else:
            return False

    def updateUserTeam(self, userId: int, teamId: int):
        if self._connectDB():
            return self._updateUserTeam(userId, teamId)
        else:
            return False

    def getTeambyOwnerId(self, ownerId):
        if self._connectDB():
            team = self._getTeambyOwnerId(ownerId)
            team = {
                "id": team[0],
                "Name": team[1],
                "Owner": team[2],
                "ProfilePic": team[3]
            }
            return team
        else:
            return None

    def getTeambyId(self, teamId: int):
        if self._connectDB():
            team = self._getTeambyId(teamId)
            if team is not None:
                team = {
                    "id": team[0],
                    "Name": team[1],
                    "Owner": team[2],
                    "ProfilePic": team[3]
                }
                return team
            else:
                return None
        else:
            return None

    def updateTeam(self, team: Team, teamId: int):
        if self._connectDB():
            return self._updateTeam(team, teamId)

    def updateUserTeamNone(self, ownerId: int):
        if self._connectDB():
            return self._updateUserTeamNone(ownerId)

    def deleteTeam(self, teamId: int, ownerId: int):
        if self._connectDB():
            if self._deleteTeam(teamId):
                return self.updateUserTeamNone(ownerId)
            else:
                return False
        else:
            return False

    def updateTeamProfilePic(self, filename: str, teamId: int):
        if self._connectDB():
            return self._updateTeamProfilePic(filename, teamId)

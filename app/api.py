from os import access
from fastapi import FastAPI, status, Body, Depends, File, Header, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from app.auth.auth_bearer import JWTBearer
from app.db import DB
from app.models.user import User, UserSignIn, UserUpdate
from app.models.exModels import resMess, resSignin, resUser
from app.models.team import Team
from app.auth.auth_handler import signJWT, decodeJWT
from typing import Optional
import shutil
import os

app = FastAPI(debug=False)
mydb = DB()

origins = ["172.17.0.1", "http://localhost", "http://localhost:3000",
           "http://localhost:8000", "http://localhost:8080",
           "https://localhost", "https://localhost:3000",
           "https://localhost:8000", "https://localhost:8080",
           "localhost", "localhost:3000",
           "localhost:8000", "localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allow_headers=['*'],
)


@app.get("/", tags=["root"], response_model=resMess)
async def read_root() -> dict:
    item = {"message": "WORKING !!!"}
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)


@app.post("/user/signin", tags=["user"], response_model=resSignin)
async def user_signin(user: UserSignIn = Body(...)):
    res = mydb.signinUser(user)
    if res == 1:
        return signJWT(user.Emailaddr)
    elif res == 2:
        item = {
            "message": "Signin Failed"
        }
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        item = {
            "message": "DB might be dead T.T"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)


@app.post("/user/signup", tags=["user"], response_model=resMess)
async def user_signup(user: User = Body(...)):
    res = mydb.signupUser(user)
    if res == 1:
        item = {
            "message": "Signup Success"
        }
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
    elif res == 2:
        item = {
            "message": "That Emailaddr already exist"
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=item)
    else:
        item = {
            "message": "DB might be dead T.T"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)


@app.get("/user/profilePic", dependencies=[Depends(JWTBearer())], tags=["user"])
async def user_getProfilePic(Authorization: Optional[str] = Header(None)):
    token = Authorization[7:]
    decoded = decodeJWT(token)
    dbUser = mydb.getDBUserData(decoded["Emailaddr"])
    if dbUser["ProfilePic"] is None:
        item = {
            "message": "there is no ProfilePic for User"
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=item)
    else:
        print("\033[32m" + "FILE" + "\033[0m", end=':     ')
        print("File read -> " + dbUser["ProfilePic"])
        path = "./imgs/" + dbUser["ProfilePic"]
        return FileResponse(path=path, filename=dbUser["ProfilePic"])


@app.post("/user/profilePic", dependencies=[Depends(JWTBearer())], tags=["user"])
async def user_PostProfilePic(file: UploadFile, Authorization: Optional[str] = Header(None)):
    ext = ["jpg", "JPG", "PNG", "png"]
    token = Authorization[7:]
    decoded = decodeJWT(token)
    dbFilename = mydb.getDBUserData(decoded["Emailaddr"])
    if dbFilename["ProfilePic"] is not None:
        os.remove("./imgs/" + dbFilename["ProfilePic"])
    filename = file.filename.split('.')
    if filename[len(filename) - 1] in ext:
        filename = decoded["Emailaddr"] + "." + filename[len(filename) - 1]
        f = open("./imgs/" + filename, 'wb')
        shutil.copyfileobj(file.file, f)
        f.close()
        mydb.updateUserProfilePic(filename, decoded["Emailaddr"])
        print("\033[32m" + "FILE" + "\033[0m", end=':     ')
        print("File written -> " + filename)
        item = {
            "message": "file uploaded"
        }
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
    else:
        item = {
            "message": "profilePic must .jpg or .png"
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=item)


@app.delete("/user/profilePic", dependencies=[Depends(JWTBearer())], tags=["user"])
async def user_deleteProfilePic(Authorization: Optional[str] = Header(None)):
    token = Authorization[7:]
    decoded = decodeJWT(token)
    dbFilename = mydb.getDBUserData(decoded["Emailaddr"])
    if dbFilename["ProfilePic"] is not None:
        os.remove("./imgs/" + dbFilename["ProfilePic"])
        mydb.updateUserProfilePic("NULL", decoded["Emailaddr"])
        item = {
            "message": "ProfilePic removed"
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    else:
        item = {
            "message": "there is no ProfilePic for User"
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=item)


@app.get("/user/userData", dependencies=[Depends(JWTBearer())], tags=["user"], response_model=resUser)
async def user_getUserData(Authorization: Optional[str] = Header(None)):
    token = Authorization[7:]
    decoded = decodeJWT(token)
    dbUser = mydb.getUserData(decoded["Emailaddr"])
    if dbUser is None:
        item = {
            "message": "there is no data"
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=item)
    if dbUser["Team"] is not None:
        dbUser["Team"] = str(True)
    else:
        dbUser["Team"] = str(False)
    # dbUser 확인하여 에러 처리 필요
    item = {
        "message": dbUser
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=item)


@app.put("/user/userData", dependencies=[Depends(JWTBearer())], tags=["user"], response_model=resMess)
async def user_update(Authorization: Optional[str] = Header(None), user: UserUpdate = Body(...)):
    token = Authorization[7:]
    decoded = decodeJWT(token)
    if mydb.updateUser(user, decoded["Emailaddr"]) == 1:
        item = {
            "message": "Update Success"
        }
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
    else:
        item = {
            "message": "not managed err"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)


@app.delete("/user/userData", dependencies=[Depends(JWTBearer())], tags=["user"], response_model=resMess)
async def user_delete(Authorization: Optional[str] = Header(None), user: UserSignIn = Body(...)):
    res = mydb.signinUser(user)
    token = Authorization[7:]
    decoded = decodeJWT(token)
    dbuser = mydb.getDBUserData(decoded["Emailaddr"])
    if dbuser["Team"] is not None:
        item = {
            "message": "You need to transfer or delete your team first"
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=item)

    deletion = mydb.deleteUser(decoded["Emailaddr"])

    if dbuser["ProfilePic"] is not None:
        os.remove("./imgs/" + dbuser["ProfilePic"])

    if not deletion:
        item = {
            "message": "DB might be dead T.T"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)
    if res == 1:
        item = {
            "message": "Thank you for using our service bye bye..."
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    elif res == 2:
        item = {
            "message": "Data does not match"
        }
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        item = {
            "message": "DB might be dead T.T"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)


@app.get("/team", dependencies=[Depends(JWTBearer())], tags=["team"], response_model=resMess)
async def team_getTeam(Authorization: Optional[str] = Header(None)):
    token = Authorization[7:]
    decoded = decodeJWT(token)
    dbuser = mydb.getDBUserData(decoded["Emailaddr"])
    dbteam = mydb.getTeambyId(dbuser["Team"])
    if dbteam is not None:
        dbteam = {
            "Name": dbteam["Name"],
            "Owner": dbuser["Name"],
            "ProfilePic": str(True) if dbteam["ProfilePic"] is not None else str(False)
        }
        item = {
            "message": dbteam
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    item = {
        "message": "there is no team with you"
    }
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=item)


@app.post("/team", dependencies=[Depends(JWTBearer())], tags=["team"], response_model=resMess)
async def team_postTeam(Authorization: Optional[str] = Header(None), team: Team = Body(...)):
    token = Authorization[7:]
    decoded = decodeJWT(token)
    dbuser = mydb.getDBUserData(decoded["Emailaddr"])
    team.Owner = dbuser["id"]
    if dbuser["Team"] is not None:
        item = {
            "message": "you have team already"
        }
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=item)
    if mydb.createTeam(team):
        dbteam = mydb.getTeambyOwnerId(dbuser["id"])
        if mydb.updateUserTeam(dbuser["id"], dbteam["id"]):
            item = {
                "message": "Team created you are owner of the team"
            }
            return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
        else:
            item = {
                "message": "DB might be dead T.T"
            }
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)
    else:
        item = {
            "message": "DB might be dead T.T"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)


@app.put("/team", dependencies=[Depends(JWTBearer())], tags=["team"], response_model=resMess)
async def team_putTeam(Authorization: Optional[str] = Header(None), team: Team = Body(...)):
    return


@app.delete("/team", dependencies=[Depends(JWTBearer())], tags=["team"], response_model=resMess)
async def team_deleteTeam(Authorization: Optional[str] = Header(None), team: Team = Body(...)):
    return


@app.get("/team/profilePic", dependencies=[Depends(JWTBearer())], tags=["team"], response_model=resMess)
async def team_getProfilePic(Authorization: Optional[str] = Header(None), team: Team = Body(...)):
    return


@app.post("/team/profilePic", dependencies=[Depends(JWTBearer())], tags=["team"], response_model=resMess)
async def team_postProfilePic(Authorization: Optional[str] = Header(None), team: Team = Body(...)):
    return


@app.get("/team/member", dependencies=[Depends(JWTBearer())], tags=["team"], response_model=resMess)
async def team_getMember(Authorization: Optional[str] = Header(None)):
    return


@app.post("/team/member", dependencies=[Depends(JWTBearer())], tags=["team"], response_model=resMess)
async def team_addMember(Authorization: Optional[str] = Header(None)):
    return


@app.delete("/team/member", dependencies=[Depends(JWTBearer())], tags=["team"], response_model=resMess)
async def team_deleteMember(Authorization: Optional[str] = Header(None)):
    return


@app.post("/project/create", dependencies=[Depends(JWTBearer())], tags=["project"], response_model=resMess)
async def team_postTeam(Authorization: Optional[str] = Header(None), team: Team = Body(...)):
    return


@app.put("/project/update", dependencies=[Depends(JWTBearer())], tags=["project"], response_model=resMess)
async def team_putTeam(Authorization: Optional[str] = Header(None), team: Team = Body(...)):
    return


@app.delete("/project/delete", dependencies=[Depends(JWTBearer())], tags=["project"], response_model=resMess)
async def team_deleteTeam(Authorization: Optional[str] = Header(None), team: Team = Body(...)):
    return


@app.post("/object/create", dependencies=[Depends(JWTBearer())], tags=["object"], response_model=resMess)
async def team_postTeam(Authorization: Optional[str] = Header(None), team: Team = Body(...)):
    return


@app.put("/object/update", dependencies=[Depends(JWTBearer())], tags=["object"], response_model=resMess)
async def team_putTeam(Authorization: Optional[str] = Header(None), team: Team = Body(...)):
    return


@app.delete("/object/delete", dependencies=[Depends(JWTBearer())], tags=["object"], response_model=resMess)
async def team_deleteTeam(Authorization: Optional[str] = Header(None), team: Team = Body(...)):
    return


@app.get("/TEST/DB/DROPTABLE", tags=["TEST"], response_model=resMess)
async def test_DropTable():
    if mydb.WarnTestDelAllTableData():
        item = {
            "message": "All tables DROPED and CREATED"
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=item)
    else:
        item = {
            "message": "Internal server error"
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=item)
